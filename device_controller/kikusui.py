# Implementation of Kikusui is based on:
# - https://github.com/mlcommons/power-dev/blob/master/power_meter_sampling/samplers/yokogawa.py
# - https://simulation4vehicle.blogspot.com/2018/07/python-3-power-supply-control-kikusui.html
#
# VISA reference:
# - https://pyvisa.readthedocs.io/en/latest/
#
# Code was developed for and tested on a Kikusui PMX18-5A Meter.
# For list of remote commands, see
#   Communication Interface Manual, Oct 2019
#   https://manual.kikusui.co.jp/P/PMX_IF_E4.pdf

import json
import logging
import os
import sys
from inspect import getfile
from typing import cast

import pyvisa
from pyvisa.resources.usb import USBInstrument
from usb.core import USBError

from device_controller.device_controller import DeviceController
from device_controller.device_info import device_addr


class Kikusui(DeviceController):
    def __init__(self, device_id: str) -> None:
        super().__init__()

        # look for parameters for sampler (json)
        param_file = f"{os.path.splitext(getfile(Kikusui))[0]}.json"
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

        # initailize Resource Manager
        self._rm = pyvisa.ResourceManager('@py')

        # try to open resource (connect to device)
        self._address = device_addr[device_id]

        try:
            # cast to make sure that meter is an instrument connected via USB
            self._meter = cast(USBInstrument, self._rm.open_resource(self._address))

            # set termination for commands (differ between devices)
            self._meter.read_termination = '\n'
            self._meter.write_termination = '\n'

            logging.debug(f"*IDN?: {self._query('*IDN?')}")
        except USBError as err:
            self._meter = None
            logging.info(f"USBERror: {err}")
            sys.exit(1)
        except ValueError as err:
            self._meter = None
            logging.info(f"ValueError: {err}")
            sys.exit(1)
            

    def close(self):
        assert self._rm is not None
        assert self._meter is not None

        self._meter.close()
        self._meter = None
        self._rm.close()
        self._rm = None

    def _write(self, command: str) -> int:
        assert self._meter is not None

        return self._meter.write(command)

    def _read(self, command: str) -> str:
        assert self._meter is not None

        return self._meter.read(command)

    def _query(self, command: str) -> str:
        assert self._meter is not None

        return self._meter.query(command)
    
    def reset(self) -> int:
        command = "rst; status:preset; *cls"
        return self._write(command)

    def set_output_current(self, val: float) -> int:
        command = f"CURR {val}"
        return self._write(command)

    def set_output_voltage(self, val: float) -> int:
        command = f"VOLT {val}"
        return self._write(command)

    def output_on(self) -> int:
        command = "OUTP 1"
        return self._write(command)

    def output_off(self) -> int:
        command = "OUTP 0"
        return self._write(command)

    def get_current(self) -> float:
        command = f"MEAS:CURR?"
        return float(self._query(command))

    def get_voltage(self) -> float:
        command = f"MEAS:VOLT?"
        return float(self._query(command))

    def get_titles(self):
        return self._titles

    def get_values(self) -> tuple[float, float]:
        '''
        [ current, voltage ]
        '''
        return ( self.get_current(), self.get_voltage() )

    def is_meter_ready(self) -> bool:
        return self._meter != None
