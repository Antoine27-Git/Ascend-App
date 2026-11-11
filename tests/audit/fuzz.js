/* Audit mission 2 — audit adversarial du moteur v2.
   Des milliers de scénarios tirés au hasard (profils × historiques × séances manquées × fatigue × décalages × maladie),
   rejoués semaine après semaine sur le VRAI moteur ; à chaque plan calculé, des invariants sont vérifiés.
   Le moteur n'est pas modifié. Reproductible : chaque scénario est entièrement défini par sa graine.
   Usage : node tests/audit/fuzz.js [n=2000] [graine0=1] [détail=<graine>]
   Sortie : nombre de violations par invariant, premières graines fautives, répartition des séances par catégorie de pic. */
process.env.TZ=process.env.TZ||'Europe/Paris';
const E=require('../engine.js');
if(process.env.ARRONDI==='0')E.CONV.arrondiSup=false;   /* variante de mesure : sans D-96 */
const isRun=s=>['ef','long','qual','race','desc'].includes(s.type);   /* définition de l'appli */
const add=(d,n)=>{const x=new Date(d+'T12:00:00Z');x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10);};
const days=(a,b)=>Math.round((new Date(b+'T12:00:00Z')-new Date(a+'T12:00:00Z'))/864e5);
const dow=d=>new Date(d+'T12:00:00Z').getUTCDay();
const lundi=d=>add(d,-((dow(d)+6)%7));
function rng(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const pick=(r,a)=>a[Math.floor(r()*a.length)];
const entre=(r,a,b)=>a+Math.floor(r()*(b-a+1));

/* ---- tirage d'un scénario ---- */
function scenario(seed){
  const r=rng(seed);
  const start=add('2026-01-05',7*entre(r,0,60));                       /* un lundi entre janvier 2026 et mars 2027 : toutes les saisons, heure d'été comprise */
  const N=pick(r,[8,10,12,16,20,26,36,47,52,60]);
  const goal=pick(r,[[30,1200],[42,1500],[50,2000],[80,4500],[100,6000],[160,9000],[42,300]]);
  const JOURS=[[3,0],[0],[6],[2,4,0],[3,6,0],[2,4,6,0],[1,2,3,4,6,0],[1,3,5],[6,0],[2,6]];
  const run=pick(r,JOURS),long=r()<0.85?run[run.length-1]:pick(r,run);
  const cf=r()<0.6?pick(r,[[2,5],[2],[1,4],[5]]):[];
  const P={goalDate:add(start,7*(N-1)+entre(r,5,6)),goalDist:goal[0],goalDplus:goal[1],planStart:start,stMode:'libre',
    modules:{strength:cf.length>0},days:{run:run.slice(),long,cf},orgs:[],start:{},races:[],manques:{},decal:{}};
  if(r()<0.3&&run.length<=3)P.orgs=[{from:pick(r,['F3','F4','bloc']),enchaine:r()<0.7,days:{run:[3,6,0],long:0,cf:cf.slice(0,1)}}];
  const hist=pick(r,['rien','longue','longue','reel','reel','declare','pause']);
  const ses=[];
  if(hist==='longue')P.start.lastLong={date:add(start,-entre(r,1,140)),dur:pick(r,[40,60,90,107,120,180,240]),dist:12,dplus:500};
  if(hist==='declare'){P.start.freq4w=entre(r,1,4);P.start.dur4w=pick(r,[30,45,60,90,120]);if(r()<0.5)P.start.lastLong={date:add(start,-entre(r,1,40)),dur:pick(r,[60,90,120,180]),dist:15,dplus:400};}
  if(hist==='pause'){P.start.pauseSince=pick(r,['lt2','2-6','gt6']);P.start.beforeFreq=entre(r,2,4);P.start.beforeDur=pick(r,[45,60,90]);}
  if(hist==='reel'){const n=entre(r,1,12);for(let i=0;i<n;i++){const d=add(start,-entre(r,1,120));if(!ses.some(s=>s.date===d))ses.push({date:d,type:r()<0.3?'long':'ef',dur:pick(r,[20,30,45,60,76,90,120,150,200]),rpe:entre(r,2,5)});}}
  const nr=r()<0.5?0:entre(r,1,2);
  for(let i=0;i<nr;i++){const w=entre(r,3,Math.max(3,N-3));const g=pick(r,[[20,800],[30,1200],[50,2000],[80,4000]]);
    P.races.push({name:'C'+i,date:add(start,7*(w-1)+pick(r,[5,6])),dist:g[0],dplus:g[1],prio:pick(r,['A','B','B','C'])});}
  /* comportement du coureur */
  const C={pManque:pick(r,[0,0,0.1,0.25,0.4]),pFatigue:pick(r,[0,0.3,1]),rpeBase:pick(r,[2,3,3,4,6]),rpeBruit:pick(r,[0,1,2]),sansRpe:pick(r,[0,0,0.5,1]),
    fDuree:pick(r,[[1,1],[1,1],[0.6,1],[0.8,1.3],[1,1.5]]),pDecal:pick(r,[0,0,0.2]),pExtra:pick(r,[0,0,0.1]),
    maladie:r()<0.35?{w:entre(r,2,Math.max(2,N-2)),k:pick(r,[1,2,3,4,6,8])}:null,lectureLundi:r()<0.15,typeLong:pick(r,['long','long','long','ef'])};
  return {seed,P,ses,C,N,start,r};
}

/* ---- référence indépendante (D-94) : plus longue course réelle des 30 jours, ou mémoire plafonnée à 60 min de séance ---- */
function refD94(runs,date){let m=0,mem=0;for(const s of runs){const a=days(s.date,date);if(a<=0)continue;if(a<=30){if(s.dur>m)m=s.dur;}else{const v=s.dur*Math.max(0,1-0.01*(a-30));if(v>mem)mem=v;}}return Math.max(m,Math.min(mem,60/1.1));}
const max30=(runs,date)=>Math.max(0,...runs.filter(s=>{const a=days(s.date,date);return a>0&&a<=30;}).map(s=>s.dur));
const limiteSL=ref=>{const l=Math.max(30,1.1*ref);return (l>=50-0.01&&E.CONV.arrondiSup)?5*Math.ceil((l-1e-9)/5):Math.floor(l+1e-9);};
function categorie(dur,m30){if(!m30)return 'aucune course dans les 30 j';const x=dur/m30-1;return x<=0.10+1e-9?'≤ +10 %':x<=0.30?'+10 à +30 %':x<=1?'+30 à +100 %':'> +100 %';}

/* ---- rejoue un scénario et vérifie les invariants ---- */
function rejoue(sc,V){
  const {P,ses,C,N,start,r}=sc;const viol=(k,msg,x)=>{(V[k]=V[k]||[]).push({seed:sc.seed,msg,x});};
  const cat={};let o;const declares=!!(P.start.freq4w);   /* séances déclarées fictives : la référence indépendante ne les connaît pas (mémoire de 130 jours → 19 semaines exclues) */
  const runsDeclares=()=>{const a=ses.filter(isRun).map(s=>({date:s.date,dur:s.dur||0}));if(P.start.lastLong&&P.start.lastLong.date<start)a.push({date:P.start.lastLong.date,dur:P.start.lastLong.dur});return a;};
  for(let w=1;w<=N;w++){
    const mon=add(start,(w-1)*7),today=C.lectureLundi?mon:add(mon,1);
    let o1;try{o=E.build({profile:P,today,sessions:ses,isRun});o1=E.build({profile:JSON.parse(JSON.stringify(P)),today,sessions:JSON.parse(JSON.stringify(ses)),isRun});}
    catch(e){viol('I0 exception',String(e.message).slice(0,80)+' S'+w);return {cat,ok:false};}
    if(!o.ok){if(w===1)return {cat,ok:false,refus:o.garde.reasons[0]};viol('I0 plan refusé en cours de route','S'+w+' '+(o.garde.reasons[0]||''));return {cat,ok:false};}
    /* I2 déterminisme : deux calculs sur des copies donnent le même plan */
    if(JSON.stringify(o.sessions)!==JSON.stringify(o1.sessions))viol('I2 déterminisme','S'+w);
    const sem=o.sessions.filter(s=>s.date>=mon&&s.date<add(mon,7)&&s.type!=='cf').sort((a,b)=>a.date<b.date?-1:1);
    /* I6 forme : durées entières positives, une course par jour, jour de course seul, endurance ≤ 90 min */
    const vus={};o.sessions.forEach(s=>{if(s.type==='cf')return;
      if(!(Number.isFinite(s.dur)&&s.dur>0&&Math.round(s.dur)===s.dur))viol('I6 durée invalide',s.date+' '+s.type+' '+s.dur);
      if(vus[s.date])viol('I6 deux courses le même jour',s.date+' '+vus[s.date]+'+'+s.type);vus[s.date]=s.type;
      if(s.type==='ef'&&s.title!=='Week-end de choc'&&s.dur>90)viol('I6 endurance > 90 min',s.date+' '+s.dur);
      if(s.date>=mon&&s.date<add(mon,7)&&s.dur<20)viol('I6b séance de moins de 20 min prescrite (plancher de 30 min non tenu)',s.date+' '+s.type+' '+s.dur+' min ('+o.weeks.find(k=>k.w===w).type+')');
      if(s.steps){const t=s.steps.reduce((a,x)=>a+(x.rep?x.rep*(x.on.sec+x.off.sec)/60:x.min),0);if(Math.abs(t-s.dur)>1.01)viol('I6 déroulé ≠ durée',s.date+' '+s.title+' '+Math.round(t)+' ≠ '+s.dur);}});
    /* I9 affûtage (repère S-COU-006, pas une règle du moteur) : mesuré en fin de boucle */
    /* I1 règle des 30 jours sur les séances de la semaine en cours, contre une référence recalculée ici à partir du réel */
    const faitsSem=[];
    for(const sMardi of sem){
      /* le coureur lit sa séance LE JOUR MÊME : c'est ce plan-là qui est vérifié et exécuté (rejeu jour après jour) */
      const oJ=C.lectureLundi?o:E.build({profile:P,today:sMardi.date,sessions:ses,isRun});
      const s=oJ.sessions.find(x=>x.date===sMardi.date&&x.type!=='cf');
      /* I2 stabilité : hors lundi, la séance du jour est celle annoncée le mardi (le lundi est traité à part : défaut d'heure d'été) */
      if(!C.lectureLundi&&dow(sMardi.date)!==1&&(!s||s.dur!==sMardi.dur||s.type!==sMardi.type))viol('I2 plan instable dans la semaine',sMardi.date+' '+sMardi.type+' mardi '+sMardi.dur+' → jour J '+(s?s.type+' '+s.dur:'absente'));
      if(!C.lectureLundi&&dow(sMardi.date)===1&&(!s||s.dur!==sMardi.dur||s.type!==sMardi.type))viol('I2b séance du lundi différente le lundi et le mardi',sMardi.date+' '+sMardi.type+' lundi '+(s?s.type+' '+s.dur:'absente')+' → mardi '+sMardi.dur);
      if(!s)continue;
      if(s.type==='race'){ses.push({date:s.date,type:'race',dur:s.dur,rpe:7});continue;}
      const base=runsDeclares().concat(faitsSem);const ref=refD94(base,s.date);
      const long=s.type==='long',lim=long?limiteSL(ref):Math.max(30,Math.ceil(1.1*ref));
      if(!(declares&&w<=19)&&s.dur>lim+0.5)viol((long?'I1 règle des 30 jours (sortie longue)':'I1 règle des 30 jours (autre séance)')+(C.lectureLundi?' — plan lu le lundi':''),'S'+w+' '+s.date+' '+s.type+' '+s.dur+' > limite '+lim+' (réf. réelle '+Math.round(ref)+')',ref>0?s.dur/ref-1:null);
      if(globalThis.DETAIL)console.log('S'+w,s.date,s.type,s.dur,'lim',lim,'ref',Math.round(ref),'| 35 j :',base.filter(x=>days(x.date,s.date)>0&&days(x.date,s.date)<=35).map(x=>x.date.slice(5)+':'+x.dur).join(' '));
      /* exécution */
      const enMaladie=C.maladie&&w>=C.maladie.w&&w<C.maladie.w+C.maladie.k;
      if(enMaladie||r()<C.pManque){P.manques[s.date]=(!enMaladie&&r()<C.pFatigue)?'fatigue':'autre';continue;}
      let d=Math.max(10,Math.round(s.dur*(C.fDuree[0]+r()*(C.fDuree[1]-C.fDuree[0]))));
      const m30=max30(ses.filter(isRun).concat(faitsSem.map(x=>({date:x.date,dur:x.dur,type:'ef'}))),s.date);
      if(d===s.dur){const c=(long?'SL ':'autre ')+categorie(d,m30);cat[c]=(cat[c]||0)+1;}
      const rec={date:s.date,type:long?C.typeLong:s.type,dur:d,rpe:r()<C.sansRpe?null:Math.max(1,Math.min(10,C.rpeBase+entre(r,-C.rpeBruit,C.rpeBruit)))};
      ses.push(rec);faitsSem.push({date:s.date,dur:d});
    }
    if(r()<C.pExtra){const d=add(mon,entre(r,0,6));if(!ses.some(s=>s.date===d))ses.push({date:d,type:'ef',dur:pick(r,[20,30,40]),rpe:3});}
    if(r()<C.pDecal){const o3=E.build({profile:P,today:add(mon,8),sessions:ses,isRun});const fut=o3.sessions.filter(s=>s.date>=add(mon,7)&&s.date<add(mon,14)&&s.type!=='cf'&&s.type!=='race');
      if(fut.length){const s=pick(r,fut),t=add(lundi(s.date),entre(r,0,6));if(!fut.some(x=>x.date===t))P.decal[s.date]=t;}}
  }
  /* I9 : dernière semaine avant la course et volume d'affûtage (mesure, sur adhérence parfaite seulement) */
  return {cat,ok:true,fin:o};
}

/* ---- I3 monotonie (D-94) : une course de plus dans le passé ne baisse jamais la prochaine sortie longue ---- */
function monotonie(seed,V){
  const sc=scenario(seed),r=rng(seed+7777),{P,ses,start}=sc;P.races=[];
  const today=add(start,7*entre(r,0,3)+1);
  const L=s=>{const o=E.build({profile:P,today,sessions:s,isRun});if(!o.ok)return null;const x=o.sessions.find(z=>z.type==='long'&&z.date>=today);return x?x.dur:null;};
  const l0=L(ses);if(l0==null)return;
  const d=add(today,-entre(r,1,100));if(ses.some(s=>s.date===d))return;
  const plus=ses.concat([{date:d,type:'ef',dur:pick(r,[15,20,30,45]),rpe:3}]);const l1=L(plus);
  if(l1!=null&&l1<l0-0.5){const cause=(d<start&&days(d,start)<=35&&P.start.freq4w&&!ses.some(s=>s.date<start&&days(s.date,start)<=35))?'déclaration annulée par une course réelle avant le départ':d>=start?'course ajoutée après le départ':'autre';
    const k='I3 monotonie : une course de plus baisse la sortie longue ('+cause+')';(V[k]=V[k]||[]).push({seed,msg:'ajout '+plus[plus.length-1].dur+' min le '+d+' (départ '+start+', lecture le '+today+') : '+l0+' → '+l1,x:l1/l0-1});}
}

module.exports={scenario,rejoue,rng,add,days,isRun,refD94,max30,limiteSL,categorie,monotonie};
if(require.main===module){
  const n=+process.argv[2]||2000,s0=+process.argv[3]||1,detail=process.argv[4]?+process.argv[4]:null;
  const V={},CAT={};let joues=0,refus=0;const t0=Date.now();
  globalThis.DETAIL=detail!=null;
  for(let i=0;i<n;i++){const sc=scenario(detail!=null?detail:s0+i);if(detail!=null)console.log(JSON.stringify({P:sc.P,C:sc.C,N:sc.N,ses:sc.ses}));const res=rejoue(sc,V);
    if(res.refus){refus++;}else joues++;
    Object.keys(res.cat).forEach(k=>{CAT[k]=(CAT[k]||0)+res.cat[k];});
    monotonie(s0+i,V);
    if(detail!=null)break;}
  console.log(joues+' scénarios rejoués ('+refus+' refusés par le moteur : moins de 6 semaines, etc.), '+Math.round((Date.now()-t0)/1000)+' s');
  const noms=Object.keys(V).sort();
  if(!noms.length)console.log('0 violation');
  noms.forEach(k=>{const g=[...new Set(V[k].map(v=>v.seed))];const xs=V[k].map(v=>v.x).filter(x=>x!=null);console.log('✗ '+k+' : '+V[k].length+' cas dans '+g.length+' scénarios'+(xs.length?' ; écart extrême '+(100*(xs[0]<0?Math.min(...xs):Math.max(...xs))).toFixed(0)+' %':'')+' — graines '+g.slice(0,6).join(', '));V[k].slice(0,3).forEach(v=>console.log('     ['+v.seed+'] '+v.msg));});
  const tot=t=>Object.keys(CAT).filter(k=>k.startsWith(t)).reduce((a,k)=>a+CAT[k],0);
  for(const t of ['SL ','autre ']){const T=tot(t);console.log((t==='SL '?'Sorties longues':'Autres séances')+' faites comme prescrites : '+T);
    Object.keys(CAT).filter(k=>k.startsWith(t)).sort().forEach(k=>console.log('   '+k.slice(t.length).padEnd(28)+String(CAT[k]).padStart(7)+'  '+(100*CAT[k]/T).toFixed(1)+' %'));}
}
