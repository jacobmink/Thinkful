import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

interest_rate = loansData['Interest.Rate']
clean_interest_rate = interest_rate.map(lambda x: round(float(x.rstrip('%'))/100,4))
print(clean_interest_rate[0:5])

loan_length = loansData['Loan.Length']
clean_loan_length = loan_length.map(lambda x: x.rstrip('months'))
print(clean_loan_length[0:5])

fico_range = loansData['FICO.Range']
loansData['FICO.Score'] = fico_range.map(lambda x: int(str(x).split('-')[0]))
fico_score = loansData['FICO.Score']
print(fico_score[0:5])

plt.figure()
p = fico_score.hist()
plt.show()

plt.figure()
a = pd.scatter_matrix(loansData, alpha=.05, figsize=(10,10), diagonal='hist')
plt.show()


loan_amount = loansData['Amount.Requested']

y = np.matrix(clean_interest_rate).transpose()

x1 = np.matrix(fico_score).transpose()

x2 = np.matrix(loan_amount).transpose()

x = np.column_stack([x1, x2])

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()
print(f.summary())







