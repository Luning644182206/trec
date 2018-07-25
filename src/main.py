# coding=utf8
# Created on July 11, 2018
# @author: luning644182206@emails.bjut.edu.cn

import sys
sys.path.append('./class')
from search import NewsSearch
from get_news import GetNews
# import socks
# import socket
# import requests
# from urllib import request

if __name__ == "__main__":
    a = NewsSearch('foxNews', 'donate money', 200)
    a.search()
    b = GetNews(a.website, a.keyWords, a.results)
    b.getNews()

    # 测试代理
    # socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
    # socket.socket = socks.socksocket
    # html = requests.get('https://www.bbc.co.uk/search/more?page=6&q=donate+money&sa_f=search-product&filter=news&suggid=')
    # soup = BS(html.text, 'html.parser')
    # # r = request.build_opener(SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1086)).open('https://www.bbc.co.uk/search/more?page=6&q=donate+money&sa_f=search-product&filter=news&suggid=')
    # print(soup) # check ips

    # 测试链接
#     b = GetNews('bbcNews', 'donate money', [{'title': 'Duchess wins damages over topless photos', 'url': 'http://www.bbc.co.uk/news/uk-41163712'},
# {'title': 'Twins, 90, donate birthday money', 'url': 'https://www.bbc.co.uk/news/world-asia-china-42639688'},{'title': 'Duchess wins damages over topless photos', 'url': 'http://www.bbc.co.uk/news/uk-41163712'}])
    # b = GetNews('foxNews', 'donate money', [{'title': 'Twins, 90, donate birthday money', 'url': 'http://www.foxnews.com/story/2001/09/08/jacko-triumphs-in-freak-show-at-garde-666714596.html'}])
    # b.getNews()
