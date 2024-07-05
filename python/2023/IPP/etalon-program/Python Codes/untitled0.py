# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 17:08:44 2023

@author: quite
"""

#matplotlib.use('TkAgg')

def redraw_graph(figure, ax):
    draw_calc(figure, ax, EtalonApp.etalon)
     
      #drawing updated values
    canvas.draw()
     
 
  # 기능2 : 입력받은 값을 가지고 다음 페이지로 넘어감
def switch_fourth_frame():
    try:
        pass#EtalonApp.etalon.lamp_data = redraw
    except:
        messagebox.showerror("Error", "에러 발생.")
             
def window_exit():
    frm.quit()
    frm.destroy()
 
'''1. 프레임 생성'''
frm= tk.Tk()
frm_top = tk.Frame(frm, pady=15, padx=15)
frm_left = tk.Frame(frm, pady=15, padx=15)
frm_right = tk.Frame(frm, pady=15, padx=15)
frm_bottom = tk.Frame(frm, pady=15, padx=15)
frm1 = tk.LabelFrame(frm_left, text="Data", pady=2, padx=15)   # pad 내부
frm1_1 = tk.Frame(frm1, pady=15, padx=15)
frm1_2 = tk.Frame(frm1, pady=15, padx=15)
frm2 = tk.Frame(frm_right, pady=15, padx = 15)
frm3 = tk.LabelFrame(frm_left, text="Noise Reduction", pady=2, padx=15)

'''1-1. 프레임 배치'''
frm_top.pack(side="top", pady=5, padx=5, fill="x", expand = "no")
frm_bottom.pack(side="bottom", pady=5, padx=5, fill="x", expand = "no")
frm_left.pack(side="left", pady=5, padx=5, fill="y", expand = "no") # pad 내부
frm_right.pack(side="right", pady=5, padx=5, fill="both", expand = "yes") # pad 내부
frm1.pack(side="top", pady=5, padx=5, fill="x", expand = "no") # pad 내부
frm1_1.pack(side="left")#, fill="both", expand = "yes")
frm1_2.pack(side="right")#, fill="both", expand = "yes")
frm2.pack(side="top", pady=5, padx=5, fill="both", expand = "yes")
frm3.pack(side="top", pady=5, padx=5, fill="x", expand = "no")
   

'''2. 요소 생성'''
###########main
#버튼
btn_next = tk.Button(frm_bottom, text="Next", command=lambda: window_exit())
btn_redraw = tk.Button(frm_bottom, text="Redraw", command=lambda: redraw_graph(figure, ax))
#레이블
lbl_title = tk.Label(frm_top, text="Page Three", font=('MalgunGothic',18))
   
###########frm1
# 레이블
lbl_filename = tk.Label(frm1_1, text='데이터 파일 선택')
lbl_exsec = tk.Label(frm1_1, text='추출 시간 (sec)')
lbl_center = tk.Label(frm1_1, text='중심 파장(nm)')
lbl_sampling = tk.Label(frm1_1, text='샘플링 수')
lbl_fsr = tk.Label(frm1_1, text='FSR (GHz)')
lbl_hz = tk.Label(frm1_1, text='주파수 (Hz)')
#리스트박스
listbox_filename = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
listbox_exsec = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
listbox_center = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
listbox_sampling = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
listbox_fsr = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
listbox_hz = tk.Listbox(frm1_2, width=40, height=1, bg='lightgray')
   
'''그래프 그리기'''
matplotlib.use('TkAgg')
###########frm2
#그래프 창
# to run GUI event loop
#plt.ion()
 
# here we are creating sub plots
figure, ax = plt.subplots()
figure.set_dpi(200)
canvas = FigureCanvasTkAgg(figure, frm2)
tkagg.NavigationToolbar2Tk(canvas, frm2)
#canvas.draw()
canvas.get_tk_widget().pack(side="top", fill="both", expand="yes")
figure.subplots_adjust(bottom=0.25)


'''폰트 설정'''
circle_size = {"peak" : 5}
font_size = {"peak" : 10, "etalon" : 10}
line_width = {"signal" : 0.2}

font_peak = {'size' : font_size["peak"]}
font_etalon = {'size' : font_size["etalon"]}

'''초기 그래프, 시작선, 끝선 그리기'''
h0 = ax.scatter([1,2],[1,2],s=circle_size["peak"], c='r')
h1 = ax.plot(range(0,len(EtalonApp.etalon.lamp_data)), EtalonApp.etalon.lamp_data, lw = line_width["signal"], color = 'b')
h2 = ax.axvline(int(len(EtalonApp.etalon.lamp_data)*0.1),color = 'red', linestyle = ':')
h3 = ax.axvline(int(len(EtalonApp.etalon.lamp_data)*0.9),color = 'red', linestyle = ':')
ax.autoscale(enable=True, axis='both', tight=True)

   
#박스 내부 컬러   
axcolor = 'lightgoldenrodyellow'

''' 추출 강도 슬라이더 추가 '''
extract_ax = plt.axes([0.25, 0.10, 0.65, 0.05], facecolor=axcolor)
# axes(rect) -> rect : left, bottom, width, height
extract_slider = Slider(extract_ax, 'Extract Strength', 0, EtalonApp.etalon.lamp_sampling // 8, valstep = 1, valinit = EtalonApp.etalon.lamp_sampling // 24)

''' 에탈론 범위 슬라이더 추가 '''
axrange = plt.axes([0.25, 0.15, 0.65, 0.05], facecolor=axcolor)
# axes(rect) -> rect : left, bottom, width, height
s_range = RangeSlider(axrange, 'Etalon Range', 0, len(EtalonApp.etalon.lamp_data), valstep = 1, valinit = [int(len(EtalonApp.etalon.lamp_data)*0.1), int(len(EtalonApp.etalon.lamp_data)*0.9)])

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
    figure.canvas.draw_idle()
s_range.on_changed(update)
   
   
###########frm3
#레이블
lbl_wvlen = tk.Label(frm3, text='스캔 범위 (Wavelength)')
lbl_etalon = tk.Label(frm3, text='Etalon Value')
#리스트박스
listbox_wvlenrange = tk.Listbox(frm3, width=40, height=1, bg='lightgray')
listbox_etalon = tk.Listbox(frm3, width=40, height=1, bg='lightgray')
   
'''2-1. 요소 배치'''
##########main
#버튼
btn_next.pack(side="right",anchor="s")
btn_redraw.pack(side="right",anchor="s")
#레이블
lbl_title.pack(side="top")

###########frm1
#레이블
lbl_title.pack(side = "top", pady=5)
lbl_filename.pack(side = "top", anchor="w", pady=5)
lbl_exsec.pack(side = "top", anchor="w", pady=5)
lbl_center.pack(side = "top", anchor="w", pady=5)
lbl_sampling.pack(side = "top", anchor="w", pady=5)
lbl_fsr.pack(side = "top", anchor="w", pady=5)
lbl_hz.pack(side = "top", anchor="w", pady=5)
#리스트박스
listbox_filename.pack(side="top", anchor="e", pady=5)
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
   
   
'''3. 값 인풋'''
#리스트박스 값 인풋
listbox_filename.delete(0, "end")
listbox_filename.insert(0, str(EtalonApp.filename_short))
listbox_exsec.insert(0, str(EtalonApp.exsec))
listbox_center.insert(0, str(EtalonApp.center))
listbox_sampling.insert(0, str(EtalonApp.etalon.sampling))
listbox_fsr.insert(0, str(EtalonApp.etalon.FSR))
listbox_hz.insert(0, str(EtalonApp.etalon.Hz))
# listbox_wvlenrange(0, str(wvlen_start) + " - " + str(wvlen_middle) + " - ", str(wvlen_end))
# listbox_etalon(0, str(etalon_value))

frm2 = tk.Tk()
frm2.wm_title("Embedding in TK")

frm.mainloop()
