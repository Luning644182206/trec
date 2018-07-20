# coding=utf8
# Created on July 11, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('./class')
from search import NewsSearch
from get_news import GetNews

if __name__ == "__main__":
    a = NewsSearch('bbcNews', 'donate money', 200)
    a.search()
    b = GetNews(a.website, a.keyWords, a.results)
    b.getNews()
#     b = GetNews('bbcNews', 'donate money', [{'title': 'Duchess wins damages over topless photos', 'url': 'http://www.bbc.co.uk/news/uk-41163712'},
# {'title': 'Twins, 90, donate birthday money', 'url': 'https://www.bbc.co.uk/news/world-asia-china-42639688'},{'title': 'Duchess wins damages over topless photos', 'url': 'http://www.bbc.co.uk/news/uk-41163712'}])
#     b.getNews()