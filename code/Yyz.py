from getData import crawl
from processData import snowNLP,wordCloud,wordfreq
#from analyzeData import lda


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

def cutWord(data_path="1-100.txt"):#分词
    return wordfreq.cut(data_path)

def getFreq(data_cutted="1-100.txt"):#词频统计
    #wordfreq.get_freq_inital(data_cutted)
    wordfreq.get_freq(data_cutted)

def getWordCloud(data_path="word_freq.xlsx"):#词云图
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
    print("1.爬取数据 2.清洗数据 3.原始数据分词 4.词频统计")
    print("5.词云图绘制 6.情感分析 7.LDA主题分析 8.退出")
    print("--------------------------------------------------------")
    num = int(input("请输入指令: "))
    if num == 8:#OK
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
    if num == 3:#OK
        cutted_word_list = cutWord()
        #print(cutted_word_list)
    if num == 4:#OK
        getFreq()
        print("词频统计结束，已保存至当前目录")
    if num == 5:#OK
        print("正在绘制词云图...")
        getWordCloud()
    if num == 6:#OK
        '''
        Yyz:准确率可能有问题
        '''
        print("正在对文本进行情感分析...")
        sentimentAnalysis("")
    if num == 7:
        '''...'''
