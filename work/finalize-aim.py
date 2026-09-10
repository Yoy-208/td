from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
old="if(t){t.angle=angle;message('포탑의 발사 방향을 변경했습니다.')}"
assert old in s
s=s.replace(old,"if(t){pendingAim={...t,existing:t};setAngle(t.angle*180/Math.PI);message('커서로 방향을 잡고 클릭으로 확정하세요. Esc로 취소합니다.');}")
old="towers.push({cell:id,...center(id),type:tool,angle,cool:0});message('포탑 설치 완료. 선택한 방향으로 자동 발사합니다.')"
assert old in s
s=s.replace(old,"pendingAim={cell:id,...center(id),type:tool,angle};message('위치 선택 완료. 커서로 방향을 잡고 다시 클릭하세요. Esc로 취소합니다.')")
p.write_text(s,encoding='utf-8')
