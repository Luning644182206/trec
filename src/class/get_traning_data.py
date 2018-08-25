# coding=utf8
# Created on July 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

# 导入tweepy
import tweepy
import socks
import socket
import json
import csv
import re
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
socket.socket = socks.socksocket

# 填写twitter提供的开发Key和secret
consumer_key = '7OB0M6DgGoeucqaZrpKwcHXHa'
consumer_secret = '2O83aNL6f55yN76B4rcE6KmVJbU8oGb4CssLpidk1S0xMweh1G'
access_token = '755029733205618688-iXzrGbgeP2chTpeiYcdrjkVeGIhOpfu'
access_token_secret = 'DB3eKCnVs5p22mgNYTQRwPBfQYnRbTJL6BC9jMVVaFlz3'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# # 遍历抓取
# for event in events:
#     eventID = event['eventid']
#     tweets = event['tweets']
#     # 抓取
#     for tweet in tweets:
#         writeData = {
#             'eventID': eventID,
#             'postID': tweet['postID'],
#             'categories': ','.join(tweet['categories']),
#             'indicatorTerms': ','.join(tweet['indicatorTerms']),
#             'priority': tweet['priority']
#         }
#         try:
#             content = api.get_status(writeData['postID'], tweet_mode='extended')
#             writeData['content'] = content.full_text
#             # 转发的原文
#             try:
#                 writeData['retweeted'] = content.retweeted_status.full_text
#             except:
#                 writeData['retweeted'] = ''
#             # 存储
#             filePath = '../data/training_data/training_data.csv'
#             file = open(filePath, 'a+')
#             # 文件的头
#             titleName = ['eventID', 'postID', 'categories', 'indicatorTerms', 'priority', 'content', 'retweeted']
#             writer = csv.DictWriter(file, fieldnames=titleName)
#             writer.writerow(writeData)
#         except:
#             print('not exit')


newsNum = 1000
# 按关键词抓取
keyWords = 'typhoon weakened'
try:
    # 搜索关键词相关的推文
    for tweet in tweepy.Cursor(api.search, tweet_mode='extended', q=keyWords, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items(newsNum):
        print(111)
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

        # 存储
        keyWords = keyWords.split(' ')
        keyWords = '_'.join(keyWords)
        filePath = '../data/original_news/twitterNews_Report-Weather_current_news.csv'
        file = open(filePath, 'a+')
        # 文件的头
        titleName = ['name', 'content', 'retweeted', 'created_at']
        writer = csv.DictWriter(file, fieldnames=titleName)
        writer.writerow(oneTweet)
except:
    print('error')
    pass
print('done')