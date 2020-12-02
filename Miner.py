from github import Github
import json

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
g = Github("Access token")

for project in projects:
    owner, name = project.split('.')
    repo = g.get_repo(owner + "/" + name)
    contents = repo.get_contents("")
    for content_file in contents:
        file_name = content_file.name
        if file_name == "pom.xml":
            print(owner + "/" + name + " uses Maven!")
