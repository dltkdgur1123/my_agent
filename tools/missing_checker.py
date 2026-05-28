import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def check_missing_parts(client_request: str, analysis: str) -> str:
    prompt = f"""
너는 외주 개발 납품 전 누락 검사를 담당하는 QA 에이전트다.

아래 요청과 분석 결과를 보고, 빠졌을 가능성이 있는 항목을 검사해라.

[클라이언트 요청]
{client_request}

[분석 결과]
{analysis}

[출력 형식]

### 1. 기능 누락 가능성
- 

### 2. 예외처리 누락 가능성
- 

### 3. 클라이언트 확인 필요사항
- 

### 4. 납품 시 필요한 문서
- 

### 5. 견적 범위가 커질 수 있는 부분
- 

### 6. 위험 요소
-
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 프리랜서 개발 납품 전 QA 체크 도우미다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content