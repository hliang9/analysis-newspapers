#!/usr/bin/env python3
import NYT
import sys
import requests
import Newspaper
import USAToday
import WSJ

f=open("apikeys.txt", "r")
lines = f.readlines()
newsapi = lines[0] #first line in text file is News API key
nytapi = lines[1]  #second line in text file is NYT API key

"""
Testing NYT
"""
articleURLs = NYT.getTopStoriesNYT(sys.argv[1], nytapi)
print("Number of articles: " + str(len(articleURLs)))
allSources = []
for link in articleURLs:
    list = NYT.obtain_links_NYT(link)
    allSources = allSources + list
Newspaper.printCategorizedSources(allSources)
print("Number of self-links: " + str(Newspaper.countSelfReference('NYT', allSources)))



# """
# Testing USAToday
# """
# excludedList = ['https://www.usatoday.com/in-depth/news/investigations/deadly-deliveries/2018/07/26/preeclampsia-high-blood-pressure-maternal-mortality-rates/546966002', 'https://www.usatoday.com/in-depth/news/investigations/deadly-deliveries/2018/07/26/maternal-mortality-rates-preeclampsia-postpartum-hemorrhage-safety/546889002']
# articleURLs = USAToday.getTopStoriesUSA(newsapi)
# allSources = []
# for link in articleURLs:
#     if link not in excludedList:
#         list = USAToday.obtain_links_USA(link)
#     if list != None and len(list) > 0:
#         allSources = allSources + list
# Newspaper.printCategorizedSources(allSources)
# print("Number of self-links: " + str(Newspaper.countSelfReference('USA', allSources)))


# """
# Testing WSJ
# """
# 
# articleURLs = WSJ.getTopStoriesWSJ(newsapi)
# allSources = []
# for link in articleURLs:
#     list = WSJ.obtain_links_WSJ(link)
#     if list != None and len(list) > 0:
#         allSources = allSources + list
# 
# Newspaper.printCategorizedSources(allSources)
# print("Percentage of self-links: " + str(Newspaper.countSelfReference('WSJ', allSources)/len(allSources)))

