'''
CS326 Lab 10
Author: D. Schuurman
Simple AprilTag detector using pi camera.
'''
import time
import sys
import cv2
from picamera2 import Picamera2
from pupil_apriltags import Detector

# Initialize camera
print("Initializing camera...")
picam2 = Picamera2()
config = picam2.create_still_configuration( )
picam2.configure(config)
picam2.start()

# initialize AprilTag detector
detector = Detector()

# Continuously capture frames from the camera
try:
    while True:
        # grab a frame and convert to grayscale
        frame = picam2.capture_array()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect any AprilTags
        results = detector.detect(img)
        # Print detection details for all tags
        for r in results:
            print(f"AprilTag detected! ID: {r.tag_id}, Family: {r.tag_family}," f"Decision Margin: {r.decision_margin:.2f}")

except KeyboardInterrupt:
    print('Done')
    picam2.stop()
