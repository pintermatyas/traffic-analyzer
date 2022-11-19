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

        closest_vehicle = self.find_closest(vehicles)[0]
        if self.in_range(closest_vehicle.pos_x, closest_vehicle.pos_y, closest_vehicle.width / 2,
                         closest_vehicle.height / 2):
            self.id = closest_vehicle.id
            self.age = closest_vehicle.age + 1
            vehicles.remove(closest_vehicle)
        else:
            self.id = self.highest_id

    def in_range(self, pos_x, pos_y, x_threshold, y_threshold):
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

        if smallest_distance_vehicle.in_range(self.pos_x, self.pos_y, self.width / 2, self.height / 2):
            self.dir = smallest_distance_vehicle.dir

            # if self.dir is None:
            if self.pos_y + self.height/2 > smallest_distance_vehicle.pos_y + smallest_distance_vehicle.height/2:
                self.dir = 0
            elif self.pos_y + self.height/2 < smallest_distance_vehicle.pos_y + smallest_distance_vehicle.height/2:
                self.dir = 1
            else:
                self.dir = smallest_distance_vehicle.dir

        else:
            self.dir = None
        return [smallest_distance_vehicle, smallest_distance]

    # Calculates the approximate location of a vehicle in case of a missed frame
    def predict_movement(self, prev_frame):
        x_movement = self.pos_x - prev_frame.pos_x
        y_movement = self.pos_y - prev_frame.pos_y
        self.predicted = [self.pos_x + 2 * x_movement, self.pos_y + 2 * y_movement]
