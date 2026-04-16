import streamlit as st
from data_loader import load_all_projects_cached
from ai_engine import guide_budget, guide_schedule, guide_reference, analyze_anchoring

st.set_page_config(
    page_title="VD 컨설팅 AI",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 VD 컨설팅 AI 어시스턴트")
st.caption("사내 아카이브 기반 · 예산 · 일정 · 레퍼런스 · 앵커링 분석")

# 사이드바
with st.sidebar:
    st.header("📁 데이터 상태")
    if st.button("🔄 데이터 새로고침", use_container_width=True):
        st.cache_data.clear()
        st.success("새로고침 완료!")
    st.divider()
    st.markdown("**사용 방법**")
    st.markdown("""
1. 탭을 선택하세요
2. 프로젝트 정보를 입력하세요
3. AI 분석 버튼을 클릭하세요
""")
    st.divider()
    st.caption("현재 로드된 데이터:")
    try:
        data = load_all_projects_cached()
        kb = len(data.encode("utf-8")) / 1024
        st.success(f"✅ {kb:.1f} KB 로드됨")
    except Exception as e:
        st.error(f"❌ 데이터 오류: {e}")


@st.cache_data(ttl=600, show_spinner="사내 데이터 불러오는 중...")
def get_data():
    return load_all_projects_cached()


tab1, tab2, tab3, tab4 = st.tabs([
    "💰 가이드 예산",
    "📅 가이드 일정",
    "🎥 레퍼런스",
    "🧠 앵커링 분석",
])

# ── 탭 1: 가이드 예산 ──────────────────────────────────────────────────────────
with tab1:
    st.subheader("💰 가이드 예산")
    st.markdown("과거 프로젝트 데이터를 분석하여 **전략적 견적안**을 도출합니다.")

    col1, col2 = st.columns([2, 1])
    with col1:
        budget_input = st.text_area(
            "프로젝트 내용을 입력하세요",
            placeholder="예: 5분짜리 기업 교육 영상 6편, 모션그래픽 위주, 다국어 자막 필요",
            height=150,
        )
    with col2:
        st.markdown("**입력 예시**")
        st.markdown("""
- 영상 포맷 (교육/광고/홍보)
- 분량 및 편수
- 제작 방식 (실사/모션/혼합)
- 특수 요구사항
""")

    if st.button("🤖 예산 가이드 생성", type="primary", key="budget_btn"):
        if not budget_input.strip():
            st.warning("프로젝트 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 과거 프로젝트 데이터를 분석하는 중..."):
                data = get_data()
                result = guide_budget(budget_input, data)
            st.success("분석 완료!")
            st.divider()
            st.markdown(result)

# ── 탭 2: 가이드 일정 ──────────────────────────────────────────────────────────
with tab2:
    st.subheader("📅 가이드 일정")
    st.markdown("과거 제작 실적을 분석하여 **신뢰도 높은 타임라인**을 제안합니다.")

    col1, col2 = st.columns([2, 1])
    with col1:
        schedule_input = st.text_area(
            "프로젝트 내용을 입력하세요",
            placeholder="예: 기업 핵심가치 교육영상 5분 x 6편, 인포그래픽 모션, 납품 희망일 2개월 후",
            height=150,
        )
    with col2:
        st.markdown("**입력 예시**")
        st.markdown("""
- 영상 포맷 및 편수
- 희망 납품일
- 촬영 필요 여부
- 수정 예상 횟수
""")

    if st.button("🤖 일정 가이드 생성", type="primary", key="schedule_btn"):
        if not schedule_input.strip():
            st.warning("프로젝트 내용을 입력해주세요.")
        else:
            with st.spinner("AI가 과거 일정 데이터를 분석하는 중..."):
                data = get_data()
                result = guide_schedule(schedule_input, data)
            st.success("분석 완료!")
            st.divider()
            st.markdown(result)

# ── 탭 3: 레퍼런스 ────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🎥 레퍼런스 매칭")
    st.markdown("키워드 입력 시 **최적 포트폴리오 + 설득 논리**를 자동 생성합니다.")

    col1, col2 = st.columns([2, 1])
    with col1:
        ref_input = st.text_input(
            "클라이언트 요구 키워드를 입력하세요",
            placeholder="예: 교육영상, 모션그래픽, B2B, 제조업",
        )
    with col2:
        st.markdown("**입력 예시**")
        st.markdown("""
- 영상 유형
- 업종/산업군
- 톤앤매너
- 타겟 시청자
""")

    if st.button("🤖 레퍼런스 매칭 시작", type="primary", key="ref_btn"):
        if not ref_input.strip():
            st.warning("키워드를 입력해주세요.")
        else:
            with st.spinner("AI가 포트폴리오 데이터를 분석하는 중..."):
                data = get_data()
                result = guide_reference(ref_input, data)
            st.success("매칭 완료!")
            st.divider()
            st.markdown(result)

# ── 탭 4: 앵커링 분석 ────────────────────────────────────────────────────────
with tab4:
    st.subheader("🧠 클라이언트 앵커링 분석")
    st.markdown("과거 미팅 데이터를 분석하여 **클라이언트가 반복 요구하는 핵심 가치**를 추출합니다.")

    st.info("이 분석은 전체 아카이브 데이터를 종합 분석합니다. 시간이 조금 걸릴 수 있어요.")

    if st.button("🤖 앵커링 분석 시작", type="primary", key="anchor_btn"):
        with st.spinner("AI가 전체 미팅 데이터를 분석하는 중... (30초~1분 소요)"):
            data = get_data()
            result = analyze_anchoring(data)
        st.success("분석 완료!")
        st.divider()
        st.markdown(result)
