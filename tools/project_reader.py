import os
import zipfile
import tempfile


IGNORE_DIRS = {
    "venv",
    ".venv",
    "__pycache__",
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    ".idea",
    ".vscode"
}

IGNORE_FILES = {
    ".env",
    ".env.local",
    ".env.production",
    ".DS_Store"
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".md",
    ".txt",
    ".json",
    ".toml",
    ".yml",
    ".yaml"
}


def unzip_project(uploaded_file) -> str:
    temp_dir = tempfile.mkdtemp(prefix="uploaded_project_")
    zip_path = os.path.join(temp_dir, uploaded_file.name)

    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extract_dir = os.path.join(temp_dir, "project")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    return extract_dir


def should_read_file(file_name: str) -> bool:
    if file_name in IGNORE_FILES:
        return False

    _, ext = os.path.splitext(file_name)

    return ext in ALLOWED_EXTENSIONS


def build_file_tree(project_dir: str) -> str:
    tree_lines = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = os.path.relpath(root, project_dir).count(os.sep)
        indent = "│   " * level

        if root == project_dir:
            tree_lines.append("project/")
        else:
            folder_name = os.path.basename(root)
            tree_lines.append(f"{indent}├── {folder_name}/")

        file_indent = "│   " * (level + 1)

        for file in files:
            if should_read_file(file):
                tree_lines.append(f"{file_indent}├── {file}")

    return "\n".join(tree_lines)


def read_project_files_from_zip(uploaded_file) -> tuple[str, list[dict]]:
    project_dir = unzip_project(uploaded_file)
    file_tree = build_file_tree(project_dir)

    project_files = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if not should_read_file(file):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_dir)

            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:
                    content = f.read()
            except Exception:
                continue

            project_files.append(
                {
                    "path": relative_path,
                    "content": content
                }
            )

    return file_tree, project_files