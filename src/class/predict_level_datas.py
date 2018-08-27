# coding=utf8
# Created on Aug 16, 2018
# @author: luning644182206@emails.bjut.edu.cn
import csv
import re
from nltk.corpus import stopwords
from sklearn.externals import joblib
import numpy as np
from sklearn import metrics


label = ['costaRicaEarthquake2012','fireColorado2012','floodColorado2013',
    'typhoonPablo2012','laAirportShooting2013','westTexasExplosion2013']

# 读取测试数据
def readDatas(path):
    testDatas = []
    testOption = []

    # 打开文件
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            level = row[0]
            content = row[1]
            testOption.append(level) # 4为level等级
            testDatas.append(content)
    return testDatas,testOption

# 主函数
if __name__ == '__main__':
    for i in range(6) :
        path = '../data/level_data/'+label[i]+'.csv'

        # 读取预测数据
        testDatas, testOption = readDatas(path)

        # 读取本地预测模型
        modelPath = '../model/level_model/'+label[i]+'json.m'
        textClf = joblib.load(modelPath)
        predicted = textClf.predict(testDatas)

        # file = open('predicted.txt', 'ab+')
        # # 分析结果
        # for index, element in enumerate(predicted):
        #     if (testOption[index] == element):
        #         # 一样
        #         counterLabel[element][0] += 1
        #     else:
        #         # 不一样
        #         counterLabel[testOption[index]][1] += 1
        # for item in counterLabel:
        #     if (counterLabel[item][0] + counterLabel[item][1] != 0):
        #         counterLabel[item][2] = counterLabel[item][0]/(counterLabel[item][0] + counterLabel[item][1])
        #     data = item + '    ' + str(counterLabel[item][0]) + '    ' + str(counterLabel[item][1]) + '    ' + str(counterLabel[item][2]) + '\n'
        #     file.write(data.encode('utf-8'))
        # # 存储
        # file.write('details\n'.encode('utf-8'))
        # # for index, element in enumerate(predicted):
        # #     data = testOption[index] + '        ' + element + '\n'
        # #     file.write(data.encode('utf-8'))
        # file.close()
        print ('SVC',np.mean(predicted == testOption))
        print (set(predicted))
        # 混淆矩阵 1,2,3 意思为真值为2，预测值为3的有1个
        print (metrics.confusion_matrix(testOption, predicted)) # 混淆矩阵





