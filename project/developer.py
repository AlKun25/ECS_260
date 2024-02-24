import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
import numpy as np
import pandas as pd
from pydriller import Repository
from github import Auth, Github, NamedUser, GitCommit
from icecream import ic
from dotenv import load_dotenv
import warnings

from constants import *
from utils import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

def get_repo_org_commit(url):
    if (url):
        commit_repo_org_part = url.split(sep="repos/")[-1] 
        print(commit_repo_org_part)
        org_repo_commit_list = commit_repo_org_part.split(sep="/")
        org = org_repo_commit_list[0]
        repo = org_repo_commit_list[1]
        commit = org_repo_commit_list[-1]
        print(org, repo, commit)
        return org, repo, commit
    else:
        return None, None, None

def get_username(url):
    if (url):
        username = url.split(sep="users/")[-1]
        return username
    else:
        return None

def developer_history(name: str, emails: list, ref_org_repo: str, obs_start: datetime, obs_end: datetime):
    print(name, obs_start, obs_end, ref_org_repo, emails)
    email_commits = []
    shared = False
    for email in emails:
        # Find commits made by that email, before Jan 1 2024
        outside_repo_commits = 0
        obs_end = obs_end + relativedelta(days=1)
        commits = g.search_commits(query=f'author-email:{email} committer-date:<{obs_end.strftime("%Y-%m-%d")}', sort='committer-date', order='desc', page=100)
        if commits.totalCount>0:
            for commit in commits:
                if(commit.author.url):
                    print("Author doesn't exist")
                    break
                # print(commit.author.html_url)
                user_name = get_username(commit.author.url) # to avoid individuals repo commits
                print(user_name)
                commit_org, commit_repo, commit_etag = get_repo_org_commit(url=commit.commit.url)
                if(commit.commit.committer.date.date() < obs_start.date()): # terminate when outside OBS period
                    break
                else:
                # To print commit made for organizations
                    if(commit_org != user_name):
                        if(f"{commit_org}/{commit_repo}" != ref_org_repo): # ! : to check for shared developer
                            shared = True
                            outside_repo_commits += 1
                        commit_date = commit.commit.committer.date
                        email_commits.append([name, user_name, commit_repo, commit_org, commit_date.day, commit_date.month, commit_date.year, email, commit_etag])

    print(email_commits)
    commits_df = pd.DataFrame(commits, columns=["name", "username", "repo", "org", "day", "month", "year", "email", "etag"])
    add_to_csv(df=commits_df, csv_pth=DEVELOPER_ACTIVITY_CSV)
    print(shared, outside_repo_commits)