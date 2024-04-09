import time
import argparse
from Utils import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="Split links according to datetime"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="whether to display information of crawled news",
    )
    args = parser.parse_args()
    return args


def crawl(debug: bool = False):
    # update statistics every 300 seconds
    while True:
        # get most recent news and save data
        recent_news, current_week = get_recent_news()
        save_data(recent_news, current_week)

        if debug:
            display_news(recent_news[:20].copy())

        time.sleep(300)


if __name__ == "__main__":
    args = parse_args()
    debug = args.debug

    crawl(debug)
