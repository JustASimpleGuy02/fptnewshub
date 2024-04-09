# return a list of news' link from a webpage
def crawl_list_news(link, tag=None, attr=None, domain="", result_end=""):
    from bs4 import BeautifulSoup
    import requests

    list_link = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(link, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    try:
        if tag:
            article_list = soup.find_all(tag)
        elif attr:
            if type(attr) == list:
                for att in attr[:-1]:
                    soup = soup.find(attrs=att)
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
            href = parent_tag["href"]
            # print(href)
            if len(result_end) > 0 and not (domain + href).endswith(
                result_end
            ):
                continue
            list_link.append(domain + href)
        except:
            continue
    return list(set(list_link))


def crawl_list_news_gg(domain, page, result_end=""):
    from bs4 import BeautifulSoup
    import requests

    list_link = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    response = requests.get(
        "https://www.google.com/search?q=đại+học+fpt+site:{}&num=100&start={}".format(
            domain, (page - 1) * 100
        ),
        headers=headers,
    )
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    article_list = soup.find_all(attrs="yuRUbf")
    for article in article_list:
        try:
            parent_tag = article.find("a", href=True)
            href = parent_tag["href"]
            # print(href)
            if len(result_end) > 0 and not (domain + href).endswith(
                result_end
            ):
                continue
            list_link.append(href)
        except:
            continue
    return list(set(list_link))


# return text from a news page
def crawl_news_text(
    link_news: str, domain_time_map: dict, language="Vietnamese"
):
    import requests
    import justext
    from bs4 import BeautifulSoup
    from htmldate import find_date

    result = []
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
    try:
        response = requests.get(link_news, headers=headers, timeout=300)
    except:
        return "", "", ""
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title_tag = soup.find("h1")
        title = title_tag.text
    except:
        title = ""
    time = ""
    try:
        time = find_date(link_news)
    except Exception as e:
        print(e)
    # for domain in domain_time_map.keys():
    #     if link_news.startswith(domain):
    #         time_tag_attr = domain_time_map[domain]
    #         if "tag" in time_tag_attr.keys():
    #             time_tag = soup.find(time_tag_attr["tag"])
    #             try:
    #                 time = time_tag["datetime"]
    #             except:
    #                 try:
    #                     time = time_tag.text
    #                 except:
    #                     time = ""
    #         elif "attr" in time_tag_attr.keys():
    #             try:
    #                 if type(time_tag_attr["attr"]) == list:
    #                     tag = soup
    #                     for attr in time_tag_attr["attr"][:-1]:
    #                         tag = tag.find(attrs=attr)
    #                     time_tag = tag.find(attrs=time_tag_attr["attr"][-1])
    #                 else:
    #                     time_tag = soup.find(attrs=time_tag_attr["attr"])
    #                 try:
    #                     time = time_tag["datetime"]
    #                 except:
    #                     time = time_tag.text
    #             except:
    #                 time = ""
    #         break
    try:
        paragraphs = justext.justext(
            response.content, justext.get_stoplist(language)
        )
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                result.append(paragraph.text)
    except:
        result = [""]
    return title, time, "\n".join(result)
