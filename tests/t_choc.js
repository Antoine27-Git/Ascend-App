/* D-105 : week-end de choc selon les avis d'experts (H-69). Lance : node t_choc.js */
const E=require('./engine.js'),base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const antoine=p=>{p.planStart='2026-11-02';p.goalDplus=5000;p.races[0].dplus=1900;p.start.pastRaces=[{dur:390,dist:42,dplus:1300,date:'2025-09-20'}];
  p.days={run:[3,0],long:0,cf:[2,5],time:{}};p.orgs=[{from:'F3',enchaine:true,days:{run:[3,6,0],long:0,cf:[2],time:{}}}];};
const plan=(on,mod,regles)=>{E.CONV.chocExperts=on;const p=JSON.parse(JSON.stringify(base));antoine(p);if(mod)mod(p);
  const o=E.build({profile:p,today:'2026-11-14',sessions:[],isRun,regles});E.CONV.chocExperts=true;return o;};
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};
const sem=(o,k)=>o.sessions.filter(x=>x.date>=k.mon&&new Date(x.date)<new Date(k.mon).getTime()+7*864e5&&x.type!=='cf');
const h=m=>Math.floor(m/60)+' h '+String(m%60).padStart(2,'0');
const o=plan(true),T=o.info.cal.T,N=o.info.cal.N,W=w=>o.weeks.find(k=>k.w===w);
const chocs=o.weeks.filter(k=>k.choc);
const princ=chocs.filter(k=>k.phase!=='fond');
t('un seul week-end de choc avant l\'objectif principal, 7 semaines avant',princ.length===1&&princ[0].w===T-5,'S'+princ.map(k=>k.w).join(',')+' ; course en S'+N);
t('la semaine qui le suit est une semaine allégée',W(T-4).type==='relache');
t('un week-end de choc avant le 50 km, 4 à 6 semaines avant',chocs.filter(k=>k.phase==='fond').length===1,chocs.filter(k=>k.phase==='fond').map(k=>'S'+k.w).join());
const ecart=chocs.slice(1).map((k,i)=>k.w-chocs[i].w);
t('au moins 4 semaines entre deux week-ends de choc',ecart.every(e=>e>=4),'écarts : '+ecart.join(', ')+' semaines');
for(const k of chocs){const s=sem(o,k),L=s.find(x=>x.type==='long'),M=s.find(x=>x.title==='Week-end de choc');
  const jj=Math.round((new Date(M.date)-new Date(L.date))/864e5);
  t('S'+k.w+' : la plus longue d\'abord, la moyenne le lendemain',jj===1,h(L.dur)+' puis '+h(M.dur));
  t('S'+k.w+' : moyenne ≤ 2/3 de la longue et 3 h au plus',M.dur<=Math.ceil(L.dur*2/3/5)*5&&M.dur<=180);
  const autres=s.filter(x=>x!==L&&x!==M);
  t('S'+k.w+' : pas de séance de qualité, autre course d\'1 h au plus',autres.every(x=>x.type==='ef'&&x.dur<=60),autres.map(x=>x.type+' '+x.dur+' min').join(', '));
  const s2=sem(o,W(k.w+1)).filter(x=>x.type!=='long');
  t('S'+(k.w+1)+' (semaine suivante) : pas de qualité, courses d\'1 h au plus',s2.every(x=>x.type==='ef'&&x.dur<=60),s2.map(x=>x.type+' '+x.dur+' min').join(', '));
  t('S'+k.w+' : le texte dit qu\'aucune étude ne le démontre',/Aucune étude/.test(M.why||''));}
/* le reste */
const off=plan(false),d0=chocs[0].mon;
t('rien ne change avant le premier week-end de choc',JSON.stringify(o.sessions.filter(x=>x.date<d0))===JSON.stringify(off.sessions.filter(x=>x.date<d0)));
t('règles v1 : plan identique',JSON.stringify(plan(true,null,'v1').sessions)===JSON.stringify(plan(false,null,'v1').sessions));
t('sans enchaînement : aucun week-end de choc',plan(true,p=>{p.orgs=[];}).weeks.every(k=>!k.choc));
if(!ok)process.exitCode=1;
