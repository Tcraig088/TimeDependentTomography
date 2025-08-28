import tkinter as tk
import os 
import sys

class Window():
    def __init__(self, controller):
        self.gui = controller.gui
        
        self.height =1100
        self.width = 1800
        
        self.subframe_height = self.height - 100
        self.subframe_width = self.width - 100
        
        self.padx = 5
        self.pady = 5

        #self.gui.geometry(str(self.width)+'x'+str(self.height))
        
        #def ResizeWindow(self,height,width)
        
        
