from pathlib import Path
p=Path('dist/game.js');s=p.read_text(encoding='utf-8')
s=s.replace("$('angle-range').value=d;",'').replace("$('angle-range').addEventListener('input',e=>setAngle(Number(e.target.value)));",'')
s=s.replace('spawnClock+=SPAWN_INTERVALS[round-1]', 'spawnClock+=SPAWN_INTERVALS[round-1]/difficulty.count')
s=s.replace('(.78+round*.04)*1.44*dt', '(.78+round*.04)*1.44*difficulty.speed*dt')
pos=s.index('const edge=')
s=s[:pos]+'''const difficulty={count:1,speed:1};let optionsResume=false;
+function setDifficulty(key,value){if(!['count','speed'].includes(key)||!Number.isFinite(value))return;value=Math.round(Math.max(.5,Math.min(3,value))*10)/10;if(key==='count'&&Number.isFinite(spawnClock))spawnClock*=difficulty.count/value;difficulty[key]=value;optionsUI()}
+function optionsUI(){for(const key of ['count','speed']){$(`option-${key}`).value=difficulty[key];$(`value-${key}`).textContent=`${difficulty[key].toFixed(1)}배`}$('enemy-estimate').textContent=SPAWN_INTERVALS.map((interval,i)=>`${i+1}R ${Math.ceil(ROUND_DURATION/interval*difficulty.count)}마리`).join(' · ')}
+function openOptions(){optionsResume=phase==='active'&&!paused;if(phase==='active')paused=true;optionsUI();$('options-dialog').showModal();ui()}
+function closeOptions(){if(optionsResume&&phase==='active')paused=false;optionsResume=false;ui()}
+$('options-open').onclick=openOptions;
+$('options-close').onclick=()=>$('options-dialog').close();
+$('options-dialog').addEventListener('close',closeOptions);
+for(const key of ['count','speed'])$(`option-${key}`).addEventListener('input',e=>setDifficulty(key,Number(e.target.value)));
+$('options-default').onclick=()=>{setDifficulty('count',1);setDifficulty('speed',1)};
+'''.replace('\n+','\n')+s[pos:]
s=s.replace("window.addEventListener('keydown',e=>{", "window.addEventListener('keydown',e=>{if($('options-dialog').open)return;")
p.write_text(s,encoding='utf-8')
p=Path('dist/index.html');s=p.read_text(encoding='utf-8').replace('<button id="reset"', '<button id="options-open" class="quiet">옵션 ⚙</button><button id="reset"')
s=s.replace('<input id="angle-range" type="range" min="0" max="359.9" step="0.1" value="0" aria-label="발사 각도 조절">','')
s=s.replace('<script src="game.js">', '''<dialog id="options-dialog" aria-labelledby="options-title"><div class="options-heading"><h2 id="options-title">게임 옵션</h2><button id="options-close" class="quiet" aria-label="옵션 닫기">닫기 ×</button></div><p>1.0배는 현재 기본 난이도입니다. 변경은 즉시 적용됩니다.</p><label class="option-label" for="option-count">적 생성량 <output id="value-count">1.0배</output></label><input id="option-count" type="range" min="0.5" max="3" step="0.1" value="1"><p id="enemy-estimate"></p><label class="option-label" for="option-speed">적 이동속도 <output id="value-speed">1.0배</output></label><input id="option-speed" type="range" min="0.5" max="3" step="0.1" value="1"><p>옵션창을 열면 전투가 잠시 멈춥니다. 이미 나온 적의 속도도 함께 바뀝니다. 생성량 변경은 이후 등장하는 적에 적용됩니다.</p><p>설정은 다음 라운드와 새 게임에도 유지되며, 페이지를 새로 열면 초기화됩니다.</p><button id="options-default" class="quiet">기본값으로 복원</button></dialog><script src="game.js">''')
p.write_text(s,encoding='utf-8')
p=Path('dist/style.css');s=p.read_text(encoding='utf-8')+'''\n#options-dialog{width:min(520px,calc(100vw - 32px));max-height:90vh;overflow:auto;background:#111b27;color:#eef3f9;border:1px solid #3b5368;border-radius:12px;padding:26px}#options-dialog::backdrop{background:#060c14cc}.options-heading{display:flex;justify-content:space-between;align-items:center;gap:16px}.options-heading h2{margin:0;font-size:22px}#options-dialog p{color:#b2c0d0;font-size:14px;line-height:1.8}.option-label{display:flex;justify-content:space-between;margin:24px 0 12px;font-size:16px}.option-label output{color:var(--cyan)}#options-dialog input[type=range]{width:100%;accent-color:var(--cyan);height:28px}#enemy-estimate{color:var(--amber)!important}@media(max-width:700px){header{flex-wrap:wrap;gap:14px}.header-right{flex-wrap:wrap}}\n''';p.write_text(s,encoding='utf-8')
