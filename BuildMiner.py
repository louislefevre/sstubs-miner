from JsonManager import JsonWriter


class BuildMiner:
    def __init__(self, github, sstubs, sstubs_file, builds_file='data/builds.txt', output_file='results/builds.json'):
        self._github = github
        self._sstubs = sstubs
        self._sstubs_file = sstubs_file
        self._projects = self._load_projects(sstubs)
        self._builds = self._load_builds(builds_file)
        self._output_file = output_file
        self._counter = 0

    def mine(self):
        self._mine_builds()
        self._add_builds()
        self._write_builds()

    def _mine_builds(self):
        for project_name in self._projects.keys():
            self._update_status(project_name)
            repo = self._github.get_repo(project_name)
            contents = repo.get_contents('')

            for file in contents:
                file_name = file.name.lower()
                for build_name in self._builds.keys():
                    if file_name == build_name:
                        self._projects[project_name] = build_name
                        self._builds[build_name] += 1
                        break
                else:
                    continue
                break
            else:
                self._builds['none'] += 1

    def _add_builds(self):
        writer = JsonWriter(self._sstubs_file)
        for i in range(len(self._sstubs)):
            for name, build in self._projects.items():
                if self._sstubs[i].project_name == name:
                    self._sstubs[i].build_system = build
                    writer.update(str(i), '_build_system', build)

    def _write_builds(self):
        writer = JsonWriter(self._output_file)
        writer.write(self._builds)

    def _update_status(self, name):
        self._counter += 1
        total_projects = len(self._projects)
        blank_string = '                                   '
        print('({}/{}) {}{}'.format(self._counter, total_projects, name, blank_string), end='\r')
        if self._counter == total_projects:
            print()

    @staticmethod
    def _load_projects(sstubs):
        projects_set = set()
        for sstub in sstubs:
            projects_set.add(sstub.project_name)

        project_dict = {}
        for name in projects_set:
            project_dict[name] = ''

        return project_dict

    @staticmethod
    def _load_builds(builds_file):
        builds = {'none': 0}
        with open(builds_file) as file:
            for line in file:
                builds[line.strip()] = 0
        return builds
