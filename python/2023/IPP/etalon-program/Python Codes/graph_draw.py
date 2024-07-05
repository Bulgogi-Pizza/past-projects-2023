# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:44:34 2023

@author: quite
"""

'''Draw function'''

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, RangeSlider, TextBox
import numpy as np

def draw_calc(fig, ax, etalon):

    '''폰트 설정'''
    circle_size = {"peak" : 5}
    font_size = {"peak" : 10, "etalon" : 10}
    line_width = {"signal" : 0.2}
    
    font_peak = {'size' : font_size["peak"]}
    font_etalon = {'size' : font_size["etalon"]}
    
    '''초기 그래프, 시작선, 끝선 그리기'''
    h0 = ax.scatter([1,2],[1,2],s=circle_size["peak"], c='r')
    h1, = ax.plot(range(0,len(etalon.lamp_data)), etalon.lamp_data, lw = line_width["signal"], color = 'b')
    ax.autoscale(enable=True, axis='both', tight=True)
    h2 = ax.axvline(int(len(etalon.lamp_data)*0.1),color = 'red', linestyle = ':')
    h3 = ax.axvline(int(len(etalon.lamp_data)*0.9),color = 'red', linestyle = ':')

       
    #박스 내부 컬러   
    axcolor = 'lightgoldenrodyellow'
    
    ''' 추출 강도 슬라이더 추가 '''
    extract_ax = plt.axes([0.25, 0.10, 0.65, 0.05], facecolor=axcolor)
    # axes(rect) -> rect : left, bottom, width, height
    extract_slider = Slider(extract_ax, 'Extract Strength', 0, etalon.lamp_sampling // 8, valstep = 1, valinit = etalon.lamp_sampling // 24)
    
    ''' 에탈론 범위 슬라이더 추가 '''
    axrange = plt.axes([0.25, 0.15, 0.65, 0.05], facecolor=axcolor)
    # axes(rect) -> rect : left, bottom, width, height
    s_range = RangeSlider(axrange, 'Etalon Range', 0, len(etalon.lamp_data), valstep = 1, valinit = [int(len(etalon.lamp_data)*0.1), int(len(etalon.lamp_data)*0.9)])

    ''' Redraw 버튼 추가 '''
    redrawax = plt.axes([0.8, 0.025, 0.1, 0.04])
    # axes(rect) -> rect : left, bottom, width, height
    redraw_button = Button(redrawax, 'Redraw', color=axcolor, hovercolor='white')
    
    ''' Add Calc Button '''
    calcax = plt.axes([0.6, 0.025, 0.1, 0.04])
    # axes(rect) -> rect : left, bottom, width, height
    calc_button = Button(calcax, 'Calc', color=axcolor, hovercolor='white')
    
    def update(val):
        start_x = val[0]
        end_x = val[1]
        h2.set_xdata(start_x)
        h3.set_xdata(end_x)
        fig.canvas.draw_idle()
    s_range.on_changed(update)
           
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
        
        # center_wavenumber = 10000000 / center_wavelength
        # start_wavenumber = center_wavenumber - (etalon_val * (new_crest[peak_nums//2] - new_crest[0]))
        # end_wavenumber = center_wavenumber + (etalon_val * (new_crest[-1] - new_crest[peak_nums//2]))
        # start_wavelength = 10000000 / start_wavenumber
        # end_wavelength = 10000000 / end_wavenumber
        
        # stem_start.set_array(np.c_[new_crest[0],etalon.lamp_data[new_crest[0]]])
        # stem_middle.set_array(np.c_[new_crest[len(new_crest)//2],etalon.lamp_data[new_crest[len(new_crest)//2]]])
        # stem_end.set_array(np.c_[new_crest[-1],etalon.lamp_data[new_crest[-1]]])
    
        # text_start.set_position([new_crest[0],0])
        # text_start.set_text(str(round(start_wavelength,3)) + "nm")
        # text_middle.set_position([new_crest[len(new_crest)//2],0])
        # text_middle.set_text(str(round(center_wavelength,3)) + "nm")
        # text_end.set_position([new_crest[-1],0])
        # text_end.set_text(str(round(end_wavelength,3)) + "nm")
    
        fig.canvas.draw_idle()
    calc_button.on_clicked(calc)
    
    # plt.show()
    # plt.draw()