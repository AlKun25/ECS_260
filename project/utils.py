import os
import shutil
import subprocess
import pandas as pd

def add_to_csv(df: pd.DataFrame, csv_pth: str):
    if os.path.isfile(csv_pth):
        df.to_csv(csv_pth, mode="a", header=False)
    else:
        df.to_csv(csv_pth)

def check_in_csv(item: any, csv_pth: str, col_name: str):
    if os.path.isfile(csv_pth):
        df = pd.read_csv(csv_pth)
        if df[col_name].isin(item):
            return True
        else:
            return False
    else:
        return False

def git_clone_repo(repo_url, target_directory):
    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, target_directory])
