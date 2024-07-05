# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:50:57 2023

@author: esc
"""

import os

f_list = os.listdir("./연도별 영어만 test")[:-1]

fn = "G:/.shortcut-targets-by-id/1C7URAIpqzbig-k5e569I-GfyYqkW9Yzh/ESC_lab6/동인/다시 정리 NLP_DL 트렌드/분석 흐름/연도별 영어만 test/"

for f_name in f_list :
    fp = open(fn + f_name, 'r', encoding = 'utf-8')
    data = fp.readlines()
    print(f_name)
    print(len(data))