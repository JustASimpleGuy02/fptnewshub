# return a list of news' link from a webpage
def crawl_list_news(link, tag = None, attr = None, domain = ""):
    from bs4 import BeautifulSoup
    import requests
    
    list_link = []
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    try:
        if tag:
            article_list = soup.find_all(tag)
        elif attr:
            if type(attr) == list:
                for att in attr[:-1]:
                    soup = soup.find(attrs = att)
                article_list = soup.find_all(attrs=attr[-1])
            else:
                article_list = soup.find_all(attrs=attr)
        else:
            article_list = soup.find_all()
    except:
        print("Exception 1")
        return list_link
    # print(article_list)
    for article in article_list:
        try:
            parent_tag = article.find("a", href=True)
            href = parent_tag['href']
            # print(href)
            list_link.append(domain + href)
        except:
            continue
    return list(set(list_link))

# return text from a news page
def crawl_news_text(link_news, language = "Vietnamese",
                    time_tag = None):
    import requests
    import justext
    from bs4 import BeautifulSoup
    
    result = []
    response = requests.get(link_news)    
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title_tag = soup.find("h1")
        title = title_tag.text
    except:
        title = ""
    paragraphs = justext.justext(response.content, justext.get_stoplist(language))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            result.append(paragraph.text)
    return title, '\n'.join(result)

# print(crawl_list_news("https://uni.fpt.edu.vn/tin-tuc-su-kien/tin-tieu-diem?pagenumber=1", attr="news-item-wrapper"))
# print(len(crawl_list_news(
#     link="https://kienthuc.net.vn/search/xJHhuqFpIGjhu41jIGZwdA==/dai-hoc-fpt.html?page=2",
#     tag="",
#     attr=["cat-listnews hzol-clear", "story clearfix"],
#     domain="https://kienthuc.net.vn/"
# )))
# crawl_news_text("https://hanoi.fpt.edu.vn/mua-he-ruc-ro-chuong-trinh-tieng-anh-chuyen-sau-level-6-tai-philippines-va-malaysia.html")