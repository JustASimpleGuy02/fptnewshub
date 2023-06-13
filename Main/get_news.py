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

def get_news_by_week(past_n_week=5):
    csv_files = glob(mentions_dir + '/*.csv')
    df_total = pd.DataFrame(columns=['link', 'time', 'title', 'text'])
    week2mention = {}
    
    # read from each csv files
    for fpath in sorted(csv_files)[-past_n_week:]:
        # read and preprocess
        df = pd.read_csv(fpath)
        df.drop(columns=['time'], inplace=True)
        df.rename(columns={'time_parsed':'time'}, inplace=True)
        
        # concat each csv file
        df_total = pd.concat([df_total, df])
        
        # accumulate the name and the 
        # number of mentions in each csv file
        week = osp.basename(fpath).split('.')[0]
        week = prettify_week(week)
        week2mention[week] = week2mention.get(week, 0) + 1
    
    df_total.reset_index(drop=True, inplace=True)
    df_total.sort_values(by=['time'], ascending=False, inplace = True)
    
    return df_total, week2mention

def get_recent_news(df, n):    
    n_recent_news = df.head(n).copy()
    return n_recent_news

def update_news(total_df, new_df):
    pass
    