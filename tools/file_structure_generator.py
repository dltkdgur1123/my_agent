import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_file_structure(client_request: str, analysis: str) -> str:
    prompt = f"""
너는 프리랜서 개발자를 돕는 프로젝트 구조 설계 에이전트다.

아래 클라이언트 요청과 분석 결과를 바탕으로,
개발자가 실제로 만들면 좋은 폴더/파일 구조를 설계해라.

중요 규칙:
- 클라이언트 요청에 가장 적합한 개발 언어 및 프레임워크 기준으로 작성해라.
- 어떤 기술 스택을 선택했는지도 함께 설명해라.
- 웹 프로젝트인지, 데스크탑 프로그램인지, AI 프로젝트인지 분석 후 적절한 구조를 제안해라.
- 파일명과 폴더명 옆에는 괄호로 역할을 설명해라.
- 너무 과하게 만들지 말고 MVP 기준으로 필요한 파일만 제안해라.
- requirements.txt, .env.example, README.md가 필요하면 포함해라.
- 출력은 복사해서 메모장에 붙여넣기 좋게 깔끔하게 작성해라.

[클라이언트 요청]
{client_request}

[분석 결과]
{analysis}

[출력 형식]

## 추천 폴더/파일 구조

project_name/                         (프로젝트 루트 폴더)
├─ main.py                            (프로그램 실행 시작 파일)
├─ requirements.txt                   (필요 패키지 목록)
├─ .env.example                       (환경변수 예시 파일)
└─ README.md                          (사용 방법 문서)

## 구조 설명
-
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "너는 실무형 Python 프로젝트 구조 설계 도우미다."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content