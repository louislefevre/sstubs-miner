from sstubs_miner.util.CSVManager import CSVWriter
from sstubs_miner.util.SStub import SStub


class BugMiner:
    def __init__(self, github, sstubs, results_file):
        self._github = github
        self._sstubs = sstubs
        self._results_file = results_file
        self._counter = 0
        self._missing = 0

    def mine(self):
        self._mine_bugs()

    def _mine_bugs(self):
        writer = CSVWriter(self._results_file, SStub.attribute_names())

        for sstub in self._sstubs:
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
                            sstub.loc = self._github.get_contents_loc(sstub.project_name, sstub.path, ref=commit.sha)
                            break
                else:
                    continue
                break
            else:
                self._missing += 1

            writer.write(sstub.attribute_list())
            self._update_status()

    def _update_status(self):
        self._counter += 1
        total_sstubs = len(self._sstubs)
        print('{}/{} SStuBs mined - {} missing ({} requests remaining)'
              .format(self._counter, total_sstubs, self._missing, self._github.request_status()), end='\r')
        if self._counter == total_sstubs:
            print()
        if self._github.exceeded_request_limit(0.01):
            self._github.sleep(offset=1)

    @staticmethod
    def _clean_patch(patch):
        clean_patch = ''
        for line in patch.splitlines():
            if line.startswith('+') or line.startswith('-'):
                line = line[1:]
                clean_patch += line.replace(' ', '')
        return clean_patch