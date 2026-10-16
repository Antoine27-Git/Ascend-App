/* ---------- moteur de plan (v1 : refonte D-67/D-68 ; règles v0 conservées derrière regles:'v1') ----------
   Port de sim8.py (règles v1 : D-63, D-65a/b/d) + GABARIT-TRAIL.md.
   Fonctions pures : entrée = profil + séances réalisées + statuts du jour + date du jour,
   sortie = calendrier, semaines, séances prescrites, garde-fou. Aucun accès à l'écran ni au stockage.
   Couche A (gabarit) : types de séances, sous-phases, progressions. Couche B (G-PLA-002) : volume.
   Couche C (sécurité) : règle des 30 jours, une seule séance de progression, journées dures. */
const ENGINE=(function(){
'use strict';
const PLANCHER=30,SEUIL=1.10,FENETRE=30,EPS=0.01,GRANDE=180,MARGE=3;
const PART={fond:0.325,bloc:0.375,pic:0.425,affutage:0.40};
const TRANCHES={
  '4-8h':{bloc:7,pic:3,affutage:2,n_cles:3,part_cle:0.60,aff:[0.65,0.45],cible:[210,270],plafond_pic:10,recup:2,min:24,confort:32},
  '8-20h':{bloc:9,pic:3,affutage:3,n_cles:3,part_cle:0.65,aff:[0.70,0.55,0.40],cible:[300,360],plafond_pic:11,recup:3,min:36,confort:52}};
const TR_COURT={aff:[0.65,0.45],recup:2};
/* D-70 : conventions réglables (H-42, H-44) — une seule table, pour tous les objectifs */
const CONV={
  moyenneMax:180,            /* sortie longue d'une semaine « moyenne » : 3 h au plus (seuil de D-22a) */
  samRatio:2/3,              /* samedi d'un week-end de choc : au plus 2/3 de la sortie longue */
  samMax:d=>d>=1200?240:180, /* … et au plus 3 h (4 h pour une course de 20 h ou plus) */
  secPart:0.5,secMax:270,    /* objectif secondaire : sortie longue cible = 50 % de sa durée, 4 h 30 au plus */
  chocsPrincipal:3,          /* week-ends de choc avant l'objectif principal, sur les semaines de sortie clé */
  chocsSecondaire:1,         /* avant un objectif secondaire exigeant, 4 à 6 semaines avant */
  secExigeant:(dur,dist,dplus)=>dur>=240||(dist>0&&dplus/dist>=30),
  efMax:{'4-8h':90,'8-20h':90}};   /* D-29 : endurance ≤ 1 h 30 pour les programmes longs (< 4 h : gabarit court non écrit, tranche 4–8 h appliquée) */  /* « beaucoup de dénivelé » : 30 m/km et plus */
/* ressenti : RPE moyen des séances faciles → échelle du simulateur. 1 point de RPE = dérive 0,12 (H-38, à calibrer). */
const RPE_REF=3,RPE_K=0.12;
const DAY=864e5;
function D(s){const p=s.split('-').map(Number);return new Date(p[0],p[1]-1,p[2]);}
function I(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function add(s,n){const d=D(s);d.setDate(d.getDate()+n);return I(d);}
function mon(s){const d=D(s);d.setDate(d.getDate()-((d.getDay()+6)%7));return I(d);}
const off=dow=>(dow+6)%7;                       /* jour de la semaine → décalage depuis lundi */
const med=a=>{const b=a.slice().sort((x,y)=>x-y),n=b.length;return n?(n%2?b[(n-1)/2]:(b[n/2-1]+b[n/2])/2):null;};

/* ---- arrondi (D-65d) : 1-2-3 → 0, 4-5-6 → 5, 7-8-9 → 10 dès 50 min ; minute en dessous ;
   jamais au-dessus du plafond ; la séance de progression qui y bute s'affiche à la minute */
function regle(m){const mi=Math.floor(m+0.5-1e-9),d=mi%10;return mi-d+(d<=3?0:d<=6?5:10);}
function arrondi(m,plafond,fin){
  if(m<=0)return 0;
  if(m>=50-EPS){let r=regle(m);
    if(plafond!=null&&r>plafond+EPS)r=fin?Math.floor(plafond+1e-9):(plafond>=50-EPS?5*Math.floor(plafond/5+1e-9):Math.floor(plafond+1e-9));
    return Math.max(r,0);}
  let r=Math.floor(m+0.5-1e-9);
  if(plafond!=null&&r>plafond+EPS)r=Math.floor(plafond+1e-9);
  return Math.max(r,0);
}
function tranche_de(min){return min>=480?'8-20h':min>=240?'4-8h':'<4h';}
function echeance(min){const plaf=min>=480?300:min>=240?210:180;return Math.min(min,plaf*SEUIL)/SEUIL;}
/* durée de course estimée : km-effort et loi de Riegel (exposant 1,07) sur la course de référence (extrapolation) */
function dureeCourse(dist,dplus,ref){
  const ke=(dist||0)+(dplus||0)/100;if(!ke)return null;
  if(ref&&ref.dur&&ref.dist){const kr=ref.dist+(ref.dplus||0)/100;return ref.dur*Math.pow(ke/kr,1.07);}
  return ke/7*60;                              /* sans référence : 7 km-effort/h, prudent */
}

/* ---- G-PLA-002 (port de ModeleBloc, règles v1) ---- */
function Modele(v0,plafond){return {volume:v0,plafond,cap:0.20,pas:0.5,cadence:3,sdr:0,base:null,ech:[],casse:null,sdc:0,sains:0,
  conso:false,gel:null,sympt:false,relDem:false,repos:[],baseInit:null,saisies:[],alerte:null,preuves:0,muet:false};}
function pasProg(m){
  if(m.casse==null)return Math.max(m.volume*(1+m.cap),m.volume+m.pas);
  if(m.sains>=4&&!m.conso){m.casse*=1.08;m.sains=0;}
  const marge=(m.casse-m.volume)/Math.max(m.casse,0.1);if(marge<=0)return m.volume;
  const f=Math.min(1,marge*2);return Math.max(m.volume*(1+m.cap/2*f),m.volume+m.pas/2*f);
}
function ajuste(m,r,saut,relache,execute){
  m.sympt=false;m.etat='prog';const manque=r==null;m.saisies.push(!manque);
  if(manque){
    if(m.casse==null&&m.saisies.length>=8&&m.saisies.slice(-8).filter(Boolean).length<=4){m.casse=m.volume;m.muet=true;}
    r=m.base!=null?m.base:1;
  }else m.ech.push(r);
  if(m.ech.length<4&&m.saisies.length<4){m.sdr+=relache?0:1;return;}
  if(m.base==null){
    if(m.ech.length>=4){const e=m.ech.slice(0,4).sort((a,b)=>a-b);m.base=(e[1]+e[2])/2;}
    else if(manque)m.base=r;
    else{m.sdr+=relache?0:1;return;}
  }
  const derive=r/m.base-1;
  if(relache){
    m.sdr=0;m.relDem=false;
    if(!manque){m.repos.push(r);
      let nb=med(m.ech.slice(0,4).sort((a,b)=>a-b).slice(1,3).concat(m.repos.slice(-6)));
      if(m.baseInit==null)m.baseInit=m.base;nb=Math.min(nb,m.baseInit*1.05);m.base=nb;
      if(m.alerte){const a=m.alerte;if(a.saut===0&&a.r/nb-1<=0.12){m.casse=a.niv;m.alerte=null;}}}
    return;
  }
  m.sdr+=1;
  if(saut>0||derive>0.12+1e-9){
    m.sympt=true;m.alerte={r,saut,niv:m.casse,v:execute!=null?execute:m.volume};m.preuves=0;
    if(execute!=null)m.volume=Math.min(m.volume,execute);
    m.casse=m.casse==null?m.volume:Math.min(m.casse,m.volume);m.sdc=0;
    m.volume*=0.92;m.sdr=m.cadence;m.relDem=true;m.sains=0;m.etat='sympt';
  }else if(derive<0.05){
    if(m.alerte&&execute!=null&&execute>=0.95*m.alerte.v)m.preuves++;
    m.sdc++;
    if(m.casse!=null&&m.sdc>=10&&!m.conso){m.casse*=1.10;m.sdc=0;}
    m.sains++;
    let nv=Math.min(m.plafond,pasProg(m));if(m.gel!=null)nv=Math.min(nv,Math.max(m.volume,m.gel));
    m.volume=nv;
  }else m.etat='maintien';
}

/* ---- calendrier (D-21, D-63f) + sous-phases du fond (gabarit § 2.2) ---- */
function Calendrier(N,tr){
  const c={N,aff:tr.aff.length};c.bloc=Math.min(tr.bloc,Math.max(0,N-c.aff-2));c.fond=N-c.aff-c.bloc;
  c.pic=Math.min(tr.pic,c.bloc);c.T=c.fond+c.bloc+1;c.grille=new Set();
  for(let k=1;k<40;k++)if(c.T-4*k>=2)c.grille.add(c.T-4*k);
  c.phase=w=>w<=c.fond?'fond':w<c.T-c.pic?'bloc':w<c.T?'pic':'affutage';
  /* F4 6, F3 8, F1 ≤ 8 ; compression : F2, puis F3 → 6, F4 → 4, F1 → 4 */
  let f1=8,f3=8,f4=6,f2=c.fond-f1-f3-f4;
  if(f2<0){f2=0;let rest=c.fond;f4=Math.min(6,rest);rest-=f4;f3=Math.min(8,Math.max(0,rest-4));rest-=f3;f1=rest;
    if(f1<4){const need=4-f1;const t3=Math.min(need,Math.max(0,f3-6));f3-=t3;f1+=t3;
      if(f1<4){const t4=Math.min(4-f1,Math.max(0,f4-4));f4-=t4;f1+=t4;}}}
  c.sp={f1,f2,f3,f4};
  c.sous=w=>{if(w>c.fond)return null;if(w<=f1)return 'F1';if(w<=f1+f2)return 'F2';if(w<=f1+f2+f3)return 'F3';return 'F4';};
  return c;
}
function relachesPrevues(c,w,derniere,charges,forcees){
  const out=new Set();
  for(let x=w;x<c.T;x++){
    if(forcees.has(x)){derniere=x;charges=0;continue;}
    if((c.grille.has(x)&&x-derniere>=3)||(charges>=4&&c.phase(x)!=='pic')){out.add(x);derniere=x;charges=0;}else charges++;
  }
  return out;
}
function atteint(mx,besoin,slots,c,trou){
  let v=Math.max(mx,PLANCHER),dernier=-9,passe=false;
  for(const x of slots){
    if(trou&&!passe&&x>trou[1]){v=Math.max(PLANCHER,trou[2]*v);passe=true;}
    if(v>=besoin-EPS)return true;
    const nv=arrondi(v*SEUIL,v*SEUIL,true);
    if(nv>GRANDE&&c.phase(x)==='fond'&&x-dernier<2)continue;
    v=nv;if(nv>GRANDE)dernier=x;
  }
  return v>=besoin-EPS;
}
function max30(hist,jour,reprise){
  let m=0;for(const h of hist)if(h.j>=jour-FENETRE&&h.j<jour&&h.d>m)m=h.d;
  if(reprise&&reprise[0]<=jour&&jour<reprise[0]+FENETRE)m=Math.max(m,reprise[1]);
  return m;
}

/* ---- contenu des séances (gabarit § 4) ---- */
const PROG={
  accel:[[4,15],[4,15],[6,20],[6,20],[6,20]],
  sprint:[[6,10],[6,10],[8,10],[8,10],[8,12],[10,12]],
  courtes:[[6,30],[6,30],[8,30],[8,30],[6,45],[6,45],[8,60]],
  me:[[5,30],[5,30],[8,40],[10,40],[12,50],[15,50],[15,60],[15,60]],
  inter:[[5,120],[4,180],[5,180],[5,240],[6,240],[6,240]],
  tempo:[[3,8],[3,10],[3,12],[2,20]],
  spe:[45,60,75,90]};
const pick=(t,i)=>t[Math.min(i,t.length-1)];
function qualite(kind,idx,slot){
  const E=(n,min,o)=>Object.assign({n,min,lo:null,hi:null,int:0},o||{});
  const fin=(work,warm)=>{const r=Math.round(slot-work-warm-10);return r>=10?[E('Endurance facile',r,{int:2}),E('Retour au calme',10,{int:3})]:[E('Retour au calme',Math.max(5,Math.round(slot-work-warm)),{int:3})];};
  if(kind==='sprint'||kind==='courtes'){const p=pick(PROG[kind],idx),sec=p[1],rec=kind==='sprint'?150:Math.max(90,sec*2);
    const work=Math.round(p[0]*(sec+rec)/60);
    return {title:(kind==='sprint'?'Sprints en côte':'Côtes courtes')+' '+p[0]+' × '+sec+' s',
      steps:[E('Échauffement',15,{int:2}),{rep:p[0],on:{n:'Montée',sec,int:5},off:{n:'Redescente en marchant',sec:rec,int:1}}].concat(fin(work,15)),
      need:work+25,notes:[kind==='sprint'?'Côte raide, vite mais relâché, récupération complète en redescendant en marchant. C\'est un travail de force, pas de souffle.':'Effort soutenu en côte, 105 % de ta vitesse critique ou ressenti 8/10. Redescente tranquille.']};}
  if(kind==='me'){const p=pick(PROG.me,idx);
    return {title:'Endurance musculaire · montée lestée '+p[1]+' min',steps:[E('Échauffement',10,{int:2}),E('Montée lestée ('+p[0]+' % du poids)',p[1],{int:2})].concat(fin(p[1],10).map(x=>x.n==='Endurance facile'?Object.assign(x,{n:'Endurance facile, sac vidé'}):x)),
      need:p[1]+20,notes:['Côte raide, sac lesté à '+p[0]+' % de ton poids. Ce sont les jambes qui limitent, pas le souffle.','Vide l\'eau du sac en haut pour épargner la descente. Sans relief : montées sur box lestées, même durée.']};}
  if(kind==='inter'){const p=pick(PROG.inter,idx),sec=p[1];const work=Math.round(p[0]*sec*2/60);
    return {title:'Intervalles en côte '+p[0]+' × '+(sec/60)+' min',steps:[E('Échauffement',15,{int:2}),{rep:p[0],on:{n:'Montée',sec,int:4},off:{n:'Descente tranquille',sec,int:1}}].concat(fin(work,15)),
      need:work+25,notes:['Montée régulière, ressenti 9/10, même effort sur chaque fraction. Récupération en descendant tranquillement, jamais de fraction en descente.']};}
  if(kind==='tempo'){const p=pick(PROG.tempo,idx);const work=p[0]*(p[1]+3);   /* le bloc répété compte aussi la récupération de la dernière fraction */
    return {title:'Tempo en montée '+p[0]+' × '+p[1]+' min',steps:[E('Échauffement',15,{int:2}),{rep:p[0],on:{n:'Tempo en montée',sec:p[1]*60,int:4},off:{n:'Récupération',sec:180,int:1}}].concat(fin(work,15)),
      need:work+25,notes:['Effort soutenu mais contrôlé, ressenti 7 à 8/10, au seuil.']};}
  if(kind==='spe'){const t=pick(PROG.spe,idx);
    return {title:'Montée spécifique '+t+' min',steps:[E('Échauffement',15,{int:2}),E('Montées à l\'effort de course',t,{int:3})].concat(fin(t,15)),
      need:t+20,notes:['Montées longues à l\'effort de ta course, courues ou marchées selon la pente. Travaille aussi la descente.']};}
  if(kind==='rappel')return {title:'Rappel d\'allure · 3 × 5 min',steps:[E('Échauffement',15,{int:2}),{rep:3,on:{n:'Allure de course',sec:300,int:3},off:{n:'Récupération',sec:120,int:1}}].concat(fin(21,15)),
      need:40,notes:['Juste pour garder le rythme de course, sans fatigue.']};
  return null;
}
const RENFO={F1:'Stabilité, gainage, dos, force générale légère',F2:'Force maximale : 3 à 5 séries de 3 à 5 répétitions lourdes (squat, soulevé de terre, step-up, mollets)',
  F3:'Force en entretien (1 série lourde par mouvement)',F4:'Force en entretien',bloc:'Force, puis entretien',pic:'Pliométrie et excentrique (sauts, descentes de marche lentes)',affutage:'Séance légère, mobilité'};

/* ---- construction ---- */
function build(inp){
  const P=inp.profile,today=inp.today,sessions=(inp.sessions||[]).filter(s=>s.date),isRun=inp.isRun,isOff=inp.isOff||(()=>false);
  const out={ok:false,weeks:[],sessions:[],garde:{level:0,reasons:[]},info:{}};
  const G=(l,t)=>{out.garde.level=Math.max(out.garde.level,l);out.garde.reasons.push(t);};
  const Dy=P.days||{},run=(Dy.run||[]).slice();
  if(!P.goalDate){G(2,'Renseigne la date de ton objectif dans Profil : le plan se construit à rebours depuis elle.');return out;}
  if(!run.length){G(2,'Choisis tes jours de course dans Profil.');return out;}
  const start=mon(P.planStart||today),raceMon=mon(P.goalDate),from=P.planFrom&&P.planStart?P.planFrom:start;   /* pas de séance avant le jour de démarrage */
  const N=Math.round((D(raceMon)-D(start))/(7*DAY))+1;
  if(N<6){G(2,'Moins de 6 semaines avant ton objectif : pas de préparation à construire.');return out;}
  /* durée de course et tranche */
  const St=P.start||{},okL=St.lastLong&&St.lastLong.dur&&St.lastLong.dist;
  const races=(St.pastRaces||[]).filter(r=>r&&r.dur&&r.dist);
  let refC=null;
  if(races.length){const keT=(P.goalDist||0)+(P.goalDplus||0)/100;
    refC=races.reduce((best,r)=>{const ke=r.dist+(r.dplus||0)/100,d=Math.abs(Math.log(Math.max(ke,0.1)/Math.max(keT,0.1)));
      return (best==null||d<best.d)?{r,d}:best;},null).r;}
  else if(okL)refC=St.lastLong;
  const dMain=dureeCourse(P.goalDist,P.goalDplus,refC);
  let trName=dMain?tranche_de(dMain):'8-20h';
  if(trName==='<4h'){trName='4-8h';G(1,'Objectif estimé à moins de 4 h : le gabarit court n\'est pas encore écrit, j\'applique celui des 4–8 h.');}
  if(inp.regles!=='v1'&&dMain&&dMain>=1200)G(1,'Objectif estimé à 20 h ou plus : le gabarit de cette durée n\'est pas encore écrit, j\'applique celui des 8–20 h (sorties clés de 5 à 6 h). Seul le samedi des week-ends de choc est adapté (4 h au plus).');
  if(!dMain)G(1,'Distance de l\'objectif manquante : tranche 8–20 h par défaut.');
  if(!refC)G(1,'Aucune course ou sortie de référence déclarée : la durée de ton objectif est estimée à 7 km-effort par heure.');
  const tr=TRANCHES[trName],c=Calendrier(N,tr);
  out.info={N,start,trName,dureeMain:dMain,cal:c,refUsed:races.length>1?refC:undefined};
  if(N<tr.min)G(1,'Préparation de '+N+' semaines pour la tranche '+trName+' : en dessous du minimum de '+tr.min+' semaines (D-21). Le plan est compressé.');
  let n=run.length,longDow=run.includes(+Dy.long)?+Dy.long:run[run.length-1],offSL=off(longDow);
  let autresDows=run.filter(d=>d!==longDow).sort((a,b)=>off(a)-off(b));
  let DyW=Dy;const tcap=dow=>{if(inp.regles!=='v1')return null;const t=(DyW.time||{})[dow];return t?+t:null;};   /* D-71 : ignoré en v2 (l'endurance est plafonnée par CONV.efMax, la sortie longue par sa progression) */
  const strength=!!(P.modules&&P.modules.strength);let cfDays=strength?(Dy.cf||[]).slice():[],renfo2=strength&&cfDays.length>=2;
  /* D-68 : organisation par phase (attachée aux phases, pas aux dates) et versions passées (le passé ne se réécrit jamais) */
  const V2=inp.regles!=='v1',ORD=['F1','F2','F3','F4','bloc','pic','affutage'];
  const okOrg=o=>o&&ORD.includes(o.from)&&o.days&&(o.days.run||[]).length;
  const cfgNow={days:Dy,orgs:V2&&Array.isArray(P.orgs)?P.orgs.filter(okOrg):[]};
  /* versions passées : {until, days, orgs} ; une semaine antérieure à until garde l'organisation de sa version */
  const versions=V2&&Array.isArray(P.orgHist)?P.orgHist.filter(v=>v&&v.until&&v.days&&(v.days.run||[]).length).map(v=>({until:v.until,days:v.days,orgs:(v.orgs||[]).filter(okOrg)})).sort((a,b)=>a.until<b.until?-1:1):[];
  if(run.length<3){const o3=cfgNow.orgs.find(o=>o.days.run.length>=3);
    G(1,o3?'Moins de 3 jours de course par semaine jusqu\'à ta phase « '+({F1:'Reprise',F2:'Base',F3:'Endurance musculaire',F4:'Intensité en côte',bloc:'Bloc spécifique',pic:'Pic',affutage:'Affûtage'}[o3.from])+' », où tu passes à '+o3.days.run.length+' jours.':'Moins de 3 jours de course par semaine : peu de place pour construire le volume d\'un ultra.');}
  const orgDe=(monW,ph,sp)=>{const cfg=versions.find(x=>monW<x.until)||cfgNow;
    const k=ORD.indexOf(ph==='fond'?sp:ph);let d=cfg.days,en=false,pos=-1;
    cfg.orgs.forEach(o=>{const i=ORD.indexOf(o.from);if(i<=k&&i>=pos){d=o.days;en=!!o.enchaine;pos=i;}});return {d,en};};
  const appliqueOrg=o=>{DyW=o.d;const r=(o.d.run||[]).slice();n=r.length;longDow=r.includes(+o.d.long)?+o.d.long:r[r.length-1];offSL=off(longDow);
    autresDows=r.filter(d=>d!==longDow).sort((a,b)=>off(a)-off(b));cfDays=strength?(o.d.cf||[]).slice():[];renfo2=strength&&cfDays.length>=2;};
  const gap=(a,b)=>Math.min((a-b+7)%7,(b-a+7)%7);
  /* courses intermédiaires : A/B = objectif secondaire (affûtage + récupération), C = course-entraînement */
  const secs=[];
  (P.races||[]).forEach(r=>{if(!r.date)return;const w=Math.round((D(mon(r.date))-D(start))/(7*DAY))+1;if(w<1||w>=N)return;
    const dur=dureeCourse(r.dist,r.dplus,refC)||120;let statut=r.prio==='C'?'entrainement':'objectif';
    const t2=TRANCHES[tranche_de(dur)]||TR_COURT;
    if(statut==='objectif'&&(w+t2.recup>c.fond)){statut='entrainement';G(1,(r.name||'Course')+' tombe dans le bloc spécifique : traitée en course-entraînement, sans affûtage ni récupération (D-25).');}
    secs.push({w,date:r.date,dur,statut,name:r.name||'Course',t2,exigeant:CONV.secExigeant(dur,+r.dist||0,+r.dplus||0)});});
  const secAff={},secRec=new Set();
  secs.filter(s=>s.statut==='objectif').forEach(s=>{s.t2.aff.forEach((f,k)=>{secAff[s.w-s.t2.aff.length+1+k]=f;});for(let k=1;k<=s.t2.recup;k++)secRec.add(s.w+k);});
  const forcees=new Set(Object.keys(secAff).map(Number).concat([...secRec]));
  const budget=forcees.size/N;if(budget>0.20)G(1,'Objectifs secondaires : '+Math.round(budget*100)+' % de la préparation en affûtage et récupération, au-delà des 20 % de D-25.');
  /* historique et volume de départ : séances réelles avant le plan, sinon la déclaration */
  const jourOf=s=>Math.round((D(s)-D(start))/DAY);
  let hist=[];
  const before=sessions.filter(s=>isRun(s)&&s.date<start&&s.date>=add(start,-35));
  before.forEach(s=>hist.push({j:jourOf(s.date),d:s.dur||0,t:'reel'}));
  let vol0=null;
  if(before.length){const wk=sessions.filter(s=>isRun(s)&&s.date<start&&s.date>=add(start,-28));vol0=wk.reduce((a,s)=>a+(s.dur||0),0)/60/4;}
  else if(St.freq4w){vol0=St.freq4w*(St.dur4w||0)/60;
    const lr=PART.fond*vol0*60,aut=(vol0*60-lr)/Math.max(1,n-1);
    for(let w=-3;w<=0;w++){autresDows.forEach(d=>hist.push({j:(w-1)*7+off(d),d:aut,t:'declare'}));hist.push({j:(w-1)*7+offSL,d:lr,t:'declare'});}}
  else if(!St.freq4w&&St.pauseSince&&St.pauseSince!=='gt6'&&St.beforeFreq){
    const f=St.pauseSince==='lt2'?0.65:0.50;vol0=St.beforeFreq*(St.beforeDur||0)/60*f;
    G(1,'Reprise après une interruption : volume de départ réduit à '+Math.round(f*100)+' % de ton volume d\'avant (H-40, extrapolation).');}
  if(St.lastLong&&St.lastLong.date&&St.lastLong.dur&&St.lastLong.date<start)hist.push({j:jourOf(St.lastLong.date),d:+St.lastLong.dur,t:'declare'});
  vol0=vol0||0;
  let vDep=vol0;if(vol0*60<Math.min(3,n)*PLANCHER-EPS)vDep=Math.min(3,n)*PLANCHER/60;   /* D-65b */
  const m=Modele(vDep,tr.plafond_pic);
  /* réalisé par semaine */
  const todayW=Math.floor((D(today)-D(start))/(7*DAY))+1;
  const runsW={};sessions.forEach(s=>{if(!isRun(s))return;const w=Math.floor((D(s.date)-D(start))/(7*DAY))+1;(runsW[w]=runsW[w]||[]).push(s);});
  /* densité de D+ (m/h) : sorties réelles récentes → déclaration → 150 ; rejoint celle de la course à la fin du fond */
  /* D-75 : en v2, point de départ figé — sorties longues et courses des 8 semaines AVANT le démarrage du plan.
     Après le démarrage, le D+ réalisé suit ce que le plan prescrit (endurances sur terrain roulant, repère de D+ en sortie longue) :
     le relire ferait tourner le plan en boucle sur ses propres consignes (A-02). La montée vers la densité de course reste linéaire. */
  const recent=V2?sessions.filter(s=>isRun(s)&&s.dplus&&s.dur&&(s.type==='long'||s.type==='race')&&s.date>=add(start,-56)&&s.date<start)
    :sessions.filter(s=>isRun(s)&&s.dplus&&s.dur&&s.date>=add(today,-56));
  let dens0=recent.length?recent.reduce((a,s)=>a+s.dplus,0)/(recent.reduce((a,s)=>a+s.dur,0)/60):(!St.noLong&&St.lastLong&&St.lastLong.dplus&&St.lastLong.dur?St.lastLong.dplus/(St.lastLong.dur/60):150);
  const densC=P.goalDplus&&dMain?P.goalDplus/(dMain/60):dens0;
  /* GABARIT § 5 : le D+ monte pendant le fond. Départ à la moitié au plus de la densité de course (H-41, extrapolation) */
  dens0=Math.min(dens0,densC*0.5);
  const dens=w=>w>=c.fond?densC:dens0+(densC-dens0)*w/Math.max(1,c.fond);
  const terr=P.terrain||{};
  if(terr.climb&&['lt1','1-5'].includes(terr.climb)&&terr.mountain==='jamais')
    G(1,'Tes montées les plus longues sont courtes et tu n\'as pas d\'accès régulier à la montagne : le bloc spécifique s\'appuiera sur des répétitions de côte, et quelques sorties en moyenne montagne pendant le bloc feront une vraie différence.');
  if(tcap(longDow)&&tcap(longDow)<tr.cible[0])G(1,'Temps disponible le '+['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'][longDow]+' : '+tcap(longDow)+' min, pour une sortie clé de '+tr.cible[0]+' min au moins.');

  let niv=null,enW=false,lrGel=0,chocsP=0;const chocsS={};   /* D-67 : niveau de sortie longue atteint */
  let derniereRel=0,charges=0,clesFaites=0,derniereCle=-99,lrPrec=null,arretC=0,ref=null,ref2=null,volsCharge=[],dernierExec=null,reprise=null,maxAvant=0,maxSec=0;
  const cnt={};const cntDone={};
  /* écart n° 5 : dernière sortie longue déclarée, sortie de la fenêtre des 30 jours depuis moins de 8 semaines → repère de reprise dégressif (même règle qu'une interruption, H-40) */
  if(V2&&St.lastLong&&St.lastLong.dur&&St.lastLong.date&&St.lastLong.date<start&&!before.some(s=>s.date>=add(start,-FENETRE))){
    const age=-jourOf(St.lastLong.date);if(age>=FENETRE-7&&age<FENETRE+56){const k=Math.max(0,Math.ceil((age-FENETRE+7)/7));reprise=[0,Math.max(0.65,1-0.07*k)*St.lastLong.dur];}}
  for(let w=1;w<=N;w++){
    const ph=c.phase(w),sp=c.sous(w),monW=add(start,(w-1)*7),past=w<todayW,cur=w===todayW;
    if(V2){const o=orgDe(monW,ph,sp);appliqueOrg(o);enW=o.en;}
    const reels=runsW[w]||[];
    /* interruption réelle : semaine passée sans aucune course */
    if(past&&!reels.length&&!forcees.has(w)&&ph!=='affutage'){
      if(arretC===0)maxAvant=max30(hist,(w-1)*7,reprise);
      arretC++;out.weeks.push({w,mon:monW,phase:ph,sous:sp,type:'arret',V:0});continue;}
    if(arretC){const f=Math.max(0.65,1-0.07*(arretC-1));reprise=[(w-1)*7,f*maxAvant];m.volume*=f;
      if(m.casse!=null)m.casse*=f;else if(arretC>=2)m.casse=m.volume/f;
      derniereRel=w-1;charges=0;m.sdr=0;m.relDem=false;arretC=0;}
    if(forcees.size){const d0=Math.min(...forcees),d1=Math.max(...forcees);
      if(w===d0)maxSec=max30(hist,(w-1)*7,reprise);
      if(w===d1+1){reprise=[(w-1)*7,Math.max(0.65,1-0.07*(d1-d0))*maxSec];}}
    const aff=ph==='affutage',sAff=(w in secAff)&&!aff&&ph==='fond',sRec=secRec.has(w)&&!aff&&ph==='fond';
    let V,relache;
    if(aff){if(ref==null)ref=volsCharge.length?med(volsCharge.slice(-3)):m.volume;V=ref*tr.aff[Math.min(w-c.T,tr.aff.length-1)];relache=false;}
    else if(sAff){if(ref2==null)ref2=volsCharge.length?med(volsCharge.slice(-3)):m.volume;V=ref2*secAff[w];relache=true;}
    else if(sRec){ref2=null;V=(V2?[0.35,0.55,0.75][Math.min([...secRec].filter(x=>x<=w).length,3)-1]:0.6)*m.volume;relache=true;}
    else{relache=m.relDem||relachesPrevues(c,w,derniereRel,charges,forcees).has(w);
      m.conso=ph==='bloc'||ph==='pic';
      if(m.conso&&m.gel==null&&m.casse==null){m.gel=(!V2&&dernierExec)?Math.min(m.volume,dernierExec):m.volume;m.volume=m.gel;}
      V=m.volume*(relache?0.6:1);if(relache)V=Math.max(V,Math.min(m.volume,2*PLANCHER/60));}
    const gele=aff||sAff||sRec,courseSem=w===N&&aff;
    let cle=false;if(!gele&&!relache&&(ph==='bloc'||ph==='pic'))cle=tr.n_cles>clesFaites&&w-derniereCle>=2&&w<=c.T-1;
    const secIci=secs.find(s=>s.w===w)||null;
    const part=p=>Math.max(PART[p],1/n);
    const doitMonter=mx=>{
      const futRel=relachesPrevues(c,w,derniereRel,charges,forcees),charge=[];for(let x=w;x<c.T;x++)if(!futRel.has(x)&&!forcees.has(x))charge.push(x);
      const clesPrev=[];let dern=derniereCle;for(const x of charge)if((c.phase(x)==='bloc'||c.phase(x)==='pic')&&clesPrev.length<tr.n_cles-clesFaites&&x-dern>=2){clesPrev.push(x);dern=x;}
      const ech=[];if(clesPrev.length)ech.push([clesPrev[clesPrev.length-1],tr.cible[0]/SEUIL]);
      secs.forEach(s=>{if(V2&&s.statut!=='objectif')return;if(s.w>=w){const lim=s.statut==='objectif'?Math.min(s.w,...Object.keys(secAff).map(Number).filter(x=>x<=s.w&&x>s.w-4)):s.w;ech.push([lim,V2?Math.min(CONV.secPart*s.dur,CONV.secMax)/SEUIL:echeance(s.dur)]);}});
      for(const [sem,besoin] of ech){if(mx>=besoin-EPS)continue;
        const slots=charge.filter(x=>x<sem&&(c.phase(x)==='fond'||clesPrev.includes(x))),futurs=slots.filter(x=>x>w),utiles=futurs.slice(0,Math.max(0,futurs.length-MARGE));
        let trou=null;if(forcees.size&&w<=Math.max(...forcees)){const d0=Math.min(...forcees),d1=Math.max(...forcees);trou=[d0,d1,Math.max(0.65,1-0.07*(d1-d0))];}
        if(!atteint(mx,besoin,utiles,c,trou))return besoin;}
      return false;};
    const aEntretenir=mx=>{const jour=(w-1)*7+offSL;let last=null;for(const h of hist)if(h.d>=mx-EPS&&h.j>=jour-FENETRE&&h.j<jour)last=last==null?h.j:Math.max(last,h.j);
      const age=jour-(last==null?jour:last);if(age<14)return null;
      const b=[];if(tr.n_cles>clesFaites)b.push(tr.cible[0]/SEUIL);secs.forEach(s=>{if(s.w>w)b.push(echeance(s.dur));});
      const ok=b.filter(x=>x<=SEUIL*mx+EPS);return ok.length?arrondi(Math.min(Math.max(...ok),mx)):null;};
    const cibleLr=mx=>{const cap=Math.max(PLANCHER,SEUIL*mx);
      if(aff||sAff)return Math.min(cap,part('affutage')*V*60);
      if(relache)return Math.min(cap,part(ph)*V*60);
      if(cle)return Math.min(cap,tr.cible[1],tr.part_cle*V*60);
      if(ph==='fond'&&doitMonter(mx)){if(lrPrec!=null&&lrPrec>GRANDE&&SEUIL*mx>GRANDE)return Math.min(cap,part(ph)*V*60);return Math.min(cap,tr.part_cle*V*60);}
      const niv=ph==='fond'?aEntretenir(mx):null;
      if(niv&&niv>part(ph)*V*60&&!(lrPrec!=null&&lrPrec>GRANDE&&niv>GRANDE))return Math.min(niv,tr.part_cle*V*60);
      return Math.min(cap,part(ph)*V*60);};
    /* D-67 : la sortie longue suit sa propre progression ; le volume de la semaine en est la conséquence */
    const cibleLr2=mx=>{const cap=Math.max(PLANCHER,SEUIL*mx);if(niv==null)niv=Math.max(PLANCHER,Math.min(mx,cap));
      if(aff)return Math.min(cap,niv*tr.aff[Math.min(w-c.T,tr.aff.length-1)]);
      if(sAff)return Math.min(cap,niv*secAff[w]);
      if(sRec){const k=[...secRec].filter(x=>x<=w&&secRec.has(x)).length;return Math.min(cap,niv*[0.35,0.55,0.75][Math.min(k,3)-1]);}   /* récupération progressive après l'objectif (convention) */
      if(relache)return Math.min(cap,0.65*niv,CONV.moyenneMax);
      if(cle)return Math.min(cap,tr.cible[1]);
      const longueAvant=lrPrec!=null&&lrPrec>GRANDE&&lrPrec>=0.9*niv;   /* au-delà de 3 h : une semaine sur deux (D-22a, convention H-27) */
      if(ph!=='fond')return Math.min(cap,Math.max(PLANCHER,Math.min(2/3*niv,CONV.moyenneMax)));
      if(longueAvant&&Math.min(cap,niv)>GRANDE)return Math.min(cap,Math.max(PLANCHER,Math.min(2/3*niv,CONV.moyenneMax)));
      const dm=lrGel===0?doitMonter(mx):false;if(dm)return Math.min(cap,Math.max(niv,dm*SEUIL));   /* on monte jusqu'à la cible, pas au-delà */   /* un signal de fatigue gèle la progression (D-67) */
      return Math.min(cap,niv);};
    /* séances de la semaine (durées : port de construit) */
    let jours=autresDows.slice();
    const lrW=(V2&&!secIci&&!courseSem)?(()=>{const mx=max30(hist,(w-1)*7+offSL,reprise),cap=Math.max(PLANCHER,SEUIL*mx);let l=arrondi(cibleLr2(mx),cap,true);const tc=tcap(longDow);if(tc&&l>tc)l=arrondi(tc,tc);return l;})():null;
    if(V2&&lrW&&lrGel>0&&!relache&&!gele&&!cle)lrGel--;
    /* week-end enchaîné : la veille de la sortie longue devient une sortie moyenne (≤ 2/3, H-42), hors budget des endurances */
    /* D-70 : week-end de choc — objectif principal : semaines de sortie clé (3 au plus) ; objectif secondaire exigeant : 1, 4 à 6 semaines avant */
    let choc=null;
    if(V2&&enW&&lrW&&!aff&&!sAff&&!sRec&&!relache){
      if(cle&&chocsP<CONV.chocsPrincipal)choc={dur:dMain||600,p:true};
      else{const s=secs.find(s=>s.statut==='objectif'&&s.exigeant&&(chocsS[s.w]||0)<CONV.chocsSecondaire&&w>=s.w-6&&w<=s.w-4&&(lrW>=0.9*(niv||0)||w===s.w-4));
        if(s)choc={dur:s.dur,s:s.w};}}
    const veille=choc?jours.find(d=>off(d)===offSL-1):null;if(veille==null)choc=null;else{if(choc.p)chocsP++;else chocsS[choc.s]=(chocsS[choc.s]||0)+1;}if(veille!=null)jours=jours.filter(d=>d!==veille);   /* hors choc, la veille reste une endurance normale */
    const partK=Math.max(PART[aff||sAff?'affutage':ph],1/Math.max(1,n)),budgetEf=V*60*(1-partK);
    let lr0=V2?(lrW||0):cibleLr(max30(hist,(w-1)*7+offSL,reprise));
    let slMax=(!V2&&!gele&&V*60<=1.2*(jours.length+1)*PLANCHER+EPS)?Math.max(PLANCHER,V*60-jours.length*PLANCHER):null,slForce=null;
    if(slMax!=null){lr0=Math.min(lr0,slMax);
      if(V*60<(jours.length+1)*PLANCHER-EPS){const ne=Math.max(1,Math.floor(V*60/PLANCHER+1e-9));jours=jours.slice(0,ne-1);
        slForce=Math.min(Math.max(PLANCHER,SEUIL*max30(hist,(w-1)*7+offSL,reprise)),V*60-(ne-1)*PLANCHER);lr0=slForce;}}
    const courseSL=courseSem||(secIci&&sAff)||(secIci&&secIci.statut==='entrainement');
    let nb=jours.length;const reste=V2?(courseSem||(secIci&&sAff)?V*60:budgetEf):V*60-(courseSem||(secIci&&sAff)?0:lr0);
    while(nb>1&&reste/nb<PLANCHER-EPS)nb--;
    /* on garde les jours les plus éloignés de la sortie longue */
    jours=jours.slice().sort((a,b)=>gap(b,longDow)-gap(a,longDow)).slice(0,nb).sort((a,b)=>off(a)-off(b));
    const aut=V2?reste/Math.max(1,nb):(courseSem||(secIci&&sAff))?V*60/Math.max(1,nb):Math.max(0,V*60-lr0)/Math.max(1,nb);
    const h=hist.slice(),rx=[];
    jours.forEach(d=>{const jour=(w-1)*7+off(d);const cap=Math.max(PLANCHER,max30(h,jour,reprise));
      let dur=arrondi(Math.min(aut,cap,V2?(CONV.efMax[trName]||90):1e9),cap);   /* D-29 : endurance plafonnée selon l'objectif */const tc=tcap(d);if(tc&&dur>tc)dur=arrondi(tc,tc);
      if(dur>0){rx.push({dow:d,jour,dur,kind:'ef'});h.push({j:jour,d:dur,t:'rx'});}});
    const jourSL=(w-1)*7+offSL;
    if(secIci&&(w===secIci.w)){rx.push({dow:D(secIci.date).getDay(),jour:jourOf(secIci.date),dur:Math.round(secIci.dur),kind:'race',name:secIci.name,statut:secIci.statut});}
    else if(courseSem){rx.push({dow:D(P.goalDate).getDay(),jour:jourOf(P.goalDate),dur:Math.round(dMain||600),kind:'goal'});}
    if(V2&&lrW){if(veille!=null){const jv=(w-1)*7+off(veille),cv=Math.max(PLANCHER,max30(h,jv,reprise));let dv=arrondi(Math.min(CONV.samRatio*lrW,CONV.samMax(choc.dur),cv),cv);const tc=tcap(veille);if(tc&&dv>tc)dv=arrondi(tc,tc);
        if(dv>0){rx.push({dow:veille,jour:jv,dur:dv,kind:'ef',moyen:true});h.push({j:jv,d:dv,t:'rx'});}}
      rx.push({dow:longDow,jour:jourSL,dur:lrW,kind:cle?'cle':'long'});}
    else if(!V2&&!(secIci)&&!courseSem){const mx=max30(hist,jourSL,reprise);let lr=cibleLr(mx);if(slMax!=null)lr=slForce!=null?slForce:Math.min(lr,slMax);
      const cap=Math.max(PLANCHER,SEUIL*mx);lr=arrondi(lr,cap,true);const tc=tcap(longDow);if(tc&&lr>tc)lr=arrondi(tc,tc);
      if(lr>0)rx.push({dow:longDow,jour:jourSL,dur:lr,kind:cle?'cle':'long'});}
    /* jour de course : rien d'autre ce jour-là */
    const raceDates=new Set();if(secIci)raceDates.add(secIci.date);if(courseSem)raceDates.add(P.goalDate);
    for(let i=rx.length-1;i>=0;i--){const x=rx[i];if(x.kind!=='race'&&x.kind!=='goal'&&raceDates.has(add(monW,off(x.dow))))rx.splice(i,1);}
    /* qualité (gabarit) : une journée dure, pas collée à la sortie longue, de préférence un jour de renforcement */
    let qk=null;
    if(!relache&&!sRec&&!(courseSem&&false)){
      if(aff&&!courseSem)qk='rappel';
      else if(!gele&&ph==='fond'){if(sp==='F2')qk=renfo2?null:((cnt.sprint||0)<6?'sprint':'courtes');else if(sp==='F3')qk='me';else if(sp==='F4')qk='inter';}
      else if(!gele&&(ph==='bloc'||ph==='pic'))qk=((w-c.fond)%2)?'tempo':'spe';}
    const efs=rx.filter(x=>x.kind==='ef');
    if(qk&&efs.length){
      const cand=efs.filter(x=>gap(x.dow,longDow)>=2).sort((a,b)=>(cfDays.includes(b.dow)-cfDays.includes(a.dow))||(gap(b.dow,longDow)-gap(a.dow,longDow)));
      /* la séance de qualité ne va que dans un créneau assez long pour elle (sinon semaine sans qualité) */
      const q0=qualite(qk,cntDone[qk]||0,999),slot=q0?cand.find(x=>x.dur>=Math.max(35,q0.need)):null;
      if(slot){const q=qualite(qk,cntDone[qk]||0,slot.dur);
        /* la séance garde la durée de son créneau (le volume de la semaine ne bouge pas) : le reste est de l'endurance facile */
        if(q&&slot.dur>=35){slot.kind='qual';slot.q=q;slot.qk=qk;cnt[qk]=(cnt[qk]||0)+1;}}
    }
    /* accélérations (F1 dès la 3e semaine, puis F2–F4) sur l'endurance la plus éloignée de la sortie longue */
    let accel=null;
    if(!gele&&!relache&&ph==='fond'&&(sp!=='F1'||w>=3)){const e=rx.filter(x=>x.kind==='ef').sort((a,b)=>gap(b.dow,longDow)-gap(a.dow,longDow))[0];
      if(e){const p=pick(PROG.accel,cnt.accel||0);e.accel=p;cnt.accel=(cnt.accel||0)+1;accel=p;}}
    /* renforcement */
    const rf=[];
    if(strength&&!courseSem){const days=aff?cfDays.slice(0,1):cfDays;
      days.forEach(d=>{const dt=add(monW,off(d));if([...raceDates].some(r=>r===dt||add(r,-1)===dt))return;
        const near=gap(d,longDow)<=1;rf.push({dow:d,near});});}
    /* D-73 : séance décalée par l'utilisateur dans la même semaine, vers un jour sans autre course */
    if(V2&&P.decal)rx.forEach(x=>{if(x.kind==='race'||x.kind==='goal')return;const o0=add(monW,off(x.dow)),t=P.decal[o0];
      if(!t||t===o0||t<monW||t>add(monW,6))return;const td=D(t).getDay();if(rx.some(y=>y!==x&&y.dow===td))return;
      x.orig=o0;x.dow=td;x.jour=jourOf(t);});
    /* D+ */
    const dz=dens(w);
    rx.forEach(x=>{if(x.kind==='race'||x.kind==='goal')return;const f=x.kind==='long'||x.kind==='cle'?1:x.kind==='qual'?0.8:0.5;
      let dp=Math.round(dz*f*x.dur/60/50)*50;
      /* F1–F2 : l'endurance se fait sur terrain roulant, son D+ est un plafond, pas un objectif */
      if(x.kind==='ef'&&ph==='fond'&&(sp==='F1'||sp==='F2')){x.dmax=Math.max(50,dp);x.dplus=null;}
      else x.dplus=dp>=50?dp:null;});
    /* exécution : réel pour le passé, prescrit ensuite */
    const volPrevu=rx.filter(x=>x.kind!=='race'&&x.kind!=='goal').reduce((a,x)=>a+x.dur,0)/60;
    let r=null,saut=0,exec=volPrevu,execH=rx.map(x=>({j:x.jour,d:x.dur,t:x.kind}));
    if(past){
      const easy=reels.filter(s=>(s.type==='ef'||(!V2&&s.type==='long'))&&s.rpe!=null);   /* v2 : endurances seules (le RPE d'une sortie longue dépend de sa durée et de son D+) */
      r=easy.length?1+(easy.reduce((a,s)=>a+s.rpe,0)/easy.length-RPE_REF)*RPE_K:null;
      rx.forEach(x=>{if(x.kind==='race'||x.kind==='goal')return;const dt=add(monW,off(x.dow));if(isOff(dt)||dt<from)return;
        if(!reels.some(s=>s.date===dt)&&(!V2||(P.manques||{})[dt]==='fatigue'))saut++;});   /* D-72 : en v2, seule une séance manquée « pour fatigue » est un signal */
      saut=Math.min(saut,3);exec=reels.reduce((a,s)=>a+(s.dur||0),0)/60;
      execH=reels.map(s=>({j:jourOf(s.date),d:s.dur||0,t:'reel'}));
      rx.forEach(x=>{if(x.kind==='qual'){const dt=add(monW,off(x.dow));if(reels.some(s=>s.date===dt))cntDone[x.qk]=(cntDone[x.qk]||0)+1;}});
    }else{rx.forEach(x=>{if(x.kind==='qual')cntDone[x.qk]=(cntDone[x.qk]||0)+1;});r=cur?null:(m.base!=null?m.base:1);if(cur)r=undefined;}
    hist=hist.concat(execH).filter(e=>e.j>=(w-1)*7+6-FENETRE-1);
    if(r!==undefined){   /* la semaine en cours n'ajuste rien : ses séances sont à venir */
      if(!gele){if(V2){const efP=rx.filter(x=>(x.kind==='ef'||x.kind==='qual')&&!x.moyen).reduce((a,x)=>a+x.dur,0),eq=efP/60/(1-partK);
          ajuste(m,r,saut,relache,eq);if(m.etat==='sympt')lrGel=2;else if(m.etat==='maintien'&&!relache)lrGel=Math.max(lrGel,1);if(!relache&&efP<budgetEf-3)m.volume=Math.min(m.volume,Math.max(eq,0.5)*(1+m.cap));}
        else{ajuste(m,r,saut,relache,volPrevu);if(!relache&&volPrevu<V-0.05)m.volume=Math.min(m.volume,Math.max(volPrevu,0.5)*(1+m.cap));}}
      else{m.sdr=0;m.relDem=false;}
    }
    if(relache||gele){derniereRel=w;charges=0;}else{charges++;volsCharge.push(V);dernierExec=volPrevu;}
    const lrObj=rx.filter(x=>x.kind==='long'||x.kind==='cle');if(lrObj.length)lrPrec=lrObj[0].dur;
    if(V2&&!relache&&!gele){const reelL=past?Math.max(0,...reels.filter(s=>s.type==='long').map(s=>s.dur||0)):0;
      const l=past?reelL:(lrObj.length?lrObj[0].dur:0);if(l>0)niv=Math.max(niv||0,l);if(past&&reelL>0)lrPrec=reelL;}
    if(cle&&lrObj.length){clesFaites++;derniereCle=w;}
    const typ=aff?'affutage':sAff?'aff_sec':sRec?'recup_sec':relache?'relache':'charge';
    out.weeks.push({w,mon:monW,phase:ph,sous:sp,type:typ,V,volPrevu,cle,sympt:m.sympt&&!gele,dens:dz,jours:V2?(DyW.run||[]).slice():undefined,enchaine:V2?enW:undefined,niv:V2?niv:undefined});
    /* séances datées */
    const why=x=>{const b=[];
      if(x.kind==='cle')b.push('Sortie clé du bloc spécifique : elle se rapproche de ta course.');
      else if(x.kind==='long')b.push(ph==='fond'?'Sortie longue : la seule séance qui progresse cette semaine (+10 % au plus sur la plus longue des 30 derniers jours).':'Sortie longue.');
      else if(x.kind==='qual')b.push({F2:'Base aérobie : travail de force en côte, car ton renforcement ne le couvre pas.',F3:'Endurance musculaire : les jambes, pas le souffle, limitent la montée. C\'est la qualité qui manque le plus en ultra de montagne.',F4:'Intensité en côte : elle relève ton plafond aérobie avant le bloc spécifique.',bloc:'Bloc spécifique : effort de course en montée.',pic:'Pic : effort de course en montée.',affutage:'Affûtage : garder le rythme sans fatigue.'}[aff?'affutage':(sp||ph)]||'Séance de qualité.');
      else if(x.moyen)b.push('Week-end de choc : sortie moyenne la veille de ta sortie longue, pour courir le lendemain sur des jambes déjà fatiguées. Il y en a peu dans la préparation : c\'est l\'un d\'eux.');
      else if(x.kind==='ef')b.push('Endurance facile : elle construit le volume sans fatigue.');
      if(typ==='relache')b.push('Semaine allégée : on assimile.');
      if(typ==='aff_sec'||typ==='recup_sec')b.push('Autour de ton objectif intermédiaire.');
      if(typ==='affutage')b.push('Affûtage : le volume baisse, l\'intensité reste.');
      return b.join(' ');};
    rx.forEach(x=>{const date=add(monW,off(x.dow));if(date<from)return;
      if(x.kind==='race'){out.sessions.push({id:'g'+date+'-race',gen:true,date,type:'race',dur:x.dur,title:x.name,note:x.statut==='objectif'?'Objectif intermédiaire':'Course-entraînement',why:x.statut==='objectif'?'Objectif intermédiaire : affûtage avant, récupération après.':'Course-entraînement : elle remplace la sortie longue de la semaine.'});return;}
      if(x.kind==='goal'){out.sessions.push({id:'g'+date+'-goal',gen:true,date,type:'race',dur:x.dur,title:P.goalName||'Objectif',why:'Ta course.'});return;}
      const o={id:'g'+(x.orig||date)+'-'+(x.kind==='qual'?'q':x.kind),gen:true,date,type:x.kind==='qual'?'qual':(x.kind==='cle'||x.kind==='long')?'long':'ef',dur:x.dur,dplus:x.dplus,why:why(x)};
      if(x.orig)o.decale=x.orig;
      if(x.moyen)o.title='Week-end de choc';
      if(x.dmax)o.dmax=x.dmax;
      if(x.kind==='cle')o.title='Sortie clé';
      if(x.q){o.title=x.q.title;o.steps=x.q.steps;o.notes=x.q.notes;}
      if(x.accel)o.note='+ '+x.accel[0]+' × '+x.accel[1]+' s d\'accélérations en fin de séance';
      out.sessions.push(o);});
    rf.forEach(x=>{const date=add(monW,off(x.dow));if(date<from)return;const key=aff?'affutage':(sp||ph);
      const libre=P.stMode==='libre';
      out.sessions.push({id:'g'+date+'-cf',gen:true,date,type:'cf',dur:45,title:'Renforcement',
        note:libre?(x.near?'Séance libre, sans jambes lourdes (sortie longue à moins de 48 h)':'Séance libre'):(x.near?'Haut du corps et gainage : sortie longue à moins de 48 h':RENFO[key]),
        why:libre?'Tu gères ton renforcement : l\'app la compte dans ta charge.':'Contenu de la phase ('+(sp||ph)+').'});});
  }
  /* garde-fou de la sortie clé (projection) */
  const maxCle=Math.max(0,...out.sessions.filter(s=>s.title==='Sortie clé').map(s=>s.dur));
  if(!V2&&maxCle<tr.cible[0])G(1,'En projection, ta sortie clé plafonne à '+maxCle+' min pour '+tr.cible[0]+' visées (D-22). Le plan tient si ta tolérance progresse ; on le reverra avec tes données.');
  /* D-69 : écarts de projection — une cible de sortie longue que le plan n'atteint pas avant son échéance */
  out.ecarts=[];
  if(V2){const longs=out.sessions.filter(s=>s.type==='long').concat(sessions.filter(s=>s.type==='long'&&s.dur));
    secs.filter(s=>s.statut==='objectif').forEach(s=>{const cible=Math.round(Math.min(CONV.secPart*s.dur,CONV.secMax)),lim=add(s.date,-14);
      const at=Math.max(0,...longs.filter(x=>x.date<lim&&x.date>=from).map(x=>x.dur));
      if(at<0.9*cible)out.ecarts.push({obj:'secondaire',nom:s.name,date:s.date,cible,atteint:at,limite:lim});});
    if(dMain&&maxCle<0.9*tr.cible[0])out.ecarts.push({obj:'principal',nom:P.goalName||'Objectif',date:P.goalDate,cible:tr.cible[0],atteint:maxCle,limite:add(P.goalDate,-7*(tr.affutage+1))});}
  if(renfo2)out.info.renfoMsg='Avec 2 séances de renforcement par semaine, l\'app ne te propose plus de côtes courtes : ton renforcement prend le relais. Assure-toi qu\'il travaille la force des jambes (squat, fentes, step-up, mollets) et le gainage : ils protègent tes descentes et ta posture en fin de course.';
  out.ok=true;out.model={volume:m.volume,casse:m.casse,base:m.base};
  return out;
}
return {build,arrondi,Calendrier,dureeCourse,tranche_de,_t:{Modele,ajuste,atteint,max30,relachesPrevues}};
})();
if(typeof module!=='undefined')module.exports=ENGINE;
