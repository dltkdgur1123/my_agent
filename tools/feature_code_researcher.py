import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def research_feature_code(feature_request: str, analysis: str, file_structure: str) -> str:
    prompt = f"""
너는 초보 개발자를 돕는 기능 구현 코드 리서치 에이전트다.

사용자가 구현하고 싶은 기능 설명을 입력하면,
그 기능을 구현하기 위해 필요한 기술, 참고할 공식문서, 코드 예시, 구현 순서를 정리해라.

중요 규칙:
- 사용자는 초보 개발자이므로 어렵게 설명하지 말고 실무적으로 설명해라.
- 단순 검색 키워드만 주지 말고, 어떤 코드 구조로 구현해야 하는지 안내해라.
- 공식문서를 참고해야 할 항목은 "공식문서에서 확인할 것"으로 정리해라.
- 실제 코드는 너무 길게 쓰지 말고, 핵심 코드 뼈대 위주로 작성해라.
- 추천 파일명은 앞에서 만든 폴더/파일 구조와 어울리게 제안해라.
- 없는 라이브러리나 확실하지 않은 기능은 단정하지 말고 "확인 필요"라고 표시해라.

[구현하고 싶은 기능]
{feature_request}

[전체 요청 분석]
{analysis}

[추천 폴더/파일 구조]
{file_structure}

[출력 형식]

## 1. 기능 요약
-

## 2. 필요한 기술
-

## 3. 공식문서에서 확인할 것
-

## 4. 추천 구현 위치
- 파일명:
- 이유:

## 5. 구현 순서
1.
2.
3.

## 6. 핵심 코드 뼈대
- 필요한 경우 짧은 코드 예시만 작성

## 7. 추가로 필요한 패키지
-

## 8. 주의할 점
-
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "너는 초보 개발자를 위한 실무형 Python 코드 리서치 도우미다."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content