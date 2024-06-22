import torch
import cv2
from ultralytics import YOLO
import time
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import base64

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # Use a larger model for better accuracy
#model = YOLO("file directory//best.pt")  # Update with the path to your trained model weights
# Open the webcam
#cap = cv2.VideoCapture(0)
classNames = []

def create_message(sender, to, subject, message_text):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = to
    msgRoot.preamble = message_text
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<b> <i>BEEP BEEP BEEP SEND HELP CALL 911</i> <br /> </b> THERE IS AN INTRUDER, HERE IS AN IMAGE OF HIM/HER<br><img src="cid:image1"><br>', 'html')
    msgAlternative.attach(msgText)
    fp = open('c1.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # message = MIMEText(message_text)
    # message['to'] = to
    # message['from'] = sender
    # message['subject'] = subject
    #return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    return {'raw': base64.urlsafe_b64encode(msgRoot.as_string().encode()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')


        
# Set a confidence threshold
confidence_threshold = 0.6  # Adjust this value as needed

# Set frame processing interval
frame_interval = 100  # Process every 2nd frame
frame_count = 0
last =0
# Print out the class names
class_names = model.names
cap = cav2.VideoCapture(0)
#cap = cv2.VideoCapture('http://IP Address/stream.mjpg')
#print("Classes used by the model:", class_names)
if __name__ =="__main__":
    person_detected_time = None
    while True:
        ret, frame = cap.read()
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
                        #start comment from this part if you do not want the gmail API
                        if label == 'person':
                            if person_detected_time is None:
                                person_detected_time = time.time()
                            elif time.time() - person_detected_time > 3:
                                cv2.imwrite('c1.png',frame)
                                #gmail API has a token that you need to place in a file called token.json
                                creds = Credentials.from_authorized_user_file('token.json')
                                service = build('gmail', 'v1', credentials=creds)
                                sender = "email.com"
                                to = "email.com"
                                subject = "INTRUDER DETECTED!"
                                message_text = "A person is detected in your room for 3 seconds"
                                message = create_message(sender, to, subject, message_text)
                                send_message(service, "me", message)
                                person_detected_time = None
                            #end comment to this part here as the GMAIL API ends here
                        else:
                            person_detected_time = None
    #Below is the never ending loop that determines what will happen when an object is identified.    
    #Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)
            

                
                # Display the frame
            cv2.imshow('YOLOv8 Webcam', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
