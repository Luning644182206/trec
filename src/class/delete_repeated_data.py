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
import os

path = '../data/original_news/'
allFile = os.listdir(path)
filePaths = []
for fileName in allFile:
    if (fileName != '.DS_Store'):
        name = path + fileName
        filePaths.append(name)

for path in filePaths:
    name = path.split('/')[3]
    name = name.split('_')[0:-1]
    name = '_'.join(name) + '_norepeat.csv'
    print(name)
    allDatas = []
    # 读数据
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            isRepeat = True
            row += [isRepeat]
            allDatas.append(row)

    for index,data in enumerate(allDatas):
        reData = data[2]
        conData = data[1]
        startIndex = index + 1
        if (startIndex < len(allDatas)):
            for index,oneData in enumerate(allDatas[startIndex:]):
                if (reData == oneData[2] and conData == oneData[1] and len(oneData) > 3):
                    allDatas[startIndex + index][4] = False

    # 写数据
    filePath = '../data/news/' + name
    file = open(filePath, 'a+')
    for data in allDatas:
        oneTweet = {}
        if ((len(data) == 5) and data[4]):
            oneTweet['name'] = data[0]
            oneTweet['content'] = data[1]
            oneTweet['retweeted'] = data[2]
            oneTweet['created_at'] = data[3]
            # 文件的头
            titleName = ['name', 'content', 'retweeted', 'created_at']
            writer = csv.DictWriter(file, fieldnames=titleName)
            writer.writerow(oneTweet)

        