"""
노션 Export zip 파일들에서 텍스트를 추출하는 모듈.
data/ 폴더 안의 모든 .zip 파일을 자동으로 읽는다.
"""
import zipfile
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _read_inner_zip(outer_zip_path: str) -> list[tuple[str, str]]:
    """
    노션 Export zip은 outer zip → inner zip → .md 파일 구조다.
    (파일명, 내용) 튜플 리스트를 반환한다.
    """
    results = []
    with zipfile.ZipFile(outer_zip_path, "r") as outer:
        inner_zip_names = [n for n in outer.namelist() if n.endswith(".zip")]
        for inner_name in inner_zip_names:
            inner_bytes = outer.read(inner_name)
            import io
            with zipfile.ZipFile(io.BytesIO(inner_bytes), "r") as inner:
                md_files = [n for n in inner.namelist() if n.endswith(".md")]
                for md_name in md_files:
                    try:
                        content = inner.read(md_name).decode("utf-8")
                        results.append((md_name, content))
                    except Exception:
                        pass
    return results


def load_all_projects() -> str:
    """
    data/ 폴더 내 모든 zip 파일을 읽어서
    하나의 큰 텍스트로 합쳐서 반환한다.
    """
    all_texts = []

    zip_files = [
        f for f in os.listdir(DATA_DIR) if f.endswith(".zip")
    ]

    for zip_file in sorted(zip_files):
        zip_path = os.path.join(DATA_DIR, zip_file)
        pages = _read_inner_zip(zip_path)
        for filename, content in pages:
            # 파일명에서 프로젝트 경로 추출 (가독성용)
            short_name = filename.split("/")[-1].split(" ")[0]
            all_texts.append(f"[파일: {filename}]\n{content}")

    return "\n\n---\n\n".join(all_texts)


def load_all_projects_cached() -> str:
    """Streamlit 캐시용 래퍼 (app.py에서 @st.cache_data 와 함께 사용)"""
    return load_all_projects()
