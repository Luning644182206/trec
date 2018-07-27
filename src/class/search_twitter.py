# coding=utf8
# Created on July 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

# 导入tweepy
import tweepy
import socks
import socket

class SearchTwitter:
    api = ''
    newsNum = 0
    keyWord = ''

    def __init__(self, key, num):
        # 设置代理
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
        socket.socket = socks.socksocket

        # 填写twitter提供的开发Key和secret
        consumer_key = '7OB0M6DgGoeucqaZrpKwcHXHa'
        consumer_secret = '2O83aNL6f55yN76B4rcE6KmVJbU8oGb4CssLpidk1S0xMweh1G'
        access_token = '755029733205618688-iXzrGbgeP2chTpeiYcdrjkVeGIhOpfu'
        access_token_secret = 'DB3eKCnVs5p22mgNYTQRwPBfQYnRbTJL6BC9jMVVaFlz3'
         
        # 提交你的Key和secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # auth.tweet_mode = 'extended' 
        # 获取类似于内容句柄的东西
        self.api = tweepy.API(auth)

        # 获取新闻数量
        self.newsNum = num

        # 记录关键词
        self.keyWord = key

    def search(self):
        datas = []
        # 搜索关键词相关的推文
        for tweet in tweepy.Cursor(self.api.search, tweet_mode = 'extended', q = self.keyWord).items(self.newsNum):
            twitter = tweet._json
            oneTweet = {}
            # 发推人的名字
            oneTweet['name'] = twitter['user']['screen_name']
            # 推文
            oneTweet['content'] = twitter['full_text']
            # 转发的原文
            try:
                oneTweet['retweeted'] = twitter['retweeted_status']['full_text']
            except:
                oneTweet['retweeted'] = ''
            # 创建时间
            oneTweet['created_at'] = twitter['created_at']
            datas.append(oneTweet)
        return datas

# if __name__ == "__main__":
#     a = SearchTwitter('donate money', 100)
#     a.search()





