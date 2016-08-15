import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from sklearn.cross_validation import KFold
import sklearn.metrics as metrics

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

loansData['Interest.Rate'] = loansData['Interest.Rate'].map(
                    lambda x: round(float(x.rstrip('%'))/100,4))
clean_interest_rate = loansData['Interest.Rate']

loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))
clean_loan_length = loansData['Loan.Length']

loansData['FICO.Score'] = loansData['FICO.Range'].map(
                        lambda x: int(str(x).split('-')[0]))
fico_score = loansData['FICO.Score']

loan_amount = loansData['Amount.Requested']

y = np.matrix(clean_interest_rate).transpose()
x1 = np.matrix(fico_score).transpose()
x2 = np.matrix(loan_amount).transpose()
x = np.column_stack([x1, x2])
X = sm.add_constant(x)

model = sm.OLS(y, X)
f = model.fit()
f.summary()

kf = KFold(len(X), n_folds=10)
mae_train_list = []
mae_test_list = []
mse_train_list = []
mse_test_list = []
r2_train_list = []
r2_test_list = []
for train, test in kf:
#     print train, '\n', test, '\n'
    f = sm.OLS(y[train], X[train]).fit()
    mae_train = metrics.mean_absolute_error(y[train],
                                            f.predict(X[train]))
    mae_test = metrics.mean_absolute_error(y[test],
                                           f.predict(X[test]))
    mse_train = metrics.mean_squared_error(y[train],
                                           f.predict(X[train]))
    mse_test = metrics.mean_squared_error(y[test],
                                          f.predict(X[test]))
    r2_train = metrics.r2_score(y[train],f.predict(X[train]))
    r2_test = metrics.r2_score(y[test],f.predict(X[test]))
    mae_train_list.append(mae_train)
    mae_test_list.append(mae_test)
    mse_train_list.append(mse_train)
    mse_test_list.append(mse_test)
    r2_train_list.append(r2_train)
    r2_test_list.append(r2_test)
    print 'Mean Absolute Error: train {}, test {}'.format(mae_train, 
                                                          mae_test)
    print 'Mean Squared Error: train {}, test {}'.format(mse_train, 
                                                         mse_test)
    print 'R-Squared: train {}, test {}'.format(r2_train,
                                                r2_test)
    print ''

avg_mse_train = sum(mse_train_list)/kf.n_folds
avg_mse_test = sum(mse_test_list)/kf.n_folds
avg_mae_train = sum(mae_train_list)/kf.n_folds
avg_mae_test = sum(mae_test_list)/kf.n_folds
avg_r2_train = sum(r2_train_list)/kf.n_folds
avg_r2_test = sum(r2_test_list)/kf.n_folds

print 'Average MAE: {}'.format(avg_mae_test)
print '\nAverage MSE: {}'.format(avg_mse_test)
print '\nAverage R-Squared: {}'.format(avg_r2_test)











