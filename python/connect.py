#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:06:37 2022

@author: habermacher
"""

import serial
import sys
import time
import MySQLdb
import pymysql
import numpy as np
import pandas as pd
from io import StringIO


db = MySQLdb.connect(
    host='31.171.148.100',
    user='livemetersql',
    passwd='limesql5200',
    db='livemeter'
)
cursor = db.cursor()

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
    outputByte = port.read(size=5864)
    print('Fertig')
    
    outputStr = outputByte.decode('utf-8')
    dataStr = outputStr.replace('(', ' ')
    dataStr = dataStr.replace(')', '')
    dataStr = dataStr.replace('*kwh','')
    dataStr = dataStr.replace('*kvar', '')
    dataStr = dataStr.replace('   ', '')
    df = pd.read_csv(StringIO(dataStr), sep=' ', skiprows=1, skipfooter=5, header=None, engine='python')
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    meterID = 123321
    powerValue = 1.234

    sql = f"INSERT INTO `meter_live_data` (`datetime`, `identity`, `value`) VALUES ('{timestamp}', '{meterID}', '{powerValue}');"
    cursor.execute(sql)
    db.commit()
        
    print(outputStr)
    print('Warte 5 Sekunden ...')
    time.sleep(5)
    