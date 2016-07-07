import requests
import pandas as pd
import numpy as np
import sqlite3 as lite
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import time
from dateutil.parser import parse
import collections


con = lite.connect('citi_bike.db')
cur = con.cursor()
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
id_bikes = collections.defaultdict(int)
key_list = []

with con:
    cur.execute('DROP TABLE citibike_reference')
    cur.execute('DROP TABLE available_bikes')

with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')

## Create a while loop that fetches the data every minute and populates the database
loop_count = 0
while loop_count < 60:

    r = requests.get('http://www.citibikenyc.com/stations/json')
    r.json()

    with con:
        for station in r.json()['stationBeanList']:
            cur.execute(sql, (station['id'],
                              station['totalDocks'],
                              station['city'],
                              station['altitude'],
                              station['stAddress2'],
                              station['longitude'],
                              station['postalCode'],
                              station['testStation'],
                              station['stAddress1'],
                              station['stationName'],
                              station['landMark'],
                              station['latitude'],
                              station['location'],
                              ))


    for station in r.json()['stationBeanList']:
        for k in station.keys():
            if k not in key_list:
                key_list.append(k)
    
    
    df = json_normalize(r.json()['stationBeanList'])
    station_ids = df['id'].tolist()
    station_ids = ['_' + str(x) + ' INT' for x in station_ids]
    exec_time = parse(r.json()['executionTime'])


    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']
    
    with con:
        cur.execute('CREATE TABLE available_bikes ( execution_time INT, ' +  ', '.join(station_ids) + ');')
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

        for k, v in id_bikes.iteritems():
            cur.execute('UPDATE available_bikes SET _' + str(k) + ' = ' + str(v) + ' WHERE execution_time = ' + exec_time.strftime('%s') + ';')
    
    time.sleep(.1)
    loop_count += 1

with con:
    cur.execute('SELECT * FROM available_bikes')
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df_test = pd.DataFrame(rows,columns=cols)
print df_test


