import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests

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
                end_date.strftime("%m/%d/%Y") if start_date is not None else "",
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

# print(len(crawl_real_time(start_date=datetime(2023, 6, 1),
#                           end_date=datetime(2023, 6, 8))))