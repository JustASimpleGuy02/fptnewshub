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

## Running Main
```
$ streamlit run Main/index.py
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