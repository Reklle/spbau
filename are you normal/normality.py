import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


def skewness(x):
    return ((x - x.mean()) ** 3).mean() / np.std(x) ** 3


def kurtosis(x):
    return ((x - x.mean()) ** 4).mean() / np.std(x) ** 4 - 3


# resistance values
data = pd.read_excel("data.xlsx")
k = kurtosis(data["r"])
s = skewness(data["r"])
print("Skewness", s)
print("Kurtosis", k)
print(data["r"].std())


print(stats.shapiro(data["r"]))  # probably the best test if kurtosis > 0
print(stats.kstest(data["r"], 'norm'))  # Kolmogorov-Smirnov test for normality
print(stats.normaltest(data["r"]))  # Test whether a sample differs from a normal distribution.

sns.histplot(data)
plt.show()
