import cv2
import numpy as np


def calculate_speed(current_vehicle, previous_frame_vehicle, cap):
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Width of vehicle is approx. 2 m
    vehicle_width = 2
    curr_x, curr_y = current_vehicle.pos_x, current_vehicle.pos_y
    curr_w, curr_h = current_vehicle.width, current_vehicle.height
    prev_x, prev_y = previous_frame_vehicle.pos_x, previous_frame_vehicle.pos_y
    prev_w, prev_h = previous_frame_vehicle.width, previous_frame_vehicle.height

    if curr_y < frame_height / 2:
        vehicle_width = 2 + (frame_height / 2 - curr_y) / (frame_height / 2) * 2

    framerate = cap.get(cv2.CAP_PROP_FPS)
    frame_elapsed_time = 1 / framerate
    distance_from_previous_frame = abs(np.sqrt(np.power(curr_x + curr_w / 2 - prev_x + prev_w / 2, 2) +
                                               np.power(curr_y + curr_h / 2 - prev_y + prev_h / 2, 2)))
    distance_in_meters = distance_from_previous_frame * vehicle_width / curr_w
    vel = distance_in_meters / frame_elapsed_time
    current_vehicle.velocity = int(vel)
