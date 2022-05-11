'''
Yyz:用于去除每行开头数字和正文之间的\t占位符
'''
import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg

file_path = input("请输入当前文件夹路径:")
#D:\code\NLP\wordfreq
os.chdir(file_path)
file_name = input("请输入文件名字:")
text = open(file_name,encoding="utf-8").read()
text_lines  = text.split('\n')
textList = []
i=0
for line in text_lines:
    line = re.sub("\t","",line)
    textList.append(line)
    i = i+1

dataOfWavebo = pd.DataFrame({"content":textList})

dataOfWavebo.to_excel("dataOfWavebo.xlsx",index=False)

print(textList)
print(i)
print(len(textList))