from tdcontroller.log import logger
import json
import importlib
import os
import socket
import zmq

class MicroscopeController():
    def __init__(self, args):
        self.args = args

        host = socket.gethostname()
        ipaddress = socket.gethostbyname(host)
        logger.info('ip address:' + ipaddress)
        spec = importlib.util.find_spec('tdcontroller')
        if spec is None or spec.origin is None:
            raise ImportError("Cannot find the 'tdcontroller' package")
        
        tdcontroller_path = os.path.dirname(spec.origin)
        json_file = os.path.join(tdcontroller_path, 'settings.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                self.settings = json.load(f)
            if args.setup:
                if getattr(args, 'reply_explicitly_set', True):  
                    self.settings['reply'] = args.reply
                if getattr(args, 'publisher_explicitly_set', True):
                    self.settings['publisher'] = args.publisher
                if getattr(args, 'manufacturer_explicitly_set', True):
                    self.settings['manufacturer'] = args.manufacturer
                if getattr(args, 'detectors_explicitly_set', True):
                    self.settings['detectors'] = args.detectors
                if getattr(args, 'magnifications_explicitly_set', True):
                    self.settings['magnifications'] = args.magnifications
                if getattr(args, 'detectorpixel_explicitly_set', True):
                    self.settings['detector pixelsize'] = args.detectorpixel

                os.remove(json_file)
                with open(json_file, 'w') as f:
                    json.dump(self.settings, f)

        else:
            self.settings = {
                "reply": args.reply,
                "publisher": args.publisher,
                "manufacturer": 'FEI',
                "detectors": ['HAADF', 'DF2', 'DF4', 'BF'],
                "magnifications": [1000, 2000, 5000, 10000],
                "detector pixelsize": 0.1,
            }
            with open(json_file, 'w') as f:
                json.dump(self.settings, f)
        
        self.connect_reply()
        self.connect_publisher()


    def connect_reply(self):
        self._context = zmq.Context()
        self._reply_socket = self._context.socket(zmq.REP)
        self._reply_socket.bind(f"tcp://*:{self.settings['reply']}")


    def connect_publisher(self):
        self._publisher_socket = self._context.socket(zmq.PUB)
        self._publisher_socket.bind(f"tcp://*:{self.settings['publisher']}")
        logger.info(f"ZeroMQ publisher socket bound to port {self.settings['publisher']}")

    def publish(self, msg):
        msg.serialize()
        self._publisher_socket.send(msg)



    def run(self):
        
        while True:
            msg = self._reply_socket.recv()
            logger.info(f"Received message: {msg}")
            self._reply_socket.send(b"OK")
            self.publish(msg)