import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

df = pd.read_csv('loansData_clean.csv')

int_rate = df['Interest.Rate']
annual_inc = df['Monthly.Income']
home_own = df['Home.Ownership']


## interest_rate = intercept + m1*x1
est_inc = smf.ols(formula='int_rate ~ annual_inc', data=df).fit()

coeff1 = est_inc.params

print(coeff1)
## Intercept     1.299563e-01
## annual_inc    1.294174e-07


## interest_rate = intercept + m1*x1 + m2*x2
est_own = smf.ols(formula='int_rate ~ annual_inc + home_own',data=df).fit()

coeff2 = est_own.params
print(coeff2)
## Intercept            1.253830e-01
## home_own[T.NONE]     5.255071e-14
## home_own[T.OTHER]    3.329327e-02
## home_own[T.OWN]      2.217405e-03
## home_own[T.RENT]     7.251277e-03
## annual_inc           3.058832e-07


## interest_rate = intercept + m1*x1 + m2*x2 + m3*x1*x2
est_combo = smf.ols(formula='int_rate ~ annual_inc * home_own',data=df).fit()

coeff3 = est_combo.params
print(coeff3)
##Intercept                       1.267167e-01
##home_own[T.NONE]                1.630260e-14
##home_own[T.OTHER]              -1.834501e-02
##home_own[T.OWN]                 3.050651e-03
##home_own[T.RENT]                2.115482e-03
##annual_inc                      1.047017e-07
##annual_inc:home_own[T.NONE]    -6.908907e-18
##annual_inc:home_own[T.OTHER]    9.232619e-06
##annual_inc:home_own[T.OWN]     -2.529469e-07
##annual_inc:home_own[T.RENT]     9.759820e-07

income_linspace = np.linspace(df['Monthly.Income'].min(),df['Monthly.Income'].max(),100)

plt.scatter(df['Monthly.Income'],df['Interest.Rate'], alpha=0.3)
plt.xlabel('Annual Income')
plt.ylabel('Interest Rate')

plt.plot(income_linspace, coeff1[0] + coeff1[1]*income_linspace, label='income')
plt.plot(income_linspace, coeff2[0] + coeff2[5]*income_linspace + coeff2[3]*1, label='income + home ownership')
##plt.plot(income_linspace, coeff2[0] + coeff2[5]*income_linspace + coeff2[3]*0, label='est_own2')
plt.plot(income_linspace, coeff3[0] + coeff3[5]*income_linspace + coeff3[3]*1 + coeff3[8]*1*income_linspace, label='income * home ownership')

plt.legend()

plt.show()

