import datetime
import os
from github import Github
from github import Auth

# Retrieving input variables from environment variables
github_token = os.environ['INPUT_TOKEN']
repo = os.environ['INPUT_REPOSITORY']
developer_team_slug = os.environ['INPUT_DEVELOPER_TEAM_SLUG']
admin_team_slug = os.environ['INPUT_ADMIN_TEAM_SLUG']

print(github_token)
print(repo)
print(developer_team_slug)
print(admin_team_slug)

# Creating authentication object with the provided token
auth = Auth.Token(github_token)

# Initialize the GitHub API client
github_instance = Github(auth=auth)

# Get the repository
repo = github_instance.get_repo(repo)

# Calculate the timestamps for 2 and 3 weeks ago
two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
three_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=3)

# Identify and manage branches
for branch in repo.get_branches():
    if branch.name == repo.default_branch:
        # Skip the default branch
        continue

    last_commit = branch.commit.commit.author.date
    last_activity = branch.commit.commit.committer.date if branch.commit.commit.committer else last_commit
