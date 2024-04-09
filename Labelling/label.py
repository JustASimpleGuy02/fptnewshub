import argparse
import pandas as pd
from termcolor import cprint


def continue_label():
    while True:
        try:
            option = int(input("Resume labelling? (0 or 1): "))
        except:
            print("Invalid input. Please enter an integer.")

        # Validate the input
        if option in [0, 1]:
            break
        else:
            print("Invalid input. Please enter 0 or 1.")
    return option


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    FLAGS = parser.parse_args()
    return FLAGS


if __name__ == "__main__":
    FLAGS = parse_args()

    input_path = FLAGS.input_path

    df = pd.read_csv(input_path, index_col=0)
    # df["Negative"] = df["Negative"].astype(int)

    for idx, row in df.iterrows():
        # if idx < 200:
        #     continue
        if str(row["Negative"]) == "nan":
            cprint(f"Line: {idx + 1}", "red")
            cprint(f"Title: {row['Title']}", "green")
            cprint(f"Text: {row['Text']}", "green")

            while True:
                negative = input(
                    "Enter the value for sentiment field: \n  0: Non-negative\n  1: Negative\n  2: Invalid\nYour choice: "
                )

                # Validate the input
                if negative in ["0", "1", "2"]:
                    break
                else:
                    print("Invalid input. Please enter 0 or 1")

            df.loc[idx, "Negative"] = int(negative)
            df.to_csv(input_path)
        else:
            continue
        if continue_label() == 0:
            break
