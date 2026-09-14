from pathlib import Path
import re
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=re.sub(r'^function (?:aimAt|confirmAim)\([^\n]+\n','',s,flags=re.M)
s=s.replace(';aimAt(hover)','').replace('if(pendingAim){confirmAim(p);return}','')
s=s.replace("pendingAim={...t,existing:t};setAngle(t.angle*180/Math.PI);message('커서로 방향을 잡고 클릭으로 확정하세요. Esc로 취소합니다.');", "if(t.type==='bank'){t.angle=angle;message('뱅크샷 발사 방향을 변경했습니다.');}else message('일반 포탑은 적을 자동 조준합니다.');")
s=s.replace("pendingAim={cell:id,...center(id),type:tool,angle};message('위치 선택 완료. 커서로 방향을 잡고 다시 클릭하세요. Esc로 취소합니다.')", "towers.push({cell:id,...center(id),type:tool,angle,cool:0});message('포탑을 설치했습니다.')")
s=re.sub(r"if\(pendingAim\)\{const a=pendingAim;.*?return;\}if\(hover&&phase", 'if(hover&&phase',s)
s=s.replace(",pendingAim=null",'').replace('pendingAim=null;','').replace('||pendingAim!==null','').replace('if(pendingAim)pendingAim.angle=angle;','')
s=re.sub(r"if\(e.key==='Escape'&&pendingAim\)\{.*?return;\}",'',s)
s=s.replace('준비 시간에 상점에서 한도를 늘릴 수 있습니다.', '상점에서 한도를 늘릴 수 있습니다.')
assert 'pendingAim' not in s
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('포탑 위치 클릭 → 커서 조준 → 클릭 확정', '도구 선택 → 위치 클릭으로 바로 설치').replace('발사 방향 <span', '뱅크샷 발사 방향 <span')
s=re.sub(r'<p class="hint">.*?</p>', '<p class="hint">포탑은 칸을 한 번 클릭하면 설치됩니다.<br>일반 포탑은 자동 조준합니다.<br>뱅크샷은 방향 버튼·각도로 설정하세요. 설치된 뱅크샷을 클릭하면 선택한 방향으로 바뀝니다.</p>',s)
p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8')
a=s.index('assert.equal(run("reset();tool=\'normal\';canvas.listeners.pointerdown({clientX:120,clientY:120});towers.length===0')
b=s.index('assert.equal(run("reset();let ranged=',a)
s=s[:a]+'''assert.equal(run("reset();tool='normal';canvas.listeners.pointerdown({clientX:120,clientY:120});towers.length===1&&towers[0].cell===11"),true);
assert.equal(run("start();phase==='active'"),true);
assert.equal(run("reset();setAngle(45);tool='bank';canvas.listeners.pointerdown({clientX:120,clientY:120});canvas.listeners.pointermove({clientX:300,clientY:500});towers.length===1&&Math.abs(towers[0].angle-Math.PI/4)<1e-10"),true);
assert.equal(run("setAngle(180);canvas.listeners.pointerdown({clientX:120,clientY:120});towers.length===1&&Math.abs(towers[0].angle-Math.PI)<1e-10"),true);
'''+s[b:]
s=s.replace('&&pendingAim===null','').replace('two-click placement and re-aim','single-click placement and fixed bank direction')
p.write_text(s,encoding='utf-8')
p=Path('work/portable.py');s=p.read_text(encoding='utf-8').replace('포탑은 위치 클릭 → 커서로 조준 → 클릭 확정.', '포탑은 위치를 한 번 클릭하면 설치됩니다. 일반 포탑은 자동 조준하며 뱅크샷은 방향 버튼이나 각도로 설정합니다.').replace('Esc: 조준 취소 / Space:', 'Space:');p.write_text(s,encoding='utf-8')
