#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportion_confint

df = pd.read_csv("../data/COVID-mhlw.csv", index_col='Date', parse_dates=['Date'])

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.bar(df.index, df['Examined'])
ax.bar(df.index, df['Confirmed'])
ax.legend(['Negative', 'Positive'])

fig.savefig('../img/COVID-mhlw2.svg', bbox_inches="tight")

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
dt = (df.index.to_series().diff() / pd.Timedelta(days=1))
ex = df['Examined'].diff() / dt
# ex1 = ex.copy()
# ex1['2020-03-04 12:00'] = 0
# m = max(ex1.max()*1.1, 300)
# plt.ylim(0, m)
m = 1500
ax.set_ylim(0, m)
ax.bar(df.index, ex, width=-dt+0.1, align='edge')
ax.bar(df.index, df['Confirmed'].diff() / dt, width=-dt+0.1, align='edge')
# t = pd.Timestamp('2020-03-04 00:00')
# ax.text(t, m, '☁', # U+2601 (CLOUD)
#         fontsize=60, color="lightgray",
#         horizontalalignment='center', verticalalignment='center')
for t in df.index:
    if ex[t] > m:
        ax.text(t, m, int(ex[t]), fontsize=8,
                horizontalalignment='center', bbox=dict(facecolor='white'))
ax.legend(['Negative', 'Positive'])
# ax.plot([pd.Timestamp('2020-03-03 12:00'), pd.Timestamp('2020-03-04 12:00')],
#         [m*0.95, m*0.98], '-w', linewidth=2)
fig.savefig('../img/COVID-mhlw3.svg', bbox_inches="tight")

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
p = df['Confirmed'].diff() / df['Examined'].diff()
ci0, ci1 = np.array([proportion_confint(x['Confirmed'], x['Examined'], method='beta')
                     for i, x in df.diff().iterrows()]).T
ax.errorbar(df.index, p, [p - ci0, ci1 - p], fmt="o", capsize=5, color="C1")
ax.grid(axis='y')
fig.savefig('../img/COVID-mhlw4.svg', bbox_inches="tight")

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
p = [x['Confirmed'] / x['Examined'] for i, x in df.iterrows()]
ci0, ci1 = np.array([proportion_confint(x['Confirmed'], x['Examined'], method='beta')
                     for i, x in df.iterrows()]).T
ax.errorbar(df.index, p, [p - ci0, ci1 - p], fmt="o", capsize=5, color="C1")
ax.grid(axis='y')

fig.savefig('../img/COVID-mhlw.svg', bbox_inches="tight")

#-----

cmap = plt.get_cmap("tab20")

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

for x, c in zip(['Confirmed', 'Hospitalized', 'Deaths'], [3, 2, 6]):
    ax.bar(df.index, df[x].diff() / dt, width=-dt+0.1, align='edge', color=cmap(c), label=x)
ax.legend(loc='upper left')

fig.savefig('../img/COVID-mhlw5.svg', bbox_inches="tight")
