import datetime

import cv2
import numpy as np
from datetime import datetime
from vehicle import Vehicle

# If you want to save the output video every time you run the script, set it to False
# Else set it to True
TEST_MODE = False

now = datetime.now()
date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

input_file_name = 'sample2.mp4'
input_file_path = 'input/' + input_file_name
output_file_name = date_string + '.mp4'
output_file_path = 'output/' + output_file_name
model_file_path = 'C:/Egyetem/5.felev/Temalab/yolov3-608.weights'
classesFile = 'configfiles/coco.names'

cap = cv2.VideoCapture(input_file_path)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
if not TEST_MODE:
    out = cv2.VideoWriter(output_file_path, fourcc, 30, (width, height))

# car, motorbike, bus, truck
accepted_class_ids = [2, 3, 5, 7]

yolo_res = 608
conf_threshold = 0.6
nms_threshold = 0.5

classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

model_configuration = 'configfiles/yolov3.cfg'
model_weights = model_file_path

net = cv2.dnn.readNetFromDarknet(model_configuration, model_weights)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

previous_frame_vehicles = []
highest_id = 0


def findObjects(outputs, img):
    global previous_frame_vehicles
    global highest_id
    height, width, cT = img.shape
    bounding_boxes = []
    class_ids = []
    ids = []
    confs = []
    vehicles = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id in accepted_class_ids:
                if confidence > conf_threshold:
                    w, h = int(detection[2] * width), int(detection[3] * height)
                    x, y = int((detection[0] * width) - w / 2), int((detection[1] * height) - h / 2)
                    if h > height / 25:
                        bounding_boxes.append([x, y, w, h])
                        vehicles.append(Vehicle(class_id, x, y, w, h, img, highest_id))
                        class_ids.append(class_id)
                        confs.append(float(confidence))

    indexes = cv2.dnn.NMSBoxes(bounding_boxes, confs, conf_threshold, nms_threshold)

    if len(vehicles) > 0:

        # processed_vehicles = []
        #
        # for prev in previous_frame_vehicles:
        #     closest = prev.find_closest(vehicles)[0]
        #     if prev.in_range(closest.pos_x, closest.pos_y):
        #         prev.id = closest.id
        #         processed_vehicles.append(closest)
        #     else:
        #         prev.id = highest_id
        #         highest_id = highest_id + 1
        #     if prev.id == highest_id:
        #         highest_id = highest_id + 1
        #     if prev.id is None:
        #         prev.id = highest_id
        #         highest_id = highest_id + 1

        for v in vehicles:

            # if v not in processed_vehicles:
            #     v.id = highest_id
            #     highest_id = highest_id + 1

            if len(previous_frame_vehicles) > 0:
                closest = v.find_closest(previous_frame_vehicles)[0]
                if v.in_range(closest.pos_x, closest.pos_y, closest.width, closest.height):
                    v.id = closest.id
                    # previous_frame_vehicles.remove(closest)
                else:
                    v.id = highest_id
                    highest_id = highest_id + 1

                # if v.id == highest_id:
                #     highest_id = highest_id + 1

                if v.id is None:
                    v.id = highest_id
                    highest_id = highest_id + 1

            else:
                v.id = highest_id
                highest_id = highest_id + 1

            ids.append(v.id)

    for i in indexes:
        box = bounding_boxes[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.putText(img, f'{classNames[class_ids[i]].upper()} {int(confs[i] * 1000)/10}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
        dirstr = ""
        if vehicles[i].dir == 0:
            dirstr = "Coming torwards us"
        else:
            dirstr = "Going away"
        cv2.putText(img, f'id: {vehicles[i].id}', (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(img, f'Dir: {dirstr}', (x, y + h + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)

    previous_frame_vehicles = vehicles.copy()
    vehicles.clear()
    return len(indexes)


while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (yolo_res, yolo_res), [0, 0, 0], crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()

    output_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(output_names)

    number_of_cars = findObjects(outputs, img)
    cv2.putText(img, f'CURRENT NUMBER OF VEHICLES: {number_of_cars}', (width - 650, height - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    if (number_of_cars > 20):
        cv2.putText(img, f'CURRENT TRAFFIC: HIGH', (width - 300, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255), 2)
    elif (number_of_cars > 10):
        cv2.putText(img, f'CURRENT TRAFFIC: MEDIUM', (width - 300, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255), 2)
    else:
        cv2.putText(img, f'CURRENT TRAFFIC: LOW', (width - 300, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255), 2)

    cv2.imshow(date_string, img)

    if not TEST_MODE:
        img = cv2.resize(img, (width, height))
        out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        if not TEST_MODE:
            out.release()
        cv2.destroyAllWindows()
        break
