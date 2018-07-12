# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('/Users/whs/work/trec-master/src')
import re, urllib.parse, urllib.request, urllib.error
import requests
from bs4 import BeautifulSoup as BS
from get_news import *
from bs4 import BeautifulSoup as BS
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

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
        'bbcNews': 'https://www.bbc.co.uk/search?' 
    }

    '''
    init:       初始化数据
    Input:      website   爬取的网站
                words     要爬的新闻关键字
                num       要爬取的篇数
    Output:     none
    others:     none
    '''
    def __init__(self, website, words, num):
        # 默认每页10个
        self.perPage = 10
        self.newsNum = num
        self.keyWords = words
        self.times = num/self.perPage
        self.baseUrl = self.websiteBaseURL[website]
        self.website = website

    '''
    createURL:  URL
    Input:      time 目前是第几次
    Output:     none
    others:     none
    ''' 
    def createURL(self, time):
        # UTF-8编码 错误处理方式是直接报错
        keyWordsEncode = self.keyWords.encode(encoding='UTF-8',errors='strict')
        # bing查询默认query字段是q
        self.query['q'] = keyWordsEncode
        # 把query放在url里面，query=xxx  python2和3表达式有区别
        querys = urllib.parse.urlencode(self.query)
        # 处理分页的情况
        startNum = str(time * self.perPage)
        # 攒URLhttps://www.bbc.co.uk/search?q=ss&sa_f=search-product&scope=
        searchUrl = self.baseUrl + querys + '&sa_f=search-product&filter=news&suggid=#page='+startNum
        return searchUrl

    '''
    foxNewsSearch:     foxNews爬虫
    Input:             none
    Output:            none
    others:            none
    '''
    def bbcNewsSearch(self):#偷懒只改了函数名
        options = Options()
        options.add_argument('-headless')  # 无头参数
        driver = Firefox(executable_path='./third_party/geckodriver', firefox_options = options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        wait = WebDriverWait(driver, timeout = 30)#设置成30
        for index in range(int(self.times)):
            searchUrl = self.createURL(index)
            driver.get(searchUrl)
            wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'num-found')))
            soup = BS(driver.page_source, 'html.parser')
            # 找到每条新闻块
            news = soup.findAll(class_= 'has_image media-text')
            for new in news:
                result = {
                    'title': '',
                    'url': ''
                }
                # 找标题
                if new.find('h1'):#这里是h1
                    title = new.find('h1').get_text()
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
        driver.quit()

    '''
    search:     爬虫
    Input:      none
    Output:     none
    others:     none
    '''
    def search(self):
        # 动态选择爬虫函数，爬虫函数命名规则为website + Search
        eval('self.' + self.website + 'Search')()