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
            sstub = SStub(obj['projectName'], obj['bugFilePath'], obj['sourceBeforeFix'],
                          obj['sourceAfterFix'], obj['fixCommitSHA1'])
            sstubs.append(sstub)

        dataset.close()
        return sstubs

    def get_project_names(self):
        project_names = set()
        sstubs = self.get_sstubs()

        for sstub in sstubs:
            project_names.add(sstub.project_name)

        return project_names
