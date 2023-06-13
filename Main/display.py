import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import os.path as osp
from Preprocess.clean_text import tien_xu_li
import numpy as np
from get_news import get_recent_news
import streamlit as st
import plotly.express as px


dir_path = os.path.dirname(os.path.realpath(__file__))

def display_statistics(weeks, mentions):
    plt.figure( figsize=(20,10))
    plt.plot(weeks, mentions)
    plt.title("Mentions Statistics")
    plt.show()
    # fig = px.line(weeks, mentions)
    # st.plotly_chart(fig)

def display_wordcloud(df_recent, n=10):
    """
    Display wordcloud of n recent news
    """
    # stopwords = open('Preprocess/stopword.txt', 'r')
    stopwords = open('Preprocess/vietnamese-stopwords.txt', 'r')
    stopwords_list = stopwords.read().split('\n')
    
    n_recent_news = get_recent_news(df_recent, n)
    texts = []
    
    for i, row in df_recent.iterrows():
        title = row.title
        text = row.text
        if title is np.nan:
            title = ''
        if text is np.nan:
            text = ''
        texts.append(title + ' ' + text)
    
    texts = ' '.join(texts)
    texts = tien_xu_li(texts)
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        stopwords=stopwords_list, 
        background_color='white'
    ).generate(texts)
    
    # st.plotly_chart(wordcloud)
    
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.title("Wordcloud")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
    
def display_news(df):
    df.sort_values(by=['time'], ascending=False, inplace=True)
    
    for i, row in df.iterrows():
        print('Time:', row.time)
        print('Link:', row.link)
        print('Title:', row.title)
        print()
    