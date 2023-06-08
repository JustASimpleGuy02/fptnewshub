import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from tqdm import tqdm
from Utils import *
from icecream import ic
from collections import defaultdict
import pytz

now = datetime.now(pytz.utc)

# only get links from the past 5 weeks
past_limit = now - timedelta(weeks=5)

def parse_args():
    parser = argparse.ArgumentParser(description="Split links according to datetime")
    parser.add_argument('ifile', help='input csv file')
    parser.add_argument('odir', help='output folder path')
    parser.add_argument('-r', '--restart', action='store_true', help='restart output dir')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    ifile = args.ifile
    odir = args.odir
    restart = args.restart
    
    start_dir(odir, restart)
    
    ### Read csv files
    df = read_csv(ifile)
    print('Original number of links:', len(df))
        
    ## Drop nan time
    df = df[df['time'].notna()]
    print('Remaining number of links:', len(df))
    
    week2links = defaultdict(list)
    
    ### Convert time to datetime
    for idx, row in tqdm(df.iterrows()):
        time = row.time

        time_parsed = convert2datetime(time)

        if time_parsed < past_limit:
            continue
        
        # get first and end day of week of the current time
        week = get_week(time_parsed)
        
        # store link, date, text of the day in the dictionary with week the corresponding key
        link_meta = {'link': row.link,
                     'title': row.title,
                     'time': time.strip(),
                     'time_parsed': time_parsed,
                     'text': row.text}
        week2links[week].append(link_meta)
        
    count = 0 
    # in each week sort the link by time and save to a csv
    for week, links_list in tqdm(week2links.items()):
        df_links = pd.DataFrame(links_list)
        
        out_path = osp.join(odir, week+'.csv')
        
        # if out_path exists 
        if osp.exists(out_path):
            # load csv from out_path
            old_df = read_csv(out_path)
            old_df['time_parsed']= pd.to_datetime(old_df['time_parsed'])
            # concat 2 dataframes and remove duplicates
            df_links = pd.concat([old_df, df_links]).drop_duplicates()
                        
        df_links.sort_values(by=['time_parsed'], ascending=False, inplace = True)
        df_links.reset_index(drop=True, inplace=True)

        df_links.to_csv(out_path, index=False)
        
        count += len(df_links)
        
    print('Number of links:', count)
        
    
    

