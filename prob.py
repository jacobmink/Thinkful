import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import collections

x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

c = collections.Counter(x)
print(c)

count_sum = sum(c.values())

for k,v in c.iteritems():
    print("The frequency of number " + str(k) + " is " + str(float(v)/count_sum))

plt.figure(1)
plt.boxplot(x)
plt.savefig("boxplot_challenge.png")
plt.show()

plt.figure(2)
plt.hist(x, histtype = 'bar')
plt.savefig("hist_challenge.png")
plt.show()

plt.figure(3)
graph1 = stats.probplot(x, dist = 'norm', plot = plt)
plt.savefig("qq_challenge.png")
plt.show()
