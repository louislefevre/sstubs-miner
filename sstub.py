class SStub:
    def __init__(self, project_name, file_path, commit_sha, source_before, source_after):
        self._project_name = project_name
        self._file_path = file_path
        self._commit_sha = commit_sha
        self._source_before = source_before
        self._source_after = source_after

    def get_project_name(self):
        return self._project_name

    def get_file_path(self):
        return self._file_path

    def get_commit_sha(self):
        return self._commit_sha

    def get_source_before(self):
        return self._source_before

    def get_source_after(self):
        return self._source_after
