# coding=utf8
# Created on Aug 16, 2018
# @author: luning644182206@emails.bjut.edu.cn

import csv
import os
import re
from nltk.corpus import stopwords
from sklearn.externals import joblib
import numpy as np
from sklearn import metrics

label = {
    'GoodsServices': 'Request-GoodsServices',
    'SearchAndRescue': 'Request-SearchAndRescue',
    'InformationWanted': 'Request-InformationWanted',
    'Volunteer': 'CallToAction-Volunteer',
    'FundRaising': 'CallToAction-FundRaising',
    'Donations': 'CallToAction-Donations',
    'MovePeople': 'CallToAction-MovePeople',
    'FirstPartyObservation': 'Report-FirstPartyObservation',
    'ThirdPartyObservation': 'Report-ThirdPartyObservation',
    'Weather': 'Report-Weather',
    'EmergingThreats': 'Report-EmergingThreats',
    'SignificantEventChange': 'Report-SignificantEventChange',
    'MultimediaShare': 'Report-MultimediaShare',
    'ServiceAvailable': 'Report-ServiceAvailable',
    'Factoid': 'Report-Factoid',
    'Official': 'Report-Official',
    'CleanUp': 'Report-CleanUp',
    'Hashtags': 'Report-Hashtags',
    'PastNews': 'Other-PastNews',
    'ContinuingNews': 'Other-ContinuingNews',
    'Advice': 'Other-Advice',
    'Sentiment': 'Other-Sentiment',
    'Discussion': 'Other-Discussion',
    'Irrelevant': 'Other-Irrelevant',
    'Unknown': 'Other-Unknown',
    'KnownAlready': 'Other-KnownAlready'
}
'''
clearIn:    去标点
Input:      none
Output:     none
others:     none
'''
def clearIn(text):
    interpunctions = [';', '_', '’', '…', 'rt', 'via', '-', '[', ']', '(', ')', '"', ':', "'", '.', ',', '?', '//', '/', '{', '}', '!', '&', '\r', '\t', '\f']
    text = text.lower()
    text = text.strip(' ')
    text = ' '.join([word for word in text.strip().split() if word not in stopwords.words("english")])
    for inter in interpunctions:
        if ((inter != '\r') or (inter != '\t') or (inter != '\f')):
            text = text.replace(inter, '')
        else:
            text = text.replace(inter, ' ')
    return text

# # 读取测试数据
# def readDatas(path):
#     testDatas = []
#     testOption = []

#     # 打开文件
#     with open(path, 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             content = row[5].strip() + ' ' + row[6].strip()
#             # content = row[3].strip() + ' ' + row[4].strip()
#             replace = ' '
#             urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
#             content = re.sub(urlRE, replace, str(content))
#             content = clearIn(content)
#             testOption.append(label[row[2]])
#             testDatas.append(content)
#     return testDatas,testOption

# 读取训练集(ontology)
def readDatas(paths):
    testDatas1 = []
    testDatas2 = []

    for path in paths:
        fileName = path.split('/')[3]
        nameSplit = fileName.split('_')
        source = nameSplit[0]
        fatherLabel = nameSplit[1]
        sonLabel = '_'.join(nameSplit[2:-1])
        counter = 0

        # 打开文件
        with open(path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            datas = []
            for row in reader:
                if (len(row) > 0):
                    content = ''
                    counter += 1
                    if (source != 'twitterNews'):
                        content = clearIn(row[2].strip())
                    else:
                        content = row[1].strip() + ' ' + row[2].strip()
                        replace = ' '
                        urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
                        content = re.sub(urlRE, replace, str(content))
                        content = clearIn(content)
                    dataPush = [content, fatherLabel]
                    # dataPush = [content, sonLabel]
                    datas.append(dataPush)
            splitNum = int(counter/2)
            # trainingDatas += datas[:splitNum]
            testDatas1 += datas[:splitNum]
            testDatas2 += datas[splitNum:]
    return testDatas2

def splitOptionAndData(datas):
    data = []
    label = []
    for oneData in datas:
        data.append(oneData[0])
        label.append(oneData[1])
    return data,label

# 主函数
if __name__ == '__main__':
    # path = '../data/training_data/training_data.csv'
    # # 读取预测数据
    # testDatas, testOption = readDatas(path)
    # =======
    path = '../data/news/'
    # path = '../data/training_data/training1/'
    allFile = os.listdir(path)
    filePaths = []
    for fileName in allFile:
        if (fileName != '.DS_Store'):
            name = path + fileName
            filePaths.append(name)

    testDatas = readDatas(filePaths)
    testContent, testOption = splitOptionAndData(testDatas)
    # ========
    # 读取本地预测模型
    textClf = joblib.load('../model/ontology_train_model.m')
    predicted = textClf.predict(testContent)
    predictedProba = textClf.predict_proba(testContent)
    # 统计 正确几个 不正确几个 正确率
    counterLabel = {
        'Request-GoodsServices': [0, 0, 0, 0, 0, 0],
        'Request-SearchAndRescue': [0, 0, 0, 0, 0, 0],
        'Request-InformationWanted': [0, 0, 0, 0, 0, 0],
        'CallToAction-Volunteer': [0, 0, 0, 0, 0, 0],
        'CallToAction-FundRaising': [0, 0, 0, 0, 0, 0],
        'CallToAction-Donations': [0, 0, 0, 0, 0, 0],
        'CallToAction-MovePeople': [0, 0, 0, 0, 0, 0],
        'Report-FirstPartyObservation': [0, 0, 0, 0, 0, 0],
        'Report-ThirdPartyObservation': [0, 0, 0, 0, 0, 0],
        'Report-Weather': [0, 0, 0, 0, 0, 0],
        'Report-EmergingThreats': [0, 0, 0, 0, 0, 0],
        'Report-SignificantEventChange': [0, 0, 0, 0, 0, 0],
        'Report-MultimediaShare': [0, 0, 0, 0, 0, 0],
        'Report-ServiceAvailable': [0, 0, 0, 0, 0, 0],
        'Report-Factoid': [0, 0, 0, 0, 0, 0],
        'Report-Official': [0, 0, 0, 0, 0, 0],
        'Report-CleanUp': [0, 0, 0, 0, 0, 0],
        'Report-Hashtags': [0, 0, 0, 0, 0, 0],
        'Other-PastNews': [0, 0, 0, 0, 0, 0],
        'Other-ContinuingNews': [0, 0, 0, 0, 0, 0],
        'Other-Advice': [0, 0, 0, 0, 0, 0],
        'Other-Sentiment': [0, 0, 0, 0, 0, 0],
        'Other-Discussion': [0, 0, 0, 0, 0, 0],
        'Other-Irrelevant': [0, 0, 0, 0, 0, 0],
        'Other-Unknown': [0, 0, 0, 0, 0, 0],
        'Other-KnownAlready': [0, 0, 0, 0, 0, 0]
    }

    file = open('predicted.txt', 'ab+')

    # 分析结果
    sumRight = 0
    allDataNum = 0
    for index, element in enumerate(predicted):
        # 添加人工筛选
        # pro = round(max(predictedProba[index]),2)
        # print(pro)
        if (testOption[index] == element):
            # 一样 TP
            counterLabel[element][0] += 1
            sumRight += 1
        else:
            # 不一样
            # FN 不属于C的，分成了C
            counterLabel[element][1] += 1
            # TN 属于C的被分成了其他类
            counterLabel[testOption[index]][2] += 1
        allDataNum += 1

    sumTP = 0
    sumFN = 0
    sumTN = 0
    for item in counterLabel:
        # FP 别人都分对的个数
        counterLabel[item][3] = sumRight - counterLabel[item][0]
        if ((counterLabel[item][1] + counterLabel[item][0]) != 0):
            # p
            counterLabel[item][4] = counterLabel[item][0]/(counterLabel[item][1] + counterLabel[item][0])
        if ((counterLabel[item][1] + counterLabel[item][2]) != 0):
            # r
            counterLabel[item][5] = counterLabel[item][0]/(counterLabel[item][0] + counterLabel[item][2])
        sumTP += counterLabel[item][0]
        sumFN += counterLabel[item][1]
        sumTN += counterLabel[item][2]
        # data = item + '    ' + str(counterLabel[item][0]) + '    ' + str(counterLabel[item][1]) + '    ' + str(counterLabel[item][2]) + '    ' + str(counterLabel[item][3]) + '    ' + str(counterLabel[item][4]) + '    ' + str(counterLabel[item][5]) + '\n'
        data = item + str(counterLabel[item][4]) + '    ' + str(counterLabel[item][5]) + '\n'
        file.write(data.encode('utf-8'))
    print(sumTP, sumFN, sumTN)
    # 存储
    file.write('details\n'.encode('utf-8'))
    # for index, element in enumerate(predicted):
    #     data = testOption[index] + '        ' + element + '\n'
    #     file.write(data.encode('utf-8'))
    file.close()
    
    # print ('SVC',np.mean(predicted == testOption))
    microP = sumTP/(sumTP + sumFN)
    microR = sumTP/allDataNum
    microF = 2 * microP * microR/(microP + microR)
    print ('microP', microP)
    print ('microR', microR)
    print ('微平均', microF)
    print (set(predicted))
    # 混淆矩阵 1,2,3 意思为真值为2，预测值为3的有1个
    # print (metrics.confusion_matrix(testOption, predicted)) # 混淆矩阵





