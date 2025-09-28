import argparse
import os
import re
import sys

from dotenv import load_dotenv

from loader import get_prompt
from pipeline import CommitAnalyzerPipeline


def check_repo_url(repo: str) -> bool:
    pattern = r"https?://\S+\.git|www\.\S+\.git"
    return re.fullmatch(pattern, repo) is not None


def get_repo_path(repo: str) -> str:
    path_repo = os.path.realpath(os.path.expanduser(repo), strict=True)
    if not os.path.isdir(path_repo):
        raise ValueError("The provided path must pe a folder!")
    if not os.path.exists(os.path.join(path_repo, ".git")):
        raise ValueError("The provided path doesn't contain a Git repository!")
    return path_repo


def main():
    load_dotenv()
    try:
        prompt = get_prompt()
    except RuntimeError as re_error:
        print(re_error, file=sys.stderr)
        exit(-1)

    parser = argparse.ArgumentParser(description="CLI for Git commit analysis with gpt-oss")

    parser.add_argument("--repo", type=str, default=".", required=False, help="The path/URL of the repository")
    parser.add_argument("--n", type=int, default=5, required=False,
                        help="The number of commit from the most recent one (Default: 5)")
    parser.add_argument("--out", type=str, default="report",
                        help="The name of the generated JSON report (Default: report.json)")

    parser.add_argument("--batch_size", type=int, default=5, required=False,
                        help="The batch size when analyzing commits. (Default: 5)")

    args = parser.parse_args()

    limit = args.n
    output_filename = args.out
    batch_size = args.batch_size
    print("Checking if the provided repository is a valid URL")
    if check_repo_url(args.repo):
        print("Repository URL is validated.")
        analyzer_pipeline = CommitAnalyzerPipeline({"value": args.repo, "type": "url"}, os.getenv("HF_ACCESS_TOKEN"),
                                                   prompt, output_filename)
        print("Analyzing commits ...")
        analyzer_pipeline.analyze(limit, batch_size)
        print("Report generated!")
    else:
        print("The provided argument is not an URL.\nTrying to see if it is a valid local path.")
        try:
            path_repo = get_repo_path(args.repo)
            print("The provided repository path is valid.")
            analyzer_pipeline = CommitAnalyzerPipeline({"value": path_repo, "type": "path"},
                                                       os.getenv("HF_ACCESS_TOKEN"), prompt, output_filename)
            print("Analyzing commits ...")
            analyzer_pipeline.analyze(limit, batch_size)
            print("Report generated!")
        except FileNotFoundError:
            print("The provided path is invalid!", file=sys.stderr)
        except OSError:
            print("The provided path is inaccessible", file=sys.stderr)
        except ValueError as ve:
            print(ve, file=sys.stderr)


if __name__ == "__main__":
    main()
