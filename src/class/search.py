# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('/Users/whs/work/trec-master/src')
import re, urllib.parse, urllib.request, urllib.error
import socks
import socket
import requests
from get_news import *
from bs4 import BeautifulSoup as BS
from driver_common import *
from search_twitter import *

class NewsSearch:
    keyWords = ''
    baseUrl = ''
    query = {}
    results = []
    perPage = 0
    newsNum = 0
    times = 0
    website = ''
    websiteBaseURL = {
        'foxNews': 'http://www.foxnews.com/search-results/search?',
        'bbcNews': 'https://www.bbc.co.uk/search/more?page=',
        'twitterNews': ''
    }
    classType = ''

    '''
    init:       初始化数据
    Input:      website   爬取的网站
                words     要爬的新闻关键字
                num       要爬取的篇数
    Output:     none
    others:     none
    '''
    def __init__(self, website, type, words, num):
        # 默认每页10个
        self.perPage = 10
        self.newsNum = num
        self.keyWords = words
        self.times = num/self.perPage
        self.baseUrl = self.websiteBaseURL[website]
        self.website = website
        self.classType = type

    '''
    createURL:  URL
    Input:      time 目前是第几次
    Output:     none
    others:     none
    ''' 
    def createURL(self, time,website):
        # UTF-8编码 错误处理方式是直接报错
        keyWordsEncode = self.keyWords.encode(encoding='UTF-8',errors='strict')
        # bing查询默认query字段是q
        self.query['q'] = keyWordsEncode
        # 把query放在url里面，query=xxx  python2和3表达式有区别
        querys = urllib.parse.urlencode(self.query)
        # 处理分页的情况
        if website == 'foxNews': # 判断是bbc还是fox
            startNum = str((time * self.perPage)) 
            searchUrl = self.baseUrl + querys +'&ss=fn&start='+startNum
        else:
            startNum = str(time+1) # page从1开始，time从0开始
            keyWords='+'.join(self.keyWords.split()) # bbc的查询空格转换为+号
            searchUrl = self.baseUrl + startNum + '&q=' + keyWords + '&sa_f=search-product&filter=news&suggid='
        return searchUrl

    '''
    bbcNewsSearch:     bbcNews爬虫
    Input:             none
    Output:            none
    others:            none
    '''
    def bbcNewsSearch(self): # 搜索bbc新闻
        bbcDriver = DriverCommon() # 生成一个driver对象
        for index in range(int(self.times)):
            try:
                searchUrl = self.createURL(index,self.website)
                print(searchUrl)
                bbcDriver.driver.get(searchUrl)
                #bbcDriver.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'search-results')))
                # 用标签li data-result number="xxx" 定位，但是不知道如何写
                soup = BS(bbcDriver.driver.page_source, 'html.parser')
                #print (soup.prettify())
                # 找到每条新闻块
                news = soup.findAll('li',attrs={'data-result-number=':''})
                print(len(news)) # 判断找到了几个，一个为失败
                for new in news: # 大循环为ol块（页数）的循环，下面操作跟foxnews一致
                    newBranch = new.findAll(class_='has_image media-text') # 还有media-text先不采用
                    for content in newBranch:
                        result = {
                            'title': '',
                            'url': ''
                        } 
                        h1Text = content.find('h1')
                        title = h1Text.get_text()
                        result['title'] = title
                    # URL 正则
                        urlRE = re.compile(r'href="([^"]*)"')
                        urls = re.search(urlRE, str(h1Text))
                    # 找URL
                        if urls:
                            for url in urls.groups():
                                result['url'] = url
                        if (result['url'] != ''):
                            print(result) # 在终端打印结果 可以注释掉
                            self.results.append(result)
            except:
                print('error in search')
        bbcDriver.driver.quit()

    '''
    foxNewsSearch:     foxNews爬虫
    Input:             none
    Output:            none
    others:            none
    '''
    def foxNewsSearch(self): # 搜索火狐的新闻
        foxDriver = DriverCommon()
        for index in range(int(self.times)):
            try:
                searchUrl = self.createURL(index, self.website)
                print(searchUrl)
                foxDriver.driver.get(searchUrl)
                foxDriver.wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'num-found')))
                soup = BS(foxDriver.driver.page_source, 'html.parser')
                # 找到每条新闻块
                news = soup.findAll(class_= 'search-directive')
                for new in news:
                    result = {
                        'title': '',
                        'url': ''
                    }
                    # 找标题
                    if new.find('h3'):
                        title = new.find('h3').get_text()
                        result['title'] = title
                    # URL 正则
                    urlRE = re.compile(r'href="([^"]*)"')
                    urls = re.search(urlRE, str(new))
                    # 找URL
                    if urls:
                        for url in urls.groups():
                            result['url'] = url
                    if (result['url'] != ''):
                        self.results.append(result)
            except:
                print('error in search')
        foxDriver.driver.quit()

    '''
    TwitterNewsSearch:     twitterNews爬虫
    Input:                 none
    Output:                none
    others:                none
    '''
    def twitterNewsSearch(self):
        twitterNews = SearchTwitter(self.keyWords, self.newsNum)
        datas = twitterNews.search()
        self.results = datas

    '''
    search:     爬虫
    Input:      none
    Output:     none
    others:     none
    '''
    def search(self):
        # 动态选择爬虫函数，爬虫函数命名规则为website + Search
        eval('self.' + self.website + 'Search')()