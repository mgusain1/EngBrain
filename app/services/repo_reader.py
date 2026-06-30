from pathlib import Path

ALLOWED = {".py",".js",".ts",".java",".md",".txt",".yml",".yaml",".json",".toml",".rst"}
IGNORED = {".git","venv",".venv","__pycache__","node_modules","dist","build",".idea",".vscode",".pytest_cache"}


def should_skip(path_to):
    path_now = Path(path_to)
    for p in path_now.parts:
        if p in IGNORED:
            return True
    if path_now.name.startswith(".env"):
        return True
    if path_now.suffix not in ALLOWED:
        return True    
    return False

def read_repo_files(repo_path:str):
    if repo_path is None:
        raise TypeError("Path cannot be found")
    
    repo = Path(repo_path)
    if not repo.exists():
        raise FileNotFoundError(f"Path does not exist: {repo_path}")
    if not repo.is_dir():
        raise ValueError(f"Path is not a folder: {repo_path}")
    files = []
    for r in repo.rglob("*"):
        if r.is_dir():
            continue
        if should_skip(r):
            continue
        try:
            content = r.read_text(encoding="utf-8")
            if not content.strip():
                continue
            relative_path = r.relative_to(repo)
            files.append({
                "file_path": str(relative_path),
                "file_type": r.suffix,
                "content": content
            })
        except (UnicodeDecodeError, PermissionError):
            continue
    return files