# cython: language_level=3

cimport numpy as np
import numpy as np
import cv2

def apply_grayscale_filter(np.ndarray[np.uint8_t, ndim=3] image):
    cdef np.ndarray[np.uint8_t, ndim=2] gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image