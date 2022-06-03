# Power Measurement with Raspberry Pi

This is a set of programs that can be used to measure the changes of voltage and current supplied to a Raspberry Pi 4 executing some programs.
The measured voltage and current measured are the values for the whole board of Rasberry Pi 4 (not a single transistor).

## Table of Contents
- [Power Measurement with Raspberry Pi](#power-measurement-with-raspberry-pi)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Interactions between Devices](#interactions-between-devices)
    - [Performing Measurements (Sequence Diagram)](#performing-measurements-sequence-diagram)
    - [Class Dependencies in Server and Client](#class-dependencies-in-server-and-client)

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
    supervisor ---> |control with USB| psu
    psu --> |"measurements (data)"| supervisor
    psu --> |power supply| dut
end

local -..-> |login via ssh\nand control| supervisor
local -..-> |login via ssh\nand control| dut
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