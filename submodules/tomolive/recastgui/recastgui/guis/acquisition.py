import tkinter as tk
import os 

class Panel():
    def __init__(self, controller):
        # Controller
        self.controller = controller
                
        # Tkinter Variables
        self.start = tk.DoubleVar()
        self.end =  tk.DoubleVar()
        self.step = tk.DoubleVar()
        self.grs =  tk.BooleanVar()

        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.gui, 
            text='Acquisition Settings', 
            borderwidth=self.controller.window.padx, 
            height=200, 
            width = self.controller.window.width)
        
        self.start_label = tk.Label(self.frame, text = "Start Angle:") 
        self.start_entry = tk.Entry(self.frame,textvariable=self.start)
        
        self.end_label = tk.Label(self.frame, text = "End Angle:") 
        self.end_entry = tk.Entry(self.frame,textvariable=self.end)
        
        self.step_label = tk.Label(self.frame, text = "Tilt Increment:") 
        self.step_entry = tk.Entry(self.frame,textvariable = self.step)
        
        self.grs_button = tk.Checkbutton(self.frame, text='grs?', variable=self.grs)

    def BuildFrame(self):
        # Build Frame
        self.frame.pack(fill='x', expand=True)
        
        #Populate Frame
        self.start_label.grid(row=0, column=0, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.start_entry.grid(row=0, column=1, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.end_label.grid(row=0, column=2, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.end_entry.grid(row=0, column=3, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        
        self.step_label.grid(row=1, column=0, columnspan = 2, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.step_entry.grid(row=1, column=1, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)
        self.grs_button.grid(row=1, column=2, sticky='W', padx=self.controller.window.padx, pady=self.controller.window.pady)

    def ClearFrame(self):
        self.start.set(0.0)
        self.end.set(0.0)
        self.step.set(0.0)
        self.grs.set(False)
        self.img_size.set(0)
        self.pixel_size.set(1)
            
    def PopulateFrame(self, args):
        self.start.set(args.start)
        self.end.set(args.end)
        self.step.set(args.step)
        self.grs.set(args.grs)
        self.img_size.set(args.img_size)
        self.pixel_size.set(args.pixel_size)
            
    def PrintArgs(self):
        print(" ")
        print("Acquisition:")
        if self.args.grs == True:
            print("\t Acquire GRS from " + str(self.args.start) + " to " + str(self.args.end))
        else:
            print("\t Acquire from " + str(self.args.start) + "to " + str(self.args.end) + "with steps of " + str(self.args.step))

    def Parse(self):
        self.args = self.Args(self)
        return self.args

    # Passable Variables
    class Args():
        def __init__(self, controller):
            self.start =  controller.start.get()
            self.end =  controller.end.get()
            self.step = controller.step.get()
            self.grs = controller.grs.get()

