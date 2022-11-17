import numpy as np


class Vehicle:
    def __init__(self, class_id, pos_x, pos_y, width, height, img, highest_id):
        self.id = ""
        self.class_id = class_id  # Class id of vehicle
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.img = img
        self.highest_id = highest_id
        self.dir = None
        self.velocity = 0
        self.predicted = [None, None]
        self.age = 0

    def track_vehicle(self, vehicles):
        image_width, image_height = self.img.shape[0], self.img.shape[1]

        for v in vehicles:
            if self.in_range(v.predicted[0], v.predicted[1], v.width, v.height):
                self.predict_movement(prev_frame=v)
                self.id = v.id
                self.age = v.age + 1
                return

        x_threshold = image_width // 10
        y_threshold = image_height // 5
        closest_vehicle = self.find_closest(vehicles)[0]
        if self.in_range(closest_vehicle.pos_x, closest_vehicle.pos_y, closest_vehicle.width/2, closest_vehicle.height/2):
            self.id = closest_vehicle.id
            self.age = closest_vehicle.age + 1
            self.predict_movement(prev_frame=closest_vehicle)
            vehicles.remove(closest_vehicle)
        else:
            self.id = self.highest_id

    def in_range(self, pos_x, pos_y, x_threshold, y_threshold):
        # image_width, image_height = self.img.shape[1], self.img.shape[0]
        # x_threshold = image_width // 30
        # y_threshold = image_height // 10
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

        if self.pos_y - smallest_distance_vehicle.pos_y > 0:
            self.dir = 0
        elif self.pos_y - smallest_distance_vehicle.pos_y < 0:
            self.dir = 1
        else:
            self.dir = smallest_distance_vehicle.dir
        return [smallest_distance_vehicle, smallest_distance]

    def predict_movement(self, prev_frame):
        x_movement = self.pos_x - prev_frame.pos_x
        y_movement = self.pos_y - prev_frame.pos_y
        self.predicted = [self.pos_x + x_movement, self.pos_y + y_movement]
