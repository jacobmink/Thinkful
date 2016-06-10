import pandas as pd
from scipy import stats as stats

data = '''Region,Alcohol,Tobacco
North,6.47,4.03
Yorkshire,6.13,3.76
Northeast,6.19,3.77
East Midlands,4.89,3.34
West Midlands,5.63,3.47
East Anglia,4.52,2.92
Southeast,5.89,3.20
Southwest,4.79,2.71
Wales,5.27,3.53
Scotland,6.08,4.51
Northern Ireland,4.02,4.56'''

data = data.splitlines()
#Alternative: data.split('\n')

data = [i.split(',') for i in data]

column_names = data[0] #this is the first row
data_rows = data[1::] # these are all the following rows
df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

# Alcohol stats

mean1 = df['Alcohol'].mean()
median1 = df['Alcohol'].median()
mode1 = stats.mode(df['Alcohol'])
range1 = max(df['Alcohol']) - min(df['Alcohol'])
std1 = df['Alcohol'].std()
var1 = df['Alcohol'].var()

# Tobacco stats

mean2 = df['Tobacco'].mean()
median2 = df['Tobacco'].median()
mode2 = stats.mode(df['Tobacco'])
range2 = max(df['Tobacco']) - min(df['Tobacco'])
std2 = df['Tobacco'].std()
var2 = df['Tobacco'].var()

print('The mean of the Alcohol dataset is {}'.format(mean1) +'\n'+
      'The median of the Alcohol dataset is {}'.format(median1) +'\n'+
      'The mode of the Alcohol dataset is {}'.format(mode1) +'\n'+
      'The range of the Alcohol dataset is {}'.format(range1) +'\n'+
      'The standard deviation of the Alcohol dataset is {}'.format(std1) +'\n'+
      'The variance of the Alcohol dataset is {}'.format(var1) +'\n'+

      'The mean of the Tobacco dataset is {}'.format(mean2) +'\n'+
      'The median of the Tobacco dataset is {}'.format(median2) +'\n'+
      'The mode of the Tobacco dataset is {}'.format(mode2) +'\n'+
      'The range of the Tobacco dataset is {}'.format(range2) +'\n'+
      'The standard deviation of the Tobacco dataset is {}'.format(std2) +'\n'+
      'The variance of the Tobacco dataset is {}'.format(var2)
      )
