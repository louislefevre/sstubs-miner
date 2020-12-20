import json
import os
import random
from sstubs_miner.miners.BugMiner import BugMiner
from sstubs_miner.miners.BuildMiner import BuildMiner
from sstubs_miner.util.CSVManager import CSVReader, CSVWriter
from sstubs_miner.util.GithubManager import GithubManager
from sstubs_miner.util.SStub import SStub


def main():
    dataset_file = 'data/sstubsLarge-0104.json'
    results_file = 'results/sstubs.csv'
    access_tokens = _load_tokens('data/tokens')

    sstubs = _load_dataset(dataset_file)
    if os.path.isfile(results_file):
        sstubs = _trim_dataset(results_file, sstubs)

    github = GithubManager(access_tokens)
    build_miner = BuildMiner(github)
    bug_miner = BugMiner(github)

    writer = CSVWriter(results_file, SStub.attribute_names())
    counter = 0
    for sstub in sstubs:
        if github.exceeded_request_limit(offset=0.05):
            github.switch_connection(request_offset=0.05, sleep_offset=2)

        try:
            build_miner.mine(sstub)
            bug_miner.mine(sstub)
            writer.write(sstub.attribute_list())
        except KeyboardInterrupt:
            print("\nExiting program...")
            return
        except:
            print("\nResetting connection...")
        finally:
            counter += 1
            _update_status(counter, len(sstubs), github.request_status())


def _load_tokens(tokens_file):
    tokens = []
    with open(tokens_file) as file:
        for line in file:
            tokens.append(line.strip())
    return tokens


def _load_dataset(input_file, randomise=False, size=0):
    file = open(input_file)
    dataset = json.load(file)

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

    file.close()
    return sstubs_list


def _trim_dataset(output_file, sstubs):
    csv_reader = CSVReader(output_file)
    data = csv_reader.read()
    last = data[-1]
    start_point = int(last['index']) + 1
    return sstubs[start_point:]


def _update_status(counter, total, requests):
    counter += 1
    print('{}/{} SStuBs Mined ({} requests remaining) '.format(counter, total, requests), end='\r')
    if counter == total:
        print()


if __name__ == '__main__':
    main()
