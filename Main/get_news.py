from pathlib import Path
from Utils import read_csv
from glob import glob
import os.path as osp
from crawl_real_time import crawl_by_week
import pandas as pd
import pytz
from datetime import datetime, timedelta
from dateutil.parser import parse

# now = datetime.now(pytz.utc) - timedelta(days=7)
now = datetime.now(pytz.utc) 

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
        # week = prettify_week(week)
        week2mention[week] = len(df)
    
    df_total.reset_index(drop=True, inplace=True)
    # df_total.sort_values(by=['time'], ascending=False, inplace = True)
    
    return df_total, week2mention

def get_recent_news():    
    print(now)
    df, week = crawl_by_week(now)
    df = df[df['time'].notna()]
    return df, week

def update_news(total_df, new_df):
    total_df = pd.concat([total_df, new_df]).drop_duplicates()
    total_df.sort_values(by=['time'], ascending=False, inplace = True)
    return total_df

def save_data(news: pd.DataFrame, week: str):
    out_path = osp.join(mentions_dir, week + '.csv')
    
    # if out_path exists 
    if osp.exists(out_path):
        # load csv from out_path
        old_df = read_csv(out_path)
        # old_df['time_parsed']= pd.to_datetime(old_df['time_parsed'])
        old_df = old_df[old_df['time'].notna()]
        old_df['time_parsed']= old_df['time'].apply(parse)
        # concat 2 dataframes and remove duplicates
        news = pd.concat([old_df, news]).drop_duplicates()
    
    news.to_csv(out_path, index=False)
    print("Total news:", len(news))