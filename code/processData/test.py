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
from snownlp import SnowNLP

#训练语料库
os.chdir(r"D:\Python\Lib\site-packages\snownlp\sentiment")
from snownlp import sentiment
print("training...")
sentiment.train('neg - 2.txt','pos2.txt')
print("train ok")
sentiment.save('sentiment.marshal')


#检测准确率
os.chdir(r"D:\MyRepository\toGraduate\Data\爬虫数据")
testData_path = "test.xlsx"
print("testing")
df = pd.read_excel(testData_path)
senti_list=[]
for row in df.iterrows():
    s = SnowNLP((row[1].values[0]))  # 用jieba.lcut替换了seg.seg
    if s.sentiments >= 0.5:
        senti_list.append(1)
    else:
        senti_list.append(0)
df['senti_test'] = senti_list
df.to_excel("testt.xlsx",index=False)
print("ok")

#==============================================

df = pd.read_excel("testt.xlsx")
sum=0
num=0
for row in df.iterrows():
    know =row[1].values[1]
    judge = row[1].values[2]
    if know == judge:
        num+=1
    sum+=1

print("准确率：%.3f%%" %(num/sum*100))





'''
pos:5  max=0.12 min = 10 
neg:3  max=0.3 min=3

random=0

Topic #0:配置好
小巧 机箱 鼠标 系统 内存 机器 硬盘 地方 声音 固态
Topic #1: 玩游戏顺畅、画质好
游戏 画质 画面 品质 完美 键盘 超薄 玩游戏 性价比 音效
Topic #2:整体质感好，颜值高
感觉 舒服 特色 手感 颜色 手机 整体 键盘 银色 金属
Topic #3:客服态度好，听他人介绍或买给他人用
客服 问题 耐心 性价比 孩子 态度 朋友 物流 服务态度 颜色
Topic #4:物流速度快，性价比高，品牌推荐
物流 价格 质量 下单 品牌 购物 体验 发货 性价比 产品

Topic #0:客服态度差，软件存在难以激活等问题
客服 问题 激活 耐心 系统 时间 无法 态度
Topic #1:噪音大，屏幕体验差，不喜欢颜值
垃圾 声音 风扇 屏幕 软件 颜值 赠品 键盘
Topic #2:配件有问题
鼠标 开机 机箱 商家 地方 不错 速度 键盘


random =1
Topic #0:玩游戏顺畅、画质好
游戏 画面 品质 很棒 问题 玩游戏 画质 软件 感觉 基本
Topic #1:物流速度快，性价比高
物流 质量 购物 价格 下单 性价比 客服 发货 鼠标 孩子
Topic #2:质感好，做工好
键盘 手感 画质 舒服 感觉 性价比 金属 整体 机身 细腻
Topic #3:便携，颜值高
小巧 特色 颜色 机箱 轻便 声音 超薄 漂亮 精致 地方
Topic #4:客服态度好，品牌
系统 客服 品牌 手机 耐心 产品 内存 问题 信赖 感觉
pos主题分析完成！已保存至结果目录
Topic #0:服务态度不好
客服 商家 耐心 软件 黑屏 系统 服务态度 疫情
Topic #1:软硬件差
鼠标 问题 客服 激活 垃圾 售后 感觉 时间
Topic #2:噪音大，开机慢
开机 机箱 声音 地方 颜值 风扇 键盘 小巧

random=2


'''
