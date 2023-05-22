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
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_list = soup.find_all("article")
    for article in article_list:
        try:
            href = article.find("a", href=True)['href']
            result.append(href)
        except:
            continue
    return result

# return text from a news page
def crawl_news_text(link_news, language = "Vietnamese"):
    import requests
    import justext
    
    result = []
    response = requests.get(link_news)    
    paragraphs = justext.justext(response.content, justext.get_stoplist(language))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            result.append(paragraph.text)
    return '\n'.join(result)

# print(crawl_list_news('https://vnexpress.net/chu-de/dai-hoc-fpt-2161'))
# print(crawl_news_text('https://vnexpress.net/tiet-kiem-hang-tram-trieu-hoc-phi-nho-hoc-bong-mba-4606366.html'))