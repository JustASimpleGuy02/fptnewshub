def read_list_webs(file_path: str):
    list_webs = []
    with open(file_path, 'r') as f:
        for line in f:
            list_webs.append(line.strip())
    return list_webs


# return a list of news' link from a webpage
def crawl_list_news(link, page_limit=20):
    from bs4 import BeautifulSoup, SoupStrainer
    import requests

    result = []
    page = 1
    use_page_format = True  # Start with the /page/ format
    
    while True:
        # Determine the URL format to use for the current page
        if use_page_format:
            page_url = f"{link}/page/{page}" if page > 1 else link
        else:
            page_url = f"{link}-p{page}" if page > 1 else link
        
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_list = soup.find_all("article")
        
        for article in article_list:
            try:
                href = article.find("a", href=True)['href']
                result.append(href)
            except:
                continue
        
        # Break the loop if the page limit is reached or there are no more pages
        if page_limit and page >= page_limit or not article_list:
            break
        
        # Switch to the alternate URL format if the current format fails
        if page == 1 and not article_list:
            use_page_format = not use_page_format
        
        page += 1

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