import random
from sstubs_miner.miners.DateMiner import DateMiner
from sstubs_miner.miners.BuildMiner import BuildMiner
from sstubs_miner.util.GithubManager import GithubMiner
from sstubs_miner.util.InputManager import validate_path, validate_extension, validate_token, file_exists
from sstubs_miner.util.JsonManager import JsonReader, JsonWriter
from sstubs_miner.util.SStub import SStub


def main():
    _main_options()
    while True:
        option: str = input()

        if option == '0' or not option:
            break
        elif option == '1':
            _miner()
            break
        elif option == '2':
            _analyser()
            break
        else:
            print("Invalid input - select an option from the list")


def _miner():
    access_token: str = input('Access Token: ')
    if not validate_token(access_token, 40):
        print("Invalid access token - must be 40 characters in length")
        return

    dataset_file: str = input('Dataset Path: ')
    if not validate_path(dataset_file) or not validate_extension(dataset_file, '.json'):
        print("Invalid path - file must be a valid JSON file")
        return

    sstubs_file = 'results/sstubs.json'
    if file_exists(sstubs_file):
        print("Results file already exists - remove 'results/sstubs.json'")
        return

    github = GithubMiner(access_token)
    sstubs = _load_dataset(dataset_file, sstubs_file)

    _miner_options()
    while True:
        option: str = input()

        if option == '0':
            break
        elif option == '1':
            build_miner = BuildMiner(github, sstubs, sstubs_file)
            build_miner.mine()
        elif option == '2':
            date_miner = DateMiner(github, sstubs, sstubs_file)
            date_miner.mine()
        else:
            print("Invalid input - select an option from the list")


def _analyser():
    pass


def _main_options():
    print()
    print('0: Exit')
    print('1: Miners')
    print('2: Analysers')


def _miner_options():
    print()
    print('0: Exit')
    print('1: Build Miner')
    print('2: Date Miner')


def _analyser_options():
    pass


def _load_dataset(input_file, output_file, randomise=False, size=0):
    reader = JsonReader(input_file)
    writer = JsonWriter(output_file)
    dataset = reader.read()

    if randomise:
        random.shuffle(dataset)
    if size == 0:
        size = len(dataset)

    sstubs_dict = {}
    sstubs_list = []
    for i in range(size):
        obj = dataset[i]
        sstub = SStub(obj['projectName'], obj['bugFilePath'], obj['sourceBeforeFix'],
                      obj['sourceAfterFix'], obj['fixCommitSHA1'])
        sstubs_dict[i] = sstub.__dict__
        sstubs_list.append(sstub)

    writer.write(sstubs_dict, mode='x')
    reader.close()
    return sstubs_list
