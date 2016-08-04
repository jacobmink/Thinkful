import requests
import pandas as pd
import numpy as np
import sqlite3 as lite
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import time
import datetime
from dateutil.parser import parse
import collections
import matplotlib.pyplot as plt


con = lite.connect('citi_bike.db')
cur = con.cursor()
sql = 'INSERT INTO citibike_reference (id, '
                                       'totalDocks, '
                                       'city, '
                                       'altitude, '
                                       'stAddress2, '
                                       'longitude, '
                                       'postalCode, '
                                       'testStation, '
                                       'stAddress1, '
                                       'stationName, '
                                       'landMark, '
                                       'latitude, '
                                       'location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
id_bikes = collections.defaultdict(int)

r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

station_ids = df['id'].tolist()
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

with con:
    cur.execute('DROP TABLE IF EXISTS citibike_reference')
    cur.execute('DROP TABLE IF EXISTS available_bikes')
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, '
                                                  'totalDocks INT, '
                                                  'city TEXT, '
                                                  'altitude INT, '
                                                  'stAddress2 TEXT, '
                                                  'longitude NUMERIC, '
                                                  'postalCode TEXT, '
                                                  'testStation TEXT, '
                                                  'stAddress1 TEXT, '
                                                  'stationName TEXT, '
                                                  'landMark TEXT, '
                                                  'latitude NUMERIC, '
                                                  'location TEXT)')
    cur.execute('CREATE TABLE available_bikes ( execution_time INT, '
                                              +  ', '.join(station_ids) + ');')


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
                          station['location']
                          ))



## Create a while loop that fetches the data every minute and populates the database
loop_count = 0
while loop_count < 60:

    r = requests.get('http://www.citibikenyc.com/stations/json')

    df = json_normalize(r.json()['stationBeanList'])

    exec_time = parse(r.json()['executionTime'])


    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']
    
    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)',
                                                 (exec_time.strftime('%s'),))

        for k, v in id_bikes.iteritems():
            cur.execute('UPDATE available_bikes SET _' +
                        str(k) + ' = ' + str(v) +
                        ' WHERE execution_time = ' +
                        exec_time.strftime('%s') + ';')
    con.commit()
    time.sleep(60)
    loop_count += 1
con.close()

#analysis
con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query('SELECT * FROM available_bikes ORDER BY execution_time',
                       con,
                       index_col='execution_time')

hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #take off the '_'
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change


def keywithmaxval(d):
    return max(d, key=lambda k: d[k])

max_station = keywithmaxval(hour_change)

cur.execute('SELECT id, stationName, latitude, longitude '
            'FROM citibike_reference '
            'WHERE id = ?', (max_station,))
data = cur.fetchone()
print 'The most active station is station id %s at %s latitude: %s longitude: %s ' % data
print 'With %d bicycles coming and going in the hour between %s and %s' % (hour_change[max_station],
                                                                           datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
                                                                           datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')
                                                                           )


plt.bar(hour_change.keys(),hour_change.values())
plt.show()




    
