# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 18:25:45 2021

@author: Anurag.Mittal
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 18:49:45 2020

@author: Anurag.Mittal
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

 

url = 'https://www.komparify.com/entertainment/movies?languagelist=hindi&contenttypelist=movie&minyear=1989&maxyear=2019&sortorder=kscore&elements=3000'
headers = {'User-Agent': 'Chrome/74.0.3729.169'}
response = requests.get(url, headers=headers ,timeout = 600000)
soup = BeautifulSoup(response.text,'lxml')
    
pages = soup.find('div',class_='card-holder')
print(pages)

links = pages.find_all('a',class_='card-lt')

urls = []
for link in links:
        x = link.get('href')
        urls.append(x)
print(urls)
len(urls)

rows = []
url = 'https://www.komparify.com/'
num = 0
for num in range(0,3040):
    try:        
        newUrl = url + urls[num]
        Movie = urls[num].split('/')[3]
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.text,'lxml')
        items = soup.find_all('div',class_='rate_score ratall')
        if (items != []):
            Box_office = items[0].find('span',class_="r_score").text.strip('\n').split('\n')[1]
        
        items = soup.find_all('div',class_='cnt-det')
        items1 = items[4].find_all('div',class_='tinfo')
        Certificate = "" ; Release_Date = "" ; Run_Time= "" ; Budget = ""; Genre = ""
        for i in items1:
            str = i.text.strip('\n')
            if (Certificate == ""):
                Certificate = str.split('\n')[1] if (str.find('Certificate') != -1) else ""
            if (Release_Date == ""):
                Release_Date = str.split('\n')[1] if (str.find('Release Date') != -1) else ""
            if (Run_Time == ""):
                Run_Time = str.split('\n')[1] if (str.find('Run Time') != -1) else ""
            if (Budget == ""):
                Budget = str.split('\n')[2] if (str.find('Budget') != -1) else ""
            if (Genre == ""):
                Genre = str.strip('\n').replace('\n', "").replace('Genre', "") if (str.find('Genre') != -1) else ""
                    
        items = soup.find_all('div',class_='dir_cc ewit')
        Producer = "";    Director = "";    Lead_Actor1 = "";Lead_Actor2 = "";Lead_Actor3 = ""
        if (items != []):
    #        i = items[0]
            for i in items:
                str = i.find('span',class_='name').text
                if (Director == ""):
                    Director = str.strip('\n').split('\n')[0] if (str.find('Director') != -1) else ""
                if (Producer == ""):
                    Producer = str.strip('\n').split('\n')[0] if (str.find('Producer') != -1) else ""
                if (Director != ""):
                    Lead_Actor1 = items[1].find('span',class_='name').text.strip('\n').split('\n')[0]
                    if (len(items) > 2):
                        Lead_Actor2 = items[2].find('span',class_='name').text.strip('\n').split('\n')[0]
                    if (len(items) > 3):
                        Lead_Actor3 = items[3].find('span',class_='name').text.strip('\n').split('\n')[0]
                else:
                    Lead_Actor1 = items[0].find('span',class_='name').text.strip('\n').split('\n')[0]                
                    if (len(items) > 1):
                        Lead_Actor2 = items[1].find('span',class_='name').text.strip('\n').split('\n')[0]                
                    if (len(items) > 2):
                        Lead_Actor3 = items[2].find('span',class_='name').text.strip('\n').split('\n')[0]                
                    
        rows.append([Movie,Box_office,Certificate,Release_Date,Run_Time,Budget,Genre,
                         Director,Producer,Lead_Actor1,Lead_Actor2,Lead_Actor3])
    except:
        pass
rows[1:10]
Movie_df = pd.DataFrame(rows, columns=["Movie", "Box_office","Certificate",
                                       "Release_Data","Run_time","Budget",
                                       "Genre","Director","Producer","Lead_Actor1","Lead_Actor2","Lead_Actor3"])

Movie_df.to_csv("~Analysis\\data5.csv", index = False)
    