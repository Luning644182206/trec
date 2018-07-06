# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('/Users/luning04/work/trec/src')
import urllib
import urllib2
import re
from get_news import *
from bs4 import BeautifulSoup as BS
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

class FoxNewsSearch:
    keyWords = ''
    baseUrl = 'http://www.foxnews.com/search-results/search?'
    query = {}
    # searchUrl = ''
    results = []
    perPage = 0
    newsNum = 0
    times = 0

    '''
    init:       初始化数据
    Input:      words     要初始化的数据
    Output:     none
    others:     none
    '''
    def __init__(self, words, num):
        # 默认每页10个
        self.perPage = 10
        self.newsNum = num
        self.keyWords = words
        self.times = num/self.perPage
    
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
        querys = urllib.urlencode(self.query)
        # 处理分页的情况
        startNum = str(time * self.perPage)
        # 攒URL
        searchUrl = self.baseUrl + querys + '&ss=fn&start=' + startNum
        return searchUrl

    '''
    search:     爬虫
    Input:      none
    Output:     none
    others:     none
    '''
    def search(self):
        options = Options()
        options.add_argument('-headless')  # 无头参数
        driver = Firefox(executable_path='./third_party/geckodriver', firefox_options = options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
        wait = WebDriverWait(driver, timeout = 5)
        for index in range(self.times):
            searchUrl = self.createURL(index)
            driver.get(searchUrl)
            wait.until(expected.visibility_of_element_located((By.CLASS_NAME, 'num-found')))
            soup = BS(driver.page_source, 'html.parser')
            # 找到每条新闻块
            news = soup.findAll(class_= 'search-directive')
            for new in news:
                result = {
                    'url': '',
                    'title': ''
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
        # print self.results
        driver.quit()
        # try:
        #     html = urllib2.urlopen(self.searchUrl)
        #     soup = BS(html, 'html.parser')
        #     td = soup.findAll('h2')
        #     count = soup.findAll(class_="sb_count")
        #     for c in count:
        #         print(c.get_text())

        #     for t in td:
        #         print(t.get_text())
        #         pattern = re.compile(r'href="([^"]*)"')
        #         h = re.search(pattern,str(t))
        #         if h:
        #             for x in h.groups():
        #                 print(x)
        # except urllib2.HTTPError as e:
        #     print(e.code)
        # except urllib2.URLError as e:
        #     print(e.reason) 


if __name__ == "__main__":
    a = FoxNewsSearch('donate money', 20)
    a.search()
    b = GetNews(a.results[0]['url'])
    b.getnNews()
# a = []
# a = ['SD卡稍等', '大萨达所']
# print str(a).decode("string_escape")
# for item in a:
#     print item
# urllib2.parse.urlencode('a')