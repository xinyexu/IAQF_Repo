# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:46:41 2019

@author: Hui Cai
"""
import pandas as pd
import numpy as np
#use least square

#https://en.wikipedia.org/wiki/Cox%E2%80%93Ingersoll%E2%80%93Ross_model
r = combined['SPREAD_SHIFT1']
r.index = combined['DATE']

#cannot use CIR, since the r could be negative
#vasicek model

#逻辑是5个月的数据放在一起calibrate一下,然后往前挪一个月
#如此可以算出parameter
#之后做参数MA, 最后可以得到需要的预测

dt = 1/252

import statsmodels.api as sm
y = r.diff()/(dt)**0.5
x1 = pd.DataFrame([(dt)**0.5]*len(y),index = y.index)
x2 = -r*(dt)**0.5

olsData = pd.concat([y,x1,x2],axis = 1).dropna()
olsData.columns = ['y','x1','x2']
olsData['year'] = [d.year for d in olsData.index]
olsData['month'] = [d.month for d in olsData.index]

#接下来按日期做划分进行输入, 5个月一波,1个月向前forward
monthSeries = olsData.resample('M').last()

output = pd.DataFrame(columns = ['start','end','a','b','sigma'])
for i in range(len(monthSeries)-3):
    start = monthSeries.index[i]
    end = monthSeries.index[i+2]
    start = olsData[(olsData['year'] == start.year) & (olsData['month'] == start.month)].index[0]
    end = olsData[(olsData['year'] == end.year) & (olsData['month'] == end.month)].index[-1]
    data = olsData.loc[start:end,['y','x1','x2']]
    
    model = sm.OLS(data['y'],data[['x1','x2']])
    results = model.fit()
    a = results.params['x2']
    b = results.params['x1']/a
    sigma = results.mse_model
    
    new = pd.DataFrame([start,end,a,b,sigma]).T
    new.columns = ['start','end','a','b','sigma']
    output = pd.concat([output,new],axis = 0)

gbmFeature = output[['a','b','sigma']]
gbmFeature.index = combined_monthly.index[2:]
combined_monthly = combined_monthly.join(gbmFeature) 