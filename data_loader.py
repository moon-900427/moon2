"""
data/text/ 폴더 안의 .md 파일들을 읽어 하나의 텍스트로 합친다.
"""
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "text")


def load_all_projects() -> str:
    all_texts = []
    md_files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".md")])
    for md_file in md_files:
        path = os.path.join(DATA_DIR, md_file)
        with open(path, "r", encoding="utf-8") as f:
            all_texts.append(f.read())
    return "\n\n---\n\n".join(all_texts)


def load_all_projects_cached() -> str:
    return load_all_projects()
