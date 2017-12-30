"""
Created on Fri Aug  4 19:19:31 2017

@author: aw1042
"""
import requests
import threading
import sys
import re
import xml.etree.ElementTree as ET
import smtplib
from credentials import *



argsObj = {}
for arg1, arg2 in zip(sys.argv[:-1], sys.argv[1:]):
    if arg1[0] == '-':
        argsObj[arg1] = arg2

posts = []
requestsNumber = 0
try:
    url = argsObj['-url']
except AttributeError:
    url = 'http://denver.craigslist.org/search/sss?format=rss'

if 'format=rss' not in url:
    url = url + ('?' if '?' not in url else '&') + 'format=rss'
print 'set url to ' + url

pollInterval = 900


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
    req = requests.get(url)
    cdata = req.content.strip()
    prevLength = len(posts)
    parsedData = ET.fromstring(cdata)
    for itemTag in parsedData:
        appendPost(itemTag)
    print len(posts), prevLength
    if len(posts) > prevLength and requestsNumber > 0:
        print 'Aggregated', len(posts[prevLength:]), 'new posts'
        emailPosts(posts[prevLength:])
    requestsNumber += 1
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
    if not postFound and not re.match('craigslist.+\|.+search', newPost.title):
        posts.append(newPost)
    

def emailPosts(newPostsArray):
    msg = ''
    for post in newPostsArray:
        msg += post.title + '\n'
        if (post.description):
            msg += post.description + '\n'
        msg += post.link + '\n  \n \n'

    toPass = password
    server = smtplib.SMTP_SSL()
    server.connect("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email, toPass)    
    server.sendmail(email, email, msg.encode('utf-8'))
    server.quit()

requestUrl()
set_interval(requestUrl, pollInterval)