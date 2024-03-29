# Power Measurement with Raspberry Pi

This is a set of programs that can be used to measure the changes of voltage and current supplied to a Raspberry Pi 4 executing some programs.
The measured voltage and current measured are the values for the whole board of Rasberry Pi 4 (not the core).

## Table of Contents
- [Power Measurement with Raspberry Pi](#power-measurement-with-raspberry-pi)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Interactions between Devices](#interactions-between-devices)
    - [Performing Measurements (Sequence Diagram)](#performing-measurements-sequence-diagram)
    - [Class Dependencies in Server and Client](#class-dependencies-in-server-and-client)
  - [How to Use?](#how-to-use)
    - [1. Start up `server_app`](#1-start-up-server_app)
    - [2. Wait for Rpi to start up and `ssh` into it](#2-wait-for-rpi-to-start-up-and-ssh-into-it)
    - [3. Start up `client_app` and perform experiments](#3-start-up-client_app-and-perform-experiments)
    - [4. After `client_app` finished its executions, measured data (`*.csv`) can be found in `./`](#4-after-client_app-finished-its-executions-measured-data-csv-can-be-found-in-)
    - [5. Terminte `server_app` (optional)](#5-terminte-server_app-optional)
    - [6. Shutdown Rpi (optional)](#6-shutdown-rpi-optional)
    - [7. Power off power supply (optional)](#7-power-off-power-supply-optional)
  - [How to add Experiment?](#how-to-add-experiment)
    - [1. Create a new class based on the `Experiment` abstract class](#1-create-a-new-class-based-on-the-experiment-abstract-class)
    - [2. Update `client_app.py`](#2-update-client_apppy)
  - [Enabling the usage of `pyvisa` without `sudo` permission](#enabling-the-usage-of-pyvisa-without-sudo-permission)

## Overview
### Interactions between Devices
```mermaid
flowchart BT

dut["Device to measure\n(execute programs)"]
psu["Power suppy unit with measure"]
supervisor["Supervisor device\n(save measurements\nas output file(s))"]
local["Local machine"]

subgraph "remote (lab)"
    direction LR
    dut -..-> |"communicate via socket (TCP)"| supervisor
    supervisor ---> |"control via USB"| psu
    psu --> |"measurements (data) via USB"| supervisor
    psu --> |power supply| dut
end

local -..-> |login and control\nvia ssh| supervisor
local -..-> |login and control\nvia ssh| dut
```

### Performing Measurements (Sequence Diagram)
```mermaid
sequenceDiagram
    autonumber

    participant local as Local machine
    participant psu as Power supply unit
    participant supervisor as Supervisor device
    participant dut as Device to measure

    local ->>+ supervisor: login via ssh

    local ->> supervisor: power on power supply unit
    supervisor ->>+ psu: power on
    psu -->> supervisor: ok

    local ->> supervisor: start server
    supervisor ->>+ supervisor: start server

    local ->>+ dut: login via ssh

    local ->> dut: start client
 
    dut ->> supervisor: start measurement
    supervisor -->> dut: ok

    dut ->>+ dut: start program executions

    loop at regular interval
    supervisor ->> psu: measure one sample
    psu -->> supervisor: one sample, (V, A)
    end

    dut ->>- dut: program executions finished

    dut ->> supervisor: stop measurement
    supervisor -->> dut: ok

    local ->> supervisor: stop server
    supervisor ->>- supervisor: stop server

    local ->> dut: shutdown
    dut -->>- local: ok

    local ->> supervisor: power off power supply unit
    supervisor ->> psu: power off
    psu -->>- supervisor: ok

    local ->> supervisor: exit
    supervisor -->>- local: ok
```

### Class Dependencies in Server and Client
```mermaid
flowchart

a[Assistant]
c[Client]
e[Experiment]

s[Server]
sampler[Sampler]
dc[Device Controller]
psu[Power Supply Unit]

subgraph client_app
    direction TB
    a --> c
    a --> e
end

subgraph server_app
    direction TB
    s --> sampler
    sampler --> dc
    dc --> psu
end
```

## How to Use?

Since there are 3 types of devices involved in a measurement session, the following format will be used to indicate which device to execute a specific command:
```sh
# local machine
local$ <command>

# device to measure
dut$ <command>

# supervisor device
supervisor$ <command>
```

### 1. Start up `server_app`
<!-- TODO: want to change the interface here  -->
```sh
# `--allow_public` option added to allow socket connection from other devices
supervisor$ python3 server_app.py --allow_public

# when `client_app` is going to be executed on the same device as `server_app`
supervisor$ python3 server_app.py
```

### 2. Wait for Rpi to start up and `ssh` into it
```sh
# find the ip address of Rpi
local$ sudo nmap -sn 192.168.1.0/24 | grep "Pi" -C 5
# example output
Nmap scan report for <ip_addr_found>
Host is up (0.87s latency).
MAC Address: <mac_addr> (Raspberry Pi Trading)

# ssh into rpi
local$ ssh ubuntu@<ip_addr_found> -i <path_to_ssh_private_key>
```

### 3. Start up `client_app` and perform experiments
<!-- TODO: want to enable command executions -->
```sh
dut$ python3 client_app.py --allow_public --server_ip <ip_addr_of_supervisor_device>
```
### 4. After `client_app` finished its executions, measured data (`*.csv`) can be found in `./`
```sh
supervisor$ ls
XXX.csv
YYY.csv
...
```

📝 The directory to store `csv` files can be specify by changing the `set_output_filename` of the `Sampler` class in `sampler/sampler.py`.

```py
# example: store `csv` files in `measurement_data/`
self.output_filename = f"measurement_data/{filename}"
```
### 5. Terminte `server_app` (optional)
```sh
# ^C a few times to stop `server_app`
^C
```

📝 This step can be skipped if you plan to run another measurement session.

### 6. Shutdown Rpi (optional)
```sh
dut$ sudo shutdown now
```

📝 This step can be skipped if you plan to run another measurement session.
### 7. Power off power supply (optional)
```sh
supervisor$ python3 power_off_supply.py
```

📝 This step can be skipped if you plan to run another measurement session.
## How to add Experiment?
### 1. Create a new class based on the `Experiment` abstract class
```py
class Experiment(ABC):
    @abstractmethod
    def get_output_filename(self) -> str:
        '''
        the filename to store experiment outputs
        '''
        pass

    @abstractmethod
    def before_run(self):
        '''
        preparation required before run
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        main part of the experiment (1 experiment out of all defined experiemnts)

        things done in this function are measured and profiled.
        '''
        pass

    @abstractmethod
    def after_run(self):
        '''
        things to do after the main part of the experiment
        '''
        pass

    @abstractmethod
    def all_finished(self) -> bool:
        '''
        whether all prepared experiment are done
        '''
        pass

```

### 2. Update `client_app.py`
```py
assistant = Assistant(client=client, experiment=NewExperiment())
```

## Enabling the usage of `pyvisa` without `sudo` permission
Check the `idVendor` and `idProduct` of the device you want to control using `pyvisa`
```sh
dut$ lsusb
# example: Bus xxx Device xxx: ID <idVendor>:<idProduct> <Device Name>
# example: Bus 001 Device 009: ID 0b3e:1029 Kikusui Electronics Corp.
```
📝 You will need to enable USB interface on the measurement device for them to show up in the output of `lsusb`
(e.g., Kikusui PMX18 series can follow the steps in this [manual](https://manual.kikusui.co.jp/P/PMX_IF_J2.pdf) to enable USB interace.

The permission to control (i.e., read, write) a usb device (specified by idVendor and idProduct) can be provided to certain user group by adding a udev rules.
```sh
dut$ sudo vi /etc/udev/rules.d/99-com.rules
```

Then, add the following to the end of `99-com.rules`.
```
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="<idVendor>", ATTRS{idProduct}=="<idProduct>", MODE="660", GROUP="plugdev"
```

Reload udev rules by
```sh
dut$ sudo udevadm control --reload
```

Add current user to the user group `plugdev`
```sh
dut$ adduser <current user username> plugdev
```

After all these settings, when the specified device is plugged in via USB, permission to control will be given to `plugdev` user group.
Because the user we are using also belongs to the `plugdev` group, our user has the permission to control the device.
This can be check using the following Python codes:
```py
import pyvisa

rm = pyvisa.ResourceManager()

# without permission
#
# resources info are not available because of absence of permission
print(rm.list_resources()) # returns ()

# with permission
print(rm.list_resources()) # returns ( smtg, smtg )
```

- Main Reference:
  - https://stackoverflow.com/a/32022908/11311980
- About udev rules:
  - https://linuxconfig.org/tutorial-on-how-to-write-basic-udev-rules-in-linux
  - https://hana-shin.hatenablog.com/entry/2022/04/28/223022
