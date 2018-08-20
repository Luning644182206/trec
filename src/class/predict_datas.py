# coding=utf8
# Created on Aug 16, 2018
# @author: luning644182206@emails.bjut.edu.cn

import csv
import re
from nltk.corpus import stopwords
from sklearn.externals import joblib
import numpy as np
from sklearn import metrics

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

# 读取测试数据
def readDatas(path):
    testDatas = []
    testOption = []

    # 打开文件
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            content = row[5].strip() + ' ' + row[6].strip()
            # content = row[3].strip() + ' ' + row[4].strip()
            replace = ' '
            urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
            content = re.sub(urlRE, replace, str(content))
            content = clearIn(content)
            testOption.append(row[4])
            testDatas.append(content)
    return testDatas,testOption

# 主函数
if __name__ == '__main__':
    path = '../data/training_data/training_data.csv'

    # 读取预测数据
    testDatas, testOption = readDatas(path)

    # 读取本地预测模型
    textClf = joblib.load('../model/level_train_model.m')
    predicted = textClf.predict(testDatas)
    print ('SVC',np.mean(predicted == testOption))
    print (set(predicted))
    # 混淆矩阵 1,2,3 意思为真值为2，预测值为3的有1个
    print (metrics.confusion_matrix(testOption, predicted)) # 混淆矩阵





