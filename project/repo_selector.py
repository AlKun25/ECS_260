import os
from github import Auth, Github, Repository, Organization
import pandas as pd
from tqdm import tqdm
from datetime import date, datetime
from icecream import ic
from dotenv import load_dotenv
import warnings

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

# Load list of all organizations
orgs = pd.read_csv("./project/org_list.csv")


# print(orgs['link'][:])
def add_to_csv(df: pd.DataFrame):
    if os.path.isfile("./project/db/selected_repos.csv"):
        df.to_csv("./project/db/selected_repos.csv", mode="a", header=False)
    else:
        df.to_csv("./project/db/selected_repos.csv")


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
        # TODO: it has been released
        releases = repo.get_releases()
        n_releases = releases.totalCount
        is_released = ic(True if n_releases > 0 else False)

        if is_released:
            last_repo_update = repo.updated_at.date()
            # TODO : last commit within 3 months (90 days)
            if ic(abs((last_observed_date - last_repo_update).days)) <= 90:
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
                        last_repo_update,
                        repo_url
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
    for repo in tqdm(repos):
        result = selector(repo)
        if result != False:
            popularRepos.append(list(result))
    if len(popularRepos) > 0:
        df = pd.DataFrame(popularRepos,
            columns=["repo", "org", "stars", "contributors", "released", "created_at", "updated_at", "url"],
        )
        ic(add_to_csv(df=df))