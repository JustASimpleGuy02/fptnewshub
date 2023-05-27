# return a list of news' link from a webpage
def crawl_list_news(link, tag = None, attr = None, domain = ""):
    from bs4 import BeautifulSoup
    import requests
    
    list_link = []
    headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    response = requests.get(link, headers=headers)
    # print(response.text)
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
def crawl_news_text(link_news: str, domain_time_map: dict,
                    language = "Vietnamese"):
    import requests
    import justext
    from bs4 import BeautifulSoup
    
    result = []
    headers = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    response = requests.get(link_news, headers=headers)    
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title_tag = soup.find("h1")
        title = title_tag.text
    except:
        title = ""
    for domain in domain_time_map.keys():
        if link_news.startswith(domain):
            time_tag_attr = domain_time_map[domain]
            if "tag" in time_tag_attr.keys():
                time_tag = soup.find(time_tag_attr["tag"])
                try:
                    time = time_tag["datetime"]
                except:
                    try:
                        time = time_tag.text
                    except:
                        time = ""
            else:
                time_tag = soup.find(attrs=time_tag_attr["attr"])
                try:
                    time = time_tag["datetime"]
                except:
                    try:
                        time = time_tag.text
                    except:
                        time = ""
            break
    paragraphs = justext.justext(response.content, justext.get_stoplist(language))
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            result.append(paragraph.text)
    return title, time, '\n'.join(result)

# print((crawl_list_news(
#     link="https://fsb.edu.vn/tin-fsb-e252.html",
#     tag=None,
#     attr="col-xs-12 col-sm-12 col-md-12 col-lg-12 list_blog_txt",
#     domain=""
# )))

# import json
# print(crawl_news_text("https://chungta.vn/nguoi-fpt/vong-tranh-tai-top-50-fpt-under-35-thay-doi-the-thuc-1136839.html",
#                       domain_time_map=json.load(open("domain_time_map.json")))[1])