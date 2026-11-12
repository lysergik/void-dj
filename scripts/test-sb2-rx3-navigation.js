const fs=require('fs'),vm=require('vm');
const vals={},log=[];let now=0,timers=[];
const engine={getValue:(g,k)=>vals[g+'.'+k]||0,
 setValue:(g,k,v)=>{vals[g+'.'+k]=v;if(v)log.push(g.replace('[','').replace(']','')+'.'+k+'='+v);
   if(g==='[Tab]'&&k==='library'&&v)vals['[Tab].current']=1;
   if(g==='[Tab]'&&k==='overview'&&v)vals['[Tab].current']=0;
   if(g==='[RX3Shortcut]'&&k==='toggle'&&v)vals['[RX3Shortcut].visible']=vals['[RX3Shortcut].visible']?0:1;},
 beginTimer:(ms,f)=>{const t={ms,f,at:now+ms};timers.push(t);return t},stopTimer:t=>{timers=timers.filter(x=>x!==t)},brake(){}};
const ctx={engine,midi:{},console,Date:{now:()=>now}};vm.createContext(ctx);
const path=require('path'),assert=require('assert');
const dir=path.join(__dirname,'../controllers/Pioneer_DDJ_SB2_RX3');
for(const f of ['Nautic-RX3-Encoder-SB2.js','Pioneer-DDJ-SB2-RX3-Browser.js'])vm.runInContext(fs.readFileSync(path.join(dir,f),'utf8'),ctx);
const results={};
const run=c=>vm.runInContext(c,ctx);
const adv=ms=>{now+=ms;for(const t of timers.slice())if(t.at<=now){timers=timers.filter(x=>x!==t);t.f();}};
function scen(name,setup,fn){for(const k in vals)delete vals[k];vals['[RX3Browser].enabled']=1;vals['[Tab].current']=0;timers=[];log.length=0;
  run('NauticSB2Browser.section=-1;NauticSB2Browser.menuOpen=false;NauticSB2Browser.accumulated=0;NauticRX3Encoder.pressed=false;NauticRX3Encoder.consumed=false;NauticRX3Encoder.moved=false');
  if(setup)setup();log.length=0;fn();results[name]=log.join(' | ');}
const press=(fn,ms)=>{run(`NauticSB2Browser.${fn}(6,0x41,127,0x96)`);adv(ms);run(`NauticSB2Browser.${fn}(6,0x41,0,0x96)`)};
const open=()=>{vals['[Tab].current']=1};
scen('BROWSE short press from PERFORMANCE',null,()=>press('enter',100));
scen('BROWSE short press when open (enter)',open,()=>press('enter',100));
scen('BROWSE 2s hold when open (back)',open,()=>press('enter',2100));
scen('BROWSE 2s hold in PERFORMANCE (grid)',null,()=>press('enter',2100));
scen('BROWSE turn cw/ccw open',open,()=>{run('NauticSB2Browser.turn(6,0x40,1,0xB6)');run('NauticSB2Browser.turn(6,0x40,0x7f,0xB6)')});
scen('SHIFT+BROWSE short press (back)',open,()=>press('shortcut',100));
scen('SHIFT+BROWSE 2s hold (SHORTCUT toggle)',open,()=>press('shortcut',2100));
scen('SHORTCUT visible: turn',()=>{vals['[RX3Shortcut].visible']=1;open()},()=>run('NauticSB2Browser.turn(6,0x40,1,0xB6)'));
scen('SHORTCUT visible: SHIFT+BROWSE short (no leak)',()=>{vals['[RX3Shortcut].visible']=1;open()},()=>press('shortcut',100));
scen('SHIFT+turn x6 clicks cw from closed',null,()=>{for(let i=0;i<12;i++)run('NauticSB2Browser.shiftTurn(6,0x64,1,0xB6)')});
scen('SHIFT+turn through MENU then back',open,()=>{for(let i=0;i<14;i++)run('NauticSB2Browser.shiftTurn(6,0x64,1,0xB6)');for(let i=0;i<4;i++)run('NauticSB2Browser.shiftTurn(6,0x64,0x7f,0xB6)')});
scen('SHIFT+LOAD1 (source) from PERFORMANCE',null,()=>run('NauticSB2Browser.source(6,0x58,127)'));
scen('SHIFT+LOAD1 with SHORTCUT open (close it)',()=>{vals['[RX3Shortcut].visible']=1},()=>run('NauticSB2Browser.source(6,0x58,127)'));
scen('SHIFT+LOAD2 toggles view open->perf',open,()=>run('NauticSB2Browser.view(6,0x59,127)'));
scen('SHIFT+LOAD2 toggles view perf->open',null,()=>run('NauticSB2Browser.view(6,0x59,127)'));

const expect={
'BROWSE short press from PERFORMANCE':'Tab.library=1 | Skin.show_maximized_library=1 | RX3Browser.open=1',
'BROWSE short press when open (enter)':'RX3Browser.enter=1',
'BROWSE 2s hold when open (back)':'RX3Browser.back=1',
'BROWSE 2s hold in PERFORMANCE (grid)':'RX3Controller.grid_mode=1',
'BROWSE turn cw/ccw open':'RX3Browser.move=1 | RX3Browser.move=-1',
'SHIFT+BROWSE short press (back)':'RX3Browser.back=1',
'SHIFT+BROWSE 2s hold (SHORTCUT toggle)':'RX3Shortcut.toggle=1',
'SHORTCUT visible: turn':'RX3Shortcut.move=1',
'SHORTCUT visible: SHIFT+BROWSE short (no leak)':'',
'SHIFT+LOAD1 (source) from PERFORMANCE':'Tab.library=1 | Skin.show_maximized_library=1 | RX3Browser.open=1 | RX3Browser.source=1',
'SHIFT+LOAD1 with SHORTCUT open (close it)':'RX3Shortcut.toggle=1',
'SHIFT+LOAD2 toggles view open->perf':'Tab.overview=1',
'SHIFT+LOAD2 toggles view perf->open':'Tab.library=1 | Skin.show_maximized_library=1 | RX3Browser.open=1'};
for(const k in expect)assert.strictEqual(results[k],expect[k],k);
assert.ok(results['SHIFT+turn x6 clicks cw from closed'].endsWith('RX3Browser.source=1 | RX3Browser.browse=1 | RX3Browser.tag_list=1 | RX3Browser.playlist=1 | RX3Browser.search=1 | RX3Browser.utility=1'));
assert.strictEqual(results['SHIFT+turn through MENU then back'],'RX3Browser.browse=1 | RX3Browser.tag_list=1 | RX3Browser.playlist=1 | RX3Browser.search=1 | RX3Browser.utility=1 | RX3Browser.close_tools=1 | RX3Browser.track_tools=1 | RX3Browser.close_tools=1 | RX3Browser.utility=1 | RX3Browser.close_tools=1 | RX3Browser.search=1');
console.log('DDJ-SB2 RX3 navigation: '+Object.keys(results).length+' gesture scenarios verified');
