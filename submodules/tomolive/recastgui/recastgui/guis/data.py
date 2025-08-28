import tkinter as tk
import os 
import pandas as pd 
from tkinter import filedialog

import recastgui.read_write.projections as rw
from recastgui.process_handlers import signalid
import recastgui.guis.data_entry as data_entry


class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
                
        # Tkinter Variables
        self.path = tk.StringVar()
        self.data = []
        self.count = 0
        
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            text='Data Settings', 
            borderwidth=self.controller.window.padx, 
            height=200, 
            width = self.controller.window.width)
        
        self.folder_label = tk.Label(self.frame, text = "Data Folder:") 
        self.folder_entry = tk.Entry(self.frame,textvariable=self.path)
        self.folder_button = tk.Button(self.frame, text="Browse Folder",command=self.GetDataPath)
        
        self.add_button = tk.Button(self.frame, text ="Add", command = self.AddData)

        
    def AddData(self):
        self.count = self.count + 1
        self.data.append(data_entry.Panel(self, self.controller.window, self.count))
        self.data[-1].BuildFrame()
        
    def RemoveData(self, row):
        del self.data[row]
        self.count = self.count -1
        for i in range(row,self.count):
            self.data[i].index=self.data[i].index-1
            
    def SelectReconstructedSignal(self,row):
        count = 0
        for entry in self.data:
            if entry.use ==True:
                count = count+1
        
        if count > 2:
            self.data[0].use.set(True)
            self.SelectAlignmentSignal(0)
            
        if self.data[row].align.get() == True and self.data[row].use.get() == False:
            self.data[row].align.set(False)
            for i in range(len(self.data)):
                if self.data[i].use.get() == True:
                    self.SelectAlignmentSignal(i)
                    break
    
    def SelectAlignmentSignal(self,row):
        if self.data[row].use.get() == True:
            if self.data[row].align.get() == False:
                self.data[row].align.set(True)
            for i in range(self.count):
                if i != row:
                    self.data[i].align.set(False)
        else:
            self.data[row].align.set(False)
            
    def GetDataPath(self):
        self.path.set(filedialog.askdirectory())

            
    def ClearFrame(self):
        self.path.set("")
        for i in range(len(self.data)):
            self.data[i].RemoveData()
            
    def PopulateFrame(self, args):
        self.path.set(args.path)
        for i in range(len(args.signals)):
            self.AddData()
            self.data[i].PopulateFrame(args.signals)
        
    def BuildFrame(self):
        # Build Frame
        self.frame.pack(fill='x', expand=True)
        #Populate Frame
        self.folder_label.grid(row=0, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.folder_entry.grid(row=0, column=1, columnspan=3, sticky='W'+'E', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.folder_button.grid(row=0, column=4, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)

        self.add_button.grid(row=1, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        
        self.AddData()
        
    def PrintArgs(self):
        print(" ")
        print("Data:")
        print("Path: " + self.args.path)
        print("Signals")
        print(self.args.signals)

    def Parse(self):
        self.args = self.Args(self)
        return self.args

    # Passable Variables
    class Args():
        def __init__(self, controller):
            self.path =  controller.path.get()
            filetypes = []
            names = []
            ids =[]
            use = []
            align =[]
            ph = signalid.Handler()
            for i in range(controller.count):
                signal = controller.data[i].Parse()
                filetypes.append(signal.filetype)
                names.append(signal.id)
                ids.append(ph.GetID(signal.id, signal.filetype))
                use.append(signal.use)
                align.append(signal.align)
            self.signals = pd.DataFrame(data={'name':names, 'identifier':ids, 'type':filetypes, 'reconstruct':use, 'align':align})



