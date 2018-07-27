# coding=utf8
# Created on July 18, 2018
# @author: luning644182206@emails.bjut.edu.cn

import logging
import csv
import re
from gensim.models import word2vec
from nltk.corpus import stopwords

class WordToVec:
    interpunctions = [';', '_', '’', '…', 'rt', 'via', '-', '[', ']', '(', ')', '"', '#', ':', "'", '.', ',', '?', '//', '/', '{', '}', '!', '@', '&', '\r', '\t', '\f']
    openFiles = []

    '''
    __init__:   初始化
    Input:      none
    Output:     none
    others:     none
    '''
    def __init__ (self, filesNames):
        self.openFiles = filesNames

    '''
    clearIn:    去标点
    Input:      none
    Output:     none
    others:     none
    '''
    def clearIn(self, text):
        text = text.lower()
        text = text.strip(' ')
        text = ' '.join([word for word in text.strip().split() if word not in stopwords.words("english")])
        for inter in self.interpunctions:
            if ((inter != '\r') or (inter != '\t') or (inter != '\f')):
                text = text.replace(inter, '')
            else:
                text = text.replace(inter, ' ')
        return text

    def wordToVec(self):
        logging.basicConfig(format = '%(asctime)s:%(levelname)s: %(message)s', level = logging.INFO)
        sentences = word2vec.Text8Corpus(u"./text_temp.txt")  # 加载语料
        model = word2vec.Word2Vec(sentences , size = 200)
        # print (model)
        # # 计算某个词的相关词列表
        y2 = model.most_similar("money", topn=50)  # 20个最相关的
        print("和moneye最相关的词有：\n")
        for item in y2:
            print(item[0], item[1])
    

    def preData(self):
        datas = ''
        # 读取所有的语料
        for path in self.openFiles:
            data = csv.reader(open(path, 'r'))
            for row in data:
                if (path.find('twitterNews')):
                    content = row[1] + ' ' + row[2]
                else:
                    content = row[2]
                replace = ' '
                urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
                content = re.sub(urlRE, replace, str(content))
                # 去标点
                content = self.clearIn(content)
                datas = ' ' + content + datas
        # 存储
        file = open('text_temp.txt', 'wb')
        file.write(datas.encode('utf-8'))
        file.close()


if __name__ == "__main__":
    # a = WordToVec(['../data/foxNews_donate_money_news.csv', '../data/bbcNews_donate_money_news.csv', '../data/twitterNews_donate_money_news.csv'])
    a = WordToVec(['../data/twitterNews_donate_money_news.csv'])
    a.preData()
    a.wordToVec()