from pathlib import Path
from glob import glob
import os.path as osp
import pandas as pd
from dateutil.parser import parse
from icecream import ic
from .utils import clean_df
from typing import Tuple

dir_name = 'Mentions_By_Week'
mentions_dir = str(Path(__file__).parent.parent / dir_name)

def prettify_week(week: str):
    """Change week to usual format: dd//mm/yyyy

    Args:
        week (str): input week

    Returns:
        week: the week changed to its format
    """
    # week = ['/'.join(w.split('-')[::-1]) for w in week.split('_')]
    week = ['/'.join(w.split('-')) for w in week.split('_')]
    week = '-'.join(week)
    return week


def get_news_by_week(past_n_week=4, n_recent=40) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Accumulate and sort by time al the articles from the most recent weeks 

    Args:
        past_n_week (int, optional): The number of past weeks to get news. Defaults to 5.

    Returns:
        df_total: DataFrame which includes all the most recent articles
        week2mention: DataFrame which maps week to number of articles
    """    
    csv_files = glob(mentions_dir + '/*.csv')
    df_total = pd.DataFrame(columns=['link', 'time', 'title', 'text', 'sentiment'])
    week2mention = pd.DataFrame(columns=["week", "mentions"])
    
    count = 0
    
    # read from each csv files of the past weeks
    for fpath in sorted(csv_files)[:-(past_n_week+1):-1]:  
        week = osp.basename(fpath).split('.')[0]
        start_week, _ = week.split('_')
        
        # read and preprocess
        df = pd.read_csv(fpath)
        # df.drop(columns=['time'], inplace=True)
        # df.rename(columns={'time_parsed': 'time'}, inplace=True)
        df = clean_df(df)
        
        # in case news with date not in current week
        df = df[df['time'] >= start_week]
        
        # if the number of recent news is not enough
        if count < n_recent:
            df_total = pd.concat([df_total, df])
            count += len(df)
        
        # accumulate the name and the 
        # number of mentions in each csv file
        week2mention.loc[len(week2mention.index)] = [week, len(df)]
    
    df_total.reset_index(drop=True, inplace=True)
    df_total.sort_values(by=['time'], ascending=False, inplace = True)
    df_total = df_total[:n_recent]
    
    return df_total, week2mention

