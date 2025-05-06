
import os
from pathlib import Path
from app.core.config import configs


def collect_py_files(base_dir="."):
    py_files = []
    for root, _, files in os.walk(base_dir):
        if any(skip_dir in root for skip_dir in ["venv", "__pycache__", ".git", "scripts"]):
            continue
        
        for file in files:
            if file.endswith(".py"):
                full_path = Path(root) / file
                py_files.append(full_path)
    return py_files

def print_file_contents(file_paths):
    for path in file_paths:
        relative_path = path.relative_to(Path.cwd())
        print(f"\n{relative_path}\n")
        
        with open(path, "r", encoding="utf-8") as f:
            print(f.read())


if __name__ == "__main__":
    project_root = configs.PROJECT_ROOT
    py_files = collect_py_files(project_root)
    print_file_contents(py_files)