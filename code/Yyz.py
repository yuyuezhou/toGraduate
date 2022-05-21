from getData import crawl
from processData import process
from analyzeData import analyze

#
'''
所需功能函数：
爬取数据、存储到本地、数据清洗、分词、词频统计、情感分析、词云图、LDA分析主题

'''

def crawlInitalData(data_url):#爬取数据 data_url为待爬取网站的网址
    return crawl.getData(data_url) #返回列表形式

def cleanData():#清洗数据 data_path为数据本地保存路径
    return process.clean()

def showData_1():#词频统计、词云图
    process.show_1()

def sentimentAnalysis():#情感分析
    analyze.senti()

def useLDA():#LDA主题分析
    analyze.lda()

def showData_2():
    process.show_2()

while True:
    print("--------------------------------------------------------")
    print("0.退出 1.爬取数据 2.数据去重、分词(数据预处理) ")
    print("3.词频统计、绘制词云图 4.情感分析 5.分别统计正负词频、绘制词云图 6.LDA主题分析")
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
        cleanData()
    if num == 3:#OK
        showData_1()
    if num == 4:#OK
        sentimentAnalysis()
    if num==5:
        showData_2()
    if num == 6:#OK
        useLDA()
