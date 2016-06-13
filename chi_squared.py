from scipy import stats
import matplotlib.pyplot as plt
import collections
import pandas as pd

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])
print(freq)

chi, p = stats.chisquare(freq.values())
print("The chi-squared test result is chi=" + str(chi) + " and p=" + str(p))

plt.figure()
plt.bar(freq.keys(), freq.values(), width = 1)
plt.show()


