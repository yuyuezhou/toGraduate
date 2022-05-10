import os
import jieba #中文分词库 关键词抽取 词频统计
import jieba.posseg as psg #分词操作
import re  #正则表达式 主要应用在字符串匹配中
import pandas as pd
# Pandas 一个强大的分析结构化数据的工具集，基础是 Numpy（提供高性能的矩阵运算）。
# Pandas 可以从各种文件格式比如 CSV、JSON、SQL、Microsoft Excel 导入数据。
# Pandas 可以对各种数据进行运算操作，比如归并、再成形、选择，还有数据清洗和数据加工特征。

def get_stop_dict(stop_file):  #获取要忽略的词汇的列表（词典）
    content = open(stop_file,encoding="utf-8")
    word_list = []
    for c in content:#此时的c是content的某一行 即按行读取
        c = re.sub('\n|\r','',c) #实现正则的替换 -->此处操作意为去除换行及回车符
        # re.sub(pattern, repl, string, count=0, flags=0)
        # re.sub通过正则表达式，实现比普通字符串的replace更加强大的替换功能，即：
        # 用repl来替换string中的pattern，并返回替换后的新字符串
        word_list.append(c)
    return word_list


def clean(data_path="1-100.txt"):#清洗数据
    '''
        Yyz:1.去除首行的”评论“ 2.去除每行开头的数字 3.去除完全重复的文本 4.将清洗完毕的数据重新写入文本并返回
    '''
    file_path = r"D:\MyRepository\toGraduate\code\wordFrequence"  # 开头加r是为了防止报错，具体原因可去掉r后运行，将报错信息百度
    # file_path = input("请输入当前文件夹路径:")
    os.chdir(file_path)
    data_path = "1-100.txt"
    text = open(data_path, encoding="utf-8").read()
    text_lines = text.split('\n')  # 列表，每个元素是源文件中的一行

    # 1. 利用pop(),直接指定删除列表第一个元素，即”评论“
    text_lines.pop(0)

    # 2. 通过观察 每行开头都是数字+\t,故可通过遍历去除
    i = 0  # 记录正在处理的行号索引
    for line in text_lines:
        line = line.split('\t')  # 此时是list形式，并已去除占位符
        line.pop(0)  # 此时的列表首个元素即为每行开头的数字序号，将其去除
        line = ''.join(line)  # 还原为str形式
        text_lines[i] = line  # 替换原有行
        i += 1
    print("正在进行去重...")
    # 3. 利用DataFrame.drop_duplicates(subset=None, keep=‘first’, inplace=False, ignore_index=False)
    df = pd.DataFrame({'评论': text_lines})  # 构建二维数组
    now_lines = df.shape[0]  # 统计此时的行数 统计列数可用shape[1]
    df = df.drop_duplicates(subset='评论', keep='first')  # 去除重复行 keep=first意为保留第一次重复
    deleted_lines = now_lines - df.shape[0]  # 统计删除掉的行数
    # print(df)
    print("成功删除了" + str(deleted_lines) + "行重复内容。")
    # for line in text_lines:  # 实现按行分析

    # 4. 保存至本地并返回列表
    df.to_excel('cleaned_data.xlsx', index=False)
    print("清洗过的数据已经成功保存至当前目录！")

    lists = df.values.tolist()  # 此时是嵌套列表[['comment1'],['comment2']....[] ]
    cleaned_list = []
    for i in lists:
        cleaned_list.append(i[0])  # ['comment1']-->'comment1'
    return cleaned_list



# def cut(data_path=""):#分词
#     '''
#     Yyz:此功能可弃
#     '''
#
# def get_freq_pos_neg(pos_path="",neg_path=""):#词频统计(针对正负两极文本)
#     '''
#     Yyz:尚待完善
#     '''

# def get_freq_inital(data_path="1-100.txt"):#词频统计(针对原始文本）
#     file_path = r"D:\MyRepository\toGraduate\code\wordFrequence"  # 开头加r是为了防止报错，具体原因可去掉r后运行，将报错信息百度
#     # file_path = input("请输入当前文件夹路径:")
#     # D:\MyRepository\toGraduate\code\NLP\wordfreq
#     os.chdir(file_path)
#     # os.chdir() 方法用于改变当前工作目录到指定的路径。
#     # 后续对文件的搜索、调用、存储都是在此路径下进行
#     stop_file = "stopwordlist.txt"#含有需忽略的词汇文本
#     user_file = "add_word_list.txt"#切割限制及词性读取
#     stop_words = get_stop_dict(stop_file)#将含有需忽略的词汇文本正则处理后变为列表形式
#     #print(stop_words)
#     #file_name = input("请输入文件名字:")
#     #file_name = "1-100.txt"
#     file_name = data_path #"1-100.txt"
#     text = open(file_name,encoding="utf-8").read()#读取待分析文本
#     jieba.load_userdict(user_file)#jieba加载自定义词库 自动搜索至指定路径
#     #每行的含义是 词 词频 词性,
#     text_lines  = text.split('\n')#列表，每个元素是源文件中的一行
#     flag_list = ['vn', 'v', 'a', 'nz', 'n']  # a,形容词，v,形容词 # 'n','nz','vn','v','a'
#     counts = {}
#     print("正在进行分词...")
#     for line in text_lines:  # 实现按行分析
#         line_seg = psg.lcut(line)  # 全称posseg 对本行文本进行切片分词、词性标注 返回列表
#         # print(line_seg)
#         for word_flag in line_seg:
#             word = re.sub("[^\u4e00-\u9fa5]", "", word_flag.word)
#             # /unicode编码,[\u4E00-\u9FA5]/ 汉字  ^为非，即此处为去掉非中文字符
#             if word_flag.flag in flag_list and len(word) > 1 and word not in stop_words:
#                 counts[word] = counts.get(word, 0) + 1
#                 #print(word)
#                 # counts.get(key, value) 返回指定键(key)的值  value选填，如果指定键的值不存在时，返回该默认值。
#     print("分词成功，正在进行词频统计")
#     word_freq = pd.DataFrame({'word':list(counts.keys()),'freq':list(counts.values())})
#     #设置二维数组  DataFrame是由多种类型的列构成的二维标签数据结构，即二维数组
#     word_freq = word_freq.sort_values(by='freq',ascending=False)
#     #设置排序 by指定根据哪一列数据进行排序，ascending=False指定降序排序
#     word_freq.to_excel("word_freq.xlsx",index=False)
#     #导出至excel index若为true则在excel中显示对应数据在原二维数组中的下标位置索引
#     print("词频统计结束，已保存至当前目录")
#
#

#print("done!")

# import wordcloud
# import matplotlib.pyplot as plt
# from PIL import Image
# import numpy as np
#
#
# backgroud_Image=np.array(Image.open(r'C:\Users\Yyz\Desktop\wordcloud.png'))
#     #plt.imread(r'C:\Users\Yyz\Desktop\wordcloud.png')
# word_cloud = wordcloud.WordCloud(font_path="STZHONGS.ttf",
#                       max_words=100,
#                       background_color='white',
#                       mask=backgroud_Image)
# my_wordcloud = word_cloud.fit_words(word_freq)
# plt.imshow(my_wordcloud)
# plt.axis('off')
# plt.show()
