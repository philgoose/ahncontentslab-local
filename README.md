# ahncontentslab-local

안콘텐츠랩(ahncontentslab.co.kr) 사이트의 로컬 정리본 및 처리 파이프라인.

## 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 홈페이지 정리 완료본 — 오류 153 배경영상 제거, 오버레이 제거, 내부 링크 로컬 변환 |
| `tools/clean_imweb.py` | imweb 저장본 일괄 정리 파이프라인 (페이지 추가 시 사용) |
| `tools/유튜브_영상_진단.html` | 유튜브 영상 임베드 가능 여부 5초 판별 도구 |
| `docs/사이트_전체_작업_안내.md` | 전체 11페이지 사이트맵 및 수집·처리 절차 |

## 처리 내용 (index.html 기준)

- Claude 브라우징 에이전트 오버레이 제거 (glow 테두리 / Stop 버튼 / 유령 커서 / 애니메이션 CSS)
- YouTube 오류 153 유발 배경영상 iframe 제거 → 정지 배경이미지 대체 + 텍스트 그림자 보정
- imweb 유튜브 재초기화(`section_youtube_list.push`) 무력화
- 로컬 실행 시 실패하는 서버 통신(비밀번호 안내 ajax, CRM SDK) 무력화
- 내부 링크 40개를 로컬 파일명으로 변환 (11페이지 상호 이동 구조)

## 자동 배포 (GitHub Actions)

`raw/` 폴더에 저장본 HTML을 넣고 커밋하면, Actions가 자동으로 정리 파이프라인을
실행해 `_site/`로 빌드하고 GitHub Pages에 배포한다. 서버에서 파이썬이 직접 도는
구조라, Pages의 정적 호스팅 한계를 우회한다.

```
raw/*.html  →  tools/build_site.py (clean_imweb 적용)  →  _site/*.html  →  Pages 배포
```

- 워크플로: `.github/workflows/deploy.yml` (push 시 자동, 수동 실행도 가능)
- 파일명 규칙: `raw/README.md` 참고
- 라이브: https://philgoose.github.io/ahncontentslab-local/

## 로컬에서 단일 파일 처리

```bash
python3 tools/clean_imweb.py 저장한페이지.html 출력파일.html
```

## 남은 작업

하위 10개 페이지(ABOUTUS, BOARD, EXHIBITION, GALLERY 등)는 사이트 봇 차단으로
직접 수집 불가 — 브라우저 `Ctrl+S`("HTML만") 저장 후 파이프라인 처리.
목록·절차는 `docs/사이트_전체_작업_안내.md` 참고.

## 라이브 사이트의 오류 153 원인

로컬 코드와 무관. 히어로 영상(`ipqws5T3gEs`)의 유튜브 측 설정
(임베드 차단·비공개·저작권 제한 추정)이 원인이며, 영상 소유자만
유튜브 스튜디오에서 해결 가능하다.

---
Maintained by [philgoose](https://github.com/philgoose)
