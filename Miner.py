import sys
import json
from github import Github


# Retrieves arguments passed with program execution. Only 1 argument is allowed.
# Used to retrieve the users personal access token for GitHub access.
# This is necessary to avoid developers accidentally committing their token to the public repository.
def validate_args(args):
    args_length = len(args)
    
    if args_length == 2:
        return True
    elif args_length < 2:
        print("Missing personal access token - pass as an argument, for example:")
        print("'python Miner.py 400acc25ffh21jj66...'")
    elif args_length > 2:
        print("Too many arguments - maximum of 1 allowed")
    return False


# Checks to see if the access token is valid, as it must be 40 characters in length.
def validate_token(token):
    if len(token) != 40:
        print("Invalid access token - must be 40 characters in length")
        return False
    return True


# Loads the dataset and extract the 'projectName' attribute from each entry.
# The project names are placed into a set to avoid duplicates.
def load_names():
    dataset = open('sstubsLarge-0104.json')
    sstubs = json.load(dataset)
    projects = set()

    for sstub in sstubs:
        projects.add(sstub['projectName'])
    
    dataset.close()
    return projects


# Generate a dictionary containing the build systems the program will check for.
def load_builds():
    builds = {
            'makefile': 0,
            'build.xml': 0,
            'pom.xml': 0,
            'build.gradle': 0,
            'build': 0,
            'cmakelists.txt': 0
            }
    return builds


# Compares the file name to the build system dictionary.
# If the file name matches one of the build file keys, its value is incremented by 1.
def match_builds(builds, name):
    name = name.lower()
    
    for key, value in builds.items():
        if name == key:
            builds[key] += 1
            return


# Accesses GitHub using a personal access token.
# Iterates through the projects retrieved from the dataset, and retrieves their top-level contents.
# For each file in the repositories contents, check it against the build systems dictionary.
def mine_repos(token, projects, builds):
    github = Github(token)
    counter = 0
    
    for project in projects:
        owner, name = project.split('.')
        repo = github.get_repo(owner + "/" + name)
        contents = repo.get_contents("")
        counter += 1
        print('({}/{}) {}/{}'.format(counter, len(projects), owner, name))

        for content_file in contents:
            file_name = content_file.name
            match_builds(builds, file_name)


# Print the results for each build system.
# Also prints the amount of projects which the program could not find a build system for.
def print_results(builds, projects):
    total_projects = len(projects)
    total_builds = 0
    
    for key, value in builds.items():
        total_builds += value
        print('{} has {} occurrences.'.format(key, value))
    print('{} projects had another or no build system.'.format(total_projects-total_builds))


# Program execution
def main(): 
    if not validate_args(sys.argv):
        sys.exit()

    access_token = sys.argv[1]
    if not validate_token(access_token):
        sys.exit()

    project_names = load_names()
    build_systems = load_builds()

    mine_repos(access_token, project_names, build_systems)
    print_results(build_systems, project_names)


# Program initialisation
if __name__ == "__main__":
    main()
