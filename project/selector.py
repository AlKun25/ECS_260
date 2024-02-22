import os
from github import Auth, Github, Repository, Organization
import pandas as pd
from tqdm import tqdm
from datetime import date, datetime
from icecream import ic
from dotenv import load_dotenv
import warnings

from utils import add_to_csv
from constants import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

# Load list of all organizations
orgs = pd.read_csv(ORG_LIST_CSV)


def selector(repo: Repository.Repository) -> bool | list:
    """
    Only consider projects with release
    At least 100 stars
    Repos created for at least 1 years
    Active: most recent commits within last 3 months
    """
    repo_name = repo.name
    repo_url = repo.url
    print(repo_name)
    last_observed_date = date(2024, 2, 1)
    # TODO : number of stars is greater than 100
    n_stars = ic(repo.stargazers_count)
    if n_stars > 100:
        # TODO: it has been released before OBS_START_DATE
        releases = repo.get_releases().reversed
        count = 0
        first_release_date = None
        is_released = None
        for release in releases:
            if count > 0:
                break
            first_release_date = release.created_at.date()
            count += 1
        if first_release_date != None:
            if (OBS_START_DATE.date() - first_release_date).days > 0:
                is_released = True
            else:
                is_released = False
        else:
            is_released = False

        if is_released:
            is_active_lately = True if repo.get_commits(since=datetime(2023,11,1)).totalCount > 0 else False
            # TODO : last commit within 3 months (90 days)
            if ic(is_active_lately):
                created_on = repo.created_at.date()
                # TODO : created for more than 1 year(365 days)
                # ? : SHOULD THIS BE date for first release?
                if ic(abs((last_observed_date - created_on).days)) >= 365:
                    n_contributors = ic(repo.get_contributors().totalCount)
                    print("Repo satisfies all critieria")
                    return (
                        repo_name,
                        org_name,
                        n_stars,
                        n_contributors,
                        is_released,
                        created_on,
                        is_active_lately,
                        repo_url,
                    )
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# Loop through each organization
for idx, link in enumerate(orgs["link"][1:2]):
    org = g.get_organization(link.split(sep="/")[-1])
    print(f"{idx}. {orgs['name'][idx]} organization loaded")

    # TODO: Get all repos of the organization
    repos = org.get_repos()
    org_name = org.name
    print(org_name)
    ic(repos.totalCount)

    # TODO: Find all the repos above 100 stars
    popularRepos = []
    for repo in tqdm(repos, total=repos.totalCount):
        result = selector(repo)
        if result != False:
            popularRepos.append(list(result))
    if len(popularRepos) > 0:
        df = pd.DataFrame(
            popularRepos,
            columns=[
                "repo",
                "org",
                "stars",
                "contributors",
                "released",
                "created_at",
                "updated_recently",
                "url",
            ],
        )
        ic(add_to_csv(df=df, csv_pth=SELECT_REPOS_CSV))
