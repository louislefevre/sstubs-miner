def mine(github, sstubs):
    for sstub in sstubs:
        repo = github.get_repo(sstub.project_name)
        fix_commit = repo.get_commit(sha=sstub.fix_sha)
        fix_commit_date = fix_commit.commit.committer.date
        commits = repo.get_commits(path=sstub.path, until=fix_commit_date)
        source_bug = sstub.bug_source
        file_name = sstub.path

        for commit in commits:
            if commit.commit.committer.date == fix_commit_date:
                continue

            for file in commit.files:
                if file.filename == file_name:
                    if source_bug in file.patch:
                        sstub.bug_sha = commit.sha
                        sstub.fix_time = fix_commit_date
                        sstub.bug_time = commit.commit.committer.date
                        break
            else:
                continue
            break
