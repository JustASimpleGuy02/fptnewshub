from get_news import *
from display import *

def main():
    df_news, weeks, mentions = get_news_by_week()
    # recent_news = get_recent_news()

    display_statistics(weeks, mentions)
    recent_news = display_wordcloud(df_news, 10)
    display_news(recent_news)

if __name__ == '__main__':
    main()