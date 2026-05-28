import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def make_code_search_keywords(client_request: str, analysis: str) -> str:
    prompt = f"""
아래 클라이언트 요청과 분석 결과를 보고,
개발자가 필요한 코드를 검색할 수 있도록 검색 키워드를 만들어라.

[클라이언트 요청]
{client_request}

[분석 결과]
{analysis}

[출력 형식]

## 1. 한국어 검색 키워드
- 

## 2. 영어 검색 키워드
- 

## 3. 공식문서에서 찾을 키워드
- 

## 4. 내 코드 템플릿 폴더에서 찾을 키워드
- 

## 5. 추천 코드 템플릿 이름
- 예: selenium_login_template.py
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 개발 코드 검색 키워드 생성 도우미다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content