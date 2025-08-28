import pandas as pd 
import numpy as np
import hyperspy.api as hp 
from recastgui.structs import enums
#Image Processing 
from PIL import Image
#import ser_parser
import csv

class Handler():
    def __init__(self):
        self.sernum = 1
       
    def GetID(self, name, filetype):
        identifier = ''
        print('Hello')
        print(filetype, enums.ProjectionType.EMI.value)
        match filetype:
            case enums.ProjectionType.EMI.value:
                identifier = '_'+str(self.sernum)+'.ser'
                self.sernum = self.sernum + 1
            case _:
                identifier = name
        return identifier

