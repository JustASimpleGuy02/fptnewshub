import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Labelling text from csv file")
    parser.add_argument('ifile', help='input csv file which has cleaned texts')
    parser.add_argument('ofile', help='output csv file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    ifile = args.ifile
    ofile = args.ofile
    
    #Tạo file csv chứa text và cột dữ liệu có negative hay không
    df = pd.read_csv(ifile)
    new_df = pd.DataFrame({'Text': df['Cleaned_Content'], 'Negative': ''})
    
    new_df.to_csv(ofile)
