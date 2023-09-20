from github import Github
from github import Auth
import os
import datetime

# Initialize the GitHub API client
g = Github("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")

# Get the repository
repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])

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

    if last_commit < two_weeks_ago:
        # Mark as stale (more than 2 weeks old)
        branch.edit(protection=False)

    if last_activity < three_weeks_ago and not branch.is_merged():
        # Prune if not merged and more than 3 weeks old with no new activity
        branch.delete()
