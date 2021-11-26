import numpy as np
import argparse
import cv2 as cv
import subprocess
import time
import os
from yolo_utils import infer_image, show_image

def inference(camSource):
    if __name__ == '__main__':
        
        # Get the labels
        labels = open('./yolov3-coco/coco-labels').read().strip().split('\n')
        
        # Intializing colors to represent each label uniquely
        colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

        # Load the weights and configutation to form the pretrained YOLOv3 model
        net = cv.dnn.readNetFromDarknet(
            './yolov3-coco/yolov3.cfg', './yolov3-coco/yolov3.weights')

        # Get the output layer names of the model
        layer_names = net.getLayerNames()
        layer_names = [layer_names[i[0] - 1]
                    for i in net.getUnconnectedOutLayers()]

        # Infer real-time on webcam
        count = 0
        vid = cv.VideoCapture(camSource)
        while True:
            _, frame = vid.read()
            height, width = frame.shape[:2]
            if count == 0:
                frame, boxes, confidences, classids, idxs = infer_image(net, layer_names,
                                                                        height, width, frame, colors, labels)
                count += 1
            else:
                frame, boxes, confidences, classids, idxs = infer_image(net, layer_names,
                                                                        height, width, frame, colors, labels, boxes, confidences, classids, idxs, infer=False)
                count = (count + 1) % 6
            # cv.imshow('webcam', frame)
            yield cv.imencode('.jpg', frame)

