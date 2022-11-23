import cv2
import numpy as np


def lanes_detection(input_image, output_image):
    height = input_image.shape[0]
    width = input_image.shape[1]

    region_of_interest_vertices = [(0, height), (0, 3 * height / 8), (width, 3 * height / 8), (width, height)]

    # filters on image
    gray = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(src=gray, ddepth=cv2.CV_8UC1, dx=1, dy=1, ksize=1)
    canny = cv2.Canny(sobelx, 50, 100, apertureSize=3)

    cropped_image = region_of_interest(canny, np.array([region_of_interest_vertices], np.int32))

    lines = cv2.HoughLinesP(cropped_image, rho=1, theta=np.pi / 180,
                            threshold=150, lines=np.array([]), minLineLength=200, maxLineGap=80)

    usable_lines = []

    if lines is not None:
        for line_iter in lines:
            l = line_iter[0]
            start_x, start_y, end_x, end_y = l[0], l[1], l[2], l[3]
            line_length = abs(np.sqrt(np.power(start_x - end_x, 2) + np.power(start_y - end_y, 2)))
            if intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2]) is not False:
                if start_y < height/2:
                    l[0], l[1] = \
                        intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2])
                if end_y < height/2:
                    l[2], l[3] = \
                        intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2])
            if np.abs(end_x - start_x) < 1.8 * np.abs(end_y - start_y):
                usable_lines.append(l)

    image_with_lines = draw_lines(output_image, usable_lines)

    return image_with_lines


def intersect_lines(line1, line2):
    x1, y1, x2, y2 = line1[0], line1[1], line1[2], line1[3]
    x3, y3, x4, y4 = line2[0], line2[1], line2[2], line2[3]

    div = (x1-x2)*(y3-y4) - (y1-y2) * (x3-x4)
    if abs(div) < 0.005:
        return False

    t = ((x1-x3)*(y3-y4) - (y1-y3) * (x3-x4)) / div
    u = ((x1-x3)*(y3-y4) - (y1-y3) * (x1-x2)) / div

    t = round_from_inf(t)
    u = round_from_inf(u)

    if abs(t)<=1 and abs(u)<=1:
        if t is not float("nan"):
            px, py = int(x1+t*(x2-x1)), int(y1 + t*(y2-y1))
            return px, py
    else:
        return False


def round_from_inf(x):
    if x in [float("-inf"),float("inf")]:
        return float("nan")
    return x


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

    height = img.shape[0]
    width = img.shape[1]

    # cv2.line(blank_image, (0, height // 2), (width, height // 2), (0, 0, 255), 2)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img
