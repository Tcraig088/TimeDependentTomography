import tkinter as tk
import os 
from recastgui.structs import enums 

class Panel():
    def __init__(self, controller, window, count):
        # Controller
        self.controller = controller
        self.window = window
        self.index = count-1
                
        # Tkinter Variables
        self.alignment_type = tk.StringVar()
            
        #Define Frame
        self.frame =  tk.LabelFrame(self.controller.frame, 
            borderwidth=0, 
            height=100, 
            width = self.window.width-2*self.window.padx)
        
        self.remove_button = tk.Button(self.frame, text="Remove", command=self.RemoveData)
        self.alignment_label = tk.Label(self.frame, text = "Signal:")
        self.alignment_menubutton = self.GetMenuButton()

        for j in enums.AlignmentType:
            self.alignment_menubutton.menu.add_radiobutton(label=j.value, variable=self.alignment_type, value=j.value, command=self.SelectDataType)
        self.alignment_menubutton['menu']=self.alignment_menubutton.menu

        #Build Frame
        self.BuildFrame()

    def SelectDataType(self):
        self.alignment_menubutton['text']= self.alignment_type.get()
        #TODO create alignment settings for funky alignment types
        
    def RemoveData(self):
        self.frame.grid_forget()
        self.controller.RemoveData(self.index)

    def GetMenuButton(self):
        button = tk.Menubutton(self.frame, text="Choose File", relief='raised')
        button.grid()
        button.menu = tk.Menu(button,tearoff = 0)
        return button
        
    def PopulateFrame(self, args):
        self.alignment_type.set(args.type)
        self.SelectDataType()

    def BuildFrame(self):
        # Build Frame
        self.frame.grid(row=self.index+2, column=0, columnspan=5)
        
        # Build Widgets
        self.remove_button.grid(row=0, column=0, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.alignment_label.grid(row=0, column=1, sticky='W', padx=self.window.padx, pady=self.window.pady)
        self.alignment_menubutton.grid(row=0, column=4, sticky='W', padx=self.window.padx, pady=self.window.pady)

    def Parse(self):
        self.args = self.Args(self)
        return self.Args(self)

    # Passable Variables
    class Args():
        def __init__(self, controller):
            self.alignment_type =  controller.alignment_type.get()

