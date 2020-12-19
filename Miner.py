import random
from sstubs_miner.miners.BugMiner import BugMiner
from sstubs_miner.miners.BuildMiner import BuildMiner
from sstubs_miner.util.GithubManager import GithubMiner
from sstubs_miner.util.InputManager import validate_path, validate_extension, validate_token, file_exists
from sstubs_miner.util.JsonManager import JsonReader
from sstubs_miner.util.SStub import SStub


def main():
    dataset_file: str = input('Dataset Path: ')
    if not validate_path(dataset_file) or not validate_extension(dataset_file, '.json'):
        print("Invalid path - file must be a valid JSON file")
        return

    access_token: str = input('Access Token: ')
    if not validate_token(access_token, 40):
        print("Invalid access token - must be 40 characters in length")
        return

    results_file = 'results/sstubs.csv'
    if file_exists(results_file):
        print("Results file already exists - remove 'results/sstubs.json'")
        return

    github = GithubMiner(access_token)
    sstubs = _load_dataset(dataset_file)

    build_miner = BuildMiner(github, sstubs)
    build_miner.mine()

    bug_miner = BugMiner(github, sstubs, results_file)
    bug_miner.mine()


def _load_dataset(input_file, randomise=False, size=0):
    reader = JsonReader(input_file)
    dataset = reader.read()

    if randomise:
        random.shuffle(dataset)
    if size == 0:
        size = len(dataset)

    sstubs_list = []
    for i in range(size):
        obj = dataset[i]
        sstub = SStub(i, obj['projectName'], obj['bugFilePath'], obj['sourceBeforeFix'],
                      obj['sourceAfterFix'], obj['fixCommitSHA1'])
        sstubs_list.append(sstub)

    reader.close()
    return sstubs_list


if __name__ == '__main__':
    main()
