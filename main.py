import pandas as pd 
from project.constants import *
from project.selector import RepositorySelector
from project.repo import RepoAnalyzer

select_orgs = pd.read_csv(ORG_LIST_CSV, engine="pyarrow")
repo_selector = RepositorySelector(orgs=select_orgs, file_pth=SELECT_REPOS_FILE)
repo_selector.process_orgs()

repo_analysis = RepoAnalyzer()
repo_analysis.get_all_commits()

for org_url in select_orgs["link"]:
    org_name = org_url.split(sep="/")[-1]
    repo_analysis.analyze_repos(org_name)
