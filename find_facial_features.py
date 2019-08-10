#!/usr/bin/env python
# coding: utf-8

import sys
import os
import dlib
import glob

import cv2
from PIL import Image
import numpy as np

def get(input_img):
    print("[INFO]: Detecting faces in image ...")

    predictor_path = 'shape_predictor_68_face_landmarks.dat' #os.path.dirname(os.path.realpath(__file__)) #

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    img = np.asarray(input_img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    print("        Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("        Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("            Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))
        
        vec = np.empty([68,2], dtype=int)
        for b in range(68):
            vec[b][0] = shape.part(b).x
            vec[b][1] = shape.part(b).y

        img = annotate_landmarks(img, vec)
    
    img = Image.fromarray(img)

    return img


####################################################################################################
# Helper Functions
####################################################################################################
def annotate_landmarks(im, landmarks):
    CIRCLE_SIZE = 1
    FONT_SCALE = 1
    THICKNESS_S = 2
    
    im = im.copy()
    
    #0-16: head
    A = (landmarks[0][0], landmarks[0][1],)
    cv2.circle(im, A, CIRCLE_SIZE, color=(255, 0, 0), thickness=THICKNESS_S)
    for idx, point in enumerate(landmarks[1:17]):
        B = (point[0], point[1])
        #cv2.putText(im, str(idx), pos, fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=FONT_SCALE, color=(0, 0, 255))
        cv2.circle(im, B, CIRCLE_SIZE, color=(255, 0, 0), thickness=THICKNESS_S)
        cv2.line(im, A, B, color=(255, 0, 0), thickness=THICKNESS_S)
        A = B

    #17-21: left eye brow
    #22-26: right eye brow
    for idx, point in enumerate(landmarks[17:27]):
        pos = (point[0], point[1])
        #cv2.putText(im, str(idx), pos,fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,fontScale=FONT_SCALE,color=(0, 0, 255))
        cv2.circle(im, pos, CIRCLE_SIZE, color=(0, 255, 0), thickness=THICKNESS_S)

    #27-35: nose
    A = (landmarks[27][0], landmarks[27][1],)
    cv2.circle(im, A, CIRCLE_SIZE, color=(0, 0, 255), thickness=THICKNESS_S)
    for idx, point in enumerate(landmarks[28:36]):
        B = (point[0], point[1])
        #cv2.putText(im, str(idx), pos,fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,fontScale=FONT_SCALE,color=(0, 0, 255))
        cv2.circle(im, B, CIRCLE_SIZE, color=(0, 0, 255), thickness=THICKNESS_S)
        cv2.line(im, A, B, color=(255, 0, 0), thickness=THICKNESS_S)
        A = B

    #36-41: left eye
    #42-47: right eye
    for idx, point in enumerate(landmarks[36:48]):
        pos = (point[0], point[1])
        #cv2.putText(im, str(idx), pos,fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,fontScale=FONT_SCALE,color=(0, 0, 255))
        cv2.circle(im, pos, CIRCLE_SIZE, color=(0, 255, 255), thickness=THICKNESS_S)

    #48-68: lips
    A = (landmarks[48][0], landmarks[48][1],)
    cv2.circle(im, A, CIRCLE_SIZE, color=(255, 0, 255), thickness=THICKNESS_S)
    for idx, point in enumerate(landmarks[49:68]):
        B = (point[0], point[1])
        #cv2.putText(im, str(idx), pos,fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,fontScale=FONT_SCALE,color=(0, 0, 255))
        cv2.circle(im, B, CIRCLE_SIZE, color=(255, 0, 255), thickness=THICKNESS_S)
        cv2.line(im, A, B, color=(255, 0, 0), thickness=THICKNESS_S)
        A = B
    
    return im