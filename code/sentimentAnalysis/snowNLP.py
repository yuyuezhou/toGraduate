from snownlp import SnowNLP

text_path = r"D:\MyRepository\toGraduate\code\wordFrequence\1-100.txt"
text = open(text_path,encoding='utf-8')
line = text.readlines()
pos=0
neg=0
for i in line:
    s = SnowNLP(i)
    if s.sentiments>=0.5:
        pos+=1
    else:neg+=1
print("总数："+str(pos+neg))
print("积极："+str(pos))
print("消极："+str(neg))

# print("1、中文分词:\n",s.words)
#
# print("2、词性标注:\n",s.tags)
#
#
#
# print("4、转换拼音:\n",s.pinyin)
# print("5、输出前4个关键词:\n",s.keywords(4))
#
# print("6、输出关键（中心）句:\n",s.summary(1))
# print("7.1、输出tf:\n",s.tf)
#
# print("7.2、输出idf:\n",s.idf)