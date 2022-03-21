from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError

from .models import Document
from .serializers import DocumentSerializer

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import numpy as np
import cv2
# import IMG


# convert file to images
def convert_to_images(file):

    images = convert_from_path(file)

    for i, image in enumerate(images):
        name = "page" + str(i) + ".png"
        image.save(name, "PNG")  # find a way to save to s3 instead of locally


# clean up image
def process_image(image):

    img = image.getOpenCVptr()

    # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
    img_copy = img.copy()

    # rescale image, may or may not need this
    # img_copy = cv2.resize(img_copy, None, fx=1.5, f=1.5, interpolation=cv2.INTER_CUBIC)

    # convert to grayscale
    gray_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # blur edges
    blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # binarization - apply threshold for black and white image
    thresh_img = cv2.threshold(blur_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # thresh_img = cv2.adaptiveThreshold(blur_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # dilate to remove noise
    # larger kernel on x axis to merge characters into one line, smaller on y axis to separate blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,5))
    dilate_img = cv2.dilate(thresh_img, kernel, iterations=5)

    # find the contours
    contours, hierarchy = cv2.findContours(dilate_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # get largest contour and surround in min box area
    largest_contour = contours[0]
    minAreaReact = cv2.minAreaRect(largest_contour)

    # get angle
    angle = minAreaReact[-1]
    if angle < -45:
        angle = 90 + angle
    skew_angle = -1.0 * angle

    # rotate the image
    final_img = img.copy()
    (h, w) = final_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, (skew_angle * -1.0), 1.0)
    final_img = cv2.warpAffine(final_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return final_img


# Create your views here.
class DocumentView(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )
                              # SessionAuthentication)

    # basically returns the document list
    queryset = Document.objects.all()

    model = Document
    serializer_class = DocumentSerializer

    @api_view(['GET'])
    def ApiOverview(self, request):
        api_urls = {
            'all_docs': '/',
            'Add': '/add',
            'Delete': '/doc/delete/pk'
        }
        return Response(api_urls)

    @api_view(['POST'])
    def add_doc(request):
        doc = DocumentSerializer(data=request.data)
        if doc.is_valid():
            doc.save()
            return Response(doc.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_docs(request):

        print(request.user.id)

        docs = Document.objects.filter(owner_id=request.user.id)
        print(docs.count())

        if docs:
            serializer = DocumentSerializer(docs, many=True)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['DELETE'])
    def delete_doc(request, pk):
        doc = get_object_or_404(Document, pk=pk)
        doc.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
