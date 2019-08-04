#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np
from skimage.util import random_noise

def gaussian(input_img):
    print("[INFO]: Adding Gaussian Noise to input image")

    # convert PIL Image to ndarray
    im_arr = np.asarray(input_img)

    # random_noise() method will convert image in [0, 255] to [0, 1.0],
    # inherently it use np.random.normal() to create normal distribution
    # and adds the generated noised back to image
    noise_img = random_noise(im_arr, mode='gaussian', var=0.05**2)
    noise_img = (255*noise_img).astype(np.uint8)

    img = Image.fromarray(noise_img)
    return img