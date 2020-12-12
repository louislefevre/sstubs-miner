from JsonManager import JsonWriter


class DateMiner:
    def __init__(self, github, sstubs, sstubs_file):
        self._github = github
        self._sstubs = sstubs
        self._sstubs_file = sstubs_file
        self._counter = 0

    def mine(self):
        self._mine_dates()

    def _mine_dates(self):
        writer = JsonWriter(self._sstubs_file)

        for i in range(len(self._sstubs)):
            self._update_status()

            sstub = self._sstubs[i]
            repo = self._github.get_repo(sstub.project_name)
            fix_commit = repo.get_commit(sha=sstub.fix_sha)
            fix_commit_date = fix_commit.commit.committer.date
            commits = repo.get_commits(path=sstub.path, until=fix_commit_date)

            source_bug = sstub.bug_source
            file_name = sstub.path

            for commit in commits:
                if commit.sha == sstub.fix_sha:
                    continue

                for file in commit.files:
                    if file.filename == file_name:
                        if file.patch is not None:
                            if source_bug in file.patch:
                                sstub.bug_sha = commit.sha
                                sstub.fix_time = fix_commit_date
                                sstub.bug_time = commit.commit.committer.date
                                writer.update(i, '_bug_sha', sstub.bug_sha)
                                writer.update(i, '_fix_time', str(sstub.fix_time))
                                writer.update(i, '_bug_time', str(sstub.bug_time))
                                break
                else:
                    continue
                break

    def _update_status(self):
        self._counter += 1
        total_sstubs = len(self._sstubs)
        print('({}/{}) SStuBs Mined'.format(self._counter, total_sstubs), end='\r')
        if self._counter == total_sstubs:
            print()

    def _write(self):
        pass
