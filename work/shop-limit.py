from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace("shopOffers=[],shopSignature=''", "shopOffers=[],shopPurchased=new Set(),shopSignature=''")
s=s.replace('function rollShop(){const pool=', 'function rollShop(){shopPurchased.clear();const pool=')
s=s.replace("!shopOffers.includes(index))return false", "!shopOffers.includes(index)||shopPurchased.has(index))return false")
s=s.replace('money-=item.price;upgrades', 'money-=item.price;shopPurchased.add(index);upgrades')
s=s.replace('round,shopOffers,upgrades]', 'round,shopOffers,upgrades,[...shopPurchased]]')
s=s.replace("!open||money<item.price?'disabled'", "!open||money<item.price||shopPurchased.has(i)?'disabled'")
s=s.replace('<strong>${item.price}원</strong>', "<strong>${shopPurchased.has(i)?'구매 완료':`${item.price}원`}</strong>")
s=s.replace("shopOffers=[];shopSignature='';pendingAim", "shopOffers=[];shopPurchased.clear();shopSignature='';pendingAim")
s=s.replace('spawnClock=2.5-(round-1)*.27', 'spawnClock=(2.5-(round-1)*.27)/1.3')
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('품절 없이 반복 구매', '상품별 라운드당 1회 구매 · 다음 라운드에 재등장 시 구매 가능');p.write_text(s,encoding='utf-8')
p=Path('work/check.cjs');s=p.read_text(encoding='utf-8');s=s[:s.index("assert.equal(run('reset();money===10")]+'''
assert.equal(run('reset();money===10&&shopOffers.length===0&&buyItem(0)===false'),true);
assert.equal(run("start();spawnClock=Infinity;remaining=STEP;update(STEP);round===2&&shopOffers.length===2&&new Set(shopOffers).size===2"),true);
assert.equal(run('money=100;shopOffers=[0,1];buyItem(0)&&!buyItem(0)&&money===85&&weaponStats().bankLife===5'),true);
assert.equal(run('buyItem(1)&&!buyItem(1)&&money===75&&weaponStats().bankDamage===2'),true);
assert.equal(nodes.get('shop-items').innerHTML.split('구매 완료').length-1,2);
assert.equal(run('start();buyItem(0)===false;spawnClock=Infinity;remaining=STEP;update(STEP);round===3&&shopPurchased.size===0&&weaponStats().bankLife===5'),true);
assert.equal(run('shopOffers=[0,1];buyItem(0)&&money===60&&weaponStats().bankLife===6'),true);
assert.equal(run('shopOffers=[2,3];buyItem(2)&&!buyItem(2)&&Math.abs(weaponStats().bankInterval-2.5)<1e-10&&buyItem(3)&&weaponStats().normalDamage===4'),true);
assert.equal(run('shopOffers=[4,5];buyItem(4)&&weaponStats().normalShots===2&&buyItem(5)&&weaponStats().normalCrit===.1&&money===15'),true);
assert.equal(run('rollShop();shopOffers=[0,1];money=9;!buyItem(1)&&money===9&&!shopPurchased.has(1)'),true);
assert.equal(run('money=100;start();!buyItem(1)&&money===100'),true);
assert.equal(run('paused=true;!buyItem(1)&&money===100'),true);
assert.equal(run("paused=false;bullets=[];upgrades.normalCrit=10;fireTower({x:2,y:2,angle:0,type:'normal'});bullets.length===2&&bullets.every(b=>b.damage===8&&b.critical)"),true);
assert.equal(run("enemies=[{id:20,x:2.4,y:2,hp:8}];bullets=bullets.filter(b=>moveBullet(b,.1));money===101&&kills===1"),true);
assert.equal(run("enemies=[];bullets=[];fireTower({x:2,y:2,angle:0,type:'bank'});bullets[0].life===6&&bullets[0].damage===2"),true);
assert.equal(run("let upgradedBullet=bullets[0];upgradedBullet.vx=0;upgradedBullet.vy=0;moveBullet(upgradedBullet,5.9)&&!moveBullet(upgradedBullet,.1)"),true);
assert.equal(run("bullets=[];enemies=[];towers=[{x:2,y:2,angle:0,type:'bank',cool:0}];spawnClock=Infinity;update(STEP);Math.abs(towers[0].cool-(2.5-STEP))<1e-9"),true);
assert.equal(run('reset();money===10&&weaponStats().bankLife===4&&weaponStats().normalShots===1&&shopOffers.length===0&&shopPurchased.size===0'),true);
assert.equal(run('Array.from({length:5},(_,i)=>{reset();round=i+1;start();update(STEP);return Math.abs(spawnClock-(2.5-i*.27)/1.3)<1e-10}).every(Boolean)'),true);
console.log('PASS: one purchase per item per round, both offers purchasable, re-purchase next round, funds, all upgrades, reset and 1.3x spawn rate.');
''';p.write_text(s,encoding='utf-8')
