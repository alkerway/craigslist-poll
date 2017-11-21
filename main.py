# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 19:19:31 2017

@author: aw1042
"""
import requests
import threading
import sys
import xml.etree.ElementTree as ET



argsObj = {}
for arg1, arg2 in zip(sys.argv[:-1], sys.argv[1:]):
    if arg1[0] == '-':
        argsObj[arg1] = arg2

posts = []
requestsNumber = 0
try:
    pollInterval = argsObj['-i']
except AttributeError:
    pollInterval = 60
print 'set poll interval to ' + str(pollInterval)

try:
    url = argsObj['-url']
except AttributeError:
    url = 'http://denver.craigslist.org/search/sss?format=rss'
if 'format=rss' not in url:
    url = url + ('?' if '?' not in url else '&') + 'format=rss'
print 'set url to ' + url


searchQuery = ''
searchCategoryCode = 'zip'


class Post():
    title = ''
    link = ''
    description = ''
    def __init__(self, title, link, description):
        self.title = title
        self.link = link
        self.description = description

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def requestUrl():
    global requestsNumber
    global url
    requestsNumber = requestsNumber + 1
    req = requests.get(url)
    cdata = req.content.strip()
    parsedData = ET.fromstring(cdata)
    for itemTag in parsedData:
        appendPost(itemTag)
    print 'Number of requests: ', requestsNumber

def appendPost(xmlItem):
    postFound = False
    title = xmlItem[0].text
    link = xmlItem[1].text
    description = xmlItem[2].text
    newPost = Post(title, link, description)
    for post in posts:
        if newPost.link == post.link:
            postFound = True
    if not postFound:
        print 'New post found', newPost.title, newPost.link
        posts.append(newPost)

requestUrl()
# set_interval(requestUrl, pollInterval)