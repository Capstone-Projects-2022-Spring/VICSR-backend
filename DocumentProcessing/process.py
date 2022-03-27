import argparse

import numpy

try:
    from PIL import Image  # PIL is the pillow
except ImportError:
    import Image
import cv2

def get_skew_angle(image):
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
def rotate_image(angle, img):
    straight_img = img.copy()
    (h, w) = straight_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, (angle * -1.0), 1.0)
    straight_img = cv2.warpAffine(straight_img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return straight_img

def reduce_noise(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    denoised_img = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    return denoised_img




def preprocess(image):
    #input is PIL Image -> convert to CV image format
    img =cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

    skew = get_skew_angle(img)
    if skew != -90.0:
        new_img = rotate_image(skew, img)
    else:
        new_img = img
    new_img = reduce_noise(new_img)

    ##after processing -> return to PIL Image and return
    new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    final_image = Image.fromarray(new_img)

    return final_image

