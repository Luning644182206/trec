# coding=utf8
# Created on July 26, 2018
# @author: luning644182206@emails.bjut.edu.cn

# 导入tweepy
import tweepy
import socks
import socket
import json
import csv

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
# file = pd.read_csv('../data/TRECIS-CTIT-H-Test.tweetids.tsv', sep='\t') # 设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
file = csv.reader(open('../data/TRECIS-CTIT-H-Test.tweetids.tsv', 'r'))
for item in file:
    data = item[0].split('\t')
    writeData = {
        'label': data[0],
        'event': data[1],
        'postID': data[2]
    }
    content = ''
    try:
        content = api.get_status(writeData['postID'], tweet_mode='extended')
        content = content.full_text
        # 转发的原文
        try:
            writeData['retweeted'] = content.retweeted_status.full_text
        except:
            writeData['retweeted'] = ''
            print('false')
    except:
        print('not exit')
    writeData['content'] = content
    # 存储
    filePath = '../data/test_data/test_data.csv'
    fileTest = open(filePath, 'a+')
    # 文件的头
    titleName = ['label', 'event', 'postID', 'content', 'retweeted']
    writer = csv.DictWriter(fileTest, fieldnames=titleName)
    writer.writerow(writeData)