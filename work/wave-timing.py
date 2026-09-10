from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace('NORMAL_RANGE=5;', 'NORMAL_RANGE=5, ROUND_DURATION=40, SPAWN_INTERVALS=[1,.8,.6,.45,.3];')
s=s.replace('remaining=60', 'remaining=ROUND_DURATION')
s=s.replace('if(spawnClock<=0){spawn();spawnClock=(2.5-(round-1)*.27)/1.3}', 'if(spawnClock<=0&&remaining>1e-9){spawn();spawnClock+=SPAWN_INTERVALS[round-1]}')
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('id="time">60<', 'id="time">40<').replace('60초 동안', '40초 동안');p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8').replace('update(1);remaining"),60)', 'update(1);remaining"),40)').replace('i<7201', 'i<4801')
s=s.replace('Math.abs(spawnClock-(2.5-i*.27)/1.3)<1e-10', 'Math.abs(spawnClock-([1,.8,.6,.45,.3][i]-STEP))<1e-10').replace('1.3x spawn rate', 'increasing per-round spawn rates')
s+='''
const waveCounts=run('Array.from({length:5},(_,i)=>{reset();round=i+1;start();for(let n=0;n<4800;n++){enemies=[];update(STEP)}return nextId})');
assert.ok(waveCounts.every((count,i)=>Math.abs(count-[40,50,67,89,134][i])<=1));
assert.ok(waveCounts.every((count,i)=>i===0||count>waveCounts[i-1]));
assert.equal(run("reset();start();spawnClock=Infinity;for(let n=0;n<4799;n++)update(STEP);phase==='active'"),true);
assert.equal(run("update(STEP);phase==='build'&&round===2&&remaining===40"),true);
console.log('PASS: 40-second duration and increasing enemy totals:',Array.from(waveCounts));
''';p.write_text(s,encoding='utf-8')
