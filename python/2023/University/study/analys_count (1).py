# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import platform
import copy

algorithm_counts = 6

check_system = platform.uname()[1]
if check_system == 'CDIs-MacBook-Pro.local':
    file_path = '/Users/cdi/Library/CloudStorage/GoogleDrive-quitendexit@gmail.com/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_real_only_rl.xlsx'
    excel_path = '/Users/cdi/Library/CloudStorage/GoogleDrive-quitendexit@gmail.com/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_real_only_rl_analys.xlsx'
else:
    file_path = "G:/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_real_1,2,stopwords.xlsx"
    excel_path = "G:/다른 컴퓨터/내 컴퓨터/Deep_learning_Algorithms/total_real_1,2,stopwords_analysed.xlsx"
    file_path = "C:/Users/quite/Desktop/total_real.xlsx"
    excel_path = "C:/Users/quite/Desktop/Deep_learning_Algorithms/total_real_analysed_231004.xlsx"
file_read = pd.read_excel(file_path,'keywords_common')  #
file_read = file_read[file_read.columns[1:]]    #0번째 열 제거
titles = list(file_read)

lists_rank_changed = []
lists_value_changed = []
list_news = []
for i in range(algorithm_counts):
    list_old = list(file_read[titles[4*i]])
    list_new = list(file_read[titles[4*i+2]])
    count_old = list(file_read[titles[4*i+1]])
    count_new = list(file_read[titles[4*i+3]])
    rank_changed = []
    value_changed = []
    
    for index_new in range(len(file_read[titles[4*i]])):
        if list_new[index_new] in list_old:
            for index_old in range(len(file_read[titles[4*i+2]])):
                if list_new[index_new] == list_old[index_old]:
                    rank_changed.append(int(index_old - index_new))
                    value_changed.append(int(count_new[index_new] - count_old[index_old]))
        else :
            rank_changed.append(-500)
            value_changed.append(-500)
            
    lists_rank_changed.append(rank_changed)
    lists_value_changed.append(value_changed)
    list_news.append(list_new)


####################################################################
###standards for ranks            ##################################
####################################################################
###rank changed
##################################
list_ranked = []    
for i in range(algorithm_counts):
    dummy = []
    for j in range(len(list_new)):
        dummy.append([list_news[i][j], lists_rank_changed[i][j]])
    list_ranked.append(dummy)
    
##################################
###rank changed, sorts
##################################
list_common = copy.deepcopy(list_ranked)
for i in range(algorithm_counts):
    list_common[i].sort(key=lambda x:x[1], reverse=True)
    
    
##################################
###rank changed, shorter
##################################
list_ranked_short = copy.deepcopy(list_ranked)
for i in range(algorithm_counts):
    list_ranked_short[i] = list_ranked_short[i][:30]

##################################
###rank changed, sort, shorter
##################################
list_common_short = copy.deepcopy(list_ranked_short)
for i in range(algorithm_counts):
    list_common_short[i].sort(key=lambda x:x[1], reverse=True)
    
    
####################################################################
###standards for values           ##################################
####################################################################
###rank value changed
##################################
list_ranked_values = []
for i in range(algorithm_counts):
    dummy = []
    for j in range(len(list_new)):
        dummy.append([list_news[i][j], lists_value_changed[i][j]])
    list_ranked_values.append(dummy)
    
##################################
###rank value changed, sort
##################################
list_common_values = copy.deepcopy(list_ranked_values)
for i in range(algorithm_counts):
    list_common_values[i].sort(key=lambda x:x[1], reverse=True)
    
##################################
###rank changed, shorter
##################################
list_ranked_short_values = copy.deepcopy(list_ranked_values)
for i in range(algorithm_counts):
    list_ranked_short_values[i] = list_ranked_short_values[i][:30]

##################################
###rank changed, sort, shorter
##################################
list_common_short_values = copy.deepcopy(list_ranked_short_values)
for i in range(algorithm_counts):
    list_common_short_values[i].sort(key=lambda x:x[1], reverse=True)
    

#list to dataframe
# df_ranked = pd.DataFrame(list(zip(list_ranked)), columns = ['ranked',''])
# df_common = pd.DataFrame(list(zip(list_common)), columns = ['common',''])
# df_ranked_short = pd.DataFrame(list(zip(list_ranked_short)), columns = ['ranked_short',''])
# df_common_short = pd.DataFrame(list(zip(list_common_short)), columns = ['common_short',''])
# df_ranked_values = pd.DataFrame(list(zip(list_ranked_values)), columns = ['ranked_values',''])
# df_common_values = pd.DataFrame(list(zip(list_common_values)), columns = ['common_values',''])
# df_ranked_short_values = pd.DataFrame(list(zip(list_ranked_short_values)), columns = ['ranked_short_values',''])
# df_common_short_values = pd.DataFrame(list(zip(list_common_short_values)), columns = ['common_short_values',''])

column_list = ['autoencoder','cnn','gan','lstm','rnn','rl']

df_ranked = pd.DataFrame(list(zip(*list_ranked)), columns = column_list)
df_common = pd.DataFrame(list(zip(*list_common)), columns = column_list)
df_ranked_short = pd.DataFrame(list(zip(*list_ranked_short)), columns = column_list)
df_common_short = pd.DataFrame(list(zip(*list_common_short)), columns = column_list)
df_ranked_values = pd.DataFrame(list(zip(*list_ranked_values)), columns = column_list)
df_common_values = pd.DataFrame(list(zip(*list_common_values)), columns = column_list)
df_ranked_short_values = pd.DataFrame(list(zip(*list_ranked_short_values)), columns = column_list)
df_common_short_values = pd.DataFrame(list(zip(*list_common_short_values)), columns = column_list)
     
#write to excel
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    
df_ranked.to_excel(writer, sheet_name= 'ranked')
df_common.to_excel(writer, sheet_name= 'common')
df_ranked_short.to_excel(writer, sheet_name= 'ranked_short')
df_common_short.to_excel(writer, sheet_name= 'common_short')
df_ranked_values.to_excel(writer, sheet_name= 'ranked_values')
df_common_values.to_excel(writer, sheet_name= 'common_values')
df_ranked_short_values.to_excel(writer, sheet_name= 'ranked_short_values')
df_common_short_values.to_excel(writer, sheet_name= 'common_short_values')

writer.save()
writer.close()



























