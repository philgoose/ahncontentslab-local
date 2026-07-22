# raw/ — 원본 저장본을 넣는 곳

브라우저에서 `Ctrl+S`("HTML만")로 저장한 imweb 페이지를 이 폴더에 넣고 커밋하면,
GitHub Actions가 자동으로 clean_imweb 파이프라인을 돌려 정리하고 Pages에 배포한다.

## 파일명 규칙 (권장)
| 원본 페이지 | 파일명 |
|---|---|
| 홈 | index.html |
| ABOUT US | ABOUTUS.html |
| History | 20_History.html |
| Press | 21_Press.html |
| ACL PROJECT | BOARD.html |
| ORCHESTRA | EXHIBITION.html |
| Odyssey Symphony | 24_Odyssey.html |
| ACL Philharmonic | 28_Philharmonic.html |
| GALLERY | 23_GALLERY.html |
| PLAYLIST | 33_PLAYLIST.html |
| IMMERSION 몰입 | 35_IMMERSION.html |
| NOTICE | 30_NOTICE.html |

파일명이 위와 달라도 처리는 되지만, 페이지 간 내부 링크가 맞으려면 이 이름을 쓰는 게 좋다.
