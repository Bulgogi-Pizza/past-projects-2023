# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 20:19:44 2022

@author: quite
"""

import re
import nltk
import gensim
import os
import pandas as pd

from nltk.corpus import stopwords
from collections import Counter

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

#for Lemmatization
from nltk.stem import WordNetLemmatizer

from keybert import KeyBERT

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# #데이터 전처리 (원본 = 문단 리스트)
# def preprocessing(paragraph_list) :
#     '''
#     Parameters
#     ----------
#     paragraph_list : LIST
#         [paragraph_0, paragraph_1, ..., paragraph_n]

#     Returns
#     -------
#     parapraph_list : LIST (preprocessed paragraph)
#         [paragraph_0, paragraph_1, ..., paragraph_n]
#     tokenized_doc_list : LIST (tokenized words)
#         [[para_1_word_1, para_1_word_2, ...para_1_word_m],[],[],[para_n,words]]
#     '''
#     tokenized_doc_list = []
#     stop_words = stopwords.words('english')
#     for i in range(0,len(paragraph_list)-1) :
#         paragraph_list[i] = re.sub('[^a-zA-Z]',' ',paragraph_list[i])
#         paragraph_list[i] = paragraph_list[i].lower()
        
#         tokenized_doc = paragraph_list[i].split()
#         tokenized_doc = [item for item in tokenized_doc if item not in stop_words]
#         tokenized_doc_list.append(tokenized_doc)
        
#     return paragraph_list, tokenized_doc_list

# #LSA topic 출력
# def get_topics(components, feature_names, n=5):
#     topics = []
#     for idx, topic in enumerate(components):
#         print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(5)) for i in topic.arg_tokensort()[:-n - 1:-1]])
#         topics.append([(feature_names[i], topic[i].round(5)) for i in topic.arg_tokensort()[:-n - 1:-1]])
#     return topics


    
##############################################################
#start#
#start#
#start#
#영어 문단 리스트 생성
#'autonomous driving','medical deep learning','Deep Belief Networks','Self Organization Map','Reinforcement Learning','Recurrent Neural Network','Radial Basis Function Network','Multilayer Perceptron','Generation Adversarial Network','Gated Recurrent Unit','Convolution Neural Network','virtual influencer','speech recognition','sentence classification','natural language processing','named entity recognition','machine translation'
#algorithms = ['Autoencoder','Deep Belief Networks','Self Organization Map','Reinforcement Learning','Recurrent Neural Network','Radial Basis Function Network','Multilayer Perceptron','Generation Adversarial','Gated Recurrent Unit','Convolution Neural Network','autonomous driving','natural language process','visual recognition','text recognition','colorization image','machine translation','image captioning','named entity recognition','speech recognition','virtual influencer','medical deep learning']
#algorithms = ['autonomous driving','natural language processing','visual recognition','text recognition','colorization image','machine translation','image captioning','named entity recognition','speech recognition','virtual influencer','medical deep learning','Autoencoder','Restricted Boltzmann Machine','Deep Belief Networks','Self Organization Map','Reinforcement Learning','Recurrent Neural Network','Radial Basis Function Network','Multilayer Perceptron','Generation Adversarial Network','Gated Recurrent Unit','Convolution Neural Network']
algorithms = ['named entity recognition','speech recognition','virtual influencer','medical deep learning','Autoencoder','Restricted Boltzmann Machine','Deep Belief Networks','Self Organization Map','Reinforcement Learning','Recurrent Neural Network','Radial Basis Function Network','Multilayer Perceptron','Generation Adversarial Network','Gated Recurrent Unit','Convolution Neural Network']

directory = "C:/Users/quite/Desktop/Deep_learning_Algorithms/연도별 영어만"

common_list_df = pd.DataFrame()
common_algorithm_df = pd.DataFrame()
common_token_df = pd.DataFrame()
keywords_common_list_df = pd.DataFrame()

fp_list = os.listdir(directory)
# for algorithm in algorithms :
#     for aaa in ['','_G','_15_18','_19_21'] :
for f_name in fp_list:
        fp = open(directory + '/' + f_name,'r',encoding="utf-8")
        #fp2 = open("data_"+algorithm+".txt",'w+',encoding="utf-8")
        data = fp.readlines()
        fp.seek(0)
        data_read = fp.read()
        
        #빈도수 출력
        word_tokens = nltk.word_tokenize(data_read)
        
        stop_words = set(stopwords.words('english')) 
        
        lemmatizer = WordNetLemmatizer()
        
        num = 0
        results = []
        tokens = []
        for i in range(0,len(word_tokens)-1):
            word_tokens[i] = re.sub(r'[^A-Za-z0-9_]', '', word_tokens[i])
            #word_tokens[i] = word_tokens[i].lower()
            #word_tokens[i] = re.sub(r'[^A-Z]', '', word_tokens[i])
        for word in word_tokens: 
            if word not in stop_words: 
                if len(word) > 2 and word != 'sub' and word != '/sub':
                    results.append(word)
                if len(word) > 2 and word != 'sub' and word != '/sub' and word.isupper():
                    for i in range(num-7,num):
                        if len(word_tokens[i+1]) > 2 :
                            if word_tokens[i+1][0].isupper() and word_tokens[i+1][1].islower() and word_tokens[i+1] not in ['The','Because'] :
                                tokens.append(word_tokens[i+1])
                    tokens.append(word)
                    
            num = num + 1
        
        results = [lemmatizer.lemmatize(word) for word in results]
        
        ngk1 = list(nltk.ngrams(tokens,1))
        ngk2 = list(nltk.ngrams(tokens,2))
        ngk3 = list(nltk.ngrams(tokens,3))
        ngk4 = list(nltk.ngrams(tokens,4))
        ngk5 = list(nltk.ngrams(tokens,5))
        ngk6 = list(nltk.ngrams(tokens,6))
        ngk7 = list(nltk.ngrams(tokens,7))
        ngk8 = list(nltk.ngrams(tokens,8))
        
        ng1 = list(nltk.ngrams(results,1))
        ng2 = list(nltk.ngrams(results,2))
        ng3 = list(nltk.ngrams(results,3))
        ng4 = list(nltk.ngrams(results,4))
        ng5 = list(nltk.ngrams(results,5))
        ng6 = list(nltk.ngrams(results,6))
        ng7 = list(nltk.ngrams(results,7))
        ng8 = list(nltk.ngrams(results,8))
        
        ng_tokens = ngk2 + ngk3 + ngk4 + ngk5 + ngk6 + ngk7 + ngk8
    
        ng = ng2 + ng3 + ng4 + ng5 + ng6 + ng7 + ng8
        tt = []
        num = 0
        for a in ng_tokens :
            popp = 0
            for i in range(0,len(a)-1):
                if a[i].isupper() :
                    popp = 1
            if a[len(a)-1].islower() or a[len(a)-1].istitle():
                popp = 1
            if(popp == 1):
                tt.append(num)
            num = num + 1
        
        
        num = 0
        for i in tt:
            ng_tokens.pop(i-num)
            num = num+1
        
        for i in range(0,len(ng_tokens)):
            for j in range(0,len(ng_tokens[i])):
                lst = [lemmatizer.lemmatize(word) for word in ng_tokens[i]]   
            ng_tokens[i] = tuple(lst)
                
            
        fdist = nltk.FreqDist(ng_tokens)
        fdist_token = nltk.FreqDist(ng)
        
        token_list = fdist_token.most_common(n=200)
        algorithm_list = fdist.most_common(n=50)
        
        count = Counter(results)
        try : noun_list = count.most_common(150)
        except : noun_list = count.most_common(20)
        
        common_token = []
        common_algorithm = []
        common_list = []    
        
        for v in noun_list:
            #print(v)
            common_list.append(list(v))
            
        for v in algorithm_list:
            #print(v)
            common_algorithm.append(list(v))
            
        for v in token_list:
            #print(v)
            common_token.append(list(v))
        
        print("done 1")

        ######################################################################
        #keyBERT
        #for keyBERT, english
        #사용 전처리 : 문단 단위 (완전한 문단, 전처리를 거치지 않은)
    
        num = 0
        
        output = []
        
        stop_words = set(stopwords.words('english')) 
        stop_list = ['learning','networks','neural','convolutional','cnn','cnns','rnns','gans','dcnn','network','rnn','gan','rbfn','mlp','gru','lstm','autoencoder','memory','generative','adversarial','autoencoders','reinforcement','using']
        
        for stop in stop_list:
            stop_words.add(stop)
        
        do_lemmatize = True
        
        if do_lemmatize :
            lemmatizer = WordNetLemmatizer()
            
            for sentence in data:
                output.append(" ".join([lemmatizer.lemmatize(i) for i in sentence.split()]))
        else :
            output = data
        
        
        md = SentenceTransformer('all-MiniLM-L6-v2')#,device="mps")
        #md = SentenceTransformer('gpt2-xl')#,device="mps")
        
        kw_model = KeyBERT(md)
        #kw_model = KeyBERT('distilbert-base-nli-mean-tokens')
        #kw_model = KeyBERT('paraphrase-MiniLM-L6-v2')
        
        keywords_list = []
        keywords_list_mss = []
        answer = []
        
        keywords = kw_model.extract_keywords(output, keyphrase_ngram_range=(1,2), stop_words=stop_words, top_n = 10)
        #keywords = kw_model.extract_keywords(output, keyphrase_ngram_range=(1,3), stop_words='english', use_maxsum=True, nr_candidates = 20,top_n = 10)
        keywords_list.append(keywords)
        #keywords_list_mss(keywords_mss)
            
        answer = sum(keywords_list[0], [])
        #answer_mss = sum(keywords_list_mss, [])
        answer = [only_keyword[0] for only_keyword in answer]
        #answer_mss = [only_keyword[0] for only_keyword in answer_mss]
        #answer_mss = [only_keyword[0] for only_keyword in answer_mss]
        count_keywords = Counter(answer)
        #count_keywords_mss = Counter(answer_mss)
        
        try : keywords_common_list = count_keywords.most_common(400)
        except : keywords_common_list = count_keywords.most_common(250)
        #try : keywords_mss_common_list = count_keywords_mss.most_common(400)
        #except : keywords_mss_common_list = count_keywords_mss.most_common(250)
        #print(k)
        
        #max_sum_sim(doc_embedding, candidate_embeddinng_tokens, candidates, top_n=10, nr_candidates=20)
        #print((mmr(doc_embedding, candidate_embeddinng_tokens, candidates, top_n=10, diversity=0.7)))
        #diversity를 낮추면 기존 코사인 유사도만 사용한 것과 매우 유사하게 나옴.(0.2)
        #0.7정도 사용 권장
        # mmr(doc_embedding, candidate_embeddinng_tokens, candidates, top_n=5, diversity=0.7)
        
        print("done 2")
    
        common_list_df = pd.concat([common_list_df, pd.DataFrame(common_list, columns = [f_name[9:-12],''])], axis=1)
        common_algorithm_df = pd.concat([common_algorithm_df, pd.DataFrame(common_algorithm, columns = [f_name[9:-12],''])], axis=1)
        common_token_df = pd.concat([common_token_df, pd.DataFrame(common_token, columns = [f_name[9:-12],''])], axis=1)
        keywords_common_list_df = pd.concat([keywords_common_list_df, pd.DataFrame(keywords_common_list, columns = [f_name[9:-12],''])], axis=1)

            
#file_names = glob("C:/Users/esc/Desktop/Deep_learning_Algorithms/*.csv") #폴더 내의 모든 csv파일 목록을 불러온다
writer = pd.ExcelWriter('C:/Users/quite/Desktop/total_real.xlsx', engine='xlsxwriter')

common_list_df.to_excel(writer, sheet_name="word_common")
common_algorithm_df.to_excel(writer, sheet_name="algorithm_common")
common_token_df.to_excel(writer, sheet_name="token_common")
keywords_common_list_df.to_excel(writer, sheet_name="keywords_common")

writer.save()
    