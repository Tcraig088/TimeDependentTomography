import os 
import pandas as pd 
import numpy as np
import hyperspy.api as hs
from structs.enums import ProjectionType as PT

class Projection():
    def __init__(self, path ,filename, args):
        df = args.data.signals
        filetype = ''
        self.signal = ''
        self.filename = filename
        self.identifier = ''
        self.angle = 0
        
        for item, row in df.iterrows():
            if row.identifier in self.filename:
                self.identifier = row.identifier
                self.signal = row['name']
                filetype = row['type']
        match filetype:
            case PT.EMI.value:
                name = filename.split('_')
                path = os.path.join(path, name[0]+'.emi')
                val = hs.load(path)
                self.data = val.data
                self.angle = val._metadata.Acquisition_instrument.TEM.Stage.tilt_alpha
                #TODO determine ser file extension
            case PT.TIFF.value:
                path = os.path.join(path,filename)
                val = hs.load(path)
                text = filename.split("_")
                text = text[1].split('.')
                self.data = val.data
                if args.acquisition.grs:
                    ang_range = np.radians(args.acquisition.end-args.acquisition.start)
                    gr = (1.0+np.sqrt(5.0))/2.0
                    self.angle = np.mod(ang_range*float(text[0])*gr,ang_range) + np.radians(args.acquisition.start)
                    self.angle = np.round(np.degrees(self.angle),2)
                else:
                    self.angle=args.acquisition.step*(float(text[0])-1)+args.acquisition.start
            case _:
                path = os.path.join(path,filename)
                self.val = hs.load(path)
                
class TiltSeries():
    def __init__(self, args):
        self.angles = np.zeros(0)
        self.angles_rad = np.zeros(0)
        self.data = np.zeros(0)
        self.index = np.zeros(0)
        self.nproj = 0
        self.nsignals = len(args.data.signals)

class Target():
    def __init__(self, args):
        self.dimx = 0
        self.dimy = 0
        self.nproj = 1
        self.nsignals = len(args.data.signals[args.data.signals['reconstruct'] == True].index.values)
        
    def Update(self, tiltseries):
        if self.dimx == 0 and self.dimy == 0:
            if tiltseries.nproj != 0:
                shape = np.shape(tiltseries.data[0])
                self.dimx = shape[0]
                self.dimy = shape[1] 
                

