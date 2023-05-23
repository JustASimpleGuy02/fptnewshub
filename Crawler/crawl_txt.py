from bs4 import BeautifulSoup
from utils.crawl import read_list_webs, crawl_list_news, crawl_news_text
import os.path as osp
import argparse
import pandas as pd
from utils.io import *
from tqdm import tqdm
from icecream import ic
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def parse_args():
    parser = argparse.ArgumentParser(description="Crawling texts")
    parser.add_argument("input_file", type=str, help="file including urls to crawl text from")
    parser.add_argument("output_file", type=str, help="csv file to save crawled texts")
    # parser.add_argument("-r", "--restar", action='store_true')
    args = parser.parse_args()
    return args

def add_to_df(df, url):
    txt = crawl_news_text(url)
    new_row = {'Url': url, 'Text': txt}
    df.loc[len(df) + 1] = new_row

if __name__ == '__main__':
    args = parse_args()
    ifile = args.input_file
    ofile = args.output_file
    # restart = args.restart
        
    df = pd.DataFrame(columns=['Url', 'Text'])
    
    # Rearranging index
    df.index = np.arange(1, len(df) + 1)
    
    list_webs = read_list_webs(ifile)
    unq_webs = list(set(list_webs))
    
    # print("Number of webs to crawl text:", len(unq_webs))
    
    t1 = time.time()
    for url in tqdm(unq_webs):
        txt = crawl_news_text(url)
        new_row = {'Url': url, 'Text': txt}
        df.loc[len(df) + 1] = new_row
    t2 = time.time()
    
    # t1 = time.time()
    # with ThreadPoolExecutor(n_threads) as executor:
    #         _ = [executor.submit(add_to_df, df, url)
    #                     for url in tqdm(unq_webs)]
    # t2 = time.time()

    print("Number of webs to crawl text:", len(df))
    print(f"Crawling time: {t2-t1:.2f}s")
    
    df.to_csv(ofile)

    