import torch
import cv2
from ultralytics import YOLO
import time
from datetime import datetime
import base64
import numpy as np

net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Use a larger model for better accuracy
#model = YOLO("D:\filename\\stationery_model\\weights\\best.pt")  # Update with the path to your trained model weights
# Open the webcam
classNames = []
        
# Set a confidence threshold
confidence_threshold = 0.6  # Adjust this value as needed

# Set frame processing interval
frame_interval = 100  # Process every 2nd frame
frame_count = 0
# Print out the class names
class_names = model.names
#print("Classes used by the model:", class_names)

def AIrecognition(ret, frame):
    while True:
        #ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Process every nth frame to improve performance
        if frame_count % frame_interval == 0:
            # Resize frame for faster processing
            resized_frame = cv2.resize(frame, (320, 240))
        # Perform object detection
        results = model(frame, verbose=False)

        # Extract bounding boxes and labels from the results
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes    
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]  # coordinates of the bounding box
                    conf = box.conf.item()  # confidence score (convert to a Python float)
                    cls = box.cls.item()  # class id (convert to a Python float)
                    label = model.names[int(cls)]
                    if conf > confidence_threshold:  # Filter by confidence
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            return frame
    #Below is the never ending loop that determines what will happen when an object is identified.    
    #Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           
    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame