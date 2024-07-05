# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:27:34 2022

@author: quite
"""
#CNN, LSTM, RNN, 
# -*- coding: utf-8 -*-

import pandas as pd
# import time
import math
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

print("start crawling..")

path = 'C:\\Users\\quite\\Desktop\\DBpia_crawler\\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-suage')
driver = set_chrome_driver()

search = ['Autoencoder','Restricted Boltzmann Machines','Deep Belief Networks','Self Organization Map','Reinforcement Learning','Recurrent Neural Network','Radial Basis Function Network','Multilayer Perceptron','Generative Adversarial Network','Gated Recurrent Unit','Convolution Neural Network','LSTM']
#search = ['Autonomous Driving','Natural Language Processing', 'Visual Recognition', 'Text Recognition','Colorization Image','Machine Translation','Image Captioning', 'Named Entity Recognition', 'Speech Recognition', 'Virtual Influencer', 'Medical Deep Learning']
print("only korean = 1")
print("include global = 2")
include_global = 2

for keyword in search :
    
    url1 = "http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery="
    #+ search keyword like - Autoencoder
    url2 = "&exQuery=pyear%3A2022%E2%97%88pyear%3A2021%E2%97%88pyear%3A2020%E2%97%88pyear%3A2019%E2%97%88pyear%3A2018%E2%97%88pyear%3A2017%E2%97%88pyear%3A2016%E2%97%88pyear%3A2015%E2%97%88&exQueryText=%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2022%5D%40%40pyear%3A2022%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2021%5D%40%40pyear%3A2021%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2020%5D%40%40pyear%3A2020%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2019%5D%40%40pyear%3A2019%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2018%5D%40%40pyear%3A2018%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2017%5D%40%40pyear%3A2017%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2016%5D%40%40pyear%3A2016%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2015%5D%40%40pyear%3A2015%E2%97%88&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0"
    #+ start num
    url3 = "&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=1&resultKeyword="
    #+ search keyword like - "Autoencoder
    url4 = "&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=100&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query="
    #+ search keyword like - "Autoencoder"
    
    # url1 = "http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery="
    # #+ search keyword
    # url2 = "&exQuery=pyear%3A2022%E2%97%88pyear%3A2021%E2%97%88pyear%3A2020%E2%97%88pyear%3A2019%E2%97%88pyear%3A2018%E2%97%88pyear%3A2017%E2%97%88pyear%3A2016%E2%97%88pyear%3A2015%E2%97%88&exQueryText=%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2021%5D%40%40pyear%3A2021%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2020%5D%40%40pyear%3A2020%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2019%5D%40%40pyear%3A2019%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2018%5D%40%40pyear%3A2018%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2017%5D%40%40pyear%3A2017%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2016%5D%40%40pyear%3A2016%E2%97%88%EB%B0%9C%ED%96%89%EC%97%B0%EB%8F%84+%5B2015%5D%40%40pyear%3A2015%E2%97%88&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount=0"
    # #+ start num
    # url3 = "&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=&sflag=1&isFDetailSearch=N&pageNumber=1&resultKeyword="
    # #+ search keyword
    # url4 = "&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=100&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query="
    # #+ search keyword
    # url4_global = "&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_over&colName=re_a_over&pageScale=100&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query="
    

    # 논문제목,날짜,초록
    titleL = []
    dateL = []
    abstractL = []
    titleL_G = []
    dateL_G = []
    abstractL_G = []

    print("start parsing")

    for mode in range(0,include_global):    
        
        #첫 페이지 접속
        #For RISS
        if(mode == 0) :
            url_forward = url1 + keyword + url2
            url_backward = url3 + keyword + url4 + keyword
            driver.get(url_forward + str(0) + url_backward)
        #For arxiv
        if(mode == 1) :
            url_forward = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=" + '' + keyword + ''
            url_backward = "&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2015&date-to_date=2022&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first&start="
            url_backward_2 = "&terms-0-field=title&classification-computer_science=y&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=2015&date-to_date=2022&date-date_type=submitted_date&abstracts=show&size=200&order=announced_date_first&start="
            driver.get(url_forward + url_backward + str(0))
        #For ScienceDirect
        if(mode == 2) :
            uri = "http://lps3.www.sciencedirect.com.libproxy.ut.ac.kr/search?qs=abc&origin=home&zone=qSearch#submit"
            driver.get()
            research_article_btn = driver.find_element("xpath",'//*[@id="srp-facets"]/div[3]/form/div[2]/div[2]/fieldset/ol/li[2]/div/label/span[1]').click()
            computer_science_btn = driver.find_element("xpath",'//*[@id="srp-facets"]/div[3]/form/div[2]/div[4]/fieldset/ol/li[3]/div/label/span[1]').click()
        
        items_source = driver.page_source
        soup = BeautifulSoup(items_source, 'html.parser')
        
        if (mode == 0):
            pages = math.ceil(int(soup.find('div','searchBox').find('span','num').text.replace(',','')) / 100)
            print("RISS" + keyword)
        if (mode == 1):
            try : pages = math.ceil(int(re.sub(r'[^0-9]','',soup.find('h1','title is-clearfix').text)[4:]) / 200)
            except : pages = 1
            print("arxiv" + keyword)
            
        for i in range(0,pages):
            #해당 페이지 소스 가져오기
            #RISS
            if(mode == 0):
                driver.get(url_forward + str(i*100) + url_backward)
            #arxiv
            if(mode == 1):
                if(i < 50):
                    driver.get(url_forward + url_backward + str(i*200))
                if(i > 49):
                    driver.get(url_forward + url_backward_2 + str((i-50) *200))
                if(i > 99):
                    print("shit i am " + keyword)

            items_source = driver.page_source
            soup = BeautifulSoup(items_source, 'html.parser')
            
            #n개 논문 소스 가져오기
            #RISS
            if(mode == 0) :
                items = soup.find('div','srchResultListW').find_all('div','cont','m160')
            #arxiv
            if(mode == 1) :
                items = soup.find('ol','breathe-horizontal').find_all('li','arxiv-result')
                         
            tLen = len(items)
        
            iCount = 0
            page = i + 1
            for item in items :
                iCount += 1
                if iCount % 20 == 0:
                    print("page [{}/{}] parsing.. [{}/{}]".format(page, pages, iCount, tLen))
            
                title = ''
                
                #riss
                if(mode == 0):
                    try : title = item.find('p','title').text
                    except : title = ''
            
                    date = ''
                    try : 
                        date = item.find('p','etc').find_all('span')
                        date = date[2].text
                    except : date = ''
                
                    abstract = ''
                    try : abstract = item.find('p','preAbstract').text
                    except : continue
                
                #arxiv
                if(mode == 1):
                    try : title = item.find('p','title is-5 mathjax').text.replace('\n','').replace('  ','')
                    except : title = ''
            
                    date = ''
                    try : 
                        date = re.sub(r'[^0-9]','',item.find('p','is-size-7').text)[-4:]
                    except : date = ''
                
                    abstract = ''
                    try : abstract = item.find('span','abstract-full has-text-grey-dark mathjax').text.replace('\n',' ').replace('  ','').replace('△ Less','')
                    except : continue
                
                # if(mode == 0) :
                #     titleL.append(title)
                #     dateL.append(date)
                #     abstractL.append(abstract)
                # if(mode == 1) :
                #     titleL_G.append(title)
                #     dateL_G.append(date)
                #     abstractL_G.append(abstract)
                if(mode == 0) :
                    titleL.append(title)
                    dateL.append(date)
                    abstractL.append(abstract)
                if(mode == 1) :
                    titleL.append(title)
                    dateL.append(date)
                    abstractL.append(abstract)
            
    print("date to .csv file")
    
    resultDict = dict(title = titleL,
                  date = dateL,
                  abstract = abstractL)
    
    # resultDict_G = dict(title = titleL_G,
    #               date = dateL_G,
    #               abstract = abstractL_G)
    
    fName = "C:\\Users\\quite\\Desktop\\Deep_learning_Algorithms\\crawling_"+keyword+".csv"
    # fName_G = "C:\\Users\\quite\\Desktop\\Deep_learning_Algorithms\\crawling_"+keyword+"_G.csv"
    
    DB = pd.DataFrame(resultDict)
    # DB_G = pd.DataFrame(resultDict_G)
    DB.to_csv(fName,encoding='utf-8-sig')
    # DB_G.to_csv(fName_G,encoding = "utf-8-sig")