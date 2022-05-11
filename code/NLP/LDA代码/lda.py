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
data = pd.read_excel("dataOfWavebo.xlsx")#读取文本。这些文本事先应已经过清洗，但未分词。
os.chdir(output_path)
dic_file = "D:/code/NLP/lda/stop_dic/dict.txt"#自编词典的存放位置
stop_file = "D:/code/NLP/lda/stop_dic/stopwords.txt"#忽略词的存放位置


def chinese_word_cut(mytext):#中文分词
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
    seg_list = psg.cut(mytext)#全称posseg 对文本切片分词并进行词性标注 返回生成器 可用for来遍历循环 不是列表 lcut返回列表
    for seg_word in seg_list:
        word = re.sub(u'[^\u4e00-\u9fa5]','',seg_word.word) #分析中文
        #word = seg_word.word #分析英文
        this_word_need_stop = False
        for stop_word in stop_list:
            if stop_word == word or len(word)<2:     #this word is stopword
                    this_word_need_stop = True
                    break
        if this_word_need_stop == False and seg_word.flag in flag_list:
            word_list.append(word)      
    return (" ").join(word_list) #返回字符串形式

data["content_cutted"] = data.content.apply(chinese_word_cut)
#将data.content这一列文本作为括号里函数的参数，并储存在data里新建的"content_cutted"列中  66666666
#apply方法就是将函数应用到由列或行形成的一维数组上 不必再自写笨拙的循环，其内部自带牛b的循环方式
#apply将函数返回的结果也组成数组，注意不是让函数直接返回数组，即编写函数时只考虑一组数据即可。

'''
#test  ---> 此时的data为DataFrame二维数组 两列：content、content_cutted 1850行：每行为一条评论
print(data)
'''


#######LDA分析
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

stopList=[] #含有停用词的列表 由于先前分词的操作已经去除了停用词，此处可以为空
n_features = 20 #设置要从所有文章中提取出1000个特征词语（关键词）。
'''
Yyz: 对‘特征词语’的理解：在若干文章(为便于理解，默认>1)中，某个词语不仅在文章a中出现，也在文章b/c/f/z...中出现
     即该词语不仅仅只在一篇文章中出现，则可认为该词语的含义可能对这若干文章的主题有影响作用
     即具有该词语的文章可能有共同的主题。这类词语就称为‘特征词语’
     当然，不能随意认定某词语为‘特征词语’，下面函数中的max_df和min_df就起到了很好的约束作用，使得特征词语的设置更准确
'''
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,#取词频最高的前max_features个词作为关键词集
                                stop_words=stopList,#此处也可删去，默认无
                                max_df = 0.5,#限制一个词作为关键词的最大出现频率  若太高，则会让废话也成为关键词 如”了“、”的“
                                min_df = 2)#限制一个词作为关键词的最小出现次数 float频率 int次数
tf = tf_vectorizer.fit_transform(data.content_cutted)#得到一个文档词频矩阵
#CountVectorizer会将文本中的词语转换为词频矩阵，它通过fit_transform函数计算各个词语出现的次数。
#CountVectorizer是通过fit_transform函数将文本中的词语转换为关键词的词频矩阵，矩阵元素a[i][j] 表示j词在第i个文本下的词频,即各个词语出现的次数.
# 通过get_feature_names()可看到所有文本的关键字，通过toarray()可看到词频矩阵的结果。
#数据输入形式为列表，列表元素为代表文章的字符串，一个字符串代表一篇文章，字符串是已经分割好的。
#上述详细解析见：
# https://blog.csdn.net/weixin_38278334/article/details/82320307
#https://blog.csdn.net/tang123246235/article/details/104528366
'''
#test:
print(tf)#如 (2,1) 3 意为：第2篇文章里编号为1的关键词出现了3次
print(tf.toarray()) #如第n个[]为[0 2 0],意为：在第n个文章里，编号为0的关键词出现了0次，编号为1的关键词出现了2次,编号为2的关键词出现了0次 （编号为下标位置的关键词出现了(下标位置对应值)次
print(tf_vectorizer.vocabulary_)#所有关键词都存放在这里，个数为n_features，形式dict:'关键词','编号' 编号范围[0,总个数-1]
'''

n_topics = 2 #设定主题个数
lda = LatentDirichletAllocation(n_components=n_topics,
                                max_iter=50,#max_iter ：EM算法的最大迭代次数。
                                learning_method='batch',#即LDA的求解算法。 batch:批处理
#                                learning_offset=50,#仅仅在算法使用"online"时有意义，取值要大于1。用来减小前面训练样本批次对最终模型的影响
#                                 doc_topic_prior=0.1, #默认是1/n_topics
#                                 topic_word_prior=0.01, #默认是1/n_topics
                               random_state=0)#随机数，随机数相同可以保证每次的结果相同
lda = lda.fit(tf)#学习tf文档中所有标记的词汇词典
#上述详细解析见：
#https://www.cnblogs.com/pinard/p/6908150.html

'''
test:
print(lda.components_)# lda.components_,形式为嵌套列表：每个元素都是列表，每个列表元素都是LDA计算出来的主题，列表元素里的元素则是LDA计算出来的每一个关键词对当前主题的贡献(影响力)(正相关)。
print(','.join(map(str,lda.components_[0])))
'''


###########每个主题对应词语
n_top_words = 25#每个主题包含的关键词数量
tf_feature_names = tf_vectorizer.get_feature_names_out()#获取所有的关键词，即特征词语；列表型 按vocabulary_中的编号排序
'''
test:
print(tf_feature_names)#such as : ['办公', '外观', '电脑', '速度']
print(tf_vectorizer.vocabulary_)#such as : {'电脑': 2, '办公': 0, '外观': 1, '速度': 3}
print(tf_feature_names)
'''

#获取某个主题下对应的主题词列表
def print_topic_words(lda_model, tf_feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(lda_model.components_,1):#enumerate:遍历一个对象，同时还可以得到当前元素的索引位置。还可自定义索引起始值，这里设为1，默认为0
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([tf_feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        #上行注释：首先对主题topic中的数值按从大到小的顺序排序，然后依次将下标【0 ~ n_top_words-1】的值之前所在的下标赋值给i(这就是argsort函数的作用，若忘了可查),
        #此时再到特征词表tf_feature_names中查找得到编号i对应的关键词，最终将这n_top_words个关键词以列表的形式返回，再经过" ".join()转为str形式
        tword.append(topic_w)
        print(topic_w)
    return tword

topic_word = print_topic_words(lda, tf_feature_names, n_top_words)

###########输出每篇文章对应主题
import numpy as np
topics=lda.transform(tf)
'''
lda.transform()注释：
得到一个文档主题分布嵌套列表，每个列表元素为一篇文章，文章列表中有n_topics个值，
这个值为对应下标编号的主题就是该文章主题的概率，故显然概率最大的主题最能代表该文档
'''

# print(topics)
topic = []
for t in topics:
    topic.append(list(t).index(np.max(t)))#选出每个文章最可能的主题，返回列表，每个元素为一篇文章的主题
data['topic']=topic
data.to_excel("data_topic.xlsx",index=False)
#topics[0]#0 1 2

print("OK")
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















