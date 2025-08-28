import math
import ser_parser
import os
import numpy as np
import pandas as pd
import scipy.signal as ss
import scipy.ndimage as nd
from scipy import ndimage
import skimage as ski
import statistics as stat
import copy
def gaussian_filter(img,sigma):
    img = nd.gaussian_filter(img,sigma)
    
def align(img, ref):
    zs = ss.fftconvolve(img, ref[::-1, ::-1])
    return np.array(np.unravel_index(np.argmax(zs, axis=None), zs.shape)) - np.array(img.shape) + [1, 1]

def center(img):
    val = copy.deepcopy(img)
    val = ski.filters.threshold_otsu(val)
    ys = copy.deepcopy(img)
    ys[ys < val] = 0.0
    x, y = ndimage.measurements.center_of_mass(ys)
    shape=np.shape(img)
    shift = np.array([shape[0] // 2 - x, shape[1] // 2 - y]).round()
    return shift
    
def bkg_correct(img):
    out = img-np.median(np.ascontiguousarray(img.ravel()))
    out[out<0] = 0
    return out
    
def square_image(img):
    shape = np.shape(img)
    x = shape[1]-shape[0]
    if x <0:
        x=0
    y = shape[0]-shape[1]
    if y<0:
        y=0
    return np.pad(img,[(0,x),(0,y)],mode='constant')

def bkg_mask(img):
    val = ski.filters.threshold_otsu(img)
    img[img < val] = 0.0
    return img
    
def resize(img, dim):
    #Assume Image is square
    shape = np.shape(img)
    if dim > shape[0]:
        d = dim-shape[0]
        return np.pad(img,[(0,d),(0,d)],mode='constant')
    else:
        return img[0:dim,0:dim]    
        
def deg2rad(x):
    return x*(math.pi/180)

def rad2deg(x):
    return x*(math.pi/180)
