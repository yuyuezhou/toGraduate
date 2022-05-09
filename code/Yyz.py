from crawl import crawl
from sentimentAnalysis import snowNLP
from wordCloud import wordCloud
from wordFrequence import wordfreq
'''
所需功能函数：
爬取数据、存储到本地、数据清洗、分词、词频统计、情感分析、词云图、LDA分析主题
'''

def crawlInitalData(data_url):#爬取数据 data_url为待爬取网站的网址
    return crawl.getData(data_url) #返回列表形式

def saveInitalData(data_list):#保存爬取到的数据至本地 data_list为列表形式的数据
    crawl.save_toexcel(data_list)

def cleanData(data_path):#清洗数据 data_path为数据本地保存路径
    return wordfreq.clean(data_path)

def cutWord(data_path):#分词
    return wordfreq.cout(data_path)

def getWordFreq(data_cutted):#词频统计
    wordfreq.getWordFreq(data_cutted)

def getWordCloud(data_path):#词云图
    wordCloud.show(data_path)

def sentimentAnalysis(data_cutted):#情感分析
    snowNLP.sentimentAnalysis(data_cutted)

#def useLDA(data_path):#LDA主题分析
    #LDA.analysis(data_path)

'''

crawlInitalData()
saveInitalData()
cleanData()
cutWord()
getWordFreq()
wordCloud()
sentimentAnalysis()
useLDA()
'''
