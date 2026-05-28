import os
import re
import zipfile
from datetime import datetime


def get_comment_style(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".py"]:
        return "#"
    if ext in [".js", ".jsx", ".ts", ".tsx", ".java", ".cs", ".cpp", ".c"]:
        return "//"
    if ext in [".html", ".xml"]:
        return "html"
    if ext in [".md", ".txt"]:
        return "text"

    return "#"


def make_file_content(file_path: str, role: str = "") -> str:
    comment_style = get_comment_style(file_path)
    file_name = os.path.basename(file_path)

    todos = [
        "필요한 라이브러리 또는 모듈 import",
        "이 파일에서 담당할 핵심 기능 함수/클래스 작성",
        "입력값 검증 및 예외처리 작성",
        "다른 파일과 연결되는 부분 작성",
        "테스트 또는 실행 확인 코드 작성"
    ]

    if comment_style == "#":
        lines = [
            f"# ==================================================",
            f"# 파일명: {file_name}",
            f"# 역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            f"# ==================================================",
            "",
        ]

        for i, todo in enumerate(todos, start=1):
            lines.extend([
                f"# TODO {i}. {todo}",
                f"# 설명:",
                f"# - 이 영역에 필요한 코드를 구현하세요.",
                "",
            ])

        return "\n".join(lines)

    if comment_style == "//":
        lines = [
            f"// ==================================================",
            f"// 파일명: {file_name}",
            f"// 역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            f"// ==================================================",
            "",
        ]

        for i, todo in enumerate(todos, start=1):
            lines.extend([
                f"// TODO {i}. {todo}",
                f"// 설명:",
                f"// - 이 영역에 필요한 코드를 구현하세요.",
                "",
            ])

        return "\n".join(lines)

    if comment_style == "html":
        return f"""<!--
==================================================
파일명: {file_name}
역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}
==================================================

TODO 1. 기본 HTML 구조 작성
TODO 2. 필요한 영역별 UI 구성
TODO 3. CSS/JS 연결
TODO 4. 접근성 및 반응형 구조 확인
-->
"""

    return f"""# {file_name}

역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}

## TODO 1. 기본 설명 작성

## TODO 2. 사용 방법 작성

## TODO 3. 구현할 기능 정리

## TODO 4. 주의사항 정리
"""


def extract_paths_from_structure(file_structure: str) -> list[tuple[str, str]]:
    results = []

    for line in file_structure.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if "├" not in clean_line and "└" not in clean_line and "/" not in clean_line:
            continue

        cleaned = re.sub(r"[│├└─]+", "", clean_line).strip()

        if not cleaned:
            continue

        role = ""

        if "(" in cleaned and ")" in cleaned:
            role = cleaned[cleaned.find("(") + 1:cleaned.rfind(")")].strip()
            path = cleaned[:cleaned.find("(")].strip()
        else:
            path = cleaned.strip()

        path = path.replace("\\", "/").strip()

        if path in ["project/", "project", "project_name/", "project_name"]:
            continue

        results.append((path, role))

    return results


def create_project_skeleton(file_structure: str) -> str:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.join("generated_projects", f"project_{now}")

    os.makedirs(base_dir, exist_ok=True)

    paths = extract_paths_from_structure(file_structure)

    for path, role in paths:
        full_path = os.path.join(base_dir, path)

        if path.endswith("/"):
            os.makedirs(full_path, exist_ok=True)
            continue

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        content = make_file_content(path, role)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return base_dir


def zip_project_folder(folder_path: str) -> str:
    zip_path = f"{folder_path}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    return zip_path