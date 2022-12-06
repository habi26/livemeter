#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 18:06:37 2022

@author: habermacher
"""

import serial
import time
import MySQLdb
import sshtunnel
import pandas as pd
from io import StringIO
import datetime as dt

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

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='habi26', ssh_password='7AS7jsT8MsB@aHT3',
    remote_bind_address=('habi26.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    db = MySQLdb.connect(
    host='127.0.0.1', port=tunnel.local_bind_port,
    user='habi26',
    passwd='limesql5200',
    db='habi26$livemeter'
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
        
        port = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=300,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=20
        )
        
        print('Ablesung beginnt ...')
        port.write(requestByte)
        answereByte = port.readline()
        print(answereByte.decode('utf-8'))
        port.write(ackByte)
        time.sleep(0.266)
        port.baudrate = 9600
        print('Baudrate auf 9600 umgeschaltet')
        outputByte = port.read_until(expected=msgEndByte)
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
    