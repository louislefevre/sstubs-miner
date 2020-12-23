from statistics import mean
from datetime import datetime, timedelta


class DataAnalyser:
    def __init__(self, sstubs):
        self._sstubs = sstubs
        self._builds = self._initialise_builds(sstubs)

    def average_time(self):
        return self._get_mean_time(self._sstubs)

    def average_build_time(self):
        build_times = {}
        for build, sstubs in self._builds.items():
            mean_time = self._get_mean_time(sstubs)
            build_times[build] = mean_time
        return build_times

    def sstub_count(self):
        return len(self._sstubs)

    def project_count(self):
        return len(self._get_projects(self._sstubs))

    def build_sstub_count(self):
        build_sstubs = {}
        for build, sstubs in self._builds.items():
            build_sstubs[build] = len(sstubs)
        return build_sstubs

    def build_project_count(self):
        build_projects = {}
        for build, sstubs in self._builds.items():
            projects = self._get_projects(sstubs)
            build_projects[build] = len(projects)
        return build_projects

    def _get_mean_time(self, sstubs):
        time_differences = []
        for sstub in sstubs:
            difference = self._get_time_difference(sstub)
            time_differences.append(difference)
        mean_time = int(mean(time_differences))
        return str(timedelta(seconds=mean_time))

    @staticmethod
    def _initialise_builds(sstubs):
        builds = {}
        for sstub in sstubs:
            build = sstub.build_system
            if build in builds:
                builds[build].append(sstub)
            else:
                builds[build] = [sstub]
        return builds

    @staticmethod
    def _get_time_difference(sstub):
        bug_date = datetime.strptime(sstub.bug_date, '%Y-%m-%d %H:%M:%S')
        fix_date = datetime.strptime(sstub.fix_date, '%Y-%m-%d %H:%M:%S')
        return (fix_date - bug_date).total_seconds()

    @staticmethod
    def _get_projects(sstubs):
        projects = set()
        for sstub in sstubs:
            projects.add(sstub.project_name)
        return projects
