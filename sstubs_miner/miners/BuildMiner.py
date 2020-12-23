class BuildMiner:
    def __init__(self, github):
        self._github = github
        self._projects = {}
        self._builds = ['build.gradle', 'build.gradle.kts',
                        'pom.xml', 'build.bazel', 'build',
                        'build.xml']

    def mine(self, sstub):
        project_name = sstub.project_name
        if project_name in self._projects.keys():
            sstub.build_system = self._projects[project_name]
            return

        contents = self._github.get_contents(project_name, '')
        for file in contents:
            file_name = file.name.lower()
            for build_name in self._builds:
                if file_name == build_name:
                    sstub.build_system = build_name
                    self._projects[project_name] = build_name
                    break
            else:
                continue
            break
