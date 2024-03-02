import os
import shutil
import subprocess
import logging
from datetime import datetime
from numpy import append
import pandas as pd
from project.constants import LOGS_PTH

def add_to_parquet(df: pd.DataFrame, file_pth: str):
    if os.path.isfile(file_pth):
        df.to_parquet(file_pth, engine="fastparquet", append=True)
    else:
        df.to_parquet(file_pth, engine="fastparquet")

def check_in_csv(item: any, csv_pth: str, col_name: str): # type: ignore
    if os.path.isfile(csv_pth):
        df = pd.read_csv(csv_pth, engine="pyarrow")
        if item in df[col_name]:
            return True
        else:
            return False
    else:
        return False

def check_in_parquet(item: any, paq_pth: str, col_name: str): # type: ignore
    if os.path.isfile(paq_pth):
        df = pd.read_parquet(paq_pth, engine="fastparquet")
        if item in df[col_name]:
            return True
        else:
            return False
    else:
        return False

def git_clone_repo(repo_url, target_directory):
    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, target_directory])

def delete_repo(repo_directory):
    # Change to the parent directory to delete the repository
    # os.chdir('..')
    print("Deleting the repo stored at ", repo_directory)
    # Delete the repository directory
    shutil.rmtree(repo_directory)

def get_metric_stats(metric: pd.DataFrame):
    stats = dict()
    stats["max"] = metric.max().tolist()
    stats["Q1"], stats["avg"], stats["Q3"] = list(metric.quantile([0.25,0.5,0.75]).values)
    stats["Q1"], stats["avg"], stats["Q3"] = float(stats["Q1"]), float(stats["avg"]), float(stats["Q3"])
    return stats

def get_logger(filename: str, log_level = logging.INFO):
    logger = logging.basicConfig(
        filename=f"{LOGS_PTH}/{filename.split(sep='/')[-1]}_{datetime.now()}.log",
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logger