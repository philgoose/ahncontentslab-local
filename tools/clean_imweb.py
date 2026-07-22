#!/usr/bin/env python3
"""
안콘텐츠랩 imweb 저장본 일괄 정리 파이프라인
- Claude 브라우징 오버레이 제거 (glow/Stop버튼/유령커서/애니메이션CSS)
- 오류 153 유발 배경영상 iframe 제거 (배경이미지로 대체)
- 로컬 실행 시 실패하는 서버 통신 무력화 (password ajax / CRM SDK)
- imweb 유튜브 재초기화 무력화
- 내부 링크를 로컬 파일명으로 변환 → 페이지 간 이동 가능
사용: python3 clean_imweb.py <입력.html> <출력.html>
"""
import re, sys

# 사이트맵: 원본 URL 경로 → 로컬 파일명
SITEMAP = {
    "": "index.html",              # 홈
    "ABOUTUS": "ABOUTUS.html",     # ABOUT US
    "20": "20_History.html",       # ├ History
    "21": "21_Press.html",         # └ Press
    "BOARD": "BOARD.html",         # ACL PROJECT
    "EXHIBITION": "EXHIBITION.html",  # ORCHESTRA
    "24": "24_Odyssey.html",       # ├ Odyssey Symphony
    "28": "28_Philharmonic.html",  # └ ACL Philharmonic
    "23": "23_GALLERY.html",       # GALLERY
    "33": "33_PLAYLIST.html",      # PLAYLIST
    "35": "35_IMMERSION.html",     # └ IMMERSION 몰입
    "30": "30_NOTICE.html",        # NOTICE
}

def clean(html: str) -> str:
    # 1) Claude 오버레이 4종
    html = re.sub(r'<div id="claude-agent-glow-border"[\s\S]*?(?=</body>)', '', html)
    html = re.sub(r'<style id="claude-agent-animation-styles">[\s\S]*?</style>', '', html)
    html = html.replace('<script type="text/javascript" id="www-widgetapi-script" '
                        'src="https://www.youtube.com/s/player/c80bf7e2/www-widgetapi.vflset/www-widgetapi.js" async=""></script>', '')

    # 2) 배경영상 iframe (오류 153) 래퍼째 제거
    html = re.sub(r'<div class="section_vg_wrap _section_vg_wrap">.*?</iframe></div>', '', html, flags=re.DOTALL)

    # 3) imweb 유튜브 배경 재초기화 무력화
    html = re.sub(r'section_youtube_list\.push\(\{[^}]*\}\);', '/* disabled */', html)

    # 4) 로컬 실행 오류 무력화
    html = re.sub(r"\$\.ajax\(\{\s*type: 'POST',\s*data: \{ \},\s*url: \('/shop/load_change_password\.cm'\),[\s\S]*?\}\);",
                  "/* local: disabled */", html, count=1)
    html = re.sub(r"const c = window\.crmService;\s*c\.boot\(\{[\s\S]*?\}\)", "/* local: disabled */", html, count=1)

    # 5) 내부 링크 → 로컬 파일명 (긴 경로 먼저 치환)
    for path, fname in sorted(SITEMAP.items(), key=lambda x: -len(x[0])):
        if path:
            html = html.replace(f'href="https://www.ahncontentslab.co.kr/{path}"', f'href="{fname}"')
    html = html.replace('href="https://www.ahncontentslab.co.kr/"', 'href="index.html"')

    # 6) 텍스트 가독성 보정
    if 'local-final-polish' not in html:
        css = ('<style id="local-final-polish">.visual_section .item.video_item .op ._text h1 em,'
               '.visual_section .item.video_item .op ._text p em,'
               '.visual_section .item.video_item .op ._text span{text-shadow:0 2px 18px rgba(0,0,0,.45)}</style>')
        html = html.replace('</head>', css + '</head>', 1)
    return html

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding='utf-8') as f:
        out = clean(f.read())
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"OK {src} -> {dst} ({len(out):,} bytes)")
