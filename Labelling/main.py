import pandas as pd
import argparse
import os.path as osp
from Utils.utils import *
from termcolor import cprint

def parse_args():
    parser = argparse.ArgumentParser(description="Labelling text from csv file")
    parser.add_argument('ifile', help='input csv file which has cleaned texts')
    parser.add_argument('index_file', help='resume index file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    ifile = args.ifile
    resume_file = args.index_file
    
    # Read the input CSV file
    df = read_csv(ifile)

    # Check if there is a resume index file
    resume_index = 0
    try:
        with open(resume_file, 'r') as file:
            resume_index = int(file.read().strip())
            if resume_index >= len(df):
                resume_index = 0
    except FileNotFoundError:
        pass


    # Iterate over each row and prompt the user for input
    for index, row in df.iterrows():
        if index < resume_index:
            continue  # Skip already processed lines
        
        cprint(f"Line: {index + 1}", 'red')
        cprint(f"Text: {row['Text']}", 'green')

        # Check if 'Negative' field is already filled
        if pd.notna(row['Negative']):
            print("Negative field already filled:", row['Negative'])
            print()
            continue
        
        #Điền xem thông tin có nội dung tiêu cực hay không (1 là có và 0 là không)
        while True:
            negative = input("Enter the value for 'Negative' field (0 or 1): ")

            # Validate the input
            if negative in ['0', '1']:
                break
            else:
                print("Invalid input. Please enter 0 or 1.")

        # Update the 'Negative' field in the DataFrame
        df.at[index, 'Negative'] = negative

        # Save the index for resuming later
        resume_index = index + 1

        # Save the DataFrame and resume index to files
        df.to_csv(ifile, index=False)
        with open(resume_file, 'w') as file:
            file.write(str(resume_index))

        print()

    print("All lines processed and saved successfully.")