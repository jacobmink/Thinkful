import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

loansData_clean = pd.read_csv('loansData_clean.csv')


ir_tf = pd.Series(loansData_clean['Interest.Rate'])
test = ir_tf < .12

loansData_clean['IR_TF'] = test

loansData_clean['Constant.Intercept'] = 1.0

ind_vars = ['FICO.Score','Amount.Requested','Constant.Intercept']

## Probability of loan for $10,000 @ <= .12 w/ FICO = 750
## p(x) = 1/(1 + e^{-(mx + b)})
## Probability threshold = 70%

##print(loansData_clean.describe())

logit = sm.Logit(loansData_clean['IR_TF'], loansData_clean[ind_vars])

result = logit.fit()

coeff = result.params
print(coeff)

def logistic_function(intercept, coeff1, coeff2, x1, x2):
    p = 1/(1 + np.exp(-(intercept + coeff1*x1 - coeff2*x2)))
    return p

probability_720 = logistic_function(coeff[2],coeff[0],coeff[1], 720, 10000)
probability_750 = logistic_function(coeff[2],coeff[0],coeff[1], 750, 10000)

X = np.linspace(500,1000,500)

prob_plot = logistic_function(coeff[2],coeff[0],coeff[1], X, 10000).ravel()

print('Probability at FICO score of 720: ' + str(probability_720*100) + ' %')
print('Probability at FICO score of 750: ' + str(probability_750*100) + ' %')

plt.plot(X, prob_plot, linewidth=2)

plt.ylabel('Probability')
plt.xlabel('FICO Score')
plt.ylim(-.01,1.01)
plt.xlim(500,1000)

plt.show()

