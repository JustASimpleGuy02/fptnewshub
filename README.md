AI1602 - DBP391 PROJECT

## Setup
```
$ conda create -n dbp python=3.8
$ conda activate dbp
$ pip install -r requirements.txt
```

## Clean Text Data
```
$ python Preprocess/clean_text.py ${PATH_TO_DATA_FILE} ${OUTPUT_FILE}
```

Example: 
``` 
$ python Preprocess/clean_text.py data/news_text_25_5.csv text_cleaned_25_5.csv
```