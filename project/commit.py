import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
import numpy as np
import pandas as pd
from pydriller import Repository
from github import Auth, Github
from icecream import ic
from dotenv import load_dotenv
import warnings

from utils import *
from constants import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# Configure logging
logging.basicConfig(
    filename=f"{LOGS_PTH}/shared_developer_{datetime.now()}.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

# TODO: List of all selected repos
repos = pd.read_csv(SELECT_REPOS_CSV)

for repo in repos['url']:
    org_name, repo_name = (repo.split(sep="repos/")[-1]).split(sep='/')
    repo_url = f"https://github.com/{org_name}/{repo_name}.git"
    repo_pth = f"{REPO_CLONE_DIR}/{repo_name}"
    git_clone_repo(repo_url=repo_url, target_directory=repo_pth)
    start_date = OBS_START_DATE
    overall_repo_contributors = set()
    active_months = 0
    logging.warning(f"PROJECT: {repo_name}")
    for month in tqdm(range(24)):
        finish_date = (start_date + relativedelta(months=1)).date()
        start_date = start_date.date()
        if((start_date - OBS_END_DATE.date()).days >= 0):
            break
        logging.warning(f"Observing month:  {(start_date.year, start_date.month)}")
        start_date = datetime.combine(start_date, datetime.min.time())
        finish_date = datetime.combine(finish_date, datetime.min.time())
        load_repo = Repository(
            path_to_repo=repo_pth, since=start_date, to=finish_date, num_workers=4
        )
        code_complexity = []
        commit_size = []
        monthly_contributors = []
        loc = []
        modified_files = []
        count = 0
        for commit in tqdm(load_repo.traverse_commits()):
            code_complexity.append(commit.dmm_unit_complexity)
            commit_size.append(commit.dmm_unit_size)
            monthly_contributors.append(commit.author.name)
            modified_files.append(len(commit.modified_files))
            loc.append(commit.lines)
            count += 1
        # TODO : loop through PRs and issues.
        start_date = datetime.combine(finish_date, datetime.min.time())
        print("Total commits: ", count)
        logging.warning(f"Total commits in this month: {count}")
        if count > 0:
            active_months += 1
        overall_repo_contributors = overall_repo_contributors.union(set(monthly_contributors))
    logging.warning(f"Contributor count: {len(overall_repo_contributors)}")
    logging.warning(f"Actve months: {active_months}")
    delete_repo(repo_directory=repo_pth)