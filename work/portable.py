from pathlib import Path
import re, shutil, zipfile
root=Path('outputs/NEXUS Defense')
(root/'resources').mkdir(parents=True,exist_ok=True)
html=Path('dist/index.html').read_text(encoding='utf-8').replace('href="style.css"','href="resources/style.css"').replace('src="game.js"','src="resources/game.js"')
css=Path('dist/style.css').read_text(encoding='utf-8')
css=re.sub(r"@import\s+url\([^;]+;\s*",'',css)
css=css.replace("'Noto Sans KR'", "'Malgun Gothic', 'Apple SD Gothic Neo'").replace("'IBM Plex Mono'", "'Consolas', 'Menlo'").replace('"IBM Plex Mono"', "'Consolas', 'Menlo'")
(root/'index.html').write_text(html,encoding='utf-8')
(root/'resources/style.css').write_text(css,encoding='utf-8')
shutil.copyfile('dist/game.js',root/'resources/game.js')
(root/'실행 안내.txt').write_text('''NEXUS 디펜스 — 휴대용 게임

실행 방법
1. 이 폴더 안의 index.html을 더블클릭하세요.
2. Chrome, Edge, Firefox 등의 브라우저에서 게임이 열립니다.
   코드 편집기로 열린다면 우클릭 → 연결 프로그램 → 웹 브라우저를 선택하세요.

다른 컴퓨터로 옮기기
NEXUS Defense 폴더 전체를 USB, 이메일 등으로 복사하세요.
index.html과 resources 폴더를 같은 폴더에 유지해 주세요.
설치, 인터넷 연결, 별도의 서버가 필요하지 않습니다.
글꼴은 각 컴퓨터의 기본 글꼴을 사용합니다.

조작
도구 선택 → 맵 클릭. 포탑은 위치 클릭 → 커서로 조준 → 클릭 확정.
Esc: 조준 취소 / Space: 일시정지 / 1~5: 도구 선택.
상점은 1라운드 클리어 후 준비 시간에 이용할 수 있습니다.

참고: 진행 상황은 저장되지 않습니다. 창을 닫거나 새로고침하면 새 게임입니다.
''',encoding='utf-8-sig')
assert not re.search(r'https?://|@import|url\(',css)
for ref in re.findall(r'(?:src|href)="([^"]+)"',html):
    assert (root/ref).is_file(),ref
assert (root/'resources/game.js').read_bytes()==Path('dist/game.js').read_bytes()
with zipfile.ZipFile('outputs/NEXUS-Defense.zip','w',zipfile.ZIP_DEFLATED) as z:
    for file in root.rglob('*'):
        if file.is_file():z.write(file,file.relative_to(root.parent))
print('Portable package verified: index.html, resources/game.js, resources/style.css, 실행 안내.txt. No network assets.')
