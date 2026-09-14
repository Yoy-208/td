from pathlib import Path

game = Path('dist/game.js')
source = game.read_text(encoding='utf-8')

old = " {key:'towerSlots',name:'타워 배치 횟수',effect:'배치 한도 +1 · 횟수 제한 없음',price:50,repeatable:true}"
new = """ {key:'towerSlots',name:'타워 배치 횟수',effect:'배치 한도 +1 · 횟수 제한 없음',price:30,repeatable:true,battle:true},
 {key:'speedRadar',name:'공속 레이더',effect:'범위 4칸 · 포탑 공격속도 +30%',price:40,repeatable:true,radarType:'speedRadar'},
 {key:'attackRadar',name:'공격 레이더',effect:'범위 4칸 · 포탑 공격력 +2',price:40,repeatable:true,radarType:'attackRadar'}"""
if old not in source:
    raise RuntimeError('shop item anchor missing')
source = source.replace(old, new)

source = source.replace(
    "let money=10,upgrades={},shopOffers=[],shopPurchased=new Set(),shopSignature='';",
    "let money=10,upgrades={},radarStock={speedRadar:0,attackRadar:0},shopOffers=[],shopPurchased=new Set(),shopSignature='';"
)

old = "function buyItem(index){const item=SHOP_ITEMS[index];if(!item||round<2||!['build','active'].includes(phase)||(!item.repeatable&&(phase!=='build'||!shopOffers.includes(index)||shopPurchased.has(index))))return false;if(money<item.price){message('돈이 부족합니다. 적을 처치하면 1원을 얻습니다.');return false}money-=item.price;if(!item.repeatable)shopPurchased.add(index);upgrades[item.key]++;message(item.repeatable?`배치 한도가 ${towerCapacity()}대로 늘어났습니다.`:`${item.name} ${item.effect} 구매 완료! 모든 해당 포탑에 누적 적용됩니다.`);ui();return true}"
new = "function canBuyItem(index){const item=SHOP_ITEMS[index];if(!item||round<2)return false;if(item.repeatable)return phase==='build'||(phase==='active'&&item.battle);return phase==='build'&&shopOffers.includes(index)&&!shopPurchased.has(index)}\nfunction buyItem(index){const item=SHOP_ITEMS[index];if(!canBuyItem(index))return false;if(money<item.price){message('돈이 부족합니다. 적을 처치하면 1원을 얻습니다.');return false}money-=item.price;if(!item.repeatable)shopPurchased.add(index);if(item.radarType)radarStock[item.radarType]++;else upgrades[item.key]++;message(item.radarType?`${item.name} 구매 완료! 배치 도구에서 설치하세요.`:item.repeatable?`배치 한도가 ${towerCapacity()}대로 늘어났습니다.`:`${item.name} ${item.effect} 구매 완료! 모든 해당 포탑에 누적 적용됩니다.`);ui();return true}"
if old not in source:
    raise RuntimeError('buy function anchor missing')
source = source.replace(old, new)

old = "function shopUI(){const stats=weaponStats();$('money').textContent=`${money}원`;const signature=JSON.stringify([money,phase,round,shopOffers,upgrades,[...shopPurchased]]);if(signature===shopSignature)return;shopSignature=signature;const open=phase==='build'&&round>=2;$('shop-state').textContent=round===1?'1라운드 클리어 후 개방':open?'준비 시간 · 구매 가능':phase==='active'?'배치 한도만 구매 가능':'상점 이용 종료';$('shop-items').innerHTML=[...shopOffers,6].map(i=>{const item=SHOP_ITEMS[i];return `<button class=\"shop-item\" data-buy=\"${i}\" ${!(open||(item.repeatable&&round>=2&&phase==='active'))||money<item.price||shopPurchased.has(i)?'disabled':''}><span><b>${item.name}</b><small>${item.effect}</small></span><strong>${shopPurchased.has(i)?'구매 완료':`${item.price}원`}</strong></button>`}).join('');$('shop-placeholder').hidden=shopOffers.length>0;$('weapon-stats').innerHTML=`<span>일반: 피해 ${stats.normalDamage} · ${stats.normalShots}발 · 치명타 ${Math.round(stats.normalCrit*100)}% · 사거리 5칸</span><span>뱅크샷: 피해 ${stats.bankDamage} · 수명 ${stats.bankLife}초 · ${Number(stats.bankInterval.toFixed(2))}초 간격</span>`;$('normal-desc').textContent=`${stats.normalDamage} 피해 · 0.455초 간격 · ${stats.normalShots}발 · 사거리 5칸`;$('bank-desc').textContent=`${stats.bankDamage} 피해 · ${Number(stats.bankInterval.toFixed(2))}초 간격 · 수명 ${stats.bankLife}초`}"
new = "function shopUI(){const stats=weaponStats();$('money').textContent=`${money}원`;$('speed-radar-stock').textContent=`보유 ${radarStock.speedRadar}`;$('attack-radar-stock').textContent=`보유 ${radarStock.attackRadar}`;const signature=JSON.stringify([money,phase,round,shopOffers,upgrades,radarStock,[...shopPurchased]]);if(signature===shopSignature)return;shopSignature=signature;const open=phase==='build'&&round>=2;$('shop-state').textContent=round===1?'1라운드 클리어 후 개방':open?'준비 시간 · 모든 상품 구매 가능':phase==='active'?'배치 한도만 구매 가능':'상점 이용 종료';$('shop-items').innerHTML=[...shopOffers,6,7,8].map(i=>{const item=SHOP_ITEMS[i],available=canBuyItem(i);return `<button class=\"shop-item\" data-buy=\"${i}\" ${!available||money<item.price?'disabled':''}><span><b>${item.name}</b><small>${item.effect}</small></span><strong>${shopPurchased.has(i)?'구매 완료':`${item.price}원`}</strong></button>`}).join('');$('shop-placeholder').hidden=shopOffers.length>0;$('weapon-stats').innerHTML=`<span>일반: 피해 ${stats.normalDamage} · ${stats.normalShots}발 · 치명타 ${Math.round(stats.normalCrit*100)}% · 사거리 5칸</span><span>뱅크샷: 피해 ${stats.bankDamage} · 수명 ${stats.bankLife}초 · ${Number(stats.bankInterval.toFixed(2))}초 간격</span><span>레이더: 범위 4칸 · 중첩 적용</span>`;$('normal-desc').textContent=`${stats.normalDamage} 피해 · 0.455초 간격 · ${stats.normalShots}발 · 사거리 5칸`;$('bank-desc').textContent=`${stats.bankDamage} 피해 · ${Number(stats.bankInterval.toFixed(2))}초 간격 · 수명 ${stats.bankLife}초`}"
if old not in source:
    raise RuntimeError('shop UI anchor missing')
source = source.replace(old, new)

source = source.replace(
    "function reset(){pendingAim=null;money=10;",
    "function reset(){pendingAim=null;money=10;radarStock={speedRadar:0,attackRadar:0};"
)

old = "else{const n=towers.length;towers=towers.filter(t=>t.cell!==id);message(n===towers.length?'제거할 포탑이나 벽을 클릭하세요.':'포탑을 제거했습니다. 설치 수가 반환되었습니다.')}"
new = "else{const removed=towers.find(t=>t.cell===id),n=towers.length;if(removed&&(removed.type==='speedRadar'||removed.type==='attackRadar'))radarStock[removed.type]++;towers=towers.filter(t=>t.cell!==id);message(n===towers.length?'제거할 포탑이나 벽을 클릭하세요.':'포탑을 제거했습니다. 설치 수가 반환되었습니다.')}"
if old not in source:
    raise RuntimeError('remove tower anchor missing')
source = source.replace(old, new)

old = "if(t){if(t.type==='bank'){pendingAim={...t,existing:t};message('커서로 조준한 뒤 클릭하세요. Esc로 취소합니다.');}else message('일반 포탑은 적을 자동 조준합니다.');}else if(towers.length>=towerCapacity())"
new = "if(t){if(t.type==='bank'){pendingAim={...t,existing:t};message('커서로 조준한 뒤 클릭하세요. Esc로 취소합니다.');}else if(t.type==='speedRadar'||t.type==='attackRadar')message('레이더는 범위 4칸 안의 공격 포탑을 강화합니다.');else message('일반 포탑은 적을 자동 조준합니다.');}else if(towers.length>=towerCapacity())"
if old not in source:
    raise RuntimeError('existing tower anchor missing')
source = source.replace(old, new)

old = "else{if(tool==='bank'){pendingAim={cell:id,...center(id),type:tool,angle};message('커서로 조준한 뒤 클릭해 설치를 확정하세요.');}else{towers.push({cell:id,...center(id),type:tool,angle,cool:0});message('포탑을 설치했습니다.');}}"
new = "else{if(tool==='bank'){pendingAim={cell:id,...center(id),type:tool,angle};message('커서로 조준한 뒤 클릭해 설치를 확정하세요.');}else if(tool==='speedRadar'||tool==='attackRadar'){if(radarStock[tool]<=0){message('상점에서 레이더를 먼저 구매하세요.');return}radarStock[tool]--;towers.push({cell:id,...center(id),type:tool,cool:0});message('레이더를 설치했습니다. 범위 4칸 안의 포탑이 강화됩니다.');}else{towers.push({cell:id,...center(id),type:tool,angle,cool:0});message('포탑을 설치했습니다.');}}"
if old not in source:
    raise RuntimeError('place tower anchor missing')
source = source.replace(old, new)

source = source.replace(
    "function fireTower(t){",
    "function radarBonuses(t){let speedCount=0,attackCount=0;for(const radar of towers){if(Math.hypot(radar.x-t.x,radar.y-t.y)>4)continue;if(radar.type==='speedRadar')speedCount++;if(radar.type==='attackRadar')attackCount++}return {speed:Math.pow(1.3,speedCount),damage:attackCount*2}}\nfunction fireTower(t){"
)
source = source.replace(
    "function fireTower(t){const stats=weaponStats(),bank=t.type==='bank',count=bank?1:stats.normalShots;",
    "function fireTower(t){const stats=weaponStats(),bank=t.type==='bank',count=bank?1:stats.normalShots,radar=radarBonuses(t);"
)
source = source.replace(
    "damage:bank?stats.bankDamage:stats.normalDamage*(critical?2:1)",
    "damage:(bank?stats.bankDamage:stats.normalDamage*(critical?2:1))+radar.damage"
)

old = "for(const t of towers){t.cool-=dt;const target=t.type==='normal'?selectTarget(t):null;if(target)t.angle=Math.atan2(target.y-t.y,target.x-t.x);if(t.cool<=0){if(t.type==='bank'||target){t.cool+=t.type==='bank'?weaponStats().bankInterval:NORMAL_INTERVAL;fireTower(t)}else t.cool=0}}"
new = "for(const t of towers){if(t.type==='speedRadar'||t.type==='attackRadar')continue;t.cool-=dt;const target=t.type==='normal'?selectTarget(t):null;if(target)t.angle=Math.atan2(target.y-t.y,target.x-t.x);if(t.cool<=0){if(t.type==='bank'||target){const radar=radarBonuses(t);t.cool+=(t.type==='bank'?weaponStats().bankInterval:NORMAL_INTERVAL)/radar.speed;fireTower(t)}else t.cool=0}}"
if old not in source:
    raise RuntimeError('update tower anchor missing')
source = source.replace(old, new)

source = source.replace(
    "if(/^[1-4]$/.test(e.key))",
    "if(/^[1-6]$/.test(e.key))"
)

old = "if(CORE!==null){const c=center(CORE),pulse="
source = source.replace(old, "if(CORE!==null){const c=center(CORE),pulse=")

old = "for(const t of towers){ctx.save();ctx.translate(t.x*s,t.y*s);ctx.rotate(t.angle);ctx.fillStyle=t.type==='bank'?'#66482d':'#245354';ctx.strokeStyle=t.type==='bank'?'#ffc16b':'#6de6db';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,18,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle=t.type==='bank'?'#ffc16b':'#6de6db';ctx.fillRect(0,-5,27,10);ctx.fillStyle='#d5e9ed';ctx.beginPath();ctx.arc(0,0,5,0,Math.PI*2);ctx.fill();ctx.restore()}"
new = "for(const radar of towers.filter(t=>t.type==='speedRadar'||t.type==='attackRadar')){ctx.save();ctx.globalAlpha=.08;ctx.fillStyle=radar.type==='speedRadar'?'#9d8cff':'#ff8c75';ctx.beginPath();ctx.arc(radar.x*s,radar.y*s,4*s,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.32;ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=2;ctx.stroke();ctx.restore()}for(const t of towers){ctx.save();ctx.translate(t.x*s,t.y*s);if(t.type==='speedRadar'||t.type==='attackRadar'){const speed=t.type==='speedRadar';ctx.fillStyle=speed?'#282852':'#542d2d';ctx.strokeStyle=speed?'#9d8cff':'#ff8c75';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,18,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.beginPath();ctx.arc(0,0,10,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.moveTo(-13,0);ctx.lineTo(13,0);ctx.moveTo(0,-13);ctx.lineTo(0,13);ctx.stroke();ctx.restore();continue}ctx.rotate(t.angle);ctx.fillStyle=t.type==='bank'?'#66482d':'#245354';ctx.strokeStyle=t.type==='bank'?'#ffc16b':'#6de6db';ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,18,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.fillStyle=t.type==='bank'?'#ffc16b':'#6de6db';ctx.fillRect(0,-5,27,10);ctx.fillStyle='#d5e9ed';ctx.beginPath();ctx.arc(0,0,5,0,Math.PI*2);ctx.fill();ctx.restore()}"
if old not in source:
    raise RuntimeError('draw tower anchor missing')
source = source.replace(old, new)

game.write_text(source, encoding='utf-8')

page = Path('dist/index.html')
html = page.read_text(encoding='utf-8')
anchor = '<button class="tool" data-tool="remove"><span class="icon">×</span><span><b>제거</b><small>포탑 또는 벽을 클릭</small></span><kbd>4</kbd></button>'
radar_buttons = anchor + '<button class="tool" data-tool="speedRadar"><span class="icon radar-speed">◎</span><span><b>공속 레이더</b><small>범위 4칸 · 공속 +30% · <i id="speed-radar-stock">보유 0</i></small></span><kbd>5</kbd></button><button class="tool" data-tool="attackRadar"><span class="icon radar-attack">⊕</span><span><b>공격 레이더</b><small>범위 4칸 · 공격력 +2 · <i id="attack-radar-stock">보유 0</i></small></span><kbd>6</kbd></button>'
if anchor not in html:
    raise RuntimeError('tool button anchor missing')
html = html.replace(anchor, radar_buttons)
html = html.replace('배치 한도 +1은 50원', '배치 한도 +1은 30원')
html = html.replace('2라운드부터 전투 중에도 구매할 수 있습니다.', '2라운드부터 전투 중에도 구매할 수 있습니다. 공속·공격 레이더는 준비 시간에 각 40원으로 횟수 제한 없이 구매할 수 있습니다.')
html = html.replace('뱅크샷 탄환은 벽에서 반사되고 적을 관통하며 기본 지속시간은 4초입니다.', '뱅크샷 탄환은 벽에서 반사되고 적을 관통하며 기본 지속시간은 4초입니다. 레이더는 범위 4칸 안의 일반·뱅크샷 포탑을 강화하며 여러 레이더의 효과는 누적됩니다.')
page.write_text(html, encoding='utf-8')

styles = Path('dist/style.css')
css = styles.read_text(encoding='utf-8')
css += "\n.radar-speed{color:#9d8cff}.radar-attack{color:#ff8c75}.tool small i{font-style:normal;color:#eef3f9}\n"
styles.write_text(css, encoding='utf-8')

portable = Path('work/portable.py')
portable_text = portable.read_text(encoding='utf-8')
portable_text = portable_text.replace('상점은 1라운드 클리어 후 준비 시간에 이용할 수 있습니다.', '상점은 1라운드 클리어 후 준비 시간에 이용할 수 있습니다. 구매한 레이더는 배치 도구로 설치합니다.')
portable.write_text(portable_text, encoding='utf-8')
