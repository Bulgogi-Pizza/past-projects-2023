# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 09:27:41 2023

@author: quite
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RangeSlider
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk
from hampel import hampel
from Etalon_Calc import Etalon
from scipy.signal import savgol_filter
import time
import pyautogui
import os

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox




class EtalonApp(tk.Tk):
    etalon = None
    filename = ''
    filename_short = ''
    exsec = 0
    center = 0
    sampling = 0
    fsr = 0
    hz = 0
    end = 0
    redraw = 0
    
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(PageTwo)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def exit_window(self):
        self.quit()
        self.destroy()

class PageOne(tk.Frame):
    #master는 EtalonApp 클래스를 가리킴
    def __init__(self, master):

        '''기능 추가''' 
        # 기능1 : 파일 1개 선택
        def select_file():
            try:
                EtalonApp.filename = askopenfilename(initialdir="./", filetypes=(("Data files", ".csv .txt"), ('All files', '*.*')))
                EtalonApp.filename_short = EtalonApp.filename.split('/')[-1]
                if EtalonApp.filename:
                    listbox_filename.delete(0, "end")
                    listbox_filename.insert(0, "../" + EtalonApp.filename_short)
            except:
                messagebox.showerror("Error", "오류가 발생했습니다.")
                
        # 기능2 : 파일과 입력받은 값을 가지고 다음 페이지로 넘어감
        def switch_second_frame():
            if len(str(eval(entry_exsec.get()))) == 0 or len(str(eval(entry_exsec.get()))) == 0 or len(EtalonApp.filename) == 0:
                messagebox.showerror("Error", "항목을 모두 입력해 주세요.")
            else :
                try:
                    EtalonApp.exsec = float(eval(entry_exsec.get()))
                    EtalonApp.center = float(eval(entry_center.get()))
                except:
                    messagebox.showerror("Error", "숫자를 입력해 주세요.")
                

        '''1. 프레임 생성'''
        tk.Frame.__init__(self,master)
        # 상단 프레임 (LabelFrame)
        frm1 = tk.LabelFrame(self, text="Data", pady=15, padx=15)   # pad 내부
        frm1.grid(row=1, column=0, pady=10, padx=10, sticky="nswe") # pad 내부
        self.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
        self.rowconfigure(0, weight=1)

        '''2. 요소 생성'''
        # 레이블
        lbl_filename = tk.Label(frm1, text='데이터 파일 선택')
        lbl_exsec = tk.Label(frm1, text='추출 시간 (sec)')
        lbl_center = tk.Label(frm1, text='중심 파장(nm)')
        lbl_pagename = tk.Label(self, text="Etalon Calculator", font=('MalgunGothic',18))

        #리스트박스
        listbox_filename = tk.Listbox(frm1, width=40, height=1, bg='lightgray')
        
        #엔트리
        entry_exsec = tk.Entry(frm1, width=40)
        entry_center = tk.Entry(frm1, width=40)

        #버튼
        btn_filename = tk.Button(frm1, text="...", width=8, command=select_file)
        tk.Button(self, text="Next", width=15,padx = 10, command=lambda: [switch_second_frame(), master.switch_frame(PageTwo)]).grid(row=5,column=0,padx=20, pady=5, sticky="e")



        '''3. 요소 배치'''
        # 상단 프레임
        lbl_pagename.grid(row=0,column=0, pady=5)
        lbl_filename.grid(row=0, column=0, sticky="e")
        lbl_exsec.grid(row=1, column=0, sticky="e", pady= 5)
        lbl_center.grid(row=2, column=0, sticky="e", pady= 5)
        listbox_filename.grid(row=0, column=1, columnspan=2, sticky="we")
        entry_exsec.grid(row=1, column=1, columnspan=2, sticky="we")
        entry_center.grid(row=2, column=1, columnspan=2, sticky="we")

        btn_filename.grid(row=0, column=3, sticky="n")
        # 상단프레임 grid (2,1)은 창 크기에 맞춰 늘어나도록
        frm1.rowconfigure(2, weight=1)      
        frm1.columnconfigure(1, weight=1)
        
        '''4. 초기값 지정'''
        entry_exsec.insert(0, "1")
        
class PageTwo(tk.Frame):
    #master는 EtalonApp 클래스를 가리킴
    def __init__(self, master):
        
        '''기능 추가'''
        # 기능1 : 파일 1개 선택
        def select_file():
            try:
                EtalonApp.filename = askopenfilename(initialdir="./", filetypes=(("Data files", ".csv .txt"), ('All files', '*.*')))
                EtalonApp.filename_short = EtalonApp.filename.split('/')[-1]
                if EtalonApp.filename:
                    listbox_filename.delete(0, "end")
                    listbox_filename.insert(0, "../" + EtalonApp.filename_short)
            except:
                messagebox.showerror("Error", "오류가 발생했습니다.")
                
        # 기능2 : 입력받은 값을 저장
        def switch_third_frame():
            if len(entry_sampling.get()) == 0 or len(entry_fsr.get()) == 0 or len(entry_hz.get()) == 0 | len(entry_exsec.get()) == 0 or len(entry_exsec.get()) == 0 or len(EtalonApp.filename) == 0:
                messagebox.showerror("Error", "항목을 모두 입력해 주세요.")
            else :
                try:
                    EtalonApp.sampling = int(eval(entry_sampling.get()))
                    EtalonApp.fsr = float(eval(entry_fsr.get()))
                    EtalonApp.hz = int(eval(entry_hz.get()))
                    EtalonApp.exsec = float(eval(entry_exsec.get()))
                    EtalonApp.center = float(eval(entry_center.get()))
                    
                    EtalonApp.etalon.sampling =  int(eval(entry_sampling.get()))
                    EtalonApp.etalon.FSR = float(eval(entry_fsr.get()))
                    EtalonApp.etalon.Hz = int(eval(entry_hz.get()))
                    EtalonApp.etalon.extraction_sec = float(eval(entry_exsec.get()))
                    EtalonApp.etalon.center_wavelength = float(eval(entry_center.get()))
                    EtalonApp.etalon.data = np.array(EtalonApp.etalon.df[combobox_data.get()][2:].astype(float))
                    
                    if EtalonApp.hz * EtalonApp.exsec < 10:
                        EtalonApp.etalon.one_hz = True
                        messagebox.showinfo("Info", "데이터 내 램프파 수가 적어 전체 데이터를 표시합니다.")
                    btn_next["state"] = tk.NORMAL
                except Exception as E:
                    messagebox.showerror("Error", "값을 바르게 입력해 주세요.")
                    print(E)
                    
        # 기능3 : 파일 이름으로부터 요소 추출
        def extract_parameters():
            try:
                EtalonApp.etalon = Etalon(EtalonApp.filename)
                EtalonApp.etalon.extract_parameters_try()
                
                entry_sampling.delete(0,"end")
                entry_fsr.delete(0,"end")
                entry_hz.delete(0,"end")
                entry_exsec.delete(0,"end")
                entry_center.delete(0,"end")

                if int(EtalonApp.etalon.sampling) != 0 :
                    entry_sampling.insert(0, str(EtalonApp.etalon.sampling))
                if float(EtalonApp.etalon.FSR) != 0 :
                    entry_fsr.insert(0, str(EtalonApp.etalon.FSR))
                if int(EtalonApp.etalon.Hz) != 0 :
                    entry_hz.insert(0, str(EtalonApp.etalon.Hz))
                if float(EtalonApp.etalon.extraction_sec) != 0 : 
                    entry_exsec.insert(0, str(EtalonApp.etalon.extraction_sec))
                if int(EtalonApp.etalon.center_wavelength) != 0 :
                    entry_center.insert(0, str(EtalonApp.etalon.center_wavelength))
                    
                combobox_data["values"] = list(EtalonApp.etalon.df.columns)
                btn_set["state"] = tk.NORMAL
            except Exception as E:
                messagebox.showerror("Error", "에러가 발생했습니다." + str(E))
                
        '''1. 프레임 생성'''
        tk.Frame.__init__(self,master)
        # 상단 프레임 (LabelFrame)
        frm1 = tk.LabelFrame(self, text="Data", pady=15, padx=15)   # pad 내부
        frm1.grid(row=1, column=0, pady=10, padx=10, sticky="nswe", columnspan=4) # pad 내부
        frm2 = tk.Frame(self, pady=2, padx=15)   # pad 내부
        frm2.grid(row=2, column=0, pady=1, padx=5, sticky="ne", columnspan=4) # pad 내부
        self.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
        self.rowconfigure(0, weight=1)      

        '''2. 요소 생성'''
        # 레이블
        lbl_filename = tk.Label(frm1, text='데이터 파일 선택')
        lbl_exsec = tk.Label(frm1, text='추출 시간 (sec)')
        lbl_center = tk.Label(frm1, text='중심 파장(nm)')
        lbl_sampling = tk.Label(frm1, text='샘플링 수')
        lbl_data = tk.Label(frm1, text='데이터 선택')
        lbl_fsr = tk.Label(frm1, text='FSR (GHz)')
        lbl_hz = tk.Label(frm1, text='주파수 (Hz)')
        lbl_title = tk.Label(self, text="Etalon Calculator", font=('MalgunGothic',18))

        #리스트박스
        listbox_filename = tk.Listbox(frm1, width=40, height=1, bg='lightgray')
        entry_exsec = tk.Listbox(frm1, width=40, height=1, bg='lightgray')
        entry_center = tk.Listbox(frm1, width=40, height=1, bg='lightgray')
        
        #엔트리
        entry_exsec = tk.Entry(frm1, width=40)
        entry_center = tk.Entry(frm1, width=40)
        entry_sampling = tk.Entry(frm1, width=40)
        entry_fsr = tk.Entry(frm1, width=40)
        entry_hz = tk.Entry(frm1, width=40)

        #버튼
        btn_filename = tk.Button(frm1, text="...", width=8, command=select_file)
        btn_filename.grid(row=0, column=3, sticky="n")
        btn_extract = tk.Button(frm2, text="Extract Parameters", width=15,padx = 10, command=lambda: extract_parameters())
        btn_extract.grid(row=1,column=0, pady=1, sticky="e")
        btn_set = tk.Button(frm2, text="Set", width=15,padx = 10, command=lambda: switch_third_frame())
        btn_set.grid(row=1,column=1, pady=1, sticky="e")
        btn_next = tk.Button(frm2, text="Next", width=15,padx = 10, command=lambda: master.switch_frame(PageThree))
        btn_next.grid(row=1,column=2, pady=1, sticky="e")
        btn_set["state"] = tk.DISABLED
        btn_next["state"] = tk.DISABLED
        #콤보박스
        combobox_data=tkinter.ttk.Combobox(frm1, height=15)#, values=list(EtalonApp.etalon.df.columns))
        
        '''4. 요소 배치'''
        # 상단 프레임
        lbl_title.grid(row=0,column=0, pady=5, columnspan=4)
        lbl_filename.grid(row=0, column=0, sticky="n", pady= 5)
        lbl_exsec.grid(row=3, column=0, sticky="n", pady= 5)
        lbl_center.grid(row=4, column=0, sticky="n", pady= 5)
        lbl_data.grid(row=5, column=0, sticky="n", pady=5)
        lbl_sampling.grid(row=6, column=0, sticky="n", pady= 5)
        lbl_fsr.grid(row=7, column=0, sticky="n", pady= 5)
        lbl_hz.grid(row=8, column=0, sticky="n")

        listbox_filename.grid(row=0, column=1, columnspan=2, sticky="we")
        entry_exsec.grid(row=3, column=1, columnspan=2, sticky="we")
        entry_center.grid(row=4, column=1, columnspan=2, sticky="we")
        combobox_data.grid(row=5, column=1, columnspan=2, sticky="we")
        entry_sampling.grid(row=6, column=1, columnspan=2, sticky="we")
        entry_fsr.grid(row=7, column=1, columnspan=2, sticky="we")
        entry_hz.grid(row=8, column=1, rowspan=2, sticky="wens")
        
        combobox_data.set("데이터 선택")


        # 상단프레임 grid (2,1)은 창 크기에 맞춰 늘어나도록
        frm1.rowconfigure(2, weight=1)      
        frm1.columnconfigure(1, weight=1)   
        
        
class PageThree(tk.Frame):
    #master는 EtalonApp 클래스를 가리킴
    def __init__(self, master):
        '''기능 추가'''
        # 기능1 : Re-draw 버튼을 누를 때마다 체크박스에 따라 그래프를 다시 그림
        def redraw_graph():
            EtalonApp.redraw = EtalonApp.etalon.lamp_data
            if var_ma.get() :
                strength = int(eval(entry_mastrength.get()))
                EtalonApp.redraw = np.convolve(EtalonApp.redraw,np.ones(strength)/float(strength), mode = 'valid')
            if var_hp.get() :
                window_size = int(eval(entry_hpwindow.get()))
                n = int(eval(entry_hpn.get()))
                ts = pd.Series(EtalonApp.redraw)
                EtalonApp.redraw = hampel(ts, window_size=window_size, n=n, imputation=True).to_list()
            if var_sg.get() :
                window_length = int(eval(entry_sgwindow.get()))
                polyorder = int(eval(entry_sgpoly.get()))
                EtalonApp.redraw = savgol_filter(EtalonApp.redraw,window_length = window_length, polyorder = polyorder)
            
                
            # to run GUI event loop
            plt.ion()
            
            #다시 그리기
            #figure.set_visible(False)
            #ax.visible(False)
            #ax.plot(range(0,len(redraw)), redraw)
            graph.set_xdata(range(0,len(EtalonApp.redraw)))
            graph.set_ydata(EtalonApp.redraw)
            ax.set_xlim(0,len(EtalonApp.redraw))
            ax.set_ylim(np.min(EtalonApp.redraw), np.max(EtalonApp.redraw))
            
            #drawing updated values
            canvas.draw()
            
            EtalonApp.redraw = np.array(EtalonApp.redraw)
            
        def only_two_char(char):
            if len(char) == 1: return "0"+char
            else : return char

        def screenshot():
            tt = time.localtime()
            year = str(tt[0])[2:]
            month = only_two_char(str(tt[1]))
            day = only_two_char(str(tt[2]))
            hour = only_two_char(str(tt[3]))
            minute = only_two_char(str(tt[4]))
            sec = only_two_char(str(tt[5]))
            date = year+month+day+"_"+hour+minute+sec
            
            x1 = start.winfo_rootx()
            x2 = start.winfo_width()
            y1 = start.winfo_rooty()
            y2 = start.winfo_height()
            
            pyautogui.screenshot(date+"_"+EtalonApp.filename_short+".png" ,region=(x1, y1, x2, y2))            
            messagebox.showinfo("ScreenShot","스크린샷이 " + os.path.dirname( os.path.abspath( __file__ )) + "\\" +date+"_"+EtalonApp.filename_short+".png 에 저장되었습니다.")

        #EtalonApp.etalon.extract_parameters_try()
        EtalonApp.etalon.extract_lampwave_parameter()
        if EtalonApp.etalon.one_hz :
            EtalonApp.etalon.extract_lamp_wave_onehz()
        else :
            EtalonApp.etalon.extract_lamp_wave()
        
        EtalonApp.redraw = EtalonApp.etalon.lamp_data
        EtalonApp.redraw = np.array(EtalonApp.redraw)
        
        if len(EtalonApp.etalon.lamp_data) < 10:
            messagebox.showerror("Error", "램프 파를 추출하지 못했습니다. 전체 데이터를 출력합니다.")
            EtalonApp.redraw = np.array(EtalonApp.etalon.data)
            EtalonApp.etalon.lamp_data = np.array(EtalonApp.etalon.data)
        
        '''1. 프레임 생성'''
        tk.Frame.__init__(self,master)
        frm_top = tk.Frame(self, pady=3, padx=3)
        frm_left = tk.Frame(self, pady=3, padx=3)
        frm_right = tk.Frame(self, pady=3, padx=3)
        frm_bottom = tk.Frame(self, pady=3, padx=3)
        frm1 = tk.LabelFrame(frm_left, text="Data", pady=2, padx=15)   # pad 내부
        frm1_1 = tk.Frame(frm1, pady=3, padx=3)
        frm1_2 = tk.Frame(frm1, pady=3, padx=3)
        frm2 = tk.Frame(frm_right, pady=3, padx = 3)
        frm3 = tk.LabelFrame(frm_left, text="Noise Reduction", pady=2, padx=15)
        frm3_1 = tk.LabelFrame(frm3, text="Moving Average Filter", pady=2, padx=15)
        frm3_2 = tk.LabelFrame(frm3, text="Hampel Filter", pady=2, padx=15)
        frm3_3 = tk.LabelFrame(frm3, text="Savitzky Golay Filter", pady=2, padx=15)
        frm3_1_1 = tk.Frame(frm3_1, pady=2, padx=5)
        frm3_1_2 = tk.Frame(frm3_1, pady=2, padx=5)
        frm3_2_1 = tk.Frame(frm3_2, pady=2, padx=5)
        frm3_2_2 = tk.Frame(frm3_2, pady=2, padx=5)
        frm3_3_1 = tk.Frame(frm3_3, pady=2, padx=5)
        frm3_3_2 = tk.Frame(frm3_3, pady=2, padx=5)
        frm3_3_3 = tk.Frame(frm3_3, pady=2, padx=5)
        
        '''1-1. 프레임 배치'''
        self.pack(side="top", fill="both", expand="yes")
        frm_top.pack(side="top", pady=3, padx=5, fill="x", expand = "no")
        frm_bottom.pack(side="bottom", pady=3, padx=5, fill="x", expand = "no")
        frm_left.pack(side="left", pady=0, padx=0, fill="y", expand = "no") # pad 내부
        frm_right.pack(side="right", pady=0, padx=0, fill="both", expand = "yes") # pad 내부
        frm1.pack(side="top", pady=5, padx=5, fill="x", expand = "no") # pad 내부
        frm1_1.pack(side="left")#, fill="both", expand = "yes")
        frm1_2.pack(side="right")#, fill="both", expand = "yes")
        frm2.pack(side="top", pady=0, padx=0, fill="both", expand = "yes")
        frm3.pack(side="top", pady=5, padx=5, fill="x", expand = "no")
        frm3_1.pack(side="top",anchor="w", fill="x", expand="yes")#, expand = "yes")
        frm3_2.pack(side="top",anchor="w", fill="x", expand="yes")#, expand = "yes")
        frm3_3.pack(side="top",anchor="w", fill="x", expand="yes")#, expand = "yes")
        frm3_1_1.pack(side="left")#, expand = "yes")
        frm3_1_2.pack(side="left")#, expand = "yes")
        frm3_2_1.pack(side="left")#, expand = "yes")
        frm3_2_2.pack(side="left")#, expand = "yes")
        frm3_3_1.pack(side="left")#, expand = "yes")
        frm3_3_2.pack(side="left")#, expand = "yes")
        frm3_3_3.pack(side="left", anchor="s")#, expand = "yes")

        
        '''2. 요소 생성'''
        ###########main
        #버튼
        btn_previous = tk.Button(frm_bottom, text="Previous", width=15,padx = 10, command=lambda: master.switch_frame(PageTwo))
        btn_next = tk.Button(frm_bottom, text="Next", width=15,padx = 10, command=lambda: master.switch_frame(PageFour))
        btn_redraw = tk.Button(frm_bottom, text="Noise Reduction", width=15,padx = 10, command=lambda: redraw_graph())
        btn_screenshot = tk.Button(frm_bottom, text="ScreenShot", width=15,padx = 10, command=lambda: screenshot())
        #레이블
        lbl_title = tk.Label(frm_top, text=EtalonApp.filename_short, font=('MalgunGothic',18))

        ###########frm1
        # 레이블
        #lbl_filename = tk.Label(frm1_1, text='데이터 파일 선택')
        lbl_exsec = tk.Label(frm1_1, text='추출 시간 (sec)')
        lbl_center = tk.Label(frm1_1, text='중심 파장(nm)')
        lbl_sampling = tk.Label(frm1_1, text='샘플링 수')
        lbl_fsr = tk.Label(frm1_1, text='FSR (GHz)')
        lbl_hz = tk.Label(frm1_1, text='주파수 (Hz)')
        #리스트박스
        #listbox_filename = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')
        listbox_exsec = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')
        listbox_center = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')
        listbox_sampling = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')
        listbox_fsr = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')
        listbox_hz = tk.Listbox(frm1_2, width=30, height=1, bg='lightgray')

        ###########frm2
        #그래프 창
        # to run GUI event loop
        plt.ion()
         
        # here we are creating sub plots
        figure = plt.Figure()
        figure.set_dpi(100)
        ax = figure.add_subplot(111)
        #graph.set_lw(0.3)
        canvas = FigureCanvasTkAgg(figure, master=frm2)
        tkagg.NavigationToolbar2Tk(canvas, frm2)
        graph, = ax.plot(range(0,len(EtalonApp.etalon.lamp_data)), EtalonApp.etalon.lamp_data,lw=0.3)
        
        #canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand="yes")
        #extract_ax = plt.axes([0.25, 0.10, 0.65, 0.05], facecolor='white')
        # axes(rect) -> rect : left, bottom, width, height
        

        ###########frm3
        #레이블
        lbl_ma = tk.Label(frm3_1_1, text='Apply')
        lbl_mastrength = tk.Label(frm3_1_1, text='Strength')
        lbl_hp = tk.Label(frm3_2_1, text='Apply')
        lbl_hpwindow = tk.Label(frm3_2_1, text='WindowSize')
        lbl_hpn = tk.Label(frm3_2_1, text='n')
        lbl_sg = tk.Label(frm3_3_1, text='Apply')
        lbl_sgwindow = tk.Label(frm3_3_1, text='WindowSize')
        lbl_sgpoly = tk.Label(frm3_3_1, text='Polynomial')
        lbl_sgwindow_2 = tk.Label(frm3_3_3, text='(홀수)')
        lbl_sgpoly_2 = tk.Label(frm3_3_3, text='(< WindowSize)')
        #체크박스 변수
        var_ma = tkinter.IntVar()
        var_hp = tkinter.IntVar()
        var_sg = tkinter.IntVar()
        #체크박스
        cb_ma = tk.Checkbutton(frm3_1_2, variable=var_ma)
        cb_hp = tk.Checkbutton(frm3_2_2, variable=var_hp)
        cb_sg = tk.Checkbutton(frm3_3_2, variable=var_sg)
        #엔트리
        entry_mastrength = tk.Entry(frm3_1_2, width=10)
        entry_hpwindow = tk.Entry(frm3_2_2, width=10)
        entry_hpn = tk.Entry(frm3_2_2, width=10)
        entry_sgwindow = tk.Entry(frm3_3_2, width=10)
        entry_sgpoly = tk.Entry(frm3_3_2, width=10)

        '''2-1. 요소 배치'''
        ##########main
        #버튼
        btn_next.pack(side="right",anchor="s")
        btn_previous.pack(side="right",anchor="s")
        btn_redraw.pack(side="right",anchor="s")
        btn_screenshot.pack(side="right", anchor="s")
        #레이블
        lbl_title.pack(side="top")
        
        ###########frm1
        #레이블
        lbl_title.pack(side = "top", pady=5)
        #lbl_filename.pack(side = "top", anchor="w", pady=5)
        lbl_exsec.pack(side = "top", anchor="w", pady=5)
        lbl_center.pack(side = "top", anchor="w", pady=5)
        lbl_sampling.pack(side = "top", anchor="w", pady=5)
        lbl_fsr.pack(side = "top", anchor="w", pady=5)
        lbl_hz.pack(side = "top", anchor="w", pady=5)
        #리스트박스
        #listbox_filename.pack(side="top", anchor="e", pady=5)
        listbox_exsec.pack(side="top", anchor="e", pady=5)
        listbox_center.pack(side="top", anchor="e", pady=5)
        listbox_sampling.pack(side="top", anchor="e", pady=5)
        listbox_fsr.pack(side="top", anchor="e", pady=5)
        listbox_hz.pack(side="top", anchor="e", pady=5)
        
        ###########frm3
        #레이블
        lbl_ma.pack(side = "top", anchor="w", pady=5)
        lbl_mastrength.pack(side="top", anchor="w", pady=5)
        lbl_hp.pack(side = "top", anchor="w", pady=5)
        lbl_hpwindow.pack(side="top", anchor="w", pady=5)
        lbl_hpn.pack(side="top", anchor="w", pady=5)
        lbl_sg.pack(side = "top", anchor="w", pady=5)
        lbl_sgwindow.pack(side="top", anchor="w", pady=5)
        lbl_sgpoly.pack(side="top", anchor="w", pady=5)
        lbl_sgpoly_2.pack(side="bottom",anchor="w", pady=5)
        lbl_sgwindow_2.pack(side="bottom",anchor="w", pady=5)
    
        #체크박스
        cb_hp.pack(side="top", anchor="w", pady=5)
        cb_ma.pack(side="top", anchor="w", pady=5)
        cb_sg.pack(side="top", anchor="w", pady=5)
        
        #엔트리
        entry_mastrength.pack(side="top", anchor="w", pady=5)
        entry_hpwindow.pack(side="top", anchor="w", pady=5)
        entry_hpn.pack(side="top", anchor="w", pady=5)
        entry_sgwindow.pack(side="top", anchor="w", pady=5)
        entry_sgpoly.pack(side="top", anchor="w", pady=5)
    
    
        '''3. 값 인풋'''
        #리스트박스 값 인풋
        #listbox_filename.delete(0, "end")
        #listbox_filename.insert(0, str(master.filename_short))
        listbox_exsec.insert(0, str(master.exsec))
        listbox_center.insert(0, str(master.center))
        listbox_sampling.insert(0, str(EtalonApp.etalon.sampling))
        listbox_fsr.insert(0, str(EtalonApp.etalon.FSR))
        listbox_hz.insert(0, str(EtalonApp.etalon.Hz))
        
class PageFour(tk.Frame):
    def __init__(self, master):
        redraw = None
        
        '''기능 추가'''                  
        def window_exit():
            yes_no = messagebox.askyesno("종료","정말 종료하시겠습니까?")
            if yes_no:
                start.destroy()
            
        def only_two_char(char):
            if len(char) == 1: return "0"+char
            else : return char

        def screenshot():
            tt = time.localtime()
            year = str(tt[0])[2:]
            month = only_two_char(str(tt[1]))
            day = only_two_char(str(tt[2]))
            hour = only_two_char(str(tt[3]))
            minute = only_two_char(str(tt[4]))
            sec = only_two_char(str(tt[5]))
            date = year+month+day+"_"+hour+minute+sec
            
            x1 = start.winfo_rootx()
            x2 = start.winfo_width()
            y1 = start.winfo_rooty()
            y2 = start.winfo_height()
            
            pyautogui.screenshot(date+"_"+EtalonApp.filename_short+".png" ,region=(x1, y1, x2, y2))
            messagebox.showinfo("ScreenShot","스크린샷이 " + os.path.dirname( os.path.abspath( __file__ )) + "\\" +date+"_"+EtalonApp.filename_short+".png 에 저장되었습니다.")
         
        '''1. 프레임 생성'''
        tk.Frame.__init__(self,master)
        frm_top = tk.Frame(self, pady=15, padx=15)
        frm_left = tk.Frame(self, pady=15, padx=15)
        frm_right = tk.Frame(self, pady=15, padx=15)
        frm_bottom = tk.Frame(self, pady=15, padx=15)
        frm1 = tk.LabelFrame(frm_left, text="Data", pady=2, padx=15)   # pad 내부
        frm1_1 = tk.Frame(frm1, pady=15, padx=15)
        frm1_2 = tk.Frame(frm1, pady=15, padx=15)
        frm2 = tk.Frame(frm_right, pady=15, padx = 15)
        frm3 = tk.LabelFrame(frm_left, text="Noise Reduction", pady=2, padx=15)
    
        '''1-1. 프레임 배치'''
        self.pack(side="top", fill="both", expand="yes")
        frm_top.pack(side="top", pady=3, padx=5, fill="x", expand = "no")
        frm_bottom.pack(side="bottom", pady=3, padx=5, fill="x", expand = "no")
        frm_left.pack(side="left", pady=0, padx=0, fill="y", expand = "no") # pad 내부
        frm_right.pack(side="right", pady=0, padx=0, fill="both", expand = "yes") # pad 내부
        frm1.pack(side="top", pady=5, padx=5, fill="x", expand = "no") # pad 내부
        frm1_1.pack(side="left")#, fill="both", expand = "yes")
        frm1_2.pack(side="right")#, fill="both", expand = "yes")
        frm2.pack(side="top", pady=0, padx=0, fill="both", expand = "yes")
        frm3.pack(side="top", pady=5, padx=5, fill="x", expand = "no")
    
        '''2. 요소 생성'''
        ###########main
        #버튼
        btn_previous = tk.Button(frm_bottom, text="Previous", width=15,padx = 10, command=lambda: master.switch_frame(PageThree))
        btn_next = tk.Button(frm_bottom, text="Done", width=15,padx = 10, command=lambda: window_exit())
        btn_screenshot = tk.Button(frm_bottom, text="ScreenShot", width=15,padx = 10, command=lambda: screenshot())
        #btn_redraw = tk.Button(frm_bottom, text="Redraw", command=lambda: redraw_graph(figure, ax))
        #레이블
        lbl_title = tk.Label(frm_top, text=EtalonApp.filename_short, font=('MalgunGothic',18))
           
        ###########frm1
        # 레이블
        #lbl_filename = tk.Label(frm1_1, text='데이터 파일 선택')
        lbl_exsec = tk.Label(frm1_1, text='추출 시간 (sec)')
        lbl_center = tk.Label(frm1_1, text='중심 파장(nm)')
        lbl_sampling = tk.Label(frm1_1, text='샘플링 수')
        lbl_fsr = tk.Label(frm1_1, text='FSR (GHz)')
        lbl_hz = tk.Label(frm1_1, text='주파수 (Hz)')
        #리스트박스
        #listbox_filename = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
        listbox_exsec = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
        listbox_center = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
        listbox_sampling = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
        listbox_fsr = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
        listbox_hz = tk.Listbox(frm1_2, width=20, height=1, bg='lightgray')
           
        '''그래프 그리기'''
        #matplotlib.use('TkAgg')
        ###########frm2
        #그래프 창
        # to run GUI event loop
        #plt.ion()
         
        # here we are creating sub plots
        figure = plt.Figure()
        figure.set_dpi(100)
        canvas = FigureCanvasTkAgg(figure, frm2)
        tkagg.NavigationToolbar2Tk(canvas, frm2)
        canvas.get_tk_widget().pack(side="top", fill="both", expand="yes")
        ax = figure.add_subplot(111)
        figure.subplots_adjust(left=0.13,bottom=0.2,right=0.83,top=0.95)
        
        #figure, ax = plt.subplots()
        #figure.set_dpi(100)
        
        
        #canvas.draw()
        
    
        '''폰트 설정'''
        circle_size = {"peak" : 5}
        font_size = {"peak" : 10, "etalon" : 10}
        line_width = {"signal" : 0.2}
    
        font_peak = {'size' : font_size["peak"]}
        font_etalon = {'size' : font_size["etalon"]}
    
        '''초기 그래프, 시작선, 끝선 그리기'''
        h0 = ax.scatter(0,EtalonApp.redraw[0],s=circle_size["peak"], c='r')
        h1 = ax.plot(range(0,len(EtalonApp.redraw)), EtalonApp.redraw, lw = line_width["signal"], color = 'b')
        h2 = ax.axvline(int(len(EtalonApp.redraw)*0.1),color = 'red', linestyle = ':')
        h3 = ax.axvline(int(len(EtalonApp.redraw)*0.9),color = 'red', linestyle = ':')
        ax.autoscale(enable=True, axis='both', tight=True)
    
           
        #박스 내부 컬러   
        #axcolor = 'lightgoldenrodyellow'
    
        ''' 추출 강도 슬라이더 추가 '''
        extract_ax = figure.add_axes([0.13, 0.07, 0.70, 0.05])#, facecolor=axcolor)
        # axes(rect) -> rect : left, bottom, width, height
        self.extract_slider = Slider(extract_ax, 'Strength', 0, EtalonApp.etalon.lamp_sampling // 8, valstep = 1, valinit = EtalonApp.etalon.lamp_sampling // 24)
    
        ''' 에탈론 범위 슬라이더 추가 '''
        axrange = figure.add_axes([0.13, 0.11, 0.70, 0.05])#, facecolor=axcolor)
        # axes(rect) -> rect : left, bottom, width, height
        self.s_range = RangeSlider(axrange, 'Range', 0, len(EtalonApp.redraw), valstep = 1, valinit = [int(len(EtalonApp.etalon.lamp_data)*0.1), int(len(EtalonApp.etalon.lamp_data)*0.9)])
    
        ''' Redraw 버튼 추가 '''
        redrawax = figure.add_axes([0.7, 0.025, 0.1, 0.04])
        # axes(rect) -> rect : left, bottom, width, height
        self.redraw_button = Button(redrawax, 'Redraw', color='lightblue', hovercolor='white')
    
        ''' Add Calc Button '''
        calcax = figure.add_axes([0.85, 0.025, 0.1, 0.04])
        # axes(rect) -> rect : left, bottom, width, height
        self.calc_button = Button(calcax, 'Calc', color='lightblue', hovercolor='white')
    
        def update(val):
            start_x = val[0]
            end_x = val[1]
            h2.set_xdata(start_x)
            h3.set_xdata(end_x)
            figure.canvas.draw_idle()
        self.s_range.on_changed(update)
        
        def redraw(event):
            crest_or_valley = 0
            extract_strength = self.extract_slider.val
            calc_width = (EtalonApp.etalon.lamp_sampling//extract_strength)//2
            
            crest = []
            valley = []
            
            for i in range(0, len(EtalonApp.redraw) - calc_width - 1) :
                data_strip = EtalonApp.redraw[i:i+calc_width]
                
                if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
                    crest.append(i+calc_width//2-1)
                    crest_or_valley = 1
                if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
                    valley.append(i+calc_width//2-1)
                    crest_or_valley = 0
                    
            start_x = self.s_range.val[0]
            end_x = self.s_range.val[1]
            new_crest = [val for val in crest if start_x<val<end_x]
            
            for txt in ax.texts:
                txt.set_visible(False)
            
            for i in range(0, len(new_crest)):
                ax.text(new_crest[i],EtalonApp.redraw[new_crest[i]],str(i+1),fontdict = font_peak)
            
            #print(start_x,"tt" ,end_x)
            h0.set_offsets(np.c_[new_crest, EtalonApp.redraw[new_crest]])
            figure.canvas.draw_idle()
        self.redraw_button.on_clicked(redraw)
        
        def calc(event):

            crest_or_valley = 0
            extract_strength = self.extract_slider.val
            calc_width = (EtalonApp.etalon.lamp_sampling//extract_strength)//2
            
            crest = []
            valley = []
            
            for i in range(0, len(EtalonApp.redraw) - calc_width - 1) :
                data_strip = EtalonApp.redraw[i:i+calc_width]
                
                if(np.max(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 0:
                    crest.append(i+calc_width//2-1)
                    crest_or_valley = 1
                if(np.min(data_strip) == data_strip[calc_width//2-1]) and crest_or_valley == 1:
                    valley.append(i+calc_width//2-1)
                    crest_or_valley = 0
            
            start_x = self.s_range.val[0]
            end_x = self.s_range.val[1]
            new_crest = [val for val in crest if start_x<val<end_x]
            peak_nums = len(new_crest)
            
            etalon_val = EtalonApp.etalon.FSR_wvnum * (len(new_crest) - 1) / (new_crest[-1] - new_crest[0])
            
            center_wavenumber = 10000000 / EtalonApp.center
            if EtalonApp.etalon.one_hz:
                start_wavenumber = center_wavenumber - (etalon_val * (new_crest[peak_nums//2] - new_crest[0]) * 5000)
                end_wavenumber = center_wavenumber + (etalon_val * (new_crest[-1] - new_crest[peak_nums//2]) * 5000)
            start_wavenumber = center_wavenumber - (etalon_val * (new_crest[peak_nums//2] - new_crest[0]))
            end_wavenumber = center_wavenumber + (etalon_val * (new_crest[-1] - new_crest[peak_nums//2]))
            start_wavelength = 10000000 / start_wavenumber
            end_wavelength = 10000000 / end_wavenumber
            
            listbox_wvlenrange.insert(0, str(round(start_wavelength,2)) + " - " + str(round(EtalonApp.center,2)) + " - " + str(round(end_wavelength,2)))
            listbox_etalon.insert(0, str(etalon_val))
            listbox_equation.insert(0, "{("+str(len(new_crest))+"-1) * [("+str(EtalonApp.fsr)+"*10^9)/(2.99792458*10^10)]} / ("+str(new_crest[-1])+"-"+str(new_crest[0])+")")
            listbox_axisx.insert(0, str(new_crest[0])+" - "+str(new_crest[-1]))
            # stem_start.set_array(np.c_[new_crest[0],EtalonApp.etalon.lamp_data[new_crest[0]]])
            # stem_middle.set_array(np.c_[new_crest[len(new_crest)//2],EtalonApp.etalon.lamp_data[new_crest[len(new_crest)//2]]])
            # stem_end.set_array(np.c_[new_crest[-1],etalon.lamp_data[new_crest[-1]]])

            # text_start.set_position([new_crest[0],0])
            # text_start.set_text(str(round(start_wavelength,3)) + "nm")
            # text_middle.set_position([new_crest[len(new_crest)//2],0])
            # text_middle.set_text(str(round(center_wavelength,3)) + "nm")
            # text_end.set_position([new_crest[-1],0])
            # text_end.set_text(str(round(end_wavelength,3)) + "nm")

            figure.canvas.draw_idle()
        self.calc_button.on_clicked(calc)
           
           
        ###########frm3
        #레이블
        lbl_wvlen = tk.Label(frm3, text='스캔 범위 (Wavelength)')
        lbl_etalon = tk.Label(frm3, text='Etalon Value')
        lbl_equation = tk.Label(frm3, text='Etalon Eqaution')
        lbl_axisx = tk.Label(frm3, text='x 범위 (x1 - x2)')
        #리스트박스
        listbox_wvlenrange = tk.Listbox(frm3, width=45, height=1, bg='lightgray')
        listbox_etalon = tk.Listbox(frm3, width=45, height=1, bg='lightgray')
        listbox_equation = tk.Listbox(frm3, width=45, height=1, bg='lightgray')
        listbox_axisx = tk.Listbox(frm3, width=45, height=1, bg='lightgray')
           
        '''2-1. 요소 배치'''
        ##########main
        #버튼
        btn_next.pack(side="right",anchor="s")
        btn_previous.pack(side="right",anchor="s")
        btn_screenshot.pack(side="right", anchor="s")
        #btn_redraw.pack(side="right",anchor="s")
        #레이블
        lbl_title.pack(side="top")
    
        ###########frm1
        #레이블
        lbl_title.pack(side = "top", pady=5)
        #lbl_filename.pack(side = "top", anchor="w", pady=5)
        lbl_exsec.pack(side = "top", anchor="w", pady=5)
        lbl_center.pack(side = "top", anchor="w", pady=5)
        lbl_sampling.pack(side = "top", anchor="w", pady=5)
        lbl_fsr.pack(side = "top", anchor="w", pady=5)
        lbl_hz.pack(side = "top", anchor="w", pady=5)
        #리스트박스
        #listbox_filename.pack(side="top", anchor="e", pady=5)
        listbox_exsec.pack(side="top", anchor="e", pady=5)
        listbox_center.pack(side="top", anchor="e", pady=5)
        listbox_sampling.pack(side="top", anchor="e", pady=5)
        listbox_fsr.pack(side="top", anchor="e", pady=5)
        listbox_hz.pack(side="top", anchor="e", pady=5)
    
        ###########frm3
        #레이블, 리스트박스
        lbl_wvlen.pack(side="top", anchor="w", pady=5)
        listbox_wvlenrange.pack(side="top", anchor="w", pady=5)
        lbl_etalon.pack(side="top", anchor="w", pady=5)
        listbox_etalon.pack(side="top", anchor="w", pady=5)
        lbl_equation.pack(side="top", anchor="w", pady=5)
        listbox_equation.pack(side="top", anchor="w", pady=5)
        lbl_axisx.pack(side="top", anchor="w", pady=5)
        listbox_axisx.pack(side="top", anchor="w", pady=5)
           
           
        '''3. 값 인풋'''
        #리스트박스 값 인풋
        #listbox_filename.delete(0, "end")
        #listbox_filename.insert(0, str(EtalonApp.filename_short))
        listbox_exsec.insert(0, str(EtalonApp.exsec))
        listbox_center.insert(0, str(EtalonApp.center))
        listbox_sampling.insert(0, str(EtalonApp.etalon.sampling))
        listbox_fsr.insert(0, str(EtalonApp.etalon.FSR))
        listbox_hz.insert(0, str(EtalonApp.etalon.Hz))
        # listbox_wvlenrange(0, str(wvlen_start) + " - " + str(wvlen_middle) + " - ", str(wvlen_end))
        # listbox_etalon(0, str(etalon_value))


start = EtalonApp()

start.mainloop()







