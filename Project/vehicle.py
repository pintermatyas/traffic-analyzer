import numpy as np


class Vehicle:
    def __init__(self, class_id, pos_x, pos_y, width, height, img, highest_id):
        self.id = None
        self.class_id = class_id  # Class id of vehicle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.img = img
        self.highest_id = highest_id

    def track_vehicle(self, vehicles):
        image_width, image_height = self.img.shape[0], self.img.shape[1]

        x_threshold = image_width // 10
        y_threshold = image_height // 5
        closest_vehicle = self.find_closest(vehicles)[0]
        if self.in_range(closest_vehicle.pos_x, closest_vehicle.pos_y, x_threshold, y_threshold):
            self.id = closest_vehicle.id
            vehicles.remove(closest_vehicle)
        else:
            self.id = self.highest_id

    def in_range(self, pos_x, pos_y):
        image_width, image_height = self.img.shape[1], self.img.shape[0]
        x_threshold = image_width // 30
        y_threshold = image_height // 10
        if pos_x + x_threshold >= self.pos_x >= pos_x - x_threshold:
            if pos_y + y_threshold >= self.pos_y >= pos_y - y_threshold:
                return True
        return False

    def find_closest(self, vehicles):
        smallest_distance_vehicle = vehicles[0]
        smallest_distance = 99999999.99
        for v in vehicles:
            dist = np.sqrt(pow((self.pos_x - v.pos_x), 2) + pow((self.pos_y - v.pos_y), 2))
            if smallest_distance > dist:
                smallest_distance_vehicle = v
                smallest_distance = dist
        return [smallest_distance_vehicle, smallest_distance]
