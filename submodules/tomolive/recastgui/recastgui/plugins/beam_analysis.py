import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import matplotlib.image as mpimg
from read_write import regtext, reset
import skimage.metrics as ski
import astra 
import copy
import os 
import sys

#data2d 
#data3d
#projector
#algorithm
#matrix
#creators
#functions
#optomo
#plugin
#astra


def GetNorm(img,slices):
    val = 0
    for i in range(slices): 
        val= val + np.sum(img[i]**2)
    val = np.sqrt(val)
    val = 128.0*128.0
    return val
    

def GetSROD(img_new, img_old, slices):
    val = 0
    norm = 0
    for i in range(slices):
        val = val + np.sum(np.abs(img_new[i]-img_old[i]))
        norm = norm + np.sum(np.abs(img_old[i]))
    val = val/norm
    return val

def GetSNR(img):
    arr = np.array(img[0])
    arr = np.append(arr,img[1])
    arr = np.append(arr,img[2])
    store = sys.getsizeof(arr[0])
    m = arr.mean()
    sd = arr.std()
    return np.where(sd == 0, 0, m/sd)

class StoredData():
    def __init__(self, slices):
        self.nproj = 0
        self.nslices = 0
        self.slices = slices
        self.duplicates = [False]*3
        self.img_old = [None]*slices
        self.norm = 0
        self.img_new = [None]*slices
        self.orientations = [None]*slices
        #self.fig = plt.figure()
        #self.axs = [None]*6
        #for i in range(self.slices):
        #    self.axs[i] = plt.add_subplot(2,3,i)
        
    def Display(self):
        print('') 
        print('Stored Data:') 
        print(self.nproj, self.nslices) 
        for i in range(self.slices):
            print(self.orientations[i])
        
def callback(args, data, orientation, shape, img ):
    slices = 3
    if data==None:
        data = StoredData(slices)

    if data.nproj ==0:
        registered_orientation = False
        for i in range(slices):
            if np.array_equal(orientation, data.orientations[i]):
                registered_orientation = True
        if registered_orientation == False:
            data.img_new[data.nslices] = np.array(img)
            data.orientations[data.nslices] = orientation
            data.nslices = data.nslices + 1

    if data.nproj >= 1:
        registered_orientation = False
        for i in range(slices):
            if np.array_equal(orientation, data.orientations[i]):
                registered_orientation = True
                if data.duplicates[i] == False:
                    data.duplicates[i] = True
                    data.img_new[i] = np.array(img)
                    data.nslices = data.nslices + 1
                else:
                    data.duplicates[i] = False
        if registered_orientation == False:
            reset.Write(os.path.join(args.data.path,'reset.txt'), True )
            data = StoredData(slices)
            #TODO Prepare a reset
    
    duplicate_set = False
    for i in range(slices):
        if data.duplicates[i] == True:
            duplicate_set = True
             
    if data.nslices == slices and duplicate_set == False:
        a=0.0
        b=0.0
        if data.nproj == 1:
            a = [GetSNR(data.img_new)]
            b = [GetSROD(data.img_new, data.img_new, slices)]

        if data.nproj >1:
            a = [GetSNR(data.img_new)]
            b = [GetSROD(data.img_new, data.img_old, slices)]
        if data.nproj == 1:
            data.df = pd.DataFrame(data={'projections':data.nproj,'snr':a, 'srod':b})
        elif data.nproj > 1:
            df2 = pd.DataFrame(data={'projections':data.nproj,'snr':a, 'srod':b})
            data.df = data.df.append(df2, ignore_index=True)
            print(data.df.loc[data.nproj-1,'projections'],
                data.df.loc[data.nproj-1,'snr'],
                data.df.loc[data.nproj-1,'srod'])
        data.nslices = 0
        data.nproj = data.nproj + 1
        data.img_old = copy.deepcopy(data.img_new)
    return [data, orientation, shape, img]
