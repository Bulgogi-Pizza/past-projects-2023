#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:37:47 2023

@author: cdi
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, RangeSlider, TextBox
import tkinter
from tkinter import filedialog
import scipy
import csv
import os
import sys
from hampel import hampel

class Etalon():
    def __init__(self,filename,extraction_sec,center_wavelength):
        abs_path = os.path.dirname( os.path.abspath( __file__ ) )
        self.filename = filename
        self.filepath_relative = os.path.relpath( filename, abs_path ).replace("\\","/")
        self.high_DPI = False
        self.one_hz = False
        self.point_size = 5
        self.circle_size = 50
        self.extraction_sec = extraction_sec
        self.center_wavelength = center_wavelength
        
        #self.data load
        line_num = 0
        arr = []
        separate_tap = False
        if self.filename[-3:] == 'txt':
            f = open(self.filename,'r',encoding='cp949')
            rdr = csv.reader(f)
            for line in rdr:
                if line_num > 2 and '\t' in line[0]:
                    line = line[0].split('\t')
                    line = [float(line[0]), float(line[1])]
                    arr.append(line)
                    separate_tap = True
                line_num = line_num + 1
            if separate_tap :
                self.data = np.array(arr)
                print("yes")
            f.close()
        if not separate_tap :
            self.data = pd.read_csv(self.filename, encoding='cp949')
            self.data = np.array(self.data)
            print("not")
            
        self.time = self.data[:,0]
        self.data = self.data[:,1]
        
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

    def moving_average(self,x,y,strength = 3):
        y_conv = np.convolve(y,np.ones(strength)/float(strength), mode = 'valid')
        x_dat = np.linspace(np.min(x), np.max(x), np.size(y_conv))
        
        return x_dat, y_conv
    
    def hampel(self, window_size = 15, n = 2, show_graph = False):
        # Just outlier detection
        ts = pd.Series(self.data)
        outlier_indices = hampel(ts, window_size=window_size, n=n)
        #print("Outlier Indices: ", outlier_indices)

        # Outlier Imputation with rolling median
        ts_imputation = hampel(ts, window_size=window_size, n=n, imputation=True)
       
        if show_graph :
            plt.rcParams["figure.dpi"] = 2000
            plt.subplot(211)
            plt.plot(data,linewidth=0.2)
            plt.subplot(212)
            ts.plot(style="k-",linewidth = 0.2)
            ts_imputation.plot(style="g-",linewidth = 0.2)
            plt.show()
            
        return np.array(ts_imputation)
    
    def savgol():
        pass
        
    def extract_parameters_try(self):
        filename = self.filepath_relative.split("/")[-1]
        
        #is that 1Hz file?
        if filename[:3] == "1Hz" :
            self.one_hz = True 
        else :
            self.one_hz = False
            
        #FSR 자동 추출
        FSR_find = filename.find("GHz")
        if FSR_find != -1 :
            self.FSR = filename[FSR_find-4:FSR_find]
            self.FSR = Etalon.make_float(self.FSR)
        else :
            self.FSR = 0

        #Sampling Num 추출
        MS = filename.find("MS")
        KS = filename.find("KS")
        if MS != -1 :
            self.sampling = filename[MS-3:MS]
            self.sampling = Etalon.make_numeric(self.sampling)
            self.sampling = int(self.sampling) * pow(10,6)
        elif KS != -1 :
            self.sampling = filename[KS-3:KS]
            self.sampling = Etalon.make_numeric(self.sampling)
            self.sampling = int(self.sampling) * pow(10,3)
        else :
            self.sampling = 0

        #Hz 추출
        Hz_find = filename[:6]
        K = False
        M = False
        float_or_int = Hz_find.find(".")
        if Hz_find.find("k") != -1:
            K = True
        elif Hz_find.find("m") != -1:
            M = True
        if Hz_find.find("Hz") != -1 :
            if float_or_int != -1 :
                self.Hz = Etalon.make_float(Hz_find,back = True)
            else :
                self.Hz = Etalon.make_numeric(Hz_find, back = True)
            
            if K :
                self.Hz = self.Hz * 1000
            elif M :
                self.Hz = self.Hz * 1000000
        else :
            self.Hz = 0
            
    def extract_lampwave_parameter(self):
        #램프파 기준 샘플링 개수 계산
        self.lamp_sampling = int(self.sampling / self.Hz / self.extraction_sec)
        self.lamp_range = int(self.lamp_sampling * 1.1)
        
        #FSR to wavenumber
        self.FSR_wvnum = (self.FSR * (pow(10,9))) / (2.9979 * (pow(10,10)))
    
    def extract_parameters(self):
        if self.filename [:5] == "data/" :
            self.filename = self.filename[5:]
        #is that 1Hz file?
        if self.filename[:3] == "1Hz" :
            self.one_hz = True 
        else :
            self.one_hz = False
            
        #FSR 자동 추출
        FSR_find = self.filename.find("GHz")
        if FSR_find != -1 :
            self.FSR = self.filename[FSR_find-4:FSR_find]
            self.FSR = Etalon.make_float(self.FSR)
        else :
            print(self.filename)
            self.FSR = float(input("FSR이 자동 추출되지 않았습니다. 수동으로 입력하시기 바랍니다.\nFSR(GHz) - "))

        #Sampling Num 추출
        MS = self.filename.find("MS")
        KS = self.filename.find("KS")
        if MS != -1 :
            self.sampling = self.filename[MS-3:MS]
            self.sampling = Etalon.make_numeric(self.sampling)
            self.sampling = int(self.sampling) * pow(10,6)
        elif KS != -1 :
            self.sampling = self.filename[KS-3:KS]
            self.sampling = Etalon.make_numeric(self.sampling)
            self.sampling = int(self.sampling) * pow(10,3)
        else :
            print(self.filename)
            self.sampling = int(input("샘플링 횟수를 인식할 수 없습니다. \n수동 입력 바랍니다. \nsamplings - "))

        #Hz 추출
        Hz_find = self.filename[:6]
        K = False
        M = False
        float_or_int = Hz_find.find(".")
        if Hz_find.find("k") != -1:
            K = True
        elif Hz_find.find("m") != -1:
            M = True
        if Hz_find.find("Hz") != -1 :
            if float_or_int != -1 :
                self.Hz = Etalon.make_float(Hz_find,back = True)
            else :
                self.Hz = Etalon.make_numeric(Hz_find, back = True)
            
            if K :
                self.Hz = self.Hz * 1000
            elif M :
                self.Hz = self.Hz * 1000000
        else :
            print(self.filename)
            self.Hz = float(input("Hz를 인식할 수 없습니다. \n수동 입력 바랍니다.\nHz - "))
    
    def optimize_plot(self, high_DPI = None, point_size = None, circle_size = None):
        if high_DPI != None:
            self.high_DPI = high_DPI
        if point_size != None:
            self.point_size = point_size
        if circle_size != None:
            self.circle_size = circle_size
    
    def data_low_n(self, n, data = None):
        #find and set max, min points
        if data == None:
            data_max = np.max(self.data)
            data_min = np.min(self.data)
        elif data != None:
            data_max = np.max(data)
            data_min = np.min(data)
            
        return data_min + ((data_max - data_min) * n / 100)         
    
    def extract_lamp_wave(self):
        low_1 = self.data_low_n(1)
        for i in range(0,len(self.data)):
            if low_1 > self.data[i] :
                start = i + self.lamp_sampling
                break

        end = start + self.lamp_range
        
        self.lamp_data = self.data[start : end]
    
    def extract_lamp_wave_onehz(self):
        data_reduce = np.array([])
        reduce = int(len(self.data)/5000)
        for i in range(0, len(self.data)-reduce, reduce):
            data_reduce = np.append(data_reduce, np.array([np.average(self.data[i:i+reduce])]))
            print(i)

        self.lamp_data = data_reduce
    
    def extraction_lamp_wave_ver1(self):
        low_1 = self.data_low_n(1)
        for i in range(0,len(self.data)):
            if low_1 > self.data[i] :
                start = i + self.lamp_sampling
                break

        end = start + self.lamp_range
        
        return self.data[start : end]
        
    def extraction_lamp_wave_ver2(self):
        #데이터 추출
        std = 0
        start_graph = 0
        end_graph = 0
        next_p = 0
        if not self.one_hz :
            for i in range(0,len(data)):    
                if self.data_low_n(20) >= data[i] >= self.data_low_n(15) and next_p == 0 :
                    std = std + 1
                    next_p = 1
                if (data[i] <= self.data_low_n(1) or data[i] >= self.data_low_n(90)) and next_p == 1 :
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
            
        return self.data[start_graph : end_graph]
        
            
    def etalon_calc_init_val(self, extraction_strength, high_p, low_p, smooth_MA = {"do" : False,"strength" : 3}, smooth_HP = {"do" : False, "window_size" : 15, "n" : 1} , smooth_SG = {"do" : False}):
        self.extract_parameters()
        
        if (self.lamp_sampling//extraction_strength)//2 < 4:
            print("추출 강도가 너무 강합니다.")
            sys.exit()
        
        print("#### -Parameters- ####")
        print("Extraction Strength : ",str(extraction_strength))
        print("Start point : ",str(high_p))
        print("End point : ",str(low_p))
        print("-----------------------------------")
        print("Selected file name : ",self.filename)
        print("FSR(GHz) : ",str(self.FSR))
        print("sampling nums : ",str(self.sampling))
        print("Hz : ",str(self.Hz))   
        #make graph more smooth
        if smooth_MA["do"] :
            time_moved , data_moved = self.moving_average(self.time,self.data, smooth_MA["strength"])
            #plt.plot(range(1,len(data_moved)+1),data_moved,linewidth = 0.3)
    
            self.time = time_moved
            data = data_moved
            
        if smooth_HP["do"] :
            data = self.hampel(window_size = smooth_HP["window_size"], n = smooth_HP["n"])     
        #extract lamp_data
        self.lamp_data = self.extraction_lamp_wave_ver1()

        #pick crests and vallies
        calc_width = (self.lamp_sampling//extraction_strength)//2
        i = 0
        crest_or_valley = 0
        self.crest = []
        valley = []
        
        for i in range(0, len(self.lamp_data) - calc_width - 1) :
            data_strip = self.lamp_data[i:i+calc_width]
            
            if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
                self.crest.append(i+calc_width//2-1)
                crest_or_valley = 1
            if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
                valley.append(i+calc_width//2-1)
                crest_or_valley = 0   
                
    def etalon_calc(self, smooth_MA = {"do" : False,"strength" : 3}, smooth_HP = {"do" : False, "window_size" : 15, "n" : 1} , smooth_SG = {"do" : False}):
        self.extract_parameters_try()
        print("Selected file name : ",self.filename)
        print("FSR(GHz) : ",str(self.FSR))
        print("sampling nums : ",str(self.sampling))
        print("Hz : ",str(self.Hz))   
        
        

##############################################################################
##### initial setting ########################################################
##############################################################################
# debugging_mode = False
# make_smooth = True
# High_DPI = False
# one_hz = False
# point_size = 5
# circle_size = 0.5
# extraction_sec = 1
# peaks = 20
# high_p = 85
# low_p = 10
# sampling = 1center_wavelength = 2325

#tk = tkinter.Tk()

#list_file = []                                          #파일 목록 담을 리스트 생성
#filename = filedialog.askopenfilename(initialdir="/",title = "파일을 선택 해 주세요",filetypes = (("*.csv","*csv"),("*.xlsx","*xlsx"),("*.xls","*xls"),("*.txt","*txt")))

# axes(rect) -> rect : left, bottom, width, height

'''
extract_sec_tbax = plt.axes([0.1, 0.90, 0.15, 0.05])
center_wavelength_tbax = plt.axes([0.1, 0.80, 0.15, 0.05])

extract_sec_tb = TextBox(extract_sec_tbax,'extract sec', hovercolor = '0.975', label_pad = 0.1)
center_wavelength_tb = TextBox(extract_sec_tbax,'center wavelength', hovercolor = '0.975', label_pad = 0.1)


#File Select
datas = os.listdir('data')
datas.sort()
filename = datas[14]
data = "data/" + filename


etalon = Etalon(data, 1, 2500)
etalon.etalon_calc(10,0,0)


#draw plot
circle_size = {"peak" : 5}
font_size = {"peak" : 10, "etalon" : 10}
line_width = {"signal" : 0.2}

plt.ion()
fig, ax = plt.subplots()
ax2 = plt.subplot()
plt.subplots_adjust(left=0.25, bottom=0.25)


font_peak = {'size' : font_size["peak"]}
font_etalon = {'size' : font_size["etalon"]}
h0 = ax.scatter(etalon.crest,etalon.lamp_data[etalon.crest],s=circle_size["peak"], c='r')

for i in range(0, len(etalon.crest)):
    ax.text(etalon.crest[i],etalon.lamp_data[etalon.crest[i]],str(i+1),fontdict = font_peak)

h1, = ax.plot(range(0,len(etalon.lamp_data)), etalon.lamp_data, lw = line_width["signal"], color = 'b')
ax.autoscale(enable=True, axis='both', tight=True)
h2 = ax.axvline(int(len(etalon.lamp_data)*0.1),color = 'red', linestyle = ':')
h3 = ax.axvline(int(len(etalon.lamp_data)*0.9),color = 'red', linestyle = ':')

#stem_start = ax.stem(0,0,'r:')[1]
#stem_middle = ax.stem(0,0,'r:')[1]
#stem_end = ax.stem(0,0,'r:')[1]

#text_start = ax.text(0,0,'',fontdict = font_etalon)
#text_middle = ax.text(0,0,'',fontdict = font_etalon)
#text_end = ax.text(0,0,'', fontdict = font_etalon)
      
axcolor = 'lightgoldenrodyellow'

'' Add Extract Strength Slider ''
extract_ax = plt.axes([0.25, 0.10, 0.65, 0.05], facecolor=axcolor)
# axes(rect) -> rect : left, bottom, width, height
extract_slider = Slider(extract_ax, 'Extract Strength', 0, etalon.lamp_sampling // 8, valstep = 1, valinit = etalon.lamp_sampling // 24)

'' Add Etalon Range Slider ''
axrange = plt.axes([0.25, 0.15, 0.65, 0.05], facecolor=axcolor)
# axes(rect) -> rect : left, bottom, width, height
s_range = RangeSlider(axrange, 'Etalon Range', 0, len(etalon.lamp_data), valstep = 1, valinit = [int(len(etalon.lamp_data)*0.1), int(len(etalon.lamp_data)*0.9)])

def update(val):
    start_x = val[0]
    end_x = val[1]
    h2.set_xdata(start_x)
    h3.set_xdata(end_x)
    fig.canvas.draw_idle()
s_range.on_changed(update)

'' Add RadioButtons ''
rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
# axes(rect) -> rect : left, bottom, width, height
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)

def colorfunc(label):
    h1.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)             

'' Add Redraw Button ''
redrawax = plt.axes([0.8, 0.025, 0.1, 0.04])
# axes(rect) -> rect : left, bottom, width, height
redraw_button = Button(redrawax, 'Re-draw', color=axcolor, hovercolor='white')

def redraw(event):
    crest_or_valley = 0
    extract_strength = extract_slider.val
    calc_width = (etalon.lamp_sampling//extract_strength)//2
    
    crest = []
    valley = []
    
    for i in range(0, len(etalon.lamp_data) - calc_width - 1) :
        data_strip = etalon.lamp_data[i:i+calc_width]
        
        if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
            crest.append(i+calc_width//2-1)
            crest_or_valley = 1
        if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
            valley.append(i+calc_width//2-1)
            crest_or_valley = 0
            
    start_x = s_range.val[0]
    end_x = s_range.val[1]
    new_crest = [val for val in crest if start_x<val<end_x]
    
    for txt in ax.texts:
        txt.set_visible(False)
    
    for i in range(0, len(new_crest)):
        ax.text(new_crest[i],etalon.lamp_data[new_crest[i]],str(i+1),fontdict = font_peak)
    
    print(start_x,"tt" ,end_x)
    h0.set_offsets(np.c_[new_crest, etalon.lamp_data[new_crest]])
    fig.canvas.draw_idle()
redraw_button.on_clicked(redraw)

'' Add Calc Button ''
calcax = plt.axes([0.6, 0.025, 0.1, 0.04])
# axes(rect) -> rect : left, bottom, width, height
calc_button = Button(calcax, 'Calc', color=axcolor, hovercolor='white')

def calc(event):

    crest_or_valley = 0
    extract_strength = extract_slider.val
    calc_width = (etalon.lamp_sampling//extract_strength)//2
    
    crest = []
    valley = []
    
    for i in range(0, len(etalon.lamp_data) - calc_width - 1) :
        data_strip = etalon.lamp_data[i:i+calc_width]
        
        if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
            crest.append(i+calc_width//2-1)
            crest_or_valley = 1
        if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
            valley.append(i+calc_width//2-1)
            crest_or_valley = 0
    
    start_x = s_range.val[0]
    end_x = s_range.val[1]
    new_crest = [val for val in crest if start_x<val<end_x]
    peak_nums = len(new_crest)
    
    etalon_val = etalon.FSR_wvnum * (len(new_crest) - 1) / (new_crest[-1] - new_crest[0])
    
    center_wavenumber = 10000000 / center_wavelength
    start_wavenumber = center_wavenumber - (etalon_val * (new_crest[peak_nums//2] - new_crest[0]))
    end_wavenumber = center_wavenumber + (etalon_val * (new_crest[-1] - new_crest[peak_nums//2]))
    start_wavelength = 10000000 / start_wavenumber
    end_wavelength = 10000000 / end_wavenumber
    
    stem_start.set_array(np.c_[new_crest[0],etalon.lamp_data[new_crest[0]]])
    stem_middle.set_array(np.c_[new_crest[len(new_crest)//2],etalon.lamp_data[new_crest[len(new_crest)//2]]])
    stem_end.set_array(np.c_[new_crest[-1],etalon.lamp_data[new_crest[-1]]])

    text_start.set_position([new_crest[0],0])
    text_start.set_text(str(round(start_wavelength,3)) + "nm")
    text_middle.set_position([new_crest[len(new_crest)//2],0])
    text_middle.set_text(str(round(center_wavelength,3)) + "nm")
    text_end.set_position([new_crest[-1],0])
    text_end.set_text(str(round(end_wavelength,3)) + "nm")

    fig.canvas.draw_idle()
calc_button.on_clicked(calc)

plt.show()
plt.draw()
'''






"""
#for debugging
if debugging_mode :
    plt.subplot(3,1,1)
    plt.plot(range(1,lamp_range+1),data[0:lamp_range],linewidth = 0.3)
# print(len(data))
# print(data_max)
# print(data_min)



if debugging_mode :
    plt.subplot(3,1,2)
    plt.plot(range(sss+1,lamp_range+1+sss),data[sss:lamp_range+sss],linewidth = 0.3)


    

    




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
crest_or_valley = 0
crest = []
valley = []
while(i != end_p-calc_width):
    data_strip = data[i:i+calc_width]
    
    if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
        crest.append(i+calc_width//2-1)
        crest_or_valley = 1
    if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
        valley.append(i+calc_width//2-1)
        crest_or_valley = 0
    
    i = i + 1
    
#calculate etalon value
try : etalon = var1 * (len(crest) - 1) / (crest[-1] - crest[0])
except IndexError :
    print("추출 강도가 낮아 에탈론이 추출되지 않았습니다. 추출 강도를 높이길 추천합니다.")
    sys.exit()

#set font
font = {'size' : 5}
font1 = {'size' : point_size}
font2 = {'size' : 8}

#calc scan range
peak_nums = len(crest)
center_wavenumber = 10000000 / center_wavelength
start_wavenumber = center_wavenumber - (etalon * (crest[peak_nums//2] - crest[0]))
end_wavenumber = center_wavenumber + (etalon * (crest[-1] - crest[peak_nums//2]))
start_wavelength = 10000000 / start_wavenumber
end_wavelength = 10000000 / end_wavenumber

plt.stem(crest[0],data[crest[0]],'r:')
plt.stem(crest[len(crest)//2],data[crest[len(crest)//2]],'r:')
plt.stem(crest[-1],data[crest[-1]],'r:')

plt.text(crest[0],0,str(round(start_wavelength,3)) + "nm",fontdict = font)
plt.text(crest[len(crest)//2],0,str(round(center_wavelength,3)) + "nm",fontdict = font)
plt.text(crest[-1],0,str(round(end_wavelength,3)) + "nm", fontdict = font)

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
plt.text(0,data_min + ((data_max - data_min) * (80/100)),"scan_range = "+str(round(end_wavelength,3)) + " ~ " + str(round(center_wavelength,3)) + " ~ " + str(round(start_wavelength,3)), fontdict = font2)

plt.text(0,data_min + ((data_max - data_min) * (72/100)),"Extraction Strength = "+str(peaks),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (68/100)),"Start Point = "+str(high_p),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (64/100)),"End Point = "+str(low_p),fontdict = font)
plt.text(0,data_min + ((data_max - data_min) * (60/100)),"Selected File Name = "+str(filename),fontdict = font)
"""