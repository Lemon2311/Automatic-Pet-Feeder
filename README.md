# Automatic-Pet-Feeder

This project is an automatic pet feeder, designed to make pet care easier and more convenient.
*Note*: This project is in active development and not yet fully tested and functional.

## Structure

The project is divided into two main parts:

1. `3d-models` - This folder contains all the 3D models used in the project. These models are used to create the physical structure of the pet feeder, following the assembly.

2. `code` - This folder contains the MicroPython code that runs on a Raspberry Pi Pico. The code controls the weight sensor and the servo that deploys the food. It also runs a web server, allowing remote access to the device.

## Hardware

- Raspberry Pi Pico
- Weight sensor
    - HX711 load cell amplifier
    - Load cell 5kg
- Servo motor MG995

## Software

The software is written in MicroPython and runs on a Raspberry Pi Pico. It uses a weight sensor to determine when to dispense food and a servo motor to deploy the food. The software also includes a web server, allowing remote access and control of the device.
