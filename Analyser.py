from sstubs_miner.analysers.DataAnalyser import DataAnalyser
from sstubs_miner.util.CSVManager import CSVReader
from sstubs_miner.util.DataCleaner import DataCleaner
from sstubs_miner.util.SStub import SStub


def main():
    output_file = 'results/sstubs.csv'
    reader = CSVReader(output_file)
    sstubs = reader.read()

    sstubs = _load_dataset(sstubs)
    cleaner = DataCleaner(sstubs)
    sstubs = cleaner.clean()

    data_analyser = DataAnalyser(sstubs)
    sstubs_count = data_analyser.sstub_count()
    project_count = data_analyser.project_count()
    average_time = data_analyser.average_time()
    build_sstubs_count = data_analyser.build_sstub_count()
    build_project_count = data_analyser.build_project_count()
    build_average_time = data_analyser.average_build_time()
    loc_range_count = data_analyser.loc_range_count()
    loc_range_time = data_analyser.average_loc_time()
    project_sstub_count = data_analyser.project_sstub_count()

    print("\n---General---")
    print("SStuBs Count: {}".format(sstubs_count))
    print("Project Count: {}".format(project_count))
    print("Average Time: {}".format(average_time))

    print("\n---Builds---")
    print("Build SStuBs Count: {}".format(build_sstubs_count))
    print("Build Project Count: {}".format(build_project_count))
    print("Build Average Times: {}".format(build_average_time))

    print("\n---LOC---")
    print("LOC SStuBs Count: {}".format(loc_range_count))
    print("LOC Average Times: {}".format(loc_range_time))

    print("\n---Projects---")
    print("Project SStuB Count: {}".format(project_sstub_count))


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
