#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 15:37:47 2023

@author: cdi
"""
import numpy as np
import pandas as pd
import csv
import os
import re

class Etalon():
    def __init__(self,filename):
        abs_path = os.path.dirname( os.path.abspath( __file__ ) )
        self.filename = filename
        try :
            self.filepath_relative = os.path.relpath( filename, abs_path ).replace("\\","/")
        except :
            self.filepath_relative = self.filename
        self.high_DPI = False
        self.one_hz = False
        self.point_size = 5
        self.circle_size = 50
        self.data=0
        
        try: 
            try:
                self.df = pd.read_csv(filename, low_memory=False)
            except:
                self.df = pd.read_csv(filename, encoding='cp949', low_memory=False)
                
            if len(self.df.columns) == 1:
                try:
                    self.df = pd.read_csv(filename, delimiter = '\t', low_memory=False)
                except:
                    self.df = pd.read_csv(filename, encoding='cp949', delimiter = '\t', low_memory=False)
                    
            if len(self.df.columns) == 1:
                try:
                    self.df = pd.read_csv(filename, delimiter = ';', low_memory=False)
                except:
                    self.df = pd.read_csv(filename, encoding='cp949', delimiter = ';', low_memory=False)
        except:
            try:
                chunk = pd.read_csv(filename, low_memory=False, chunksize = 20000)
                self.df = pd.concat(chunk)
            except:
                chunk = pd.read_csv(filename, encoding='cp949', low_memory=False, chunksize = 20000)
                self.df = pd.concat(chunk)
            if len(self.df.columns) == 1:
                try:
                    chunk = pd.read_csv(filename, delimiter = '\t', low_memory=False, chunksize = 20000)
                    self.df = pd.concat(chunk)
                except:
                    chunk = pd.read_csv(filename, encoding='cp949', delimiter = '\t', low_memory=False, chunksize = 20000)
                    self.df = pd.concat(chunk)
            if len(self.df.columns) == 1:
                try:
                    chunk = pd.read_csv(filename, delimiter = ';', low_memory=False, chunksize = 20000)
                    self.df = pd.concat(chunk)
                except:
                    chunk = pd.read_csv(filename, encoding='cp949', delimiter = ';', low_memory=False, chunksize = 20000)
                    self.df = pd.concat(chunk)
        
        
        '''old data load codes'''
        '''
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
        '''
        
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
        
    def extract_parameters_try(self):
        filename = self.filepath_relative.split("/")[-1]
        
        # sampling = re.search('[0-9]{1,3}(M|K)',filename)[0]
        # fsr = re.search('[0-9.]{1,5}(GHz|ghz)',filename)[0]
        # hz = re.search('[0-9.]{1,5}(KHz|Hz|kHz|hz|khz)',filename)[0]
        # exsec = re.search('[0-9.]{1,4}(sec|s|Sec)',filename)[0]
        # wvlength = re.search('[0-9.]{3,7}(nm)',filename)[0]
        
        #is that 1Hz file?
        # if hz == "1Hz" | hz == "1hz" :
        #     self.one_hz = True 
        # else :
        #     self.one_hz = False
            
        #FSR 자동 추출
        try:
            fsr = re.search('[0-9.]{1,5}(GHz|ghz)',filename)[0]
            self.FSR = float(re.search('[0-9.]{1,5}',fsr)[0])
        except:
            self.FSR = 0
        # FSR_find = filename.find("GHz")
        # if FSR_find != -1 :
        #     self.FSR = filename[FSR_find-4:FSR_find]
        #     self.FSR = Etalon.make_float(self.FSR)
        # else :
        #     self.FSR = 0

        #Sampling Num 추출
        try:
            sampling = re.search('[0-9]{1,3}(MS|KS|kS|mS|M_|K_)',filename)[0]
            if re.search('[0-9]{1,3}(MS|KS|kS|mS|M_|K_)',filename)[1] in ['MS', 'mS', 'M_']:
                self.sampling = int(re.search('[0-9.]{1,3}',sampling)[0]) * pow(10,6)
            elif re.search('[0-9]{1,3}(MS|KS|kS|mS|M_|K_)',filename)[1] in ['KS', 'kS', 'K_']:
                self.sampling = int(re.search('[0-9.]{1,3}',sampling)[0]) * pow(10,3)
        except:
            self.sampling = 0
        # MS = filename.find("MS")
        # KS = filename.find("KS")
        # if MS != -1 :
        #     self.sampling = filename[MS-3:MS]
        #     self.sampling = Etalon.make_numeric(self.sampling)
        #     self.sampling = int(self.sampling) * pow(10,6)
        # elif KS != -1 :
        #     self.sampling = filename[KS-3:KS]
        #     self.sampling = Etalon.make_numeric(self.sampling)
        #     self.sampling = int(self.sampling) * pow(10,3)
        # else :
        #     self.sampling = 0
        

        #Hz 추출
        try:
            hz = re.search('[0-9.]{1,5}(KHz|Hz|kHz|hz|khz)',filename)[0]
            if re.search('[0-9.]{1,5}(KHz|Hz|kHz|hz|khz)',filename)[1] in ['kHz', 'KHz', 'khz']:
                self.Hz = float(re.search('[0-9.]{1,5}',hz)[0]) * pow(10,3)
            elif re.search('[0-9.]{1,5}(KHz|Hz|kHz|hz|khz)',filename)[1] in ['Hz', 'hz']:
                self.Hz = float(re.search('[0-9.]{1,5}',hz)[0])
        except:
            self.Hz = 0
        # Hz_find = filename[:6]
        # K = False
        # M = False
        # float_or_int = Hz_find.find(".")
        # if Hz_find.find("k") != -1:
        #     K = True
        # elif Hz_find.find("m") != -1:
        #     M = True
        # if Hz_find.find("Hz") != -1 :
        #     if float_or_int != -1 :
        #         self.Hz = Etalon.make_float(Hz_find,back = True)
        #     else :
        #         self.Hz = Etalon.make_numeric(Hz_find, back = True)
            
        #     if K :
        #         self.Hz = self.Hz * 1000
        #     elif M :
        #         self.Hz = self.Hz * 1000000
        # else :
        #     self.Hz = 0
        
        #extraction time 추출
        try:
            exsec = re.search('[0-9.]{1,4}(sec|s|Sec)',filename)[0]
            self.extraction_sec = float(re.search('[0-9.]{1,4}',exsec)[0])
        except Exception as E:
            self.extraction_sec = 0
            print(str(E))
        
        #center wavelength 추출
        try:
            wvlength = re.search('[0-9.]{1,7}(nm|um)',filename)[0]
            if re.search('[0-9.]{1,7}(nm|um)',filename)[1] == 'um':
                self.center_wavelength = float(re.search('[0-9.]{1,7}',wvlength)[0]) * pow(10,3)
            else:
                self.center_wavelength = float(re.search('[0-9.]{1,7}',wvlength)[0])
        except Exception as E:
            self.center_wavelength = 0
            print(str(E))
            
    def extract_lampwave_parameter(self):
        #램프파 기준 샘플링 개수 계산
        self.lamp_sampling = int(self.sampling / self.Hz / self.extraction_sec)
        self.lamp_range = int(self.lamp_sampling * 1.1)
        
        #FSR to wavenumber
        self.FSR_wvnum = (self.FSR * (pow(10,9))) / (2.99792458 * (pow(10,10)))
    
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
            #print(i)

        self.lamp_data = data_reduce
        #self.lamp_data = self.data
    
    def extraction_lamp_wave_ver1(self):
        low_1 = self.data_low_n(1)
        for i in range(0,len(self.data)):
            if low_1 > self.data[i] :
                start = i + self.lamp_sampling
                break

        end = start + self.lamp_range
        
        return self.data[start : end]
        
