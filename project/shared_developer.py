import os
from github import Auth, Github
from pydriller import Repository
import pandas as pd
from tqdm import tqdm
from datetime import date, datetime
from icecream import ic
from dotenv import load_dotenv
import warnings

from utils import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

OBS_START_DATE = datetime.combine(date(2020, 1, 1), datetime.min.time())
OBS_END_DATE = datetime.combine(date(2023, 12, 31), datetime.max.time())



# TODO: List of all selected repos
repos = pd.read_csv("./project/db/selected_repos.csv")


for repo in repos['url']:
    org_name, repo_name = (repo.split(sep="repos/")[-1]).split(sep='/')
    repo_url = f"https://github.com/{org_name}/{repo_name}.git"
    repo_pth = f"./project/repo_holder/{repo_name}"
    git_clone_repo(repo_url=repo_url, target_directory=repo_pth)
    specific_repo = Repository(path_to_repo=repo_pth, since=OBS_START_DATE, to=OBS_END_DATE)
    developers = []
    for commit in specific_repo.traverse_commits():
        print("----------------")
        print(commit.hash)
        # print("Message: ", commit.msg)
        print("Author Name: ", commit.author.name)
        print("Author Mail: ", commit.author.email)
        print("Author Date?: ", commit.author_date)
        # print("Committer Name: ", commit.committer.name)
        # print("Committer Email: ", commit.committer.email)
        # print("Committer date: ", commit.committer_date)
        if check_in_csv(item=commit.author.email, col_name='email', csv_pth='./project/db/developers.csv'):
            # update the csv row with repos and commit dates
            pass
        else:
            developers.append[commit.author.name, commit.author.email, [repo_name, commit.author_date], 1, False]


# TODO: Loop through each repo
# for repo in repos['url']:
    # TODO : Find all the contributors and loop through them
    # repo_id = repo.split(sep="repos/")[-1]
    # contributors = g.get_repo(repo_id).get_contributors()
    # for contributor in contributors:
        # TODO : Update developer table with it
        # * : [name, email, [repo1, repo2, repo3 ...], created_at, ]
        # username = contributor.url.split(sep="/")[-1]
        
        # find if the contributor exists in the 'name' column
            # if it exists, just update the 
            # add the repo to the list in 'repos' column for that