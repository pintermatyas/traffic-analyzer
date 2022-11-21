import cv2
import numpy as np


def calculate_speed(current_vehicle, previous_frame_vehicle, cap):
    # Width of vehicle is approx. 2 m
    avg_vehicle_width = 2
    convert_to_kph = 3.6
    current_x, current_y = current_vehicle.pos_x, current_vehicle.pos_y
    current_width, current_height = current_vehicle.width, current_vehicle.height
    prev_frame_x, prev_frame_y = previous_frame_vehicle.pos_x, previous_frame_vehicle.pos_y
    prev_frame_width, prev_frame_height = previous_frame_vehicle.width, previous_frame_vehicle.height

    framerate = cap.get(cv2.CAP_PROP_FPS)
    frame_elapsed_time = 1 / framerate
    d1 = (current_x + current_width / 2) - (prev_frame_x + prev_frame_width / 2)
    d2 = (current_y + current_height / 2) - (prev_frame_y + prev_frame_height / 2)
    distance_from_previous_frame = abs(np.sqrt(np.power(d1, 2) + np.power(d2, 2)))
    distance_in_meters = distance_from_previous_frame * avg_vehicle_width / current_width
    vel = distance_in_meters * convert_to_kph / frame_elapsed_time

    current_vehicle.velocity = int(vel)

    if (current_x, current_y) == (prev_frame_x, prev_frame_y):
        current_vehicle.velocity = previous_frame_vehicle.velocity
