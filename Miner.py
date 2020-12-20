import json
import os
import random
import sys

from sstubs_miner.miners.BugMiner import BugMiner
from sstubs_miner.miners.BuildMiner import BuildMiner
from sstubs_miner.util.CSVManager import CSVReader, CSVWriter
from sstubs_miner.util.GithubManager import GithubManager
from sstubs_miner.util.SStub import SStub


def main():
    dataset_file = 'data/sstubsLarge-0104.json'
    output_file = 'results/sstubs.csv'
    access_tokens = _load_tokens('data/tokens')

    sstubs = _load_dataset(dataset_file)
    start_index = _last_entry(output_file) if os.path.isfile(output_file) else 0
    end_index = len(sstubs)
    sstubs = sstubs[start_index+1:end_index]

    github = GithubManager(access_tokens)
    build_miner = BuildMiner(github)
    bug_miner = BugMiner(github)

    writer = CSVWriter(output_file, SStub.attribute_names())
    counter = start_index
    for sstub in sstubs:
        if github.exceeded_request_limit(offset=0.01):
            github.switch_connection(request_offset=0.01, sleep_offset=1)

        _update_status(counter, end_index, github.request_status())

        try:
            build_miner.mine(sstub)
            bug_miner.mine(sstub)
            writer.write(sstub.attribute_list())
            counter += 1
        except:
            os.execl(sys.executable, sys.executable, *sys.argv)


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


def _last_entry(output_file):
    csv_reader = CSVReader(output_file)
    data = csv_reader.read()
    last = data[-1]
    last_index = int(last['index'])
    return last_index


def _update_status(counter, total, requests):
    print('{}/{} SStuBs Mined ({} requests remaining) '.format(counter, total, requests), end='\r')
    if counter == total:
        print()


if __name__ == '__main__':
    main()
