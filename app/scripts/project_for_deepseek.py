
import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from app.config import configs


def collect_py_files(base_dir="."):
    py_files = []
    for root, _, files in os.walk(base_dir):
        if any(skip_dir in root for skip_dir in ["venv", "__pycache__", ".git", "scripts"]):
            continue
        
        for file in files:
            if file.endswith(".py") or file.endswith(".pyw") or file.endswith(".qss") or file.endswith(".bat") or file.endswith(".md"):
                full_path = Path(root) / file
                py_files.append(full_path)
    return py_files

def file_contents(file_paths):
    texts = []

    for path in file_paths:
        relative_path = path.relative_to(Path.cwd())
        texts.append(f"\n{relative_path}\n")
        
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())

    return '\n'.join(texts)


if __name__ == "__main__":
    project_root = configs.PROJECT_ROOT
    py_files = collect_py_files(project_root)
    text = file_contents(py_files)

    print(text)
    app = QApplication(sys.argv)
    clipboard = QGuiApplication.clipboard()
    clipboard.setText(text)