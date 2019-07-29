"""python facial recognition"""
import numpy
import cv2

"""opens up laptop webcam"""
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
#vc = cv2.VideoCapture(0, cv2.CAP_DSHOW)#eliminate async callback warming?

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
    elif key == 27:
        break

vc.release()
cv2.destroyAllWindows()
"""-----"""
