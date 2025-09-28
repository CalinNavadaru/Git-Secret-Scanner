import json
from utils import shannon_entropy
from fetchers import CommitGitPathFetcher, CommitGitUrlFetcher
from model import IntelligentCommitAnalyzer



class CommitAnalyzerPipeline:

    def __init__(self, repo_details: dict, api_key: str, prompt: str, output_filename: str):
        if repo_details["type"] == "path":
            self.fetcher = CommitGitPathFetcher(repo_details["value"])
        else:
            self.fetcher = CommitGitUrlFetcher(repo_details["value"])
        self.analyzer = IntelligentCommitAnalyzer(api_key, prompt)
        self.output = output_filename

    @staticmethod
    def __reduce_fp(latest_results: list):
        actual_issues = []
        for result in latest_results:
            if result['finding_type'] == 1 or shannon_entropy(result['snippet']) > 3.5:
                actual_issues.append(result)

        return actual_issues

    def analyze(self, limit: int, batch_size=5):
        commits = self.fetcher.fetch(limit)

        result = []

        for i in range(0, len(commits), batch_size):
            latest_results = json.loads(self.analyzer.generate_report(json.dumps(commits[i: i + batch_size])))
            latest_results: list
            result.extend(CommitAnalyzerPipeline.__reduce_fp(latest_results))

        with open(f"{self.output}.json", "w") as f:
            f.write(json.dumps(result))
