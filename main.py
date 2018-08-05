"""
Created on Fri Aug  4 19:19:31 2017

@author: aw1042
"""
import urllib.request
import threading
import sys
import re
import os
from xml.etree import ElementTree
import smtplib

argsObj = {}
for arg1, arg2 in zip(sys.argv[:-1], sys.argv[1:]):
    if arg1[0] == '-':
        argsObj[arg1] = arg2

posts = []
requestsNumber = 0

try:
    url = argsObj['-url']
except KeyError:
    print('no url provided, exiting')
    sys.exit()
    

if 'format=rss' not in url:
    url = url + ('?' if '?' not in url else '&') + 'format=rss'
print('set url to ' + url)

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
    req = urllib.request.urlopen(url).read()
    prevLength = len(posts)
    parsedData = ElementTree.fromstring(req)
    for itemTag in parsedData.getchildren():
        appendPost(itemTag)
    if len(posts) > prevLength:
        print('Aggregated', len(posts[prevLength:]), 'new posts')
        emailPosts(posts[prevLength:])
    requestsNumber += 1
    print('Number of requests: ', requestsNumber)

def appendPost(xmlItem):
    postFound = False
    title = xmlItem.getchildren()[0].text
    link = xmlItem.getchildren()[1].text
    description = xmlItem.getchildren()[2].text
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

    fromPass = os.environ['CPOLL_PW']
    fromEmail = os.environ['CPOLL_FROMEMAIL']
    toEmail = os.environ['CPOLL_TOEMAIL']
    server = smtplib.SMTP_SSL()

    server.connect("smtp.gmail.com", 465)
    server.ehlo()
    server.login(fromEmail, fromPass)
    server.sendmail(fromEmail, toEmail, msg.encode('utf-8'))
    server.quit()

requestUrl()
set_interval(requestUrl, pollInterval)
