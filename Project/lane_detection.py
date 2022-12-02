import cv2
import numpy as np


def lanes_detection(input_image, output_image):
    height = input_image.shape[0]
    width = input_image.shape[1]

    # set the shape we want to be looking at
    region_of_interest_vertices = [(0, height), (0, 3 * height / 8), (width, 3 * height / 8), (width, height)]

    # filters on image
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    sobel_image = cv2.Sobel(src=gray_image, ddepth=cv2.CV_8UC1, dx=1, dy=1, ksize=1)
    canny_image = cv2.Canny(sobel_image, 50, 100, apertureSize=3)

    # Crop the region of interest
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))

    # Create lines with edge detection
    lines = cv2.HoughLinesP(cropped_image, rho=1, theta=np.pi / 180,
                            threshold=150, lines=np.array([]), minLineLength=200, maxLineGap=80)

    usable_lines = []

    if lines is not None:
        for line_iter in lines:
            l = line_iter[0]
            start_x, start_y, end_x, end_y = l[0], l[1], l[2], l[3]
            line_length = abs(np.sqrt(np.power(start_x - end_x, 2) + np.power(start_y - end_y, 2)))
            if intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2]) is not False:
                if start_y < height / 2:
                    l[0], l[1] = \
                        intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2])
                if end_y < height / 2:
                    l[2], l[3] = \
                        intersect_lines([start_x, start_y, end_x, end_y], [0, height // 2, width, height // 2])
            if np.abs(end_x - start_x) < 1.8 * np.abs(end_y - start_y):
                usable_lines.append(l)

    bounding_lines = get_bounding_lines(usable_lines, output_image)

    image_with_lines = draw_lines(output_image, bounding_lines)

    return image_with_lines, bounding_lines


def get_bounding_lines(lines, output_image):
    height = output_image.shape[0]
    width = output_image.shape[1]
    lines_ending_on_border = []
    for l in lines:
        if l[1] == height // 2 or l[3] == height // 2:
            if l[3] == height // 2:
                l[0], l[1], l[2], l[3] = l[2], l[3], l[0], l[1]
            lines_ending_on_border.append(l)

    different_lines = get_different_lines(lines_ending_on_border, output_image)

    return different_lines


def get_different_lines(lines, output_image):
    height = output_image.shape[0]
    width = output_image.shape[1]
    check_interval = 80
    width_interval = range(0, width, check_interval)
    different_lines = []
    for x_interval in width_interval:
        similar_ending_lines = []
        similar_ending_lines_length = []
        for l in lines:
            if x_interval - int(3 * check_interval / 4 - 1) < l[0] < x_interval + int(3 * check_interval / 4 - 1):
                similar_ending_lines.append(l)
                similar_ending_lines_length.append(get_length_of_line(l))
        if len(similar_ending_lines) > 0:
            longest_index = similar_ending_lines_length.index(max(similar_ending_lines_length))
            different_lines.append(similar_ending_lines[longest_index])

    return different_lines


def get_best_lines(lines, threshold):
    best_lines = []
    for l1 in lines:
        for l2 in lines:
            if l1[0] - threshold < l2[0] < l1[0] + threshold:
                best_line = choose_longest_line(l1, l2)
                best_lines.append(best_line)
    return best_lines


def get_length_of_line(line):
    line_length = abs(np.sqrt(np.power(line[0] - line[2], 2) + np.power(line[1] - line[3], 2)))
    return line_length


def choose_longest_line(line1, line2):
    if get_length_of_line(line1) < get_length_of_line(line2):
        return line2
    return line1


def intersect_lines(line1, line2):
    x1, y1, x2, y2 = line1[0], line1[1], line1[2], line1[3]
    x3, y3, x4, y4 = line2[0], line2[1], line2[2], line2[3]

    div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    # To prevent later dividing by (close to) zero
    if abs(div) < 0.005:
        return False

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
    u = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x1 - x2)) / div

    t = round_from_inf(t)
    u = round_from_inf(u)

    if abs(t) <= 1 and abs(u) <= 1:
        if t is not float("nan"):
            intersect_x, intersect_y = int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1))
            return intersect_x, intersect_y
    else:
        return False


def round_from_inf(f):
    if f in [float("-inf"), float("inf")]:
        return float("nan")
    return f


def region_of_interest(input_image, vertices):
    mask = np.zeros_like(input_image)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(input_image, mask)
    return masked_image


def draw_lines(output_image, lines):
    output_image = np.copy(output_image)
    blank_image = np.zeros((output_image.shape[0], output_image.shape[1], 3), np.uint8)

    for l in lines:
        x1, y1, x2, y2 = l[0], l[1], l[2], l[3]
        cv2.line(blank_image, (x1, y1), (x2, y2), (204, 12, 201), 8)

    height = output_image.shape[0]
    width = output_image.shape[1]

    # cv2.line(blank_image, (0, 3 * height // 4 - 20), (width, 3 * height // 4 - 20), (0, 0, 255), 4)
    # cv2.line(blank_image, (0, 3 * height // 4 - 120), (width, 3 * height // 4 - 120), (0, 0, 255), 4)

    # cv2.line(blank_image, (0, height // 2), (width, height // 2), (0, 0, 255), 2)

    output_image = cv2.addWeighted(output_image, 0.8, blank_image, 1, 0.0)
    return output_image
