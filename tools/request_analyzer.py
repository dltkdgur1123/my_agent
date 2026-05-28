import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_request(client_request: str) -> str:
    prompt = f"""
너는 프리랜서 개발자를 돕는 요구사항 분석 에이전트다.

아래 클라이언트 요청을 분석해서 다음 형식으로 정리해줘.

각 To Do 항목 끝에는 반드시 괄호로 추천 파일명을 적어줘.

파일명은 클라이언트 요청에 가장 적합한 개발 언어 및 프레임워크 기준으로 작성해라.


[클라이언트 요청]
{client_request}

[출력 형식]

### 1. 요청 요약
- 

### 2. 개발 To Do 리스트
- 

### 3. 필요한 기술
- 

### 4. 클라이언트에게 확인해야 할 질문
- 

### 5. 기본 기능
- 

### 6. 추가 비용 가능 기능
- 


### 7. 주의사항
-
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 실무형 개발 PM이자 Python 자동화 외주 분석 도우미다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content