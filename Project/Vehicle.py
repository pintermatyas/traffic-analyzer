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
        x_threshold = image_width // 30
        y_threshold = image_height // 15
        for v in vehicles:
            if self.class_id == v.class_id:
                if self.in_range(v.pos_x, v.pos_y, x_threshold, y_threshold):
                    self.id = v.id
                    break

    def in_range(self, pos_x, pos_y, x_threshold, y_threshold):
        if self.pos_x <= pos_x + x_threshold & self.pos_x >= pos_x - x_threshold:
            if self.pos_y <= pos_y + y_threshold & self.pos_y >= pos_y - y_threshold:
                return True
        return False
