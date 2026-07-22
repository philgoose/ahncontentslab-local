#!/usr/bin/env python3
"""
build_site.py — raw/ 폴더의 imweb 저장본을 일괄 정리해 _site/ 로 배포 빌드.
GitHub Actions가 이 스크립트를 실행한다.

흐름:
  raw/*.html  →  clean_imweb.clean()  →  _site/*.html
  - 파일명이 SITEMAP 값과 일치하면 그대로, 아니면 원본명 유지
  - raw/ 가 비어있거나 없으면, 저장소 루트의 index.html 을 그대로 사용(현 상태 유지)
"""
import os, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from clean_imweb import clean, SITEMAP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 저장소 루트
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "_site")

def main():
    # 배포 폴더 초기화
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    processed = 0

    # 1) raw/ 저장본 정리
    if os.path.isdir(RAW):
        for fn in sorted(os.listdir(RAW)):
            if not fn.lower().endswith(".html"):
                continue
            src = os.path.join(RAW, fn)
            with open(src, encoding="utf-8", errors="ignore") as f:
                cleaned = clean(f.read())
            with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"  cleaned: raw/{fn} -> _site/{fn}")
            processed += 1

    # 2) raw 처리분이 없으면 기존 루트 index.html 을 배포에 포함(현 상태 유지)
    if processed == 0:
        root_index = os.path.join(ROOT, "index.html")
        if os.path.exists(root_index):
            shutil.copy(root_index, os.path.join(OUT, "index.html"))
            print("  raw/ 없음 → 기존 index.html 사용")
        else:
            with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
                f.write("<h1>raw/ 폴더에 저장본 HTML을 넣어 커밋하세요.</h1>")
            print("  raw/ 없고 index.html 도 없음 → 안내 페이지 생성")

    # 3) Jekyll 비활성화(밑줄 폴더/파일 그대로 서빙)
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # 4) 배포 결과 요약
    files = sorted(os.listdir(OUT))
    print(f"\n빌드 완료: _site/ 에 {len([x for x in files if x.endswith('.html')])}개 페이지")

if __name__ == "__main__":
    main()
