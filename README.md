# AI1602 - DBP391 PROJECT: 
# Tổng hợp và phân loại tin tức về ĐH FPT trên báo điện tử, forum, blog.

## Setup
```
$ pip install -r requirements.txt
```

## Save all crawled links to a file
```
$ python Crawler/get_links.py \
    ${PROJECT_DIR}/Crawler/data/list_webs.txt \
    ${PROJECT_DIR}/Crawler/data/crawled_urls.txt
```

## Save all crawled links to a file
```
$ python Crawler/crawl_txt.py \
    ${PROJECT_DIR}/Crawler/data/crawled_urls.txt \
    ${PROJECT_DIR}/Crawler/data/crawled.csv
```
