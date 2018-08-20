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

# 读取json
file = open('../data/TRECIS-CTIT-H-Training.json', encoding='utf-8')  # 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
traningDatas = json.load(file)
events = traningDatas['events'] # 注意多重结构的读取语法

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


# # 扩展抓取
# levels = {
#     'Medium': [],
#     'Critical': [],
#     'Low': [],
#     'High': []
# }
# '''
# clearIn:    去标点
# Input:      none
# Output:     none
# others:     none
# '''
# def clearIn(text):
#     interpunctions = ['‘', '@', ';', '’', '…', 'rt', 'via', '-', '[', ']', '(', ')', '"', '#', ':', "'", '.', ',', '?', '//', '/', '{', '}', '!', '&', '\r', '\t', '\f']
#     text = text.lower()
#     text = text.strip(' ')
#     # text = ' '.join([word for word in text.strip().split() if word not in stopwords.words("english")])
#     for inter in interpunctions:
#         if ((inter != '\r') or (inter != '\t') or (inter != '\f')):
#             text = text.replace(inter, '')
#         else:
#             text = text.replace(inter, ' ')
#     return text

def splitWords(words):
    # 按大写字母做拆分
    pattern = '[A-Z]'
    # 遇到大写字母就给加空格
    newWords = re.sub(pattern, lambda x:' ' + x.group(0), words)
    # 出去头尾空格
    newWords = newWords.strip()
    # 变成小写
    newWords = newWords.lower()
    return newWords

# # 把关键词提取出来
# for event in events:
#     tweets = event['tweets']
#     # 抓取
#     for tweet in tweets:
#         if (len(tweet['indicatorTerms'])):
#             keyWords = ''
#             for key in tweet['indicatorTerms']:
#                 key = clearIn(key).capitalize()
#                 keyWords += key
#             if keyWords not in levels[tweet['priority']]:
#                 levels[tweet['priority']].append(keyWords)


# 存储
file = open('level.txt', 'r')
lines = file.readlines()
file.close()
newsNum = 1000
# 按关键词抓取
for line in lines:
    level = (line.strip()).split(' ')[0]
    keyWords = splitWords((line.strip()).split(' ')[1])
    print(level + ' ' + keyWords)
    try:
        # 搜索关键词相关的推文
        for tweet in tweepy.Cursor(api.search, tweet_mode='extended', q=keyWords, wait_on_rate_limit=True, wait_on_rate_limit_notify=True).items(newsNum):
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
            filePath = '../data/training_data/' + level + '_' + keyWords + '.csv'
            file = open(filePath, 'a+')
            # 文件的头
            titleName = ['name', 'content', 'retweeted', 'created_at']
            writer = csv.DictWriter(file, fieldnames=titleName)
            writer.writerow(oneTweet)
    except:
        print('error')
        pass
print('done')