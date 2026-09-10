from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace('let CORE=44;', '''const SHOP_ITEMS=[
 {key:'bankLife',name:'뱅크샷 · 탄환 지속시간',effect:'+1초',price:15},
 {key:'bankDamage',name:'뱅크샷 · 탄환 피해량',effect:'+1 피해',price:10},
 {key:'bankSpeed',name:'뱅크샷 · 공격속도',effect:'+20% (누적 곱연산)',price:10},
 {key:'normalDamage',name:'일반 포탑 · 공격력',effect:'+1 피해',price:10},
 {key:'normalShots',name:'일반 포탑 · 추가 탄환',effect:'한 번에 +1발',price:15},
 {key:'normalCrit',name:'일반 포탑 · 치명타율',effect:'+10%p · 피해 2배 (최대 100%)',price:10}
];
let money=10,upgrades={},shopOffers=[],shopSignature='';
function weaponStats(){return {bankLife:4+upgrades.bankLife,bankDamage:1+upgrades.bankDamage,bankInterval:3/Math.pow(1.2,upgrades.bankSpeed),normalDamage:3+upgrades.normalDamage,normalShots:1+upgrades.normalShots,normalCrit:Math.min(1,upgrades.normalCrit*.1)}}
function rollShop(){const pool=SHOP_ITEMS.map((_,i)=>i);shopOffers=[];for(let n=0;n<2;n++)shopOffers.push(pool.splice(Math.floor(Math.random()*pool.length),1)[0]);shopSignature=''}
function buyItem(index){if(phase!=='build'||round<2||!shopOffers.includes(index))return false;const item=SHOP_ITEMS[index];if(money<item.price){message('돈이 부족합니다. 적을 처치하면 1원을 얻습니다.');return false}money-=item.price;upgrades[item.key]++;message(`${item.name} ${item.effect} 구매 완료! 모든 해당 포탑에 누적 적용됩니다.`);ui();return true}
function shopUI(){const stats=weaponStats();$('money').textContent=`${money}원`;const signature=JSON.stringify([money,phase,round,shopOffers,upgrades]);if(signature===shopSignature)return;shopSignature=signature;const open=phase==='build'&&round>=2;$('shop-state').textContent=round===1?'1라운드 클리어 후 개방':open?'준비 시간 · 구매 가능':'전투 중 구매 불가';$('shop-items').innerHTML=shopOffers.map(i=>{const item=SHOP_ITEMS[i];return `<button class="shop-item" data-buy="${i}" ${!open||money<item.price?'disabled':''}><span><b>${item.name}</b><small>${item.effect}</small></span><strong>${item.price}원</strong></button>`}).join('');$('shop-placeholder').hidden=shopOffers.length>0;$('weapon-stats').innerHTML=`<span>일반: 피해 ${stats.normalDamage} · ${stats.normalShots}발 · 치명타 ${Math.round(stats.normalCrit*100)}% · 사거리 5칸</span><span>뱅크샷: 피해 ${stats.bankDamage} · 수명 ${stats.bankLife}초 · ${Number(stats.bankInterval.toFixed(2))}초 간격</span>`;$('normal-desc').textContent=`${stats.normalDamage} 피해 · 0.5초 간격 · ${stats.normalShots}발 · 사거리 5칸`;$('bank-desc').textContent=`${stats.bankDamage} 피해 · ${Number(stats.bankInterval.toFixed(2))}초 간격 · 수명 ${stats.bankLife}초`}
$('shop-items').addEventListener('click',e=>{const button=e.target.closest('[data-buy]');if(button)buyItem(Number(button.dataset.buy))});
let CORE=44;''')
s=s.replace('function reset(){pendingAim=null;', "function reset(){money=10;upgrades=Object.fromEntries(SHOP_ITEMS.map(item=>[item.key,0]));shopOffers=[];shopSignature='';pendingAim=null;")
s=s.replace("function ui(){$('round-results')", "function ui(){shopUI();$('round-results')")
s=s.replace('4-(b.age??0)', '(b.life??weaponStats().bankLife)-(b.age??0)').replace('expired=b.age>=4-1e-9', 'expired=b.age>=(b.life??weaponStats().bankLife)-1e-9')
s=s.replace("e.hp-=b.type==='bank'?1:3;", "e.hp-=b.damage??(b.type==='bank'?weaponStats().bankDamage:weaponStats().normalDamage);")
s=s.replace('kills++;roundKills++;', 'kills++;roundKills++;money++;')
old="t.cool+=t.type==='bank'?3:.5;bullets.push({x:t.x,y:t.y,vx:Math.cos(t.angle)*6,vy:Math.sin(t.angle)*6,type:t.type,age:0,traveled:0,contacts:new Set()})"
assert old in s
s=s.replace(old,"t.cool+=t.type==='bank'?weaponStats().bankInterval:.5;fireTower(t)")
s=s.replace('function update(dt){', '''function fireTower(t){const stats=weaponStats(),bank=t.type==='bank',count=bank?1:stats.normalShots;for(let i=0;i<count;i++){const critical=!bank&&Math.random()<stats.normalCrit,offset=count===1?0:(i/(count-1)-.5)*.16;bullets.push({x:t.x-Math.sin(t.angle)*offset,y:t.y+Math.cos(t.angle)*offset,vx:Math.cos(t.angle)*6,vy:Math.sin(t.angle)*6,type:t.type,age:0,traveled:0,life:stats.bankLife,damage:bank?stats.bankDamage:stats.normalDamage*(critical?2:1),critical,contacts:new Set()})}}
function update(dt){''')
s=s.replace("round++;phase='build';remaining=60;", "round++;phase='build';remaining=60;rollShop();")
s=s.replace("b.type==='bank'?'#ffc16b':'#94fff0'", "b.type==='bank'?'#ffc16b':b.critical?'#ffb8ee':'#94fff0'")
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8')
s=s.replace('<div class="header-right">','<div class="header-right"><span id="money" class="money">10원</span>')
s=s.replace('<small>3 피해 · 0.5초 간격 · 사거리 5칸</small>', '<small id="normal-desc">3 피해 · 0.5초 간격 · 사거리 5칸</small>')
s=s.replace('<small>1 피해 · 3초 간격 · 관통 · 수명 4초</small>', '<small id="bank-desc">1 피해 · 3초 간격 · 관통 · 수명 4초</small>')
s=s.replace('<footer>', '<section class="shop"><div class="shop-heading"><h2>방어 보급 상점</h2><span id="shop-state">1라운드 클리어 후 개방</span></div><p>라운드 준비마다 무작위 상품 2개 · 품절 없이 반복 구매 · 효과는 모든 해당 포탑에 누적 적용</p><p id="shop-placeholder">1라운드를 클리어하면 상품이 도착합니다. 시작 자금 10원, 적 처치마다 +1원.</p><div id="shop-items"></div><div id="weapon-stats"></div></section><footer>')
s=s.replace('발사 후 4초가 지나면 사라집니다.', '기본 지속시간은 4초입니다. 구매한 강화 효과는 다음 라운드에도 유지됩니다.')
p.write_text(s,encoding='utf-8')
p=Path('dist/style.css');s=p.read_text(encoding='utf-8')+'''
.money{font:600 17px 'IBM Plex Mono',monospace;color:var(--amber);white-space:nowrap}.shop{margin-top:26px;border:1px solid var(--border);border-radius:9px;padding:22px;background:var(--panel)}.shop-heading{display:flex;align-items:center;justify-content:space-between;gap:12px}.shop h2{font-size:19px;margin:0}.shop-heading>span{font-size:14px;color:var(--amber)}.shop p{font-size:14px;color:var(--muted);line-height:1.8}#shop-items{display:grid;grid-template-columns:1fr 1fr;gap:14px}.shop-item{display:flex;justify-content:space-between;gap:16px;align-items:center;text-align:left;background:#172e36;border:1px solid #3b666d;border-radius:7px;padding:18px}.shop-item b{font-size:16px}.shop-item small{display:block;margin-top:7px;font-size:14px;color:var(--muted)}.shop-item>strong{white-space:nowrap;color:var(--amber)}#weapon-stats{display:flex;flex-wrap:wrap;gap:12px 28px;font-size:14px;color:var(--cyan);line-height:1.8;margin-top:18px}@media(max-width:700px){#shop-items{grid-template-columns:1fr}.shop{padding:16px}.header-right{gap:10px}.shop-heading{align-items:flex-start;flex-direction:column}.money{font-size:15px}}
''';p.write_text(s,encoding='utf-8')
