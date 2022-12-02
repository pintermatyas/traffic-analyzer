import cv2
import numpy as np
from lane_detection import intersect_lines

# Coming from top to bottom
passed_through_top_gate_id = []
passed_through_top_gate_frame_num = []

# Coming from bottom to top
passed_through_bottom_gate_id = []
passed_through_bottom_gate_frame_num = []


def calculate_speed_with_control_lines(current_vehicle, previous_frame_vehicle, cap, frame_num):
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    framerate = cap.get(cv2.CAP_PROP_FPS)

    # Bottom control line
    control_line1_y = 3 * FRAME_HEIGHT // 4 - 20
    # Top control line
    control_line2_y = 3 * FRAME_HEIGHT // 4 - 120

    dist_between_control_lines = 21.36

    control_pos_current_vehicle = current_vehicle.pos_y + current_vehicle.height
    control_pos_prev_vehicle = previous_frame_vehicle.pos_y + previous_frame_vehicle.height

    if current_vehicle.id in passed_through_top_gate_id and current_vehicle.id in passed_through_bottom_gate_id:
        index_top = passed_through_top_gate_id.index(current_vehicle.id)
        index_bot = passed_through_bottom_gate_id.index(current_vehicle.id)
        frame_difference = passed_through_bottom_gate_frame_num[index_bot] - passed_through_top_gate_frame_num[
            index_top]
        elapsed_time_second = abs(frame_difference) * 1 / framerate

        speed = 3.6 * dist_between_control_lines / elapsed_time_second
        current_vehicle.velocity = int(speed)

    if control_pos_current_vehicle < control_line1_y <= control_pos_prev_vehicle \
            or control_pos_current_vehicle >= control_line1_y > control_pos_prev_vehicle:
        if current_vehicle.id not in passed_through_bottom_gate_id:
            passed_through_bottom_gate_id.append(current_vehicle.id)
            passed_through_bottom_gate_frame_num.append(frame_num)
        else:
            index = passed_through_bottom_gate_id.index(current_vehicle.id)
            passed_through_bottom_gate_frame_num[index] = frame_num

    if control_pos_current_vehicle < control_line2_y <= control_pos_prev_vehicle \
            or control_pos_current_vehicle >= control_line2_y > control_pos_prev_vehicle:
        if current_vehicle.id not in passed_through_top_gate_id:
            passed_through_top_gate_id.append(current_vehicle.id)
            passed_through_top_gate_frame_num.append(frame_num)
        else:
            index = passed_through_top_gate_id.index(current_vehicle.id)
            passed_through_top_gate_frame_num[index] = frame_num


def calculate_speed(current_vehicle, previous_frame_vehicle, cap, lines):
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    cv2.line(cap.read()[1], (0, FRAME_HEIGHT // 4), (FRAME_WIDTH, FRAME_HEIGHT // 4), (204, 12, 201), 8)

    # Width of vehicle is approx. 2 m
    avg_vehicle_width = 2
    avg_lane_width = 3.5

    convert_to_kph = 3.6
    current_x, current_y = current_vehicle.pos_x, current_vehicle.pos_y
    current_width_in_pixels, current_height = current_vehicle.width, current_vehicle.height
    # prev_frame_x, prev_frame_y = previous_frame_vehicle.pos_x, previous_frame_vehicle.pos_y
    # prev_frame_width, prev_frame_height = previous_frame_vehicle.width, previous_frame_vehicle.height
    first_frame_x, first_frame_y, first_frame_width, first_frame_height = current_vehicle.first_pos
    # prev_frame_width, prev_frame_height = previous_frame_vehicle.width, previous_frame_vehicle.height

    if current_y + current_height < 3 * FRAME_HEIGHT // 4:
        angle_offset = 3.2 + 1.2 * (1 - (current_y - 3 * FRAME_HEIGHT // 4) / (3 * FRAME_HEIGHT // 4))
    else:
        angle_offset = 3.2

    intersecting_line = [0, current_y, FRAME_WIDTH, current_y]
    intersect_points = []
    for l in lines:
        intersect_points.append(intersect_lines(l, intersecting_line))
    closest_intersection_points = find_closest_points(current_vehicle, intersect_points)
    if not closest_intersection_points:
        current_vehicle.velocity = "N/A"
        return None

    road_width_in_pixels = abs(closest_intersection_points[0][0] - closest_intersection_points[1][0])

    number_of_lanes = get_number_of_lanes(current_vehicle, lines, cap)
    if number_of_lanes is None:
        current_vehicle.velocity = "N/A"
        return None

    road_width_in_meters = number_of_lanes * avg_lane_width
    framerate = cap.get(cv2.CAP_PROP_FPS)
    frame_elapsed_time = 1 / framerate
    d1 = current_x - first_frame_x
    d2 = current_y - first_frame_y
    distance_from_previous_frame = np.sqrt(np.power(d1, 2) + np.power(d2, 2))
    car_width = road_width_in_meters * current_width_in_pixels / road_width_in_pixels
    distance_in_meters = distance_from_previous_frame * car_width / current_width_in_pixels
    distance_in_meters /= current_vehicle.age
    vel = distance_in_meters * angle_offset * convert_to_kph / frame_elapsed_time

    if vel == float("nan"):
        current_vehicle.velocity = "N/A"
    else:
        if vel < 150:
            current_vehicle.velocity = (int(vel))
        # elif vel < 180:
        #     current_vehicle.velocity = 140
        else:
            current_vehicle.velocity = "N/A"

        if (current_x, current_y) == (first_frame_x, first_frame_y):
            current_vehicle.velocity = previous_frame_vehicle.velocity


def get_number_of_lanes(vehicle, lines, cap):
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    current_x, current_y = vehicle.pos_x, vehicle.pos_y
    current_width, current_height = vehicle.width, vehicle.height
    intersecting_line = [0, current_y - current_height / 2, FRAME_WIDTH, current_y - current_height / 2]
    intersect_points = []
    for l in lines:
        intersect_points.append(intersect_lines(l, intersecting_line))

    closest_points = find_closest_points(vehicle, intersect_points)
    if closest_points is False:
        return None
    width = abs(closest_points[0][0] - closest_points[1][0])

    if vehicle.class_id in [5, 7]:
        return width // current_width + 1
    return width // current_width


def find_closest_points(vehicle, points):
    to_left = []
    to_right = []
    vehicle_x = vehicle.pos_x + vehicle.width
    for p in points:
        if p is not False:
            if vehicle_x < p[0]:
                to_right.append(p)
            else:
                to_left.append(p)

    if len(to_left) == 0 or len(to_right) == 0:
        return False

    closest_left = to_left[0]
    closest_right = to_right[0]

    for l in to_left:
        if abs(l[0] - vehicle_x) < abs(closest_left[0] - vehicle_x):
            closest_left = l

    for r in to_right:
        if abs(r[0] - vehicle_x) > abs(closest_right[0] - vehicle_x):
            closest_right = r
    return [closest_left, closest_right]
