from dotenv import load_dotenv
import streamlit as st
import os

from tools.request_analyzer import analyze_request
from tools.file_structure_generator import generate_file_structure
from tools.missing_checker import check_missing_parts
from tools.report_writer import save_report
from tools.feature_code_researcher import research_feature_code
from tools.dev_journal_writer import generate_final_portfolio,save_dev_journal
from tools.project_reader import read_project_files_from_zip
from tools.file_portfolio_generator import generate_all_file_portfolios
from tools.project_scaffolder import create_project_skeleton, zip_project_folder
from tools.project_type_detector import detect_project_type

st.set_page_config(
    page_title="외주 개발 에이전트",
    page_icon="🧰",
    layout="wide"
)

st.title("외주 개발 에이전트")
st.caption("클라이언트 요청 분석, To Do 생성, 파일 구조 설계, 누락 검사, 기능 구현 코드 리서치를 도와줍니다.")

tab1, tab2, tab3 = st.tabs(["외주 요청 분석", "기능 구현 코드 리서치", "작업일지 작성"])


with tab1:
    st.subheader("외주 요청 분석")

    client_request = st.text_area(
        "클라이언트 요청 내용을 입력하세요",
        height=180,
        placeholder="예: 네이버 쇼핑 리뷰를 수집해서 엑셀로 저장하는 프로그램을 만들고 싶습니다."
    )

    if st.button("요청 분석 시작", type="primary"):
        if not client_request.strip():
            st.warning("클라이언트 요청 내용을 입력해주세요.")
        else:
            with st.spinner("프로젝트 유형 분석 중..."):
                project_type = detect_project_type(
                    client_request
                )
            
            with st.spinner("요청 분석 중..."):
                analysis = analyze_request(client_request)

            with st.spinner("폴더/파일 구조 생성 중..."):
                file_structure = generate_file_structure(client_request, analysis)

            with st.spinner("누락 항목 검사 중..."):
                missing = check_missing_parts(client_request, analysis)

            file_path = save_report(
                client_request,
                analysis,
                file_structure,
                missing
            )

            st.session_state["project_type"] = project_type
            st.session_state["analysis"] = analysis
            st.session_state["file_structure"] = file_structure
            st.session_state["missing"] = missing
            st.session_state["report_path"] = file_path

        st.markdown("## 0. 프로젝트 유형 분석")

        st.markdown(
            st.session_state["project_type"]
        )
        
        
    if "analysis" in st.session_state:
        st.success(f"리포트 저장 완료: {st.session_state['report_path']}")

        st.markdown("## 1. 요청 분석")
        st.markdown(st.session_state["analysis"])

        st.markdown("## 2. 추천 폴더/파일 구조")
        st.code(st.session_state["file_structure"])

        if st.button("프로젝트 뼈대 생성"):
            project_dir = create_project_skeleton(
                st.session_state["file_structure"]
            )

            zip_path = zip_project_folder(project_dir)

            st.success(f"프로젝트 뼈대 생성 완료: {project_dir}")

            with open(zip_path, "rb") as f:
                st.download_button(
                    label="생성된 프로젝트 ZIP 다운로드",
                    data=f,
                    file_name=os.path.basename(zip_path),
                    mime="application/zip"
                )

        st.markdown("## 3. 누락 검사")
        st.markdown(st.session_state["missing"])


with tab2:
    st.subheader("기능 구현 코드 리서치")

    feature_request = st.text_area(
        "구현하고 싶은 기능을 설명하세요",
        height=180,
        placeholder="예: PDF를 업로드하고 LangChain으로 문서를 나눈 뒤 FAISS에 저장해서 질문할 수 있게 만들고 싶습니다."
    )

    analysis_context = st.text_area(
        "전체 요청 분석 내용이 있다면 붙여넣으세요",
        height=120,
        placeholder="선택사항입니다. 없으면 비워도 됩니다."
    )

    file_structure_context = st.text_area(
        "추천 폴더/파일 구조가 있다면 붙여넣으세요",
        height=120,
        placeholder="선택사항입니다. 없으면 비워도 됩니다."
    )

    if st.button("코드 리서치 시작"):
        if not feature_request.strip():
            st.warning("구현하고 싶은 기능을 입력해주세요.")
        else:
            with st.spinner("기능 구현 코드 리서치 중..."):
                feature_research = research_feature_code(
                    feature_request,
                    analysis_context,
                    file_structure_context
                )

            st.markdown("## 기능 구현 코드 리서치 결과")
            st.markdown(feature_research)


with tab3:
    st.subheader("작업일지 / 포트폴리오 생성")

    uploaded_zip = st.file_uploader(
        "작업한 프로젝트 폴더를 ZIP 파일로 업로드하세요",
        type=["zip"]
    )

    if uploaded_zip is not None:
        st.info(f"업로드된 파일: {uploaded_zip.name}")

    if st.button("파일별 포트폴리오 생성", type="primary"):
        if uploaded_zip is None:
            st.warning("먼저 프로젝트 ZIP 파일을 업로드해주세요.")
        else:
            with st.spinner("프로젝트 파일을 읽는 중입니다..."):
                file_tree, project_files = read_project_files_from_zip(
                    uploaded_zip
                )

            with st.spinner("파일별 포트폴리오를 생성 중입니다..."):
                file_portfolios = generate_all_file_portfolios(
                    project_files
                )

            with st.spinner("최종 포트폴리오 문서로 정리 중입니다..."):
                final_portfolio = generate_final_portfolio(
                    file_tree,
                    file_portfolios
                )

            st.session_state["dev_journal_preview"] = final_portfolio

    if "dev_journal_preview" in st.session_state:
        st.markdown("## 포트폴리오 작업일지 미리보기")
        st.markdown(st.session_state["dev_journal_preview"])

        if st.button("Markdown 파일로 저장"):
            file_path = save_dev_journal(
                st.session_state["dev_journal_preview"]
            )

            st.success(f"작업일지 저장 완료: {file_path}")
    
     
