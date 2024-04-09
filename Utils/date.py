from datetime import datetime, timedelta
from dateutil.parser import parse
import re
from pytz import timezone

imezone = timezone("Asia/Saigon")
import pytz

now = datetime.now(pytz.utc)

so_vn = ["không", "một", "hai", "ba", "tư", "năm", "sáu", "bảy", "tám", "chín"]


def get_date_str(dt: datetime):
    dt = str(dt)
    ymd = dt.split(" ")[0]
    return ymd


def get_week(dt: datetime):
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    week = get_date_str(start) + "_" + get_date_str(end)
    return start, end, week


def pop_pattern(ptn: str, text: str):
    try:
        substr = re.search(ptn, text)[0]
    except:
        substr = ""
    text = text.replace(substr, "")
    return substr, text


def clean_datetime(text: str):
    text = text.lower()

    gmt_pattern = r"(?:GMT|UTC)?[+-]\d{2}(?::\d{2})?"
    gmt = re.search(gmt_pattern, text)

    # date_pattern = "[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}"
    date_pattern = (
        r"\d{1,2}[-/]\d{1,2}[-/]\d{4}"  # dd/mm/yyyy (or dd-mm-yyyy) hh:mm
    )
    date = re.search(date_pattern, text)

    if date:
        time_pattern = r"\d{1,2}:\d{2}"
        # gmt_pattern = r"GMT[+-]\d{1,2}[:\d{1,2}]*"

        time = re.search(time_pattern, text)
        # gmt = re.search(gmt_pattern, text)

        date = date[0].replace("-", "/")
        date = "-".join(date.split("/")[::-1])

        assert date is not None

        if time is None:
            time = ["00:00"]

    elif "tháng" in text:
        month_pattern = r"tháng \d+"
        number_pattern = r"\d+"
        year_pattern = r"\d{4}"
        time_pattern = r"\d{1,2}:\d{2}"

        for idx, so in enumerate(so_vn):
            text = text.replace(so, str(idx))

        time, text = pop_pattern(time_pattern, text)
        year, text = pop_pattern(year_pattern, text)
        month, text = pop_pattern(month_pattern, text)
        month, _ = pop_pattern(number_pattern, month)
        date, _ = pop_pattern(number_pattern, text)

        date = "-".join([year, month, date])

        if len(time) == 0:
            time = ["00:00"]
        else:
            time = [time]

    if gmt is None:
        gmt = ["+0700"]

    datetime = [date, time[0], gmt[0]]
    datetime = parse(" ".join(datetime))

    return datetime


def convert2datetime(time):
    try:
        time_parsed = clean_datetime(time)
    except:
        time_parsed = parse(time)

    # localize a datetime
    if time_parsed.tzinfo is None:
        time_parsed = imezone.localize(time_parsed)

    return time_parsed


if __name__ == "__main__":
    text = "Tháng 5 ngày 20 năm 2019 8:20 GMT+09:00"
    # text = "2023-06-05"
    # text = "26, Tháng 04, 2023 | 07:15"
    # text = 'Chủ nhật, 23:27 31/01/2021'
    print(str(convert2datetime(text)))
