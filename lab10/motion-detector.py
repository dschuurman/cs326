'''
CS326 Lab 10
Author: D. Schuurman
Simple motion detector using pi camera.
'''
import time
import sys
import cv2

# Motion threshold: tune for sensitivity to motion
MOTION_THRESHOLD = 1000000

def get_frame(cap):
    ''' Return grayscale image from camera if capture successful
    '''
    ret, frame = cap.read()
    if not ret:
        print('Frame capture failed...')
        sys.exit(1)    
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

# Initialize camera
print("Initializing camera...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera...')
    sys.exit(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 2)

# initialize last frame
last_frame = get_frame(cap)

# Continuously capture frames from the camera
try:
    while True:
        # grab a frame
        current_frame = get_frame(cap)

        # compute the abs of difference between current and last frame
        frameDelta = cv2.absdiff(current_frame, last_frame)
        diff = frameDelta.sum()

        # If diff > threshold, report motion detected
        if diff > MOTION_THRESHOLD:
            print('motion detected!')
            time.sleep(2)
            last_frame = get_frame(cap)
        else:
            last_frame = current_frame

except KeyboardInterrupt:
    print('Done')
    cap.release()
