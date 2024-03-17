import csv
import os
import pandas as pd

# def filter_csv(df: pd.DataFrame, file_pth: str, substring: str):
#     # Filter rows containing the specified substring
#     filtered_df = df[~df['name'].str.contains(substring)]  
#     if os.path.isfile(file_pth):
#         filtered_df.to_csv(file_pth, mode='a', index=False, header=False)
#     else:
#         filtered_df.to_csv(file_pth, mode='w', index=False)
        
def filter_csv(input_file, output_file, substrings):
    df = pd.read_csv(input_file)
    # filtered_df = df[df['email'].apply(lambda row: (any((substring in str(cell)) for substring in substrings) for cell in row))]
    filtered_df = df[~df['email'].str.contains('|'.join(substrings), case=False)]
    # filtered_df.to_csv(output_file, index=False)
    filtered_df.to_csv(output_file, mode='w', index=False)

if __name__ == "__main__":
    input_file = input("Org name: ")
    # output_file = input("Path to output csv from db/org/: ")
    
    substring_list = ["bot", "team"]
    
    index = input_file.find(".csv")
    path = "orgs/"
    input_csv = os.path.join(path, input_file, f"{input_file}_commits_0.csv")
    output_csv = os.path.join(path, input_file, f"{input_file}_commits_0_bots_removed.csv")

    filter_csv(input_csv, output_csv, substring_list)
    print("Bots removed in", output_csv)