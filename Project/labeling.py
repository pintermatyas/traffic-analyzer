import cv2


def label_vehicles(indexes, bounding_boxes, vehicles, image):
    for i in indexes:
        box = bounding_boxes[i]
        vehicle = vehicles[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        if vehicle.dir == 0:
            dir_string = "Approaching"
            color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        elif vehicle.dir == 1:
            dir_string = "Going away"
            color = (255, 0, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        elif vehicle.dir is None:
            dir_string = "N/A"
            color = (255, 255, 255)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)
        cv2.putText(image, f'id: {vehicle.id}', (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(image, f'{vehicle.velocity} km/h', (x, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
