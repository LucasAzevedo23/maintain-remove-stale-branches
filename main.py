import os
from github import Github
from github import Auth

github_token = os.environ['INPUT_TOKEN']
repo = os.environ['INPUT_REPOSITORY']
developer_team_slug = os.environ['INPUT_DEVELOPER_TEAM_SLUG']
admin_team_slug = os.environ['INPUT_ADMIN_TEAM_SLUG']

print(github_token)
print(repo)
print(developer_team_slug)
print(admin_team_slug)

auth = Auth.Token(github_token)

# Initialize the GitHub API client
github_instance = Github(auth=auth)

# Get the repository
repo = github_instance.get_repo(repo)

for branch in repo.get_branches():
    print(branch.name)

# # Calculate the timestamps for 2 and 3 weeks ago
# two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
# three_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=3)

# # Identify and manage branches
# for branch in repo.get_branches():
#     if branch.name == repo.default_branch:
#         # Skip the default branch
#         continue

#     last_commit = branch.commit.commit.author.date
#     last_activity = branch.commit.commit.committer.date if branch.commit.commit.committer else last_commit

#     if last_commit < two_weeks_ago:
#         # Mark as stale (more than 2 weeks old)
#         branch.edit(protection=False)

#     if last_activity < three_weeks_ago and not branch.is_merged():
#         # Prune if not merged and more than 3 weeks old with no new activity
#         branch.delete()
