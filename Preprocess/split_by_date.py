import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from tqdm import tqdm

def convert_datetime(time: str):
    format = '%d/%m/%Y %H:%M %z' 

    time = time.replace(',', '')
    time = time.split(' ')
    date_time = time[2] + ' ' + time[3] + ' ' + '+0700'
    
    date_time_python = datetime.strptime(date_time, format)
    return date_time_python

def get_first_date_of_week(time: str):
    ymd = time.split(' ')[0].split('-')
    start_date = ymd[2] + '_' + ymd[1]
    return start_date

def parse_args():
    parser = argparse.ArgumentParser(description="Split links according to datetime")
    parser.add_argument('ifile', help='input csv file')
    parser.add_argument('odir', help='output folder path')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    ifile = args.ifile
    odir = args.odir
    
    ### Get today's time, first day, and last day of week
    now = datetime.now()
    start_week = now - timedelta(days=now.weekday())
    end_week = start_week + timedelta(days=6)
    print(start_week)    

    ### Get last week's first day, and last week's last day
    start_last_week = start_week - timedelta(days=7)
    end_last_week = end_week - timedelta(days=7)
    print(start_last_week)    
    
    ### Read csv files
    df = pd.read_csv(ifile)
    print('Original number of links:', len(df))
    
    ## Remove unecessary column
    remove_col = 'Unnamed: 0'

    if remove_col in df.columns.to_list():
        df.drop(columns=remove_col, inplace=True)
        
    ## Drop nan time
    df = df[df['time'].notna()]
    print('Remaining number of links:', len(df))
        
    ### Convert time to datetime
    for idx, row in tqdm(df.iterrows()):
        try:
            row.time = parse(row.time)
        except:
            row.time = convert_datetime(row.time)
            
    df.sort_values(by=['time'], ascending = False, inplace = True)

    print(df.head())    

