import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../data/osakadeaths.csv')

def days(year, month):
    m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return m[month - 1] + ((month == 2) and
                           ((year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)))

perday = np.array([r[2] / days(r[0], r[1]) for i, r in df.iterrows()])

plt.clf()
for y in range(2015, 2021):
    plt.plot(df[df['year'] == y]['month'], perday[df['year'] == y], 'o-', label=y)

plt.legend()
plt.savefig('../img/osakadeaths.svg', bbox_inches="tight")

plt.clf()
plt.plot(df[df['month'] == 1]['year'], perday[df['month'] == 1], 'o-', label='Jan')
plt.plot(df[df['month'] == 2]['year'], perday[df['month'] == 2], 'o-', label='Feb')
plt.plot(df[df['month'] == 3]['year'], perday[df['month'] == 3], 'o-', label='Mar')
plt.plot(df[df['month'] == 4]['year'], perday[df['month'] == 4], 'o-', label='Apr')
plt.plot(df[df['month'] == 5]['year'], perday[df['month'] == 5], 'o-', label='May')
plt.xticks(range(2016, 2021))
plt.legend()
plt.savefig('../img/osakadeaths1.svg', bbox_inches="tight")

