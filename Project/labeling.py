import cv2


def label_vehicles(indexes, vehicles, image, imgPlot):
    for i in indexes:
        vehicle = vehicles[int(i)]
        x, y, w, h = vehicle.pos_x, vehicle.pos_y, vehicle.width, vehicle.height
        if vehicle.dir == 0:
            # dir_string = "Approaching"
            color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            # cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        elif vehicle.dir == 1:
            # dir_string = "Going away"
            color = (255, 0, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            # cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        elif vehicle.dir is None:
            # dir_string = "N/A"
            color = (255, 255, 255)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            # cv2.putText(image, f'{dir_string}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2)
        cv2.putText(image, f'id: {vehicle.id}', (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(image, f'{vehicle.velocity} km/h', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        # imgPlot = cv2.circle(imgPlot, (int(x+w/2), int(y+h/2)), radius=8, color=(255, 255, 255), thickness=-1)

