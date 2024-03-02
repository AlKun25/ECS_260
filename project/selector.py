import logging
from datetime import date, datetime
from tqdm import tqdm
import pandas as pd
from github import Repository
import warnings

from project.utils import add_to_parquet, get_logger
from project.constants import *

# System setup
warnings.filterwarnings("ignore")
logger = get_logger(filename=__file__)

class RepositorySelector:
    def __init__(self, orgs, file_pth):
        self.orgs = orgs
        self.g = GITHUB_OBJ
        self.file_pth = file_pth
        self.last_obs_date = date(2024, 2, 1)

    def select(self, repo: Repository.Repository, org: str):
        """
        Only consider projects with release
        At least 100 stars
        Repos created for at least 1 years
        Active: most recent commits within last 3 months
        """
        repo_name = repo.name
        repo_url = repo.url
        n_stars = repo.stargazers_count
        if n_stars > 100:
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

            if is_released and repo.get_commits(since=datetime(2023, 11, 1)).totalCount > 0:
                created_on = repo.created_at
                if abs((self.last_obs_date - created_on.date()).days) >= 365:
                    n_contributors = repo.get_contributors().totalCount
                    n_commits = repo.get_commits(since=OBS_START_DATE, until=OBS_END_DATE).totalCount
                    logging.info(f"Repo {repo_name} satisfies all criteria")
                    return (
                        repo_name,
                        org,
                        n_stars,
                        n_contributors,
                        n_commits,
                        is_released,
                        created_on.strftime("%d/%m/%Y"),
                        True,  # is_active_lately
                        repo_url,
                    )
            return False

    def process_orgs(self):
        for idx, link in enumerate(self.orgs["link"][6:7]):
            org = self.g.get_organization(link.split(sep="/")[-1])
            org_name = org.name or "NA"
            logging.info(f"{idx}. {org_name} organization loaded")
            repos = org.get_repos()
            popular_repos = []
            for repo in tqdm(repos, total=repos.totalCount):
                result = self.select(repo, org_name)
                if result:
                    popular_repos.append(list(result))
            if len(popular_repos) > 0:
                df = pd.DataFrame(
                    popular_repos,
                    columns=[
                        "repo",
                        "org",
                        "stars",
                        "contributors",
                        "commits",
                        "released",
                        "created_at",
                        "updated_recently",
                        "url",
                    ],
                )
                # df['created_at'] = df['created_at'].astype(datetime)
                add_to_parquet(df=df, file_pth=self.file_pth)

if __name__=="__main__":
    # Load list of all organizations
    select_orgs = pd.read_csv(ORG_LIST_CSV, engine="pyarrow")
    repo_selector = RepositorySelector(orgs=select_orgs, file_pth=SELECT_REPOS_FILE)
    repo_selector.process_orgs()