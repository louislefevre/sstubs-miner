class SStub:
    def __init__(self, index, project_name, path, bug_source, fix_source, fix_sha):
        self._index = index
        self._project_name = project_name
        self._path = path
        self._build_system = None
        self._loc = None
        self._bug_source = bug_source
        self._fix_source = fix_source
        self._bug_sha = None
        self._fix_sha = fix_sha
        self._bug_date = None
        self._fix_date = None

    def attribute_list(self):
        return [self.index, self.project_name, self.path, self.build_system,
                self.loc, self.bug_source, self.fix_source, self.bug_sha,
                self.fix_sha, self.bug_date, self.fix_date]

    @staticmethod
    def attribute_names():
        return ['index', 'project_name', 'path', 'build_system',
                'loc', 'bug_source', 'fix_source', 'bug_sha',
                'fix_sha', 'bug_date', 'fix_date', ]

    @property
    def index(self):
        return self._index

    @property
    def project_name(self):
        if '.' in self._project_name:
            owner, name = self._project_name.split('.')
            return owner + "/" + name
        return self._project_name

    @property
    def path(self):
        return self._path

    @property
    def bug_source(self):
        return self._bug_source

    @property
    def fix_source(self):
        return self._fix_source

    @property
    def fix_sha(self):
        return self._fix_sha

    @property
    def bug_sha(self):
        return self._bug_sha

    @bug_sha.setter
    def bug_sha(self, sha):
        self._bug_sha = sha

    @property
    def fix_date(self):
        return self._fix_date

    @fix_date.setter
    def fix_date(self, time):
        self._fix_date = str(time)

    @property
    def bug_date(self):
        return self._bug_date

    @bug_date.setter
    def bug_date(self, time):
        self._bug_date = str(time)

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, loc):
        self._loc = loc

    @property
    def build_system(self):
        return self._build_system

    @build_system.setter
    def build_system(self, build_system):
        self._build_system = build_system
