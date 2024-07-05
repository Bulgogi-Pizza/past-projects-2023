# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:39:36 2022

크롤링 한 abstract 파일들을 영어와 한글 분리해주는 함수
크롤링 할 파일들이 있는 디렉토리로 이동 후 사용

@author: quite
"""
import re
import os

directory = "G:/.shortcut-targets-by-id/1C7URAIpqzbig-k5e569I-GfyYqkW9Yzh/ESC_lab6/동인/다시 정리 NLP_DL 트렌드/Deep_learning_Algorithms/전반기 후반기"
directory = "C:/Users/quite/Desktop/Deep_learning_Algorithms/연도별"

fp_list = os.listdir(directory)
for f_name in fp_list :
    if '.txt' in f_name :
        pass
    else :
        continue
    #파일 불러오기
    fp_lines = open(directory + '/' + f_name,'r',encoding="utf-8")
    data_lines = fp_lines.readlines()
    
    # #step 1
    # #초록 없는 문단 제거
    # pop_num = []
    # num = 0
    
    # for sentences in data_lines:
    #     if(len(sentences) < 10) :
    #         pop_num.append(num)
    #     num = num + 1
    
    # for i in range(0,len(pop_num) - 1):
    #     data_lines.pop(pop_num[i]-i)
        
    #step 2
    #영어 문단과 한글 문단 분리
    
    korean = []
    english = []
    
    #sentence_enko는
    #result = re.search('[가-힇].*$',sentence) 
    #korean_start = result.start() 가 절대 10 이하로 나오지 않음
    
    #sentence_koen은
    #result = re.search('.*[가-힇]',sentence)
    #korean_end = result.end() 가 절대 len(sentence)-10 보다 크지 않음
    
    #sentence_ko 는
    #korean_start가 10이하이고 korean_end가 len(sentence)-10 보다 큼
    
    #sentence_eng 는
    #result.start() 등의 함수를 실행할 수 없음
    
    attempts = 0
    for sentence in data_lines:
        
        result = re.search('[가-힇].*$',sentence)
        try : korean_start = result.start()
        except : english.append(sentence)
            
        result = re.search('.*[가-힇]',sentence)
        try : korean_end = result.end() + 1
        except : pass
            
        try : 
            result.start()
            if(korean_start < 10 and korean_end > len(sentence)-10) :
                korean.append(sentence)
            if(korean_start < 10 and not(korean_end > len(sentence)-10)) :
                korean.append(sentence[:korean_end])
                english.append(sentence[korean_end+1:])
            if(not(korean_start < 10) and korean_end > len(sentence)-10) :
                korean.append(sentence[korean_start:])
                english.append(sentence[:korean_start-1])
        except : pass
        
    #step 3
    #한국어 txt, 영어 txt 출력
    f_onlyname = f_name.replace('.txt','')
    fp_eng = open("C:/Users/quite/Desktop/Deep_learning_Algorithms/연도별/" + f_onlyname + "_english.txt",'w+',encoding="utf-8")
    #fp_kor = open(f_onlyname + "_korean.txt", 'w+',encoding="utf-8")
    
    # english_txt = ''.join(english)
    # korean_txt = ''.join(korean)
    english_txt = ''
    korean_txt = ''
    for english_sen in english :
        if len(english_sen) > 50 :
            english_txt = english_txt + english_sen + '\n'
    for korean_sen in korean :
        if len(korean_sen) > 50 :
            korean_txt = korean_txt + korean_sen + '\n'
    
    english_txt = english_txt.replace('\n\n','\n')
    korean_txt = korean_txt.replace('\n\n','\n')
    
    fp_eng.write(english_txt)
    #fp_kor.write(korean_txt)
    
    fp_lines.close()
    fp_eng.close()
    #fp_kor.close()

            
        
    

# num = 0
# if(is_first_eng and is_end_eng) :
#     english.append(num)
    

# def first_end(sentence) :
#     print("first : ",sentence[0])
#     print("end : ",sentence[len(sentence)-3])
    
#     return sentence[0], sentence[len(sentence)-3]
