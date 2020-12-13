import random
from DateMiner import DateMiner
from BuildMiner import BuildMiner
from GithubMiner import GithubMiner
from JsonManager import JsonReader, JsonWriter
from SStub import SStub


def mine(dataset_file, token, sstubs_file='results/sstubs.json'):
    github = GithubMiner(token)
    sstubs = _load_dataset(dataset_file, sstubs_file)

    build_miner = BuildMiner(github, sstubs, sstubs_file)
    build_miner.mine()

    date_miner = DateMiner(github, sstubs, sstubs_file)
    date_miner.mine()


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
