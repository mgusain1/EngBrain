import base64
from pathlib import Path
from urllib.parse import urlparse
import os
import requests


ALLOWED = {
    ".py", ".js", ".ts", ".java", ".go",
    ".md", ".txt", ".yml", ".yaml",
    ".json", ".toml", ".rst"
}

IGNORED_PARTS = {
    ".git", "venv", ".venv", "__pycache__",
    "node_modules", "dist", "build",
    ".idea", ".vscode", ".pytest_cache"
}

def should_skip_dir(dir_path: str) -> bool:
    path = Path(dir_path)

    for part in path.parts:
        if part in IGNORED_PARTS:
            return True

    return False

def github_headers():
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = "Bearer " + token

    return headers

def is_github_url(repo_input: str) -> bool:
    return (
        repo_input.startswith("https://github.com/")
        or repo_input.startswith("http://github.com/")
    )


def parse_github_url(repo_url: str):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")

    owner = parts[0]
    repo = parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


def should_skip_file(file_path: str) -> bool:
    path = Path(file_path)
    if path.name.lower() in {"license", "license.txt", "copying", "notice"}:
        return True

    for part in path.parts:
        if part in IGNORED_PARTS:
            return True

    if path.name.startswith(".env"):
        return True

    if path.suffix not in ALLOWED:
        return True

    return False


def get_default_branch(owner: str, repo: str) -> str:
    url = "https://api.github.com/repos/" + owner + "/" + repo

    response = requests.get(
            url,
            headers=github_headers(),
            timeout=20
        )

    if response.status_code == 404:
        raise RuntimeError("Repo not found or private. Connect GitHub to continue.")

    if response.status_code != 200:
        raise RuntimeError("GitHub API error: " + response.text)

    data = response.json()
    return data.get("default_branch", "main")


def list_directory(owner: str, repo: str, path: str, branch: str):
    if path:
        url = (
            "https://api.github.com/repos/"
            + owner
            + "/"
            + repo
            + "/contents/"
            + path
            + "?ref="
            + branch
        )
    else:
        url = (
            "https://api.github.com/repos/"
            + owner
            + "/"
            + repo
            + "/contents"
            + "?ref="
            + branch
        )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=20
    )

    if response.status_code == 404:
        raise RuntimeError("GitHub directory not found: " + path)

    if response.status_code == 403 or response.status_code == 429:
        raise RuntimeError("GitHub API rate limit hit while listing repository files.")

    if response.status_code != 200:
        raise RuntimeError("GitHub contents API error: " + response.text)

    data = response.json()

    if not isinstance(data, list):
        return []

    return data


def get_repo_tree(owner: str, repo: str, branch: str):
    url = (
        "https://api.github.com/repos/"
        + owner
        + "/"
        + repo
        + "/git/trees/"
        + branch
        + "?recursive=1"
    )

    response = requests.get(
            url,
            headers=github_headers(),
            timeout=20
        )

    if response.status_code == 404:
        raise RuntimeError("Repo tree not found or repo is private.")

    if response.status_code != 200:
        raise RuntimeError("GitHub tree API error: " + response.text)

    data = response.json()
    return data.get("tree", [])


def fetch_file_content(owner: str, repo: str, file_path: str, branch: str) -> str:
    url = (
        "https://api.github.com/repos/"
        + owner
        + "/"
        + repo
        + "/contents/"
        + file_path
        + "?ref="
        + branch
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=20
    )

    if response.status_code != 200:
        return ""

    data = response.json()

    if data.get("encoding") != "base64":
        return ""

    raw_content = data.get("content", "")

    try:
        decoded = base64.b64decode(raw_content).decode("utf-8", errors="ignore")
        return decoded
    except Exception:
        return ""
    
def walk_github_repo(owner: str, repo: str, branch: str):
    files = []
    stack = [""]

    while stack:
        current_path = stack.pop()

        items = list_directory(
            owner=owner,
            repo=repo,
            path=current_path,
            branch=branch
        )

        for item in items:
            item_type = item.get("type")
            item_path = item.get("path", "")

            if item_type == "dir":
                if should_skip_dir(item_path):
                    continue

                stack.append(item_path)

            elif item_type == "file":
                if should_skip_file(item_path):
                    continue

                content = fetch_file_content(
                    owner=owner,
                    repo=repo,
                    file_path=item_path,
                    branch=branch
                )

                if not content.strip():
                    continue

                files.append({
                    "file_path": item_path,
                    "file_type": Path(item_path).suffix,
                    "content": content
                })

    return files


def read_github_repo(repo_url: str):
    owner, repo = parse_github_url(repo_url)
    branch = get_default_branch(owner, repo)

    files = walk_github_repo(
        owner=owner,
        repo=repo,
        branch=branch
    )

    if not files:
        raise RuntimeError("No supported files were found in this GitHub repository.")

    return files

