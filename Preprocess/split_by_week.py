import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from tqdm import tqdm
from Utils.utils import *
from pytz import timezone
from icecream import ic

imezone = timezone("Asia/Saigon")


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
    
    ### Read csv files
    df = read_csv(ifile)
    print('Original number of links:', len(df))
        
    ## Drop nan time
    df = df[df['time'].notna()]
    print('Remaining number of links:', len(df))
        
    ### Convert time to datetime
    for idx, row in tqdm(df.iterrows()):
        time = row.time

        try:
            time_parsed = parse(time)
        except:
            time_parsed = extract_datetime(time)
        
        # localize a datetime 
        if time_parsed.tzinfo is None:
            time_parsed = imezone.localize(time_parsed)
            
        row.time  = time_parsed
    
    df.sort_values(by=['time'], ascending = False, inplace = True)

    print(df.head())    

