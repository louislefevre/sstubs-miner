import datetime
import time

from github import Github


class GithubManager:
    def __init__(self, tokens):
        self._github_instances = self._initialise_instances(tokens)
        self._github = self._github_instances[0]
        self._limit = self._github.get_rate_limit().core.limit
        self._current_project = None
        self._current_repo = None
        self._current_sha = None
        self._current_commit = None

    def get_repo(self, name):
        if name != self._current_project:
            self._current_project = name
            self._current_repo = self._github.get_repo(name)
        return self._current_repo

    def get_contents(self, name, path, ref=None):
        if ref is None:
            return self.get_repo(name).get_contents(path)
        return self.get_repo(name).get_contents(path, ref)

    def get_contents_loc(self, name, path, ref=None):
        return len(self.get_contents(name, path, ref).decoded_content.splitlines())

    def get_commit(self, name, sha):
        if sha != self._current_sha:
            self._current_sha = sha
            self._current_commit = self.get_repo(name).get_commit(sha=sha)
        return self._current_commit

    def get_commit_patch(self, name, sha, file_name):
        commit = self.get_commit(name, sha)
        for file in commit.files:
            if file.filename == file_name and file.patch is not None:
                return file.patch

    def get_commit_date(self, name, sha):
        return self.get_commit(name, sha).commit.committer.date

    def get_commit_history(self, name, path, date):
        return self.get_repo(name).get_commits(path=path, until=date)

    def exceeded_request_limit(self, offset=0):
        remaining = self._github.get_rate_limit().core.remaining
        return remaining <= (self._limit * offset)

    def sleep(self, offset=0):
        reset_time = self._github.get_rate_limit().core.reset
        current_time = datetime.datetime.today()
        wake_time = reset_time + datetime.timedelta(minutes=offset)
        sleep_time = (wake_time - current_time).total_seconds()
        print('\nRequests limit exceeded - will resume at {}'.format(wake_time.strftime('%H:%M:%S')))
        time.sleep(sleep_time)

    def request_status(self):
        remaining = self._github.get_rate_limit().core.remaining
        return '{}/{}'.format(remaining, self._limit)

    def switch_connection(self, request_offset=0, sleep_offset=0):
        highest_remaining = self._get_highest_remaining()
        if highest_remaining.get_rate_limit().core.remaining > (
                highest_remaining.get_rate_limit().core.limit * request_offset):
            self._github = highest_remaining
        else:
            self._github = self._get_lowest_reset()
            self.sleep(offset=sleep_offset)
        self._limit = self._github.get_rate_limit().core.limit

    def _get_highest_remaining(self):
        remaining = {}
        for github in self._github_instances:
            remaining[github] = github.get_rate_limit().core.remaining
        github = max(remaining, key=remaining.get)
        return github

    def _get_lowest_reset(self):
        resets = {}
        for github in self._github_instances:
            resets[github] = github.get_rate_limit().core.reset
        github = min(resets, key=resets.get)
        return github

    @staticmethod
    def _initialise_instances(tokens):
        instances = []
        for token in tokens:
            instances.append(Github(token, timeout=60))
        return instances
