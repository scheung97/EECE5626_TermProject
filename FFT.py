#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np

def FFT(input_img):
    print("[INFO]: Performing 2-D RFFT to input image")

    # convert image to ndarray
    im_arr = np.asarray(input_img)
    bw_img = cv2.cvtColor(im_arr, cv2.COLOR_BGR2GRAY)

    pre_fft_img = 'pre-fft.jpg'
    post_fft_img = 'post-fft.jpg'
    post_post_img = 'post-post-fft.jpg'
    cv2.imwrite(pre_fft_img,bw_img)
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

    """ outputs fft image """
    filtered_img = np.fft.rfft2(bw_img)
    filt_shift_img = np.fft.fftshift(filtered_img)
    mag_spec = 20*np.log(np.abs(filt_shift_img))
    mag_spec = mag_spec.astype(np.uint8)
    cv2.imwrite(post_fft_img,mag_spec)
    img = Image.fromarray(mag_spec)

    """performs reverse fft to verify result is correct for fft transform"""
    reverse_img_shift = np.fft.ifftshift(filt_shift_img)
    reverse_img = np.fft.irfft2(reverse_img_shift)
    reverse_img = np.abs(reverse_img)
    cv2.imwrite(post_post_img, reverse_img)
    return img
