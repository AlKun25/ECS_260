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
    stats = {"avg": None, "max": None, "Q1": None, "Q3": None}
    stats["max"] = metric.max().tolist()
    stats["Q1"], stats["avg"], stats["Q3"] = list(metric.quantile([0.25,0.5,0.75]).values)
    stats["Q1"], stats["avg"], stats["Q3"] = float(stats["Q1"]), float(stats["avg"]), float(stats["Q3"])
    return stats