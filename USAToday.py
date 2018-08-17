#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import re
import requests
import json

"""
Returns BeautifulSoup object given a link
"""
def getSoupObject(url):
    html = urllib.request.urlopen(url)
    return BeautifulSoup(html, "lxml")


def getTopStoriesUSA(api_key):
    base = "https://newsapi.org/v2/top-headlines"
    PARAMS = {"sources" : "usa-today", "apiKey" : ""}
    responseObject = requests.get(url = base, params = PARAMS)
    jsonObject = responseObject.json()
    #print("results number: " + str(jsonObject['totalResults']))
    articles = jsonObject['articles']
    links = []
    for article in articles:
        links.append(article['url'])
    return links
    
def obtain_links_USA(url):
    soup = getSoupObject(url)
    excludedLinks = []
    links = []
    pattern = re.compile("www.|http:\/\/|https:\/\/")
    articleBody = soup.find(itemprop = 'mainEntity articleBody')
    if articleBody == None:
        articleBody = soup.find(itemprop = 'articleBody')
        print(url)
    unwanted_p = soup.find_all(attrs={"class": "exclude-from-newsgate"})
    for p_tag in unwanted_p:
        p_tag.decompose()
   
    for child in articleBody.children:
        if child.name == 'p': # and child.get('class') != None and child['class'] == ['p-text']:
            #extra links you don't want, delete
            a_tags = child.find_all("a")
            if len(a_tags) > 0: 
                for link in a_tags:
                    sourceLink = link.get('href')
                    if sourceLink not in excludedLinks:
                        if pattern.match(sourceLink) == None:
                            sourceLink = "https://www.usatoday.com" + sourceLink
                        links.append(sourceLink)
                        #print(sourceLink)
    return links
