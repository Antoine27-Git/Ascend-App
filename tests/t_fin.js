/* D-103 : fin de préparation — sorties clés à rebours, niveau tenu en bloc, affûtage qui baisse (H-67). Lance : node t_fin.js */
const E=require('./engine.js'),base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const antoine=p=>{p.planStart='2026-11-02';p.goalDplus=5000;p.races[0].dplus=1900;p.start.pastRaces=[{dur:390,dist:42,dplus:1300,date:'2025-09-20'}];
  p.days={run:[3,0],long:0,cf:[2,5],time:{}};p.orgs=[{from:'F3',enchaine:true,days:{run:[3,6,0],long:0,cf:[2],time:{}}}];};
const plan=(on,mod,today,regles)=>{E.CONV.finPrepa=on;const p=JSON.parse(JSON.stringify(base));if(mod)mod(p);
  const o=E.build({profile:p,today:today||'2026-09-27',sessions:[],isRun,regles});E.CONV.finPrepa=true;o.p=p;return o;};
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};
const sem=(o,k)=>o.sessions.filter(x=>x.date>=k.mon&&new Date(x.date)<new Date(k.mon).getTime()+7*864e5&&x.type!=='cf');
const longue=(o,k)=>(sem(o,k).find(x=>x.type==='long')||{}).dur||0;
const vol=(o,k)=>sem(o,k).filter(x=>x.type!=='race').reduce((a,x)=>a+x.dur,0);
const h=m=>Math.floor(m/60)+' h '+String(m%60).padStart(2,'0');

for(const [nom,mod,today] of [['profil de base (4 jours)',null],['profil d\'Antoine (3 jours en spécifique)',antoine,'2026-11-14']]){
  console.log('— '+nom);
  const o=plan(true,mod,today),T=o.info.cal.T,W=w=>o.weeks.find(k=>k.w===w);
  const cles=o.weeks.filter(k=>k.cle).map(k=>k.w);
  t('sorties clés 7, 5 et 3 semaines avant la course',JSON.stringify(cles)===JSON.stringify([T-5,T-3,T-1]),'semaines '+cles.join(', ')+' ; course en S'+o.info.cal.N);
  const d=cles.map(w=>longue(o,W(w)));
  t('sorties clés croissantes, 5 h à 6 h',d[0]===300&&d[1]===330&&d[2]===360,d.map(h).join(' → '));
  const der=sem(o,W(T-1)).find(x=>x.type==='long'),j=Math.round((new Date(o.p.goalDate)-new Date(der.date))/864e5);
  t('dernière sortie clé à 3 semaines de la course',j>=19&&j<=21,j+' jours avant');
  const avant=o.weeks.filter(k=>(k.phase==='bloc'||k.phase==='pic')&&k.w<T-5&&k.type==='charge').map(k=>longue(o,k));
  t('avant la première sortie clé, le niveau est tenu (au moins une sortie de 4 h 30 ou plus)',Math.max(0,...avant)>=270,avant.map(h).join(', '));
  const moy=o.weeks.filter(k=>(k.phase==='bloc'||k.phase==='pic')&&k.type==='charge'&&!k.cle).map(k=>longue(o,k));
  t('semaine moyenne : 4 h au plus hors sortie clé une fois les clés commencées',o.weeks.filter(k=>k.w>T-5&&k.w<T&&k.type==='charge'&&!k.cle).every(k=>longue(o,k)<=240),moy.map(h).join(', '));
  const aff=o.weeks.filter(k=>k.type==='affutage'&&k.w<o.info.cal.N),la=aff.map(k=>longue(o,k));
  t('affûtage : sortie longue de 3 h puis 2 h, jamais en hausse',la[0]===180&&la[1]===120,la.map(h).join(' → '));
  const charge=o.weeks.filter(k=>k.w<T&&k.type==='charge').slice(-3).map(k=>vol(o,k)),ref=charge.reduce((a,x)=>a+x,0)/3;
  const baisse=aff.map(k=>Math.round((1-vol(o,k)/ref)*100)),bm=baisse.reduce((a,x)=>a+x,0)/baisse.length;
  t('affûtage : baisse moyenne du volume entre 41 et 60 %',bm>=41&&bm<=60,baisse.map(x=>'−'+x+' %').join(', ')+' ; moyenne −'+Math.round(bm)+' %');
  const chocs=o.weeks.filter(k=>k.phase!=='fond'&&sem(o,k).some(x=>x.title==='Week-end de choc')).map(k=>k.w);
  t('deux week-ends de choc au plus avant l\'objectif principal, jamais sur la dernière sortie clé',chocs.length<=2&&!chocs.includes(T-1),chocs.length?'semaines '+chocs.join(', '):'aucun (enchaînement non activé)');
  /* règle des 30 jours : aucune sortie longue au-delà de +10 % (arrondi 5 min) de la plus longue des 30 jours */
  const S=o.sessions.filter(x=>x.type!=='cf');let pire=0;
  S.filter(x=>x.type==='long'&&x.date>=W(Math.min(...o.weeks.filter(k=>k.phase==='bloc').map(k=>k.w))).mon).forEach(x=>{const tt=new Date(x.date).getTime(),mx=Math.max(0,...S.filter(y=>new Date(y.date).getTime()<tt&&new Date(y.date).getTime()>=tt-30*864e5).map(y=>y.dur));pire=Math.max(pire,x.dur-Math.ceil(1.1*mx/5)*5);});
  t('règle des 30 jours respectée en bloc, en pic et en affûtage',pire<=0);
  const off=plan(false,mod,today),ds=o.weeks.find(k=>k.type==='aff_sec'),lim=ds?ds.mon:W(o.weeks.find(k=>k.phase==='bloc').w).mon;
  t('rien ne change avant l\'affûtage du 50 km',JSON.stringify(o.sessions.filter(x=>x.date<lim))===JSON.stringify(off.sessions.filter(x=>x.date<lim)));
  const s2=o.weeks.filter(k=>k.type==='aff_sec').map(k=>longue(o,k)).filter(Boolean);
  t('affûtage du 50 km : sortie longue en baisse, 1 h 30 au plus 6 jours avant',s2.length===2&&s2[0]>s2[1]&&s2[1]<=95,s2.map(h).join(' → '));
}
console.log('— règles v1');
t('règles v1 : plan identique',JSON.stringify(plan(true,null,null,'v1').sessions)===JSON.stringify(plan(false,null,null,'v1').sessions));
if(!ok)process.exitCode=1;
