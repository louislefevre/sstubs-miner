from JsonManager import JsonReader
from SStub import SStub


class Dataset:
    def __init__(self, path):
        self._path = path

    def get_sstubs(self):
        reader = JsonReader(self._path)
        json_objects = reader.read()
        sstubs = []

        for obj in json_objects:
            sstub = SStub(obj['projectName'], obj['bugFilePath'], obj['sourceBeforeFix'],
                          obj['sourceAfterFix'], obj['fixCommitSHA1'])
            sstubs.append(sstub)

        reader.close()
        return sstubs
