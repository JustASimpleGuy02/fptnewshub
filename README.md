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
## Clean Text Data
```
$ python Preprocess/clean_text.py ${PATH_TO_DATA_FILE} ${OUTPUT_FILE}
```

Example: 
``` 
$ python Preprocess/clean_text.py data/news_text_25_5.csv text_cleaned_25_5.csv
```

## Labelling Text
```
$ python Labelling/preprocess.py ${PATH_TO_DATA_FILE} ${OUTPUT_FILE}
$ python Labelling/main.py ${PATH_TO_DATA_FILE} ${RESUME_INDEX_FILE}
```

Example: 
``` 
$ python Labelling/preprocess.py Cleaned_Data/cleaned_text_25_5.csv labelling_text_25_5.csv
$ python Labelling/main.py labelling_text_25_5.csv resume.txt
```
Label lại từ đầu:
``` 
$ rm resume.txt
$ python Labelling/main.py labelling_text_25_5.csv -r
```

## Running Main
```
& python Main/main.py
```
