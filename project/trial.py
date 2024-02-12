import os
from github import Github, Repository
from dotenv import load_dotenv

load_dotenv()

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# First create a Github instance:

def get_commit_count(repo: Repository.Repository):
    return repo.get_commits().totalCount

def get_commit_count(repo: Repository.Repository, file_path: str):
    return repo.get_commits(path=file_path).totalCount

def get_contributors(repo: Repository.Repository):
    return repo.get_contributors()

def get_all_files(repo: Repository.Repository):
    return repo.get_dir_contents("./")

def get_events_repo(repo: Repository.Repository):
    return repo.get_events()

def commit_time_diff(commit1, commit2):
    pass

# Public Web Github
g = Github(auth=auth)

repos = ["pytorch/pytorch"]
# Then play with your Github objects:
for repo in repos:
    open_issues = g.repo.get_issues(state='open')
    print(open_issues.totalCount)

# To close connections after use
g.close()
