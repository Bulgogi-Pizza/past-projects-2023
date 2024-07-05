# -*- coding: utf-8 -*-
"""
Created on Wed May 31 22:04:52 2023

@author: quitendexit
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#decision tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from subprocess import check_call
from itertools import combinations

#random forest
from category_encoders import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder

def convert_time_to_minute(time):
    min = 0
    if len(time[10:]) == 4:
        min = int(time[10]) * 60 + int(time[12:])
    elif len(time[10:]) == 5:
        min = int(time[10:12]) * 60 + int(time[13:])

    return min

def calc_gradient(data):
    grad_y = [0]
    
    for i in range(0,len(data)-1):
        x_var = float(data[i+1]) - float(data[i])
        grad_y.append(x_var)
        
    #plt.plot(range(len(grad_y)), grad_y)
    return grad_y


def moving_average(y,strength = 3):
    y = y.T
    y_conv = np.convolve(y,np.ones(strength)/float(strength), mode = 'valid')
    
    return y_conv.T

#open data files
f_test = open('경진대회 DATA/test_data.csv', 'r', encoding='cp949')
f_train = open('경진대회 DATA/train_data.csv', 'r', encoding='cp949')

#read data files
rdr_train = csv.reader(f_train)
rdr_test = csv.reader(f_test)

#read datas without none
train_data = []
test_data = []

for line in rdr_train:
    if line[2] == '':
        pass
    else :
        train_data.append(line)
for line in rdr_test:
    if line[2] == '':
        pass
    else :
        test_data.append(line)

train_data_arr = np.array(train_data)   #train_data array type
test_data_arr = np.array(test_data)     #test_data array type

#convert time to minute
time = train_data_arr[:,0][1:]
for i in range(len(train_data_arr[:,0][1:])):
    train_data_arr[:,0][i+1] = convert_time_to_minute(time[i])

time = test_data_arr[:,0][1:]
for i in range(len(test_data_arr[:,0][1:])):
    test_data_arr[:,0][i+1] = convert_time_to_minute(time[i])


pick = []

biggest = 0
ma_on = True
grad_on = True
windowsize = 3
best_big = []
best_datas = []
best_depth = []

#set y data
if ma_on == True:
    y_train = train_data_arr.T[11][windowsize:].astype(float)
    y_test = test_data_arr.T[11][windowsize:].astype(float)
else :
    y_train = train_data_arr.T[11][1:].astype(float)
    y_test = test_data_arr.T[11][1:].astype(float)

for i in range(len(y_train)):
    if int(y_train[i]) > 0:
        y_train[i] = str(1)
for i in range(len(y_test)):
    if int(y_test[i]) > 0:
        y_test[i] = str(1)
        
#set y for in & out data
y_train_inout = ['None']
y_test_inout = ['None']

for i in range(len(y_train)-1):
    if int(y_train[i]) == 0 and int(y_train[i+1]) == 1:
        y_train_inout.append('In')
    elif int(y_train[i]) == 1 and int(y_train[i+1]) == 0:
        y_train_inout.append('Out')
    elif int(y_train[i]) == int(y_train[i+1]):
        y_train_inout.append('None')
for i in range(len(y_test)-1):
    if int(y_test[i]) == 0 and int(y_test[i+1]) == 1:
        y_test_inout.append('In')
    elif int(y_test[i]) == 1 and int(y_test[i+1]) == 0:
        y_test_inout.append('Out')
    elif int(y_test[i]) == int(y_test[i+1]):
        y_test_inout.append('None')


for max_depth in range(5,6):
    for num in range(6,7):
        pick = list(combinations(range(0,6), num))
        for i in range(0,len(pick)):
            used_datas = ''
            pick = [[0,3,6,7,8,10]]
            for index in pick[i]:
                used_datas = used_datas + ", " + test_data_arr.T[index][0]

            if ma_on == True :
                x_train = moving_average(train_data_arr.T[pick[i][0]][1:].astype(float),windowsize)
                x_test = moving_average(test_data_arr.T[pick[i][0]][1:].astype(float),windowsize)
                for index in pick[i][1:]:
                    x_train = np.c_[x_train, moving_average(train_data_arr.T[index][1:].astype(float),windowsize)]
                    x_test = np.c_[x_test, moving_average(test_data_arr.T[index][1:].astype(float),windowsize)]
                    if grad_on == True and index not in  [0,6]:
                        x_train = np.c_[x_train, calc_gradient(moving_average(train_data_arr.T[index][1:].astype(float),windowsize))]
                        x_test = np.c_[x_test, calc_gradient(moving_average(test_data_arr.T[index][1:].astype(float),windowsize))]
            else :
                x_train = train_data_arr.T[pick[i][0]][1:].astype(float)
                x_test = test_data_arr.T[pick[i][0]][1:].astype(float)
                for index in pick[i][1:]:
                    x_train = np.c_[x_train, train_data_arr.T[index][1:].astype(float)]
                    x_test = np.c_[x_test, test_data_arr.T[index][1:].astype(float)]

            ##################################################################
            #random forest
            for n in [500] :
               for j in [7] :
                    for k in [3] :
                        for l in [3]:
                            for m in [9]:
                                pipe = make_pipeline(
                                OrdinalEncoder(),
                                SimpleImputer(strategy = 'mean'),
                                RandomForestClassifier(n_estimators = 500, max_depth = 7,
                                                     min_samples_split =3, min_samples_leaf =3,
                                                     class_weight ='balanced' ,n_jobs=-1, 
                                                     random_state=9, oob_score=True)
                                )
                                
                                # #origin code
                                # pipe = make_pipeline(
                                # OrdinalEncoder(),
                                # SimpleImputer(strategy = 'mean'),
                                # RandomForestClassifier(n_estimators = 100, max_depth = 5,
                                #                      min_samples_split =6, min_samples_leaf =4,
                                #                      class_weight ='balanced' ,n_jobs=-1, 
                                #                      random_state=2, oob_score=True)
                                # )
                                
                                
                                pipe.fit(x_train, y_train)
                                print(used_datas)
                                print('학습세트 정확도', pipe.score(x_train,y_train))
                                print('검정세트 정확도', pipe.score(x_test, y_test))
                                print(n," ",j," ",k," ",l," ",m)
                                
                                if pipe.score(x_test, y_test) > 0.80:
                                    best_big.append(pipe.score(x_test, y_test))
                                    best_datas.append(used_datas)
                                    
                                # #in out
                                # result_train = pipe.predict(x_train)
                                # result_test = pipe.predict(x_test)
                                # result_train_conv = []
                                # result_test_conv = []
                                
                                # index = 0
                                # repeat = 0
                                # while(repeat != len(result_train)):
                                #     if result_train[repeat] == 'In':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                #         for jj in range(index):
                                #             result_train_conv.append(0)
                                #         index = 0
                                #     elif result_train[repeat] == 'Out':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                #         for jj in range(index):
                                #             result_train_conv.append(1)
                                #         index = 0
                                #     if result_train[repeat] == 'None':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                # if result_train[repeat-index-1] == 'In':
                                #     index = index + 1
                                #     for jj in range(index):
                                #         result_train_conv.append(1)
                                #     index = 0
                                # elif result_train[repeat-index-1] == 'Out':
                                #     index = index + 1
                                #     for jj in range(index):
                                #         result_train_conv.append(0)
                                #     index = 0
                                # #result_train_conv = result_train_conv[1:]
                                    
                                # index = 0
                                # repeat = 0
                                # while(repeat != len(result_test)-1):
                                #     if result_test[repeat] == 'In':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                #         for jj in range(index):
                                #             result_test_conv.append(0)
                                #         index = 0
                                #     elif result_test[repeat] == 'Out':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                #         for jj in range(index):
                                #             result_test_conv.append(1)
                                #         index = 0
                                #     if result_test[repeat] == 'None':
                                #         index = index + 1
                                #         repeat = repeat + 1
                                # if result_test[repeat-index-1] == 'In':
                                #     index = index + 1
                                #     for jj in range(index):
                                #         result_test_conv.append(1)
                                #     index = 0
                                # elif result_test[repeat-index-1] == 'Out':
                                #     index = index + 1
                                #     for jj in range(index):
                                #         result_test_conv.append(0)
                                #     index = 0
                                # #result_test_conv = result_test_conv[1:]
                                
                                # correct = 0
                                # accur = 0
                                # for index in range(len(y_train)):
                                #     if int(result_train_conv[index]) == int(y_train[index]):
                                #         correct = correct + 1
                                # print(correct/len(y_train))
                                # correct = 0
                                # for index in range(len(y_test)):
                                #     if int(result_test_conv[index]) == int(y_test[index]):
                                #         correct = correct + 1
                                # print(correct/len(y_test))
            
              
            #################################################################
            # #decision tree
            # tree_model = DecisionTreeClassifier(max_depth=max_depth)
            # tree_model.fit(x_train,y_train)
            
            # result = tree_model.predict(x_test)
              
            # same = 0
            # wrong = 0
              
            # for i in range(len(result)):
            #   if result[i] == y_test[i]:
            #     same = same + 1
            #   else :
            #     wrong = wrong + 1
              
            # print(used_datas, max_depth)
            # print("(O/X) = (",same,"/",wrong,")")
            # print(( same / len(result) ) * 100)
              
            # accuracy = ( same / len(result) ) * 100
              
            # if accuracy > biggest :
            #   biggest = accuracy
            #   best_big.append(biggest)
            #   best_datas.append(used_datas)
            #   best_depth.append(max_depth)
            #   print("****** new record - ", biggest)
            #   print("******",used_datas, max_depth)


