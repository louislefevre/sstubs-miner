import json
from sstub import SStub


class Dataset:
    def __init__(self, path):
        self._path = path

    def get_sstubs(self):
        dataset = open(self._path)
        json_objects = json.load(dataset)
        sstubs = []

        for obj in json_objects:
            project_name = obj['projectName']
            file_path = obj['bugFilePath']
            commit_sha = obj['fixCommitSHA1']
            source_before = obj['sourceBeforeFix']
            source_after = obj['sourceAfterFix']

            sstub = SStub(project_name, file_path, commit_sha, source_before, source_after)
            sstubs.append(sstub)

        dataset.close()
        return sstubs

    def get_project_names(self):
        project_names = set()
        sstubs = self.get_sstubs()

        for sstub in sstubs:
            project_names.add(sstub.get_project_name())

        return project_names
