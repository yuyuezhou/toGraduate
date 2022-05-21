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
os.chdir(output_path)
test_list = []
def senti():
    '''
    读取由clean()去完重的文件，进行情感分析。在源文件中对每条评论的极性进行标注
    （考虑更新语料库、如何跳过其自身的分词，直接用之前自己分好词的文件）
    '''
    text_path = r"D:\MyRepository\toGraduate\Data\数据处理数据\cleaned_data.xlsx"
    #text_path = r"D:\MyRepository\toGraduate\Data\爬虫数据\test.xlsx"
    text = pd.read_excel(text_path).astype(str)
    df = pd.DataFrame(text)
    pos = 0
    neg = 0
    senti_list = []
    senti_point_list =[]
    print("正在进行情感分析..")
    for row in df.iterrows():
        phrase = re.sub("[^\u4e00-\u9fa5]", "", str(row[1].values[0]) )
        s = SnowNLP(phrase)  # 去掉了分词操作 直接引用先前分好的词列表 节省了时间
        #print(s.sentiments)
        if s.sentiments > 0.3:
            pos += 1
            #pos_list.append(re.sub("\n |\t", "", str(phrase)))
            senti_list.append(1)
            senti_point_list.append(float(s.sentiments))
            #test_list.append(1)
        elif s.sentiments<=0.3:
            neg += 1
            # neg_list.append(re.sub("[^\u4e00-\u9fa5]", "", i))
            senti_list.append(0)
            senti_point_list.append(float(s.sentiments))
            #test_list.append(0)
        # print("\r已经运行了"+str(time.perf_counter())+"秒",end="",flush=True)#覆盖输出
        #print("\r正在运行...已经运行了%.1f" % time.perf_counter() + "秒", end="", flush=True)  # 覆盖输出

    save_path = r"D:\MyRepository\toGraduate\Data\情感分析数据"
    os.chdir(save_path)
    df['senti'] = senti_list
    df['senti_point'] = senti_point_list
    df.to_excel("sentied.xlsx",index=False)

    print("\n总数：" + str(pos + neg))
    print("积极：" + str(pos))
    print("消极：" + str(neg))
    print("情感分析完成")

data = pd.read_excel(r"D:\MyRepository\toGraduate\Data\情感分析数据\sentied.xlsx")
def lda():
    '''
    读取由clean()分好词得到的文件，进行LDA主题分析。
    '''

    stopList = []  # 含有停用词的列表 由于先前分词的操作已经去除了停用词，此处可以为空
    pos_list_1 = []
    neg_list_1 = []
    pos_list_2 =[]
    neg_list_2=[]
    for row in data.iterrows():  # 实现按行分析
        if int(row[1].values[2]) == 1 :
            pos_list_1.append(row[1].values[0])
            pos_list_2.append(row[1].values[1])
        else:
            neg_list_1.append(row[1].values[0])
            neg_list_2.append(row[1].values[1])
    output_path = r'D:\MyRepository\toGraduate\Data\LDA数据\result'
    os.chdir(output_path)
    po = pd.DataFrame({'contents':pos_list_1 , 'cutted_contents':pos_list_2})
    po.to_excel("posSenti.xlsx", index=False)
    ne = pd.DataFrame({'contents':neg_list_1 ,'cutted_contents':neg_list_2})
    ne.to_excel("negSenti.xlsx", index=False)

    #pos LDA
    pos_data = pd.read_excel("posSenti.xlsx")
    n_features = 1000  # 设置要从所有文章中提取出1000个特征词语（关键词）。
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,  # 取词频最高的前max_features个词作为关键词集
                                    stop_words=stopList,  # 此处也可删去，默认无
                                    max_df=0.12,  # 限制一个词作为关键词的最大出现频率  若太高，则会让废话也成为关键词 如”了“、”的“
                                    min_df=10)  # 限制一个词作为关键词的最小出现次数 float频率 int次数
    tf = tf_vectorizer.fit_transform(pos_data.cutted_contents.astype('U'))  # 得到一个文档词频矩阵
   # x = v.fit_transform(df['Review'].values.astype('U'))
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
    n_top_words = 10  # 每个主题包含的关键词数量
    tf_feature_names = tf_vectorizer.get_feature_names_out()  # 获取所有的关键词，即特征词语；列表型 按vocabulary_中的编号排序

    # 获取某个主题下对应的主题词列表
    topic_word = []
    for topic_idx, topic in enumerate(lda.components_):  # enumerate:遍历一个对象，同时还可以得到当前元素的索引位置。还可自定义索引起始值，这里设为1，默认为0
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
    pos_data['topic'] = topic
    output_path = r'D:\MyRepository\toGraduate\Data\LDA数据\result'
    os.chdir(output_path)
    pos_data.to_excel("pos_topic.xlsx", index=False)
    print("pos主题分析完成！已保存至结果目录")

    # import matplotlib.pyplot as plt
    #
    # plexs = []
    # n_max_topics = 8
    # for i in range(2, n_max_topics):
    #     print(i)
    #     lda = LatentDirichletAllocation(n_components=i, max_iter=50,
    #                                     learning_method='batch',
    #                                     learning_offset=50, random_state=0)
    #     lda.fit(tf)
    #     plexs.append(lda.perplexity(tf))
    #
    # n_t = 4  # 区间最右侧的值。注意：不能大于n_max_topics
    # x = list(range(2, 8))
    # plt.plot(x, plexs)
    # plt.xlabel("number of topics")
    # plt.ylabel("perplexity")
    # plt.show()
    # print("OK")
#============================================================================

    neg_data = pd.read_excel("negSenti.xlsx")
    n_features = 100  # 设置要从所有文章中提取出1000个特征词语（关键词）。
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,  # 取词频最高的前max_features个词作为关键词集
                                    stop_words=stopList,  # 此处也可删去，默认无
                                    max_df=0.3,  # 限制一个词作为关键词的最大出现频率  若太高，则会让废话也成为关键词 如”了“、”的“
                                    min_df=3)  # 限制一个词作为关键词的最小出现次数 float频率 int次数
    tf = tf_vectorizer.fit_transform(neg_data.cutted_contents.astype('U'))  # 得到一个文档词频矩阵
   # x = v.fit_transform(df['Review'].values.astype('U'))
    n_topics = 3  # 设定主题个数
    lda = LatentDirichletAllocation(n_components=n_topics,
                                    max_iter=50,  # max_iter ：EM算法的最大迭代次数。
                                    learning_method='batch',  # 即LDA的求解算法。 batch:批处理
                                    #                                learning_offset=50,#仅仅在算法使用"online"时有意义，取值要大于1。用来减小前面训练样本批次对最终模型的影响
                                    #                                 doc_topic_prior=0.1, #默认是1/n_topics
                                    #                                 topic_word_prior=0.01, #默认是1/n_topics
                                    random_state=0)  # 随机数，随机数相同可以保证每次的结果相同
    lda = lda.fit(tf)  # 学习tf文档中所有标记的词汇词典

    ###########每个主题对应词语
    n_top_words = 8  # 每个主题包含的关键词数量
    tf_feature_names = tf_vectorizer.get_feature_names_out()  # 获取所有的关键词，即特征词语；列表型 按vocabulary_中的编号排序

    # 获取某个主题下对应的主题词列表
    topic_word = []
    for topic_idx, topic in enumerate(lda.components_):  # enumerate:遍历一个对象，同时还可以得到当前元素的索引位置。还可自定义索引起始值，这里设为1，默认为0
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
    neg_data['topic'] = topic
    output_path = r'D:\MyRepository\toGraduate\Data\LDA数据\result'
    os.chdir(output_path)
    neg_data.to_excel("neg_topic.xlsx", index=False)
    print("neg主题分析完成！已保存至结果目录")


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

'''
pos
Topic #0 配置好
品牌 系统 机器 内存 合适 信赖 硬盘 国产 大方 固态
Topic #1 物流速度快 服务态度好
客服反馈 物流 小巧 购物 体积 服务态度 质量 打游戏 耐心 精致
Topic #2: 画质好
画面 完美 品质 画质 漂亮 物流 下单 产品 大家 尺寸
Topic #3:质感好
手感 键盘 舒服 手机 机身 品牌 画质 金属 颜色 配置差
Topic #4:使用好（用途）
上学 打游戏 速度 鼠标 声音 整体 软件 风b键盘 视频

neg
Topic #0: 软件不好用 小故障
激活 垃圾 软件 黑屏 屏幕 上学 下载 便宜
Topic #1: 客服态度 性价比低
客服反馈 配置差 客服 性价比 服务态度 耐心 打游戏 系统
Topic #2: 开机慢 配件不好用 游戏太卡
开机速度 鼠标 打游戏 体积 键盘 声音 看电影 颜值

'''