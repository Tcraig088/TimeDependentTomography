import os
import numpy as np
import pandas as pd
import csv

def GetDelimit():
    return '\t'
    
def Read(path):
    line =''
    with open(path, 'r') as f:
        line = f.readline()
    return line
        
def Write(path, reset_bool):
    if reset_bool:
        with open(path, 'w') as f:
            f.write('reset')
            
