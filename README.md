# AI1602 - DBP391 PROJECT

## Demo
<p align="center">
   <img src="Images/2024-04-09_17-23.png" />
</p>

<p align="center">
   <img src="Images/2024-04-09_17-23_1.png" />
</p>   

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
Tải và giải nén thư mục ở [link](https://drive.google.com/file/d/1SNaYdNTq7DUc-M_o3afE1ciY_mY8tRHX/view?usp=drive_link) rồi đặt trong thư mục của project fptunewshub.


## Running Main
```
$ streamlit run Main/index.py
```
Crawling tin tức mới nhất:
```
$ python Main/crawl.py
```

## Labelling Text
Code for Ubuntu, check the path when run in Windows
Change the path to process file
Example:
``` 
python Labelling/new_preprocess.py Mentions_By_Week/2023-06-19_2023-06-25.csv result.csv
python Labelling/label.py result.csv
```