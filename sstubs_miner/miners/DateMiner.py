from sstubs_miner.util.JsonManager import JsonWriter


class DateMiner:
    def __init__(self, github, sstubs, sstubs_file):
        self._github = github
        self._sstubs = sstubs
        self._sstubs_file = sstubs_file

    def mine(self):
        self._mine_dates()

    def _mine_dates(self):
        index, missing = -1, 0

        for sstub in self._sstubs:
            index += 1
            self._update_status(index, missing)

            fix_date = self._github.get_commit_date(sstub.project_name, sstub.fix_sha)
            commits = self._github.get_commit_history(sstub.project_name, sstub.path, fix_date)

            for commit in commits:
                if commit.sha == sstub.fix_sha:
                    continue

                for file in commit.files:
                    if file.filename == sstub.path and file.patch is not None:
                        source_bug = sstub.bug_source.replace(' ', '')
                        patch = self._clean_patch(file.patch)

                        if source_bug in patch:
                            sstub.bug_sha = commit.sha
                            sstub.fix_date = fix_date
                            sstub.bug_date = commit.commit.committer.date
                            self._write(index, sstub)
                            break
                else:
                    continue
                break
            else:
                missing += 1

    def _update_status(self, counter, missing):
        counter += 1
        total_sstubs = len(self._sstubs)
        print('{}/{} SStuBs mined - {} missing ({} requests remaining)'
              .format(counter, total_sstubs, missing, self._github.request_status()), end='\r')
        if counter == total_sstubs:
            print()
        if self._github.exceeded_request_limit(0.01):
            self._github.sleep(offset=1)

    def _write(self, index, sstub):
        writer = JsonWriter(self._sstubs_file)
        writer.update(index, '_bug_sha', sstub.bug_sha)
        writer.update(index, '_fix_time', str(sstub.fix_date))
        writer.update(index, '_bug_time', str(sstub.bug_date))

    @staticmethod
    def _clean_patch(patch):
        clean_patch = ''
        for line in patch.splitlines():
            line = line[1:]
            clean_patch += line.replace(' ', '')
        return clean_patch
