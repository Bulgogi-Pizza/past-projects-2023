#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:37:47 2023

@author: cdi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import csv
import os
import sys

def make_numeric(string, back = False):
    for i in range(1,len(string)):
        if string.isnumeric():
            break
        elif back == False :
            string = string[1:]
        else :
            string = string[:-1]
    
    return int(string)

def make_float(string, back = False):
    for i in range(1,len(string)):
        try : 
            float(string)
            break
        except :
            pass
        
        if back == False :
            string = string[1:]
        else :
            string = string[:-1]

    return float(string)

def moving_average(x,y):
    y_conv = np.convolve(y,np.ones(7)/float(7), mode = 'valid')
    x_dat = np.linspace(np.min(x), np.max(x), np.size(y_conv))
    
    return x_dat, y_conv

##############################################################################
##### initial setting ########################################################
##############################################################################
debugging_mode = False
make_smooth = False
High_DPI = False
one_Hz = False
point_size = 1
circle_size = 0.5
extraction_sec = 1
peaks = 20
high_p = 75
low_p = 5
sampling = 1
center_linelength = 2325



#File Select
datas = os.listdir('data')
filename = datas[18]
data = "data/" + filename

#is that 1Hz file?
if filename[:3] == "1Hz" :
    one_Hz = True 
else :
    one_Hz = False

#FSR 자동 추출
FSR = filename.find("GHz")
if FSR != -1 :
    FSR = filename[FSR-4:FSR]
    FSR = make_float(FSR)
else :
    print(filename)
    FSR = float(input("FSR이 자동 추출되지 않았습니다. 수동으로 입력하시기 바랍니다.\nFSR(GHz) - "))

#Sampling Num 추출
MS = filename.find("MS")
KS = filename.find("KS")
if MS != -1 :
    sampling = filename[MS-3:MS]
    sampling = make_numeric(sampling)
    sampling = int(sampling) * pow(10,6)
elif KS != -1 :
    sampling = filename[KS-3:KS]
    sampling = make_numeric(sampling)
    sampling = int(sampling) * pow(10,3)
else :
    print(filename)
    print("샘플링 횟수를 인식할 수 없습니다. \n수동 입력 바랍니다.")
    sampling = int(input("samplings - "))

#Hz 추출
Hz = filename[:6]
K = False
M = False
float_or_int = Hz.find(".")
if Hz.find("k") != -1:
    K = True
elif Hz.find("m") != -1:
    M = True
if Hz.find("Hz") != -1 :
    if float_or_int != -1 :
        Hz = make_float(Hz,back = True)
    else :
        Hz = make_numeric(Hz, back = True)
    
    if K :
        Hz = Hz * 1000
    elif M :
        Hz = Hz * 1000000
else :
    print(filename)
    print("Hz를 인식할 수 없습니다. \n수동 입력 바랍니다.")
    Hz = float(input("Hz - "))
    
#램프파 기준 샘플링 개수 계산
lamp_sampling = int(sampling / Hz / extraction_sec)
lamp_range = int(lamp_sampling * 1.1)

if (lamp_sampling//peaks)//2 < 4:
    print("추출 강도가 너무 강합니다.")
    sys.exit()
    

print("#### -Parameters- ####")
print("Extraction Strength : ",str(peaks))
print("Start point : ",str(high_p))
print("End point : ",str(low_p))
print("-----------------------------------")
print("Selected file name : ",data)
print("FSR(GHz) : ",str(FSR))
print("sampling nums : ",str(sampling))
print("Hz : ",str(Hz))

#data load
l = 0
dd = []
tt = False
if data[-3:] == 'txt':
    f = open(data,'r',encoding='cp949')
    rdr = csv.reader(f)
    for line in rdr:
        if l > 2 and '\t' in line[0]:
            line = line[0].split('\t')
            line = [float(line[0]), float(line[1])]
            dd.append(line)
            tt = True
        l = l + 1
    if tt :
        data = np.array(dd)
    f.close()
if not tt :
    data = pd.read_csv(data, encoding='cp949')
    data = np.array(data)
    
time = data[:,0]
data = data[:,1]

#make graph more smooth
if make_smooth :
    time_moved , data_moved = moving_average(time,data)
    #plt.plot(range(1,len(data_moved)+1),data_moved,linewidth = 0.3)
    
    time = time_moved
    data = data_moved

#set version
ver = 3
while(ver != 0 or ver != 1 or ver != 2) :
    #ver = int(input("version(1-auto, 2-manual, 0 - exit) - "))
    ver = 1
    
    if ver == 0:
        quit()
    if ver == 1:
        break
    if ver == 2:
        #피크에 점이 찍히지 않으면 추출 강도를 높임.
        #피크가 아닌 곳에도 점이 찍히면 추출 강도를 낮춤.
        peaks = int(input("추출 강도 (default = 20) - "))
        high_p = float(input("set peak start[0-100] (default = 80) - "))
        low_p = float(input("set peak end[0-100] (default = 25) - "))
        break
    
#set FSR
#FSR = float(input("FSR(GHz) - "))
var1 = (FSR * (pow(10,9))) / (2.99 * (pow(10,10)))

#find and set max, min points
data_max = np.max(data)
data_min = np.min(data)
data_low20 = data_min + ((data_max - data_min) * 0.2)
data_low15 = data_min + ((data_max - data_min) * 0.15)
data_low1 = data_min + ((data_max - data_min) * 0.01)
data_high90 = data_min + ((data_max - data_min) * 0.8)

#for debugging
if debugging_mode :
    plt.subplot(3,1,1)
    plt.plot(range(1,lamp_range+1),data[0:lamp_range],linewidth = 0.3)
# print(len(data))
# print(data_max)
# print(data_min)

for i in range(0,len(data)):
    if data_low1 > data[i] :
        sss = i + lamp_sampling
        break

if debugging_mode :
    plt.subplot(3,1,2)
    plt.plot(range(sss+1,lamp_range+1+sss),data[sss:lamp_range+sss],linewidth = 0.3)

#데이터 추출
std = 0
start_graph = 0
end_graph = 0
next_p = 0
if not one_Hz :
    for i in range(0,len(data)):    
        if data_low20 >= data[i] >= data_low15 and next_p == 0 :
            std = std + 1
            next_p = 1
        if (data[i] <= data_low1 or data[i] >= data_high90) and next_p == 1 :
            next_p = 0
        if std == 5:
            start_graph = i
        if std == 8:
            end_graph = i
            break
    
    if start_graph == 0 or end_graph == 0:
        print("그래프 부분 추출 실패")
        plt.plot(range(1,len(data)+1),data,linewidth = 0.3)
        print("수동으로 고점과 저점을 지정하십시오.")
        data_max = input("고점 - ")
        data_min = input("저점 - ")
        
        data_low20 = data_min + ((data_max - data_min) * 0.10)
        data_low15 = data_min + ((data_max - data_min) * 0.05)
        data_low1 = data_min + ((data_max - data_min) * 0.005)
        data_high90 = data_min + ((data_max - data_min) * 0.95)
        
        #for debugging
        #plt.plot(range(1,5001),data[0:5000],linewidth = 0.3)
        # print(len(data))
        # print(data_max)
        # print(data_min)
        
        #데이터 추출
        std = 0
        start_graph = 0
        end_graph = 0
        next_p = 0
        for i in range(0,len(data)):    
            if data_low20 >= data[i] >= data_low15 and next_p == 0 :
                std = std + 1
                next_p = 1
            if (data[i] <= data_low1 or data[i] >= data_high90) and next_p == 1 :
                next_p = 0
            if std == 5:
                start_graph = i
            if std == 8:
                end_graph = i
                break
            
        if start_graph == 0 or end_graph == 0 :
            print("수동 추출 실패, 프로그램을 종료합니다.")
            sys.exit()
else :
    for i in range(0,len(data)):    
        if data_low20 >= data[i] >= data_low15 and next_p == 0 :
            std = std + 1
            next_p = 1
        if (data[i] <= data_low1 or data[i] >= data_high90) and next_p == 1 :
            next_p = 0
        if std == 5:
            start_graph = i
        if std == 8:
            end_graph = i
            break
    end_graph = len(data)
    
start_graph = sss
end_graph = sss + lamp_range
    


#redefine graph
do = data
data = data[start_graph:end_graph]
if debugging_mode : 
    plt.subplot(3,1,3)
plt.plot(range(1,len(data)+1),data,linewidth = 0.3)

#find and set max, min points
data_max = np.max(data)
data_min = np.min(data)
data_high = data_min + ((data_max - data_min) * (high_p/100))
data_low = data_min + ((data_max - data_min) * (low_p/100))
start_p = 0
end_p = 0

#set graph's start point and end point
for i in range(0,len(data)):
    if data[i] >= data_max :
        start_p = i
    if start_p != 0 and data[i] > data_high :
        start_p = i
    if start_p != 0 and data[i] < data_low :
        end_p = i
        break



#pick crests and vallies
calc_width = (lamp_sampling//peaks)//2
i = start_p
crest = []
valley = []
while(i != end_p-calc_width):
    data_strip = data[i:i+calc_width]
    
    if(np.max(data_strip) == data_strip[calc_width//2-1]):
        crest.append(i+calc_width//2-1)
    if(np.min(data_strip) == data_strip[calc_width//2-1]):
        valley.append(i+calc_width//2-1)
    
    i = i + 1
    
#calculate etalon value
try : etalon = var1 * (len(crest) - 1) / (crest[-1] - crest[0])
except IndexError :
    print("추출 강도가 낮아 에탈론이 추출되지 않았습니다. 추출 강도를 높이길 추천합니다.")
    sys.exit()

#calc scan range
font = {'size' : 5}
font1 = {'size' : point_size}
font2 = {'size' : 8}

peak_nums = len(crest)
center_linenumber = 10000000 / center_linelength
start_linenumber = center_linenumber - (etalon * ((peak_nums-1) //2))
end_linenumber = center_linenumber + (etalon * ((peak_nums-1) //2))
start_linelength = 10000000 / start_linenumber
end_linelength = 10000000 / end_linenumber

plt.stem(crest[0],data[crest[0]],'r:')
plt.stem(crest[len(crest)//2],data[crest[len(crest)//2]],'r:')
plt.stem(crest[-1],data[crest[-1]],'r:')

plt.text(crest[0],0,str(round(start_linelength,3)) + "nm",fontdict = font)
plt.text(crest[len(crest)//2],0,str(round(center_linelength,3)) + "nm",fontdict = font)
plt.text(crest[-1],0,str(round(end_linelength,3)) + "nm", fontdict = font)

#draw the graph
if High_DPI :
    plt.rcParams["figure.dpi"] = 5000
else :
    plt.rcParams["figure.dpi"] = 1000

if debugging_mode :
    plt.plot(range(1,len(data)+1),data,linewidth = 0.3)
for i in range(0,len(crest)):
    plt.scatter(crest[i],data[crest[i]],s=circle_size, c='r')
    plt.text(crest[i],data[crest[i]],str(i+1),fontdict = font1)


#주석
plt.text(0,data_min + ((data_max - data_min) * (100/100)),"etalon_value = "+str(etalon),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (96/100)),"peak_nums = "+str(len(crest)),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (92/100)),"etalon_start_point(x1) = "+str(crest[0]),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (88/100)),"etalon_end_point(x2) = "+str(crest[-1]),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (80/100)),"scan_range = "+str(round(end_linelength,3)) + " ~ " + str(round(center_linelength,3)) + " ~ " + str(round(start_linelength,3)), fontdict = font2)

plt.text(0,data_min + ((data_max - data_min) * (72/100)),"Extraction Strength = "+str(peaks),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (68/100)),"Start Point = "+str(high_p),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (64/100)),"End Point = "+str(low_p),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (60/100)),"Selected File Name = "+str(filename),fontdict = font)
