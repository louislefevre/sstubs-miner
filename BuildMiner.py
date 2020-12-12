# Generate a dictionary containing the files the program will check for.
from JsonManager import JsonWriter


def load_builds(path):
    builds = {}
    with open(path) as file:
        for line in file:
            builds[line.strip()] = 0
    return builds


def load_names(sstubs):
    project_names_set = set()
    for sstub in sstubs:
        project_names_set.add(sstub.project_name)

    project_names_dict = {}
    for name in project_names_set:
        project_names_dict[name] = ''

    return project_names_dict


# Accesses GitHub using a personal access token.
# Iterates through the projects retrieved from the dataset, and retrieves their top-level contents.
# For each file in the repositories contents, check it against the build systems dictionary.
def mine_repos(github, project_names, builds):
    counter = 0
    
    for name in project_names.keys():
        counter += 1
        blank_string = '                                   '
        print('({}/{}) {}{}'.format(counter, len(project_names), name, blank_string), end='\r')

        repo = github.get_repo(name)
        contents = repo.get_contents('')

        for content_file in contents:
            file_name = content_file.name.lower()

            for key in builds.keys():
                if file_name == key:
                    project_names[name] = key
                    builds[key] += 1
                    break
            else:
                continue
            break


def add_builds(sstubs, project_names):
    for sstub in sstubs:
        for name, build in project_names.items():
            if sstub.project_name == name:
                sstub.build_system = build


# Print the results for each build system.
# Also prints the amount of projects which the program could not find a build system for.
def print_results(builds, project_names):
    total_projects = len(project_names)
    total_builds = 0

    for key, value in builds.items():
        total_builds += value
        print('{} has {} occurrences.'.format(key, value))
    print('{} projects had another or no build system.'.format(total_projects-total_builds))


def mine(github, sstubs):
    build_names = load_builds('builds.txt')
    project_names = load_names(sstubs)

    mine_repos(github, project_names, build_names)
    add_builds(sstubs, project_names)

    writer = JsonWriter('builds')
    writer.write(build_names)

    print_results(build_names, project_names)
