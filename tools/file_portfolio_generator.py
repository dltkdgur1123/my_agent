import os

from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_file_portfolio(
    file_path: str,
    file_content: str
) -> str:

    prompt = f"""
너는 개발 프로젝트의 각 파일을
Notion 포트폴리오용으로 해설하는 에이전트다.

아래 파일 하나를 분석해서,
해당 파일 안의 코드를 기능/주제별 파트로 나누고,
각 파트마다 실제 코드와 설명을 작성해라.

가장 중요한 규칙:
- 각 프로젝트 파일마다 여러 개의 파트로 나눠라.
- 각 파트 제목은 반드시 "# 환경변수 설정", "# 페이지 타이틀 구성", "# 파일 업로드 처리" 같은 형태로 작성해라.
- 각 파트마다 반드시 아래 4가지를 작성해라.
  1. 코드
  2. 이 코드에 들어간 내용
  3. 어떤 기능을 하는지
  4. 구현 이유
- 코드 블록에는 실제 파일에 들어있는 코드를 넣어라.
- 코드 설명만 하고 코드 블록을 생략하지 마라.
- 코드 전체를 한 번에 붙이지 말고 기능 단위로 나누어 보여줘라.
- 파일명만 보고 단정하지 말고 코드 내용을 기준으로 설명해라.
- 너무 사소한 줄은 생략 가능하지만, 기능 이해에 필요한 코드는 반드시 포함해라.
- 초보 개발자가 Notion 포트폴리오에 붙여넣어도 자연스럽게 작성해라.
- 오늘/어제/내일 같은 날짜 표현은 쓰지 마라.
- 확실하지 않은 내용은 "코드 구조상" 또는 "분석 기준"이라고 표현해라.

예시 형식:

### 파일: main.py

#### 파일 역할
Streamlit 기반 메인 UI와 전체 기능 흐름을 담당하는 파일이다.

---

# 환경변수 설정

## 코드

    from dotenv import load_dotenv

    load_dotenv()

## 코드에 들어간 내용
- dotenv 라이브러리에서 load_dotenv 함수를 불러온다.
- .env 파일에 저장된 환경변수를 프로그램 실행 시점에 불러온다.

## 어떤 기능을 하는지
OpenAI API Key 같은 민감한 설정값을 코드에 직접 작성하지 않고,
환경변수로 관리할 수 있게 한다.

## 구현 이유
API 키를 코드에 직접 넣으면 보안 문제가 생길 수 있기 때문에,
.env 파일을 통해 안전하게 관리하도록 설계했다.

---

# 페이지 타이틀 구성

## 코드

    st.set_page_config(
        page_title="외주 개발 에이전트",
        page_icon="🧰",
        layout="wide"
    )

## 코드에 들어간 내용
- Streamlit 페이지 제목을 설정한다.
- 페이지 아이콘을 설정한다.
- 화면 레이아웃을 wide 모드로 설정한다.

## 어떤 기능을 하는지
앱 실행 시 브라우저 탭 제목과 화면 배치를 설정한다.

## 구현 이유
사용자가 앱을 열었을 때 서비스 목적을 바로 이해할 수 있게 하고,
넓은 화면에서 분석 결과를 보기 좋게 표시하기 위해 wide 레이아웃을 사용했다.

[파일 경로]
{file_path}

[파일 코드]
{file_content[:16000]}

[출력 형식]

### 파일: {file_path}

#### 파일 역할
-

---

# 파트명

## 코드

    실제 코드

## 코드에 들어간 내용
-

## 어떤 기능을 하는지
-

## 구현 이유
-

---

# 파트명

## 코드

    실제 코드

## 코드에 들어간 내용
-

## 어떤 기능을 하는지
-

## 구현 이유
-

---

#### 파일 전체 흐름 정리
-

#### 포트폴리오 설명
-

#### 개선 가능 포인트
-
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
                    "너는 코드 파일을 "
                    "Notion 포트폴리오용 개발 기록으로 "
                    "상세하게 해설하는 도우미다."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,
    )

    return response.choices[0].message.content


def generate_all_file_portfolios(
    project_files: list[dict]
) -> list[str]:

    portfolios = []

    for project_file in project_files:

        file_path = project_file["path"]

        file_content = project_file["content"]

        portfolio = generate_file_portfolio(
            file_path=file_path,
            file_content=file_content
        )

        portfolios.append(portfolio)

    return portfolios