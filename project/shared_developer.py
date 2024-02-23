import os
import sys
from github import Auth, Github
from pydriller import Repository
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import date, datetime
from icecream import ic
import logging
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
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)


def idx_for_email(email: str, dev_list: list):
    if len(dev_list) > 0:
        df = pd.DataFrame(
            dev_list,
            columns=[
                "name",
                "email",
                "commit_activity",
                "shared",
                "created_at",
            ],
        )
        if email in df["email"].values:
            # print("OOOOOOOOOO")
            result = df["email"].values.tolist().index(email)
            return result
        else:
            # print("Why tho")
            return None
    else:
        # print("Please no")
        return None


# TODO: List of all selected repos
repos = pd.read_csv(SELECT_REPOS_CSV)

for repo in repos['url']:
    org_name, repo_name = (repo.split(sep="repos/")[-1]).split(sep='/')
    repo_url = f"https://github.com/{org_name}/{repo_name}.git"
    repo_pth = f"{REPO_CLONE_DIR}/{repo_name}"
    git_clone_repo(repo_url=repo_url, target_directory=repo_pth)
    specific_repo = Repository(
        path_to_repo=repo_pth, since_as_filter=OBS_START_DATE, to=OBS_END_DATE
    )
    print("----------------")
    developers = []
    for commit in specific_repo.traverse_commits():
        # logging.info(commit.hash, commit.author.name, commit.author.email)
        # print(commit.hash, commit.author.name, commit.author.email)
        idx = idx_for_email(email=commit.author.email, dev_list=developers)
        if idx != None:
            # print("Checking for email...")
            developers[idx][2].add(
                (
                    org_name+"/"+repo_name,
                    (commit.committer_date.date().year, commit.committer_date.date().month),
                )
            )
        elif check_in_csv(
            item=commit.author.email,
            col_name="email",
            csv_pth=DEVELOPERS_CSV,
        ):
            print("Found in CSV")
        #     df = pd.read_csv("./projects/db/developers.csv")
        #     csv_index = df["email"].values.tolist().index(commit.author.email)
        #     df["commit_activity"][csv_index].add(
        #         (
        #             repo_name,
        #             (commit.committer_date.date().year, commit.committer_date.date().month),
        #         )
        #     )
        #     df.to_csv('./project/db/developers.csv')
        else:
            # ? : Maybe define commit_months as set of tuples of two values. Values : repo_name, commit_month
            developers.append(
                [
                    commit.author.name,
                    commit.author.email,
                    {
                        (
                            org_name+"/"+repo_name,
                            (
                                commit.committer_date.date().year,
                                commit.committer_date.date().month,
                            ),
                        )
                    },
                    False,
                    None,
                ]
            )
    if len(developers) > 0:
        df = pd.DataFrame(
            developers,
            columns=["name", "email", "commit_activity", "shared", "created_at"],
        )
        add_to_csv(df=df, csv_pth=DEVELOPERS_CSV)
    delete_repo(repo_directory=repo_pth)