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

# port = serial.Serial(
#     port='/dev/ttyUSB0',
#     baudrate=300,
#     parity=serial.PARITY_EVEN,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.SEVENBITS,
#     timeout=120
#     )
msgEnd = '\x03'
msgEndByte = msgEnd.encode('utf-8')

while True:
    print('Verbindung wird hergestellt ...')
    timeStart = dt.datetime.now()
    print(timeStart.strftime("%d.%m.%Y %H:%M"))
    port = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=300,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=20
    )
    print('Ablesung beginnt ...')
    # request = bytes.fromhex('2f3f210d0a')
    request = '/?!\r\n'
    requestByte = request.encode('utf-8')
    ack = '\x06050\r\n'
    ackByte = ack.encode('utf-8')
    
    # ackByte = bytes.fromhex(ack)
    
    port.write(requestByte)
    # time.sleep(0.27)
    answereByte = port.readline()
    # time.sleep(0.27)
    print(answereByte.decode('utf-8'))
    # time.sleep(0.27)
    port.write(ackByte)
    time.sleep(0.266)
    # port.send_break()
    port.baudrate = 9600
    # port.send_break()
    # time.sleep(0.27)
    print('Baudrate auf 9600 umgeschaltet')
    outputByte = port.read_until(expected=msgEndByte)
    # outputByte = port.read(size=8000)
    print(f'{dt.datetime.now()}Fertig')
    
    outputStr = outputByte.decode('utf-8')
    dataStr = outputStr.replace('(', ';')
    dataStr = dataStr.replace(')', '')
    dataStr = dataStr.replace('*kWh','')
    dataStr = dataStr.replace('*kW','')
    dataStr = dataStr.replace('*kvar', '')
    dataStr = dataStr.replace('h','')
    dataStr = dataStr.replace('   ', '')
    dataStr = dataStr.replace('', '')
    df = pd.read_csv(StringIO(dataStr), sep=';', skiprows=0, skipfooter=0, header=None, engine='python', error_bad_lines=False)
    df.rename(columns={0: 'obis', 1: 'value'}, inplace=True)
    df = df.set_index(df['obis'])
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    meterID = int(df.loc['0.0.0', 'value'])
    powerValue = df.loc['1.7.0', 'value']

    sql = f"INSERT INTO `meter_live_data` (`datetime`, `identity`, `value`) VALUES ('{timestamp}', '{meterID}', '{powerValue}');"
    cursor.execute(sql)
    db.commit()
        
    print(outputStr)
    timeEnd = dt.datetime.now()
    readingTime = timeEnd - timeStart
    print(timeEnd.strftime("%d.%m.%Y %H:%M"))
    print(f'Auslesedauer: {readingTime}')
    print('Warte 5 Sekunden ...')
    time.sleep(5)
    