from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace('let CORE=44;', 'const ROUND_HP=[8,11,20,32,47], NORMAL_RANGE=5;\nlet CORE=44;')
s=s.replace('8+(round-1)*3', 'ROUND_HP[round-1]').replace('health=8+3*(round-1)', 'health=ROUND_HP[round-1]')
s=s.replace('6-(b.traveled??0)', 'NORMAL_RANGE-(b.traveled??0)').replace('b.traveled>=6-1e-9', 'b.traveled>=NORMAL_RANGE-1e-9').replace("a.type==='normal'?6:12", "a.type==='normal'?NORMAL_RANGE:12")
s=s.replace('Math.cos(angle)*12', "Math.cos(angle)*(tool==='normal'?NORMAL_RANGE:12)").replace('Math.sin(angle)*12', "Math.sin(angle)*(tool==='normal'?NORMAL_RANGE:12)")
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('6칸','5칸');p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8').replace('moveBullet(ranged,.99)', 'moveBullet(ranged,.8)').replace('moveBullet(ranged,.01)', 'moveBullet(ranged,1/30)').replace('ranged.x-7','ranged.x-6').replace('x:7.3,y:1','x:6.3,y:1').replace('six-cell range','five-cell range')
s+="\nassert.equal(run('reset();[8,11,20,32,47].every((expected,i)=>{round=i+1;enemies=[];spawn();ui();return enemies[0].hp===expected&&enemies[0].max===expected&&$(\"enemy-hp\").textContent===`적 HP ${expected}`})'),true);\nconsole.log('PASS: all five round HP values and displayed HP.');\n"
p.write_text(s,encoding='utf-8')
