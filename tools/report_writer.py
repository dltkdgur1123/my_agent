from datetime import datetime
import os


def save_report(
    client_request: str,
    analysis: str,
    file_structure: str,
    missing: str
) -> str:
    os.makedirs("reports", exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reports/report_{now}.md"

    content = f"""
# 외주 개발 요청 분석 리포트

---

# 클라이언트 요청

{client_request}

---

# 요청 분석

{analysis}

---

# 추천 폴더/파일 구조

{file_structure}

---

# 누락 검사

{missing}
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path