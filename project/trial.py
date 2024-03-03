from github import Repository, RateLimit
from datetime import date, datetime, timedelta
from project.constants import *
from project.utils import *
import pandas as pd
from datetime import datetime


g = GITHUB_OBJ
email = "danclark@redhat.com"

shared = False
outside_repo_commits = 0

print(g.rate_limiting)

def rate_limit_status(rate_limit: RateLimit.RateLimit):
    print("--Rate Limit Status--")
    print("Core: ", [rate_limit.core.remaining, rate_limit.core.reset, rate_limit.core.limit])
    print("Search: ",[rate_limit.search.remaining, rate_limit.search.reset, rate_limit.search.limit])
    print("GraphQL: ", [rate_limit.graphql.remaining, rate_limit.graphql.reset])
    print()
t1 = datetime.now()
commits = g.search_commits(
    query=f'author-email:{email} committer-date:>{OBS_END_DATE.strftime("%Y-%m-%d")}'
)
for commit in commits:
    print(commit.commit.etag, commit.commit.committer.date, commit.commit.url, commit.author.url, commit.author.name)
    rate_limit_status(g.get_rate_limit())
    print("Normal Rate Limit: ", g.rate_limiting)

print(g.rate_limiting)
t2 = datetime.now()
print(t2 - t1)