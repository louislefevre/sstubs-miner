from github import Github
import random
import BuildMiner
import DataAnalyser
import DateMiner
from Dataset import Dataset


def mine(path, token):
    dataset = Dataset(path)
    github = Github(token)
    sstubs = dataset.get_sstubs()
    sstubs = minimize_dataset(sstubs)

    DateMiner.mine(github, sstubs)
    BuildMiner.mine(github, sstubs)

    DataAnalyser.analyse(sstubs)


# Used for testing purposes only.
def minimize_dataset(sstubs):
    while True:
        if len(sstubs) <= 200:
            break
        rand = random.randint(0, len(sstubs)-1)
        del sstubs[rand]
    return sstubs
