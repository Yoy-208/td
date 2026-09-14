from pathlib import Path

game = Path('dist/game.js')
source = game.read_text(encoding='utf-8')
replacements = {
    "if(tool==='core'){placeCore(id);}else if(tool==='wall'){": "if(tool==='wall'){",
    "else if(id===CORE){if(phase!=='build'){message('라운드 진행 중에는 넥서스를 제거할 수 없습니다.');return}CORE=null;refreshSpawns();dist=distances();message('넥서스를 제거했습니다. 넥서스를 다시 설치해야 라운드를 시작할 수 있습니다.');}": "else if(id===CORE){message('넥서스는 중앙에 고정되어 있어 제거할 수 없습니다.');}",
    "if(/^[1-5]$/.test(e.key))": "if(/^[1-4]$/.test(e.key))",
    "round++;phase='build';": "round++;addSpawnPoint();phase='build';",
}
for old, new in replacements.items():
    if old not in source:
        raise RuntimeError(f'missing game replacement: {old[:60]}')
    source = source.replace(old, new)
game.write_text(source, encoding='utf-8')

page = Path('dist/index.html')
html = page.read_text(encoding='utf-8')
core_button = '<button id="core-tool" class="tool" data-tool="core"><span class="icon">◇</span><span><b>넥서스 설치 / 이동</b><small>1개만 설치 · 라운드 준비 중 변경</small></span><kbd>5</kbd></button>'
if core_button not in html:
    raise RuntimeError('core tool button not found')
html = html.replace(core_button, '')
html = html.replace('생성 가능 칸', '현재 스폰 지역')
html = html.replace('적은 넥서스에서 상하좌우 기준 5칸 이상 떨어진 칸에 생성됩니다. 넥서스는 준비 중에만 설치·이동·제거할 수 있습니다.', '넥서스는 중앙에 고정됩니다. 적은 넥서스에서 상하좌우 기준 5칸 이상 떨어진 스폰 지역에서 생성되며, 라운드마다 스폰 지역이 하나씩 추가됩니다.')
page.write_text(html, encoding='utf-8')

tests = Path('work/check.cjs')
text = tests.read_text(encoding='utf-8')
start = text.index("run('const terrainReset=reset;")
end = text.index("assert.equal(run('setAngle(37.5)", start)
new_block = """run('const terrainReset=reset;reset=function(){terrainReset();obstacles.clear();obstacleGroups=[];refreshSpawnCandidates();spawns=[];addSpawnPoint();dist=distances()};reset()');
assert.equal(run('CORE===44&&spawns.length===1&&spawnCandidates.length===59'),true);
assert.equal(run('spawns.every(i=>spawnCandidates.includes(i)&&dist[i]>=5)'),true);
assert.equal(run(\"tool='remove';canvas.listeners.pointerdown({clientX:360,clientY:360});CORE===44\"),true);
assert.equal(run(\"tool='normal';canvas.listeners.pointerdown({clientX:360,clientY:360});towers.length===0&&CORE===44\"),true);
"""
text = text[:start] + new_block + text[end:]
text = text.replace("towers.length===0&&!placeCore(blocked)", "towers.length===0&&CORE===44")
text = text.replace("refreshSpawns();dist=distances();dist[45]===Infinity&&dist[46]===4&&!spawns.includes(45)", "refreshSpawnCandidates();spawns=[];addSpawnPoint();dist=distances();dist[45]===Infinity&&dist[46]===4&&!spawnCandidates.includes(45)")
text += """
assert.equal(run("reset();Array.from({length:30},()=>{enemies=[];spawn();return spawns.includes(enemies[0].cell)}).every(Boolean)"),true);
assert.equal(run("reset();let spawnHistory=[spawns[0]];Array.from({length:4},()=>{phase='active';remaining=STEP;spawnClock=Infinity;update(STEP);return spawns.length===round&&new Set(spawns).size===spawns.length&&spawnHistory.every(i=>spawns.includes(i))&&(spawnHistory=[...spawns])}).every(Boolean)&&round===5"),true);
assert.equal(run("spawns.every(i=>spawnCandidates.includes(i)&&Math.abs(i%10-CORE%10)+Math.abs(Math.floor(i/10)-Math.floor(CORE/10))>=5)"),true);
assert.ok(!fs.readFileSync('dist/index.html','utf8').includes('id="core-tool"'));
console.log('PASS: fixed central core, one persistent spawn point per round, eligible spawn distance and removed core controls.');
"""
tests.write_text(text, encoding='utf-8')
