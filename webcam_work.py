"""python facial recognition"""
import numpy
import cv2
import time
from matplotlib import pyplot as plt #using to check edges

"""DNN stuff needed and taken from online: """
DNN = "TF"
if DNN == "CAFFE":
    modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
    modelFile = "opencv_face_detector_uint8.pb"
    configFile = "opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
""" ----------------"""

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
"""
time.sleep(0)
output = cv2.imread('testoutput.jpg')
cv2.imshow('test',output)
gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #converts rgb2gray
cv2.imshow("gray image",gray)
time.sleep(10)
"""

"""DNN code taken from online: """
blob = cv2.dnn.blobFromImage(output, 1.0, (300, 300), [104, 117, 123], False, False)

net.setInput(blob)
detections = net.forward()
bboxes = []
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > conf_threshold:
        x1 = int(detections[0, 0, i, 3] * frameWidth)
        y1 = int(detections[0, 0, i, 4] * frameHeight)
        x2 = int(detections[0, 0, i, 5] * frameWidth)
        y2 = int(detections[0, 0, i, 6] * frameHeight)

		#[x1, y1, x2,y2] = face_box
""" -----"""

#use bounding box dimensions for edge detection:
for x,y in range(face_box): #range(x1,x2):
	#for y in range(y1,y2):
	edges = cv2.Sobel([x,y],CV_64F,1,1,ksize = 3)
#outputing edges to see if it works:
plt.plot(edges)
plt.title('Edges')
plt.xticks([])
plt.yticks([])

""" Matlab pseudo code implementation:
	Gx=[-1 0 1; -2 0 2; -1 0 1]
	Gy=[-1 -2 -1; 0 0 0; 1 2 1]

	rows = size(output,1)
	columns = size(output,2)
	mag=zeros(output)

	for i=x1:x2
		for j=y1:y2
			S1=sum(sum(Gx.*output(i:i+2,j:j+2)))
			S2=sum(sum(Gy.*output(i:i+2,j:j+2)))

			mag(i+1,j+1)=sqrt(S1.^2+S2.^2)
		end for
	end for

	threshold = 70 #varies for application [0 255]
	output_image = max(mag,threshold)
	output_image(output_image=round(threshold))=0;
	return output_image
"""



"""-----"""
