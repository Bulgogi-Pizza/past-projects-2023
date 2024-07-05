# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 09:27:41 2023

@author: quite
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


import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
from tkinter import messagebox

root = tk.Tk()
root.title('Etalon Calc Program')
root.minsize(400, 300)  # 최소 사이즈


'''기능 추가'''
# 기능1 : 파일 1개 선택
def select_file():
    try:
        filename = askopenfilename(initialdir="./", filetypes=(("Data files", ".csv .txt"), ('All files', '*.*')))
        filename_short = filename.split('/')[-1]
        if filename:
            listbox_filename.delete(0, "end")
            listbox_filename.insert(0, "../" + filename_short)
    except:
        messagebox.showerror("Error", "오류가 발생했습니다.")

'''1. 프레임 생성'''
# 상단 프레임 (LabelFrame)
frm1 = tk.LabelFrame(root, text="Data", pady=15, padx=15)   # pad 내부
frm1.grid(row=0, column=0, pady=10, padx=10, sticky="nswe") # pad 내부
root.columnconfigure(0, weight=1)   # 프레임 (0,0)은 크기에 맞춰 늘어나도록
root.rowconfigure(0, weight=1)      
# 하단 프레임 (Frame)
frm2 = tk.Frame(root, pady=10)
frm2.grid(row=1, column=0, pady=10)

'''2. 요소 생성'''
# 레이블
lbl_filename = tk.Label(frm1, text='데이터 파일 선택')
lbl_exsec = tk.Label(frm1, text='추출 시간 (sec)')
lbl_center = tk.Label(frm1, text='중심 파장(nm)')
lbl_sampling = tk.Label(frm1, text='샘플링 수')
lbl_fsr = tk.Label(frm1, text='FSR (GHz)')
lbl_hz = tk.Label(frm1, text='주파수 (Hz)')

#리스트박스
listbox_filename = tk.Listbox(frm1, width=40, height=1)
listbox_exsec = tk.Listbox(frm1, width=40, height=1)
listbox_center = tk.Listbox(frm1, width=40, height=1)
listbox_sampling = tk.Listbox(frm1, width=40, height=1)
listbox_fsr = tk.Listbox(frm1, width=40, height=1)
listbox_hz = tk.Listbox(frm1, width=40, height=1)

#버튼
btn_filename = tk.Button(frm1, text="...", width=8, command=select_file)


'''3. 요소 배치'''
# 상단 프레임
lbl_filename.grid(row=0, column=0, sticky="e")
lbl_exsec.grid(row=1, column=0, sticky="e", pady= 20)
lbl_center.grid(row=2, column=0, sticky="e", pady= 20)
lbl_sampling.grid(row=3, column=0, sticky="e", pady= 20)
lbl_fsr.grid(row=4, column=0, sticky="e", pady= 20)
lbl_hz.grid(row=5, column=0, sticky="n")
listbox_filename.grid(row=0, column=1, columnspan=2, sticky="we")
listbox_exsec.grid(row=1, column=1, columnspan=2, sticky="we")
listbox_center.grid(row=2, column=1, columnspan=2, sticky="we")
listbox_sampling.grid(row=3, column=1, columnspan=2, sticky="we")
listbox_fsr.grid(row=4, column=1, columnspan=2, sticky="we")
listbox_hz.grid(row=5, column=1, rowspan=2, sticky="wens")

btn_filename.grid(row=0, column=3, sticky="n")
# 상단프레임 grid (2,1)은 창 크기에 맞춰 늘어나도록
frm1.rowconfigure(2, weight=1)      
frm1.columnconfigure(1, weight=1)   

root.mainloop()