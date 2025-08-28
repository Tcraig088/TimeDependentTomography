import pandas as pd 

import matplotlib.pyplot as plt
import multiprocessing as mp
import time
import matplotlib
import numpy as np
import slicerecon
import copy
from structs.enums import PluginType as PT
import sklearn.preprocessing as pp
from plugins import beam_analysis as ba

class Handler():
    def __init__(self, args, processes):
        self.args = args
        #matplotlib.use('GTK4Agg')
        #print(matplotlib.get_backend())
        self.callback_data = [None]*len(self.args.plugins.plugins)
        
        self.plot_pipe = args.plot_pipe
        self.plotter_pipe = args.plotter_pipe
        self.plotter = args.plotter
        self.plot_process = processes.t4

        p = slicerecon.plugin("tcp://*:5652", "tcp://localhost:5555")
        p.set_slice_callback(self.callback)
        p.listen()
         
    def callback(self, orientation, shape, img, _):
        for index, row in self.args.plugins.plugins.iterrows():
            identifier=row['name']
            match identifier:
                case PT.BeamDamage.value:
                    self.callback_data[index], orientation, shape, img = ba.callback(self.args,self.callback_data[index], orientation,shape,img)
                    send = self.plot_pipe.send
                    if hasattr(self.callback_data[index], "df") and self.callback_data[index].nslices==0:
                        df = self.callback_data[index].df.iloc[-1]
                        img_new=copy.deepcopy(self.callback_data[index].img_new)
                        img_old=copy.deepcopy(self.callback_data[index].img_old)
                        for i in range(len(img_new)):
                            img_new[i]=np.reshape(img_new[i],shape)
                            img_old[i]=np.reshape(img_old[i],shape)
                        data = [df['projections'], 
                            df['snr'], 
                            df['srod'],
                            img_new[0],
                            img_new[1],
                            img_new[2], 
                            img_old[0],
                            img_old[1],
                            img_old[2]]
                        send(data)
                        #print(df['projections'],df['srod'],df['pdinit'],df['pdaverage'])
                    
                case _:
                    print('undefined plugin')
        return [orientation, shape, img]
    
