import streamlit as st  # pip install streamlit
from icecream import ic
from Utils import *

def main():
    st.set_page_config(page_title='FPT News Hub')
    st.title('Welcome to FPT News Hub 📈')
    st.subheader('Created by Group 3 - DBP391 Project')

    # count number of articles by past n weeks, default n = 5
    recent_news, week2mentions = get_news_by_week()

    # display number of mentions in line graph by week
    display_mention_statistics(week2mentions)

    # display most recent news' word cloud
    display_wordcloud(recent_news)

    # display details about news
    display_news(recent_news)
        
if __name__ == '__main__':
    main()