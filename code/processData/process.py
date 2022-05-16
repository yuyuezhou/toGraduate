'''
Yyz:
    process.get_stop_list()获取停用词列表
    process.clean()首先将数据去重，然后进行分词，继而去除停用词、特殊符号、非中文字符等，将清洗后结果以xlsx形式保存(1.去重版 2.去重且分好词版)
    process.show()读取由clean()分好词得到的文件，进行词频统计并保存至本地(.xlsx),然后进行词云图的绘制以增强可读性。出现频次越大，词云图中对应词汇的显示应该更大
'''

#导入所需模块
import os
import jieba #中文分词库 关键词抽取 词频统计
import jieba.posseg as psg #分词操作
import re  #正则表达式 主要应用在字符串匹配中
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image,ImageSequence
import numpy as np
from wordcloud import ImageColorGenerator,WordCloud

#所需文件的路径
inital_data = r"D:\MyRepository\toGraduate\Data\爬虫数据\淘宝笔记本电脑评论数据\test.xlsx" #爬取到的数据所存放的地址
result_path =r"D:\MyRepository\toGraduate\Data\数据处理数据" #本模块生成的结果文件的保存地址
os.chdir(result_path)
stop_file_path =r"D:\MyRepository\toGraduate\Data\数据处理数据\stopwordlist.txt" #停用词表所在地址
custom_file_path =r"D:\MyRepository\toGraduate\Data\数据处理数据\add_word_list.txt"#自定义词表所在地址

def get_stop_list(stop_file_path):#获取停用词表
    try:
        stopword_list = open(stop_file_path,encoding ='utf-8')#打开忽略词文本
    except:
        stopword_list = []
        print("停用词表文件不存在")
    stop_list = []#获取忽略词列表
    for line in stopword_list:
        line = re.sub(u'\n|\r', '', line)
        stop_list.append(line)#获取可用的忽略词列表
    return stop_list

def clean():
    '''
    去重，分词，去除停用词、特殊符号、非中文字符等，以xlsx形式保存(1.去重版 2.去重且分好词版)
    '''
    #text = open(inital_data, encoding="utf-8").readlines()#列表,每个元素是一行
    #df = pd.DataFrame({'contents': text})  # 构建二维数组
    df = pd.read_excel(inital_data)
    #去重
    now_lines = df.shape[0]  # 统计此时的行数 统计列数可用shape[1]
    df = df.drop_duplicates(subset='contents', keep='first')  # 去除重复行 keep=first意为保留第一次重复
    deleted_lines = now_lines - df.shape[0]  # 统计删除掉的行数
    print("成功删除了" + str(deleted_lines) + "行重复内容。")
    result_path = r"D:\MyRepository\toGraduate\Data\数据处理数据"  # 本模块生成的结果文件的保存地址
    os.chdir(result_path)
    df.to_excel('noRepeat_data.xlsx', index=False)
    print("去重过的数据已经成功保存至当前目录！")
    #分词
    print("正在进行分词...")
    jieba.load_userdict(custom_file_path)#将自编词典读入jieba中备用
    jieba.initialize()#此处手动初始化，加载jia词典
    cutted_word_list = []
    noRepeat_data = "noRepeat_data.xlsx"
    df = pd.read_excel(noRepeat_data)
    flag_list = ['vn', 'v', 'a', 'nz', 'n']  # a,形容词，v,形容词 # 'n','nz','vn','v','a'
    for row in df.iterrows():  # 实现按行分析
        line_seg = psg.lcut(row[1].values[0])  # 全称posseg 对本行文本进行切片分词、词性标注 返回列表
        cutted_word_list_temporary=[]
        for word_flag in line_seg:
            word = re.sub("[^\u4e00-\u9fa5]", "", word_flag.word)
            # /unicode编码,[\u4E00-\u9FA5]/ 汉字  ^为非，即此处为去掉非中文字符
            if word_flag.flag in flag_list:
                cutted_word_list_temporary.append(word)
        cutted_word_list.append(",".join(cutted_word_list_temporary))
    df = pd.DataFrame({'cutted_contents': cutted_word_list})
    result_path = r"D:\MyRepository\toGraduate\Data\数据处理数据"  # 本模块生成的结果文件的保存地址
    os.chdir(result_path)
    df.to_excel('cutted_data.xlsx', index=False)
    print("分词成功！已保存至当前目录")

def show():
    '''
    读取由clean()分好词得到的文件，进行词频统计(不是只统计具有所需词性的词语，而是全部都统计)并保存至本地(.xlsx);
    进行词云图的绘制,并保存
    '''
    #词频统计
    print("正在进行词频统计")
    cutted_data = "cutted_data.xlsx"
    #text = open(cutted_data, encoding="utf-8").read()#str 文件中的所有内容
    text = pd.read_excel(cutted_data)
    word_list=[]
    for row in text.iterrows():  # 实现按行分析
        contempty = str(row[1].values[0]).split(',')
        for word in contempty:
            word_list.append(word)
    counts = {}
    #flag_list = ['vn', 'v', 'a', 'nz', 'n']  # a,形容词，v,形容词 # 'n','nz','vn','v','a'
    stop_list = get_stop_list(stop_file_path)
    for word in word_list:
        if len(word)>1 and word not in stop_list:
            counts[word] = counts.get(word, 0) + 1
    word_freq = pd.DataFrame({'word':list(counts.keys()),'freq':list(counts.values())})
    word_freq = word_freq.sort_values(by='freq',ascending=False)
    result_path = r"D:\MyRepository\toGraduate\Data\数据处理数据"  # 本模块生成的结果文件的保存地址
    os.chdir(result_path)
    word_freq.to_excel("word_freq.xlsx",index=False)
    print("词频统计结束！已保存至当前目录")
    #词云图
    wordfreq_path="word_freq.xlsx"
    wordfreq = pd.read_excel(wordfreq_path)
    os.chdir(r"D:\MyRepository\toGraduate\Data\词云图数据")
    font_path = r'c:\\windows\\Fonts\\simhei.ttf'  # 字体路径
    backgroud_image = Image.open("PC.jpg")  # 将文件中的图像读取到数组中
    graph = np.array(backgroud_image)
    wc = WordCloud(
        font_path=font_path,
        max_words=100,
        background_color='white',
        mask=graph)
    word = wordfreq.word
    freq = wordfreq.freq
    dic = dict(zip(word, freq))
    wc.generate_from_frequencies(dic)
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file('WordCloud.png')
    print("词云图已保存至当前目录")

# while True:
#     print("--------------------------------------------------------")
#     print("1.去重、分词 2.词频统计、词云图 3.exit")
#     print("--------------------------------------------------------")
#     num = int(input("输入："))
#     if num == 1:#OK
#         clean()
#     if num == 2:
#         show()
#     if num ==3:
#         break;
