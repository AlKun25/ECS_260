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
    filename=f"{LOGS_PTH}/{__file__.split(sep='/')[-1]}_{datetime.now()}.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# GitHub object
g = GITHUB_OBJ

def get_repo_org_commit(url):
    if (url):
        commit_repo_org_part = url.split(sep="repos/")[-1] 
        # print(commit_repo_org_part)
        org_repo_commit_list = commit_repo_org_part.split(sep="/")
        org = org_repo_commit_list[0]
        repo = org_repo_commit_list[1]
        commit = org_repo_commit_list[-1]
        # print(org, repo, commit)
        return org, repo, commit
    else:
        return None, None, None

def get_username(url):
    username = url.split(sep="users/")[-1]
    return username

def developer_history(name: str, email: str, ref_org_repo: str, obs_start: datetime, obs_end: datetime):
    # print(name, obs_start, obs_end, ref_org_repo, emails)
    email_commits = []
    shared = False
    # Find commits made by that email, before Jan 1 2024
    outside_repo_commits = 0
    within_org_commits = 0
    obs_end = obs_end + relativedelta(days=1)
    commits = g.search_commits(query=f'author-email:{email} committer-date:<{obs_end.strftime("%Y-%m-%d")}', sort='committer-date', order='desc')
    print(commits.totalCount)
    if commits.totalCount>0:
        for commit in commits:
            # print(commit.author.html_url)
            # user_name = get_username(commit.author) # to avoid individuals repo commits
            # ic(commit.author)
            # ic(commit.author.url)
            if commit.author is not None:
                user_name = get_username(commit.author.url)
            else:
                return "Non-existent users"
            commit_org, commit_repo, commit_etag = get_repo_org_commit(url=commit.commit.url)
            if(commit.commit.committer.date.date() < obs_start.date()):# terminate when outside OBS period
                break
            else:
                if(commit_org != user_name):
                    commit_date = commit.commit.committer.date
                    email_commits.append([name, user_name, commit_repo, commit_org, commit_date.day, commit_date.month, commit_date.year, email, commit_etag])
                    
                    if(f"{commit_org}/{commit_repo}" != ref_org_repo): # ! : to check for shared developer
                        shared = True
                        outside_repo_commits += 1
                        if(commit_org == ref_org_repo.split(sep="/")[0]):
                            within_org_commits += 1
    return outside_repo_commits

# TODO: List of all selected repos
repos = pd.read_parquet(SELECT_REPOS_CSV, engine="fastparquet")
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
            path_to_repo=repo_pth, since=start_date, to=finish_date, num_workers=4
        )
        code_complexity = []
        commit_size = []
        shared = 0
        contributor_to_email = dict()
        contributor_to_commits = dict()
        loa = []  # lines of anything
        modified_files = []
        count = 0
        commits_by_shared = 0
        shared_dev = []
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
        # print(contributor_to_commits)
        for name in contributor_to_email.keys():
            for email in list(contributor_to_email[name]):
                outside_commits = developer_history(name=name, email=email, ref_org_repo=f"{org_name}/{repo_name}", obs_start=start_date, obs_end=finish_date)
                if (outside_commits != "Non-existent users" and outside_commits>0):
                    shared += 1
                    commits_by_shared += contributor_to_commits.get(name, 1)
                    shared_dev.append(name)
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
                len(contributor_to_commits),
                count,
                contributor_to_commits,
                shared, 
                commits_by_shared, 
                shared_dev
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
                '',
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
                'contributors_to_commits',
                "n_shared", 
                "commits_by_shared",
                "shared_dev"
            ],
        )
        logging.warning("Month added to commit activity CSV.")
        add_to_file(df=month_df, file_pth=COMMIT_ACTIVITY_CSV)

        # Update start date and convert to datetime
        start_date = datetime.combine(finish_date, datetime.min.time())

    # logging.warning(f"Contributor count: {len(overall_repo_contributors)}")
    logging.warning(f"Actve months: {active_months}")
    delete_repo(repo_directory=repo_pth)

