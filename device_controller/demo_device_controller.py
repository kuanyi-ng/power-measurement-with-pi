import json
import logging
import os
import random
import sys
from inspect import getfile

from device_controller.device_controller import DeviceController


class DemoDeviceController(DeviceController):
    def __init__(self) -> None:
        super().__init__()

        # look for parameters for sampler (json)
        param_file = f"{os.path.splitext(getfile(DemoDeviceController))[0]}.json"
        # try to load parameters from json file
        try:
            with open(param_file) as param_json:
                self._parameters = json.load(param_json)
        except FileNotFoundError:
            self._parameters = {}
        
        # set titles of CSV file
        if "titles" in self._parameters:
            self._titles  = tuple(self._parameters["titles"])
        else:
            logging.error(f"ERROR: must set titles in {param_file}")
            sys.exit(1)

    def close(self):
        logging.debug("Closing FakeDeviceController")

    def _write(self, command: str) -> int:
        return len(command)
    
    def _read(self, command: str) -> str:
        return command

    def _query(self, command: str) -> str:
        return command
    
    def reset(self):
        logging.debug("Reseting FakeDeviceController")

    def set_output_current(self, val: float) -> int:
        return int(val)

    def set_output_voltage(self, val: float) -> int:
        return int(val)

    def output_on(self) -> int:
        logging.debug("Set output to on")
        return 1

    def output_off(self) -> int:
        logging.debug("Set output to off")
        return 0

    def get_current(self) -> float:
        return 3.0 - random.random()

    def get_voltage(self) -> float:
        return 5.1 - random.random()

    def get_titles(self):
        return self._titles

    def get_values(self) -> tuple[float, float]:
        return ( self.get_current(), self.get_voltage() )
    
    def is_meter_ready(self) -> bool:
        return True

