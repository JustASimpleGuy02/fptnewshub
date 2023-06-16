from get_news import *
from display import *
from datetime import datetime
import time

def main():
    # get news by past n weeks 
    total_news, week2mentions = get_news_by_week()

    # update statistics every 300 seconds
    while True:
        # get most recent news and save data
        # one thread
        recent_news, current_week = get_recent_news()
        
        # current_week = '2023-06-12_2023-06-18'
        # recent_news = pd.read_csv(f'Mentions_By_Week/{current_week}.csv')
        
        save_data(recent_news, current_week)
        
        # update current news to total news
        total_news = update_news(recent_news, total_news)
        week2mentions[current_week] = week2mentions.get(current_week, 0) + len(recent_news)
        
        # display number of mentions in line graph by week
        display_mention_statistics(week2mentions)
        
        # display most recent news' word cloud
        recent_news = total_news.head(20).copy()
        display_wordcloud(recent_news)

        # display details about news   
        display_news(recent_news)
        
        time.sleep(300)

if __name__ == '__main__':
    main()