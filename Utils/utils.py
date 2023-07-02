import pandas as pd
import re
from dateutil.parser import parse
from glob import glob
import os.path as osp

def read_csv(fpath: str):
    df = pd.read_csv(fpath, 
                    #  encoding='latin-1', 
                     on_bad_lines='skip',
                     lineterminator='\n',
                     )
    
    for column in df.columns.to_list():
        if 'Unnamed' in column:
            df.drop(columns=column, inplace=True)
    
    if 'link' in df.columns.to_list():
        df.drop_duplicates(subset=['link'], inplace=True)
        
    return df

def count_link_in_csv_dir(csv_dir):
    count = 0
    
    for fpath in glob(osp.join(csv_dir, "*.csv")):
        df = read_csv(fpath)
        count += len(df)
        
    return count

def clean_df(df):
    df = df[df['time'].notna()]
    df = df[df['title'].notna()]
    df = df.loc[~df["title"].str.contains("Error")]  # remove error news
    df.reset_index(drop=True, inplace=True)
    return df
