class TestMiner:
    def __init__(self, github, sstubs):
        self._github = github
        self._sstubs = sstubs
        self._projects = self._load_projects(sstubs)
        self._counter = 0

    def mine(self):
        self._mine_tests()

    def _mine_tests(self):
        for project_name in self._projects.keys():
            tests = 0
            contents = self._github.get_contents(project_name, '')
            while contents:
                file_content = contents.pop(0)
                if file_content.type == 'dir':
                    contents.extend(self._github.get_contents(project_name, file_content.path))
                    continue
                if file_content.name.endswith('Test.java'):
                    tests += 1
            print('{}: {}'.format(project_name, tests))
            self._update_status()

    def _update_status(self):
        self._counter += 1
        total_projects = len(self._projects)
        print('({}/{}) Tests mined ({} requests remaining)'
              .format(self._counter, total_projects, self._github.request_status()), end='\r')
        if self._counter == total_projects:
            print()
        if self._github.exceeded_request_limit(0.1):
            self._github.sleep(offset=1)

    @staticmethod
    def _load_projects(sstubs):
        project_dict = {}
        for sstub in sstubs:
            project_dict[sstub.project_name] = ''
        return project_dict
