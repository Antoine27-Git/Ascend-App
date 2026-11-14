/* D-102 : le D+ des sorties se cale sur la course intermédiaire la plus proche (H-66). Lance : node t_densite.js
   Profil d'Antoine : plan démarré le 2/11/2026, 42 km / 1 300 m en 6 h 30 comme référence, 50 km / 1 900 m le 8/05/2027, 80 km au bout. */
const E=require('./engine.js'),base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
function prof(gd,mod){const p=JSON.parse(JSON.stringify(base));p.planStart='2026-11-02';p.goalDplus=gd;p.races[0].dplus=1900;
  p.start.pastRaces=[{dur:390,dist:42,dplus:1300,date:'2025-09-20'}];p.start.lastLong={date:'2026-09-03',dur:120,dist:12,dplus:500};
  p.days={run:[3,6,0],long:0,cf:[2],time:{}};p.orgs=[{from:'F1',enchaine:true,days:{run:[3,6,0],long:0,cf:[2],time:{}}}];if(mod)mod(p);return p;}
const plan=(on,gd,mod,regles)=>{E.CONV.densCourse=on;const o=E.build({profile:prof(gd,mod),today:'2026-11-14',sessions:[],isRun,regles});E.CONV.densCourse=true;return o;};
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};
const avant=(o,d)=>o.sessions.filter(x=>x.type==='long'&&x.date<d);
const maxDp=(o,d)=>Math.max(0,...avant(o,d).map(x=>x.dplus||0));

/* 1. Profil d'Antoine (80 km à 3 000 m) : plus gros D+ avant le 50 km */
const off=plan(false,3000),on=plan(true,3000);
const rS=on.info.inter&&on.info.inter[0];
t('la course intermédiaire est repérée, à 38 m de D+ par km',!!rS&&Math.round(rS.mkm)===38,rS?Math.round(rS.dens)+' m/h':'absente');
t('plus gros D+ en sortie longue avant le 50 km : plus haut qu\'avant',maxDp(on,'2027-04-24')>maxDp(off,'2027-04-24'),maxDp(off,'2027-04-24')+' → '+maxDp(on,'2027-04-24')+' m');
t('… et au moins 1 000 m',maxDp(on,'2027-04-24')>=1000);
const ch=o=>o.sessions.filter(x=>x.title==='Week-end choc'&&x.date<'2027-05-08');
t('week-end choc avant le 50 km : la veille passe à pleine densité',ch(on).length>0&&ch(on)[0].dplus>ch(off)[0].dplus,ch(off).map(x=>x.dur+' min/'+x.dplus+' m').join()+' → '+ch(on).map(x=>x.dur+' min/'+x.dplus+' m').join());
const dpH=x=>x.dplus/(x.dur/60);
t('la veille de choc est à la densité de la sortie longue (±15 %)',ch(on).length>0&&dpH(ch(on)[0])>=0.85*dpH(avant(on,'2027-05-08').filter(x=>x.date>ch(on)[0].date)[0]||{dplus:0,dur:1}));

/* 2. Densité par semaine */
const dw=o=>o.weeks.map(k=>k.dens).filter(Number.isFinite);   /* la semaine 1 peut ne pas porter de densité */
t('jamais plus basse que la rampe d\'avant',dw(on).every((v,i)=>v>=dw(off)[i]-1e-9));
const on4=plan(true,4000);const w4=on4.info.inter[0];
t('8 semaines avant la course : au moins la densité de la course',on4.weeks.filter(k=>k.w>=w4.w-8&&k.w<w4.w).every(k=>k.dens>=w4.dens-1e-9),Math.round(w4.dens)+' m/h');
const d4=dw(on4);
t('pas de saut d\'une semaine à l\'autre (≤ 10 m/h)',d4.every((v,i)=>i===0||v-d4[i-1]<=10),'plus grand pas : '+Math.round(Math.max(...d4.map((v,i)=>i?v-d4[i-1]:0)))+' m/h');
t('après la course, la densité ne redescend pas',d4.every((v,i)=>i===0||v>=d4[i-1]-1e-9));
t('la densité ne dépasse pas celle de l\'objectif principal',d4.every(v=>v<=on4.info.densite.course+1e-9));

/* 3. Rien d'autre ne bouge */
const dur=o=>JSON.stringify(o.sessions.map(x=>[x.date,x.type,x.dur]));
/* avant le bloc spécifique (juin 2027) : les week-ends choc de l'objectif principal, plus tard, passent aussi à pleine densité */
const tot=o=>JSON.stringify(o.sessions.filter(x=>x.date<'2027-06-01'));
t('durées des séances inchangées',dur(on)===dur(off));
const sans=mod=>{mod.races=[];};
t('sans course intermédiaire : plan identique jusqu\'au bloc spécifique',tot(plan(true,3000,sans))===tot(plan(false,3000,sans)));
t('règles v1 : plan identique',JSON.stringify(plan(true,3000,null,'v1').sessions)===JSON.stringify(plan(false,3000,null,'v1').sessions));
t('course de priorité C (course-entraînement) : plan identique',tot(plan(true,3000,p=>{p.races[0].prio='C';}))===tot(plan(false,3000,p=>{p.races[0].prio='C';})));

/* 4. Texte */
const L=avant(on,'2027-05-08').filter(x=>x.dplus).slice(-1)[0];
t('le texte de la sortie longue parle des descentes',/descentes/.test(L.why||''));
const densTxt=on.sessions.filter(x=>x.type==='long'&&x.date<'2027-04-24'&&/38 m de D\+ par km/.test(x.why||''));
t('« 38 m de D+ par km, comme ta course » apparaît dans la fenêtre',densTxt.length>0,densTxt.length+' sortie(s)');
if(!ok)process.exitCode=1;
