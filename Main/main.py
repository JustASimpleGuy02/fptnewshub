from get_news import *
from display import *
from datetime import datetime
import time

def main():
    # get news by past n weeks 
    total_news, week2mentions = get_news_by_week()

    # update statistics every 300 seconds
    while True:
        # get most recent news
        recent_news, current_week = get_recent_news()
        
        # update to current news
        total_news = update_news(recent_news, total_news)
        week2mentions[current_week] = week2mentions.get(current_week, 0) + len(recent_news)
        
        # update and display number of mentions in line graph by week
        display_mention_statistics(week2mentions)
        
        # display most recent news' word cloud
        recent_news = get_recent_news(total_news, 30)
        display_wordcloud(recent_news)

        # display details about news   
        display_news(recent_news)
        
        time.sleep(300)

if __name__ == '__main__':
    main()