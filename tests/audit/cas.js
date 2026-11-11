/* Audit mission 2 — cas reproductibles, sur le profil d'Antoine au 10/11/2026 (sim_adherence.js : ANTOINE, SES0).
   Chaque cas imprime ce qui est observé sur le moteur v54. Rien n'est modifié.
   Usage : node tests/audit/cas.js [lettre] */
process.env.TZ=process.env.TZ||'Europe/Paris';
const E=require('../engine.js'),S=require('./sim_adherence.js'),{add,days,isRun}=S;
const START='2026-11-02',mon=w=>add(START,(w-1)*7);
const hm=m=>Math.floor(m/60)+' h '+String(Math.round(m%60)).padStart(2,'0');
/* rejoue de S2 à S(fin) ; faire(w, séance) → false (manquée), true (faite comme prescrite) ou un objet séance */
function rejoue(P,ses,fin,faire,lecture,debut){
  for(let w=debut||2;w<=fin;w++){const o=E.build({profile:P,today:add(mon(w),lecture==='lundi'?0:1),sessions:ses,isRun});
    o.sessions.filter(s=>s.date>=mon(w)&&s.date<add(mon(w),7)&&s.type!=='cf').forEach(s=>{
      const f=s.type==='race'?true:(faire?faire(w,s):true);if(f===false){P.manques[s.date]='autre';return;}
      ses.push(typeof f==='object'?f:{date:s.date,type:s.type,dur:s.dur,rpe:s.type==='race'?7:3,dplus:s.dplus||0});});}
  return ses;
}
const plan=(P,ses,today)=>E.build({profile:P,today,sessions:ses,isRun});
const SLsem=(o,w)=>{const x=o.sessions.find(s=>s.type==='long'&&s.date>=mon(w)&&s.date<add(mon(w),7));return x?x.dur:null;};
const CAS={};

CAS.A=()=>{console.log('A — Heure d\'été : le lundi, la semaine écoulée n\'est pas « passée »');
  console.log('   voir tests/audit/t_audit_heure_ete.js (2 défauts reproduits) ; variante sécurité : node tests/audit/fuzz.js 1 1 101');
  console.log('   (graine 101 : sortie longue du 09/08/2026 manquée, plan lu le lundi 10/08 → sortie longue de 170 min pour 140 min réelles dans le mois, +21 %)');};

CAS.B=()=>{console.log('B — Sortie clé consommée sans être faite (S36 : seule l\'endurance est courue)');
  for(const cas of ['S36 entièrement manquée','S36 : endurance faite, sortie clé manquée']){const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),36,(w,s)=>w!==36?true:(cas.includes('entièrement')?false:s.type!=='long'));
    const P2=JSON.parse(JSON.stringify(P));const tout=(()=>{const s2=ses.slice();for(let w=37;w<=47;w++){const o=E.build({profile:P2,today:add(mon(w),1),sessions:s2,isRun});o.sessions.filter(s=>s.date>=mon(w)&&s.date<add(mon(w),7)&&s.type!=='cf').forEach(s=>s2.push({date:s.date,type:s.type,dur:s.dur,rpe:3}));}return s2;})();
    const cles=tout.filter(s=>s.type==='long'&&s.date>=mon(36)&&s.date<mon(45)&&s.dur>=270).map(s=>s.date.slice(5)+' '+hm(s.dur));
    console.log('   '+cas+' → sorties de 4 h 30 ou plus réellement faites ensuite : '+cles.length+' ('+cles.join(', ')+')');}};

CAS.B2=()=>{console.log('B2 — Alternance sur une séance fantôme : sortie longue de 3 h 50 manquée en S18 (endurance faite), que propose S19 ?');
  for(const cas of ['S18 entièrement manquée','S18 : endurance faite, sortie longue manquée']){const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),18,(w,s)=>w!==18?true:(cas.includes('entièrement')?false:s.type!=='long'));
    const o=plan(P,ses,add(mon(19),1));console.log('   '+cas.padEnd(46)+' → S19 : '+hm(SLsem(o,19))+', S20 : '+hm(SLsem(o,20))+' (dernière longue réelle : '+hm(Math.max(...ses.filter(s=>s.type==='long'&&s.date>=mon(15)).map(s=>s.dur)))+' le '+ses.filter(s=>s.type==='long').pop().date+')');}};

CAS.C=()=>{console.log('C — La course en fenêtre masque le besoin de monter (coupure de 4 semaines S3–S6, tout le reste parfait)');
  const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),30,(w)=>!(w>=3&&w<=6));
  const o=plan(P,ses,add(mon(31),1));const ref=Math.max(...ses.filter(s=>isRun(s)&&days(s.date,add(mon(31),6))<=30&&days(s.date,add(mon(31),6))>0).map(s=>s.dur));
  console.log('   S31 (4 semaines après le 50 km) : sortie longue prescrite '+hm(SLsem(o,31))+' ; plus longue des 30 jours = la course, '+hm(ref)+' → la règle autoriserait jusqu\'à '+hm(1.1*ref));
  const s2=rejoue(P,ses,47,null,null,31);const mx=Math.max(...s2.filter(s=>s.type==='long'&&s.date>=mon(36)).map(s=>s.dur));const f=plan(P,s2,P.goalDate);
  console.log('   plus longue sortie du bloc : '+hm(mx)+' (plan sans coupure : 6 h 00) ; alerte d\'écart sur l\'objectif principal : '+(f.ecarts.some(e=>e.obj==='principal')?'oui':'NON')+' ; sur le 50 km : '+(f.ecarts.some(e=>e.obj==='secondaire')?'oui':'non'));};

CAS.E=()=>{console.log('E — L\'affûtage n\'allège pas (2 jours, adhérence parfaite)');
  const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),47);
  for(let w=40;w<=47;w++){const x=ses.filter(s=>s.date>=mon(w)&&s.date<add(mon(w),7)&&s.type!=='race');console.log('   S'+w+' '+mon(w)+' : '+x.map(s=>s.date.slice(8)+'/'+s.date.slice(5,7)+' '+s.type+' '+s.dur).join(', ')+' → '+hm(x.reduce((a,s)=>a+s.dur,0)));}
  console.log('   course le '+P.goalDate+'. Repère S-COU-006 (Bosquet 2007) : volume réduit de 41 à 60 % sur environ 2 semaines.');};

CAS.F=()=>{console.log('F — D-96 : catégorie de pic (Frandsen 2025) des sorties longues du plan, adhérence parfaite');
  for(const sup of [true,false]){const sv=E.CONV.arrondiSup;E.CONV.arrondiSup=sup;const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),47);E.CONV.arrondiSup=sv;
    const c={};let depMax=0;ses.filter(s=>s.type==='long'&&s.date>'2026-11-08').forEach(s=>{const m=Math.max(0,...ses.filter(x=>isRun(x)&&days(x.date,s.date)>0&&days(x.date,s.date)<=30).map(x=>x.dur));
      const x=s.dur/m-1,k=x<=0.1+1e-9?'≤ +10 %':x<=0.3?'+10 à +30 %':'> +30 %';c[k]=(c[k]||0)+1;if(x>0.1&&x<=0.3)depMax=Math.max(depMax,x);});
    console.log('   arrondiSup='+sup+' : '+JSON.stringify(c)+(depMax?' ; plus grand dépassement : +'+(100*depMax).toFixed(1)+' %':''));}};

CAS.G=()=>{console.log('G — Effet de seuil à 8 h sur la durée estimée du 50 km (tranche 4–8 h ou 8–20 h)');
  for(const dur of [107,105]){const P=S.ANTOINE();P.start.lastLong.dur=dur;const o=plan(P,S.SES0(),'2026-11-10');const r=o.sessions.find(s=>s.type==='race'&&s.date==='2027-05-08');
    console.log('   sortie de référence '+dur+' min → 50 km estimé à '+hm(r.dur)+' ; semaines d\'affûtage + récupération autour : '+o.weeks.filter(k=>k.type==='aff_sec').length+' + '+o.weeks.filter(k=>k.type==='recup_sec').length+' ; objectif principal estimé à '+hm(o.info.dureeMain));}};

CAS.H=()=>{console.log('H — Monotonie (D-94) : une course réelle avant le départ annule l\'historique déclaré');
  const base=()=>{const P=S.ANTOINE();P.start={freq4w:2,dur4w:90,lastLong:{date:'2026-10-18',dur:120,dist:14,dplus:400}};return P;};
  const o0=plan(base(),[],'2026-11-03'),o1=plan(base(),[{date:'2026-10-20',type:'ef',dur:15,rpe:3}],'2026-11-03');
  const ef=o=>o.sessions.filter(s=>s.type==='ef'&&s.date<'2026-11-09').map(s=>s.dur).join('+');
  console.log('   déclaré « 2 × 1 h 30 par semaine, dernière longue 2 h le 18/10 », aucune course saisie : S1 = endurance '+ef(o0)+', sortie longue '+SLsem(o0,1)+' min');
  console.log('   même profil + un footing de 15 min saisi le 20/10                               : S1 = endurance '+ef(o1)+', sortie longue '+SLsem(o1,1)+' min');
  const sans=()=>{const P=base();delete P.start.lastLong;return P;};const p0=plan(sans(),[],'2026-11-03'),p1=plan(sans(),[{date:'2026-10-20',type:'ef',dur:15,rpe:3}],'2026-11-03');
  console.log('   sans « dernière longue » déclarée : sortie longue de S1 '+SLsem(p0,1)+' min → '+SLsem(p1,1)+' min avec le footing ; endurance '+ef(p0)+' → '+ef(p1));};

CAS.I=()=>{console.log('I — Dépassement suivi : sortie longue de 2 h prévue, 3 h faites');
  const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),7,(w,s)=>(w===7&&s.type==='long')?{date:s.date,type:'long',dur:180,rpe:5}:true);
  const o=plan(P,ses,add(mon(8),1));console.log('   S7 prévue '+hm(120)+', faite 3 h 00 (+50 % sur la plus longue du mois) → S8 prescrite '+hm(SLsem(o,8))+' ; signal du moteur : '+(o.weeks.find(k=>k.w===7).sympt?'fatigue':'aucun')+' ; garde-fou : '+(o.garde.reasons.filter(r=>/dépass|30 jours|trop/i.test(r)).length?'message':'aucun message'));};

CAS.J=()=>{console.log('J — Le signal de fatigue est relatif : un ressenti toujours haut ne déclenche rien');
  for(const [nom,f] of [['ressenti 7/10 sur toutes les endurances',()=>7],['ressenti 3/10 puis 5/10 en S12',w=>w===12?5:3],['aucun ressenti saisi',()=>null]]){
    const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),16,(w,s)=>({date:s.date,type:s.type,dur:s.dur,rpe:s.type==='ef'||s.type==='qual'?f(w):3}));
    const o=plan(P,ses,add(mon(17),1));console.log('   '+nom.padEnd(42)+' → semaines marquées « fatigue » : '+(o.weeks.filter(k=>k.w<=16&&k.sympt).map(k=>'S'+k.w).join(', ')||'aucune')+' ; sortie longue S17 : '+SLsem(o,17));}};

CAS.K=()=>{console.log('K — Import montre : une sortie longue de moins de 1 h 30 arrive typée « endurance »');
  for(const typ of ['long','ef']){const P=S.ANTOINE();P.races=[];const ses=[{date:'2026-09-27',type:'long',dur:30,rpe:2},{date:'2026-11-08',type:typ,dur:76,rpe:3}];
    rejoue(P,ses,12,(w,s)=>({date:s.date,type:s.type==='long'&&s.dur<90?typ:s.type,dur:s.dur,rpe:3}));
    const o=plan(P,ses,add(mon(13),1));console.log('   sorties longues < 1 h 30 enregistrées « '+typ+' » : niveau retenu par le moteur en S12 = '+o.weeks.find(k=>k.w===12).niv+' min ; ressenti de ces sorties compté comme endurance : '+(typ==='ef'?'oui':'non'));}};

CAS.M=()=>{console.log('M — Maladie : 3 semaines sans courir à partir de S33 (niveau 4 h 35), puis reprise');
  const P=S.ANTOINE(),ses=rejoue(P,S.SES0(),35,(w)=>!(w>=33&&w<=35));
  const o=plan(P,ses,add(mon(36),1));const s=o.sessions.filter(x=>x.date>=mon(36)&&x.date<add(mon(38),7)&&x.type!=='cf').map(x=>x.date.slice(5)+' '+x.type+' '+x.dur).join(', ');
  console.log('   reprise prescrite S36–S38 : '+s);console.log('   alerte d\'écart : '+JSON.stringify(o.ecarts.map(e=>[e.obj,e.atteint+'/'+e.cible]))+' ; messages du garde-fou : '+o.garde.reasons.length);
  const P2=S.ANTOINE(),ses2=rejoue(P2,S.SES0(),38,(w)=>!(w>=33&&w<=38));const o2=plan(P2,ses2,add(mon(39),1));
  console.log('   même chose avec 6 semaines (blessure) : reprise S39 = '+o2.sessions.filter(x=>x.date>=mon(39)&&x.date<add(mon(39),7)&&x.type!=='cf').map(x=>x.type+' '+x.dur).join(', ')+' ; projection de la plus longue sortie avant la course : '+hm(Math.max(...o2.sessions.filter(x=>x.type==='long'&&x.date>=mon(39)).map(x=>x.dur)))+' ; écart principal signalé : '+(o2.ecarts.some(e=>e.obj==='principal')?'oui':'non'));};

const lettre=process.argv[2];
Object.keys(CAS).filter(k=>!lettre||k===lettre).forEach(k=>{try{CAS[k]();}catch(e){console.log(k+' : erreur '+e.message);}console.log('');});
