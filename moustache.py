#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np
from skimage.util import random_noise

import find_facial_features as fff

def moustache(input_img):
    print("[INFO]: Adding a moustache to input image")

    # Find and overlay facial feature points
    #img = fff.get(input_img)

    # Add more facial feature processing here
####################################################################################
    #-----------------------------------------------------------------------------
    #       Load and configure Haar Cascade Classifiers
    #-----------------------------------------------------------------------------
    
    # location of OpenCV Haar Cascade Classifiers:
    #baseCascadePath = "/usr/local/share/OpenCV/haarcascades/"
    
    # xml files describing our haar cascade classifiers
    faceCascadeFilename = "haarcascade_frontalface_default.xml"
    noseCascadeFilename = "haarcascade_mcs_nose.xml"
    
    # build our cv2 Cascade Classifiers
    faceCascade = cv2.CascadeClassifier(faceCascadeFilename)
    noseCascade = cv2.CascadeClassifier(noseCascadeFilename)

    #-----------------------------------------------------------------------------
    #       Load and configure mustache (.png with alpha transparency)
    #-----------------------------------------------------------------------------
    
    # Load our overlay image: mustache.png
    imgMustache = cv2.imread('mustache.png', -1)
    
    # Create the mask for the mustache
    orig_mask = imgMustache[:, :, 3]
    
    # Create the inverted mask for the mustache
    orig_mask_inv = cv2.bitwise_not(orig_mask)
    
    # Convert mustache image to BGR
    # and save the original image size (used later when re-sizing the image)
    imgMustache = imgMustache[:, :, 0:3]
    origMustacheHeight, origMustacheWidth = imgMustache.shape[:2]

    ##########################################################################
    #img = input_img.copy()
    frame = np.array(input_img)
    
    # Create greyscale image from input image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # Detect faces in input image
    print("[INFO]: Detecting faces in image ...")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        #flags=cv2.CV_HAAR_SCALE_IMAGE
    )
    print("        Number of faces detected: {}".format(len(faces)))

    # Iterate over each face found
    for (x, y, w, h) in faces:
        print("        Detection {}: X: {} Y: {} W: {} H: {}".format(
            len(faces), x, y, w, h))
        # Un-comment the next line for debug (draw box around all faces)
        face_box = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
 
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
 
        # Detect a nose within the region bounded by each face (the ROI)
        print("[INFO]: Detecting nose in face {} ...".format(len(faces)))
        nose = noseCascade.detectMultiScale(roi_gray)
 
        for (nx, ny, nw, nh) in nose:
            print("        Detection {}: Nose X: {} Nose Y: {} Nose W: {} Nose H: {}".format(
                len(nose), nx, ny, nw, nh))
            # Un-comment the next line for debug (draw box around the nose)
            nose_box = cv2.rectangle(roi_color, (nx, ny), (nx+nw, ny+nh), (255, 0, 0), 2)
 
            # The mustache should be three times the width of the nose
            mustacheWidth =  3 * nw
            mustacheHeight = mustacheWidth * origMustacheHeight / origMustacheWidth
 
            # Center the mustache on the bottom of the nose
            x1 = int( nx - (mustacheWidth/4) )
            x2 = int( nx + nw + (mustacheWidth/4) )
            y1 = int( ny + nh - (mustacheHeight/3) )
            y2 = int( ny + nh + (mustacheHeight/2) )
 
            # Check for clipping
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > w:
                x2 = w
            if y2 > h:
                y2 = h
 
            # Re-calculate the width and height of the mustache image
            mustacheWidth = int( x2 - x1 )
            mustacheHeight = int( y2 - y1 )
 
            # Re-size the original image and the masks to the mustache sizes
            # calculated above
            print("[INFO]: Resizing mustache image and masks")
            mustache = cv2.resize(imgMustache, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)
            mask = cv2.resize(orig_mask, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (mustacheWidth, mustacheHeight), interpolation = cv2.INTER_AREA)
 
            print("[INFO]: Evaluating ROI")
            # take ROI for mustache from background equal to size of mustache image
            roi = roi_color[y1:y2, x1:x2]
 
            # roi_bg contains the original image only where the mustache is not
            # in the region that is the size of the mustache.
            roi_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)
 
            # roi_fg contains the image of the mustache only where the mustache is
            roi_fg = cv2.bitwise_and(mustache, mustache, mask = mask)
 
            print("[INFO]: Adding ROI images")
            # join the roi_bg and roi_fg
            dst = cv2.add(roi_bg, roi_fg)
 
            print("[INFO]: Updating destination image")
            # place the joined image, saved to dst back over the original image
            roi_color[y1:y2, x1:x2] = dst

            # make sure we only draw one mustache, even if there are multiple "noses"
            break

    print("[INFO]: Moustache added to image")
    frame = Image.fromarray(frame)

    return frame