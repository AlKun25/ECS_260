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

# Configure logging
logging.basicConfig(
    filename=f"{LOGS_PTH}/{__file__.split(sep='/')[-1]}_{datetime.now()}.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)


def get_contributor_id(fullname: str, emails: set):
    related_users = g.search_users(query=f"fullname:{fullname}")
    for user in related_users:
        if(user.email in emails):
            return user.id

# Defining constants for this repo
org_name = "eclipse"
repo_name = "che"
repo_url = f"https://github.com/{org_name}/{repo_name}.git"
repo_pth = "/Users/kunalmundada/Documents/code/ECS_260/project/repo_holder/che"
start_date = OBS_START_DATE

# overall_repo_contributors = set()
contributor_to_email = dict()
# Looping through months
for month in tqdm(range(24)):
    finish_date = (start_date + relativedelta(months=1)).date()
    start_date = start_date.date()
    if (start_date - OBS_END_DATE.date()).days >= 0:
        break
    logging.warning(f"Observing month:  {(start_date.year, start_date.month)}")
    
    # Convert date to datetime
    start_date = datetime.combine(start_date, datetime.min.time())
    finish_date = datetime.combine(finish_date, datetime.min.time())
    
    # Load the Repo class of pydriller for commit traversal
    repo = Repository(
        path_to_repo=repo_pth, since=start_date, to=finish_date, num_workers=4
    )
    monthly_contributors = set()
    
    for commit in tqdm(repo.traverse_commits()):
        author_name = commit.author.name
        monthly_contributors.add(author_name)
        
        # Mapping name to multiple emails
        if contributor_to_email.get(author_name) != None:
            contributor_to_email[author_name].add(commit.author.email)
        else:
            contributor_to_email[author_name] = {commit.author.email}
    logging.warning(monthly_contributors)
    
    # Update start date and convert to datetime
    start_date = datetime.combine(finish_date, datetime.min.time())
logging.warning(contributor_to_email)

print("Searching related commits ...")
# Looping through all emails
for email in contributor_to_email.values():
    # Find commits made by that email, before Jan 1 2024
    commits = g.search_commits(query=f'author-email:{email} committer-date:<2024-01-01', sort='committer-date', order='desc')
    count = 0
    for commit in commits:
        user_name = commit.author.url.split(sep="/")[-1] # to avoid individuals repo commits
        commit_org_name = (commit.commit.html_url).split(sep="/commit")[0].split(sep="github.com/")[-1]
        # if(commit.commit.committer.date.date() < OBS_START_DATE.date()): # terminate when outside OBS period
        #     break
        # else:
        # To print commit made for organizations
        if(commit_org_name != user_name):
            print(commit_org_name)
            print(commit.commit.committer.date)
            print(commit.commit.author.name)


# contributor_to_id = dict()
# logging.warning(overall_repo_contributors)
# for user in contributor_to_email.keys():
#     contributor_to_id[user] = get_contributor_id(fullname=user, emails=contributor_to_email[user])

# logging.warning(contributor_to_id)



# # g.get_repo("eclipse/che").get_contributors()

# user = g.get_user_by_id(53429438)
# repos = user.get_repos(sort="pushed", direction="desc")
# events = user.get_public_events()
# for repo in repos:
#     print(repo.)


# for event in events.reversed:
    # if event.type == "PushEvent":
        # print(event.id)
        # print(event.repo.name)
        # print(event.org)
        # print(event.payload)
        # print(event.public)
        # print(event.created_at)
        # print(event.etag)


# results = g.search_users(query="fullname:balaji makam")

# for result in results:
#     print(result.name)
#     print(result.email)


# TODO : search_users -> get result's email and look for match -> save match's ID in dict -> always check dict first before doing a search for user
