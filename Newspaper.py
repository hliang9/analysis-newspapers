#!/usr/bin/env python3
import re
import json
########################### METHODS ###################################

"""
Prints out the sources, categorized.
Parameter: List of source links and BeautifulSoup object
"""

def printCategorizedSources(links):
    print("List of links: ")
    official = 0
    social_media = 0
    trusted = 0
    sometimes_trusted = 0
    other = 0
    for link in links:
        #print(link)
        if is_trusted_newspaper(link):
            trusted += 1
        elif is_social_media(link):
            social_media += 1
        elif is_official_source(link):
            official += 1
        elif is_sometimes_trusted_newspaper(link):
            sometimes_trusted += 1
        else:
            other += 1
    dict = {'Government, University, or Organization': official, 'Social Media':social_media, 'Trusted Newspapers':trusted, 'Sometimes Newspapers': sometimes_trusted, 'Other':other}
            
    print("Number of edu/gov/org links: \n" + str(official))
    print("Number of social media links: \n" + str(social_media))
    print("Number of trusted newspapers: \n" + str(trusted))
    print("Number of sometimes trusted newspapers: \n" + str(sometimes_trusted))
    print("Number of other sources: \n" + str(other))
    
    
"""
Returns true if url belongs to social media site (Twitter, Facebook, Youtube, Reddit, or Instagram)
Parameter: URL
"""
def is_social_media(link):
    pattern = re.compile("(www\.|(https*:\/\/))(twitter\.com|facebook\.com|youtube\.com|reddit\.com|instagram\.com)")
    if pattern.search(link):
        return True
    else:
        return False

"""
Returns true if the link is .edu, .gov, .org 
Parameter: url
"""

def is_official_source(url):
    pattern = re.compile("\.(edu|gov|org)")
    if pattern.search(url):
        return True
    else:
        return False
        
"""
Given an url, returns either True if the url is of a trusted or False otherwise
Trusted is defined as "More trusted than distrusted" according to
http://www.journalism.org/2014/10/21/section-1-media-sources-distinct-favorites-emerge-on-the-left-and-right/
Only recognizes newspaper urls based in the United States. Will not recognize other country
versions of a newspaper such as bbc.co.uk
Exception: news.google is not recognized since it links to other newspapers and is not a newspaper itself
"""
def is_trusted_newspaper(url):
    pattern = re.compile("(www\.|(https*:\/\/))(economist\.com|bbc\.com|npr\.org|pbs\.org|wsj\.com|quotes\.wsj\.com|abcnews\.go\.com|cbsnews\.com|nbcnews\.com|cnn\.com|usatoday\.com|theblaze\.com|nytimes\.com|washingtonpost\.com|msnbc\.com|theguardian\.com|bloomberg\.com|newyorker\.com|politico\.com|yahoo\.com|foxnews\.com)")
    if pattern.search(url):
        return True
    return False

"""
Given an url, returns either True if the url is of a "sometimes trusted" newspaper, False otherwise
Sometimes trusted is defined as "About equally trusted and distrusted" according to
http://www.journalism.org/2014/10/21/section-1-media-sources-distinct-favorites-emerge-on-the-left-and-right/
Exception: The Drudge Report is omitted since it only gathers news from other newspapers
"""
def is_sometimes_trusted_newspaper(url):
    pattern = re.compile("(www.|(https*:\/\/))(motherjones\.com|slate\.com|breitbart\.com|huffingtonpost\.(com|co\.uk)|cc\.com|thinkprogress\.org)")
    if pattern.search(url):
        return True
    return False

def is_NYT(url):
    pattern = re.compile("(www.|(https*:\/\/))(nytimes\.com)")
    if pattern.search(url):
        return True
    return False

def is_WSJ(url):
    pattern = re.compile("(www.|(https*:\/\/))(wsj\.com|quotes\.wsj\.com)")
    if pattern.search(url):
        return True
    return False

def is_USAToday(url):
    pattern = re.compile("(www.|(https*:\/\/))(usatoday\.com)")
    if pattern.search(url):
        return True
    return False

def countSelfReference(name, links):
    count = 0
    if name == 'USA':
        for link in links:
            if is_USAToday(link):
                count = count + 1
    elif name == 'NYT':
        for link in links:
            if is_NYT(link):
                count = count + 1
    elif name == 'WSJ':
        for link in links:
            if is_WSJ(link):
                count = count + 1
    return count
"""
DEPRECATED
----------------
Extracts the links to sources in an article
Parameter: url string
Returns: list of links in the article

def getLinks(url):
   #  html = urlopen(url) soup = BeautifulSoup(html)
   # #new list: listOfLinks
   #  for link in soup.findAll('each', attrs={'href': re.compile("^http://")}):
   #      print link.get('href')
    print("i'm running")
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    links = []
    print("got here")
    excludedLinks = ["http://on.fb.me/1paTQ1h", "http://nyti.ms/1MbHaRU"] #sign up for NYT newsletter and like the science times links
    
    #bracketAdLinks = soup.find_all(re.compile("[strongemaLike the Science Times page on Facebook.]"))
    #print(bracketAdLinks)
        #bracketAdLinks.append(adLink.get('href'))
        
    for link in soup.find_all("a", rel="noopener noreferrer"):
        if link.get('href') not in excludedLinks:
            links.append(link.get('href'))
    
    links = links[3 : len(links) - 3] #get rid of article sharing links
    return links
"""