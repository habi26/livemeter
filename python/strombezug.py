#!/usr/bin/python

import sys
import serial
import time
import MySQLdb

port = serial.Serial(
	port='/dev/ttyUSB1',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

db = MySQLdb.connect(
	host='localhost',
	user='root',
	passwd='raspberry',
	db='stromzaehler'
)

cur = db.cursor()

start = '1b1b1b1b01010101'
end = '1b1b1b1b1a'

data = ''
timestamp = ''

while True:
	char = port.read()

	data = data + char.encode('HEX')
	pos = data.find(start)
	if (pos <> -1):
		data = data[pos:len(data)]
	pos = data.find(end)
	if (pos <> -1):
		timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

		search = '070100010801ff'
		pos = data.find(search)
		if (pos <> -1):
			pos = pos + len(search) + 14
			value = data[pos:pos + 10]

			valuedb = str(int(value, 16) / 1e4)
			sql = ("INSERT INTO `leistung_bezug` (`zaehlerid`, `time`, `leistung`) VALUES (2, '"+timestamp+"', '"+valuedb+"');")	
#			print sql
			cur.execute(sql) 		
			db.commit()
			break		
		data = ''

db.close()
