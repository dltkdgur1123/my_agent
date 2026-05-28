import subprocess
import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def run_git_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    if result.returncode != 0:
        return result.stderr.strip()

    return result.stdout.strip()


def get_git_status() -> str:
    return run_git_command(
        ["git", "status", "--short"]
    )


def get_git_diff_summary() -> str:
    return run_git_command(
        ["git", "diff", "--stat"]
    )


def get_git_remote() -> str:
    return run_git_command(
        ["git", "remote", "-v"]
    )


def get_current_branch() -> str:
    return run_git_command(
        ["git", "branch", "--show-current"]
    )


def generate_commit_message(portfolio_text: str) -> str:
    prompt = f"""
너는 Git 커밋 메시지를 작성하는 개발 도우미다.

아래 포트폴리오 내용을 바탕으로
짧고 명확한 Git 커밋 메시지를 작성해라.

중요 규칙:
- 영어로 작성
- 한 줄 작성
- conventional commit 형식 사용
- 너무 길게 작성하지 말 것

예시:
feat: add streamlit portfolio workflow
fix: improve project zip analysis
refactor: separate portfolio generation modules

[포트폴리오 내용]
{portfolio_text[:4000]}

[출력]
커밋 메시지만 출력
"""

    response = client.chat.completions.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini"
        ),
        messages=[
            {
                "role": "system",
                "content": (
                    "너는 실무형 Git 커밋 메시지 작성 도우미다."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def commit_changes(commit_message: str) -> str:
    add_result = run_git_command(
        ["git", "add", "."]
    )

    commit_result = run_git_command(
        ["git", "commit", "-m", commit_message]
    )

    return f"""
[git add 결과]
{add_result}

[git commit 결과]
{commit_result}
"""


def push_to_github() -> str:
    remote = get_git_remote()
    branch = get_current_branch()

    if not remote:
        return """
GitHub 원격 저장소가 연결되어 있지 않습니다.

먼저 아래 명령으로 원격 저장소를 연결해야 합니다.

git remote add origin https://github.com/사용자명/저장소명.git
"""

    if not branch:
        return """
현재 Git 브랜치를 확인할 수 없습니다.

먼저 Git 저장소가 초기화되어 있는지 확인해주세요.

git init
"""

    push_result = run_git_command(
        ["git", "push", "origin", branch]
    )

    return f"""
[현재 브랜치]
{branch}

[원격 저장소]
{remote}

[git push 결과]
{push_result}
"""