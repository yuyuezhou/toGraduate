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

inital_data = r"D:\MyRepository\toGraduate\Data\爬虫数据\淘宝笔记本电脑评论数据\test.xlsx"
# text = open(inital_data, encoding="utf-8").readlines()  # 列表,每个元素是一行
cutted_data = r"D:\MyRepository\toGraduate\Data\数据处理数据\cutted_data.xlsx"
text = pd.read_excel(cutted_data)
df = pd.DataFrame(text)
word_list = []
for row in text.iterrows():  # 实现按行分析
    contempty = str(row[1].values[0]).split(',')
    for word in contempty:
        word_list.append(word)
print(word_list)