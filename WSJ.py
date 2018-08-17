#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import re
import requests
import json

"""
Returns BeautifulSoup object given a link
"""
def getSoupObject(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'referer': 'https://l.facebook.com/'})
    webpage = urlopen(req).read()
    return BeautifulSoup(webpage, "lxml")
    #html = urllib.request.urlopen(url)
    #return BeautifulSoup(html, "lxml")

"""
https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal&apiKey=3b9ec6743226409aa00c0787a01d42e8
"""
def getTopStoriesWSJ(wsjapi):
    base = "https://newsapi.org/v2/top-headlines"
    PARAMS = {"sources" : "the-wall-street-journal", "apiKey" : ""} #WSJ API Key here
    responseObject = requests.get(url = base, params = PARAMS)
    jsonObject = responseObject.json()
    articles = jsonObject['articles']
    links = []
    for article in articles:
        links.append(article['url'])
    return links

def obtain_links_WSJ(url):
    pattern = re.compile("mailto:")
    soup = getSoupObject(url)
    excludedLinks = []
    links = []
    a_tags = []
    articleBody = soup.find(itemprop="articleBody")
    if articleBody == None:
        print("cannot find article body for this url: " + url)
    p_tags = articleBody.find_all("p")
    for p_tag in p_tags:
        a_tags = a_tags + p_tag.find_all("a")
    if len(a_tags) > 0:
        for a in a_tags:
            if pattern.search(a.get('href')) == None:
                links.append(a.get('href'))
    links = links + getTwitterTweetsfromWSJ(soup)
    return links
            
def getTwitterTweetsfromWSJ(soup):
    URLs = []
    tweet_tags = soup.find_all("blockquote", "twitter-tweet")
    for tag in tweet_tags:
        link = tag.find("a")
        URLs.append(link.get('href'))
    return URLs
