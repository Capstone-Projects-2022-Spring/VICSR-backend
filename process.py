import argparse

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import numpy as np
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])


def get_skew_angle(image):

    cv2.imshow("original", image)
    cv2.waitKey(0)

    # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
    img_copy = image.copy()

    # convert to grayscale
    gray_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    # blur edges
    blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # binarization - apply threshold for black and white image
    thresh_img = cv2.threshold(blur_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # dilate to remove noise
    # larger kernel on x axis to merge characters into one line, smaller on y axis to separate blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
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
    return skew_angle


# rotate the image
def rotate_image(angle):
    straight_img = img.copy()
    (h, w) = straight_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, (angle * -1.0), 1.0)
    straight_img = cv2.warpAffine(straight_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return straight_img


skew = get_skew_angle(img)
if skew != -90.0:
    final_img = rotate_image(skew)
else:
    final_img = img


cv2.imshow("final", final_img)
cv2.waitKey(0)

