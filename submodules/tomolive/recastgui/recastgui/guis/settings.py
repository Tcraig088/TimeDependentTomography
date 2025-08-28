
import tkinter as tk
import os 
import read_write.projections as rw
import guis.data_entry as data_entry
import pandas as pd 
from tkinter import filedialog

class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
                
        # Tkinter Variables
        self.path = tk.StringVar()

        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            text='Load/Save Reconstruction Settings', 
            borderwidth=self.controller.window.padx, 
            height=200, 
            width = self.controller.window.width)
        
        self.file_label = tk.Label(self.frame, text = "Load/Save File (.txt):") 
        self.file_entry = tk.Entry(self.frame,textvariable=self.path)
        self.file_button = tk.Button(self.frame, text="Browse Files",command=self.GetPath)
        
        self.save_button = tk.Button(self.frame, text="Save",command=self.controller.SaveSettings)
        self.load_button = tk.Button(self.frame, text="Load",command=self.controller.LoadSettings)

    def GetPath(self):
        self.path.set(filedialog.askopenfilename())
        
    def BuildFrame(self):
        # Build Frame
        self.frame.pack(fill='x', expand=True)
        #Populate Frame
        self.file_label.grid(row=0, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.file_entry.grid(row=0, column=1, columnspan=3, sticky='W'+'E', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.file_button.grid(row=0, column=4, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.save_button.grid(row=0, column=5, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.load_button.grid(row=0, column=6, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)

