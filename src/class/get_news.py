# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import re, urllib.parse, urllib.request, urllib.error
import requests
import csv
from bs4 import BeautifulSoup as BS
from nltk.corpus import stopwords

class GetNews:
    newsURLs = []
    keyWords = ''
    website = ''

    '''
    init:       初始化数据
    Input:      website   爬取的网站
                words     要爬的新闻关键字
                URLs      链接
    Output:     none
    others:     none
    '''
    def __init__(self, website, words, URLs):
        self.newsURLs = URLs
        self.keyWords = words
        self.website = website

    '''
    getNews:    爬文章
    Input:      none
    Output:     none
    others:     none
    '''
    def getNews(self):
        if self.website =='bbcNews':
            for item in self.newsURLs:
                try:
                    html = requests.get(item['url'])
                    soup = BS(html.text, 'html.parser')
                    # 把script都删除
                    [scriptPart.extract() for scriptPart in soup('script')]
                    # 把header和footer删除
                    head = soup.find('head')
                    head.decompose()
                    footer = soup.findAll('footer')
                    length = len(footer)
                    footer = footer[length - 1]
                    footer.decompose()
                    # 拿到内容
                    # content = soup.get_text().decode('UTF-8',errors='strict')
                    content = soup.get_text()
                    # 去停止词
                    text = ' '.join([word for word in content.strip().split() if word not in stopwords.words("english")])
                    # stripContent = text.strip().split()
                    # print (text)
                    # 保存
                    item['content'] = text
                    self.saveNews(item)
                except urllib.error.HTTPError as e:
                      print(e.code)
                except urllib.error.URLError as e:
                      print(e.reason)
        else :
            for item in self.newsURLs:
                try:
                    html = requests.get(item['url'])
                    soup = BS(html.text, 'html.parser')
                    # 把header和footer删除
                    head = soup.find('head')
                    head.decompose()
                    header = soup.find('header')
                    header.decompose()
                    footer = soup.findAll('footer')
                    length = len(footer)
                    footer = footer[length - 1]
                    footer.decompose()
                    # 拿到内容
                    # content = soup.get_text().decode('UTF-8',errors='strict')
                    content = soup.get_text()
                    # 去停止词
                    text = ' '.join([word for word in content.strip().split() if word not in stopwords.words("english")])
                    # stripContent = text.strip().split()
                    # print (text)
                    # 保存
                    item['content'] = text
                    self.saveNews(item)
                except urllib.error.HTTPError as e:
                      print(e.code)
                except urllib.error.URLError as e:
                      print(e.reason)
        print('表格存储成功')


    '''
    saveNews:   保存文章
    Input:      none
    Output:     none
    others:     none
    '''
    def saveNews(self, news):
        # 文件的路径 命名方式参看公式即可
        filePath = './data/' + self.website + '_' + '_'.join(self.keyWords.split()) +  '_news.csv'
        file = open(filePath, 'a+')
        titleName = ['title','url', 'content']
        writer = csv.DictWriter(file, fieldnames = titleName)
        writer.writerow(news)