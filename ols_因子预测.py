
import pandas as pd
import numpy as ny
from datetime import datetime,timedelta
import os
from WindPy import w
from time import time
from multiprocessing import Process
from os import getpid
import pandas as pd
import statsmodels.api as sm

'''
dataframe遍历
字典转pd
多元线性回归
cd = 'F:\Projects\***\Data'

'''



def get_month(t):
    t = pd.Timestamp(t)
    t = t.to_period(freq = 'M')
    return t

def get_months(t):
    for index, value in enumerate(t):
        t[index] = get_month(t[index])
    return t

#获取wind数据：.Data[0]贴现承兑余额:电子银票, .Data[1]票据贴现发生额:电子银票
def wind_data(t1, t2):
    ef1 = time()
    w.start()
    # bill = w.edb("M0329670,M0329682", m1, m2,"Fill=Previous")
    w_data = w.edb("M0331243,M0329686", t1, t2,"Fill=Previous")
    t = w_data.Times

    d = pd.DataFrame(w_data.Data).T

    d.columns = ['余额', '发生额']
    # d.loc['due'] = '0'
    for index, row in d.iterrows():
        if index >= 2:
            d.loc[index,'due'] = (d.loc[index-1,'余额'] 
            + d.loc[index,'发生额'] - d.loc[index,'余额'])
    ef2 = time()

 
    print('...1.Wind data loaded, ~ Time:', '%.3f' % (ef2 - ef1))
    print('...  Data from %s to %s, len = %d' 
           % (get_month(t[0]), get_month(t[-1]), len(t)))
        
    d['date'] = get_months(t)
    print('...  data.head(10):\n', d.head(10))
    return d

def f1(d):
    r = {'y':[],'x1':[],'x3':[],'x6':[],'x9':[],'x12':[]}
    for index, row in d.iterrows():
        if get_month('2020-07') <= row['date'] <= get_month('2021-06'):
            r['y'].append(row['due']) 
            r['x1'].append(d['发生额'][index - 1])
            r['x3'].append(d['发生额'][index - 3])
            r['x6'].append(d['发生额'][index - 6])
            r['x9'].append(d['发生额'][index - 9])
            r['x12'].append(d['发生额'][index - 12])
    r = pd.DataFrame(r)
    print('...2.y~x:\n',r)
    return r

    
def reg(y,x):
    x = sm.add_constant(x)
    model = sm.OLS(y,x).fit()
    print('...3.OLS:\n', model.summary())
    return model


if __name__ == '__main__':


    df = wind_data('2018-01', '2021-12')
    func = f1(df)
    Y = func['y']
    X = func.iloc[:, 1:]
    m = reg(Y,X)



    




