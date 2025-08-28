import numpy as np
import pandas as pd
import csv

def Read(path):
    return pd.read_csv(path, delimiter=self.delimit)
        
def Write(path, projection):
    if projection == 0:
        if not os.path.exists(path):
            with open(path, 'a') as f:
                writer = csv.writer(f, delimiter= self.delimit)
                row =['file', 'angle', 'signal', 'pid']
                writer.writerow(row)
    else:
        filelist = pd.read_csv(path, delimiter=self.delimit)
        pid = 0
        for item in filelist:
            if projection.signal == item.signal:
                pid = item.pid+1 
        with open(path, 'w') as f:
            writer = csv.writer(f, delimiter=self.delimit)
            row =[projection.filename, projection.angle, projection.signal, pid]
            writer.writerow(row)
