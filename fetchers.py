import tempfile

from git import Repo


class BaseCommitFetcher:

    def __init__(self, repo: Repo):
        self.repo = repo

    def fetch(self, limit=10):
        commits = []
        for commit in list(self.repo.iter_commits(max_count=limit)):
            diff_text = "\n".join(d.diff.decode(errors="ignore") for d in commit.diff(create_patch=True))
            commit_data = {"hash": commit.hexsha, "author": commit.author.name, "email": commit.author.email,
                "date": str(commit.committed_datetime), "message": commit.message.strip(), "diff": diff_text, }
            commits.append(commit_data)
        return commits


class CommitGitPathFetcher(BaseCommitFetcher):

    def __init__(self, repo_path: str):
        super().__init__(Repo(repo_path))


class CommitGitUrlFetcher(BaseCommitFetcher):

    def __init__(self, repo_url: str):
        tmpdir = tempfile.mkdtemp()
        super().__init__(Repo.clone_from(repo_url, tmpdir))
