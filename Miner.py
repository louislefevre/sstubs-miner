from github import Github
import BuildMiner
import DateMiner
from Dataset import Dataset


def mine(path, token):
    dataset = Dataset(path)
    github = Github(token)
    sstubs = dataset.get_sstubs()

    DateMiner.mine(github, sstubs)
    BuildMiner.mine(github, sstubs)
