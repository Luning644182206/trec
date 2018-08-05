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
    proxies = {
        'http': 'http://127.0.0.1:1087',
        'https': 'https://127.0.0.1:1087'
    }
    classType = ''

    '''
    init:       初始化数据
    Input:      website   爬取的网站
                words     要爬的新闻关键字
                URLs      链接
    Output:     none
    others:     none
    '''
    def __init__(self, website, type, words, URLs):
        self.newsURLs = URLs
        self.keyWords = words
        self.website = website
        self.classType = type


    '''
    getNews:    爬文章
    Input:      none
    Output:     none
    others:     none
    '''
    def getNews(self):
        if (self.website =='bbcNews'):
            for item in self.newsURLs:
                try:
                    html = requests.get(item['url'], proxies = self.proxies, timeout = 10)
                    soup = BS(html.text, 'html.parser')
                    # 把图片都删了
                    figure = soup.find('figure')
                    if (figure != None):
                        figure.decompose()
                    # 把script都删除
                    [scriptPart.extract() for scriptPart in soup('script')]
                    content = soup.find(class_='story-body__inner')
                    if (content != None):
                        # 拿到内容
                        content = content.get_text()
                        # 去停止词
                        text = ' '.join([word for word in content.strip().split() if word not in stopwords.words("english")])
                        # 保存
                        item['content'] = content
                        self.saveNews(item, True)
                except:
                    print('save faild')
                    self.saveNews(item, False)
        elif (self.website =='foxNews') :
            for item in self.newsURLs:
                try:
                    html = requests.get(item['url'])
                    soup = BS(html.text, 'html.parser')
                    # 把script都删除
                    [scriptPart.extract() for scriptPart in soup('script')]
                    # 拿到内容
                    content = soup.find(class_='article-text')
                    if (content == None):
                        content = soup.find(class_='article-content')
                        if (content != None):
                            content = content.get_text()
                            # 保存
                            item['content'] = content
                            self.saveNews(item, True)
                except:
                    print('save faild')
                    self.saveNews(item, False)
        else:
            # 处理twitter
            for item in self.newsURLs:
                # 保存
                self.saveNews(item, True)
        print('表格存储成功')


    '''
    saveNews:   保存文章
    Input:      none
    Output:     none
    others:     none
    '''
    def saveNews(self, news, type):
        filePath = ''
        if (type):
        # 文件的路径 命名方式参看公式即可
            filePath = './data/news/' + self.website + '_' + self.classType + '_' + '_'.join(self.keyWords.split()) +  '_news.csv'
        else:
            filePath = './data/faild.csv'
        file = open(filePath, 'a+')
        # 文件的头
        titleName = []
        if (self.website == 'twitterNews'):
            titleName = ['name', 'content', 'retweeted', 'created_at']
        else:
            titleName = ['title','url', 'content']
        writer = csv.DictWriter(file, fieldnames = titleName)
        writer.writerow(news)