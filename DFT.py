#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np

def DFT(input_img):
    print("[INFO]: Performing 2-D DFT to input image")

    # convert image to ndarray
    im_arr = np.asarray(input_img)

    """
    # do not use original image, it overwrites the image
    noise_arr = np.zeros(im_arr.shape, np.uint8)

    # create the random distribution
    mean = (1, 1, 1)
    sigma = (10, 10, 10)
    cv2.randn(noise_arr, mean, sigma)

    # add the noise to the original image
    img = cv2.add(im_arr, noise_arr)
    img = Image.fromarray(img)

    """
    filtered_img = np.fft.fft2(im_arr)
    #filtered_img = filtered_img.astype(np.uint8)
    filtered_img = (255*filtered_img).astype(np.uint8)
    img = Image.fromarray(filtered_img)

    return img
