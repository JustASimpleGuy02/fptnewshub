def read_list_webs(file_path: str):
    list_webs = []
    with open(file_path, 'r') as f:
        list_webs.append(f.readline())
    return list_webs

def crawl_list_news(link):
    from bs4 import BeautifulSoup, SoupStrainer
    import requests
    
    raw_data = requests.get(link)
    soup = BeautifulSoup(raw_data.text, 'html.parser')
    article_list = soup.find_all("article")
    for article in article_list:
        try:
            print(article.find("a", href=True)['href'])
        except:
            continue

# crawl_list_news('https://vnexpress.net/chu-de/dai-hoc-fpt-2161')