from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d, DatetimeTickFormatter
import numpy as np
import MySQLdb
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import pytz

def stream(request):

    # MySQL Verbindung
    db = MySQLdb.connect(
        host='habi26.mysql.pythonanywhere-services.com',
        user='habi26',
        passwd='limesql5200',
        db='habi26$livemeter'
    )

    cursor = db.cursor()

    # if request.method == "GET":
    while True:
        dtStartToday = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
        dtNow = dt.datetime.now()
        tz = pytz.timezone("Europe/Zurich")
        
        
        # Definition SQL Queries
        sqlQdata = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
        sqlQcounterLP = f"SELECT COUNT(`value`) AS `values` FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"
        sqlQdataLP = f"SELECT * FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"
        
        # Ausführung SQL Queries
        cursor.execute(sqlQdata)
        sqlSELdata = cursor.fetchone()
        
        cursor.execute(sqlQcounterLP)
        sqlSELcounterLP = cursor.fetchone()
        
        cursor.execute(sqlQdataLP)
        sqlSELdataLP = cursor.fetchall()
        
        # Datenverarbeitung
        data = np.array(list(sqlSELdata))
        counterLP = sqlSELcounterLP
        df = pd.DataFrame(sqlSELdataLP, columns=['id', 'datetime', 'meterID',  'value'])
        trStart = df['datetime'].iloc[0]
        trEnd = (df['datetime'].iloc[-1]) + dt.timedelta(hours=1)
        tRange = trEnd - trStart
        wDay = ((df['value'].sum())/counterLP) * (tRange.total_seconds()/3600)
        
        meterID = data[2]
        value = data[3]
        timestamp = data[1]
        
        
        # Gauge Plot Plotly
        gaugePlot = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            number = {'valueformat': '2.2f', 'suffix': 'kW'},
            domain = {'x': [0, 1], 'y': [0, 1]},
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
        
        # Lastprofil Plot Bokeh
        x = df['datetime']
        y = df['value']
        p1 = figure(plot_width=500, plot_height=300, x_axis_type="datetime", sizing_mode="scale_both")
        p1.title.text_color = "black"
        p1.background_fill_color = "white"
        p1.background_fill_alpha = 0.75
        #p1.border_fill_alpha = 0.5
        p1.xaxis.formatter = DatetimeTickFormatter(days="%d.%m.%y %H:%M", months="%d.%m.%y %H:%M", hours="%d.%m.%y %H:%M", minutes="%d.%m.%y %H:%M")
        
        p1.step(x, y, legend_label="Leistung", line_width=3, color='coral', mode="center")
        p1.y_range = Range1d(0, 5)
        
        p1.xaxis.axis_label = "Zeit"
        p1.yaxis.axis_label = "kW"
        
        
        p1.toolbar.logo = None
        
        
        script, div = components(p1)
        tsPlot = script + div
        
        
        
        return render(request, 'index.html', {'meterID': meterID, 'value': value, 'timestamp': timestamp, 'trStart': trStart, 'trEnd': trEnd, 'wDay' : wDay, 'gauge': gaugeHTML, 'tsPlot': tsPlot})
        db.close()


#     # if request.method == "POST":
# while True:
#             dtStartToday = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
#             dtNow = dt.datetime.now()
#             tz = pytz.timezone("Europe/Zurich")


#             #Define SQL Querries
#             sqlQdata = "SELECT * FROM `meter_live_data` ORDER BY id DESC LIMIT 1;"
#             sqlQcounterLP = f"SELECT COUNT(`value`) AS `values` FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"
#             sqlQdataLP = f"SELECT * FROM meter_live_data WHERE `datetime` BETWEEN '{dtStartToday}' AND '{dtNow}';"

#             #Execute SQL Querries
#             cursor.execute(sqlQdata)
#             sqlSELdata = cursor.fetchone()

#             cursor.execute(sqlQcounterLP)
#             sqlSELcounterLP = cursor.fetchone()

#             cursor.execute(sqlQdataLP)
#             sqlSELdataLP = cursor.fetchall()

#             data = np.array(list(sqlSELdata))
#             counterLP = sqlSELcounterLP
#             df = pd.DataFrame(sqlSELdataLP, columns=['id', 'datetime', 'meterID',  'value'])
#             trStart = df['datetime'].iloc[0]
#             trEnd = (df['datetime'].iloc[-1]) + dt.timedelta(hours=1)
#             tRange = trEnd - trStart
#             wDay = ((df['value'].sum())/counterLP) * (tRange.total_seconds()/3600)

#             meterID = data[2]
#             value = data[3]
#             timestamp = data[1]

#             gaugePlot = go.Figure(go.Indicator(
#                 mode = "gauge+number",
#                 value = value,
#                 number = {'valueformat': '2.2f', 'suffix': 'kW'},
#                 domain = {'x': [0, 1], 'y': [0, 1]},
#                 gauge = {'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
#                          'bar': {'color': "darkblue"},
#                          'bgcolor': "white",
#                          'borderwidth': 2,
#                          'bordercolor': "gray",
#                          'steps': [{'range': [0, 2.5], 'color': 'lightgreen'},
#                         {'range': [2.5, 4], 'color': 'lightyellow'}, {'range': [4, 5], 'color': 'lightcoral'}],
#                         'threshold': {
#                         'line': {'color': "blue", 'width': 4},
#                         'thickness': 0.75,
#                         'value': 20}}))

#             gaugePlot.update_layout(paper_bgcolor = 'rgba(255, 0, 0, 0.0)', font = {'color': "white", 'family': "Arial"})
#             gaugeHTML = gaugePlot.to_html(config=None, full_html=False, div_id='streamGauge')

#             #Lastprofil Plot
#             x = df['datetime']
#             y = df['value']
#             p1 = figure(plot_width=500, plot_height=300, x_axis_type="datetime", sizing_mode="scale_both")
#             p1.title.text_color = "black"
#             p1.background_fill_color = "white"
#             p1.background_fill_alpha = 0.5
#             #p1.border_fill_alpha = 0.0

#             p1.step(x, y, legend_label="Leistung", line_width=3, color='coral', mode="center")
#             p1.y_range = Range1d(0, 5)

#             p1.xaxis.axis_label = "Zeit"
#             p1.yaxis.axis_label = "kW"


#             p1.toolbar.logo = None

#             script, div = components(p1)
#             tsPlot = script + div

#             return render(request, 'index.html', {'meterID': meterID, 'value': value, 'timestamp': timestamp, 'trStart': trStart, 'trEnd': trEnd, 'wDay' : wDay, 'gauge': gaugeHTML, 'tsPlot': tsPlot})

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
