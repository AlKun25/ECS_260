import os
from pydriller import Repository
import pandas as pd
from tqdm import tqdm
from icecream import ic
from dotenv import load_dotenv
import warnings

# System setup
warnings.filterwarnings('ignore')
load_dotenv()

REPO_URL = "https://github.com/sqlalchemy/sqlalchemy"
CLONE_FOLDER_NAME = REPO_URL.split(sep="/")[-1]

# # GitHub Auth
# auth = Auth.Token(os.getenv("GITHUB_PAT"))

# # GitHub object
# g = Github(auth=auth)

def mcc(start_time, end_time):
    """Calculate the McCabe's code complexity for the repository.

    Args:
        start_time (_type_): _description_
        end_time (_type_): _description_
    """    
    pass

def pac(start_time, end_time):
    """Calculate the PR Accpetance rate for the specific time window

    Args:
        start_time (_type_): _description_
        end_time (_type_): _description_
    """    
    pass

# * S_FOCUS
def sfocus(start_time, end_time):    
    pass



os.chdir('/Users/kunalmundada/Documents/code/ECS_260/project/db')

os.system("git clone "+REPO_URL)

count = 0
for commit in Repository("/Users/kunalmundada/Documents/code/ECS_260/project/db/sqlalchemy").traverse_commits():
    print(commit.hash, commit.msg)
    print("| {} | {} | {} | {} |".format(
                commit.msg,
                commit.dmm_unit_size,
                commit.dmm_unit_complexity,
                commit.dmm_unit_interfacing
                ))
    if count > 10:
        break
    count +=1