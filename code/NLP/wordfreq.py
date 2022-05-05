import os
import jieba #中文分词库 关键词抽取 词频统计
import jieba.posseg as psg #分词操作
import re  #正则表达式 主要应用在字符串匹配中
import pandas as pd
# Pandas 一个强大的分析结构化数据的工具集，基础是 Numpy（提供高性能的矩阵运算）。
# Pandas 可以从各种文件格式比如 CSV、JSON、SQL、Microsoft Excel 导入数据。
# Pandas 可以对各种数据进行运算操作，比如归并、再成形、选择，还有数据清洗和数据加工特征。

def get_stop_dict(file):  #获取要忽略的词汇的列表（词典）
    content = open(file,encoding="utf-8")
    word_list = []
    for c in content:
        c = re.sub('\n|\r','',c) #实现正则的替换 -->此处操作意为去除换行及回车符
        # re.sub(pattern, repl, string, count=0, flags=0)
        # re.sub通过正则表达式，实现比普通字符串的replace更加强大的替换功能，即：
        # 用repl来替换string中的pattern，并返回替换后的新字符串
        word_list.append(c)
    return word_list

file_path = input("请输入当前文件夹路径:")
#D:\code\NLP\wordfreq
os.chdir(file_path)
#os.chdir() 方法用于改变当前工作目录到指定的路径。
#后续对文件的搜索、调用、存储都是在此路径下进行


stop_file = "stopwordlist.txt"#含有需忽略的词汇文本
user_file = "add_word_list.txt"#切割限制及词性读取

stop_words = get_stop_dict(stop_file)#将含有需忽略的词汇文本正则处理后变为列表形式
file_name = input("请输入文件名字:")
text = open(file_name,encoding="utf-8").read()#读取待分析文本
jieba.load_userdict(user_file)#jieba加载自定义词库 自动搜索至指定路径
#每行的含义是 词 词频 词性,
text_lines  = text.split('\n')#逐行分析

flag_list = ['vn','v','a','nz','n']#a,形容词，v,形容词 # 'n','nz','vn','v','a'
counts={}

for line in text_lines:
    line_seg = psg.lcut(line)#全称posseg 对文本切片分词并进行词性标注 返回列表
    #print(line_seg)
    for word_flag in line_seg:
        word = re.sub("[^\u4e00-\u9fa5]","",word_flag.word)
        #/unicode编码,[\u4E00-\u9FA5]/ 汉字  ^为非，即此处为去掉非中文字符
        if word_flag.flag in flag_list and len(word)>1 and word not in stop_words:
            counts[word]=counts.get(word,0)+1
            print(word)
            #counts.get(key, value) 返回指定键(key)的值  value选填，如果指定键的值不存在时，返回该默认值。

word_freq = pd.DataFrame({'word':list(counts.keys()),'freq':list(counts.values())})
#设置二维数组  DataFrame是由多种类型的列构成的二维标签数据结构，即二维数组
word_freq = word_freq.sort_values(by='freq',ascending=False)
#设置排序 by指定根据哪一列数据进行排序，ascending=False指定降序排序
word_freq.to_excel("word_freq.xlsx",index=False)
#导出至excel index若为true则在excel中显示对应数据在原二维数组中的下标位置索引

print("done!")