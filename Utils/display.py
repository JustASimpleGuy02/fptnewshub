import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import os.path as osp
from Preprocess.clean_text import tien_xu_li
import numpy as np
from Utils.extract_news import prettify_week
import streamlit as st
import plotly.express as px
from Model.model import sentiment
from termcolor import cprint
import pandas as pd
from PIL import Image


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
    st.plotly_chart(fig)

def display_wordcloud(df_recent, n=10):
    """
    Display wordcloud of n recent news
    """
    # stopwords = open('Preprocess/stopword.txt', 'r')
    stopwords = open('Preprocess/vietnamese-stopwords.txt', 'r', encoding='UTF-8')
    stopwords_list = stopwords.read().split('\n')
    
    texts = []
    
    for _, row in df_recent.iterrows():
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
        
    fig = plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.title("Wordcloud")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("/home/dungmaster/Study/DBP391/Project/fptnewshub/Images/wordcloud.png")
    image = Image.open('/home/dungmaster/Study/DBP391/Project/fptnewshub/Images/wordcloud.png')
    st.image(image, caption='Wordcloud')
    
def print_news(df: pd.DataFrame, debug=False):
    df.sort_values(by=['time'], ascending=False, inplace=True)
    
    for _, row in df.iterrows():
        print('Time:', row.time)
        print('Link:', row.link)
        
        title = str(row.title).strip()
        if not isinstance(title, float) and len(title) > 0:
            print('Title: ' + title)
        
        if isinstance(row.text, float):
            print()
            continue
        
        if debug:
            stm = sentiment(row)
            cprint(f'Sentiment: {stm}', text2color[stm])
                
        print()
        
        
def display_news(recent_news: pd.DataFrame):
    st.divider()
    for _, row in recent_news.iterrows():
        st.write('Time: ' + str(row.time))
        st.write('Link: ' + row.link)
        
        title = str(row.title).strip()
        if not isinstance(title, float) and len(title) > 0:
            st.write('Title: ' + title)
            
        st.divider()
    
    