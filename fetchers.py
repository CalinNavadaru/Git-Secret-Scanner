import tempfile

from git import Repo


class BaseCommitFetcher:

    def __init__(self, repo: Repo):
        self.repo = repo

    def fetch(self, limit=10):
        commits = []
        for commit in self.repo.iter_commits(max_count=limit):
            parent = commit.parents[0] if commit.parents else None
            diff_index = commit.diff(parent, create_patch=True)

            file_diffs = []
            for d in diff_index:
                patch_text = d.diff.decode(errors="ignore")

                file_diffs.append({
                    "a_path": d.a_path,
                    "b_path": d.b_path,
                    "change_type": d.change_type,
                    "patch": patch_text.splitlines(),
                })

            commit_data = {
                "hash": commit.hexsha,
                "author": commit.author.name,
                "email": commit.author.email,
                "date": str(commit.committed_datetime),
                "message": commit.message.strip(),
                "files": file_diffs,
            }
            commits.append(commit_data)

        return commits


class CommitGitPathFetcher(BaseCommitFetcher):

    def __init__(self, repo_path: str):
        super().__init__(Repo(repo_path))


class CommitGitUrlFetcher(BaseCommitFetcher):

    def __init__(self, repo_url: str):
        tmpdir = tempfile.mkdtemp()
        super().__init__(Repo.clone_from(repo_url, tmpdir))
