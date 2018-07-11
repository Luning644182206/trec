# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import re,urllib.parse,urllib.request,urllib.error
from bs4 import BeautifulSoup as BS
import requests
from nltk.corpus import stopwords

class GetNews:
    newsURL = ''

    def __init__(self, url):
        self.newsURL = url

    def getNews(self):
        try:
            html = requests.get(self.newsURL)
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
            print (text)
        except urllib.error.HTTPError as e:
              print(e.code)
        except urllib.error.URLError as e:
              print(e.reason)