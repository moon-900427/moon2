"""
Groq API를 사용하는 AI 분석 엔진.
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
# 무료 티어 토큰 제한에 맞게 데이터 크기를 제한 (약 8,000자)
MAX_DATA_CHARS = 8000


def _trim(data: str) -> str:
    """데이터가 너무 길면 앞부분만 사용한다."""
    if len(data) > MAX_DATA_CHARS:
        return data[:MAX_DATA_CHARS] + "\n\n...(데이터 일부 생략됨)"
    return data


def _ask(prompt: str) -> str:
    response = _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500,
    )
    return response.choices[0].message.content


def guide_budget(project_description: str, data: str) -> str:
    prompt = f"""당신은 영상 제작 컨설팅 회사 VD스튜디오의 베테랑 PD입니다.
아래는 우리 회사의 과거 프로젝트 데이터입니다.

=== 사내 아카이브 데이터 ===
{_trim(data)}
===========================

신규 문의 내용:
{project_description}

위 데이터를 분석하여 다음을 제공해주세요:

1. **추천 견적 범위**: 유사 프로젝트 기준 최소~최대 금액과 근거
2. **전략적 제안 금액**: 수주 가능성이 가장 높은 금액 1개와 이유
3. **주요 비용 항목**: 어디에 얼마 정도 배분하면 좋은지
4. **협상 팁**: 클라이언트가 예산 조정을 요청할 때 대응 방법

숫자와 근거를 구체적으로 제시해주세요."""
    return _ask(prompt)


def guide_schedule(project_description: str, data: str) -> str:
    prompt = f"""당신은 영상 제작 컨설팅 회사 VD스튜디오의 베테랑 PD입니다.
아래는 우리 회사의 과거 프로젝트 데이터입니다.

=== 사내 아카이브 데이터 ===
{_trim(data)}
===========================

신규 문의 내용:
{project_description}

위 데이터를 분석하여 다음을 제공해주세요:

1. **예상 전체 기간**: 총 소요 일수와 근거
2. **단계별 일정**: 기획 → 촬영 → 편집 → 납품 각 단계별 소요 기간
3. **주의할 변수**: 일정이 늘어날 수 있는 요소들
4. **클라이언트 제시용 마일스톤**: 납품일 기준 역산한 주요 체크포인트 4~5개

구체적인 날짜 단위와 근거를 포함해주세요."""
    return _ask(prompt)


def guide_reference(keywords: str, data: str) -> str:
    prompt = f"""당신은 영상 제작 컨설팅 회사 VD스튜디오의 베테랑 영업 전략가입니다.
아래는 우리 회사의 과거 프로젝트 데이터입니다 (레퍼런스 및 포트폴리오 정보 포함).

=== 사내 아카이브 데이터 ===
{_trim(data)}
===========================

클라이언트 요구 키워드:
{keywords}

위 데이터를 분석하여 다음을 제공해주세요:

1. **추천 레퍼런스 TOP 3**: 가장 적합한 과거 프로젝트 또는 포트폴리오 3개
2. **각 레퍼런스가 왜 적합한지**: 클라이언트에게 설명할 수 있는 설득 논리
3. **클라이언트가 중시하는 가치**: 키워드 기반 분석
4. **제안서 오프닝 문구**: 레퍼런스를 소개할 때 쓸 수 있는 문장 2~3개

설득력 있고 구체적으로 작성해주세요."""
    return _ask(prompt)


def analyze_anchoring(data: str) -> str:
    prompt = f"""당신은 영상 제작 컨설팅 회사 VD스튜디오의 영업 전략가입니다.
아래는 우리 회사의 과거 미팅 회의록과 프로젝트 데이터입니다.

=== 사내 아카이브 데이터 ===
{_trim(data)}
===========================

데이터를 분석하여 다음을 도출해주세요:

1. **클라이언트가 반복적으로 요구하는 핵심 가치 TOP 5**: 과거 데이터에서 패턴 추출
2. **업종별 특징**: 어떤 업종의 클라이언트가 무엇을 중시하는지
3. **수주 성공 vs 미수주 패턴**: 수주된 프로젝트와 그렇지 않은 프로젝트의 차이
4. **소통 시 주안점**: 첫 미팅에서 반드시 확인해야 할 질문 5가지

인사이트 중심으로 분석해주세요."""
    return _ask(prompt)
