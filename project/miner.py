import os
from github import Auth, Github, Repository, Organization
import pandas as pd
from tqdm import tqdm
from icecream import ic
from dotenv import load_dotenv
import warnings

# System setup
warnings.filterwarnings('ignore')
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

# Load list of all organizations
orgs = pd.read_csv("./project/org_list.csv")

# print(orgs['link'][:])

# Loop through each organization
for idx, link in enumerate(orgs['link'][:]):
    ic(idx, link)
    org = g.get_organization(link.split(sep='/')[-1])
    print(f"{idx}. {orgs['name'][idx]} organization loaded")
    
    # TODO: Get all repos of the organization
    repos = org.get_repos()
    ic(repos.totalCount)
    
    # TODO: Find all the repos above 100 stars
    popularRepos = []
    for repo in tqdm(repos):
        if repo.stargazers_count > 100:
            popularRepos.append(repo.name)
    ic(len(popularRepos))
