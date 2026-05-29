from datetime import datetime


def make_report_content(
    client_request: str,
    project_type: str,
    analysis: str,
    file_structure: str,
    missing: str
) -> str:

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return f"""# 외주 요청 분석 리포트

생성일시: {created_at}

---

# 원본 요청

{client_request}

---

# 프로젝트 유형 분석

{project_type}

---

# 요청 분석

{analysis}

---

# 추천 파일 구조

```text
{file_structure}

---

# 누락검사

{missing}
"""

