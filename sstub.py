class SStub:
    def __init__(self, project_name, path, bug_source, fix_source, fix_sha):
        self._project_name = project_name
        self._path = path
        self._bug_source = bug_source
        self._fix_source = fix_source
        self._fix_sha = fix_sha
        self._bug_sha = None
        self._fix_time = None
        self._bug_time = None

    @property
    def project_name(self):
        owner, name = self._project_name.split('.')
        return owner + "/" + name

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
    def fix_time(self):
        return self._fix_time

    @fix_time.setter
    def fix_time(self, time):
        self._fix_time = time

    @property
    def bug_time(self):
        return self._bug_time

    @bug_time.setter
    def bug_time(self, time):
        self._bug_time = time
