import tkinter as tk
import os 
from tkinter import filedialog

class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
                
        # Tkinter Variables
        self.gaussian = tk.BooleanVar()
        self.tilt = tk.BooleanVar()
        self.path = tk.StringVar()
        
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            text='Data Settings', 
            borderwidth=self.controller.window.padx, 
            height=200, 
            width = self.controller.window.width)
    
                
        self.file_label = tk.Label(self.frame, text = "Filter (Default Ram-Lak):") 
        self.file_entry = tk.Entry(self.frame,textvariable=self.path)
        self.file_button = tk.Button(self.frame, text="Browse Files",command=self.GetPath)
        
        self.gaussian_button = tk.Checkbutton(self.frame, text='Gaussian Filter?', variable=self.gaussian)
        self.tilt_button = tk.Checkbutton(self.frame, text='Align Tilt Axis (Manuel)?', variable=self.tilt)

    def GetPath(self):
        self.path.set(filedialog.askopenfilename())
        
    def ClearFrame(self):
        self.gaussian.set(False)
        self.tilt.set(False)
        self.path.set("")

    def PopulateFrame(self, args):
        self.gaussian.set(args.gaussian)
        self.tilt.set(args.tilt)
        
    def BuildFrame(self):
        # Build Frame
        self.frame.pack(fill='x', expand=True)
        
        #Populate Frame
        self.file_label.grid(row=0, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.file_entry.grid(row=0, column=1, columnspan=3, sticky='W'+'E', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.file_button.grid(row=0, column=4, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        
        self.gaussian_button.grid(row=1, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.tilt_button.grid(row=1, column=1, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
    
    def PrintArgs(self):
        print(" ")
        print("Reconstruction:")
        if self.args.filter == "":
            print("Using Ram-Lak Filter")
        else:
            print("Using "+self.args.filter) 
            print("Check Filter is Compatible with the reconstruction setting ") 
        if self.args.gaussian == True:
            print("applying gaussian filter")
        if self.args.tilt == True:
            print("applying maunel tilt axis alignment")

    def Parse(self):
        self.args = self.Args(self)
        return self.args

    # Passable Variables
    class Args():
        def __init__(self, controller):
            self.filter = controller.path.get()
            self.gaussian = controller.gaussian.get()
            self.tilt = controller.tilt.get()

