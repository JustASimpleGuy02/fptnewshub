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
    
    remove_col = 'Unnamed: 0'

    if remove_col in df.columns.to_list():
        df.drop(columns=remove_col, inplace=True)
        
    return df

def count_link_in_csv_dir(csv_dir):
    count = 0
    
    for fpath in glob(osp.join(csv_dir, "*.csv")):
        df = read_csv(fpath)
        count += len(df)
        
    return count


# def merge_csv(fpath1, fpath2, fpath_out):
#     df1 = read_csv(fpath1)
#     df2 = read_csv(fpath1)
    
#     df_links = pd.concat([df1, df2]).drop_duplicates()

def clean_df(df):
    df = df[df['title'].notna()]
    df = df.loc[~df["title"].str.contains("Error")]  # remove error news
    return df
