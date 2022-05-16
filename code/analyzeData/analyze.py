'''
.senti()读取由clean()去完重的文件，进行情感分析。（考虑更新语料库、如何跳过其自身的分词，直接用之前自己分好词的文件）
.lda()读取由clean()分好词得到的文件，进行LDA主题分析。
'''
import time
import re
from snownlp import SnowNLP
import pandas as pd
import os
import pandas as pd
import jieba
import jieba.posseg as psg
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

output_path = r'D:\MyRepository\toGraduate\Data\LDA数据\result' #主题结果的存放位置
data = pd.read_excel(r"D:\MyRepository\toGraduate\Data\数据处理数据\cutted_data.xlsx")
os.chdir(output_path)

def senti():
    '''
    读取由clean()去完重的文件，进行情感分析。
    （考虑更新语料库、如何跳过其自身的分词，直接用之前自己分好词的文件）
    '''
    text_path = r"D:\MyRepository\toGraduate\Data\数据处理数据\noRepeat_data.xlsx"
    #text_path = r"D:\MyRepository\toGraduate\Data\爬虫数据\八爪-京东笔记本电脑评论\1-10.xlsx"
    text = pd.read_excel(text_path)
    df = pd.DataFrame(text)
    pos = 0
    neg = 0
    pos_list = []
    neg_list = []
    for row in df.iterrows():
        phrase = re.sub("[^\u4e00-\u9fa5]", "", row[1].values[0] )
        s = SnowNLP(phrase)  # 用jieba.lcut替换了seg.seg
        if s.sentiments >= 0.7:
            pos += 1
            pos_list.append(re.sub("\n |\t", "", phrase))
        else:
            neg += 1
            # neg_list.append(re.sub("[^\u4e00-\u9fa5]", "", i))
            neg_list.append(re.sub("\n|\t", "", phrase))
        # print("\r已经运行了"+str(time.perf_counter())+"秒",end="",flush=True)#覆盖输出
        print("\r正在运行...已经运行了%.1f" % time.perf_counter() + "秒", end="", flush=True)  # 覆盖输出

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

def lda():
    '''
    读取由clean()分好词得到的文件，进行LDA主题分析。
    '''
    stopList = []  # 含有停用词的列表 由于先前分词的操作已经去除了停用词，此处可以为空
    n_features = 1000  # 设置要从所有文章中提取出1000个特征词语（关键词）。
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,  # 取词频最高的前max_features个词作为关键词集
                                    stop_words=stopList,  # 此处也可删去，默认无
                                    max_df=0.5,  # 限制一个词作为关键词的最大出现频率  若太高，则会让废话也成为关键词 如”了“、”的“
                                    min_df=2)  # 限制一个词作为关键词的最小出现次数 float频率 int次数
    tf = tf_vectorizer.fit_transform(data.cutted_contents)  # 得到一个文档词频矩阵

    n_topics = 5  # 设定主题个数
    lda = LatentDirichletAllocation(n_components=n_topics,
                                    max_iter=50,  # max_iter ：EM算法的最大迭代次数。
                                    learning_method='batch',  # 即LDA的求解算法。 batch:批处理
                                    #                                learning_offset=50,#仅仅在算法使用"online"时有意义，取值要大于1。用来减小前面训练样本批次对最终模型的影响
                                    #                                 doc_topic_prior=0.1, #默认是1/n_topics
                                    #                                 topic_word_prior=0.01, #默认是1/n_topics
                                    random_state=0)  # 随机数，随机数相同可以保证每次的结果相同
    lda = lda.fit(tf)  # 学习tf文档中所有标记的词汇词典

    ###########每个主题对应词语
    n_top_words = 15  # 每个主题包含的关键词数量
    tf_feature_names = tf_vectorizer.get_feature_names_out()  # 获取所有的关键词，即特征词语；列表型 按vocabulary_中的编号排序

    # 获取某个主题下对应的主题词列表
    topic_word = []
    for topic_idx, topic in enumerate(lda.components_, 1):  # enumerate:遍历一个对象，同时还可以得到当前元素的索引位置。还可自定义索引起始值，这里设为1，默认为0
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        # 上行注释：首先对主题topic中的数值按从大到小的顺序排序，然后依次将下标【0 ~ n_top_words-1】的值之前所在的下标赋值给i(这就是argsort函数的作用，若忘了可查),
        # 此时再到特征词表tf_feature_names中查找得到编号i对应的关键词，最终将这n_top_words个关键词以列表的形式返回，再经过" ".join()转为str形式
        topic_word.append(topic_w)
        print(topic_w)

    ###########输出每篇文章对应主题
    topics = lda.transform(tf)
    topic = []
    for t in topics:
        topic.append(list(t).index(np.max(t)))  # 选出每个文章最可能的主题，返回列表，每个元素为一篇文章的主题
    data['topic'] = topic
    output_path = r'D:\MyRepository\toGraduate\Data\LDA数据\result'
    os.chdir(output_path)
    data.to_excel("data_topic.xlsx", index=False)
    print("LDA主题分析完成！已保存至结果目录")


# while True:
#     print("--------------------------------------------------------")
#     print("1.情感分析 2.lda 3.exit")
#     print("--------------------------------------------------------")
#     num = int(input("输入："))
#     if num == 1:#OK
#         senti()
#     if num == 2:
#         lda()
#     if num ==3:
#         break;