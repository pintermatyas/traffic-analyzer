import cv2
import numpy as np


def lanes_detection(input_image, output_image):
    height = input_image.shape[0]
    width = input_image.shape[1]

    region_of_interest_vertices = [(0, height), (0, 3 * height / 8), (width, 3 * height / 8), (width, height)]

    #filters on image
    gray = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(src=gray, ddepth=cv2.CV_8UC1, dx=1, dy=1, ksize=1)
    canny = cv2.Canny(sobelx, 50, 100, apertureSize=3)

    cropped_image = region_of_interest(canny, np.array([region_of_interest_vertices], np.int32))

    lines = cv2.HoughLinesP(cropped_image, rho=1.5, theta=np.pi / 180,
                            threshold=150, lines=np.array([]), minLineLength=100, maxLineGap=80)

    usable_lines = []

    if lines is not None:
        for line_iter in lines:
            l = line_iter[0]
            start_x, start_y, end_x, end_y = l[0], l[1], l[2], l[3]
            if np.abs(end_x - start_x) < 1.8 * np.abs(end_y - start_y):
                usable_lines.append(l)

    image_with_lines = draw_lines(output_image, usable_lines)

    return image_with_lines


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines):
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    for l in lines:
        x1, y1, x2, y2 = l[0], l[1], l[2], l[3]
        cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img
