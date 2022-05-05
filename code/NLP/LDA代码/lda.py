import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg


#######预处理

output_path = 'D:/code/NLP/lda/result' #主题结果的存放位置
file_path = 'D:/code/NLP/lda/data' #文本数据的位置
os.chdir(file_path)
# data=pd.read_excel("data.xlsx")#content type
data = pd.read_excel("dataOfWavebo.xlsx")
os.chdir(output_path)
dic_file = "D:/code/NLP/lda/stop_dic/dict.txt"#自编词典的存放位置
stop_file = "D:/code/NLP/lda/stop_dic/stopwords.txt"#忽略词的存放位置


def chinese_word_cut(mytext):
    jieba.load_userdict(dic_file)#将自编词典读入jieba中备用
    jieba.initialize()#此处手动初始化，加载jia词典
    #jieba采用延迟加载方式，import jieba 时不会立刻加载jieba词典，使用时才开始加载。
    #如果想提前加载和初始化，可以手动触发
    try:
        stopword_list = open(stop_file,encoding ='utf-8')#打开忽略词文本
    except:
        stopword_list = []
        print("error in stop_file")
    stop_list = []#获取可用的忽略词列表
    flag_list = ['n','nz','vn']#标注想获取什么样词性的词语
    for line in stopword_list:
        line = re.sub(u'\n|\\r', '', line)#将回车和空格去掉
        #前缀u表示后面字符串以 Unicode 格式 进行编码，一般用在中文字符串前面
        #防止因为源码储存格式问题，导致再次使用时出现乱码
        stop_list.append(line)#获取可用的忽略词列表
    
    word_list = []#获取分词结果列表
    #jieba分词
    seg_list = psg.cut(mytext)#全称posseg 对文本切片分词并进行词性标注 返回列表
    for seg_word in seg_list:
        word = re.sub(u'[^\u4e00-\u9fa5]','',seg_word.word) #分析中文
        #word = seg_word.word #分析英文
        find = 0
        for stop_word in stop_list:
            if stop_word == word or len(word)<2:     #this word is stopword
                    find = 1
                    break
        if find == 0 and seg_word.flag in flag_list:
            word_list.append(word)      
    return (" ").join(word_list) #返回字符串形式


data["content_cutted"] = data.content.apply(chinese_word_cut)
#将data.content这一列文本作为括号里函数的参数，并储存在data里新建的"content_cutted"列中


#######LDA分析

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword
stopList=[]
n_features = 1000 #提取1000个特征词语
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,#取词频最高的前max_features个词作为关键词集
                                stop_words=stopList,
                                max_df = 0.5,#限制一个词作为关键词的最大出现频率  若太高，则会让废话也成为关键词 如”了“、”的“
                                min_df = 10)#限制一个词作为关键词的最小出现次数 float频率 int次数
tf = tf_vectorizer.fit_transform(data.content_cutted)#得到一个文档词频矩阵
#用数据输入形式为列表，列表元素为代表文章的字符串，一个字符串代表一篇文章，字符串是已经分割好的。
#上述详细解析见：
# https://blog.csdn.net/weixin_38278334/article/details/82320307


n_topics = 8
lda = LatentDirichletAllocation(n_components=n_topics,
                                max_iter=50,#max_iter ：EM算法的最大迭代次数。
                                learning_method='batch',#即LDA的求解算法。
                                learning_offset=50,#仅仅在算法使用"online"时有意义，取值要大于1。用来减小前面训练样本批次对最终模型的影响
#                                 doc_topic_prior=0.1,
#                                 topic_word_prior=0.01,
                               random_state=0)
lda.fit(tf)#学习tf文档中所有标记的词汇词典
#上述详细解析见：
#https://www.cnblogs.com/pinard/p/6908150.html

###########每个主题对应词语
n_top_words = 25
tf_feature_names = tf_vectorizer.get_feature_names()#获取所有文本的词汇；列表型
topic_word = print_top_words(lda, tf_feature_names, n_top_words)

###########输出每篇文章对应主题
import numpy as np
topics=lda.transform(tf)#得到一个文档词频矩阵
topic = []
for t in topics:
    topic.append(list(t).index(np.max(t)))
data['topic']=topic
data.to_excel("data_topic.xlsx",index=False)
#topics[0]#0 1 2


"""
###########可视化

import pyLDAvis
import pyLDAvis.sklearn

#pyLDAvis.enable_notebook()
pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.display(pic)
pyLDAvis.save_html(pic, 'lda_pass'+str(n_topics)+'.html')
# enable_notebook功能仅适用于您使用笔记本时。
# 如果您正在编写一个将可视化输出为HTML文档的脚本，那么您不需要（也不应该）调用该函数。
# 相反，我认为您只需要使用prepare和^{}函数。
#去工作路径下找保存好的html文件
#pyLDAvis.show(pic)


###########困惑度
import matplotlib.pyplot as plt

plexs = []
n_max_topics = 16
for i in range(1,n_max_topics):
    print(i)
    lda = LatentDirichletAllocation(n_components=i, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,random_state=0)
    lda.fit(tf)
    plexs.append(lda.perplexity(tf))


n_t=15#区间最右侧的值。注意：不能大于n_max_topics
x=list(range(1,n_t))
plt.plot(x,plexs[1:n_t])
plt.xlabel("number of topics")
plt.ylabel("perplexity")
plt.show()
print("OK")
"""















