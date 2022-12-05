from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
import MySQLdb
import pandas as pd

db = MySQLdb.connect(
    host='31.171.148.100',
    user='livemetersql',
    passwd='limesql5200',
    db='livemeter'
)

cursor = db.cursor()

# def stream(request):
#     if request.POST:
        

# def chart(request):
#     if request.POST:  # wenn "Enter" gedrückt wird
#     time.strftime("%Y-%m-%d %H:%M:%S")
sql = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
cursor.execute(sql)
sqlSelect = cursor.fetchone()
data = np.array(list(sqlSelect))
print(f"ID: {data[0]}")
print(f"Timestamp: {data[1]}")
print(f"MeterID: {data[2]}")
print(f"Value: {data[3]}")
print(data)

    #     print('mal sehen was das ist: ' + str(dic))
    #     nCycle = int(dic['nCycle'])
    # else:
    #     nCycle = int(1)

    # x = np.linspace(0, 100, 100)
    # y = np.sin(x / 100 * 2 * 3.1415 * nCycle)
    # p1 = figure(width=460, height=200)
    # p1.line(x, y)
    # p1.toolbar.logo = None

    # script, div = components(p1)  # hier wird html-Code erzeugt
    # chart = script + div

    # return render(request, 'index.html', {'nCycle': nCycle, 'chart': chart})
