#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:06:37 2022

@author: habermacher
"""

import serial
import sys
import time

while True:
    print('Verbindung wird hergestellt ...')
    port = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=300,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=120
        )
    print('Ablesung beginnt ...')
    request = bytes.fromhex('2f3f210d0a')
    port.write(request)
    answere = port.read(size=5864)
    print('Fertig')
    print(answere.decode('utf-8'))
    print('Warte 5 Sekunden ...')
    time.sleep(5)
    