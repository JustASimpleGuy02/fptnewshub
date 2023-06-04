from datetime import datetime, timedelta
from dateutil.parser import parse

def get_date_str(dt: datetime):
    dt = str(dt)
    ymd = dt.split(' ')[0]
    return ymd
    

def get_first_day_of_week(dt: datetime):
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    week = get_date_str(start) + '_' + get_date_str(end)
    return week

if __name__ == '__main__':
    date = parse('2023-05-26 01:05:00+00:00')
    print(get_first_day_of_week(date))
    