import datetime
from github import Github
from github import Auth

# Inputs
token=""
repo_slug="wexinc/ps-ds-peng-docs"
admin_team_slug="platform-eng-admin"
developer_team_slug="platform-eng"

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
org = github_instance.get_organization("wexinc")

# Branches, teams and closed pull requests retrieval
branches = repo.get_branches()
pull_requests = repo.get_pulls(state='closed')
teams = org.get_teams()

for pr in pull_requests:
    array_merged_branches.append(pr.head.ref)

print("-- Merged branches --")
print(array_merged_branches)
print()

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
    if branch.name == "main" or branch.name == "dev":
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
    # Check if branch author is older than 14 days
    if delta.days >= 14:
        dict_branches.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'should_be_deleted': True })
    else:
        dict_branches.append({ 'branch_name': branch.name,
                'author_name': branch.commit.commit.author.name,
                'author_email': branch.commit.commit.author.email,
                'last_modified': delta.days,
                'should_be_deleted': False })

print()
print(dict_branches)

print()
print()
print('Branches to be deleted:')
for d in dict_branches:
    if d.get('should_be_deleted') == True:
        print(d.get('branch_name'))
        print(d.get('last_modified'))
        print(d.get('should_be_deleted'))
        print()
