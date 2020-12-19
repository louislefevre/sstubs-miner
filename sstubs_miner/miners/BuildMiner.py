from sstubs_miner.util.JsonManager import JsonWriter


class BuildMiner:
    def __init__(self, github, sstubs):
        self._github = github
        self._sstubs = sstubs
        self._projects = self._load_projects(sstubs)
        self._projects_file = 'results/project_builds.json'
        self._builds = self._load_builds('data/builds.txt')
        self._builds_file = 'results/builds.json'
        self._counter = 0

    def mine(self):
        self._mine_builds()
        self._add_builds()
        self._write_builds()
        self._write_projects()

    def _mine_builds(self):
        for project_name in self._projects.keys():
            contents = self._github.get_contents(project_name, '')

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
            self._update_status()

    def _add_builds(self):
        sstub_dict = {}
        for i in range(len(self._sstubs)):
            sstub_dict[i] = self._sstubs[i]
            for name, build in self._projects.items():
                if self._sstubs[i].project_name == name:
                    self._sstubs[i].build_system = build

    def _write_builds(self):
        writer = JsonWriter(self._builds_file)
        writer.write(self._builds)

    def _write_projects(self):
        writer = JsonWriter(self._projects_file)
        writer.write(self._projects)

    def _update_status(self):
        self._counter += 1
        total_projects = len(self._projects)
        print('{}/{} Builds mined ({} requests remaining)'
              .format(self._counter, total_projects, self._github.request_status()), end='\r')
        if self._counter == total_projects:
            print()
        if self._github.exceeded_request_limit(0.01):
            self._github.sleep(offset=1)

    @staticmethod
    def _load_projects(sstubs):
        project_dict = {}
        for sstub in sstubs:
            project_dict[sstub.project_name] = ''
        return project_dict

    @staticmethod
    def _load_builds(builds_file):
        builds = {'none': 0}
        with open(builds_file) as file:
            for line in file:
                builds[line.strip()] = 0
        return builds
