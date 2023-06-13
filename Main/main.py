from get_news import *
from display import *
from datetime import datetime

def main():
    df_news, weeks, mentions = get_news_by_week()
    # recent_news = get_recent_news()

    display_statistics(weeks, mentions)
    
    recent_news = get_recent_news(df_news, 10)
    display_wordcloud(recent_news)
    
    display_news(recent_news)

if __name__ == '__main__':
    main()