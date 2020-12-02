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


# Accesses GitHub using a personal access token.
# Iterates through the projects retrieved from the dataset, and retrieves their top-level contents.
# For each file within their contents, check to see if it matches the Maven build file.
g = Github(access_token)

for project in projects:
    owner, name = project.split('.')
    repo = g.get_repo(owner + "/" + name)
    contents = repo.get_contents("")
    for content_file in contents:
        file_name = content_file.name
        if file_name == "pom.xml":
            print(owner + "/" + name + " uses Maven!")
