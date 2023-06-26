import streamlit as st  # pip install streamlit
import pandas as pd  # pip install pandas
import plotly.express as px  # pip install plotly-express
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
import requests as rq
from bs4 import BeautifulSoup as bs
import numpy as np
import PIL
from urllib.request import urlopen
from get_news import *
from display import *
from datetime import datetime

def main():
    st.set_page_config(page_title='FPT News Hub')
    st.title('Welcome to FPT News Hub 📈')
    st.subheader('Created by Group 3 - DBP391 Project')

    total_news, week2mentions = get_news_by_week()
    
    # recent_news, current_week = get_recent_news()
    # save_data(recent_news, current_week)
    
    current_week = '2023-06-19_2023-06-25'
    recent_news = pd.read_csv(f'Mentions_By_Week/{current_week}.csv')

    # update current news to total news
    total_news = update_news(recent_news, total_news)
    week2mentions[current_week] = week2mentions.get(current_week, 0) + len(recent_news)

    # display number of mentions in line graph by week
    mention_fig = display_mention_statistics(week2mentions)
    if mention_fig is not None:
        st.plotly_chart(mention_fig)
    else:
        st.write("Cannot plot mention_fig")

    # display most recent news' word cloud
    recent_news = total_news.head(20).copy()
    wordcloud_fig = display_wordcloud(recent_news)
    if wordcloud_fig is not None:
        st.plotly_chart(wordcloud_fig)
    else:
        st.write("Cannot plot Wordcloud")

    # display details about news
    st.divider()
    for _, row in recent_news.iterrows():
        p = st.info
        st.write('Time: ' + str(row.time))
        st.write('Link: ' + row.link)
        if not isinstance(row.title, float) and len(row.title) > 0:
            st.write('Title: ' + str(row.title).strip())
        st.divider()
        
if __name__ == '__main__':
    main()