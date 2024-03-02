from github import Repository
from datetime import date, datetime
from project.constants import *
from project.utils import *
import pandas as pd

g = GITHUB_OBJ
email = "danclark@redhat.com"

shared = False
outside_repo_commits = 0
commits = g.search_commits(
    query=f'author-email:{email} committer-date:<{OBS_END_DATE.strftime("%Y-%m-%d")}'
)
for commit in commits:
    print(commit.commit.etag, commit.commit.committer.date, commit.commit.url, commit.author.url, commit.author.name)
