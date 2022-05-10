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

def cleanData(data_path='1-100.txt'):#清洗数据 data_path为数据本地保存路径
    return wordfreq.clean(data_path)

def cutWord(data_path):#分词
    return wordfreq.cut(data_path)

def getFreqInital(data_cutted):#词频统计（初始数据）
    wordfreq.get_freq_inital(data_cutted)

def getFreqPosNeg(pos_path,neg_path):#词频统计(针对正负两极文本)
    wordfreq.get_freq_pos_neg(pos_path,neg_path)

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
while True:
    print("--------------------------------------------------------")
    print("0.退出 1.爬取数据 2.清洗数据 3.原始数据分词 4.初始数据词频统计")
    print("5.正负两极文本词频统计 6.词云图绘制 7.情感分析 8.LDA主题分析")
    print("--------------------------------------------------------")
    num = int(input("请输入指令: "))
    if num == 0:#OK
        print("结束运行\n")
        break
    if num == 1:#OK
        data_url = input("请输入待爬取的网址: ")
        #crawlInitalData(data_url)
        print("正在进行爬取...")
        print("爬取成功，正在进行本地保存")
        print("爬取到的数据已成功保存至当前目录")
    if num == 2:#OK
        cleaned_data_list = cleanData()
        print(cleaned_data_list)
    if num == 3:
        '''...'''
    if num == 4:
        getFreqInital("1-100.txt")
    if num == 5:
        '''...'''
    if num == 6:
        getWordCloud("")
    if num == 7:
        '''...'''
    if num == 8:
        '''...'''
