import sys
import json
from github import Github

# Retrieves arguments passed with program execution. Only 1 argument is allowed.
# Used to retrieve the users personal access token for GitHub access.
# This is necessary to avoid developers accidentally committing their token to the public repository.
args_length = len(sys.argv)
if args_length < 2:
    print("Missing personal access token - pass as an argument, for example:")
    print("'python Miner.py 400acc25ffh21jj66...'")
    sys.exit()
elif args_length > 2:
    print("Too many arguments - maximum of 1 allowed")
    sys.exit()


# Checks to see if the access token is valid, as it must be 40 characters in length.
access_token = sys.argv[1]
if len(access_token) != 40:
    print("Invalid access token - must be 40 characters in length")
    sys.exit()


# Loads the dataset and extract the 'projectName' attribute from each entry.
# The project names are placed into a set to avoid duplicates.
dataset = open('sstubsLarge-0104.json')
sstubs = json.load(dataset)
projects = set()

for sstub in sstubs:
    projects.add(sstub['projectName'])

dataset.close()


###
build_systems = {
        'makefile': 0,
        'build.xml': 0,
        'pom.xml': 0,
        'build.gradle': 0,
        '': 0
        }


# Accesses GitHub using a personal access token.
# Iterates through the projects retrieved from the dataset, and retrieves their top-level contents.
# For each file within their contents, check to see if it matches the Maven build file.
github = Github(access_token)

counter = 0
for project in projects:
    owner, name = project.split('.')
    repo = github.get_repo(owner + "/" + name)
    contents = repo.get_contents("")
    counter += 1
    print('({}/{}) {}/{}'.format(counter, len(projects), owner, name))
    for content_file in contents:
        file_name = content_file.name.lower()
        for key, value in build_systems.items():
            if file_name == key:
                build_systems[key] += 1
                break

for key, value in build_systems.items():
    print('{} has {} occurrences'.format(key, value))




