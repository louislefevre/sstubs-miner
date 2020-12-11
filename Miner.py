from github import Github
import random
import BuildMiner
import DataAnalyser
import DateMiner
from JsonManager import JsonWriter
from Dataset import Dataset


def mine(path, token):
    dataset = Dataset(path)
    github = Github(token)
    data_saver = JsonWriter('results.json')
    sstubs = dataset.get_sstubs()
    sstubs = minimise_dataset(sstubs, 10)

    BuildMiner.mine(github, data_saver, sstubs)
    DateMiner.mine(github, sstubs)
    DataAnalyser.analyse(sstubs)


# Used for testing purposes only.
def randomise_dataset(sstubs, size):
    while True:
        if len(sstubs) <= size:
            break
        rand = random.randint(0, len(sstubs)-1)
        del sstubs[rand]
    return sstubs


# Used for testing purposes only.
def minimise_dataset(sstubs, size):
    del sstubs[:size]
    return sstubs
