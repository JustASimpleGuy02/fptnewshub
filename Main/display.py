import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import os.path as osp
from Preprocess.clean_text import tien_xu_li
import numpy as np
from get_news import prettify_week
import streamlit as st
import plotly.express as px
from Model.model import sentiment
from termcolor import cprint
import pandas as pd


dir_path = os.path.dirname(os.path.realpath(__file__))

text2color = {
    "Positive": "green",
    "Neutral": "yellow",
    "Negative": "red"
}


def display_mention_statistics(week2mention: dict):
    # lists = sorted(week2mention.items())
    weeks, mentions = zip(*week2mention.items())
    weeks = list(map(prettify_week, weeks))
    # fig = plt.figure( figsize=(20,10))
    fig = plt.figure( figsize=(12, 6))

    plt.plot(weeks, mentions)
    plt.title("Mentions Statistics")
    # plt.show()
    # fig = px.line(weeks, mentions)
    # st.plotly_chart(fig)
    return fig

def display_wordcloud(df_recent, n=10):
    """
    Display wordcloud of n recent news
    """
    # stopwords = open('Preprocess/stopword.txt', 'r')
    stopwords = open('Preprocess/vietnamese-stopwords.txt', 'r', encoding='UTF-8')
    stopwords_list = stopwords.read().split('\n')
    
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
    
    fig = plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.title("Wordcloud")
    plt.axis("off")
    plt.tight_layout(pad=0)
    # plt.show()
    return fig
    
def display_news(df: pd.DataFrame):
    df.sort_values(by=['time'], ascending=False, inplace=True)
    
    for _, row in df.iterrows():
        print('Time:', row.time)
        print('Link:', row.link)
        
        if not isinstance(row.title, float) and len(row.title) > 0:
            print('Title:', row.title.strip())
        
        if isinstance(row.text, float):
            print()
            continue
        
        stm = sentiment(row)
        cprint(f'Sentiment: {stm}', text2color[stm])
                
        print()
        
    
    