import tkinter as tk
import os 
import sys
import pickle

from threading import Thread
from multiprocessing import Process, Pipe

from recastgui.guis import window, acquisition, data, alignment, reconstructor, plugin, submit, settings
from recastgui.plugins import plugin as plugin_exe
from recastgui.acquisition_schemes import acquire
from recastgui.plotter.plotter import ProcessPlotter

class RECASTLauncher():
    def __init__(self):
        
        #Window Settings
        self.gui = tk.Tk()
        self.gui.title('RECAST Launcher')
        self.window = window.Window(self)
        
        #panels
        self.settings_frame = settings.Panel(self)
        self.data_frame = data.Panel(self)
        self.acquisition_frame = acquisition.Panel(self)
        self.alignments_frame = alignment.Panel(self)
        self.reconstructor_frame = reconstructor.Panel(self)
        self.plugins_frame = plugin.Panel(self)
        self.submit_frame = submit.Panel(self) 
        
        self.plot_pipe, self.plotter_pipe = Pipe()
        self.plotter = ProcessPlotter()
        
        self.BuildGui()
        
    def Start(self):
        self.gui.mainloop()
        
    def End(self):
        self.t1.terminate()
        self.t2.terminate()
        self.t3.terminate()
        self.t4.terminate()
        self.t5.terminate()
        self.gui.destroy()
    
    def BuildGui(self):
        self.settings_frame.BuildFrame()
        self.data_frame.BuildFrame()
        self.acquisition_frame.BuildFrame()
        self.alignments_frame.BuildFrame()
        self.reconstructor_frame.BuildFrame()
        self.plugins_frame.BuildFrame()
        self.submit_frame.BuildFrame()
        
    def Parse(self):
        self.args = self.Args(self)
        
    def Bash_Start_Recast(self):
        self.BashCMD('./recast3d')
        
    def Bash_Start_SliceRecon(self):
        if self.args.reconstructor.gaussian:
            gaussian = ' --gaussian'
        else:
            gaussian = ''
        if self.args.reconstructor.tilt:
            tilt = ' --tilt'
        else:
            gaussian = ''
            tilt = ''
        self.BashCMD('./slicerecon_server --pyplugin --filter'+ self.args.reconstructor.filter +' '+ gaussian + tilt)

    def BashCMD(self,path):
        dirpath = os.path.dirname(sys.executable)
        if dirpath.find('bin') != -1:
            dirpath = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dirpath,'bin',path)
        cmd_string = 'gnome-terminal --tab -- /bin/bash -c "' + path + '; bash"'
        os.system(cmd_string)
    
    def Plugin_Start(self):
        plugin_exe.Handler(self.args, self.processes)

    def Adapter_Start(self):
        acquire.Read(self.args)
    
    def SaveSettings(self):
        with open(self.settings_frame.path.get(), 'wb') as f:
            self.Parse()
            self.PrintArgs()
            pickle.dump(self.args, f)

    def LoadSettings(self):
        with open(self.settings_frame.path.get(), 'rb') as f:
            args = pickle.load(f)
        
        self.data_frame.args = args.data
        self.acquisition_frame.args = args.acquisition
        self.alignments_frame.args = args.alignments
        self.reconstructor_frame.args = args.reconstructor
        self.plugins_frame.args = args.plugins
        
        self.PrintArgs()
        
        self.data_frame.ClearFrame()
        self.acquisition_frame.ClearFrame()
        self.alignments_frame.ClearFrame()
        self.reconstructor_frame.ClearFrame()
        self.plugins_frame.ClearFrame()
        
        self.data_frame.PopulateFrame(args.data)
        self.acquisition_frame.PopulateFrame(args.acquisition)
        self.alignments_frame.PopulateFrame(args.alignments)
        self.reconstructor_frame.PopulateFrame(args.reconstructor)
        self.plugins_frame.PopulateFrame(args.plugins)
        
    def PrintArgs(self):
        print("Passing Arguements:")
        self.data_frame.PrintArgs()
        self.acquisition_frame.PrintArgs()
        self.alignments_frame.PrintArgs()
        self.reconstructor_frame.PrintArgs()
        self.plugins_frame.PrintArgs()

        
    class Args():
        def __init__(self,controller):
            self.acquisition = controller.acquisition_frame.Parse()
            self.data = controller.data_frame.Parse()
            self.alignments = controller.alignments_frame.Parse()
            self.reconstructor = controller.reconstructor_frame.Parse()
            self.plugins = controller.plugins_frame.Parse()
            self.plot_pipe = controller.plot_pipe
            self.plotter_pipe = controller.plotter_pipe
            self.plotter = controller.plotter
            
    class Processes():
        def __init__(self,controller):
            #Subprocesses
            self.t1 = Process(target=controller.Bash_Start_Recast) 
            self.t2 = Process(target=controller.Bash_Start_SliceRecon)
            self.t3 = Process(target=controller.plotter, args=(controller.plotter_pipe,), daemon=True)
            self.t4 = Process(target=controller.Plugin_Start)
            self.t5 = Process(target=controller.Adapter_Start)
        
        def Start(self):
            self.t1.start()
            self.t2.start()
            self.t3.start()
            self.t4.start()
            self.t5.start()
            
            self.t1.join()
            self.t2.join()
            self.t3.join()
            self.t4.join()
            self.t5.start()
            
        def End(self):
            self.t1.kill()
            self.t2.kill()
            self.t3.kill()
            self.t4.kill()
            self.t5.start()

