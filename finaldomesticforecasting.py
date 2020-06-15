# -*- coding: utf-8 -*-
"""FinalDomesticForecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cGnh6Ydy9ge3f7x6Mnl4iuhvX6J985-4
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA

from statsmodels.tsa.statespace.sarimax import SARIMAX

from sklearn.metrics import mean_squared_error,mean_absolute_error

import warnings
warnings.filterwarnings('ignore')

#pip install pyramid-arima

data = pd.read_csv('FinalDomesticDataset.csv')


prophetData = data[['InvoiceDate','AvgNetFare']]

sns.set_style('whitegrid')
size=(19,9)

data

data.info()

data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

data

ax = data.plot(x='InvoiceDate',y='AvgNetFare',figsize=size)

ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter('%b-%y'))
# ax.yaxis.set_minor_locator(AutoMinorLocator(4))
# ax.xaxis.set_minor_locator(AutoMinorLocator(10))

"""Lets Perform the dickey fuller Test"""

data.set_index('InvoiceDate',inplace=True)

def DickeyFullerTest(val):
  ad = adfuller(val['AvgNetFare'])

  print('Crictical Value -   ',ad[0])
  print('P Value -   ',ad[1])
  print('No. of Lag Used -   ',ad[2])
  print('No. of value used -   ',ad[3])

  for key,val in ad[4].items():
    print(key,val)

  if(ad[1]>=0.05):
    print('Data is not Stationary')
  else:
    print('Data is Stationary')

DickeyFullerTest(data)

plot_acf(data['AvgNetFare'],lags=30)

plot_pacf(data['AvgNetFare'],lags=30)

plt.show()

len(data)-30

xTrain,xTest = data['AvgNetFare'][:406],data['AvgNetFare'][406:]

#len(xTest)
xTest

arima = ARIMA(xTrain,order=(10,2,1))
arima = arima.fit()
arima.summary()

pred = arima.forecast(steps=len(xTest))

print(mean_squared_error(xTest,pred[0]))
print(np.sqrt(mean_squared_error(xTest,pred[0])))

#pred

ax=arima.plot_predict(start='2019-05-12' , end='2019-06-10')
ax.set_figheight(9)
ax.set_figwidth(19)

import itertools

"""Auto Arima"""

auto = auto_arima(xTrain,start_p=0,start_q=0,d=0,max_d=9,max_p=30,end_q=30,
                  start_P=0,start_Q=0,D=0,max_P=30,max_Q=30,max_D=30,
                  trace=True,n_jobs=1,station)

auto = auto.fit(xTrain)
pred = auto.predict(len(xTest))

mean_squared_error(xTest,pred)
np.sqrt(mean_squared_error(xTest,pred))

"""Use of SARIMAX"""

sar = SARIMAX(xTrain,order=(6,2,4),seasonal_order=(6,2,4,1),trend='n',)
sar= sar.fit()

pred = sar.forecast(steps=len(xTest))

print(mean_squared_error(xTest,pred))
print(np.sqrt(mean_squared_error(xTest,pred)))


import pickle
# Saving model to disk
pickle.dump(sar, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[2020-01-01]]))
