import tkinter as tk
import os 
import pandas as pd
from recastgui.structs import enums

class Panel():
    def __init__(self, controller, window, count):
        # Controller
        self.controller = controller
        self.window = window
        self.index = count-1
                
        # Tkinter Variables
        self.id = tk.StringVar()
        self.filetype = tk.StringVar()
        self.use = tk.BooleanVar()
        self.use.set(True)
        self.align = tk.BooleanVar()
        if self.index == 0:
            self.align.set(True)
            
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.frame, 
            borderwidth=0, 
            height=100, 
            width = self.window.width-2*self.window.padx)
        
        
        self.remove_button = tk.Button(self.frame, text="Remove", command=self.RemoveData)
        self.id_label = tk.Label(self.frame, text = "Signal:")
        self.id_entry = tk.Entry(self.frame,textvariable=self.id)
        self.type_label = tk.Label(self.frame, text = "Data Type:")
        self.type_menubutton = self.GetMenuButton()
        self.use_button = tk.Checkbutton(self.frame, text='reconstruct?', variable=self.use, command = self.SelectReconstructedSignal)
        self.align_button = tk.Checkbutton(self.frame, text='Allign to?', variable=self.align, command = self.SelectAlignmentSignal)
        
        for j in enums.ProjectionType:
            self.type_menubutton.menu.add_radiobutton(label=j.value, variable=self.filetype, value=j.value, command=self.SelectDataType)
        self.type_menubutton['menu']=self.type_menubutton.menu

        #Build Frame
        self.BuildFrame()
        
    def SelectReconstructedSignal(self):
        self.controller.SelectReconstructedSignal(self.index)
    
    def SelectAlignmentSignal(self):
        self.controller.SelectAlignmentSignal(self.index)
        
    def SelectDataType(self):
        self.type_menubutton['text']= self.filetype.get()

    def RemoveData(self):
        self.frame.grid_forget()
        self.controller.RemoveData(self.index)

    def GetMenuButton(self):
        button = tk.Menubutton(self.frame, text="Choose File", relief='raised')
        button.grid()
        button.menu = tk.Menu(button,tearoff = 0)
        return button
        
    def PopulateFrame(self, args):
        self.id.set(args['name'][self.index])
        self.filetype.set(args['type'][self.index])
        self.SelectDataType()
        self.use.set(args['reconstruct'][self.index].item())
        self.align.set(args['align'][self.index].item())
        
    def BuildFrame(self):
        # Build Frame
        self.frame.grid(row=self.index+2, column=0, columnspan=5)
        
        # Build Widgets
        self.remove_button.grid(row=0, column=0, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.id_label.grid(row=0, column=1, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.id_entry.grid(row=0, column=2, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.type_label.grid(row=0, column=3, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.type_menubutton.grid(row=0, column=4, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.use_button.grid(row=0, column=5, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.align_button.grid(row=0, column=6, sticky='W', padx=self.window.padx, pady=self.window.pady)
        
    def Parse(self):
        self.args = self.Args(self)
        return self.Args(self)

    # Passable Variables
    class Args():
        def __init__(self, controller):
            self.id = controller.id.get()
            self.filetype =  controller.filetype.get()
            self.use =  controller.use.get()
            self.align = controller.align.get()

