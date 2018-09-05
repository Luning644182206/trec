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

# 读取测试数据
def readDatas(path):
    testDatas = []

    # 打开文件
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            eventNum = row[0].strip().split('-')[4]
            eventName = row[1].strip()
            tweetID = row[2].strip()
            content = row[3].strip()
            replace = ' '
            urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
            content = re.sub(urlRE, replace, str(content))
            content = clearIn(content)
            data = [eventNum, eventName, tweetID, content]
            testDatas.append(data)
    return testDatas

def splitOptionAndData(datas):
    data = []
    for oneData in datas:
        data.append(oneData[3])
    return data

# 预测等级
def levelpredict(testDatas, predicted):
    dataList = []
    fireModel = joblib.load('../whs_text_training/model/fireColorado2012json.m')
    floodModel = joblib.load('../whs_text_training/model/floodColorado2013json.m')
    earthquakeModel = joblib.load('../whs_text_training/model/costaRicaEarthquake2012json.m')
    typhoonModel = joblib.load('../whs_text_training/model/typhoonPablo2012json.m')
    shootModel = joblib.load('../whs_text_training/model/laAirportShooting2013json.m')
    explosionModel = joblib.load('../whs_text_training/model/westTexasExplosion2013json.m')
    for index, item in enumerate(predicted):
        data = testDatas[index] + [item]
        eventName = data[1]
        content = data[3]
        # if (content == ''):
        # 	data[4] = 'Other-Irrelevant'
        if ('fire' in eventName):
            data += [fireModel.predict([content])[0]]
        elif (('flood' in eventName) or ('Flood' in eventName)):
            data += [floodModel.predict([content])[0]]
        elif (('earthquake' in eventName) or ('Earthquake' in eventName)):
            data += [earthquakeModel.predict([content])[0]]
        elif (('typhoon' in eventName) or ('Tornado' in eventName)):
            data += [typhoonModel.predict([content])[0]]
        elif (('shoot' in eventName) or ('Shoot' in eventName)):
            data += [shootModel.predict([content])[0]]
        elif (('Bombings' in eventName) or ('Attacks' in eventName)):
            data += [explosionModel.predict([content])[0]]
        dataList.append(data)
    return dataList

# 计算分数
def countScore(dataList):
    levelScore = {
        'Critical': 5,
        'High': 4,
        'Medium': 3,
        'Low': 2
    }
    Label = {
        'Request-GoodsServices': 5,
        'Request-SearchAndRescue': 5,
        'Request-InformationWanted': 4.5,
        'CallToAction-Volunteer': 4,
        'CallToAction-FundRaising': 4,
        'CallToAction-Donations': 4,
        'CallToAction-MovePeople': 4,
        'Report-FirstPartyObservation': 3,
        'Report-ThirdPartyObservation': 3,
        'Report-Weather': 3.5,
        'Report-EmergingThreats': 4,
        'Report-SignificantEventChange': 3.5,
        'Report-MultimediaShare': 2,
        'Report-ServiceAvailable': 3.5,
        'Report-Factoid': 3,
        'Report-Official': 3,
        'Report-CleanUp': 3,
        'Report-Hashtags': 2,
        'Other-PastNews': 1,
        'Other-ContinuingNews': 2,
        'Other-Advice': 2,
        'Other-Sentiment': 1,
        'Other-Discussion': 1,
        'Other-Irrelevant': 0.5,
        'Other-Unknown': 1,
        'Other-KnownAlready': 1 
    }
    dataScoreList = []
    for index, item in enumerate(dataList):
        score = Label[item[4]] * levelScore[item[5]]
        data = item + [score]
        dataScoreList.append(data)
    return dataScoreList

# 整理数据
def orderList(dataList):
    datas = {}
    dataReturn = []
    for data in dataList:
        try:
            datas[data[0]].append(data)
        except:
            datas[data[0]] = []
            datas[data[0]].append(data)
    for event in datas:
        sortListData = sortList(datas[event])
        for index, data in enumerate(sortListData):
        	sortNum = index + 1
        	data += [sortNum]
        	dataReturn.append(data)
    return dataReturn

# 排序
def sortList(dataList):
    return sorted(dataList, key=lambda data: data[6], reverse=True)
# 主函数
if __name__ == '__main__':
    # path = '../data/test_data/test_data.csv'
    # # 读取预测数据
    # testDatas = readDatas(path)
    # testDatasContent = splitOptionAndData(testDatas)
    # # 读取本地预测模型
    # textClf = joblib.load('../model/ontology_train_model.m')
    # predicted = textClf.predict(testDatasContent)
    # predictedProba = textClf.predict_proba(testDatasContent)
    # # 人工干预
    # file = open('predicted_real1.txt', 'ab+')
    # for index, item in enumerate(predicted):
    #     result = round(max(predictedProba[index]), 2)
    #     data = testDatas[index]
    #     if (data[3] != ''):
    #         if (result > 0.15):
    #             data += [item]
    #         else:
    #             data += ['UNKOWN']
    #     else:
    #         data += ['Other-Irrelevant']
    #     dataWrite = data[0] + ',' + 'Q0' + ',' + data[1] + ',' + data[2] + ',' + data[3] + ',' + data[4] + '\n'
    #     file.write(dataWrite.encode('utf-8'))
    # file.close()

    # 读取人为干预结果
    file = open('myrun1.txt', 'r')
    files = open('myrun1.1.txt', 'ab+')
    lines = file.readlines()   
    file.close()
    predicted = []
    testDatas = []
    labelIndex = {}
    for line in lines:
        line = line.split('	')
        id = line[1][2:]
        try:
            labelIndex[id].append(True)
        except:
            labelIndex[id] = []
            labelIndex[id].append(True)
            dataWrite = 'TRECIS-CTIT-H-Test-' + line[0] + '	' + 'Q0' +  '  ' + id + '	' + line[2] + '	' + line[3] + '	' + line[4] + '	' + line[5] + '\n'
            files.write(dataWrite.encode('utf-8'))
    files.close()
    # # 预测level
    # dataList = levelpredict(testDatas, predicted)
    # # 计算分数
    # dataList = countScore(dataList)
    # # 排序
    # dataList = orderList(dataList)
    # file = open('myrun2.txt', 'ab+')
    # for data in dataList:
    #     dataWrite = 'TRECIS-CTIT-H-Test-' + data[0] + '	' + 'Q0' +  '  ' + data[2] + '	' + str(data[7]) + '	' + str(data[6]) + '	' + data[4] + '	' + 'myrun2' + '\n'
    #     file.write(dataWrite.encode('utf-8'))
    # file.close()


    




