#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:06:37 2022

@author: habermacher
"""

import serial
import time
import MySQLdb
import pandas as pd
from io import StringIO
import datetime as dt


db = MySQLdb.connect(
    host='31.171.148.100',
    user='livemetersql',
    passwd='limesql5200',
    db='livemeter'
)
cursor = db.cursor()

while True:
    print(f'{dt.datetime.now()}Verbindung wird hergestellt ...')
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
    port = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=300,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=120
        )
    print('Baudrate auf 9600 umgeschaltet')
    outputByte = port.read(size=1664)
    print(f'{dt.datetime.now()}Fertig')
    
    outputStr = outputByte.decode('utf-8')
    dataStr = outputStr.replace('(', ' ')
    dataStr = dataStr.replace(')', '')
    dataStr = dataStr.replace('*kWh','')
    dataStr = dataStr.replace('*kW','')
    dataStr = dataStr.replace('*kvar', '')
    dataStr = dataStr.replace('h','')
    dataStr = dataStr.replace('   ', '')
    dataStr = dataStr.replace('', '')
    df = pd.read_csv(StringIO(dataStr), sep=' ', skiprows=1, skipfooter=7, header=None, engine='python')
    df.rename(columns={0: 'obis', 1: 'value'}, inplace=True)
    df = df.set_index(df['obis'])
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    meterID = int(df.loc['0.0.0', 'value'])
    powerValue = df.loc['1.7.0', 'value']

    sql = f"INSERT INTO `meter_live_data` (`datetime`, `identity`, `value`) VALUES ('{timestamp}', '{meterID}', '{powerValue}');"
    cursor.execute(sql)
    db.commit()
        
    print(outputStr)
    print('Warte 5 Sekunden ...')
    time.sleep(5)
    