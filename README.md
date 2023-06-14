# AI1602 - DBP391 PROJECT

## Setup
```
$ conda create -n dbp python=3.8
$ conda activate dbp
$ pip install -r requirements.txt
```
### Export PYTHONPATH
Ubuntu
```
$ export PYTHONPATH=$(pwd)
```
Windows
```
(cmd) set PYTHONPATH=%PYTHONPATH%;c:\PATH\TO\PROJECT
```
## Extract Mentions by Week
Tải và giải nén thư mục ở [link](https://drive.google.com/file/d/1SNaYdNTq7DUc-M_o3afE1ciY_mY8tRHX/view?usp=drive_link) rồi đặt trong thư mục Project.
Hoặc chạy các lệnh sau với các file data đã được trích text từ các link báo ở [link](https://drive.google.com/drive/folders/15rWZJ4H4skCWS1y7iLZKf3UxEhMOjQAK?usp=drive_link):
```
$ python Preprocess/split_by_week.py Data/news_text_25_5.csv Mentions_By_Week -r
$ python Preprocess/split_by_week.py Data/news_text_26_5.csv Mentions_By_Week
$ python Preprocess/split_by_week.py Data/news_text_27_5.csv Mentions_By_Week 
...
```

## Running Main
```
$ python Main/main.py
```
