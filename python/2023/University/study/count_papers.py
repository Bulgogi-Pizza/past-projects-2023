# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:31:24 2023

@author: esc
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

f_name = "C:/Users/quite/Desktop/Deep_learning_Algorithms/total_delete_linechange.xlsx"
#f_name = "/Users/cdi/Library/CloudStorage/GoogleDrive-quitendexit@gmail.com/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_delete_linechange.xlsx"
df = pd.read_excel(f_name, sheet_name=None, engine = 'openpyxl')
sheets = list(df.keys())

lists = []
lists_2 = []
x = list(range(2015,2023,1))
i = 0
for key in sheets:
    i = i + 1
    lists.append([key+"_15_18",0])
    lists.append([key+"_19_22",0])
    lists_2.append([key,0,0,0,0,0,0,0,0])

    years = df[key]['date']
    
    for year in years:
        try :
            if int(year) < int(2019) :
                lists[-2][1] = lists[-2][1] + 1
            elif int(year) > int(2018) :
                lists[-1][1] = lists[-1][1] + 1
        except : pass

    for year in years:
        try :
            if int(year) > 2014 :
                lists_2[-1][int(year)-2023] = lists_2[-1][int(year)-2023] + 1
        except : pass

    fit = np.polyfit(x,lists_2[-1][1:],2)
    
    fit2 = fit[0]*np.array(x)**2 + fit[1]*np.array(x) + fit[2]
        
    #plt.subplot(1,23,i)
    plt.plot(x,fit2)
    plt.scatter(x,lists_2[-1][1:])
    total = sum(lists_2[-1][1:])
    
    temp = None
    for i in range(1,len(fit2)-1):
        if fit2[i-1] < fit2[i] and fit2[i] > fit2[i+1]:
            temp = "cold"
        elif fit2[i-1] > fit2[i] and fit2[i] < fit2[i+1]:
            temp = "hot"
        elif fit2[0] > fit2[-1]:
            temp = "cold"
        elif fit2[0] < fit2[-1]:
            temp = "hot"
    
    print(key + " - " + temp + str(total))
        
    print(fit)
    #print()
    
        
    X = np.reshape(x,(8,1))
    Y = lists_2[-1][1:]
    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly_features.fit_transform(X)
    
    print(x[0])
    print(X_poly[0])
    
    lin_reg = LinearRegression()
    lin_reg.fit(X_poly,Y)
    lin_reg.intercept_ , lin_reg.coef_
    
    print()
    
    X_new = np.linspace(2015,2022,8).reshape(8,1)
    X_new_poly = poly_features.transform(X_new)
    Y_new = lin_reg.predict(X_new_poly)
    
    #plt.subplot(X,Y,"b.")
    #plt.plot(X_new,Y_new,"r-", linewidth=2)

















