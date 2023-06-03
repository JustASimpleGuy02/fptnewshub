import pandas as pd
import re
from dateutil.parser import parse


def read_csv(fpath: str):
    df = pd.read_csv(fpath)
    
    remove_col = 'Unnamed: 0'

    if remove_col in df.columns.to_list():
        df.drop(columns=remove_col, inplace=True)
        
    return df

def extract_datetime(text: str):
    date_pattern = "[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}"
    time_pattern = "[0-9]{2}:[0-9]{2}"
    gmt_pattern = r"GMT[+-]\d{1,2}[:\d{1,2}]*"

    date = re.search(date_pattern, text)
    time = re.search(time_pattern, text)
    gmt = re.search(gmt_pattern, text)
    
    date = '-'.join(date[0].split('/')[::-1])
    
    assert date is not None
    assert time is not None

    if gmt is None:
        gmt = ['+0700']
    
    datetime = [date, time[0], gmt[0]]
    datetime = parse(' '.join(datetime))

    return datetime
