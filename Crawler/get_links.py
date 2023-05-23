from bs4 import BeautifulSoup
from utils.crawl import read_list_webs, crawl_list_news, crawl_news_text
import os.path as osp
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Add links to crawl")
    parser.add_argument("input_file", type=str, help="file including to get other links")
    parser.add_argument("output_file", type=str, help="file to save crawled links")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    ifile = args.input_file
    ofile = args.output_file
    
    list_webs = read_list_webs(ifile)
    
    res = []
    for web in list_webs:
        links = crawl_list_news(web)
        print(len(links))
        for link in links: 
            res.append(link)
            
    print(res)
    print(len(res))
    
    with open(ofile, "w", encoding='utf-8') as f:
        for link in res:
            f.write(str(link)+'\n')
        f.close()