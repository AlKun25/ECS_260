from github import Auth, Github
from datetime import date, datetime
from dotenv import load_dotenv
import warnings

from constants import *
from utils import *

# System setup
warnings.filterwarnings("ignore")
load_dotenv()

# GitHub Auth
auth = Auth.Token(os.getenv("GITHUB_PAT"))

# GitHub object
g = Github(auth=auth)

# related_user = g.search_users(query="fullname:Sergey Skorik")

# for user in related_user:
#     print(user.name)
#     print(user.email)
#     print(user.company)
#     print(user.id)

'''
Sergey Skorik
sskoryk@redhat.com
Red Hat
7760565
'''

commits = g.search_commits(query=f"author-email:sskoryk@redhat.com committer-date:<2022-02-01", sort="committer-date", order="desc")


# URL = https://github.com/eclipse/che/commit/e76edad6aa73ae0737c8dba170fc63c724ec8f4a
for commit in commits:
    # print(commit.raw_headers)
    # user_url = commit.author.url.split(sep="/")[-1]
    # org_name = (commit.commit.html_url).split(sep="/commit")[0].split(sep="github.com/")[-1].split(sep="/")[0]
    print(commit.commit.url)
    print(commit.author.url)
    # print(commit.author.html_url)
    # if(commit.commit.committer.date.date() < OBS_START_DATE.date()):
    #     break
    # else:
    # if(org_name != user_url):
    # print(org_name)
        # print(commit.commit.committer.date)
        # print(commit.commit.author.name)