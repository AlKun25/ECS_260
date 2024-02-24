import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
import numpy as np
import pandas as pd
from pydriller import Repository
from github import Auth, Github, NamedUser
from icecream import ic
from dotenv import load_dotenv
import warnings

from constants import *
from utils import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

def developer_history(name: str, emails: str, ref_org: str, obs_start: datetime, obs_end: datetime):
    commits = []
    for email in emails.values():
        # Find commits made by that email, before Jan 1 2024
        obs_end.time = datetime.min.time()
        obs_end = obs_end + relativedelta(days=1)
        email = list(email)[0]
        commits = g.search_commits(query=f'author-email:{email} committer-date:<{obs_end.strftime("%Y-%m-%d")}', sort='committer-date', order='desc')
        for commit in commits:
            user_name = commit.author.url.split(sep="/")[-1] # to avoid individuals repo commits
            commit_org, commit_repo = (commit.commit.html_url).split(sep="/commit")[0].split(sep="github.com/")[-1]
            if(commit.commit.committer.date.date() < obs_start.date()): # terminate when outside OBS period
                break
            else:
            # To print commit made for organizations
                if(commit_org != user_name):
                    if(commit_org != ref_org and not shared): # ! : to check for shared developer
                        shared = True
                    commit_date = commit.commit.committer.date
                    commits.append([name, user_name, commit_repo, commit_org, commit_date.day, commit_date.month, commit_date.year, email, commit.commit.etag])
    commits_df = pd.DataFrame(commits, columns=["name", "user_name", "repo", "org", "day", "month", "year", "email", "etag"])
    add_to_csv(df=commits_df, csv_pth=DEVELOPER_ACTIVITY_CSV)
    return shared