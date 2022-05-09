'''
Yyz:本模块用于实现词云图的显示
'''
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image,ImageSequence
import numpy as np
from wordcloud import ImageColorGenerator,WordCloud

def show(data_path=""):
    os.chdir(r"D:\MyRepository\toGraduate\code\wordFrequence")
    wordfreq = pd.read_excel("word_freq.xlsx")
    os.chdir(r"D:\MyRepository\toGraduate\code\wordCloud")
    font_path = r'c:\\windows\\Fonts\\simhei.ttf'  # 字体路径
    backgroud_image = Image.open("PC.jpg")  # 将文件中的图像读取到数组中
    graph = np.array(backgroud_image)
    wc = WordCloud(
        font_path=font_path,
        max_words=100,
        background_color='white',
        mask=graph)
    word = wordfreq.word
    freq = wordfreq.freq
    dic = dict(zip(word, freq))
    wc.generate_from_frequencies(dic)
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file('WordCloud.png')
    print("词云图已成功保存至当前目录")