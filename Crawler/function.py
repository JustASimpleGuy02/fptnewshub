def read_list_webs(file_path: str):
    list_webs = []
    with open(file_path, 'r') as f:
        list_webs.append(f.readline())
    return list_webs


# return a list of news' link from a webpage
def crawl_list_news(link):
    from bs4 import BeautifulSoup, SoupStrainer
    import requests
    
    result = []
    
    raw_data = requests.get(link)
    soup = BeautifulSoup(raw_data.text, 'html.parser')
    article_list = soup.find_all("article")
    for article in article_list:
        try:
            href = article.find("a", href=True)['href']
            result.append(href)
        except:
            continue
        
    return result

# return text from a news page
def crawl_news_text(link_news):
    from bs4 import BeautifulSoup
    import requests
    
    result = []
    
    raw_data = requests.get(link_news)
    
    soup = BeautifulSoup(raw_data.text, 'html.parser')
    
    article = soup.find("article")
    
    list_paragraph = article.find_all()
    
    t = 0
    
    for paragraph in list_paragraph:
        if len(paragraph.find_all()) == 0:
            result.append(paragraph.text)
    
    return ' '.join(result)

# print(crawl_list_news('https://vnexpress.net/chu-de/dai-hoc-fpt-2161'))
# print(crawl_news_text('https://vnexpress.net/tiet-kiem-hang-tram-trieu-hoc-phi-nho-hoc-bong-mba-4606366.html'))
# print(crawl_news_text('https://hanoi.fpt.edu.vn/cuu-sinh-vien-dai-hoc-fpt-gianh-hoc-bong-tien-si-tai-phap.html'))
# print(crawl_news_text('https://hanoi.fpt.edu.vn/doc-dao-do-an-thiet-ke-bo-nhan-dien-thuong-hieu-cho-lien-doan-xiec-viet-nam-cua-sinh-vien-dai-hoc-fpt.html'))