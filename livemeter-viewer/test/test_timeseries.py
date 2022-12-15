#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:43:45 2022

@author: habermacher
"""

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from bokeh.models import Range1d
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.embed import file_html
import os
import numpy as np
import MySQLdb
import pandas as pd
import time
import datetime as dt
import plotly.graph_objects as go
from plotly.offline import plot
import pytz


db = MySQLdb.connect(
    host='31.171.148.100',
    user='livemeter',
    passwd='limesql5200',
    db='livemeter'
)

cursor = db.cursor()

dtStartToday = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
dtNow = dt.datetime.now()
tRange = dtNow-dtStartToday
tz = pytz.timezone("Europe/Zurich")


#Define SQL Querries
sqlQdata = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
sqlQcounterLP = f"SELECT COUNT(`value`) AS `values` FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"
sqlQdataLP = f"SELECT * FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"

#Execute SQL Querries
cursor.execute(sqlQdata)
sqlSELdata = cursor.fetchone()

cursor.execute(sqlQcounterLP)
sqlSELcounterLP = cursor.fetchone()

cursor.execute(sqlQdataLP)
sqlSELdataLP = cursor.fetchall()

df = pd.DataFrame(sqlSELdataLP, columns=['id', 'datetime', 'meterID',  'value'])
trStart = df['datetime'].iloc[0]
trEnd = (df['datetime'].iloc[-1]) + dt.timedelta(hours=1)
tRange = trEnd - trStart


x = df['datetime']
y = df['value']    
p1 = figure(plot_width=750, plot_height=500, x_axis_type="datetime")
p1.title.text_color = "black"
p1.background_fill_color = "white"
p1.background_fill_alpha = 0.5

p1.step(x, y, legend_label="Leistung", line_width=3, color='lightblue', mode="center")
p1.y_range = Range1d(0, 5)

p1.xaxis.axis_label = "Zeit"
p1.yaxis.axis_label = "kW"


p1.toolbar.logo = None

show(p1)

script, div = components(p1) # hier wird html-Code erzeugt
chart = script + div


tsPlotHTML = file_html(p1, CDN)

# data = np.array(list(sqlSELdata))
# counterLP = sqlSELcounterLP
# dfLP = pd.read_csv(StringIO(dataStr), sep=';', skiprows=0, skipfooter=0, header=None, engine='python')
# meterID = data[2]
# value = data[3]
# timestamp = data[1]