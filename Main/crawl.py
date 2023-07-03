import time
import argparse
from Utils import *

# now = datetime.now(pytz.utc) - timedelta(days=7)
now = datetime.now(pytz.utc) 

def get_recent_news():    
    """Crawl the latest news and remove news with some preprocess

    Returns:
        df: DataFrame of news with their attributes
        week: week including the news
    """
    df, week = crawl_by_week(now)
    df = clean_df(df)
    return df, week

def update_news(total_df, new_df):
    total_df = pd.concat([total_df, new_df]).drop_duplicates()
    total_df.sort_values(by=['time'], ascending=False, inplace = True)
    return total_df

def save_data(news: pd.DataFrame, week: str):
    """Save latest articles to database

    Args:
        news (pd.DataFrame): DataFrame including news to save
        week (str): the week of the saved news
        
    Returns:
        news: DataFrame of all the news in week
    """
    out_path = osp.join(mentions_dir, week + '.csv')
    
    # if out_path exists 
    if osp.exists(out_path):
        # load csv from out_path
        old_df = pd.read_csv(out_path)
        old_df = old_df[old_df['time'].notna()]
        # old_df['time_parsed']= old_df['time'].apply(parse)
        
        # concat 2 dataframes and remove duplicates
        news = pd.concat([old_df, news]).drop_duplicates()

    # Sort all the news by time
    news.sort_values(by=['time'], ascending=False, inplace = True)    
    
    news.to_csv(out_path, index=False)
    print(f"Total number of news in week {week}:", len(news))
        
    return news


def crawl(debug: bool = False):
    # update statistics every 300 seconds
    while True:
        # get most recent news and save data
        recent_news, current_week = get_recent_news()
        save_data(recent_news, current_week)
        
        if debug:
            display_news(recent_news[:20].copy(), debug=debug)
            
        time.sleep(300)

def parse_args():
    parser = argparse.ArgumentParser(description="Split links according to datetime")
    parser.add_argument('-d', '--debug', action='store_true', help='whether to display information of crawled news')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    debug = args.debug
    
    crawl(debug)