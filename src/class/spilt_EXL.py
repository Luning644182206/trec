import csv
import re
from nltk.corpus import stopwords

label = ['costaRicaEarthquake2012','fireColorado2012','floodColorado2013',
    'typhoonPablo2012','laAirportShooting2013','westTexasExplosion2013']
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

def readDatas(path,i):
    item = {}
    savePath = '../data/level_data/'
    # 打开文件
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if(row[0] == label[i]) :
                content = row[5].strip() + ' ' + row[6].strip()
                replace = ' '
                urlRE = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
                content = re.sub(urlRE, replace, str(content))
                content = clearIn(content)
                item['level'] = row[4]
                item['content'] = content
                saveNews(item,savePath,i)

def saveNews(news,path,i):
                filePath = ''
                filePath = path+label[i]+'.csv'
                file = open(filePath, 'a+')
                titleName = ['level','content']
                writer = csv.DictWriter(file, fieldnames = titleName)
                writer.writerow(news)

if __name__== "__main__" :
    path = '../data/training_data/training_data.csv'
    for i in range(6):
        readDatas(path,i)
            