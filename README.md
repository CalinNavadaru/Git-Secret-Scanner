# Git Secret Scanner AI

Scan your Git repositories for potential secrets or credentials automatically using AI-powered detection (Hugging Face `gpt-oss 20b`).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Arguments](#arguments)
6. [Examples](#examples)
7. [Generating Your Own Prompt](#generating-your-own-prompt)
8. [License](#license)

---

## Prerequisites

* Python 3.10 or higher
* Git
* Hugging Face API token

---

## Installation

```bash
git clone https://github.com/CalinNavadaru/git-secret-scanner-ai.git
cd git-secret-scanner-ai
pip install -r requirements.txt
```

---

## Configuration

Set up your environment variables:

```bash
export HF_ACCESS_TOKEN=your_token_here
export PROMPT_PASSWORD=<generated-password>
```

Or create a `.env` file at the project root:

```env
HF_ACCESS_TOKEN=your_token_here
PROMPT_PASSWORD=<generated-password>
```

**Note:** The application uses an encrypted prompt (`prompt.enc` + `prompt.salt`). You must provide a password in `PROMPT_PASSWORD` to decrypt it.

---

## Usage

```bash
python -m git_scanner --repo <repo_path_or_url> [options]
```

---

## Arguments

| Argument       | Type | Default  | Description                                  |
| -------------- | ---- | -------- | -------------------------------------------- |
| `--repo`       | str  | `.`      | Path to a local Git repository or remote URL |
| `--n`          | int  | 5        | Number of most recent commits to analyze     |
| `--out`        | str  | `report` | Name of the generated JSON report            |
| `--batch_size` | int  | 5        | Batch size when analyzing commits            |

---

## Examples

```bash
# Analyze a local repository
python -m git_scanner --repo ./demo_repo --n 10 --out local_report.json

# Analyze a remote repository
python -m git_scanner --repo https://github.com/user/project.git --n 20 --batch_size 10 --out remote_report.json
```

The results will be saved as a JSON file (`local_report.json` or `remote_report.json`).

---

## Generating Your Own Prompt

1. Edit `gen_encrypt_with_password.py` with your desired prompt text.
2. Run the script and enter a strong password when prompted:

```bash
python gen_encrypt_with_password.py
```

3. Use the generated `prompt.enc` and `prompt.salt` files with your `PROMPT_PASSWORD` for scanning.

---

## License

This project is licensed under the MIT License.

## Additional Info

This project is intended as a learning experience, showcasing my skills in Python, AI integration, 
and my general knowledge of cybersecurity.

Under no circumstances should this project be used in a production environment without a code review and additional
security measures.