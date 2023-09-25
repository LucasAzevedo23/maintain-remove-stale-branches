from datetime import datetime, timezone
import os
from github import Github
from github import Auth

# Retrieving input variables from environment variables
github_token = os.environ['INPUT_TOKEN']
repo = os.environ['INPUT_REPOSITORY']
days_to_stale = int(os.environ['INPUT_DAYS_TO_STALE'])

# Structures to be used
branches_dictionary = []
merged_branches = []

# Github Library initial configuration
auth = Auth.Token(github_token)
github_instance = Github(auth=auth)

# Get the repository
repo = github_instance.get_repo(repo)

# Branches, teams and closed pull requests retrieval
branches = repo.get_branches()
pull_requests = repo.get_pulls(state='closed')

# Retrieve branch name from closed pull requests
for pr in pull_requests:
    merged_branches.append(pr.head.ref)


print("-- Checking branches --")
print()
for branch in branches:
    # Check if branch is main or dev and skip
    if branch.name == "main" or branch.name == "dev" or branch.name == "develop" or branch.name == "master":
        continue

    # Setup date variables and delta between now and last modified
    date_now = datetime.now(timezone.utc)
    date_last_modified = datetime.strptime(branch.commit.commit.last_modified, '%a, %d %b %Y %H:%M:%S GMT').astimezone(timezone.utc)
    delta = date_now - date_last_modified

    # Check if branch was already merged
    if branch.name in merged_branches:
        print(" - branch", branch.name, "was already merged")
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'already merged',
                'should_be_deleted': True })
        continue
    # Check if branch last_modified is older than the defined days_to_stale input
    elif delta.days >= days_to_stale:
        print(" - branch", branch.name, "have not been modified in", delta.days, "days")
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'stale',
                'should_be_deleted': True })
        continue
    else:
        print(" - branch", branch.name, "is active")
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': '',
                'should_be_deleted': False })
        continue

print('-- Branches to be marked as stale --')
print()
for d in branches_dictionary:
    if d.get('should_be_deleted') == True:
        print(" Branch name: ",  d.get('branch_name'))
        print(" Last Modification: ", d.get('last_modified'), "days")
        print(" Reason: ", d.get('reason'))
        print()
