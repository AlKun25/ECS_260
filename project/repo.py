import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
from tqdm import tqdm
import pandas as pd
from glob import glob
from pydriller import Repository
from dotenv import load_dotenv
from typing import Optional
import warnings
from project.developer import DeveloperTracker

from project.utils import *
from project.constants import *

# System setup
load_dotenv()
warnings.filterwarnings("ignore")
logger = get_logger()


class RepoAnalyzer:
    def __init__(self):
        """This is the main class that handles both the commit downloads for selected repos as well as metric retrieval
        """        
        # GitHub object
        self.g = check_rate_limit()

    def get_all_releases(self, org_repo: str):
        """Extract all the release for a specific repo in our predefined time period

        Args:
            org_repo (str): compunded string of structure 'org/repo'
        """        
        releases = self.g.get_repo(org_repo).get_releases()
        self.g = check_rate_limit()
        relevant_releases = []
        org_name, repo_name = org_repo.split(sep="/")
        for release in releases:
            if release.published_at.date()>=OBS_START_DATE.date() and release.published_at.date()<=OBS_END_DATE.date():
                relevant_releases.append([release.id, release.published_at.strftime("%d/%m/%Y"), release.tag_name, repo_name])
        releases_df = pd.DataFrame(relevant_releases, columns=[
            "id",
            "date",
            "version",
            "repo_name"
        ])
        add_to_file(releases_df, ORG_COMMITS_DIR+f"/{org_name}/releases.csv")
        self.g = check_rate_limit()
        logging.info(f"Saved all releases for {org_repo}")
    
    def get_all_commits(self, ref_org: Optional[str]):
        """It downloads all the commits for all the repos.
        Scheduling: Orgs and repos with lower number of commits are priortized for processing
        """        
        repos = pd.read_parquet(SELECT_REPOS_FILE, engine="fastparquet")

        # Group the DataFrame by 'org' and sum the 'commits' for each organization
        org_commits_sum = repos.groupby("org")["commits"].sum().reset_index()

        # Sort the organizations by their sum of commits in descending order
        org_commits_sum_sorted = org_commits_sum.sort_values(
            by="commits", ascending=True
        )

        for org in org_commits_sum_sorted["org"]:
            if len(ref_org)>0: # type: ignore
                if org != ref_org:
                    continue
            org_repos = repos[repos["org"] == org]
            # Sort the filtered DataFrame by commits in ascending order
            org_repos_df_sorted = org_repos.sort_values(by="commits", ascending=True)

            org_commit_counter = 0
            # visited=False
            # ref_repo = "bosh-bootloader"
            for repo in org_repos_df_sorted["url"]:
                org_name, repo_name = (repo.split(sep="repos/")[-1]).split(sep="/")
                # if not visited and repo_name != ref_repo:
                #     continue
                # elif not visited and repo_name == ref_repo:
                #     visited=True
                org_dir_path = f"{ORG_COMMITS_DIR}/{org_name}"
                if not os.path.exists(org_dir_path):
                    # If the directory doesn't exist, create it
                    os.makedirs(org_dir_path)
                logging.info(f"Loaded {org_name}/{repo_name}")
                repo_url = f"https://github.com/{org_name}/{repo_name}.git"
                repo_pth = f"{REPO_CLONE_DIR}/{repo_name}"
                self.get_all_releases(f"{org_name}/{repo_name}")
                git_clone_repo(repo_url=repo_url, target_directory=repo_pth)
                

                load_repo = Repository(
                    path_to_repo=repo_pth,
                    since=OBS_START_DATE,
                    to=OBS_END_DATE,
                    num_workers=128,
                )

                for commit in tqdm(
                    load_repo.traverse_commits(),
                    total=int(org_repos[org_repos["url"] == repo]["commits"]),
                ):
                    commit_dt = commit.committer_date
                    commit_week = str(commit_dt.date().isocalendar()[:2])

                    commit_df = pd.DataFrame(
                        [
                            [
                                commit.hash,
                                repo_name,
                                org_name,
                                commit.author.name,
                                commit.author.email,
                                commit_dt.year,
                                commit_dt.month,
                                commit_dt.day,
                                commit_week,
                                commit.dmm_unit_complexity,
                                commit.dmm_unit_size,
                                commit.lines,
                                len(commit.modified_files),
                            ]
                        ],
                        columns=[
                            "id",
                            "repo",
                            "org",
                            "name",
                            "email",
                            "year",
                            "month",
                            "day",
                            "week",
                            "unit_complexity",
                            "unit_size",
                            "lines",
                            "n_modified_files",
                        ],
                    ).fillna(0.0)
                    file_num = org_commit_counter // 10000
                    add_to_file(
                        df=commit_df,
                        file_pth=f"{org_dir_path}/{org_name}_commits_{file_num}.csv",
                    )
                    org_commit_counter += 1
                delete_repo(repo_directory=repo_pth)
                print(f"Saved all commits from Repo: {org_name}/{repo_name}")
                logging.info(f"Saved all commits from Repo: {org_name}/{repo_name}")
            print(f"Saved all commits from Org: {org}")
            logging.info(f"Saved all commits from Org: {org}")

    def analyze_repos(self, org_name: str):
        """Loop through all commits from all selected repos within a specific org

        Args:
            org_name (str): Name of the organization, as in a URL
        """        
        for org_commit_csv in glob(
            f"{ORG_COMMITS_DIR}/{org_name}/{org_name}_commits*.csv"
        ):
            self.org = org_name # !:use this only in analysis part
            logging.info(f"Analyzing {org_name}")
            org_df = pd.read_csv(org_commit_csv, engine="pyarrow")
            repos = org_df["repo"].unique()
            for repo in repos:
                repo_df = org_df[org_df["repo"] == repo]
                self.repo = repo # !:use this only in analysis part
                logging.info(f"Analyzing {repo}")
                self.analyze_repo(repo_df=repo_df)

    def analyze_repo(self, repo_df: pd.DataFrame):
        """Loop through various weeks of commit history in a specific year for a repo

        Args:
            repo_df (pd.DataFrame): Contains all commits for a specific repo 
        """        
        for year in [2022, 2023]:
            logging.info(f"Analyzing for {year}")
            year_df = repo_df[repo_df["year"] == year]
            if year_df.shape[0] > 0:
                self.year = year # !:use this only in analysis part
                self.analyze_yearly(year_df)

    def analyze_yearly(self, year_df: pd.DataFrame):
        """Loop through various weeks of commit history in a specific year for a repo

        Args:
            year_df (pd.DataFrame): Contains yearly commits for a specific repo
        """        
        active_weeks = year_df["week"].unique()
        for week in active_weeks:
            logging.info(f"Analyzing for {week}")
            week_df = year_df[year_df["week"] == week]
            if week_df.shape[0] > 0:
                self.week = week # !:use this only in analysis part
                t_year, t_week = map(int, week.strip("()").split(","))
                week_start_dt = datetime.strptime(f"{t_year}-W{t_week}-1", "%Y-W%U-%w")
                week_end_dt = datetime.strptime(f"{t_year}-W{t_week}-6", "%Y-W%U-%w")
                self.analyze_weekly(week_df, week_start_dt, week_end_dt)

    def analyze_monthly(self, month: int, year: int):
        pass

    def analyze_weekly(self, week_df: pd.DataFrame, sow: datetime, eow: datetime):
        """Saves weekly summary overview of each repo in db/weekly_analysis.csv.

        Args:
            week_df (pd.DataFrame): Contains weekly commits for a specific repo
            sow (datetime): Start of the week
            eow (datetime): End of the week
        """        
        weekly_org_pth = f"{ORG_COMMITS_DIR}/{str(week_df['org'].unique()[0])}/{str(week_df['org'].unique()[0])}_weekly.csv"

        weekly_metrics = dict()
        weekly_metrics["unit_complexity"] = get_metric_stats(
            week_df["unit_complexity"].to_frame()
        )
        weekly_metrics["unit_size"] = get_metric_stats(week_df["unit_size"].to_frame())
        weekly_metrics["lines"] = get_metric_stats(week_df["lines"].to_frame())
        weekly_metrics["n_modified_files"] = get_metric_stats(
            week_df["n_modified_files"].to_frame()
        )
        
        grouped_df = week_df.groupby(['name'])
        
        contributor_emails_pair = []
        for name, group in grouped_df:
            print(f"Name: {name}")
            emails = list(set(group['email']))
            commit_count = group.shape[0]
            contributor_emails_pair.append([name, emails, commit_count])
        
        dev_activity_obj = DeveloperTracker(contributors_email=contributor_emails_pair, obs_start=sow, obs_end=eow, org=week_df["org"].unique()[0], repo=week_df["repo"].unique()[0])
        dev_activity_obj.weekly_activity()
        n_shared = dev_activity_obj.n_shared
        
        week_repo_df = pd.DataFrame(
            [
                [
                    self.repo,
                    self.org,
                    self.week,
                    str(weekly_metrics["unit_complexity"]),
                    str(weekly_metrics["unit_size"]),
                    str(weekly_metrics["lines"]),
                    str(weekly_metrics["n_modified_files"]),
                    len(week_df["name"].unique()),
                    n_shared,
                    week_df.shape[0],
                ]
            ],
            columns=[
                "repo",
                "org",
                "week",
                "unit_complexity",
                "unit_size",
                "lines",
                "n_modified_files",
                "total_contributors",
                "n_shared",
                "n_commits",
            ],
        )
        add_to_file(week_repo_df, weekly_org_pth)
        logging.info(f"Analysis for period {sow}-{eow} done.")


if __name__ == "__main__":
    # Usage
    analyzer = RepoAnalyzer()
    org_name = input("Which org to download? ")
    # analyzer.get_all_commits(ref_org=org_name)
    analyzer.analyze_repos(org_name="RedHatOfficial") # name of the folder in the orgs folder
