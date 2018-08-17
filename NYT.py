#!/usr/bin/env python3
import bs4 #import BeautifulSoup to data scrape
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

"""
Returns: a list of links, each link is an article in the top stories section
Parameter: section as defined by https://developer.nytimes.com/top_stories_v2.json#/Documentation. Example: home, world
The sample URL is http://api.nytimes.com/svc/topstories/v2/{section}.{response-format}?api-key={your-api-key}
Most viewed: https://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/7.json
"""
def getTopStoriesNYT(section, nytapi):
    # base = "http://api.nytimes.com/svc/topstories/v2/"
    api_key = nytapi
    # URL = base + section + "." + "json"
    URL = 'https://api.nytimes.com/svc/mostpopular/v2/mostviewed/all-sections/30.json'
    PARAMS = {'api-key': api_key}
    responseObject = requests.get(url = URL, params = PARAMS)
    #print(responseObject.url)
    jsonObject = responseObject.json()
    #print("printing status" + jsonObject['status'])
    print(jsonObject['num_results'])
    results = jsonObject['results']
    articleURLs = []
    for articleURL in results:
        articleURLs.append(articleURL['url'])

    return articleURLs

"""
Returns: a 2D list, each element is a list of sources for each article in the list 'articles'
Parameter: list of articles
"""
# def getSources(articles):
    

"""
Extracts the links to sources in a New York Times article
Parameter: article URL
Returns: list of links in the article, including twitter tweets
"""

def obtain_links_NYT(url):
    #print(url)
    excludedLinks = ["http://on.fb.me/1paTQ1h", "http://nyti.ms/1MbHaRU", "https://www.nytimes.com/newsletters/offsides"] #sign up for NYT newsletter and like the science times links
    soup = getSoupObject(url)
    links = []
    articleBody = soup.find('article', {'id' : 'story'})
    for child in articleBody.children:
        if child.name == 'div' and child.get('class') != None and child['class'] == ['css-18sbwfn', 'StoryBodyCompanionColumn']:
           # print("found children")
            a_tags = child.find_all("a")
            if len(a_tags) > 0: 
                for link in a_tags:
                    if link.get('href') not in excludedLinks:
                        links.append(link.get('href'))
    #Getting Twitter embed URLs
    links = links + getTwitterTweetsfromNYT(soup)
   # printCategorizedSources(links)
    return links
        
"""
Extracts embedded twitter tweet links from New York Times article.
Used in obtain_links_NYT method
Parameter: BeautifulSoup object
Returns: list of links to tweets
"""
def getTwitterTweetsfromNYT(soup):
    twitter_urls = []
    allScriptTags = soup.find_all('script')
    tag = "" #we want the <script> tag with window.__preloadedData in it
    for script_tag in allScriptTags:
        if 'window.__preloadedData' in str(script_tag): #found the <script> containing twitter urls
            tag = script_tag
            rawString = str(script_tag)
            jsonString = rawString[rawString.index('preloadedData') + 16 : rawString.index('</script>') - 1] #chop off the beginning and end
            jsonObject = json.loads(jsonString)
            for key,val in jsonObject["initialState"].items():
                if "twitterUrl" in val:
                    twitter_urls.append(val['twitterUrl'])                    
            break
    return twitter_urls

