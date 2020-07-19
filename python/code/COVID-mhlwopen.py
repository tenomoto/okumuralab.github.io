#! /usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import time

def readcsv(url):
    try:
        df = pd.read_csv(url, parse_dates=['日付'])
        print('utf-8:', url)
    except UnicodeDecodeError:
        df = pd.read_csv(url, parse_dates=['日付'], encoding='cp932')
        print('cp932:', url)
    return df

now = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime())

# PCR検査陽性者数
df1 = readcsv("https://www.mhlw.go.jp/content/pcr_positive_daily.csv")

# PCR検査実施人数
df2 = readcsv("https://www.mhlw.go.jp/content/pcr_tested_daily.csv")

# 死亡者数
df5 = readcsv("https://www.mhlw.go.jp/content/death_total.csv")

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)

fig, ax = plt.subplots()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
fig.text(0.9, 0.89, 'generated: ' + now, horizontalalignment='right')

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.bar(df2['日付'], df2['PCR 検査実施件数(単日)'], width=1)
ax.bar(df1['日付'], df1['PCR 検査陽性者数(単日)'], width=1)
ax.legend(['Negative', 'Positive'])
fig.savefig('../img/COVID-mhlwopen1.svg', bbox_inches="tight")

ax.clear()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.bar(df1['日付'], df1['PCR 検査陽性者数(単日)'], width=1, color='C1')
ax.bar(df5['日付'], df5['死亡者数'].diff(), width=1, color='C3')
ax.legend(['Positive', 'Deaths'])
fig.savefig('../img/COVID-mhlwopen2.svg', bbox_inches="tight")
