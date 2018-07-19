# coding=utf8
# Created on July 18, 2018
# @author: luning644182206@emails.bjut.edu.cn

import csv
from gensim.models import word2vec
import logging

class WordToVec:
    interpunctions = ['#', ':', "'", '.', ',', '?', '//', '/', '{', '}', '!', '@', '&', '\r', '\t', '\f']
    openFiles = []

    texta = ''

    def __init__ (self, filesNames, text):
        self.openFiles = filesNames
        self.texta = text

    '''
    clearIn:    去标点
    Input:      none
    Output:     none
    others:     none
    '''
    def clearIn(self, text):
        text = text.strip(' ')
        for inter in self.interpunctions:
            if ((inter != '\r') or (inter != '\t') or (inter != '\f')):
                text = text.replace(inter, '')
            else:
                text = text.replace(inter, ' ')
        return text

    def wordToVec(self):
        text = self.clearIn(self.texta)

        f = open("text2.txt",'wb')
        f.write(text.encode("utf-8"))
        f.close()

        logging.basicConfig(format = '%(asctime)s:%(levelname)s: %(message)s', level = logging.INFO)
        sentences = word2vec.Text8Corpus(u"./text2.txt")  # 加载语料
        model = word2vec.Word2Vec(sentences , size = 200)
        # print (model)
        # # 计算某个词的相关词列表
        y2 = model.most_similar("donate", topn=20)  # 20个最相关的
        print("和good最相关的词有：\n")
        for item in y2:
            print(item[0], item[1])

if __name__ == "__main__":
    file = open(r'./text1.txt')
    text = file.readlines()
    a = WordToVec([], text[0])
    a.wordToVec()