from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def detect_project_type(client_request: str) -> str:

    prompt = f"""
사용자의 요청을 분석하여
프로젝트 유형과 예상 기술스택을 분류해라.

출력 형식:

프로젝트 유형:
- ...

예상 기술스택:
- ...

AI 분석 이유:
- ...
- ...

사용자 요청:
{client_request}
"""

    response = client.chat.completions.create(
        model=os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini"
        ),
        messages=[
            {
                "role": "system",
                "content": "너는 소프트웨어 아키텍트다."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content