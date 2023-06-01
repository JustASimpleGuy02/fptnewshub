import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
import os.path as osp

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    stopwords = open(osp.join(dir_path, 'stopword.txt'), 'r')
    stopwords_list = stopwords.read().split('\n')
    
    text = 'Xin chào tôi là Dũng tôi đến từ Hà Nội Việt Nam rất vui được gặp bạn'
    wordcloud = WordCloud(stopwords=stopwords_list).generate(text)
    plt.figure(figsize=(8,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
