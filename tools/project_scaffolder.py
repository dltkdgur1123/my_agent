import os
import re
import zipfile
from datetime import datetime


def get_comment_style(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".py":
        return "#"

    if ext in [".js", ".jsx", ".ts", ".tsx", ".java", ".cs", ".cpp", ".c"]:
        return "//"

    if ext in [".html", ".xml"]:
        return "html"

    if ext in [".md", ".txt"]:
        return "text"

    return "#"


def clean_path_name(path: str) -> str:
    path = path.strip()

    path = path.replace("```", "")
    path = path.replace("`", "")
    path = path.replace("*", "")
    path = path.replace(":", "")
    path = path.replace('"', "")
    path = path.replace("'", "")
    path = path.replace("**", "")

    path = path.strip()

    if " " in path:
        path = path.split(" ")[0]

    return path.strip()


def get_sections_by_file_role(file_path: str, role: str = "") -> list[dict]:
    lower_text = f"{file_path} {role}".lower()

    if any(keyword in lower_text for keyword in ["rag", "retriever", "vector", "faiss", "chroma", "embedding", "langchain"]):
        return [
            {
                "title": "환경변수 및 모델 설정 섹션",
                "todos": [
                    "OPENAI_API_KEY 같은 환경변수를 불러온다.",
                    "사용할 LLM 모델과 Embedding 모델을 설정한다.",
                    "LangChain 관련 객체를 초기화한다."
                ]
            },
            {
                "title": "문서 로드 섹션",
                "todos": [
                    "PDF, TXT, DOCX 등 입력 문서를 불러온다.",
                    "문서를 LangChain Document 형태로 변환한다.",
                    "파일이 비어 있거나 형식이 맞지 않는 경우 예외처리한다."
                ]
            },
            {
                "title": "Chunk 분할 섹션",
                "todos": [
                    "TextSplitter를 설정한다.",
                    "chunk_size와 chunk_overlap 값을 정한다.",
                    "긴 문서를 검색 가능한 단위로 나눈다."
                ]
            },
            {
                "title": "Embedding 및 Vector DB 생성 섹션",
                "todos": [
                    "문서 chunk를 Embedding 벡터로 변환한다.",
                    "FAISS 또는 Chroma 같은 Vector DB에 저장한다.",
                    "기존 인덱스가 있으면 재사용할 수 있게 처리한다."
                ]
            },
            {
                "title": "Retriever 검색 섹션",
                "todos": [
                    "사용자 질문을 입력받는다.",
                    "질문과 관련 있는 문서 chunk를 검색한다.",
                    "검색 결과가 없는 경우 안내 메시지를 제공한다."
                ]
            },
            {
                "title": "Prompt 및 답변 생성 섹션",
                "todos": [
                    "검색된 문서를 기반으로 Prompt를 구성한다.",
                    "LLM을 호출하여 답변을 생성한다.",
                    "답변과 참고 문서를 함께 반환한다."
                ]
            },
            {
                "title": "결과 출력 섹션",
                "todos": [
                    "생성된 답변을 화면에 출력한다.",
                    "참고 문서 또는 근거 텍스트를 함께 보여준다.",
                    "필요하면 결과를 Markdown 또는 txt 파일로 저장한다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["whisper", "audio", "video", "transcript", "subtitle", "youtube"]):
        return [
            {
                "title": "영상/오디오 입력 섹션",
                "todos": [
                    "사용자가 업로드한 영상 또는 오디오 파일을 받는다.",
                    "파일 확장자와 용량을 검증한다.",
                    "임시 저장 경로를 생성한다."
                ]
            },
            {
                "title": "오디오 추출 섹션",
                "todos": [
                    "영상 파일에서 오디오를 추출한다.",
                    "ffmpeg 또는 moviepy 사용 여부를 결정한다.",
                    "추출된 오디오 파일 경로를 반환한다."
                ]
            },
            {
                "title": "Whisper 변환 섹션",
                "todos": [
                    "Whisper 모델 또는 API를 호출한다.",
                    "음성을 텍스트로 변환한다.",
                    "변환 실패 시 사용자에게 오류 메시지를 제공한다."
                ]
            },
            {
                "title": "자막 스크립트 저장 섹션",
                "todos": [
                    "변환된 텍스트를 txt 파일로 저장한다.",
                    "필요하면 srt 형식으로 저장한다.",
                    "인코딩 문제를 방지하기 위해 UTF-8로 저장한다."
                ]
            },
            {
                "title": "요약 및 Q&A 연결 섹션",
                "todos": [
                    "자막 스크립트를 요약 기능에 연결한다.",
                    "RAG 또는 검색 기능과 연결할 수 있게 문서화한다.",
                    "사용자가 질문할 수 있는 흐름을 만든다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["crawl", "crawler", "scrape", "scraper", "selenium", "beautifulsoup", "requests"]):
        return [
            {
                "title": "요청 설정 섹션",
                "todos": [
                    "requests 또는 Selenium 사용 여부를 결정한다.",
                    "User-Agent, headers, timeout 값을 설정한다.",
                    "접속 차단 또는 응답 실패에 대비한다."
                ]
            },
            {
                "title": "페이지 접속 섹션",
                "todos": [
                    "대상 URL에 접속한다.",
                    "검색어 또는 페이지 번호를 URL에 반영한다.",
                    "페이지 로딩 완료를 기다린다."
                ]
            },
            {
                "title": "데이터 추출 섹션",
                "todos": [
                    "HTML에서 필요한 요소를 선택한다.",
                    "상품명, 가격, 리뷰, 날짜 등 필요한 데이터를 추출한다.",
                    "누락된 값이 있을 경우 기본값을 처리한다."
                ]
            },
            {
                "title": "페이지네이션 섹션",
                "todos": [
                    "다음 페이지 URL 또는 버튼을 찾는다.",
                    "지정한 페이지 수만큼 반복한다.",
                    "마지막 페이지 도달 시 반복을 종료한다."
                ]
            },
            {
                "title": "데이터 정리 및 저장 섹션",
                "todos": [
                    "수집 데이터를 list[dict] 형태로 정리한다.",
                    "중복 데이터를 제거한다.",
                    "CSV 또는 Excel 파일로 저장한다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["streamlit", "main.py", "app.py", "ui", "dashboard"]):
        return [
            {
                "title": "환경변수 및 초기 설정 섹션",
                "todos": [
                    "load_dotenv()로 환경변수를 불러온다.",
                    "필요한 라이브러리를 import한다.",
                    "앱 실행에 필요한 기본 설정을 준비한다."
                ]
            },
            {
                "title": "페이지 타이틀 및 레이아웃 섹션",
                "todos": [
                    "st.set_page_config()로 페이지 제목과 레이아웃을 설정한다.",
                    "st.title()과 st.caption()으로 앱 목적을 보여준다.",
                    "사용자가 기능을 쉽게 이해할 수 있게 화면을 구성한다."
                ]
            },
            {
                "title": "입력 UI 섹션",
                "todos": [
                    "st.text_area(), st.file_uploader(), st.text_input() 등 입력 UI를 만든다.",
                    "입력값이 비어 있을 때 경고 메시지를 출력한다.",
                    "사용자가 어떤 값을 넣어야 하는지 placeholder를 작성한다."
                ]
            },
            {
                "title": "실행 버튼 및 처리 로직 섹션",
                "todos": [
                    "st.button()으로 기능 실행 버튼을 만든다.",
                    "버튼 클릭 시 필요한 함수를 호출한다.",
                    "spinner를 사용해 처리 중 상태를 보여준다."
                ]
            },
            {
                "title": "결과 출력 섹션",
                "todos": [
                    "st.markdown(), st.code(), st.success()로 결과를 출력한다.",
                    "분석 결과와 파일 구조를 구분해서 보여준다.",
                    "긴 텍스트는 코드블록 또는 접힘 영역으로 보여준다."
                ]
            },
            {
                "title": "파일 저장 및 다운로드 섹션",
                "todos": [
                    "생성된 결과를 파일로 저장한다.",
                    "st.download_button()으로 다운로드 기능을 제공한다.",
                    "저장 완료 메시지를 사용자에게 보여준다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["html", "homepage", "landing", "website", "frontend", "page"]):
        return [
            {
                "title": "HEAD 섹션",
                "todos": [
                    "meta charset과 viewport를 설정한다.",
                    "페이지 title을 작성한다.",
                    "CSS 파일과 필요한 외부 리소스를 연결한다."
                ]
            },
            {
                "title": "HEADER / 메뉴 섹션",
                "todos": [
                    "로고 영역을 만든다.",
                    "메뉴 또는 내비게이션 링크를 배치한다.",
                    "로그인 또는 CTA 버튼이 필요한지 확인한다."
                ]
            },
            {
                "title": "HERO 섹션",
                "todos": [
                    "메인 타이틀을 작성한다.",
                    "서비스 설명 문구를 작성한다.",
                    "주요 버튼 또는 대표 이미지를 배치한다."
                ]
            },
            {
                "title": "BODY / 콘텐츠 섹션",
                "todos": [
                    "서비스 소개 내용을 구성한다.",
                    "카드 UI 또는 섹션별 설명을 배치한다.",
                    "사용자가 이해하기 쉬운 흐름으로 내용을 정리한다."
                ]
            },
            {
                "title": "FOOTER 섹션",
                "todos": [
                    "회사 정보 또는 연락처를 작성한다.",
                    "저작권 문구를 작성한다.",
                    "SNS 또는 관련 링크를 추가한다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["api", "server", "fastapi", "flask", "express", "route", "router"]):
        return [
            {
                "title": "서버 초기화 섹션",
                "todos": [
                    "서버 프레임워크 객체를 생성한다.",
                    "환경변수와 설정값을 불러온다.",
                    "미들웨어 또는 공통 설정을 추가한다."
                ]
            },
            {
                "title": "라우터 정의 섹션",
                "todos": [
                    "API 엔드포인트를 정의한다.",
                    "GET, POST, PUT, DELETE 메서드를 구분한다.",
                    "요청 경로와 함수 역할을 명확히 분리한다."
                ]
            },
            {
                "title": "요청 데이터 검증 섹션",
                "todos": [
                    "필수 파라미터가 있는지 확인한다.",
                    "잘못된 데이터 형식을 예외처리한다.",
                    "검증 실패 시 적절한 응답을 반환한다."
                ]
            },
            {
                "title": "비즈니스 로직 처리 섹션",
                "todos": [
                    "실제 기능 처리 함수를 호출한다.",
                    "DB 조회, 외부 API 호출, 계산 로직 등을 분리한다.",
                    "복잡한 로직은 별도 서비스 파일로 분리한다."
                ]
            },
            {
                "title": "응답 및 예외처리 섹션",
                "todos": [
                    "성공 응답 형식을 통일한다.",
                    "에러 발생 시 사용자에게 이해 가능한 메시지를 반환한다.",
                    "서버 로그를 남길 수 있게 처리한다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["db", "database", "model", "schema", "prisma", "supabase", "sql"]):
        return [
            {
                "title": "DB 연결 설정 섹션",
                "todos": [
                    "DB 접속 정보를 환경변수에서 불러온다.",
                    "DB 클라이언트 또는 ORM을 초기화한다.",
                    "연결 실패 시 예외처리한다."
                ]
            },
            {
                "title": "스키마 / 모델 정의 섹션",
                "todos": [
                    "테이블 또는 컬렉션 구조를 정의한다.",
                    "필드 타입과 기본값을 설정한다.",
                    "관계형 데이터라면 관계 설정을 작성한다."
                ]
            },
            {
                "title": "CRUD 함수 섹션",
                "todos": [
                    "데이터 생성 함수를 작성한다.",
                    "데이터 조회 함수를 작성한다.",
                    "데이터 수정 및 삭제 함수를 작성한다."
                ]
            },
            {
                "title": "트랜잭션 및 예외처리 섹션",
                "todos": [
                    "여러 작업이 함께 처리되어야 하는 경우 트랜잭션을 적용한다.",
                    "중복 데이터나 무결성 오류를 처리한다.",
                    "실패 시 롤백 또는 사용자 안내를 제공한다."
                ]
            }
        ]

    if any(keyword in lower_text for keyword in ["excel", "csv", "xlsx", "export", "report"]):
        return [
            {
                "title": "데이터 입력 섹션",
                "todos": [
                    "저장할 데이터를 인자로 받는다.",
                    "list[dict] 또는 DataFrame 형태인지 확인한다.",
                    "비어 있는 데이터일 경우 예외처리한다."
                ]
            },
            {
                "title": "데이터 정리 섹션",
                "todos": [
                    "컬럼 순서를 정리한다.",
                    "누락값을 처리한다.",
                    "사용자가 보기 좋은 컬럼명으로 변경한다."
                ]
            },
            {
                "title": "파일 저장 섹션",
                "todos": [
                    "CSV 또는 Excel 파일로 저장한다.",
                    "저장 경로를 생성한다.",
                    "파일명 중복을 방지한다."
                ]
            },
            {
                "title": "다운로드 / 반환 섹션",
                "todos": [
                    "저장된 파일 경로를 반환한다.",
                    "Streamlit 또는 웹 UI에서 다운로드할 수 있게 연결한다.",
                    "저장 실패 시 오류 메시지를 제공한다."
                ]
            }
        ]

    return [
        {
            "title": "초기 설정 섹션",
            "todos": [
                "필요한 라이브러리 또는 모듈을 import한다.",
                "환경변수 또는 설정값이 필요한지 확인한다.",
                "이 파일에서 사용할 기본 상수나 경로를 정의한다."
            ]
        },
        {
            "title": "핵심 기능 구현 섹션",
            "todos": [
                "이 파일의 주요 역할에 해당하는 함수 또는 클래스를 작성한다.",
                "입력값과 출력값의 형태를 정한다.",
                "다른 파일과 연결되는 부분을 명확히 한다."
            ]
        },
        {
            "title": "예외처리 섹션",
            "todos": [
                "입력값이 비어 있거나 잘못된 경우를 처리한다.",
                "외부 API, 파일, DB 사용 시 실패 가능성을 처리한다.",
                "사용자에게 이해 가능한 에러 메시지를 제공한다."
            ]
        },
        {
            "title": "테스트 및 실행 확인 섹션",
            "todos": [
                "간단한 테스트 코드를 작성한다.",
                "예상 입력과 예상 출력을 확인한다.",
                "실행 흐름이 정상적으로 이어지는지 점검한다."
            ]
        }
    ]


def format_section_comment(comment_style: str, title: str, todos: list[str]) -> str:
    if comment_style == "#":
        lines = [
            "# ==================================================",
            f"# {title}",
            "# ==================================================",
            "",
            "# TODO:"
        ]

        for todo in todos:
            lines.append(f"# - {todo}")

        lines.append("")

        return "\n".join(lines)

    if comment_style == "//":
        lines = [
            "// ==================================================",
            f"// {title}",
            "// ==================================================",
            "",
            "// TODO:"
        ]

        for todo in todos:
            lines.append(f"// - {todo}")

        lines.append("")

        return "\n".join(lines)

    if comment_style == "html":
        lines = [
            "<!-- ==================================================",
            title,
            "==================================================",
            "",
            "TODO:"
        ]

        for todo in todos:
            lines.append(f"- {todo}")

        lines.append("-->")
        lines.append("")

        return "\n".join(lines)

    lines = [
        f"## {title}",
        "",
        "TODO:"
    ]

    for todo in todos:
        lines.append(f"- {todo}")

    lines.append("")

    return "\n".join(lines)


def make_file_content(file_path: str, role: str = "") -> str:
    comment_style = get_comment_style(file_path)
    file_name = os.path.basename(file_path)

    sections = get_sections_by_file_role(file_path, role)

    if comment_style == "#":
        lines = [
            "# ==================================================",
            f"# 파일명: {file_name}",
            f"# 역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            "# ==================================================",
            ""
        ]

    elif comment_style == "//":
        lines = [
            "// ==================================================",
            f"// 파일명: {file_name}",
            f"// 역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            "// ==================================================",
            ""
        ]

    elif comment_style == "html":
        lines = [
            "<!-- ==================================================",
            f"파일명: {file_name}",
            f"역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            "================================================== -->",
            ""
        ]

    else:
        lines = [
            f"# {file_name}",
            "",
            f"역할: {role or '이 파일의 역할을 구현 단계에서 구체화'}",
            ""
        ]

    for section in sections:
        lines.append(
            format_section_comment(
                comment_style,
                section["title"],
                section["todos"]
            )
        )

    return "\n".join(lines)


def extract_paths_from_structure(file_structure: str) -> list[tuple[str, str]]:
    results = []

    for line in file_structure.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if "├" not in clean_line and "└" not in clean_line and "/" not in clean_line:
            continue

        cleaned = re.sub(r"[│├└─]+", "", clean_line)
        cleaned = cleaned.replace("**", "")
        cleaned = cleaned.replace("`", "")
        cleaned = cleaned.strip()

        if not cleaned:
            continue

        role = ""

        if "(" in cleaned and ")" in cleaned:
            role = cleaned[cleaned.find("(") + 1:cleaned.rfind(")")].strip()
            path = cleaned[:cleaned.find("(")].strip()
        else:
            path = cleaned.strip()

        path = path.replace("\\", "/").strip()
        path = clean_path_name(path)

        if not path:
            continue

        if path.startswith("#"):
            continue

        if path.startswith("-"):
            path = path.lstrip("-").strip()

        if not path:
            continue

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