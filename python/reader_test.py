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
import random as rd

# def clean_meterdata_elster(output,data):
#     return 
#     data = outputStr.replace('(', ';')
#     data = data.replace(')', '')
#     data = data.replace('*kWh','')
#     data = data.replace('*kW','')
#     data = data.replace('*kvar', '')
#     data = data.replace('h','')
#     data = data.replace('   ', '')
#     data = data.replace('', '')

db = MySQLdb.connect(
    host='31.171.148.100',
    user='livemetersql',
    passwd='limesql5200',
    db='livemeter'
)
cursor = db.cursor()

msgEnd = '\x03'
msgEndByte = msgEnd.encode('utf-8')
request = '/?!\r\n'
requestByte = request.encode('utf-8')
ack = '\x06050\r\n'
ackByte = ack.encode('utf-8')

while True:
    print('Verbindung wird hergestellt ...')
    timeStart = dt.datetime.now()
    print(timeStart.strftime("%d.%m.%Y %H:%M"))
    
    
    print('Ablesung beginnt ...')


    time.sleep(0.266)
    print('Baudrate auf 9600 umgeschaltet')
    time.sleep(14)
    print(f'{dt.datetime.now()} Fertig')

    randomP = rd.uniform(0.5,4)
    obis = ['0.0.0','1.7.0']
    value = [28450,randomP]
    randomData = {
        "obis": ['0.0.0', '1.7.0'],
        "value": [28450, randomP]
}
    df = pd.DataFrame(randomData)
    df = df.set_index(df['obis'])
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    meterID = int(df.loc['0.0.0', 'value'])
    powerValue = df.loc['1.7.0', 'value']

    sql = f"INSERT INTO `meter_live_data` (`datetime`, `identity`, `value`) VALUES ('{timestamp}', '{meterID}', '{powerValue}');"
    cursor.execute(sql)
    db.commit()
        
    timeEnd = dt.datetime.now()
    readingTime = timeEnd - timeStart
    print(timeEnd.strftime("%d.%m.%Y %H:%M"))
    print(f'Auslesedauer: {readingTime}')
    print('Warte 5 Sekunden ...')
    time.sleep(5)
    