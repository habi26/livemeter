#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:06:37 2022

@author: habermacher
"""

import serial
import sys
import time

port = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=300,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=120
)

request = bytes.fromhex('2f3f210d0a')
port.write(request)
# port = serial.Serial(baudrate=9600)

answere = port.read(size=5864)
#time.sleep(10)
print(answere)
print('Fertig')
