class BugMiner:
    def __init__(self, github):
        self._github = github

    def mine(self, sstub):
        fix_date = self._github.get_commit_date(sstub.project_name, sstub.fix_sha)
        fix_patch = self._github.get_commit_patch(sstub.project_name, sstub.fix_sha, sstub.path)
        commits = self._github.get_commit_history(sstub.project_name, sstub.path, fix_date)

        for commit in commits:
            if commit.sha == sstub.fix_sha:
                continue

            for file in commit.files:
                if file.filename == sstub.path and file.patch is not None and file.patch != fix_patch:
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

    @staticmethod
    def _clean_patch(patch):
        clean_patch = ''
        for line in patch.splitlines():
            if line.startswith('+'):
                line = line[1:]
                clean_patch += line.replace(' ', '')
        return clean_patch
