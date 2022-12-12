from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from bokeh.plotting import figure
from bokeh.embed import components
import os
import numpy as np
import MySQLdb
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.offline import plot

def stream(request):

    db = MySQLdb.connect(
        host='habi26.mysql.pythonanywhere-services.com',
        user='habi26',
        passwd='limesql5200',
        db='habi26$livemeter'
    )

    cursor = db.cursor()

    if request.method == "GET":
        while True:
            sql = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
            cursor.execute(sql)
            sqlSelect = cursor.fetchone()
            data = np.array(list(sqlSelect))
            meterID = data[2]
            value = data[3]
            timestamp = data[1]
            print(f'Ausgabe: {request} {data}')
            print('Update GET DATA')
            # print(f"ID: {data[0]}")
            # print(f"Timestamp: {data[1]}")
            # print(f"MeterID: {data[2]}")
            # print(f"Value: {data[3]}")
            # print(data)
            # return redirect(reverse(request))
            # time.sleep(10)
            gaugePlot = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                number = {'valueformat': '2.2f', 'suffix': 'kW'},
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Leistungsbezug", 'font': {'size': 24}},
                gauge = {'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                         'bar': {'color': "darkblue"},
                         'bgcolor': "white",
                         'borderwidth': 2,
                         'bordercolor': "gray",
                         'steps': [{'range': [0, 2.5], 'color': 'lightgreen'},
                        {'range': [2.5, 4], 'color': 'lightyellow'}, {'range': [4, 5], 'color': 'lightcoral'}],
                        'threshold': {
                        'line': {'color': "blue", 'width': 4},
                        'thickness': 0.75,
                        'value': 20}}))

            gaugePlot.update_layout(paper_bgcolor = 'rgba(255, 0, 0, 0.0)', font = {'color': "white", 'family': "Arial"})
            gaugeHTML = gaugePlot.to_html(config=None, full_html=False, div_id='streamGauge')
            print('Update GET GAUGE')
            gaugePlot.write_image("livemeter/static/gauge.png")


            return render(request, 'index.html', {'meterID': meterID, 'value': value, 'timestamp': timestamp, 'gauge': gaugeHTML})


    if request.method == "POST":
        while True:
            sql = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
            cursor.execute(sql)
            sqlSelect = cursor.fetchone()
            data = np.array(list(sqlSelect))
            meterID = data[2]
            value = data[3]
            timestamp = data[1]
            print(f'Ausgabe: {request} {data}')
            print('Update POST DATA')
            # print(f"ID: {data[0]}")
            # print(f"Timestamp: {data[1]}")
            # print(f"MeterID: {data[2]}")
            # print(f"Value: {data[3]}")
            # print(data)
            # return redirect(request.META['HTTP_REFERER'])
            gaugePlot = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                number = {'valueformat': '2.2f', 'suffix': 'kW'},
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Leistungsbezug", 'font': {'size': 24}},
                gauge = {'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                         'bar': {'color': "darkblue"},
                         'bgcolor': "white",
                         'borderwidth': 2,
                         'bordercolor': "gray",
                         'steps': [{'range': [0, 2.5], 'color': 'lightgreen'},
                        {'range': [2.5, 4], 'color': 'lightyellow'}, {'range': [4, 5], 'color': 'lightcoral'}],
                        'threshold': {
                        'line': {'color': "blue", 'width': 4},
                        'thickness': 0.75,
                        'value': 20}}))

            gaugePlot.update_layout(paper_bgcolor = 'rgba(255, 0, 0, 0.0)', font = {'color': "white", 'family': "Arial"})
            gaugeHTML = gaugePlot.to_html(config=None, full_html=False, div_id='streamGauge')
            print('Update POST GAUGE')
            gaugePlot.write_image("livemeter/static/gauge.png")

            return render(request, 'index.html', {'meterID': meterID, 'value': value, 'timestamp': timestamp, 'gauge': gaugeHTML})

    db.close()

# def chart(request):
#     if request.POST:  # wenn "Enter" gedrückt wird
#         dic = request.POST # Werte von Page übernehmen
#     # time.strftime("%Y-%m-%d %H:%M:%S")
#     # sql = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
#     # cursor.execute(sql)
#     # sqlSelect = cursor.fetchone()
#     # data = np.array(list(sqlSelect))
#     # print(f"ID: {data[0]}")
#     # print(f"Timestamp: {data[1]}")
#     # print(f"MeterID: {data[2]}")
#     # print(f"Value: {data[3]}")
#     # print(data)

#         print('mal sehen was das ist: ' + str(dic))
#         nCycle = int(dic['nCycle'])
#     else:
#         nCycle = int(1)

#     x = np.linspace(0, 100, 100)
#     y = np.sin(x / 100 * 2 * 3.1415 * nCycle)
#     p1 = figure(width=460, height=200)
#     p1.line(x, y)
#     p1.toolbar.logo = None

#     script, div = components(p1)  # hier wird html-Code erzeugt
#     chart = script + div

#     return render(request, 'index.html', {'nCycle': nCycle, 'chart': chart})
