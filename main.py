import datetime
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

for branch in branches:
    # Check if branch is main or dev and skip
    if branch.name == "main" or branch.name == "dev" or branch.name == "develop" or branch.name == "master":
        continue

    # Setup date variables and delta between now and last modified
    date_now = datetime.datetime.utcnow()
    date_last_modified = branch.commit.commit.last_modified
    converted = datetime.datetime.strptime(date_last_modified, '%a, %d %b %Y %H:%M:%S GMT')
    delta = date_now - converted

    # Check if branch was already merged
    if branch.name in merged_branches:
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'already merged',
                'should_be_deleted': True })
        continue
    # Check if branch last_modified is older than the defined days_to_stale input
    elif delta.days >= days_to_stale:
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'stale',
                'should_be_deleted': True })
        continue
    else:
        branches_dictionary.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': '',
                'should_be_deleted': False })
        continue

print('Branches to be deleted:')
for d in branches_dictionary:
    if d.get('should_be_deleted') == True:
        print("Branch name: ",  d.get('branch_name'))
        print("Last Modification: ", d.get('last_modified'), "days")
        print("Reason: ", d.get('reason'))
        print()
