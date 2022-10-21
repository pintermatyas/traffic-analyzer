import cv2
import numpy as np


input_file_name = 'sample2.mp4'
output_file_name = 'sampleOutput.mp4'
model_file_path = 'C:/Egyetem/5.felev/Temalab/yolov3-608.weights'

cap = cv2.VideoCapture(input_file_name)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file_name, fourcc, 30, (width, height))


yolo_res=608
conf_threshold = 0.5
nms_threshold = 0.5

classesFile = 'coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

model_configuration = 'yolov3.cfg'
model_weights = model_file_path

net = cv2.dnn.readNetFromDarknet(model_configuration, model_weights)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

def findObjects(outputs, img):
    height, width, cT = img.shape
    bounding_boxes = []
    class_ids = []
    confs = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                w, h = int(detection[2] * width), int(detection[3] * height)
                x,y = int((detection[0] * width) - w/2), int((detection[1] * height) - h/2)
                bounding_boxes.append([x,y,w,h])
                class_ids.append(class_id)
                confs.append(float(confidence))

    indexes = cv2.dnn.NMSBoxes(bounding_boxes, confs, conf_threshold, nms_threshold)

    for i in indexes:
        box = bounding_boxes[i]
        x,y,w,h = box[0], box[1], box[2], box[3]

        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        # cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i] * 1000)/10}%', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
    return len(indexes)

while True:
    success, img = cap.read()

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (yolo_res, yolo_res), [0, 0, 0], crop=False)
    net.setInput(blob)

    layer_names = net.getLayerNames()

    output_names = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    outputs = net.forward(output_names)

    number_of_cars = findObjects(outputs, img)
    cv2.putText(img, f'CURRENT NUMBER OF VEHICLES: {number_of_cars}', (width - 650, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    if(number_of_cars > 20):
        cv2.putText(img, f'CURRENT TRAFFIC: HIGH', (width-300, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    elif(number_of_cars > 10):
        cv2.putText(img, f'CURRENT TRAFFIC: MEDIUM', (width-300, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
    else:
        cv2.putText(img, f'CURRENT TRAFFIC: LOW', (width-300, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)


    cv2.imshow('Image', img)
    img = cv2.resize(img, (width, height))
    out.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break