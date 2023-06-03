import pandas as pd

def read_csv(fpath: str):
    df = pd.read_csv(fpath)
    
    remove_col = 'Unnamed: 0'

    if remove_col in df.columns.to_list():
        df.drop(columns=remove_col, inplace=True)
        
    return df