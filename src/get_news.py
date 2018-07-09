# coding=utf8
# Created on June 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

import re,urllib.parse,urllib.request,urllib.error
from bs4 import BeautifulSoup as BS
import requests

class GetNews:
    newsURL = ''

    def __init__(self, url):
        self.newsURL = url

    def getnNews(self):
        try:
            html = requests.get(self.newsURL)
            soup = BS(html.text, 'html.parser')
            head = soup.find('head')
            head.decompose()
            header = soup.find('header')
            header.decompose()
            footer = soup.findAll('footer')
            length = len(footer)
            footer = footer[length - 1]
            footer.decompose()
            content = soup.get_text().encode(encoding='UTF-8',errors='strict')
            print (content.strip().split())
            # for line in content.readlines():
            #     # if (line.get_text() != ''):
            #     print line
        except urllib.error.HTTPError as e:
              print(e.code)
        except urllib.error.URLError as e:
              print(e.reason)