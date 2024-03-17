import pandas as pd
import glob

file_pattern = 'output/_rq1/minor/*.csv'
csv_files = glob.glob(file_pattern)

dfs = []
for file in csv_files:
    print(file)
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=False)

combined_df.to_csv('output/release_minor_rq1_data.csv', index=False)