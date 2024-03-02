import os
from datetime import date, datetime
from github import Auth, Github
from dotenv import load_dotenv

load_dotenv()

OBS_START_DATE = datetime.combine(date(2022, 1, 1), datetime.min.time())
OBS_END_DATE = datetime.combine(date(2023, 12, 31), datetime.max.time())

ORG_LIST_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/org_list.csv"
SELECT_REPOS_FILE = "/Users/kunalmundada/Documents/code/ECS_260/project/db/selected_repos.parquet"
DEVELOPERS_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/developers.csv"
DEVELOPER_ACTIVITY_DIR = "/Users/kunalmundada/Documents/code/ECS_260/project/db/devs"
ORG_COMMITS_DIR = "/Users/kunalmundada/Documents/code/ECS_260/project/db/orgs"

LOGS_PTH = "/Users/kunalmundada/Documents/code/ECS_260/project/logs"
REPO_CLONE_DIR = "/Users/kunalmundada/Documents/code/ECS_260/project/repo_holder"

GITHUB_OBJ = Github(auth=Auth.Token(os.getenv("GITHUB_PAT"))) # type: ignore