from datetime import date, datetime

OBS_START_DATE = datetime.combine(date(2022, 1, 1), datetime.min.time())
OBS_END_DATE = datetime.combine(date(2023, 12, 31), datetime.max.time())

ORG_LIST_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/org_list.csv"
SELECT_REPOS_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/selected_repos.csv"
DEVELOPER_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/developers.csv"
DEVELOPER_ACTIVITY_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/developer_activity.csv"
COMMIT_ACTIVITY_CSV = "/Users/kunalmundada/Documents/code/ECS_260/project/db/commit_activity.csv"

LOGS_PTH = "/Users/kunalmundada/Documents/code/ECS_260/project/logs"
REPO_CLONE_DIR = "/Users/kunalmundada/Documents/code/ECS_260/project/repo_holder"