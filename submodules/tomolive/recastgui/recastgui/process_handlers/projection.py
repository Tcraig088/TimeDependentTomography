import os 
import pandas as pd 
from structs import enums, classes
from process_handlers import alignment
from read_write import rec, regtext

class Handler():
    def __init__(self, args):
        self.args = args
        self.tiltseries = classes.TiltSeries(args)
        self.target = classes.Target(args)
        self.status = enums.ProjectionHandlerState.Initialized
        
        #File Names 
        self.path = self.args.data.path
        self.save = os.path.join(args.data.path, 'save.rec')
        self.reg = os.path.join(args.data.path, 'files.csv')
        regtext.Write(self.reg, 0)
        
        self.alignh = alignment.Handler(args)
        
        self.filename = ''
        
    def Update(self):
        self.GetStatus()
        
        match self.status:
            case enums.ProjectionHandlerState.Saved:
                self.tiltseries = rec.Read(self.save)
                self.filelist = regtext.Read(self.reg)
                self.target.Update(self.tiltseries)
                self.status = enums.ProjectionHandlerState.Checked
            case enums.ProjectionHandlerState.Registered:
                self.filelist = regtext.Read(self.reg)
                if not self.filelist.empty:
                    if self.tiltseries.nproj == 0:
                        print(self.filelist)
                    index = self.tiltseries.nproj
                    projection = classes.Projection(self.path, self.filelist.file[index], self.args)
                    self.tiltseries = self.alignh.Align(self.tiltseries, projection)
                self.target.Update(self.tiltseries)
                if self.tiltseries.nproj == len(self.filelist):
                    self.status = enums.ProjectionHandlerState.Checked
            case enums.ProjectionHandlerState.NewData:
                projection = classes.Projection(self.path, self.filename, self.args)
                regtext.Write(self.reg, projection)
                self.filelist = regtext.Read(self.reg)
                self.tiltseries = self.alignh.Align(self.tiltseries, projection)
                self.target.Update(self.tiltseries)
                self.status = enums.ProjectionHandlerState.Checked
            case enums.ProjectionHandlerState.SaveRequested:
                rec.Write(self.save, self.tiltseries)
                self.target.Update(self.tiltseries)
                self.status = enums.ProjectionHandlerState.Checked
            case enums.ProjectionHandlerState.ResetRequested:
                #rec.Write(self.save, self.tiltseries)
                self.target = classes.Target(self.args)
                self.tiltseries = classes.TiltSeries(self.args)
                self.status = enums.ProjectionHandlerState.Initialized
        
    def GetStatus(self):
        if self.status == enums.ProjectionHandlerState.Initialized:
            if os.path.exists(self.save):
                self.status =  enums.ProjectionHandlerState.Saved
            else:
                self.status =  enums.ProjectionHandlerState.Registered
        if self.status == enums.ProjectionHandlerState.Checked:
            path = os.path.join(self.args.data.path,'reset.txt')
            if os.path.exists(path):
                with open(path, 'r') as f:
                    line = f.readline()
                    if "reset" in line:
                        self.status = enums.ProjectionHandlerState.ResetRequested
                    else:
                        self.status = enums.ProjectionHandlerState.SaveRequested
                os.remove(path)
            else:
                for filename in os.listdir(self.args.data.path):
                    for idx, row in self.args.data.signals.iterrows():
                        if row['identifier'] in filename:
                            found = self.filelist['file'].eq(filename).any()
                            if not found:
                                self.status = enums.ProjectionHandlerState.NewData 
                                self.filename = filename
    

