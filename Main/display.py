import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import os.path as osp
from Preprocess.clean_text import tien_xu_li
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

def display_statistics(weeks, mentions):
    plt.plot(weeks, mentions)
    plt.show()

def display_wordcloud(df, n):
    """
    Display wordcloud of n recent news
    """
    stopwords = open('Preprocess/stopword.txt', 'r')
    stopwords_list = stopwords.read().split('\n')
    
    n_recent_news = df.tail(n).copy()
    texts = []
    
    for i, row in n_recent_news.iterrows():
        title = row.title
        text = row.text
        if title is np.nan:
            title = ''
        if text is np.nan:
            text = ''
        texts.append(title + ' ' + text)
    
    texts = ' '.join(texts)
    texts = tien_xu_li(texts)
    
    wordcloud = WordCloud(stopwords=stopwords_list).generate(texts)
    plt.figure(figsize=(8,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    return n_recent_news


def display_news(df):
    df.sort_values(by=['time'], ascending=False, inplace=True)
    
    for i, row in df.iterrows():
        print('Time:', row.time)
        print('Link:', row.link)
        print('Title:', row.title)
        print()
    