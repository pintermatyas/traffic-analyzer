import cv2
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from vehicle import Vehicle

# If you want to save the output video every time you run the script, set it to False
# Else set it to True
SAVE_VIDEO = True

now = datetime.now()
DATE_STRING = now.strftime("%Y-%m-%d-%H-%M-%S")

INPUT_FILE_NAME = 'sample2.mp4'
INPUT_FILE_PATH = 'input/' + INPUT_FILE_NAME
OUTPUT_FILE_NAME = DATE_STRING + '.mp4'
OUTPUT_FILE_PATH = 'output/' + OUTPUT_FILE_NAME
MODEL_FILE_PATH = 'C:/Egyetem/5.felev/Temalab/yolov3-608.weights'
CLASSES_FILE_PATH = 'configfiles/coco.names'

cap = cv2.VideoCapture(INPUT_FILE_PATH)
FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
if SAVE_VIDEO:
    OUT = cv2.VideoWriter(OUTPUT_FILE_PATH, fourcc, 30, (FRAME_WIDTH, FRAME_HEIGHT))

# car, motorbike, bus, truck
ACCEPTED_CLASS_IDS = [2, 3, 5, 7]

YOLO_RES = 608
CONF_THRESHOLD = 0.5
NMS_THRESHOLD = 0.3

CLASS_NAMES = []

with open(CLASSES_FILE_PATH, 'rt') as f:
    CLASS_NAMES = f.read().rstrip('\n').split('\n')

MODEL_CONFIGURATION = 'configfiles/yolov3.cfg'
MODEL_WEIGHTS = MODEL_FILE_PATH

net = cv2.dnn.readNetFromDarknet(MODEL_CONFIGURATION, MODEL_WEIGHTS)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

previous_frame_vehicles = []
highest_id = 0

MAX_DETECTION_HEIGHT = FRAME_HEIGHT//2


def calculate_speed(current_vehicle, previous_frame_vehicle):
    # Width of vehicle is approx. 2 m
    vehicle_width = 2
    curr_x, curr_y = current_vehicle.pos_x, current_vehicle.pos_y
    curr_w, curr_h = current_vehicle.width, current_vehicle.height
    prev_x, prev_y = previous_frame_vehicle.pos_x, previous_frame_vehicle.pos_y
    prev_w, prev_h = previous_frame_vehicle.width, previous_frame_vehicle.height

    if curr_y < FRAME_HEIGHT/2:
        vehicle_width = 2 + (FRAME_HEIGHT/2 - curr_y)/(FRAME_HEIGHT/2) * 2

    meter_per_pixel = curr_w/vehicle_width
    framerate = cap.get(cv2.CAP_PROP_FPS)
    frame_elapsed_time = 1 / framerate
    distance_from_previous_frame = abs(np.sqrt(np.power(curr_x + curr_w / 2 - prev_x + prev_w / 2, 2) +
                                               np.power(curr_y + curr_h / 2 - prev_y + prev_h / 2, 2)))
    distance_in_meters = distance_from_previous_frame * vehicle_width / curr_w
    vel = distance_in_meters / frame_elapsed_time
    current_vehicle.velocity = int(vel)


def find_objects(outputs, image):
    global previous_frame_vehicles
    global highest_id
    ht, wt, cT = image.shape
    bounding_boxes = []
    class_ids = []
    ids = []
    confs = []
    vehicles = []
    detections = []

    for output in outputs:
        for detection in output:
            confidence_scores = detection[5:]
            class_id = np.argmax(confidence_scores)
            confidence = confidence_scores[class_id]
            if class_id in ACCEPTED_CLASS_IDS:
                if confidence > CONF_THRESHOLD:
                    w, h = int(detection[2] * wt), int(detection[3] * ht)
                    x, y = int((detection[0] * wt) - w / 2), int((detection[1] * ht) - h / 2)
                    if y > MAX_DETECTION_HEIGHT:
                        if h > ht / 25:
                            if h < ht/5:
                                bounding_boxes.append([x, y, w, h])
                                vehicles.append(Vehicle(class_id, x, y, w, h, image, highest_id))
                                class_ids.append(class_id)
                                confs.append(float(confidence))
                                detections.append([[x, y, w, h], confidence, class_id])

    indexes = cv2.dnn.NMSBoxes(bounding_boxes, confs, CONF_THRESHOLD, NMS_THRESHOLD)

    if len(vehicles) > 0:

        for v in vehicles:
            if v.pos_y > MAX_DETECTION_HEIGHT:
                if len(previous_frame_vehicles) > 0:
                    closest = v.find_closest(previous_frame_vehicles)[0]
                    if v.in_range(closest.pos_x, closest.pos_y, closest.width/2, closest.height/2):
                        v.id = closest.id
                        v.age = closest.age + 1
                        # previous_frame_vehicles.remove(closest)
                    else:
                        v.id = highest_id
                        highest_id = highest_id + 1

                    # if v.id == highest_id:
                    #     highest_id = highest_id + 1

                    if v.id is None:
                        v.id = highest_id
                        highest_id = highest_id + 1

                    calculate_speed(v, closest)

                else:
                    v.id = highest_id
                    highest_id = highest_id + 1
                    v.velocity = 'N/A'

                ids.append(v.id)

    for i in indexes:
        box = bounding_boxes[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        dirstr = ""
        if vehicles[i].dir == 0:
            dirstr = "Approaching"
        else:
            dirstr = "Going away"
        cv2.putText(image, f'id: {vehicles[i].id}', (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(image, f'{dirstr}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, f'{vehicles[i].velocity} km/h', (x, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)
        plt.scatter(box[0] - box[2] / 2, FRAME_HEIGHT - box[1] - box[3] / 2, c ="red", marker="s")
    previous_frame_vehicles = vehicles.copy()
    vehicles.clear()
    return len(indexes)


while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (YOLO_RES, YOLO_RES), [0, 0, 0], crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()

    output_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    output = net.forward(output_names)

    number_of_cars = find_objects(output, img)

    cv2.putText(img, f'CURRENT NUMBER OF VEHICLES: {number_of_cars}', (FRAME_WIDTH - 350, FRAME_HEIGHT - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.imshow(DATE_STRING, img)

    if SAVE_VIDEO:
        img = cv2.resize(img, (FRAME_WIDTH, FRAME_HEIGHT))
        OUT.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if SAVE_VIDEO:
            OUT.release()
        cv2.destroyAllWindows()
        plt.xlim(0, FRAME_WIDTH)
        plt.ylim(0, FRAME_HEIGHT)
        plt.show()
        break
