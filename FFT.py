#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np

def FFT(input_img):
    print("[INFO]: Performing 2-D RFFT to input image")

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
    # random_noise() method will convert image in [0, 255] to [0, 1.0],
    # inherently it use np.random.normal() to create normal distribution
    # and adds the generated noise back to image

    filtered_img = np.fft.rfft2(im_arr)
    filtered_img = (255*filtered_img).astype(np.uint8)
    img = Image.fromarray(filtered_img)
    return img
