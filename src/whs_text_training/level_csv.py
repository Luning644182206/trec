import json
import csv
# path = '/Users/whs/work/search/ITR-H.types.json'
def loadJson(path): # 列表形式存储json数据
    with open(path,'r') as f:
        setting = json.load(f)
        id = setting["events"]
        item = {}
        for i in range(len(id)):
            item["id"] = id[i]["eventid"]
            path ="../whs_text_training/data/"+id[i]["eventid"]
            tweetslens = id[i]["tweets"]
            for e in range(len(tweetslens)):
                item["content"] = id[i]["tweets"][e]["indicatorTerms"]
                if len(id[i]["tweets"][e]["indicatorTerms"]) != 0 :
                    item["level"] = id[i]["tweets"][e]["priority"]
                    saveNews(item,True,path) #True为列表形式
        # for i in id :
        # print (id)

# def loadJsonLongList(path): # 一个id一个examples存储数据
#     with open(path,'r') as f:
#         setting = json.load(f)
#         id = setting["informationTypes"]
#         item = {}
#         for i in range(len(id)):
#             item["id"] = id[i]["id"]
#             lens = len(id[i]["exampleLowLevelTypes"])
#             for j in range(lens):
#                 item["content"] =  id[i]["exampleLowLevelTypes"][j]
#             saveNews(item,False) # False为长列表格式

def saveNews(news, type,path):
        filePath = ''
        if (type):
        # 文件的路径 保存在与json文件同一个文件夹下
            filePath = path+'json.csv'
        else:
            filePath = '/Users/whs/work/trec-master/src/data/jsonLonglist.csv'
        file = open(filePath, 'a+')
        titleName = ['id','content','level']
        writer = csv.DictWriter(file, fieldnames = titleName)
        writer.writerow(news)


if __name__ == "__main__":
    loadJson("/Users/whs/work/trec-master/src/data/TRECIS-CTIT-H-Training.json")
    #loadJsonLongList("/Users/whs/work/trec-master/src/class/ITR-H.types.json")