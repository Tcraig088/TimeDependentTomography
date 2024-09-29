# i need an argument parser
import argparse
import socket

from  tdcontroller.log import logger
from tdcontroller.controller import MicroscopeController


class StoreWithDefault(argparse.Action):
    def __init__(self, option_strings, dest, default=None, required=False, help=None, metavar=None):
        super().__init__(option_strings=option_strings, dest=dest, nargs=1, default=default, required=required, help=help, metavar=metavar)
        self.explicitly_set = False

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values[0])
        setattr(namespace, f"{self.dest}_explicitly_set", True)

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--setup',
                        action='store_true',
                        help='setup the microscope')
    
    parser.add_argument('--reply', 
                        metavar='REP', 
                        type=int, 
                        help='the socket to reply on', 
                        default=50031,
                        action=StoreWithDefault)
    
    parser.add_argument('--publisher', 
                        metavar='PUB', 
                        type=int, 
                        help='the socket to publish on', 
                        default=50030,
                        action=StoreWithDefault)
    
    parser.add_argument('--manufacturer',
                        metavar='MANU',
                        type=str,
                        help='the microscope manufacturer',
                        default='FEI',
                        action=StoreWithDefault)
    
    parser.add_argument('--detectors' ,
                        metavar='DETECTORS',
                        type=str,
                        nargs='+',
                        help='the detectors',
                        default=['HAADF', 'DF2', 'DF4', 'BF'],
                        action=StoreWithDefault)
    
    parser.add_argument('--magnifications',
                        metavar='MAGNIFICATIONS',
                        type=int,
                        nargs='+',
                        help='the magnifications',
                        default=[1000, 2000, 5000, 10000],
                        action=StoreWithDefault)
    
    parser.add_argument('--detectorpixel',
                        metavar='PIXEL_SIZE',
                        type=float,
                        help='the detector pixel size',
                        default=0.001,
                        action=StoreWithDefault)

    args = parser.parse_args()
    microscope_controller = MicroscopeController(args)


