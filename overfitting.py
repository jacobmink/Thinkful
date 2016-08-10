import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Set seed for reproducible results
np.random.seed(414)

# Generate toy data
X = np.linspace(0, 15, 1000)
y = 3 * np.sin(X) + np.random.normal(1 + X, .2, 1000)

train_X, train_y = X[:700], y[:700]
test_X, test_y = X[700:], y[700:]

train_df = pd.DataFrame({'X': train_X, 'y': train_y})
test_df = pd.DataFrame({'X': test_X, 'y': test_y})

# Linear fit
poly_1 = smf.ols(formula='y ~ 1 + X', data=train_df).fit()

# Quadratic fit
poly_2 = smf.ols(formula='y ~ 1 + X + I(X**2)',
                 data=train_df).fit()

# Cubic fit
poly_3 = smf.ols(formula='y ~ 1 + X + I(X**2) + I(X**3)',
                 data=train_df).fit()

# Quartic fit
poly_4 = smf.ols(formula='y ~ 1 + X + I(X**2) + I(X**3) + I(X**4)',
                 data=train_df).fit()


## Run prediction on training set
y_train_1 = poly_1.predict(train_df)
y_train_2 = poly_2.predict(train_df)
y_train_3 = poly_3.predict(train_df)
y_train_4 = poly_4.predict(train_df)

    ## Calculate error
train_difference_1 = y_train_1 - train_y
train_difference_2 = y_train_2 - train_y
train_difference_3 = y_train_3 - train_y
train_difference_4 = y_train_4 - train_y

    ## Calculate mean squared error and root MSE
train_rmse_1 = (sum((train_difference_1)**2)/len(train_y))**0.5
train_mse_1 = sum((train_difference_1)**2)/len(train_y)
train_rmse_2 = (sum((train_difference_2)**2)/len(train_y))**0.5
train_mse_2 = sum((train_difference_2)**2)/len(train_y)
train_rmse_3 = (sum((train_difference_3)**2)/len(train_y))**0.5
train_mse_3 = sum((train_difference_3)**2)/len(train_y)
train_rmse_4 = (sum((train_difference_4)**2)/len(train_y))**0.5
train_mse_4 = sum((train_difference_4)**2)/len(train_y)



## Run prediction on testing set
y_predict_1 = poly_1.predict(test_df)
y_predict_2 = poly_2.predict(test_df)
y_predict_3 = poly_3.predict(test_df)
y_predict_4 = poly_4.predict(test_df)

    ## Calculate error
difference_1 = y_predict_1 - test_y
difference_2 = y_predict_2 - test_y
difference_3 = y_predict_3 - test_y
difference_4 = y_predict_4 - test_y

    ## Calculate mean squared error and root MSE
rmse_1 = (sum((difference_1)**2)/len(test_y))**0.5
mse_1 = sum((difference_1)**2)/len(test_y)
rmse_2 = (sum((difference_2)**2)/len(test_y))**0.5
mse_2 = sum((difference_2)**2)/len(test_y)
rmse_3 = (sum((difference_3)**2)/len(test_y))**0.5
mse_3 = sum((difference_3)**2)/len(test_y)
rmse_4 = (sum((difference_4)**2)/len(test_y))**0.5
mse_4 = sum((difference_4)**2)/len(test_y)

## Print results

print 'TRAINING SET:'
print 'Linear RMSE = {:.2f}, Linear MSE = {:.2f}'.format(train_rmse_1,
                                               train_mse_1)
print 'Quadratic RMSE = {:.2f}, Quadratic MSE = {:.2f}'.format(train_rmse_2,
                                               train_mse_2)
print 'Cubic RMSE = {:.2f}, Cubic MSE = {:.2f}'.format(train_rmse_3,
                                               train_mse_3)
print 'Quartic RMSE = {:.2f}, Quartic MSE = {:.2f}'.format(train_rmse_4,
                                               train_mse_4)
print 'TESTING SET:'
print 'Linear RMSE = {:.2f}, Linear MSE = {:.2f}'.format(rmse_1,mse_1)
print 'Quadratic RMSE = {:.2f}, Quadratic MSE = {:.2f}'.format(rmse_2,mse_2)
print 'Cubic RMSE = {:.2f}, Cubic MSE = {:.2f}'.format(rmse_3,mse_3)
print 'Quartic RMSE = {:.2f}, Quartic MSE = {:.2f}'.format(rmse_4,mse_4)


## Plots

fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(poly_1,1,ax=ax)
fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(poly_2,1,ax=ax)
fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(poly_3,1,ax=ax)
fig, ax = plt.subplots()
fig = sm.graphics.plot_fit(poly_4,1,ax=ax)

plt.show()

