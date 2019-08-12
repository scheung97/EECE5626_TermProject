#!/usr/bin/env python
# coding: utf-8

import cv2
from PIL import Image
import numpy as np

def DFT(input_img):
    print("[INFO]: Performing 2-D DFT to input image")
    # convert image to ndarray
    im_arr = np.asarray(input_img)
    bw_img = cv2.cvtColor(im_arr, cv2.COLOR_BGR2GRAY)

    pre_dft_img = 'pre-dft.jpg'
    post_dft_img = 'post-dft.jpg'
    post_post_img = 'post-post-dft.jpg'

    cv2.imwrite(pre_dft_img,bw_img)
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

    """ outputs dft image """
    filtered_img = np.fft.fft2(bw_img)
    filt_shift_img = np.fft.fftshift(filtered_img)
    mag_spec = 20*np.log(np.abs(filt_shift_img))
    mag_spec = mag_spec.astype(np.uint8)
    cv2.imwrite(post_dft_img,mag_spec)
    img = Image.fromarray(mag_spec)

    """performs reverse fft to verify result is correct for dft transform"""
    reverse_img_shift = np.fft.ifftshift(filt_shift_img)
    reverse_img = np.fft.ifft2(reverse_img_shift)
    reverse_img = np.abs(reverse_img)
    cv2.imwrite(post_post_img, reverse_img)
    return img
