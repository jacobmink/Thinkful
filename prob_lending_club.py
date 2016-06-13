import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

loansData.dropna(inplace = True)

loansData.boxplot(column = 'Amount.Requested')
plt.savefig('lending_data_box.png')
plt.show()

loansData.hist(column = 'Amount.Requested')
plt.savefig('lending_data_hist.png')
plt.show()

# Slightly lower frequency in the 7500-10000 range as compared to 'Amount.Funded.By.Investors',
# but otherwise similar distribution.

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist = 'norm', plot=plt)
plt.savefig('lending_data_qq.png')
plt.show()

# Similar distribution shape as 'Amount.Funded.By.Investors'

