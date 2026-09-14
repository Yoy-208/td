from pathlib import Path

game_path = Path("dist/game.js")
game = game_path.read_text(encoding="utf-8")
replacements = {
    "const ROUND_HP=[8,11,20,32,47], NORMAL_RANGE=5, NORMAL_INTERVAL=.5/1.1, ROUND_DURATION=40, SPAWN_INTERVALS=[1,.8,.4,.3,.2];":
        "const ROUND_HP=[8,11,20,32,47,65,86,110], NORMAL_RANGE=5, NORMAL_INTERVAL=.5/1.1, ROUND_DURATION=40, SPAWN_INTERVALS=[1,.8,.4,.3,.2,.18,.16,.14], MAX_ROUND=8;\nfunction roundDuration(r=round){return r>=5?60:ROUND_DURATION}",
    "price:25,repeatable:true,radarType:'speedRadar'": "price:25,repeatable:true,battle:true,radarType:'speedRadar'",
    "price:25,repeatable:true,radarType:'attackRadar'": "price:25,repeatable:true,battle:true,radarType:'attackRadar'",
    "function towerCapacity(){return 4+upgrades.towerSlots}":
        "function towerCapacity(){return 4+upgrades.towerSlots}\nfunction isRadar(t){return t.type==='speedRadar'||t.type==='attackRadar'}\nfunction placedTowerCount(){return towers.filter(t=>!isRadar(t)).length}",
    "Math.ceil(ROUND_DURATION/interval*difficulty.count)": "Math.ceil(roundDuration(i+1)/interval*difficulty.count)",
    "remaining=ROUND_DURATION;phase='build'": "remaining=roundDuration(1);phase='build'",
    "$('round').innerHTML=`0${round} <em>/ 05</em>`": "$('round').innerHTML=`${String(round).padStart(2,'0')} <em>/ ${String(MAX_ROUND).padStart(2,'0')}</em>`",
    "$('capacity').textContent=`${towers.length} / ${cap}`": "$('capacity').textContent=`${placedTowerCount()} / ${cap} · 레이더 ${towers.length-placedTowerCount()}`",
    "`스폰 지역 ${spawns.length}개 · 포탑 ${cap}개 배치 가능.<br>준비가 되면 라운드를 시작하세요.`": "`스폰 지역 ${spawns.length}개 · 공격 포탑 ${cap}개 배치 가능 · 레이더는 별도.<br>준비가 되면 라운드를 시작하세요.`",
    "remaining=ROUND_DURATION;spawnClock=0": "remaining=roundDuration(round);spawnClock=0",
    "`5개 라운드 클리어 · 이번 라운드 ${roundKills}마리 · 총 ${kills}마리 처치`": "`${MAX_ROUND}개 라운드 클리어 · 이번 라운드 ${roundKills}마리 · 총 ${kills}마리 처치`",
    "else if(towers.length>=towerCapacity())": "else if(!isRadar({type:tool})&&placedTowerCount()>=towerCapacity())",
    "if(round===5)end(true)": "if(round===MAX_ROUND)end(true)",
    "phase='build';remaining=ROUND_DURATION;rollShop()": "phase='build';remaining=roundDuration(round);rollShop()",
    "phase==='active'?'배치 한도만 구매 가능'": "phase==='active'?'배치 한도·레이더 구매 가능'",
}
for old, new in replacements.items():
    if old not in game:
        raise RuntimeError(f"game pattern missing: {old}")
    game = game.replace(old, new)
game_path.write_text(game, encoding="utf-8")

html_path = Path("dist/index.html")
html = html_path.read_text(encoding="utf-8")
html = html.replace("5 ROUNDS · ONE CORE", "8 ROUNDS · ONE CORE")
html = html.replace("01 <em>/ 05</em>", "01 <em>/ 08</em>")
html = html.replace("넥서스를 40초 동안 지키세요", "1~4R 40초 · 5~8R 60초")
html = html.replace("공속·공격 레이더는 준비 시간에 각 25원으로 횟수 제한 없이 구매할 수 있습니다.", "공속·공격 레이더는 준비 시간과 전투 중에 각 25원으로 횟수 제한 없이 구매할 수 있습니다.")
html = html.replace("레이더는 범위 3칸 안의 일반·뱅크샷 포탑을 강화하며", "레이더는 공격 포탑 배치 한도를 사용하지 않고, 범위 3칸 안의 일반·뱅크샷 포탑을 강화하며")
html = html.replace("20260914-radar3", "20260914-round8")
html_path.write_text(html, encoding="utf-8")
