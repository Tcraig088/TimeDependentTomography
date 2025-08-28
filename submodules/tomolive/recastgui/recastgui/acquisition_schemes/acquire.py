import math
import pandas as pd
import numpy as np
import os
import time
import tomop
import script
import shutil

from process_handlers import projection as pp

def Read(args):
    # Register preexisting geometry
    fh = pp.Handler(args)
    #TODO Dont hard code the ports
    #pub = tomop.publisher(args.host, args.port)
    pub = tomop.publisher("localhost", 5558)
    #j = 1
    time.sleep(30)
    while(True):
        time.sleep(1)
        #if j>=1 and j<=71:
         #   path = str(j)+'_.tiff'
          #  path1 = 'sim_'+str(j)+'_.tiff'
           # x = args.data.path.split('/')
            #src = '/home/recast/Documents/Test-Data/GRS-Simulations/nanostar-2'
            #if os.path.exists(os.path.join(src, path)):
             #   shutil.copy2(os.path.join(src, path), os.path.join(args.data.path,path1)) 
        fh.Update()
        if fh.tiltseries.nproj == fh.target.nproj:
            dim = fh.target.dimx
            nsignals = fh.target.nsignals
            count =  fh.target.nproj
        
            # Set Up Geometry
            #TODO make work with non square geometry 
            geom_spec = tomop.geometry_specification_packet(0, [-dim / 2, -dim / 2, -dim / 2],[dim / 2, dim/2, dim/ 2])
            pub.send(geom_spec)
            #TODO make work with multimode 
            #par_beam = tomop.parallel_beam_geometry_packet(0, dim, dim, nsignals, int(count), fh.tiltseries.angles_rad)
            par_beam = tomop.parallel_beam_geometry_packet(0, dim, dim, int(count), fh.tiltseries.angles_rad)
            pub.send(par_beam)
            #Honestly dont know why it exists but linearize defaulted true
            scan_set = tomop.scan_settings_packet(0, 0, 0, True)
            pub.send(scan_set)
        
            for i in range(fh.tiltseries.nproj):
                img = fh.tiltseries.data[i]
                #TODO make work with multimode 
                #projection = tomop.projection_packet(2, fh.tiltseries.angles[i], [dim, dim, nsignals], np.ascontiguousarray(img.ravel()))
                proj = tomop.projection_packet(2, fh.tiltseries.index[i], [dim, dim], np.ascontiguousarray(img.ravel()))
                pub.send(proj)
            fh.target.nproj = fh.target.nproj+1
            #j= j+1



