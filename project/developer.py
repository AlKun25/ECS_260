from matplotlib.dates import WEEKLY
from pydriller import Repository
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from icecream import ic
from glob import glob
import warnings

from project.utils import *
from project.constants import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# Configure logging
logger = get_logger()

class DeveloperTracker:
    def __init__(
        self,
        contributors_email: list,
        obs_start: datetime,
        obs_end: datetime,
        org: str,
        repo: str,
    ) -> None:
        """This class helps us track the developer activity outside of the reference repository

        Args:
            contributors_email (list): passes a nested list of name, list[emails] and number of commits
            obs_start (datetime): start of the observation date & time. Start of the week
            obs_end (datetime): end of the observation date & time. End of the week
            org (str): name of the GitHub organization
            repo (str): name of the GitHub repository
        """
        self.g = check_rate_limit()        
        self.name_email_pairs = contributors_email
        self.obs_start = obs_start
        self.obs_end = obs_end
        self.week = obs_start.isocalendar()[0:2]
        self.ref_org_repo = f"{org}/{repo}"
        self.n_shared = 0 # * : used in repo.py for repo's weekly activity
        self.shared_dev_names = set()
        
        self.org_name = ic(org)
        self.repo_name = ic(repo)

        dev_files = glob(
            f"{DEVELOPER_ACTIVITY_DIR}/developer_activity_*.csv"
        )
        if(len(dev_files)>0):
            latest_file_name = dev_files[-1] 
            latest_file_num = int((latest_file_name.split(sep="_")[-1]).split(sep=".")[0])
            self.all_developer_commits = (
                latest_file_num * 10000 + pd.read_csv(latest_file_name, engine="pyarrow").shape[0]
            )
        else:
            self.all_developer_commits = 0

    def get_repo_org_commit(self, url: str):
        """Extract crucial commit information using URL

        Args:
            url (str): url of the commit

        Returns:
            str: If url exists, returns three strings for name of organization, repository and the commit's etag/hash. Else, it returns None
        """        
        if url:
            commit_repo_org_part = url.split(sep="repos/")[-1]
            org_repo_commit_list = commit_repo_org_part.split(sep="/")
            org = org_repo_commit_list[0]
            repo = org_repo_commit_list[1]
            commit = org_repo_commit_list[-1]
            return org, repo, commit
        else:
            return None, None, None

    def get_username(self, url: str):
        """Extracts the username of the developer

        Args:
            url (str): The author's url 

        Returns:
            str: It send back the username of the developer.
        """        
        username = url.split(sep="users/")[-1]
        return username

    def get_developer_activity(self, name: str, email: str) -> list:
        """This contains the developer's commit activity in the same week outside the repo.
        Conditions: we drop users that don't exist anymore. we don't consider activity in personal repos/forks.

        Args:
            name (str): Name of the developer
            email (str): Email of the developer

        Returns:
            list: it contains number of commits made outside the repo and whether developer is shared or not.
        """        
        email_commits = []
        if type(name) != str:
            name =str (name[0])
        if type(email) != str:
            email = str(email[0])
        # TODO : Save all commits to a single series of developers.csv
        shared = False
        outside_repo_commits = 0
        within_org_commits = 0
        self.obs_end = self.obs_end + relativedelta(days=1)
        # Find all the commits in the time frame
        logging.info(f"Looking for commits from {name} by email : {email}")
        self.g = check_rate_limit()
        commits = self.g.search_commits(
            query=f'author-email:{email} committer-date:>{self.obs_start.strftime("%Y-%m-%d")}'
        )
        if commits.totalCount > 0:
            self.g = check_rate_limit()
            logging.info("Looping through the commits")
            for commit in commits:
                self.g = check_rate_limit()
                if commit.author is None or not hasattr(commit.author, 'url') or not commit.author.url:
                    logging.critical("Author doesn't exist!Breaking the loop")
                    break
                user_name = self.get_username(commit.author.url)
                commit_org, commit_repo, commit_etag = self.get_repo_org_commit(
                    url=commit.commit.url
                )
                if (commit.commit.committer.date.date() < self.obs_end.date()):
                    logging.info(f"Checking for commit: {commit_etag}")
                    if (commit_org != user_name and not (commit_repo == self.repo_name and commit_org == self.org_name)): # ! : to check for shared developer
                        shared = True
                        outside_repo_commits += 1
                        if(commit_org == self.org_name):
                            within_org_commits += 1
                        commit_date = commit.commit.committer.date
                        email_commits.append(
                            [
                                name,  # name
                                user_name,
                                commit_repo,
                                commit_org,
                                commit_date,
                                commit_date.isocalendar()[1],
                                email,  # email
                                commit_etag,
                            ]
                        )
                        print("This commit is shared: ", commit_etag)
                        self.shared_dev_names.add(name)
                self.g = check_rate_limit()
        # loop through the weeks for that specific monthly only.
        # TODO : save all the commits in db/devs with S-focus in a separate organization file.
        # save all commits in a common file name.
        print(email_commits)
        commits_df = pd.DataFrame(
            email_commits,
            columns=[
                "name",
                "username",
                "repo",
                "org",
                "date",
                "week",
                "email",
                "etag",
            ],
        )
        self.all_developer_commits += commits_df.shape[0]
        file_num = self.all_developer_commits // 10000
        add_to_file(
            df=commits_df,
            file_pth=f"{DEVELOPER_ACTIVITY_DIR}/kunal_developer_activity_{file_num}.csv",
        )
        return [outside_repo_commits, within_org_commits, shared]

    def weekly_activity(self):
        """This saves weekly activity for each developer, for developers who made commits to the reference repo in same week.
        """        
        activity = []
        for name_email_pair in self.name_email_pairs:
            final_res = [0, 0, False]
            name = name_email_pair[0][0]
            if "[bot]" in name:
                continue
            for email in name_email_pair[1]:
                self.g = check_rate_limit()
                res = self.get_developer_activity(
                    name, email
                )
                final_res = [final_res[0] + res[0], final_res[1] + res[1],final_res[2] or res[2]]
            if final_res[1]:
                self.n_shared += 1
            s_focus = name_email_pair[2] / (name_email_pair[2] + final_res[0])
            repo = self.ref_org_repo.split(sep="/")[-1]
            activity.append(
                [
                    name,
                    str(name_email_pair[1]),
                    s_focus,
                    self.repo_name,
                    int(final_res[0]),
                    int(final_res[1]),
                    bool(final_res[2]),
                    str(self.week),
                ]
            )
        # save the specific repo-related developers in a common
        # name, username, emails(list/set), s-focus, repo, outside_repo_commits, shared, week
        weekly_activity_df = pd.DataFrame(
            activity,
            columns=[
                "name",
                "emails",
                "s_focus",
                "repo",
                "outside_repo_commits",
                "within_org_commits",
                "shared",
                "week",
            ],
        )

        pth = f"{ORG_COMMITS_DIR}/{self.org_name}/weekly_dev_activity.csv"
        add_to_file(weekly_activity_df, pth)

if __name__ == "__main__":
    contributor_emails_pair = [[('Dan Clark',), ['danclark@redhat.com'], 1]]
    sow = datetime(2023, 11, 27, 0, 0)
    eow = datetime(2023, 12, 2, 0, 0)
    tracker = DeveloperTracker(contributors_email=contributor_emails_pair, obs_start=sow, obs_end=eow, org="RedHatOfficial", repo="ansible-role-rhel7-stig")
    tracker.weekly_activity()
    # tracker.get_developer_activity(name="Dan Clark", email="danclark@redhat.com")