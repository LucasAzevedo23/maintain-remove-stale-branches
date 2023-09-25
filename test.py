import datetime
from github import Github
from github import Auth

# Inputs
token="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"
repo_slug="wexinc/ps-ds-peng-docs"
days_to_stale=21
# admin_team_slug="platform-eng-admin"
# developer_team_slug="platform-eng"

# Structures to be used
dict_branches = []
array_admins = []
array_developers = []
array_merged_branches = []

# Github Library initial configuration
auth = Auth.Token(token)
github_instance = Github(auth=auth)

# Repo and Org retrieval
repo = github_instance.get_repo(repo_slug)
#org = github_instance.get_organization("wexinc")

# Branches, teams and closed pull requests retrieval
branches = repo.get_branches()
pull_requests = repo.get_pulls(state='closed')
#teams = org.get_teams()

for pr in pull_requests:
    array_merged_branches.append(pr.head.ref)

# for team in teams:
#     # Append admin members to array_admins
#     if team.name == admin_team_slug:
#         for member in team.get_members():
#             user = github_instance.get_user(member.login)
#             array_admins.append({'name': user.name, 'email': user.email, 'login': user.login})
#     # Append developer members to array_developers
#     if team.name == developer_team_slug:
#         for member in team.get_members():
#             user = github_instance.get_user(member.login)
#             array_developers.append({'name': user.name, 'email': user.email, 'login': user.login})

# print("-- Admins --")
# print(array_admins)
# print()

# print("-- Developers --")
# print(array_developers)
# print()

for branch in branches:
    # Check if branch is main or dev and skip
    if branch.name == "main" or branch.name == "dev" or branch.name == "develop" or branch.name == "master":
        continue

    # Setup date variables and delta between now and last modified
    date_now = datetime.datetime.utcnow()
    date_last_modified = branch.commit.commit.last_modified
    converted = datetime.datetime.strptime(date_last_modified, '%a, %d %b %Y %H:%M:%S GMT')
    delta = date_now - converted


    # Check if branch author is not in users array
    # if branch.commit.commit.author.email not in array_admins and branch.commit.commit.author.email not in array_developers:
    #     dict_branches.append({ 'branch_name': branch.name,
    #             'author_name': branch.commit.commit.author.name,
    #             'author_email': branch.commit.commit.author.email,
    #             'last_modified': delta.days,
    #             'should_be_deleted': True })
    # Check if branch was already merged
    if branch.name in array_merged_branches:
        dict_branches.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'already merged',
                'should_be_deleted': True })
        continue
    # Check if branch author is older than 14 days
    elif delta.days >= days_to_stale:
        dict_branches.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': 'stale',
                'should_be_deleted': True })
        continue
    else:
        dict_branches.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'reason': '',
                'should_be_deleted': False })
        continue

print('Branches to be deleted:\n')
for d in dict_branches:
    if d.get('should_be_deleted') == True:
        print("Branch name: ",  d.get('branch_name'))
        print("Last Modification: ", d.get('last_modified'), "days")
        print("Reason: ", d.get('reason'))
        print()
