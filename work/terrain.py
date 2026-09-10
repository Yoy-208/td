from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace('let spawns=[];', '''let spawns=[],obstacles=new Set(),obstacleGroups=[];
function adjacentCells(id){return dirs.map(([dx,dy])=>[id%10+dx,Math.floor(id/10)+dy]).filter(([x,y])=>x>=0&&x<10&&y>=0&&y<10).map(([x,y])=>y*10+x)}
function generateTerrain(){const previous=[...obstacles].sort((a,b)=>a-b).join(',');for(let attempt=0;attempt<100;attempt++){obstacles=new Set();obstacleGroups=[];const count=1+Math.floor(Math.random()*2);for(let group=0;group<count;group++){const length=1+Math.floor(Math.random()*3),candidates=[];for(let id=0;id<100;id++)for(const vertical of [false,true]){const cells=Array.from({length},(_,i)=>id+i*(vertical?10:1));if(cells.some(c=>c>=100||(!vertical&&Math.floor(c/10)!==Math.floor(id/10))||c===44||obstacles.has(c)||adjacentCells(c).some(n=>obstacles.has(n))))continue;for(const c of cells)obstacles.add(c);const valid=distances().every((d,i)=>obstacles.has(i)||Number.isFinite(d));for(const c of cells)obstacles.delete(c);if(valid)candidates.push(cells)}const chosen=candidates[Math.floor(Math.random()*candidates.length)];if(chosen){obstacleGroups.push(chosen);chosen.forEach(c=>obstacles.add(c))}}if([...obstacles].sort((a,b)=>a-b).join(',')!==previous)break}}
''')
s=s.replace('.filter(i=>Math.abs(i%10-CORE%10)', '.filter(i=>!obstacles.has(i)&&Math.abs(i%10-CORE%10)')
s=s.replace("function placeCore(id){if(phase", "function placeCore(id){if(obstacles.has(id)){message('장애물 위에는 넥서스를 설치할 수 없습니다.');return false}if(phase")
s=s.replace('!walls.has(edge(a,b))&&d[b]', '!obstacles.has(b)&&!walls.has(edge(a,b))&&d[b]')
s=s.replace('!walls.has(edge(a,b))&&dist[b]', '!obstacles.has(b)&&!walls.has(edge(a,b))&&dist[b]')
s=s.replace('CORE=44;refreshSpawns();walls=new Map();', 'CORE=44;walls=new Map();generateTerrain();refreshSpawns();')
s=s.replace('d.some(v=>!Number.isFinite(v))', 'd.some((v,i)=>!obstacles.has(i)&&!Number.isFinite(v))')
s=s.replace("}else{if(id===CORE){message('넥서스 위에는", "}else{if(obstacles.has(id)){message('장애물 위에는 포탑을 설치할 수 없습니다.');return}if(id===CORE){message('넥서스 위에는")
needle="if(spawns.includes(id)){ctx.fillStyle='#87616b';ctx.fillRect(x+12,y+12,4,4)}"
assert needle in s
s=s.replace(needle,needle+"if(obstacles.has(id)){ctx.fillStyle='#3c4653';ctx.fillRect(x+5,y+5,s-10,s-10);ctx.strokeStyle='#87929e';ctx.lineWidth=2;ctx.strokeRect(x+8,y+8,s-16,s-16);ctx.save();ctx.beginPath();ctx.rect(x+10,y+10,s-20,s-20);ctx.clip();ctx.strokeStyle='#596574';ctx.lineWidth=3;for(let h=-s;h<s*2;h+=16){ctx.beginPath();ctx.moveTo(x+h,y+10);ctx.lineTo(x+h+s,y+s-10);ctx.stroke()}ctx.restore()}")
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('<span><i class="red"></i> 적</span>', '<span><i class="red"></i> 적</span><span><i style="background:#87929e"></i> 장애물</span>').replace('모든 경로를 막는 벽은 설치할 수 없습니다.', '빗금 표시 장애물은 새 게임마다 생성되며 적 이동과 포탑 설치를 막습니다. 라운드 사이에는 유지됩니다. 모든 경로를 막는 벽은 설치할 수 없습니다.');p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8').replace("const run=s=>vm.runInContext(s,sandbox);", "const run=s=>vm.runInContext(s,sandbox);\nrun('const terrainReset=reset;reset=function(){terrainReset();obstacles.clear();obstacleGroups=[];refreshSpawns();dist=distances()};reset()');")
s+='''
assert.equal(run('Array.from({length:30},()=>{terrainReset();return obstacleGroups.length>=1&&obstacleGroups.length<=2&&obstacleGroups.every(g=>g.length>=1&&g.length<=3)&&!obstacles.has(CORE)&&dist.every((d,i)=>obstacles.has(i)||Number.isFinite(d))&&spawns.every(i=>!obstacles.has(i))}).every(Boolean)'),true);
assert.equal(run("let blocked=[...obstacles][0];tool='normal';canvas.listeners.pointerdown({clientX:(blocked%10+.5)*80,clientY:(Math.floor(blocked/10)+.5)*80});towers.length===0&&pendingAim===null&&!placeCore(blocked)"),true);
assert.equal(run("let terrainSignature=[...obstacles].join(',');start();remaining=STEP;spawnClock=Infinity;update(STEP);[...obstacles].join(',')===terrainSignature"),true);
assert.equal(run("terrainReset();[...obstacles].join(',')!==terrainSignature"),true);
assert.equal(run("reset();obstacles=new Set([45]);refreshSpawns();dist=distances();dist[45]===Infinity&&dist[46]===4&&!spawns.includes(45)"),true);
console.log('PASS: random terrain size, connected map, placement and spawn exclusion, round persistence, new-game changes and detour.');
''';p.write_text(s,encoding='utf-8')
