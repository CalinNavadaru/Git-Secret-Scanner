import json

from fetchers import CommitGitPathFetcher, CommitGitUrlFetcher
from model import CommitAnalyzer


class CommitAnalyzerPost:

    def __init__(self, result: list[dict]):
        self.__result = result


class CommitAnalyzerPipeline:

    def __init__(self, repo_details: dict, api_key: str, prompt: str, output_filename: str):
        if repo_details["type"] == "path":
            self.fetcher = CommitGitPathFetcher(repo_details["value"])
        else:
            self.fetcher = CommitGitUrlFetcher(repo_details["value"])
        self.analyzer = CommitAnalyzer(api_key, prompt)
        self.output = output_filename

    def analyze(self, limit: int, batch_size=5):
        commits = self.fetcher.fetch(limit)

        result = []

        for i in range(0, len(commits), batch_size):
            result.extend(json.loads(self.analyzer.generate_report(json.dumps(commits[i: i + batch_size]))))

        with open(f"{self.output}.json", "w") as f:
            f.write(json.dumps(result))
