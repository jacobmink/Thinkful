import time
import datetime
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import sqlite3 as lite
import collections
import statsmodels.api as sm


cities = {"Austin":'30.303936,-97.754355',
          "Boston":'42.331960,-71.020173',
          "Chicago":'41.837551,-87.681844',
          "Denver":'39.761850,-104.881105',
          "New_Orleans":'30.053420,-89.934502',
          "New_York":'40.663619,-73.938589',
          "Philadelphia":'40.009376,-75.133346',
          "Buffalo":'42.8864, -78.8784'
}

api_key = 'ccac8a4b658f4a6e2b0c9f0791e8e4ab/'
url = 'https://api.forecast.io/forecast/'
austin = cities['Austin']

now = datetime.datetime.now()
start_date = now - datetime.timedelta(days=30)

con = lite.connect('weather.db')
cur = con.cursor()

with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')
    cur.execute('CREATE TABLE daily_temp '
                '( day_of_reading INT, '
                'New_Orleans REAL, '
                'Buffalo REAL, '
                'Chicago REAL, '
                'Boston REAL, '
                'New_York REAL, '
                'Austin REAL, '
                'Philadelphia REAL, '
                'Denver REAL);')
    while start_date < now:
        cur.execute('INSERT INTO daily_temp(day_of_reading) VALUES (?)',
                    (int(start_date.strftime('%s')),))
        start_date += datetime.timedelta(days=1)


#Make actual API requests
for k,v in cities.iteritems():
    start_date = now - datetime.timedelta(days=30)
    while start_date != now:
        #API request
        r = requests.get(url +
                         api_key +
                         v + ',' +
                         start_date.strftime('%Y-%m-%dT%I:%M:%S'))
        
        with con:
            cur.execute('UPDATE daily_temp SET ' +
                        k + ' = ' +
                        str(r.json()['daily']['data'][0]['temperatureMax']) +
                        ' WHERE day_of_reading = ' + start_date.strftime('%s'))
        start_date += datetime.timedelta(days=1)

con.close()

## Analysis

con = lite.connect('weather.db')
cur = con.cursor()
with con:
    cur.execute('SELECT * FROM daily_temp')
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df_test = pd.DataFrame(rows,columns=cols)

df = pd.read_sql_query('SELECT * FROM daily_temp ORDER BY day_of_reading',
                       con,index_col='day_of_reading')

attributes = pd.DataFrame(index=df.columns,
                          columns=['max_temps',
                                   'min_temps',
                                   'range',
                                   'variance',
                                   'mean'])

i = 0
for city in attributes.index:
    attributes.loc[city,'max_temps'] = max(df[city])
    attributes.loc[city,'min_temps'] = min(df[city])
    attributes.loc[city,'range'] = max(df[city]) - min(df[city])
    attributes.loc[city,'variance'] = df[city].var()
    attributes.loc[city,'mean'] = df[city].mean()
    i +=1


day_change = collections.defaultdict(int)
for col in df.columns:
    city_vals = df[col].tolist() # change each column into a list
    city_id = col
    city_change = [] #Create an empty list
    for k,v in enumerate(city_vals):
        if k < len(city_vals) - 1:
            city_change.append(abs(city_vals[k] - city_vals[k+1]))
    day_change[city_id] = city_change #Populate day_change

#Create DataFrame of day-to-day changes for each city
df_changes = pd.DataFrame(columns=day_change.keys())

for col in df_changes.columns:
    df_changes[col] = day_change[col]


#Plot DataFrame info
fig1 = df.plot(kind='line',
              subplots=True,
              figsize=(15,15),
              fontsize=15,
              style=['r','b','y','g','b','k','b','b'])

fig2 = attributes.plot(kind='bar',
              subplots=True,
              figsize=(15,15),
              fontsize=15,
              style=['r','b','y','g','b','k','b','b'],
              legend=False)

fig3 = df_changes.plot(kind='line',
              subplots=True,
              figsize=(15,15),
              fontsize=15,
              style=['r','b','y','g','b','k','b','b'])

print 'The city with the most temperature fluctuation over the time period is Denver.'

plt.show()
