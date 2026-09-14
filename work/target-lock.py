from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace('NORMAL_RANGE=5,', 'NORMAL_RANGE=5, NORMAL_INTERVAL=.5/1.1,')
s=s.replace("b.type==='bank'?.21*1.2:.21", '.21*1.2')
s=s.replace("weaponStats().bankInterval:.5", "weaponStats().bankInterval:NORMAL_INTERVAL")
s=s.replace('const core=center(CORE);return enemies.filter', "const locked=enemies.find(e=>e.id===t.targetId&&e.hp>0);if(locked)return Math.hypot(locked.x-t.x,locked.y-t.y)<=NORMAL_RANGE?locked:null;const core=center(CORE);const target=enemies.filter")
s=s.replace('||a.id-b.id)[0]??null}', '||a.id-b.id)[0]??null;t.targetId=target?.id??null;return target}')
s=s.replace('towers.forEach(t=>t.cool=0)', 'towers.forEach(t=>{t.cool=0;t.targetId=null})')
s=s.replace('피해 · 자동 조준 · ${stats.normalShots}발', '피해 · 0.455초 간격 · ${stats.normalShots}발')
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('0.5초 간격','0.455초 간격').replace('일반 포탑은 사거리 5칸 안에서 넥서스에 가장 가까운 적을 자동 조준합니다.', '일반 포탑은 사거리 5칸 안에서 넥서스에 가장 가까운 적을 고르고, 해당 적이 처치되거나 사라질 때까지 조준을 유지합니다. 대상이 사거리 밖에 있으면 발사를 멈춥니다.');p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8')
s=s.replace("enemies[0].hp=8;moveBullet({x:1,y:1,vx:6,vy:0,type:'normal',contacts:new Set()},.1);enemies[0].hp===8", "enemies[0].hp=8;moveBullet({x:1,y:1,vx:6,vy:0,type:'normal',contacts:new Set()},.1);enemies[0].hp===5")
s=s.replace('enemies[0].y=1.26;moveBullet', 'enemies[0].hp=8;enemies[0].y=1.26;moveBullet')
s=s.replace('normal unchanged.', 'normal hit radius also increased 20%.')
s+='''
assert.equal(run("reset();let lockTower={x:2,y:2,type:'normal',cool:0};enemies=[{id:101,x:3,y:3,hp:8},{id:102,x:1,y:2,hp:8}];selectTarget(lockTower).id===101"),true);
assert.equal(run("enemies[1].x=4.5;enemies[1].y=4.5;selectTarget(lockTower).id===101"),true);
assert.equal(run("enemies[0].x=9;enemies[0].y=9;selectTarget(lockTower)===null&&lockTower.targetId===101"),true);
assert.equal(run("enemies[0].x=3;enemies[0].y=3;selectTarget(lockTower).id===101"),true);
assert.equal(run("enemies[0].hp=0;selectTarget(lockTower).id===102"),true);
assert.equal(run("enemies=[];selectTarget(lockTower)===null&&lockTower.targetId===null"),true);
assert.equal(run("reset();start();spawnClock=Infinity;towers=[{x:2,y:2,type:'normal',cool:0}];enemies=[{id:10,cell:33,to:null,x:3.5,y:3.5,hp:8}];update(STEP);Math.abs(towers[0].cool-(.5/1.1-STEP))<1e-10"),true);
assert.equal(run("reset();enemies=[{id:1,x:1.3,y:1.26,hp:8}];moveBullet({x:1,y:1,vx:6,vy:0,type:'normal',contacts:new Set()},.1);enemies[0].hp===8"),true);
console.log('PASS: 10% normal fire rate increase, target lock until death/removal, range hold and enlarged hit boundary.');
''';p.write_text(s,encoding='utf-8')
