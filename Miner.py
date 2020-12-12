from github import Github
import random
import BuildMiner
import DataAnalyser
import DateMiner
from JsonManager import JsonReader
from SStub import SStub


def mine(path, token):
    github = Github(token)
    sstubs = _load_dataset(path)

    BuildMiner.mine(github, sstubs)
    DateMiner.mine(github, sstubs)
    DataAnalyser.analyse(sstubs)


def _load_dataset(path, randomise=False, size=0):
    reader = JsonReader(path)
    dataset = reader.read()

    if randomise:
        random.shuffle(dataset)
    if size == 0:
        size = len(dataset)

    sstubs = []
    for i in range(size):
        obj = dataset[i]
        sstub = SStub(i, obj['projectName'], obj['bugFilePath'], obj['sourceBeforeFix'],
                      obj['sourceAfterFix'], obj['fixCommitSHA1'])
        sstubs.append(sstub)

    reader.close()
    return sstubs
