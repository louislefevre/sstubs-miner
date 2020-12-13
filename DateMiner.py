from JsonManager import JsonWriter


class DateMiner:
    def __init__(self, github, sstubs, sstubs_file):
        self._github = github
        self._sstubs = sstubs
        self._sstubs_file = sstubs_file

    def mine(self):
        self._mine_dates()

    def _mine_dates(self):
        current_project = None
        current_repo = None
        counter = 0
        missing = 0

        for i in range(len(self._sstubs)):
            self._update_status(counter, missing)
            sstub = self._sstubs[i]

            if sstub.project_name != current_project:
                current_project = sstub.project_name
                current_repo = self._github.get_repo(sstub.project_name)
            repo = current_repo

            fix_commit = repo.get_commit(sha=sstub.fix_sha)
            fix_commit_date = fix_commit.commit.committer.date
            commits = repo.get_commits(path=sstub.path, until=fix_commit_date)

            for commit in commits:
                if commit.sha == sstub.fix_sha:
                    continue

                for file in commit.files:
                    if file.filename == sstub.path:
                        if file.patch is not None:
                            source_bug = sstub.bug_source.replace(' ', '')
                            patch = self._clean(file.patch)

                            if source_bug in patch:
                                sstub.bug_sha = commit.sha
                                sstub.fix_time = fix_commit_date
                                sstub.bug_time = commit.commit.committer.date
                                self._write(i, sstub)
                                break
                else:
                    continue
                break
            else:
                missing += 1

    def _update_status(self, counter, missing):
        counter += 1
        total_sstubs = len(self._sstubs)
        print('({}/{}) SStuBs Mined - {} missing'.format(counter, total_sstubs, missing), end='\r')
        if counter == total_sstubs:
            print()

    def _write(self, index, sstub):
        writer = JsonWriter(self._sstubs_file)
        writer.update(index, '_bug_sha', sstub.bug_sha)
        writer.update(index, '_fix_time', str(sstub.fix_time))
        writer.update(index, '_bug_time', str(sstub.bug_time))

    @staticmethod
    def _clean(patch):
        clean_patch = ''
        for line in patch.splitlines():
            line = line[1:]
            clean_patch += line.replace(' ', '')
        return clean_patch
