import tkinter as tk
import os 
import recastgui.guis.plugin_entry as plugin_entry
import pandas as pd
from recastgui.plugins import plugin

class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
                
        # Tkinter Variables
        self.data = []
        self.count = 0
        
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            text='Plugin Settings', 
            borderwidth=self.controller.window.padx, 
            height=200, 
            width = self.controller.window.width)
        
        self.add_button = tk.Button(self.frame, text ="Add", command = self.AddData)

        
    def AddData(self):
        self.count = self.count + 1
        self.data.append(plugin_entry.Panel(self, self.controller.window, self.count))
        self.data[-1].BuildFrame()
        
    def RemoveData(self, row):
        del self.data[row]
        self.count = self.count -1
        for i in range(row,self.count):
            self.data[i].index=self.data[i].index-1

    def ClearFrame(self):
        for i in range(len(self.data)):
            self.data[i].RemoveData()
            
    def PopulateFrame(self, args):
        for i in range(len(args.plugins)):
            self.AddData()
            self.data[i].PopulateFrame(args.plugins[i])
        
    def BuildFrame(self):
        # Build Frame
        self.frame.pack(fill='x', expand=True)
        #Populate Frame
        self.add_button.grid(row=1, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)

    def PrintArgs(self):
        print(" ")
        print("Plugins:")
        print(self.args.plugins)

    def Parse(self):
        self.args = self.Args(self)
        return self.args

    # Passable Variables
    class Args():
        def __init__(self, controller):
            names = []
            for i in range(controller.count):
                val = controller.data[i].Parse()
                names.append(val.plugin)
            self.plugins = pd.DataFrame(data={'name':names})
