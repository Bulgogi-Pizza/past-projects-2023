# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

file_path = "G:/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_real_1,2,stopwords.xlsx"
file_read = pd.read_excel(file_path,'keywords_common')  #
file_read = file_read[file_read.columns[1:]]    #0번째 열 제거
titles = list(file_read)

lists_rank_changed = []
list_news = []
for i in range(6):
    list_old = list(file_read[titles[4*i]])
    list_new = list(file_read[titles[4*i+2]])
    count_old = list(file_read[titles[4*i+1]])
    count_new = list(file_read[titles[4*i+3]])
    rank_changed = []
    
    for index_new in range(len(file_read[titles[4*i]])):
        if list_new[index_new] in list_old:
            for index_old in range(len(file_read[titles[4*i+2]])):
                if list_new[index_new] == list_old[index_old]:
                    rank_changed.append(int(index_old - index_new))
        else :
            rank_changed.append('-')
              
    lists_rank_changed.append(rank_changed)
    list_news.append(list_new)

list_ranked = []    
for i in range(6):
    list_ranked.append(list_news[i])
    list_ranked.append(lists_rank_changed[i])
    
list_common = list_ranked
