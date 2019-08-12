#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np
from skimage.util import random_noise

import find_facial_features as fff

def beard(input_img):
    mustashe = cv2.imread(**insert file name here**)
    print("[INFO]: Adding a beard to input image")

    vec = np.empty([68,2], dtype=int)
    # Find and overlay facial feature points
    img, vec[b][0], vec[b][1] = fff.get(input_img)

    """ find lowest chin/head point and then input image there """
    #https://towardsdatascience.com/facial-mapping-landmarks-with-dlib-python-160abcf7d672
    #vec[b][0] = x
    #vec[b][1] = y
    chin.x = vec[8][0]
    chin.y = vec[8][1]

    chin_position = [chin.x,chin.y]
    




    # Add more facial feature processing here

    return img
