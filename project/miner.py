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
def add_to_csv(df: pd.DataFrame):
    if os.path.isfile('./project/db/popular_repos.csv'):
        df.to_csv('./project/db/popular_repos.csv', mode='a', header=False)
    else:
        df.to_csv('./project/db/popular_repos.csv')

# Loop through each organization
for idx, link in enumerate(orgs['link'][1:]):
    ic(idx, link)
    org = g.get_organization(link.split(sep='/')[-1])
    print(f"{idx}. {orgs['name'][idx]} organization loaded")

    # TODO: Get all repos of the organization
    repos = org.get_repos()
    org_name = org.name
    ic(repos.totalCount)

    # TODO: Find all the repos above 100 stars
    popularRepos = []
    for repo in tqdm(repos):
        n_stars = repo.stargazers_count
        if n_stars > 100:
            repo_name = ic(repo.name)
            ic(n_stars)
            n_contributors = ic(repo.get_contributors().totalCount)
            # n_downloads = ic(repo.get_downloads().totalCount)
            n_releases = ic(repo.get_releases().totalCount)
            is_released = ic(True if n_releases > 0 else False)
            popularRepos.append([repo_name, org_name, n_stars, n_contributors, is_released])
    df = pd.DataFrame(popularRepos, columns=['repo', 'org', 'stars', 'contributors', 'released'])
    add_to_csv(df=df)
# ic(len(popularRepos))

# df.to_csv("./project/db/popular_repos.csv")

