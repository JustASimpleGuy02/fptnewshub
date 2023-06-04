from pathlib import Path
from Utils import read_csv
from glob import glob
import os.path as osp

import pandas as pd

mentions_dir = str(Path(__file__).parent.parent / 'Mentions_By_Week')

def prettify_week(week: str):
    week = ['/'.join(w.split('-')[::-1]) for w in week.split('_')]
    week = '-'.join(week)
    return week

def get_news_by_week():
    csv_files = glob(mentions_dir + '/*.csv')
    df_total = pd.DataFrame(columns=['link', 'time', 'title', 'text'])
    weeks = []
    mentions_by_weeks = []
    
    # read from each csv files
    for fpath in sorted(csv_files):
        # read and preprocess
        df = pd.read_csv(fpath)
        df.drop(columns=['time'], inplace=True)
        df.rename(columns={'time_parsed':'time'}, inplace=True)
        
        # concat each csv file
        df_total = pd.concat([df_total, df])
        
        # accumulate the name and the 
        # number of mentions in each csv file
        week = osp.basename(fpath).split('.')[0]
        weeks.append(prettify_week(week))
        mentions_by_weeks.append(len(df))
        
    # sort the final csv file by datetime
    # df_total.sort_values(by=['time'], ascending=True, inplace = True)
    df_total.reset_index(drop=True, inplace=True)
    
    return df_total, weeks, mentions_by_weeks

def get_recent_news():
    # crawl recent news
    
    pass