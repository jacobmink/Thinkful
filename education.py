from bs4 import BeautifulSoup
import requests
import sqlite3 as lite
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
# import seaborn as sns
import string
import csv
import re
import unicodedata

## Scrape data from UN website, turn HTML into BeautifulSoup format
url = 'http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
soup_6 = soup('table')[6]

## Put all data from relevant data table into list format
raw_data = []
for string in soup_6.stripped_strings:
    raw_data.append(string)
raw_data = raw_data[8:-29]
## Remove all footnote letters from data
raw_data = [x for x in raw_data if all([x!='a',
                                        x!='b',
                                        x!='c',
                                        x!='d',
                                        x!='e',
                                        x!='f',
                                        x!='g',
                                        x!='h'])]
## Separate data into categorical lists based on raw_data list indexing
country = [country for country in raw_data[4:] if raw_data.index(country) % 5 == 0]
year = raw_data[6::5]
year = [int(i) for i in year]
total = raw_data[7::5]
total = [int(i) for i in total]
men = raw_data[8::5]
men = [int(i) for i in men]
women = raw_data[9::5]
women = [int(i) for i in women]

## Create DataFrame using data lists as input, with country as index
df = pd.DataFrame(index=country,
                  columns=[raw_data[1],
                           raw_data[2],
                           raw_data[3],
                           raw_data[4]])
df['Year'] = year
df['Total'] = total
df['Men'] = men
df['Women'] = women
## Rename DataFrame
population_data = df

## Connect to UN_Data database in SQLite3
con = lite.connect('UN_Data.db')
cur = con.cursor()

## Update SQLite3 data table
with con:
    cur.execute('DELETE FROM gdp')
    cur.execute('CREATE TABLE IF NOT EXISTS gdp (country_name TEXT, '
                        '_1999 REAL, '
                        '_2000 REAL, '
                        '_2001 REAL, '
                        '_2002 REAL, '
                        '_2003 REAL, '
                        '_2004 REAL, '
                        '_2005 REAL, '
                        '_2006 REAL, '
                        '_2007 REAL, '
                        '_2008 REAL, '
                        '_2009 REAL, '
                        '_2010 REAL) ')
## Read in GDP data line by line, update SQLite3 data table
un_file = []
with open('API_NY.GDP.MKTP.CD_DS2_en_csv_v2.csv','rU') as inputFile:
    next(inputFile)
    next(inputFile)
    next(inputFile)
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
            country_name_clean = unicode(line[0])
            query_string = ('INSERT INTO gdp (country_name, '
                            '_1999, '
                            '_2000, '
                            '_2001, '
                            '_2002, '
                            '_2003, '
                            '_2004, '
                            '_2005, '
                            '_2006, '
                            '_2007, '
                            '_2008, '
                            '_2009, '
                            '_2010) '
                            'VALUES ("' + country_name_clean + '","' + '","'.join(line[43:-5]) + '");')
            try:
                cur.execute(query_string)
            except:
                print query_string
                
## Bring SQLite3 data table into DataFrame
with con:
    cur.execute('SELECT * FROM gdp')
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    gdp = pd.DataFrame(rows,columns=cols)

## Format DataFrame
gdp = gdp.sort(columns='country_name').drop_duplicates()
gdp = gdp.reset_index(drop=True)
gdp.replace('',np.nan,inplace=True)
gdp.set_index('country_name',inplace=True)
gdp = gdp.dropna(subset=gdp.columns[0:],how='all')

## Merge the two DataFrames
merged = population_data.merge(gdp,
                               how='outer',
                               left_index=True,
                               right_index=True)
merged = merged.drop_duplicates()
merged.insert(4,'log_gdp',0)
merged.columns = ['Year',
                  'Total',
                  'Men',
                  'Women',
                  'log_gdp',
                  '1999',
                  '2000',
                  '2001',
                  '2002',
                  '2003',
                  '2004',
                  '2005',
                  '2006',
                  '2007',
                  '2008',
                  '2009',
                  '2010']
## Take log transform of GDP values
for col in merged.columns[5:16]:
    merged[col] = np.log(merged[col])
merged['2010'] = np.log(merged['2010'])
    
## Manually sort through data to find different names for same country, combine rows
list(merged.index)

## From manual search, these countries are named differently and need to be joined:
## Bolivia
merged.index = merged.index.to_series().replace(
    {'Bolivia (Plurinational State of)':'Bolivia'})

## Republic of Congo
merged.index = merged.index.to_series().replace(
    {'Congo':'Congo, Rep.'})

## Democratic Republic of Congo
merged.index = merged.index.to_series().replace(
    {'Democratic Republic of the Congo':'Congo, Dem. Rep.'})

## Cote d'Ivoire (manual work-around because one of the name versions is not Unicode)
merged.ix["Cote d'Ivoire"]['Year'] = 2000
merged.ix["Cote d'Ivoire"]['Total'] = 6
merged.ix["Cote d'Ivoire"]['Men'] = 8
merged.ix["Cote d'Ivoire"]['Women'] = 5

## Egypt
merged.index = merged.index.to_series().replace(
    {'Egypt, Arab Rep.':'Egypt'})

## Gambia
merged.index = merged.index.to_series().replace(
    {'Gambia, The':'Gambia'})

## Hong Kong
merged.index = merged.index.to_series().replace(
    {'China, Hong Kong SAR':'Hong Kong'})
merged.index = merged.index.to_series().replace(
    {'Hong Kong SAR, China':'Hong Kong'})

## Iran
merged.index = merged.index.to_series().replace(
    {'Iran (Islamic Republic of)':'Iran'})

## Kyrgyzstan
merged.index = merged.index.to_series().replace(
    {'Kyrgyz Republic':'Kyrgyzstan'})

## Lao PDR
merged.index = merged.index.to_series().replace(
    {"Lao People's Democratic Republic":'Lao PDR'})

## Libya
merged.index = merged.index.to_series().replace(
    {'Libyan Arab Jamahiriya':'Libya'})

## Macao
merged.index = merged.index.to_series().replace(
    {'China, Macao SAR':'Macao'})
merged.index = merged.index.to_series().replace(
    {'Macao SAR, China':'Macao'})

## Macedonia
merged.index = merged.index.to_series().replace(
    {'TFYR of Macedonia':'Macedonia'})
merged.index = merged.index.to_series().replace(
    {'Macedonia, FYR':'Macedonia'})

## Moldova
merged.index = merged.index.to_series().replace(
    {'Republic of Moldova':'Moldova'})

## Republic of Korea
merged.index = merged.index.to_series().replace(
    {'Republic of Korea':'Korea, Rep.'})

## Slovakia
merged.index = merged.index.to_series().replace(
    {'Slovak Republic':'Slovakia'})

## Tanzania
merged.index = merged.index.to_series().replace(
    {'United Republic of Tanzania':'Tanzania'})

## UK
merged.index = merged.index.to_series().replace(
    {'United Kingdom of Great Britain and Northern Ireland':'United Kingdom'})

## US
merged.index = merged.index.to_series().replace(
    {'United States of America':'United States'})

## Venezuela
merged.index = merged.index.to_series().replace(
    {'Venezuela (Bolivarian Republic of)':'Venezuela'})
merged.index = merged.index.to_series().replace(
    {'Venezuela, RB':'Venezuela'})

## Vietnam
merged.index = merged.index.to_series().replace(
    {'Viet Nam':'Vietnam'})

## Yemen
merged.index = merged.index.to_series().replace(
    {'Yemen, Rep.':'Yemen'})

## Replace all NaN with integer 0, join rows with sum()
merged.ix['Bolivia'].replace(np.nan,0,inplace=True)
merged.ix['Congo, Rep.'].replace(np.nan,0,inplace=True)
merged.ix['Congo, Dem. Rep.'].replace(np.nan,0,inplace=True)
merged.ix['Egypt'].replace(np.nan,0,inplace=True)
merged.ix['Gambia'].replace(np.nan,0,inplace=True)
merged.ix['Hong Kong'].replace(np.nan,0,inplace=True)
merged.ix['Kyrgyzstan'].replace(np.nan,0,inplace=True)
merged.ix['Lao PDR'].replace(np.nan,0,inplace=True)
merged.ix['Libya'].replace(np.nan,0,inplace=True)
merged.ix['Macao'].replace(np.nan,0,inplace=True)
merged.ix['Macedonia'].replace(np.nan,0,inplace=True)
merged.ix['Korea, Rep.'].replace(np.nan,0,inplace=True)
merged.ix['Moldova'].replace(np.nan,0,inplace=True)
merged.ix['Slovakia'].replace(np.nan,0,inplace=True)
merged.ix['United Kingdom'].replace(np.nan,0,inplace=True)
merged.ix['Tanzania'].replace(np.nan,0,inplace=True)
merged.ix['United States'].replace(np.nan,0,inplace=True)
merged.ix['Venezuela'].replace(np.nan,0,inplace=True)
merged.ix['Vietnam'].replace(np.nan,0,inplace=True)
merged.ix['Yemen'].replace(np.nan,0,inplace=True)

merged = merged.groupby(merged.index).sum()

## Drop rows with either no education values or no GDP values
merged = merged.dropna(subset=merged.columns[0:3],how='all')
merged = merged.dropna(subset=merged.columns[5:],how='all')

## Convert 'Year' values from float to string
merged['Year'] = merged['Year'].apply(int).apply(str)

## Fill in log_gdp column with relevant UN data year's log-GDP:
for row in merged.index:
    for col in merged.columns:
        if np.all(merged.ix[row]['Year'] == col):
            merged.ix[row,'log_gdp'] = merged.ix[row,col]




## Analysis
fig = df.plot(x=df.index,
              y='Men',
              kind='bar',
              figsize=(15,5),
             subplots=True,
             legend=False)
fig;
print 'The median education years for men is ' + str(df.Men.median())
print 'The median education years for women is ' + str(df.Women.median())

## Two ways to get a scatter plot
## 1)
total_plot = merged.plot(x='Total',
                         y='log_gdp',
                         kind='scatter')
## 2)
x1 = np.matrix(merged['Total']).transpose()

X = sm.add_constant(x1)
y = np.matrix(merged['log_gdp']).transpose()

results = sm.OLS(y,X).fit()
results.summary()

fig, ax = plt.subplots(figsize=(8,6))
fig = sm.graphics.plot_fit(results, 1, ax=ax)
ax.legend(loc='best');

plt.show()







