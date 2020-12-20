# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 11:36:22 2020

@author: matt hanson
"""
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#get the names of the country to find the csv files already made
countryMap={}
source=requests.get('https://www.beeradvocate.com/beer/top-rated/').text
soup=BeautifulSoup(source,'lxml')
countries=soup.find('select').find_all('option')


#get data from csv files
for ite in countries:
    acr=ite['value']
    country=ite.text
    if (country=='Countries:'):
         country='World'
    countryMap[country]=pd.read_csv(country+'.csv')
    #print(countryMap[country].tail())
    
newMap={}

#get the alc percentage to be graphed
for country in countryMap.keys():
    newMap[country]=countryMap[country]['Alcohol Percent'].mean()
    #print(newMap[country])


#set values to be graphed x is the country and y is alc percent
x=[] 
y=[]
for val in newMap.keys():
    x.append(val)
    y.append(newMap[val])



figure, axis = plt.subplots(figsize=(20, 10))  
  
#set width and where the country labels are
width = 0.8 
indent = np.arange(len(y))
axis.barh(indent, y, width, color="blue")

#set where the ticks are
axis.set_yticks(indent+width/2-0.4)
axis.set_yticklabels(x, minor=False)

#set titles
plt.title('Average Alcohol Percentage of Favorite Beer by Country')
plt.xlabel('Alcohol Percentage')
plt.ylabel('Country')      


plt.show()