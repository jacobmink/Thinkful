import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = pd.read_csv('LoanStats3b.csv', header=1, low_memory=False)

df['issue_d_format'] = pd.to_datetime(df['issue_d'])

dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

fig = plt.figure()
fig = loan_count_summary.plot()
fig = sm.graphics.tsa.plot_acf(loan_count_summary)
print 'There are no noticeable autocorrelated structures in the data.'
fig = sm.graphics.tsa.plot_pacf(loan_count_summary)

fig = plt.show()
