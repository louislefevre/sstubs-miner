from sstubs_miner.analysers.DataAnalyser import DataAnalyser
from sstubs_miner.util.CSVManager import CSVReader

from sstubs_miner.util.DataCleaner import DataCleaner
from sstubs_miner.util.SStub import SStub


def main():
    output_file = 'results/sstubs.csv'
    reader = CSVReader(output_file)
    sstubs = reader.read()
    sstubs = _load_dataset(sstubs)

    cleaner = DataCleaner()
    sstubs = cleaner.clean(sstubs)
    data_analyser = DataAnalyser(sstubs)

    sstubs_count = data_analyser.sstub_count()
    average_time = data_analyser.average_time()
    project_count = data_analyser.project_count()

    build_sstubs_count = data_analyser.build_sstub_count()
    build_average_time = data_analyser.average_build_time()
    build_project_count = data_analyser.build_project_count()

    print("Total SStuBs: {}".format(sstubs_count))
    print("Average Time: {}".format(average_time))
    print("Project Count: {}".format(project_count))
    print("Average Build Times: {}".format(build_average_time))
    print("Build SStuBs Count: {}".format(build_sstubs_count))
    print("Build Project Count: {}".format(build_project_count))


def _load_dataset(sstubs):
    sstub_objects = []
    for sstub in sstubs:
        sstub_obj = SStub(sstub.get('index'), sstub.get('project_name'),
                          sstub.get('path'), sstub.get('bug_source'),
                          sstub.get('fix_source'), sstub.get('fix_sha'))
        sstub_obj.build_system = sstub.get('build_system')
        sstub_obj.loc = sstub.get('loc')
        sstub_obj.bug_sha = sstub.get('bug_sha')
        sstub_obj.bug_date = sstub.get('bug_date')
        sstub_obj.fix_date = sstub.get('fix_date')
        sstub_objects.append(sstub_obj)
    return sstub_objects


if __name__ == '__main__':
    main()
