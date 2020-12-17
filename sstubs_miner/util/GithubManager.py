import datetime
import time

from github import Github


class GithubMiner:
    def __init__(self, token):
        self._github = Github(token)
        self._current_project = None
        self._current_repo = None
        self._current_sha = None
        self._current_commit = None

    def get_repo(self, name):
        if name != self._current_project:
            self._current_project = name
            self._current_repo = self._github.get_repo(name)
        return self._current_repo

    def get_commit(self, name, sha):
        if sha != self._current_sha:
            self._current_sha = sha
            self._current_commit = self.get_repo(name).get_commit(sha=sha)
        return self._current_commit

    def get_commit_date(self, name, sha):
        return self.get_commit(name, sha).commit.committer.date

    def get_commit_history(self, name, path, date):
        return self.get_repo(name).get_commits(path=path, until=date)

    def exceeded_request_limit(self, offset=0):
        return self.request_remaining < (self.request_limit * offset)

    def sleep(self, offset=0):
        current_time = datetime.datetime.today()
        wake_time = self.request_reset + datetime.timedelta(minutes=offset)
        sleep_time = (wake_time - current_time).total_seconds()
        print('\nRequests limit exceeded - will resume at {}'.format(wake_time.strftime('%H:%M:%S')))
        time.sleep(sleep_time)

    def request_status(self):
        return '{}/{}'.format(self.request_remaining, self.request_limit)

    @property
    def github(self):
        return self._github

    @property
    def request_limit(self):
        return self._github.get_rate_limit().core.limit

    @property
    def request_remaining(self):
        return self._github.get_rate_limit().core.remaining

    @property
    def request_reset(self):
        return self._github.get_rate_limit().core.reset
