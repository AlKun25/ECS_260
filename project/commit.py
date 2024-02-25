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
from developer import developer_history

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

# TODO: List of all selected repos
repos = pd.read_csv(SELECT_REPOS_CSV)
for repo in repos["url"]:
    org_name, repo_name = (repo.split(sep="repos/")[-1]).split(sep="/")
    repo_url = f"https://github.com/{org_name}/{repo_name}.git"
    repo_pth = f"{REPO_CLONE_DIR}/{repo_name}"
    git_clone_repo(repo_url=repo_url, target_directory=repo_pth)
    start_date = OBS_START_DATE
    # overall_repo_contributors = set()
    active_months = 0
    logging.warning(f"PROJECT: {repo_name}")

    for month in tqdm(range(24)):
        finish_date = (start_date + relativedelta(months=1)).date()
        start_date = start_date.date()
        if (start_date - OBS_END_DATE.date()).days >= 0:
            break
        logging.warning(f"Observing month:  {(start_date.year, start_date.month)}")
        start_date = datetime.combine(start_date, datetime.min.time())
        finish_date = datetime.combine(finish_date, datetime.min.time())
        load_repo = Repository(
            path_to_repo=repo_pth, since=start_date, to=finish_date, num_workers=8
        )
        code_complexity = []
        commit_size = []

        contributor_to_email = dict()
        contributor_to_commits = dict()
        loa = []  # lines of anything
        modified_files = []
        count = 0
        for commit in tqdm(load_repo.traverse_commits()):
            code_complexity.append(commit.dmm_unit_complexity)
            commit_size.append(commit.dmm_unit_size)
            # monthly_contributors.add(commit.author.name)
            author = commit.author
            # Mapping name to multiple emails
            if contributor_to_email.get(author.name) != None:
                contributor_to_email[author.name].add(author.email)
            else:
                contributor_to_email[author.name] = {author.email}

            if contributor_to_commits.get(author.name) != None:
                contributor_to_commits[author.name] += 1
            else:
                contributor_to_commits[author.name] = 1

            modified_files.append(len(commit.modified_files))
            loa.append(commit.lines)
            count += 1
        print(contributor_to_commits)
        # for name in contributor_to_email.keys():
            # developer_history(name=name, emails=list(contributor_to_email[name]), ref_org_repo=f"{org_name}/{repo_name}", obs_start=start_date, obs_end=finish_date)

        print("Total commits: ", count)
        logging.warning(f"Total commits in this month: {count}")
        monthly_row = []
        if count > 0:
            active_months += 1
            monthly_row = [
                repo_name,
                org_name,
                (start_date, finish_date),
                get_metric_stats(pd.DataFrame(code_complexity)),
                get_metric_stats(pd.DataFrame(commit_size)),
                get_metric_stats(pd.DataFrame(loa)),
                get_metric_stats(pd.DataFrame(modified_files)),
                len(contributor_to_email),
                count,
                contributor_to_commits
            ]
        else:
            monthly_row = [
                repo_name,
                org_name,
                (start_date, finish_date),
                0,
                0,
                0,
                0,
                0,
                0,
                ''
            ]
        month_df = pd.DataFrame(
            [monthly_row],
            columns=[
                "repo",
                "org",
                "obs_period",
                "unit_complexity",
                "unit_size",
                "lines",
                "n_modified_files",
                "n_contributors",
                "n_commits",
                "contributor_to_commits"
            ],
        )
        logging.warning("Month added to commit activity CSV.")
        add_to_csv(df=month_df, csv_pth=COMMIT_ACTIVITY_CSV)

        # Update start date and convert to datetime
        start_date = datetime.combine(finish_date, datetime.min.time())

    # logging.warning(f"Contributor count: {len(overall_repo_contributors)}")
    logging.warning(f"Actve months: {active_months}")
    delete_repo(repo_directory=repo_pth)
