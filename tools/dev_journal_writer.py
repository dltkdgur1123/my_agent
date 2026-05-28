import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_final_portfolio(file_tree: str, file_portfolios: list[str]) -> str:
    joined_file_portfolios = "\n\n---\n\n".join(file_portfolios)

    prompt = f"""
너는 Notion 포트폴리오용 개발 문서를 작성하는 에이전트다.

아래 프로젝트 파일 구조와 파일별 포트폴리오 내용을 바탕으로,
최종 프로젝트 포트폴리오 문서를 작성해라.

중요 규칙:
- 파일별 포트폴리오 내용을 최대한 유지해라.
- 프로젝트 파일 구조에는 파일/폴더마다 괄호로 역할 설명을 붙여라.
- 프로젝트 전체 개요를 먼저 작성해라.
- 그 다음 파일별 구현 기록을 정리해라.
- 코드 흐름, 구현 이유, 설계 포인트가 드러나게 작성해라.
- Notion에 붙여넣기 좋은 Markdown 형식으로 작성해라.
- 오늘/어제/내일 같은 날짜 표현은 쓰지 마라.

[프로젝트 파일 구조]
{file_tree}

[파일별 포트폴리오 내용]
{joined_file_portfolios}

[출력 형식]

# 프로젝트 포트폴리오 작업일지

## 1. 프로젝트 개요

## 2. 프로젝트 파일 구조와 역할

project/
├── 파일명 (역할 설명)

## 3. 파일별 구현 기록

### 3-1. 파일명

#### 파일 역할

#### 코드 흐름

#### 주요 구현 파트

#### 구현 이유

#### 개선 가능 포인트

## 4. 사용 기술 스택

## 5. 문제 해결 및 설계 포인트

## 6. 포트폴리오용 요약
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "너는 개발 프로젝트를 Notion 포트폴리오 문서로 정리하는 도우미다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content


def save_dev_journal(journal: str) -> str:
    os.makedirs("reports", exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/dev_journal_{now}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(journal)

    return file_path