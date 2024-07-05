# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:54:40 2023

@author: esc
"""


import pandas as pd
from glob import glob

file_names = glob("C:/Users/quite/Desktop/Deep_learning_Algorithms/*.csv") #폴더 내의 모든 csv파일 목록을 불러온다
writer = pd.ExcelWriter('C:/Users/quite/Desktop/Deep_learning_Algorithms/total.xlsx', engine='xlsxwriter')

for file_name in file_names:
    temp = pd.read_csv(file_name, sep=',', encoding='utf-8') #csv파일을 하나씩 열어 임시 데이터프레임으로 생성한다
    temp.to_excel(writer, sheet_name=file_name.split('\\')[-1].split('_')[1][:-4])

writer.save()