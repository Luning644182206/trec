# coding=utf8
# Created on Aug 14, 2018
# @author: luning644182206@emails.bjut.edu.cn

import csv
import re
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn import metrics
from nltk.corpus import stopwords
from sklearn.externals import joblib
'''
clearIn:    去标点
Input:      none
Output:     none
others:     none
'''
def clearIn(text):
    interpunctions = [';', '_', '’', '…', 'rt', 'via', '-', '[', ']', '(', ')', '"', '#', ':', "'", '.', ',', '?', '//', '/', '{', '}', '!', '&', '\r', '\t', '\f']
    text = text.lower()
    text = text.strip(' ')
    text = ' '.join([word for word in text.strip().split() if word not in stopwords.words("english")])
    for inter in interpunctions:
        if ((inter != '\r') or (inter != '\t') or (inter != '\f')):
            text = text.replace(inter, '')
        else:
            text = text.replace(inter, ' ')
    return text

# # 读取训练集
# def readtrain(paths):
#     trainingDatas = []
#     testDatas = []

#     for path in paths:
#         fileName = path.split('/')[3]
#         nameSplit = fileName.split('_')
#         source = nameSplit[0]
#         fatherLabel = nameSplit[1]
#         sonLabel = '_'.join(nameSplit[2:-1])
#         counter = 0

#         # 打开文件
#         with open(path, 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             datas = []
#             for row in reader:
#                 content = ''
#                 counter += 1
#                 if (source != 'twitterNews'):
#                     content = clearIn(row[2].strip())
#                 else:
#                     content = row[1].strip() + ' ' + row[2].strip()
#                     replace = ' '
#                     urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
#                     content = re.sub(urlRE, replace, str(content))
#                     content = clearIn(content)
#                 # dataPush = [content, sonLabel, fatherLabel]
#                 dataPush = [content, sonLabel]
#                 datas.append(dataPush)
#             splitNum = int(counter/2)
#             trainingDatas += datas[:splitNum]
#             testDatas += datas[splitNum:]
#     return trainingDatas, testDatas

# 读取训练集
def readtrain(paths):
    trainingDatas = []
    testDatas = []

    for path in paths:
        counter = 0
        # 打开文件
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            datas = []
            for row in reader:
                counter += 1
                # content = row[5].strip() + ' ' + row[6].strip()
                content = row[1].strip()
                replace = ' '
                urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
                content = re.sub(urlRE, replace, str(content))
                content = clearIn(content)
                dataPush = [content, row[2]]
                datas.append(dataPush)
            splitNum = int(counter/9)
            testDatas += datas[:splitNum]
            trainingDatas += datas[splitNum:]
    return trainingDatas, testDatas

def splitOptionAndData(datas):
    data = []
    label = []
    for oneData in datas:
        data.append(oneData[0])
        label.append(oneData[1])
    return data,label

if __name__ == '__main__':
    # path = '../data/news/'
    path = '../whs_text_training/data/'
    allFile = os.listdir(path)
    for i in range(len(allFile)):
        filePaths = []
        name = path + allFile[i]
        filePaths.append(name)

        trainingDatas, testDatas = readtrain(filePaths)

        # 划分
        trainContent, trainOpinion = splitOptionAndData(trainingDatas)
        testContent, testOpinion = splitOptionAndData(testDatas)

        # 训练和预测一体
        textClf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SVC(C=1.0, kernel = 'linear'))])
        textClf = textClf.fit(trainContent, trainOpinion)
        # 保存模型
        joblib.dump(textClf, '../whs_text_training/model/'+allFile[i]+'.m')
        predicted = textClf.predict(testContent)
        print ('SVC',np.mean(predicted == testOpinion))
        print (set(predicted))
        # 混淆矩阵 1,2,3 意思为真值为2，预测值为3的有1个
        print (metrics.confusion_matrix(testOpinion, predicted)) # 混淆矩阵







