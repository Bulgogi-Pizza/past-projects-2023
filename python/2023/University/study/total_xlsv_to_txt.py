# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:01:00 2023

@author: esc
"""


import csv
import re
import os
import codecs
import pandas as pd

f_name = "C:/Users/quite/Desktop/Deep_learning_Algorithms/total_delete_linechange.xlsx"
f_name = "G:/다른 컴퓨터/내 컴퓨터 (1)/Deep_learning_Algorithms/total_delete_linechange.xlsx"
df = pd.read_excel(f_name, sheet_name=None, engine = 'openpyxl')
sheets = list(df.keys())


for key in sheets:
    abstract_15_18 = []
    abstract_19_22 = []
    abstract_total = []
    years = df[key]['date']
    abstracts = df[key]['abstract']
    
    i = 0
    for year in years:
        try :
            if int(year) < int(2019) and int(year) > int(2014) :
                abstract_15_18.append(abstracts[i])
            elif int(year) > int(2018) :
                abstract_19_22.append(abstracts[i])
        except : pass
        #abstract_total.append(abstract)
        i = i + 1
    print(key)
    # data = '\n'.join(abstract)
    # data = data[9:]
    
    data = '\n'.join(abstract_15_18)
    fp_3 = open('C:/Users/quite/Desktop/crawling_'+key+"_15_18.txt",'w+',encoding = 'utf-8')
    fp_3.write(data)
    fp_3.close()

    
    data = '\n'.join(abstract_19_22)
    fp_4 = open('C:/Users/quite/Desktop/crawling_'+key+"_19_22.txt",'w+',encoding = 'utf-8')
    fp_4.write(data)
    fp_4.close()
    
    # #data_total = '\n'.join(abstract_total)
    # data_15_18 = '\n'.join(abstract_15_18)
    # data_19_22 = '\n'.join(abstract_19_22)
    
    # #fp_2 = open('crawling_'+key+"_total.txt",'w+',encoding = 'utf-8')
    # fp_3 = open('crawling_'+key+"_15_18.txt",'w+',encoding = 'utf-8')
    # fp_4 = open('crawling_'+key+"_19_22.txt",'w+',encoding = 'utf-8')
    
    # #fp_2.write(data_total)
    # fp_3.write(data_15_18)
    # fp_4.write(data_19_22)

#fp_2.close()

