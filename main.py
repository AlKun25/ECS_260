import pandas as pd 
from project.constants import *
from project.selector import RepositorySelector
from project.repo import RepoAnalyzer
from project.utils import get_logger
import logging

logger = get_logger()

# select_orgs = pd.read_csv(ORG_LIST_CSV, engine="pyarrow")
# logging.info("Repo selection phase")
# repo_selector = RepositorySelector(orgs=select_orgs, file_pth=SELECT_REPOS_FILE)
# repo_selector.process_orgs()

repo_analysis = RepoAnalyzer()
logging.info("Commit download phase")
repo_analysis.get_all_commits()

logging.info("Metric retrieval phase")
# for org_url in select_orgs["link"]:
#     org_name = org_url.split(sep="/")[-1]
#     repo_analysis.analyze_repos(org_name)

repo_analysis.analyze_repos("RedHatOfficial")
