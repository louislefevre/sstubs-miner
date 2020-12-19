import random
from sstubs_miner.miners.BugMiner import BugMiner
from sstubs_miner.miners.BuildMiner import BuildMiner
from sstubs_miner.util.CSVManager import CSVReader
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

    sstubs = _load_dataset(dataset_file)
    github = GithubMiner(access_token)

    results_file = 'results/sstubs.csv'
    if file_exists(results_file):
        print("'{}' already exists - would you like to continue from where you left off? [yes/no]".format(results_file))
        choice: str = input()
        if choice == 'yes' or choice == 'y':
            sstubs = _trim_dataset(results_file, sstubs)
        elif choice == 'no' or choice == 'n':
            print("Remove '{}' and rerun the program".format(results_file))
            return
        else:
            print('Invalid input')
            return

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


def _trim_dataset(output_file, sstubs):
    csv_reader = CSVReader(output_file)
    data = csv_reader.read()
    last = data[-1]
    start_point = int(last['index']) + 1
    return sstubs[start_point:]


if __name__ == '__main__':
    main()
