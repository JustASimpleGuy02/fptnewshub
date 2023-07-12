import streamlit as st  # pip install streamlit
from icecream import ic
from Utils import *

def main():    
    display_headings()

    # count number of articles by past n weeks, default n = 5
    recent_news, week2mentions = get_news_by_week()

    col1, col2 = st.columns(2)
    
    with col1:
        # display number of mentions in line graph by week
        display_mention_statistics(week2mentions)

    with col2:
        # display most recent news' word cloud
        display_wordcloud(recent_news)

    # display details about news
    st_display_news(recent_news)
        
        
if __name__ == '__main__':
    main()