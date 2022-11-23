import cv2
import numpy as np
from lane_detection import intersect_lines


def calculate_speed(current_vehicle, previous_frame_vehicle, cap, lines):
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # Width of vehicle is approx. 2 m
    avg_vehicle_width = 2
    avg_lane_width = 3.5


    convert_to_kph = 3.6
    current_x, current_y = current_vehicle.pos_x, current_vehicle.pos_y
    current_width_in_pixels, current_height = current_vehicle.width, current_vehicle.height
    prev_frame_x, prev_frame_y = previous_frame_vehicle.pos_x, previous_frame_vehicle.pos_y
    prev_frame_width, prev_frame_height = previous_frame_vehicle.width, previous_frame_vehicle.height

    if current_y + current_height < 3 * FRAME_HEIGHT // 4:
        angle_offset = 3.2 + 2 * (1-(current_y - 3*FRAME_HEIGHT//4)/(3*FRAME_HEIGHT//4))
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
    road_width_in_meters = number_of_lanes * avg_lane_width
    framerate = cap.get(cv2.CAP_PROP_FPS)
    frame_elapsed_time = 1 / framerate
    d1 = current_x - prev_frame_x
    d2 = current_y - prev_frame_y
    distance_from_previous_frame = np.sqrt(np.power(d1, 2) + np.power(d2, 2))
    car_width = road_width_in_meters * current_width_in_pixels / road_width_in_pixels
    distance_in_meters = distance_from_previous_frame * car_width / current_width_in_pixels
    vel = distance_in_meters * angle_offset * convert_to_kph / frame_elapsed_time

    if vel < 140:
        current_vehicle.velocity = (int(vel)//10) * 10
    elif vel < 180:
        current_vehicle.velocity = 140
    else:
        current_vehicle.velocity = "N/A"

    if (current_x, current_y) == (prev_frame_x, prev_frame_y):
        current_vehicle.velocity = previous_frame_vehicle.velocity


def get_number_of_lanes(vehicle, lines, cap):
    FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    current_x, current_y = vehicle.pos_x, vehicle.pos_y
    current_width, current_height = vehicle.width, vehicle.height
    intersecting_line = [0, current_y, FRAME_WIDTH, current_y]
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
