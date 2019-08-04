"""python facial recognition"""
import numpy
import cv2
import time

"""opens up laptop webcam"""
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

#define output file:
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    image = 'testoutput.jpg'
    cv2.imshow("preview", frame)
    rval, frame = vc.read()

    key = cv2.waitKey(10)
    if key == ord('c'):
        cv2.imwrite(image, frame)
        print("image captured")
    elif key == 27: #key 27 = esc key
        break
vc.release()
cv2.destroyAllWindows()
#TA says to use DLIB, and show qualitative data for report
    #DLIB frontal face detector doesn't include the forehead and chin (which we want)

"""perform OpenCV DNN face detection: """
time.sleep(0)
output = cv2.imread('testoutput.jpg')
cv2.imshow('test',output)
gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #converts rgb2gray
cv2.imshow("gray image",gray)
time.sleep(10)

#use bounding box dimensions for edge detection



"""-----"""

"""
to do
#Haar detection --> come up with bounding box --> use sobel detection in bounding box to map face.

#facialCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
"""
