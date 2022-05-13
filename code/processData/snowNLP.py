'''
Yyz:此模块用于实现对文本的情感分析,将文本划分为正负两极
目前准确度感觉有点问题
'''
import time
import re
from snownlp import SnowNLP
import pandas as pd
import os
"""
snownlp分析原理（个人总结，其中的贝叶斯原理及最终赋值方法还需进一步查资料）：
1.读取已经分好类的neg.txt和pos.txt 
    如neg.txt="不行，讨厌，一般般，糟糕，差劲，一般般"
    pos.txt="还可以，一般般，不错，喜欢"
2.计算每个词出现的频数
    如neg中”一般般“出现2次，pos中”一般般“出现1次
3.基于贝叶斯原理计算正面负面先验概率P(pos)和P(neg)
    如对于”一般般“，P(pos)=1/4 , P(neg)=2/6=1/3
4.对待分析文本data.txt分词 
    如data.txt="感觉一般般" ----->  "感觉","一般般"
5.计算每个词的后验概率p(词|neg)和p(词|pos)
    如对于”一般般“，p("一般般"|pos)=(1/4)/(1/4+1/3)=3/7 , p("一般般”|neg)=4/7
    上述的3/7、4/7可能计算有误（个人理解） 但思路无误
6.选择计算出的概率较大的类别（正或负）
    如对于“一般般”,p("一般般"|pos) < p("一般般”|neg) 故认为该词属于neg类别 赋值0 (pos则为1）
    实际情况下，并不是只有0、1之分，而是会返回0-1中的某个数，越接近0负面性越强，越接近1则认为正面性越强
"""
from processData import wordfreq

def sentimentAnalysis(data_cutted=""):
    text_path = r"D:\MyRepository\toGraduate\Data\数据处理数据\cleaned_data.xlsx"
    text = pd.read_excel(text_path)
    df = pd.DataFrame(text)
    pos = 0
    neg = 0
    pos_list = []
    neg_list = []
    for row in df.iterrows():
        s = SnowNLP((row[1].values[0]))  # 用jieba.lcut替换了seg.seg
        if s.sentiments >= 0.5:
            pos += 1
            pos_list.append(re.sub("\n |\t", "", (row[1].values[0])))
        else:
            neg += 1
            # neg_list.append(re.sub("[^\u4e00-\u9fa5]", "", i))
            neg_list.append(re.sub("\n|\t", "", (row[1].values[0])))
        # print("\r已经运行了"+str(time.perf_counter())+"秒",end="",flush=True)#覆盖输出
        print("\r正在运行...已经运行了%.1f" % time.perf_counter() + "秒", end="", flush=True)  # 覆盖输出
        # print("\r"+"information", end='',flush="True")  ‘\r’转义字符是将光标移到一行的开始,所以\r之后的内容会覆盖掉上次打印的内容

    # 导出至excel
    save_path = r"D:\MyRepository\toGraduate\Data\情感分析数据"
    os.chdir(save_path)
    pos_List = pd.DataFrame({'pos': pos_list})
    pos_List.to_excel("pos_list.xlsx", index=False)
    neg_List = pd.DataFrame({'neg': neg_list})
    neg_List.to_excel("neg_list.xlsx", index=False)

    print("\n总数：" + str(pos + neg))
    print("积极：" + str(pos))
    print("消极：" + str(neg))

    print("情感分析完成")
    # 自带分词分析结果：pos:1562 neg:289 total:1851 整个平均用时：15s
    # 换用jieba.lcut分词结果： pos:1511 neg:340 total:1851 整个平均用时：4s
    # print("1、中文分词:\n",s.words)
    # print("2、词性标注:\n",s.tags)
    # print("4、转换拼音:\n",s.pinyin)
    # print("5、输出前4个关键词:\n",s.keywords(4))
    # print("6、输出关键（中心）句:\n",s.summary(1))
    # print("7.1、输出tf:\n",s.tf)
    # print("7.2、输出idf:\n",s.idf)


#sentimentAnalysis()