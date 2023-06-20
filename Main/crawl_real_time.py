import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from Crawler import crawl_news_text
import json
from Utils import get_week, convert2datetime, read_csv
import pandas as pd
import os.path as osp
from tqdm import tqdm
from icecream import ic

domain_time_map = json.load(open("Crawler/domain_time_map.json"))

def crawl_real_time(term:str = "đại học fpt", 
                    start_date: datetime = None, 
                    end_date: datetime = None):
    
    list_link = []
    
    page = 1
    
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    try:
        while True:
            url = 'https://www.google.com/search?q="{}"&tbm=nws&tbs=cdr:1,cd_min:{},cd_max:{}&num=100&start={}'.format(
                "+".join(term.lower().split(" ")),
                start_date.strftime("%m/%d/%Y") if start_date is not None else "",
                end_date.strftime("%m/%d/%Y") if end_date is not None else "",
                (page - 1) * 100
            )
            
            response = requests.get(url=url,
                                    headers=headers)
            
            soup = BeautifulSoup(response.text, 'html.parser')
        
            article_list = soup.find_all(attrs="SoaBEf")
            
            if len(article_list) == 0:
                break
            
            for article in article_list:
                try:
                    parent_tag = article.find("a", href=True)
                    href = parent_tag['href']
                    list_link.append(href)
                except:
                    continue
            
            time.sleep(10)
            
            article_list = []
            page += 1
    except Exception as e:
        print(e)
        return list(set(list_link))
        
    return list(set(list_link))

def crawl_by_week(date: datetime):
    # get week of current date
    start, end, week = get_week(date)
    
    # crawl realtime then save to csv
    recent_news = crawl_real_time(start_date=start, end_date=end)
    print('Number of crawled news:', len(recent_news))
    
    df = pd.DataFrame(columns=["link", "title", "time", "text", "sentiment"])
    for link in tqdm(recent_news):
        title, time, text = crawl_news_text(link, domain_time_map)
        if time == "":
            time = None
        # time_parsed = convert2datetime(time) if time is not None else date
        # ic(time_parsed)
        df.loc[len(df.index)] = [link, title, time, text, ""]

    df['time'].fillna(method='ffill', inplace=True)
    return df, week

if __name__ == '__main__':
    # now = datetime(2023, 6, 1)
    # df, week = crawl_by_week(now)
    # out_path = osp.join('Mentions_By_Week', week+'.csv')
    # df.to_csv(out_path, index=False)


    print(len(crawl_real_time(start_date=datetime(2023,6,1), \
                                    end_date=datetime(2023,6,10))))

    