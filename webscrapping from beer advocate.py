# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import requests

import pandas as pd

#map to store the data per country
countryMap={}

#get the main page html text
source=requests.get('https://www.beeradvocate.com/beer/top-rated/').text
soup=BeautifulSoup(source,'lxml')

#scrape the option bar
countries=soup.find('select').find_all('option')


#for each option in bar
for ite in countries:
    
    #get the acronym of each country for the url
    acr=ite['value']
    country=ite.text
    if (country=='Countries:'):
         country='World'
         
    #url is main page + the acrynom found above
    url='https://www.beeradvocate.com/beer/top-rated/'+acr
    
    # get the html info for each country
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')

    #set the columns for data
    data=pd.DataFrame(columns=['Name','Company','Type Of Beer','Alcohol Percent','Number of Ratings','Average Rating'])
    
    
    #get all beers on the page
    items = soup.find_all('tr')
    index=0
    #print(items[1].prettify())
    
    # for each beer skipping the first one
    for subItems in items[1:]:
        index+=1
        #print(index)
        
        # get all the info per beer
        subItems=subItems.find_all('td')
        
        
        #name
        name=subItems[1].find('b').text
        
        #description of beer including alc percentage and brewery
        descript=subItems[1].find('span')
        
        #get the alc percentage if there is one
        if descript.text.find('%') !=-1:
            
            alcPercent=float(descript.text.split('|')[1].split('%')[0].split(' ')[1])
            
        #get the drewery and type of beer
        temp=descript.find_all('a')
        comp=temp[0].text
        typeOBeer=temp[1].text
        
        #get the number of user ratings
        stringRat=subItems[2].text
        if stringRat.find(',')!=-1:
            stringRat=stringRat.replace(',','')
        numRatings=int(stringRat)
        
        #get the average rating of each beer
        avgRating=float(subItems[3].text)
        data=data.append({'Name':name,'Company':comp,'Type Of Beer':typeOBeer,'Alcohol Percent':alcPercent,'Number of Ratings':numRatings,'Average Rating':avgRating}, ignore_index=True)
    
    print(data.tail())
    
    #add data to country map and write to a csv file
    countryMap[country]=data
    data.to_csv(country+'.csv',index=False)



