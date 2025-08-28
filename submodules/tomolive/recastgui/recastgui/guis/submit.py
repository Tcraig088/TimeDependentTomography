import tkinter as tk
import os
import sys

class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
        
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            borderwidth=self.controller.window.padx, 
            height=100, 
            width = self.controller.window.width)
        
        self.submit_button = tk.Button(self.frame, text ="Submit", command = self.Launch)
        self.close_button = tk.Button(self.frame, text ="Close", command = self.End)
        
    def BuildFrame(self):
        # Build Frame
        #self.frame.grid(row=position, column=0, padx = self.controller.window.padx, pady = self.controller.window.pady)
        #self.frame.grid_propagate(0)
        self.frame.pack(fill='x', expand=True)
        # Populate Frame
        self.submit_button.grid(row=0, column=0, sticky = 'W', padx = self.controller.window.padx, pady = self.controller.window.pady)
        self.close_button.grid(row=0, column=1, sticky = 'W', padx = self.controller.window.padx, pady = self.controller.window.pady)
        
    def Launch(self):
        self.controller.Parse()
        self.controller.PrintArgs()
        self.controller.processes = self.controller.Processes(self.controller)
        self.controller.processes.Start()
        
    def End(self):
        self.controller.processes.End()
        self.controller.gui.destroy()
