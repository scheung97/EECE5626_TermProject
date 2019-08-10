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
    img = fff.get(input_img)

    # Add more facial feature processing here

    return img