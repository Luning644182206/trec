# coding=utf8
# Created on July 11, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('./class')
from search import NewsSearch
from get_news import GetNews

if __name__ == "__main__":
    a = NewsSearch('foxNews', 'donate money', 20)
    a.search()
    b = GetNews(a.website, a.keyWords, a.results)
    b.getNews()