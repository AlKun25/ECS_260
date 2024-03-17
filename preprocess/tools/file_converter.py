import os
import sys
import pyarrow.parquet as pq
import pandas as pd

# from constants import PATH

"""
Usage example: 
create a folder called csv/ in db/
python3 file_converter.py './db/selected_repos.parquet' 'selected_repos.csv'
selected_repos.csv is stored in ./db/csv/selected_repos.csv
"""

def convert_parquet_to_csv(parquet_file_path, csv_file_path):
    """
    Convert a Parquet file to a CSV file.
    
    Parameters:
    - parquet_file_path (str): Path to the input Parquet file.
    - csv_file_path (str): Path to the output CSV file.
    """
    parquet_file = pq.ParquetFile(parquet_file_path)
    table = parquet_file.read()
    df = table.to_pandas()
    if os.path.isfile(csv_file_path):
        df.to_csv(csv_file_path, mode="a", header=False)
    else:
        df.to_csv(csv_file_path)
    print(f"Conversion successful. CSV file saved at {csv_file_path}")

if __name__ == "__main__":
    # Check if two file paths are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py input.parquet output.csv")
        sys.exit(1)

    input_parquet_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    convert_parquet_to_csv(input_parquet_path, output_csv_path)
