# -*- coding: utf-8 -*-
"""
Created on Wed May 31 22:04:52 2023

@author: quitendexit
"""

import csv
import numpy as np

#random forest
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
import joblib

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
windowsize = 2
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

#data pick
pick = [[0,3,6,7,8,10]]
for i in range(0,len(pick)):
    used_datas = ''
    
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
            if grad_on == True and index not in  [0,6]:
                x_train = np.c_[x_train, calc_gradient(train_data_arr.T[index][1:].astype(float))]
                x_test = np.c_[x_test, calc_gradient(test_data_arr.T[index][1:].astype(float))]

##################################################################
#random forest
#############
#O/X
pipe = make_pipeline(
OrdinalEncoder(),
SimpleImputer(strategy = 'mean'),
RandomForestClassifier(n_estimators = 500, max_depth = 7,
                     min_samples_split =3, min_samples_leaf =3,
                     class_weight ={0:8, 1:2} ,n_jobs=-1, 
                     random_state=9, oob_score=True)
)

pipe.fit(x_train, y_train)
print('O/X 학습세트 정확도', (pipe.score(x_train,y_train))*100, '%')
print('O/X 검정세트 정확도', (pipe.score(x_test, y_test))*100, '%')

joblib.dump(pipe, './OX_RandomForest_Model.pkl')

#############
#in out
pipe = make_pipeline(
OrdinalEncoder(),
SimpleImputer(strategy = 'mean'),
RandomForestClassifier(n_estimators = 150, max_depth = 5,
                     min_samples_split =3, min_samples_leaf =3,
                     class_weight ='balanced' ,n_jobs=-1, 
                     random_state=5, oob_score=True)
)

pipe.fit(x_train, y_train_inout)

joblib.dump(pipe, './InOut_RandomForest_Model.pkl')

result_train = pipe.predict(x_train)
result_test = pipe.predict(x_test)
result_train_conv = []
result_test_conv = []

index = 0
repeat = 0
while(repeat != len(result_train)):
    if result_train[repeat] == 'In':
        index = index + 1
        repeat = repeat + 1
        for jj in range(index):
            result_train_conv.append(0)
        index = 0
    elif result_train[repeat] == 'Out':
        index = index + 1
        repeat = repeat + 1
        for jj in range(index):
            result_train_conv.append(1)
        index = 0
    if result_train[repeat] == 'None':
        index = index + 1
        repeat = repeat + 1
if result_train[repeat-index-1] == 'In':
    index = index + 1
    for jj in range(index):
        result_train_conv.append(1)
    index = 0
elif result_train[repeat-index-1] == 'Out':
    index = index + 1
    for jj in range(index):
        result_train_conv.append(0)
    index = 0
    
index = 0
repeat = 0
while(repeat != len(result_test)-1):
    if result_test[repeat] == 'In':
        index = index + 1
        repeat = repeat + 1
        for jj in range(index):
            result_test_conv.append(0)
        index = 0
    elif result_test[repeat] == 'Out':
        index = index + 1
        repeat = repeat + 1
        for jj in range(index):
            result_test_conv.append(1)
        index = 0
    if result_test[repeat] == 'None':
        index = index + 1
        repeat = repeat + 1
if result_test[repeat-index-1] == 'In':
    index = index + 1
    for jj in range(index):
        result_test_conv.append(1)
    index = 0
elif result_test[repeat-index-1] == 'Out':
    index = index + 1
    for jj in range(index):
        result_test_conv.append(0)
    index = 0

correct = 0
accur = 0
for index in range(len(y_train)):
    if int(result_train_conv[index]) == int(y_train[index]):
        correct = correct + 1
print('In/Out 학습세트 정확도', (correct/len(y_train))*100, '%')
correct = 0
for index in range(len(y_test)):
    if int(result_test_conv[index]) == int(y_test[index]):
        correct = correct + 1
print('In/Out 검정세트 정확도', (correct/len(y_test))*100, '%')


