# Security bot

## Configuration

stream.py should be able to run without any changes

image identification requires change of ip if wants to access raspberry pi camera footage (Ignore if using webcam of computer) 

image identification also require Gmail API token (ignore if you commented the gmail API section)

website requires mongodb configuraiton in configuration.ini and the same steps in image identification except for the gmail API

## Steps to run in order
run stream.py in your raspberry pi (ignore if using laptop webcam)

run either run.py in website or yolov8v2.py in image identification , based on what you want to start


## Reference
Gmail API https://developers.google.com/gmail/api/quickstart/python
stream.py https://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming
website https://github.com/chriswilson1982/flask-mongo-app/tree/main


