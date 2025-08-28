import pandas as pd 
import numpy as np
import hyperspy.api as hp 

#Image Processing 
from PIL import Image
#import ser_parser
import csv

data_types = ['emi/ser','edx txt', 'edx bcf','tiff']

def ReadProjection(filename, filetype):
    match filetype:
        case 'emi/ser':
            (m, n), proj = ser_parser.parser(filename)
            return np.reshape(proj, (m,n))
        case 'edx/txt':
            df = pd.read_csv(filename,sep=';',header=None)
            return df.to_numpy()
        case 'edx/bcf':
            #TODO Populate with Correct read function
            return np.array(Image.open(os.path.join(args.path,filename)))
        case 'tiff':
            return np.array(Image.open(os.path.join(args.path,filename)))

class ProjectionHandler():
    def __init__(self):
        self.sernum = 1
       
    def GetID(self, name, filetype):
        identifier = ''
        match filetype:
            case 'emi/ser':
                identifier = '_'+str(self.sernum)+'.ser'
                self.sernum = self.sernum + 1
            case 'edx/txt':
                identifier = name
            case 'edx/bcf':
                identifier = name
            case 'tiff':
                identifier = name
            case _:
                identifier = name
        return identifier

