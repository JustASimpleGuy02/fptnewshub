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
Hoặc chạy lệnh sau với các file data đã được trích text từ các link báo ở [link](https://drive.google.com/drive/folders/15rWZJ4H4skCWS1y7iLZKf3UxEhMOjQAK?usp=drive_link):
```
./Preprocess/split_by_week.sh
```

## Running Main
```
$ python Main/main.py
```

## Labelling Text
Code for Ubuntu, check the path when run in Windows
Change the path to process file
Example:
``` 
python Labelling/new_preprocess.py Mentions_By_Week/2023-06-19_2023-06-25.csv result.csv
python Labelling/label.py result.csv
```