import math
import pandas as pd
import numpy as np
import ser_parser
import os
import time
import tomop
import csv
import helpers.preprocess as pp

#import mxnet as mx
from PIL import Image
from scipy import ndimage


def Write_Filelist(path, df=pd.DataFrame()):
    if len(df.index)==0:
        a ='w'
    else:
        a='a'
    with open(path, a) as f:
        writer = csv.writer(f)
        if len(df.index)==0:
            row =['projection','angle','file']
        else:
            row =[df.index[-1], df['angle'].iloc[-1],df['file'].iloc[-1]]
        writer.writerow(row)
    
def Update_Reconstruction(pub, args, filelist,img_array):
    images=[]
    i=len(filelist.index)
    filelist = filelist.sort_index()
    shape = np.shape(img_array)
    geom_spec = tomop.geometry_specification_packet(0, [-shape[1] / 2, -shape[1] / 2, -shape[1] / 2],[shape[0] / 2, shape[0]/2, shape[0]/ 2])
    pub.send(geom_spec)
    par_beam = tomop.parallel_beam_geometry_packet(0, shape[0], shape[1], i, pp.deg2rad(filelist['angle'].to_numpy()))
    pub.send(par_beam)
    pub.send(tomop.scan_settings_packet(0, 0, 0, args.linearize)) 
    print('Update Reconstruction')
    for j in range(len(filelist.index)):
        index = filelist.index[j]
        if i==1:
            img=img_array[0:-1,0:-1]
            img=pp.resize(img,shape[0])
        else:
            img=img_array[0:-1,0:-1,index]
            img=pp.resize(img,shape[0])
            
        print(np.shape(img), pp.deg2rad(filelist['angle'].to_numpy()),index+1)
        image=Image.fromarray(img).convert('P')
        images.append(image)
        pub.send(tomop.projection_packet(2, index+1, [shape[0], shape[1]], np.ascontiguousarray(img.ravel())))
    alignpath = os.path.join(args.path, "align.gif")
    images[0].save(alignpath, save_all=True, append_images=images[0:], optimize=False, duration=200, loop=0)

def Run(args):
    filepath = os.path.join(args.path, "files.txt")
    save, reset = WriteSave(reset)
    if os.path.exists(filepath) and not !save:
        filelist = ReadFiles()
    elif save:
        filelist = ReadSave()
    else:
        filelist = pd.DataFrame()
        WriteFileList(filepath)
    
    pub = tomop.publisher(args.host, args.port)
    steps = args.stop
    angles = np.linspace(args.acquisition.start, args.acquisition.stop, ,True)
    angles = np.radians(angles)
    
    
    angle_range = args.end - args.start
    ang_list = []

    pub = tomop.publisher(args.host, args.port)
    filelist = pd.read_csv(filepath)
    
    print('Reading from Directory: ', args.path)
    filepath = os.path.join(args.path, "files.txt")
    resetpath = os.path.join(args.path, "reset.txt")
    if os.path.exists(filepath):
        #filelist = Read_Filelist(filepath)
        reset = True
        ## read in image array
    else:
        filelist = pd.DataFrame()
        Write_Filelist(filepath)
        reset = False
    
    angle_range = args.end - args.start
    ang_list = []

    pub = tomop.publisher(args.host, args.port)
    
    if os.path.exists(filepath):
        filelist = pd.read_csv(filepath)
        print(filelist)
        for j in range(len(filelist.index)):
            df=filelist.iloc[j]
            print(j)
            filename = df['file']
            shape, img = ser_parser.parser(os.path.join(args.path,filename))

            img = np.array(img)
            img = np.reshape(img,shape)
            img = pp.bkg_correct(img)
            img = pp.bkg_mask(img)
            img = pp.square_image(img)
            img = pp.center(img)
            if j+1 > 1:
                shift = pp.align(img,img_old)
                img = np.roll(img, -shift, (0, 1))
            img_old = img    
            if j+1 == 1:
                img_array = img
            else:
                img_array = np.dstack([img_array,img])
            Update_Reconstruction(pub,args, filelist.iloc[0:j],img_array)
            
            
    while True:
        time.sleep(1)
        if os.path.exists(resetpath):
            reset = True
        i=len(filelist.index)
        for filename in os.listdir(args.path):
            if filename.endswith(args.ext):
                if i != 0:
                    found = filelist[filelist['file'].str.contains(filename)].empty
                else: 
                    found = True
                if found == True:
                    i = i+1
                    angle = (math.radians(angle_range)*i*((1+math.sqrt(5))/2)) % math.radians(angle_range)
                    angle = math.degrees(angle) + args.start
                    print(angle, ' ', math.radians(angle))
                    angle = math.radians(angle)
                    shape, img = ser_parser.parser(os.path.join(args.path,filename))
                    if i == 1:
                        filelist = pd.DataFrame([[i,math.degrees(angle), filename]], columns=['projection','angle', 'file'])
                    else:
                        df = pd.DataFrame([[i,math.degrees(angle), filename]], columns=['projection','angle', 'file'])
                        filelist = filelist.append(df,ignore_index=True)
                    Write_Filelist(filepath,filelist)
                    print(shape)
                    img = np.array(img)
                    img = np.reshape(img,shape)
                    img = pp.bkg_correct(img)
                    img = pp.bkg_mask(img)
                    img = pp.square_image(img)
                    img = pp.center(img)
                    if i > 1:
                        shift = pp.align(img,img_old)
                        img = np.roll(img, -shift, (0, 1))
                    img_old = img
                    if i == 1:
                        img_array = img
                    else:
                        img_array = np.dstack([img_array,img])
                    Update_Reconstruction(pub, args, filelist,img_array)
                    
        filelist = filelist.sort_index()
        if reset == True:
            print('Reconstruction Updated')
            for item in filelist:
                update_reconstruction(filelist,img_array)
            if os.exists(resetpath):
                os.remove(resetpath)
            reset = False



