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
  chocsPrincipal:1,          /* D-105 : un seul week-end de choc avant l'objectif principal, sur la première sortie clé (2 en D-103, 3 avant) */
  chocExperts:true,          /* D-105, H-69 : false = week-end de choc d'avant (comparaison dans les tests) */
  chocEfMax:60,              /* D-105 : semaine du choc et semaine suivante, les autres courses sont des endurances d'1 h au plus, sans qualité */
  chocsSecondaire:1,         /* avant un objectif secondaire exigeant, 4 à 6 semaines avant */
  secExigeant:(dur,dist,dplus)=>dur>=240||(dist>0&&dplus/dist>=30),
  efMax:{'4-8h':90,'8-20h':90},
  memPente:0.01,             /* D-94, H-40 : une sortie sortie de la fenêtre des 30 jours garde un repère qui baisse de 1 % par jour (0 au 130e jour) */
  memSeance:60,              /* D-94 : la mémoire n'autorise pas de séance de plus d'1 h (= 2 × le plancher de 30 min) ; au-delà, règle des 30 jours stricte */
  finPrepa:true,             /* D-103, H-67 : false = fin de préparation d'avant (comparaison dans les tests) */
  moyenneBloc:0.75,moyenneMaxBloc:240,   /* D-103 : semaine moyenne en bloc et en pic = 75 % du niveau, 4 h au plus */
  affLongue:[0.5,1/3],       /* D-103 : sortie longue d'affûtage = 50 % du niveau 13 jours avant, puis un tiers */
  densCourse:true,           /* D-102 : false = sans la densité de la course intermédiaire (comparaison dans les tests) */
  fenetreSpe:8,              /* D-102, H-66 : 8 semaines avant un objectif intermédiaire, la densité de D+ des sorties longues vaut au moins celle de la course */
  densVeille:1,              /* D-102, H-66 : la veille d'un week-end de choc est à pleine densité (0,5 avant) */
  arrondiSup:true};          /* D-96, H-58 : la séance de progression qui bute sur la limite de +10 % est arrondie au multiple de 5 min supérieur (dès 50 min), dépassement < 5 min ; false = minute inférieure (D-65d) */
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
let SUP=false;   /* D-96 : arrondi supérieur au plafond, règles v2 seulement (fixé dans build) */
function arrondi(m,plafond,fin){
  if(m<=0)return 0;
  if(m>=50-EPS){let r=regle(m);
    if(plafond!=null&&r>plafond+EPS)r=fin?((SUP&&plafond>=50-EPS)?5*Math.ceil((plafond-1e-9)/5):Math.floor(plafond+1e-9)):(plafond>=50-EPS?5*Math.floor(plafond/5+1e-9):Math.floor(plafond+1e-9));
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
/* D-103 : les sorties clés se placent à rebours, toutes les 2 semaines, la dernière en T−1 (3 semaines avant la course) */
const creneauCle=(c,tr,x)=>(c.T-1-x)%2===0&&x>=c.T-1-2*(tr.n_cles-1);
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
/* D-94 (v2) : référence sans effet de seuil = plus longue des 30 jours, ou mémoire des sorties plus anciennes
   (baisse de 1 %/jour après 30 jours, H-40), plafonnée pour que la séance prescrite (+10 %) ne dépasse pas 1 h.
   Continue et monotone : une course de plus ne baisse jamais la référence. Au-delà d'1 h, seule la règle des 30 jours compte.
   Remplace le repère de reprise dégressif (D-67 h, D-63k5, H-48) en v2. */
function ref30(hist,jour){
  let m=0,mem=0;
  for(const h of hist){const a=jour-h.j;if(a<=0)continue;
    if(a<=FENETRE){if(h.d>m)m=h.d;}
    else{const v=h.d*Math.max(0,1-CONV.memPente*(a-FENETRE));if(v>mem)mem=v;}}
  return Math.max(m,Math.min(mem,CONV.memSeance/SEUIL));
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
  out.info={N,start,trName,dureeMain:dMain,cal:c,refUsed:races.length>1?refC:undefined,cible:tr.cible.slice()};   /* D-92 : cible de sortie clé (sortie seule) */
  if(N<tr.min)G(1,'Préparation de '+N+' semaines pour la tranche '+trName+' : en dessous du minimum de '+tr.min+' semaines (D-21). Le plan est compressé.');
  let n=run.length,longDow=run.includes(+Dy.long)?+Dy.long:run[run.length-1],offSL=off(longDow);
  let autresDows=run.filter(d=>d!==longDow).sort((a,b)=>off(a)-off(b));
  let DyW=Dy;const tcap=dow=>{if(inp.regles!=='v1')return null;const t=(DyW.time||{})[dow];return t?+t:null;};   /* D-71 : ignoré en v2 (l'endurance est plafonnée par CONV.efMax, la sortie longue par sa progression) */
  const strength=!!(P.modules&&P.modules.strength);let cfDays=strength?(Dy.cf||[]).slice():[],renfo2=strength&&cfDays.length>=2;
  /* D-68 : organisation par phase (attachée aux phases, pas aux dates) et versions passées (le passé ne se réécrit jamais) */
  const V2=inp.regles!=='v1',FIN=V2&&CONV.finPrepa;SUP=V2&&CONV.arrondiSup;const ORD=['F1','F2','F3','F4','bloc','pic','affutage'];
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
    secs.push({w,date:r.date,dur,statut,name:r.name||'Course',dist:+r.dist||0,dplus:+r.dplus||0,t2,exigeant:CONV.secExigeant(dur,+r.dist||0,+r.dplus||0)});});
  const secAff={},secRec=new Set();
  secs.filter(s=>s.statut==='objectif').forEach(s=>{s.t2.aff.forEach((f,k)=>{secAff[s.w-s.t2.aff.length+1+k]=f;});for(let k=1;k<=s.t2.recup;k++)secRec.add(s.w+k);});
  const forcees=new Set(Object.keys(secAff).map(Number).concat([...secRec]));
  const budget=forcees.size/N;if(budget>0.20)G(1,'Objectifs secondaires : '+Math.round(budget*100)+' % de la préparation en affûtage et récupération, au-delà des 20 % de D-25.');
  /* historique et volume de départ : séances réelles avant le plan, sinon la déclaration */
  const jourOf=s=>Math.round((D(s)-D(start))/DAY);
  let hist=[];
  const before=sessions.filter(s=>isRun(s)&&s.date<start&&s.date>=add(start,-35));
  before.forEach(s=>hist.push({j:jourOf(s.date),d:s.dur||0,t:'reel'}));
  const MEMO=FENETRE+Math.ceil(1/CONV.memPente);   /* D-94 : profondeur de la mémoire (130 jours) */
  if(inp.regles!=='v1')sessions.filter(s=>isRun(s)&&s.date<add(start,-35)&&s.date>=add(start,-MEMO)).forEach(s=>hist.push({j:jourOf(s.date),d:s.dur||0,t:'reel'}));
  let vol0=null;
  if(before.length){const wk=sessions.filter(s=>isRun(s)&&s.date<start&&s.date>=add(start,-28));vol0=wk.reduce((a,s)=>a+(s.dur||0),0)/60/4;}
  else if(St.freq4w){vol0=St.freq4w*(St.dur4w||0)/60;
    const lr=PART.fond*vol0*60,aut=(vol0*60-lr)/Math.max(1,n-1);   /* D-94 (v2) : la plus longue déclarée du mois vaut au moins la durée moyenne déclarée */
    for(let w=-3;w<=0;w++){autresDows.forEach(d=>hist.push({j:(w-1)*7+off(d),d:aut,t:'declare'}));hist.push({j:(w-1)*7+offSL,d:inp.regles!=='v1'?Math.max(lr,+St.dur4w||0):lr,t:'declare'});}}
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
  out.info.densite={dep:dens0,course:densC};   /* D-92 : rampe de D+ exposée à l'écran (sortie seule, règles inchangées) */
  /* D-102 (H-66) : la densité se cale sur la course intermédiaire la plus proche. Points d'ancrage (semaine, m/h), jamais décroissants :
     départ → début de la fenêtre (densité de la course) → veille de la course → fin du fond (densité de l'objectif principal). Sans course intermédiaire : rampe linéaire d'avant. */
  const ancres=[[0,dens0]];
  if(V2&&CONV.densCourse)secs.filter(s=>s.statut==='objectif'&&s.dplus>0&&s.dur>0&&s.w<=c.fond).sort((a,b)=>a.w-b.w).forEach(s=>{
    const dS=Math.min(s.dplus/(s.dur/60),densC),a=Math.max(1,s.w-CONV.fenetreSpe),L=ancres[ancres.length-1],v=Math.max(L[1],dS);
    if(a>L[0])ancres.push([a,v]);else L[1]=v;
    if(s.w-1>ancres[ancres.length-1][0])ancres.push([s.w-1,v]);
    s.densSpe=v;s.mkm=s.dist?s.dplus/s.dist:null;});
  ancres.push([Math.max(c.fond,ancres[ancres.length-1][0]),densC]);
  const rampe=w=>w>=c.fond?densC:dens0+(densC-dens0)*w/Math.max(1,c.fond);   /* rampe d'avant (parité v1) */
  const dens=w=>{if(w>=c.fond||ancres.length<3)return rampe(w);
    for(let k=1;k<ancres.length;k++){const[x0,y0]=ancres[k-1],[x1,y1]=ancres[k];if(w<=x1)return Math.max(rampe(w),y0+(y1-y0)*(w-x0)/Math.max(1,x1-x0));}
    return rampe(w);};   /* au moins la rampe d'avant : la course intermédiaire ne fait que relever la densité */
  out.info.inter=secs.filter(s=>s.densSpe).map(s=>({w:s.w,name:s.name,dens:s.densSpe,mkm:s.mkm}));
  const terr=P.terrain||{};
  if(terr.climb&&['lt1','1-5'].includes(terr.climb)&&terr.mountain==='jamais')
    G(1,'Tes montées les plus longues sont courtes et tu n\'as pas d\'accès régulier à la montagne : le bloc spécifique s\'appuiera sur des répétitions de côte, et quelques sorties en moyenne montagne pendant le bloc feront une vraie différence.');
  if(tcap(longDow)&&tcap(longDow)<tr.cible[0])G(1,'Temps disponible le '+['dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi'][longDow]+' : '+tcap(longDow)+' min, pour une sortie clé de '+tr.cible[0]+' min au moins.');

  let niv=null,enW=false,lrGel=0,chocsP=0,chocPrec=false;const chocsS={};   /* D-67 : niveau de sortie longue atteint */
  let derniereRel=0,charges=0,clesFaites=0,derniereCle=-99,lrPrec=null,arretC=0,ref=null,ref2=null,volsCharge=[],dernierExec=null,reprise=null,maxAvant=0,maxSec=0;
  const cnt={};const cntDone={};
  /* D-94 : l'écart n° 5 (repère de reprise dégressif, H-48) est remplacé par la mémoire de ref30 : la sortie déclarée est une séance à sa date */
  const R30=V2?(h,j)=>ref30(h,j):(h,j)=>max30(h,j,reprise);
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
    let cle=false;if(!gele&&!relache&&(ph==='bloc'||ph==='pic'))cle=tr.n_cles>clesFaites&&w-derniereCle>=2&&w<=c.T-1&&(!FIN||creneauCle(c,tr,w));
    const secIci=secs.find(s=>s.w===w)||null;
    const part=p=>Math.max(PART[p],1/n);
    const doitMonter=mx=>{
      const futRel=relachesPrevues(c,w,derniereRel,charges,forcees),charge=[];for(let x=w;x<c.T;x++)if(!futRel.has(x)&&!forcees.has(x))charge.push(x);
      const clesPrev=[];let dern=derniereCle;for(const x of charge)if((c.phase(x)==='bloc'||c.phase(x)==='pic')&&clesPrev.length<tr.n_cles-clesFaites&&x-dern>=2&&(!FIN||creneauCle(c,tr,x))){clesPrev.push(x);dern=x;}
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
      const affL=sem=>CONV.affLongue[sem<=1?1:0];   /* D-103 : semaines avant la course → un tiers la dernière (6 jours avant), 50 % avant */
      if(aff)return FIN?Math.min(cap,lrPrec!=null?lrPrec:cap,niv*affL(N-w)):Math.min(cap,niv*tr.aff[Math.min(w-c.T,tr.aff.length-1)]);
      if(sAff){if(FIN){const s0=secs.find(s=>s.statut==='objectif'&&s.w>=w);return Math.min(cap,lrPrec!=null?lrPrec:cap,niv*affL(s0?s0.w-w:1));}return Math.min(cap,niv*secAff[w]);}
      if(sRec){const k=[...secRec].filter(x=>x<=w&&secRec.has(x)).length;return Math.min(cap,niv*[0.35,0.55,0.75][Math.min(k,3)-1]);}   /* récupération progressive après l'objectif (convention) */
      if(relache)return Math.min(cap,0.65*niv,CONV.moyenneMax);
      if(cle)return Math.min(cap,tr.cible[1]);
      const longueAvant=lrPrec!=null&&lrPrec>GRANDE&&lrPrec>=0.9*niv;   /* au-delà de 3 h : une semaine sur deux (D-22a, convention H-27) */
      if(ph!=='fond'&&FIN){if(clesFaites===0&&!longueAvant)return Math.min(cap,niv);   /* D-103 : niveau tenu jusqu'à la première sortie clé */
        return Math.min(cap,Math.max(PLANCHER,Math.min(CONV.moyenneBloc*niv,CONV.moyenneMaxBloc)));}
      if(ph!=='fond')return Math.min(cap,Math.max(PLANCHER,Math.min(2/3*niv,CONV.moyenneMax)));
      if(longueAvant&&Math.min(cap,niv)>GRANDE)return Math.min(cap,Math.max(PLANCHER,Math.min(2/3*niv,CONV.moyenneMax)));
      const dm=lrGel===0?doitMonter(mx):false;if(dm)return Math.min(cap,Math.max(niv,dm*SEUIL));   /* on monte jusqu'à la cible, pas au-delà */   /* un signal de fatigue gèle la progression (D-67) */
      return Math.min(cap,niv);};
    /* séances de la semaine (durées : port de construit) */
    let jours=autresDows.slice();
    const lrW=(V2&&!secIci&&!courseSem)?(()=>{const mx=R30(hist,(w-1)*7+offSL),cap=Math.max(PLANCHER,SEUIL*mx);let l=arrondi(cibleLr2(mx),cap,true);const tc=tcap(longDow);if(tc&&l>tc)l=arrondi(tc,tc);return l;})():null;
    if(V2&&lrW&&lrGel>0&&!relache&&!gele&&!cle)lrGel--;
    /* week-end enchaîné : la veille de la sortie longue devient une sortie moyenne (≤ 2/3, H-42), hors budget des endurances */
    /* D-70 : week-end de choc — objectif principal : semaines de sortie clé (3 au plus) ; objectif secondaire exigeant : 1, 4 à 6 semaines avant */
    let choc=null;const CX=V2&&CONV.chocExperts;
    if(V2&&enW&&lrW&&!aff&&!sAff&&!sRec&&!relache&&!(CX&&lrGel>0)){   /* D-105 : pas de week-end de choc si la sortie longue est gelée par le ressenti */
      if(cle&&chocsP<(CX?CONV.chocsPrincipal:2)&&(!FIN||w<c.T-1))choc={dur:dMain||600,p:true};
      else{const s=secs.find(s=>s.statut==='objectif'&&s.exigeant&&(chocsS[s.w]||0)<CONV.chocsSecondaire&&w>=s.w-6&&w<=s.w-4&&(lrW>=0.9*(niv||0)||w===s.w-4));
        if(s)choc={dur:s.dur,s:s.w};}}
    const veille=choc?jours.find(d=>off(d)===offSL-1):null;if(veille==null)choc=null;else{if(choc.p)chocsP++;else chocsS[choc.s]=(chocsS[choc.s]||0)+1;}if(veille!=null)jours=jours.filter(d=>d!==veille);   /* hors choc, la veille reste une endurance normale */
    const partK=Math.max(PART[aff||sAff?'affutage':ph],1/Math.max(1,n)),budgetEf=V*60*(1-partK);
    let lr0=V2?(lrW||0):cibleLr(R30(hist,(w-1)*7+offSL));
    let slMax=(!V2&&!gele&&V*60<=1.2*(jours.length+1)*PLANCHER+EPS)?Math.max(PLANCHER,V*60-jours.length*PLANCHER):null,slForce=null;
    if(slMax!=null){lr0=Math.min(lr0,slMax);
      if(V*60<(jours.length+1)*PLANCHER-EPS){const ne=Math.max(1,Math.floor(V*60/PLANCHER+1e-9));jours=jours.slice(0,ne-1);
        slForce=Math.min(Math.max(PLANCHER,SEUIL*R30(hist,(w-1)*7+offSL)),V*60-(ne-1)*PLANCHER);lr0=slForce;}}
    const courseSL=courseSem||(secIci&&sAff)||(secIci&&secIci.statut==='entrainement');
    let nb=jours.length;const reste=V2?(courseSem||(secIci&&sAff)?V*60:budgetEf):V*60-(courseSem||(secIci&&sAff)?0:lr0);
    while(nb>1&&reste/nb<PLANCHER-EPS)nb--;
    /* on garde les jours les plus éloignés de la sortie longue */
    jours=jours.slice().sort((a,b)=>gap(b,longDow)-gap(a,longDow)).slice(0,nb).sort((a,b)=>off(a)-off(b));
    const aut=V2?reste/Math.max(1,nb):(courseSem||(secIci&&sAff))?V*60/Math.max(1,nb):Math.max(0,V*60-lr0)/Math.max(1,nb);
    const h=hist.slice(),rx=[];
    jours.forEach(d=>{const jour=(w-1)*7+off(d);const cap=Math.max(PLANCHER,R30(h,jour));
      let dur=arrondi(Math.min(aut,cap,V2?(CONV.efMax[trName]||90):1e9,CX&&(choc||chocPrec)?CONV.chocEfMax:1e9),cap);   /* D-29 : endurance plafonnée selon l'objectif */const tc=tcap(d);if(tc&&dur>tc)dur=arrondi(tc,tc);
      if(dur>0){rx.push({dow:d,jour,dur,kind:'ef'});h.push({j:jour,d:dur,t:'rx'});}});
    const jourSL=(w-1)*7+offSL;
    if(secIci&&(w===secIci.w)){rx.push({dow:D(secIci.date).getDay(),jour:jourOf(secIci.date),dur:Math.round(secIci.dur),kind:'race',name:secIci.name,statut:secIci.statut});}
    else if(courseSem){rx.push({dow:D(P.goalDate).getDay(),jour:jourOf(P.goalDate),dur:Math.round(dMain||600),kind:'goal'});}
    if(V2&&lrW){if(veille!=null){const jv=(w-1)*7+off(veille),cv=Math.max(PLANCHER,R30(h,jv));let dv=arrondi(Math.min(CONV.samRatio*lrW,CONV.samMax(choc.dur),cv),cv);const tc=tcap(veille);if(tc&&dv>tc)dv=arrondi(tc,tc);
        const inv=CX&&dv>0&&!(tc&&lrW>tc);   /* D-105 : la plus longue d'abord, sur des jambes fraîches ; la moyenne le lendemain (sauf si le temps disponible la veille ne le permet pas) */
        if(inv){rx.push({dow:veille,jour:jv,dur:lrW,kind:cle?'cle':'long',choc:true});h.push({j:jv,d:lrW,t:'rx'});rx.push({dow:longDow,jour:jourSL,dur:dv,kind:'ef',moyen:true,apres:true});}
        else{if(dv>0){rx.push({dow:veille,jour:jv,dur:dv,kind:'ef',moyen:true});h.push({j:jv,d:dv,t:'rx'});}rx.push({dow:longDow,jour:jourSL,dur:lrW,kind:cle?'cle':'long'});}}
      else rx.push({dow:longDow,jour:jourSL,dur:lrW,kind:cle?'cle':'long'});}
    else if(!V2&&!(secIci)&&!courseSem){const mx=R30(hist,jourSL);let lr=cibleLr(mx);if(slMax!=null)lr=slForce!=null?slForce:Math.min(lr,slMax);
      const cap=Math.max(PLANCHER,SEUIL*mx);lr=arrondi(lr,cap,true);const tc=tcap(longDow);if(tc&&lr>tc)lr=arrondi(tc,tc);
      if(lr>0)rx.push({dow:longDow,jour:jourSL,dur:lr,kind:cle?'cle':'long'});}
    /* jour de course : rien d'autre ce jour-là */
    const raceDates=new Set();if(secIci)raceDates.add(secIci.date);if(courseSem)raceDates.add(P.goalDate);
    for(let i=rx.length-1;i>=0;i--){const x=rx[i];if(x.kind!=='race'&&x.kind!=='goal'&&raceDates.has(add(monW,off(x.dow))))rx.splice(i,1);}
    /* qualité (gabarit) : une journée dure, pas collée à la sortie longue, de préférence un jour de renforcement */
    let qk=null;
    if(!relache&&!sRec&&!(courseSem&&false)&&!(CX&&(choc||chocPrec))){   /* D-105 : pas de qualité la semaine du choc ni la suivante */
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
    /* D-97 : les décalages de la semaine sont appliqués ensemble ; deux séances qui prennent chacune le jour de l'autre s'échangent.
       Un décalage est refusé si, une fois tous appliqués, deux courses tombent le même jour (on retire les décalages en conflit jusqu'à stabilité). */
    if(V2&&P.decal){
      const mv=new Map();rx.forEach(x=>{if(x.kind==='race'||x.kind==='goal')return;const o0=add(monW,off(x.dow)),t=P.decal[o0];
        if(!t||t===o0||t<monW||t>add(monW,6))return;mv.set(x,{o0,t,td:D(t).getDay()});});
      for(let k=0;k<8;k++){const fin=x=>mv.has(x)?mv.get(x).td:x.dow,bad=[...mv.keys()].filter(x=>rx.some(y=>y!==x&&fin(y)===fin(x)));
        if(!bad.length)break;bad.forEach(x=>mv.delete(x));}
      mv.forEach((m,x)=>{x.orig=m.o0;x.dow=m.td;x.jour=jourOf(m.t);});}
    /* D+ */
    const dz=dens(w);
    rx.forEach(x=>{if(x.kind==='race'||x.kind==='goal')return;const f=x.kind==='long'||x.kind==='cle'?1:x.kind==='qual'?0.8:x.moyen?(CONV.densCourse?CONV.densVeille:0.5):0.5;
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
    hist=hist.concat(execH).filter(e=>e.j>=(w-1)*7+6-(V2?MEMO:FENETRE)-1);
    if(r!==undefined){   /* la semaine en cours n'ajuste rien : ses séances sont à venir */
      if(!gele){if(V2){const efP=rx.filter(x=>(x.kind==='ef'||x.kind==='qual')&&!x.moyen).reduce((a,x)=>a+x.dur,0),eq=efP/60/(1-partK);
          ajuste(m,r,saut,relache,eq);if(m.etat==='sympt')lrGel=2;else if(m.etat==='maintien'&&!relache)lrGel=Math.max(lrGel,1);if(!relache&&efP<budgetEf-3&&!(CX&&(choc||chocPrec)))m.volume=Math.min(m.volume,Math.max(eq,0.5)*(1+m.cap));}
        else{ajuste(m,r,saut,relache,volPrevu);if(!relache&&volPrevu<V-0.05)m.volume=Math.min(m.volume,Math.max(volPrevu,0.5)*(1+m.cap));}}
      else{m.sdr=0;m.relDem=false;}
    }
    if(relache||gele){derniereRel=w;charges=0;}else{charges++;volsCharge.push(V);dernierExec=volPrevu;}
    const lrObj=rx.filter(x=>x.kind==='long'||x.kind==='cle');if(lrObj.length)lrPrec=lrObj[0].dur;
    if(V2&&!relache&&!gele){const reelL=past?Math.max(0,...reels.filter(s=>s.type==='long').map(s=>s.dur||0)):0;
      const l=past?reelL:(lrObj.length?lrObj[0].dur:0);if(l>0)niv=Math.max(niv||0,l);if(past&&reelL>0)lrPrec=reelL;}
    if(cle&&lrObj.length){clesFaites++;derniereCle=w;}
    const typ=aff?'affutage':sAff?'aff_sec':sRec?'recup_sec':relache?'relache':'charge';
    chocPrec=!!choc;
    out.weeks.push({w,mon:monW,phase:ph,sous:sp,type:typ,choc:V2?!!choc:undefined,V,volPrevu,cle,sympt:m.sympt&&!gele,dens:dz,jours:V2?(DyW.run||[]).slice():undefined,enchaine:V2?enW:undefined,niv:V2?niv:undefined});
    /* séances datées */
    const why=x=>{const b=[];
      if(x.kind==='cle')b.push('Sortie clé du bloc spécifique : elle se rapproche de ta course.');
      if(x.choc)b.push('Week-end de choc : la plus longue aujourd\'hui, sur des jambes fraîches. Demain, une sortie moyenne sur la fatigue.');
      else if(x.kind==='long')b.push(ph==='fond'?'Sortie longue : la seule séance qui progresse cette semaine (environ +10 % sur la plus longue des 30 derniers jours, durée arrondie aux 5 min supérieures).':'Sortie longue.');
      else if(x.kind==='qual')b.push({F2:'Base aérobie : travail de force en côte, car ton renforcement ne le couvre pas.',F3:'Endurance musculaire : les jambes, pas le souffle, limitent la montée. C\'est la qualité qui manque le plus en ultra de montagne.',F4:'Intensité en côte : elle relève ton plafond aérobie avant le bloc spécifique.',bloc:'Bloc spécifique : effort de course en montée.',pic:'Pic : effort de course en montée.',affutage:'Affûtage : garder le rythme sans fatigue.'}[aff?'affutage':(sp||ph)]||'Séance de qualité.');
      else if(x.moyen)b.push(x.apres?'Week-end de choc : sortie moyenne le lendemain de ta sortie longue, sur des jambes déjà fatiguées. Aucune étude ne montre que c\'est mieux qu\'une sortie longue seule : il sert à courir fatigué et à répéter ta nutrition. Si tu es très fatigué ce matin, raccourcis ou supprime cette sortie.':'Week-end de choc : sortie moyenne la veille de ta sortie longue, pour courir le lendemain sur des jambes déjà fatiguées. Il y en a peu dans la préparation : c\'est l\'un d\'eux.');
      else if(x.kind==='ef')b.push('Endurance facile : elle construit le volume sans fatigue.');
      if(x.dplus&&(x.kind==='long'||x.kind==='cle'||x.moyen)){   /* D-102 : densité de la course, et descentes */
        const sp0=secs.find(s=>s.densSpe&&w>=s.w-CONV.fenetreSpe&&w<s.w),refD=sp0?sp0.densSpe:(ph!=='fond'||w>=c.fond?densC:null),mk=sp0?sp0.mkm:(P.goalDist&&P.goalDplus?P.goalDplus/P.goalDist:null);
        if(refD&&mk&&x.dplus/(x.dur/60)>=0.9*refD)b.push('Environ '+Math.round(mk)+' m de D+ par km, comme ta course.');
        b.push('Cours aussi les descentes, en contrôle : en fin de course, c\'est là que la vitesse baisse le plus.');}
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
/* ---- D-99 : bilan de séance, étage A (calculé, déterministe ; ne modifie pas le plan) ----
   Seuils des messages : conventions (H-59), réglables ici. */
const BILAN={baseZ:2,baseHaut:155,haut:0.40,bas:0.20,rpeBas:3,rpeHaut:7,ecart:0.25};

/* ---------- D-100 : zones de Karvonen et indicateurs tirés des données seconde par seconde ---------- */
const KARV=[0.6,0.7,0.8,0.9];   /* bornes hautes des zones 1 à 4, en part de la FC de réserve (zone 5 au-delà) */
const FLUX={pente:3,fauxPlat:1,fenetreM:200,lissage:7,depart:600,plateau:0.95,ecartTerrain:5,deriveMin:2400,deriveSeuil:5};   /* H-60, H-62, H-63 */
/* Minetti et al. 2002 : coût énergétique de la course (J/kg/m) selon la pente i (fraction, −0,45 à +0,45). */
function minetti(i){i=Math.max(-0.45,Math.min(0.45,i));return 155.4*i**5-30.4*i**4-43.3*i**3+46.3*i**2+19.5*i+3.6;}
const TERRAIN=[['montee',0.03,1],['fpm',0.01,0.03],['plat',-0.01,0.01],['fpd',-0.03,-0.01],['descente',-1,-0.03]];
/* D-101 : repères de progression. Valeurs d'une sortie ramenées à une FC de référence fixe (ref) par proportion sur la FC de réserve.
   allure (s/km, plus bas = mieux), montee (m/h, plus haut = mieux), tenue (% perdu en 2e moitié, plus bas = mieux). H-64. */
const PROGR={utilMin:20,tenueDur:75,seuil:3,fen6:[56,28],fenNow:28,nb:3};
function repSeance(f,dur,ref,repos){if(!f||(f.v||1)<3||!(ref>repos))return null;const k=fc=>fc>repos+20?(ref-repos)/(fc-repos):null,o={};
  if(f.util&&f.util.min>=PROGR.utilMin){const q=k(f.util.fc);if(q)o.allure=Math.round(1000/(f.util.v*q));}
  if(f.vam&&f.terrain&&f.terrain.montee&&f.terrain.montee.fc){const q=k(f.terrain.montee.fc);if(q)o.montee=Math.round(f.vam*q);}
  if(f.derive&&dur>=PROGR.tenueDur)o.tenue=f.derive.pct;
  return Object.keys(o).length?o:null;}
function progression(sessions,o){/* o = {start,today,ref,repos} ; sessions : {date,dur,flux} déjà filtrées sur la course */
  const add=(d,n)=>{const x=new Date(d+'T12:00:00Z');x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10);};
  const pts=sessions.filter(s=>s.date>=o.start&&s.date<=o.today).sort((a,b)=>a.date<b.date?-1:1).map(s=>({date:s.date,r:repSeance(s.flux,s.dur,o.ref,o.repos)})).filter(p=>p.r);
  const moy=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:null,out={};
  ['allure','montee','tenue'].forEach(k=>{const L=pts.filter(p=>p.r[k]!=null).map(p=>({date:p.date,v:p.r[k]}));
    if(!L.length){out[k]=null;return;}
    const dep=L.slice(0,2),f6=L.filter(p=>p.date>=add(o.today,-PROGR.fen6[0])&&p.date<add(o.today,-PROGR.fen6[1])).slice(-PROGR.nb),
      now=L.filter(p=>p.date>=add(o.today,-PROGR.fenNow)).slice(-PROGR.nb);
    const c=a=>a.length>=2?Math.round(10*moy(a.map(p=>p.v)))/10:null;
    const R={depart:Math.round(10*moy(dep.map(p=>p.v)))/10,provisoire:dep.length<2,s6:c(f6),now:c(now),n:L.length,derniere:L[L.length-1]};
    /* verdict : maintenant contre il y a 6 semaines, à défaut contre le départ (s'il ne partage pas les mêmes sorties) */
    const depD=new Set(dep.map(p=>p.date)),base=R.s6!=null?R.s6:(!R.provisoire&&now.some(p=>!depD.has(p.date))?R.depart:null);
    if(R.now==null||base==null)R.verdict=L.length===1?'premiere':'attente';
    else{const sens=k==='montee'?1:-1,d=k==='tenue'?(R.now-base):100*(R.now-base)/base;
      R.ecart=Math.round(10*d)/10;R.verdict=sens*d>=PROGR.seuil?'progres':-sens*d>=PROGR.seuil?'baisse':'stable';}
    const M={};L.forEach(p=>{(M[p.date.slice(0,7)]=M[p.date.slice(0,7)]||[]).push(p.v);});
    R.mois=Object.keys(M).sort().map(m=>({mois:m,v:Math.round(10*moy(M[m]))/10,n:M[m].length}));
    out[k]=R;});
  return out;}
function zonesKarvonen(fcMax,fcRepos){
  if(!(fcMax>0&&fcRepos>0&&fcMax>fcRepos+40))return null;
  const R=fcMax-fcRepos;return KARV.map(x=>Math.floor(fcRepos+R*x));}
/* st = {time:[s],hr:[bpm],dist:[m],alt:[m]} (mêmes longueurs) ; zones = bornes hautes (zonesKarvonen) ou null.
   Renvoie un résumé compact, gardé avec la séance ; la trace brute n'est pas conservée. */
function flux(st,zones){
  if(!st||!Array.isArray(st.time)||!Array.isArray(st.hr))return null;
  const n=st.time.length;if(n<60)return null;
  const T=st.time,H=st.hr,Dd=st.dist||[],A=st.alt||[];
  const ok=i=>i>0&&T[i]-T[i-1]>0&&T[i]-T[i-1]<=10;   /* les pauses (écart > 10 s) ne comptent pas */
  /* altitude lissée (moyenne glissante) */
  let Al=null;if(A.length===n&&A.some(x=>x!=null)){Al=new Array(n);const L=FLUX.lissage;
    for(let i=0;i<n;i++){let s=0,c=0;for(let j=Math.max(0,i-L);j<=Math.min(n-1,i+L);j++)if(A[j]!=null){s+=A[j];c++;}Al[i]=c?s/c:null;}}
  const hasD=Dd.length===n&&Dd[n-1]>0;
  /* temps en mouvement et zones */
  let tm=0;const zt=zones?[0,0,0,0,0]:null;
  for(let i=1;i<n;i++){if(!ok(i))continue;const d=T[i]-T[i-1];tm+=d;if(zt&&H[i]>0)zt[zones.reduce((z,b)=>z+(H[i]>b?1:0),0)]+=d;}
  if(tm<300)return null;
  const zTot=zt?zt.reduce((a,b)=>a+b,0):0;
  const zonesOut=zt&&zTot?{bornes:zones.slice(),pct:zt.map(x=>Math.round(100*x/zTot)),dessusBase:Math.round(100*(zt[2]+zt[3]+zt[4])/zTot)}:null;
  /* FC de croisière : médiane après le départ ; temps pour l'atteindre */
  const t0=T[0],apres=[];for(let i=0;i<n;i++)if(T[i]-t0>=FLUX.depart&&H[i]>0)apres.push(H[i]);
  let crois=null;if(apres.length>=300){apres.sort((a,b)=>a-b);const fc=apres[Math.floor(apres.length/2)];
    let k=0;while(k<n&&!(H[k]>=fc*FLUX.plateau))k++;
    let deb=0,c=0;for(let i=0;i<n&&T[i]-t0<FLUX.depart;i++)if(H[i]>0){deb+=H[i];c++;}
    crois={fc,montee_s:k<n?Math.round(T[k]-t0):null,depart:c?Math.round(deb/c):null};}
  /* tranches par km (par 5 km au-delà de 15 km) */
  let tranches=null;
  if(hasD){const km=Dd[n-1]/1000,pas=km>15?5:1;tranches=[];let a=0;
    for(let b=pas;a<n;b+=pas){const lim=b*1000;let i=a,t=0,hs=0,hc=0,dp=0,dm=0;
      for(i=a+1;i<n&&Dd[i]<=lim;i++){if(!ok(i))continue;t+=T[i]-T[i-1];if(H[i]>0){hs+=H[i];hc++;}
        if(Al&&Al[i]!=null&&Al[i-1]!=null){const dz=Al[i]-Al[i-1];if(dz>0)dp+=dz;else dm-=dz;}}
      const dist=(Dd[Math.min(i,n-1)]-Dd[a]);
      if(dist>=(pas*1000)*0.3&&t>0)tranches.push({de:b-pas,a:Math.min(b,Math.round(km*10)/10),allure:Math.round(t/(dist/1000)),fc:hc?Math.round(hs/hc):null,dp:Al?Math.round(dp):null,dm:Al?Math.round(dm):null});
      if(i>=n-1)break;a=i;}}
  /* profil de terrain (D-100, v64) : pente sur ~200 m centrés, 5 catégories ; allure équivalente plat (Minetti) hors descente */
  let terrain=null,vam=null,derive=null,util=null;
  if(Al&&hasD){const g=new Array(n).fill(null),W=FLUX.fenetreM/2;let a=0,b=0;
    for(let i=0;i<n;i++){while(a<i&&Dd[a]<Dd[i]-W)a++;while(b<n-1&&Dd[b]<Dd[i]+W)b++;
      const dd=Dd[b]-Dd[a];if(dd>=FLUX.fenetreM*0.6&&Al[a]!=null&&Al[b]!=null)g[i]=(Al[b]-Al[a])/dd;}
    const S={};TERRAIN.forEach(c=>S[c[0]]={t:0,d:0,de:0,h:0,hc:0,dz:0});const seg=[];
    for(let i=1;i<n;i++){if(!ok(i)||g[i]==null)continue;const gi=g[i],c=TERRAIN.find(c=>gi>=c[1]&&gi<c[2])||(gi>=0.03?TERRAIN[0]:TERRAIN[4]);
      const x=S[c[0]],dt=T[i]-T[i-1],ds=Math.max(0,Dd[i]-Dd[i-1]),de=ds*minetti(gi)/3.6;
      x.t+=dt;x.d+=ds;x.de+=de;if(H[i]>0){x.h+=H[i];x.hc++;}if(Al[i-1]!=null)x.dz+=Al[i]-Al[i-1];
      if(gi>=-FLUX.fauxPlat/100&&T[i]-T[0]>=FLUX.depart)seg.push([dt,de,H[i]]);}
    terrain={};TERRAIN.forEach(c=>{const k=c[0],x=S[k];terrain[k]=x.t>=60&&x.d>0?{min:Math.round(x.t/60),kmh:Math.round(x.d/x.t*36)/10,allure:Math.round(x.t/(x.d/1000)),
      eq:k!=='descente'&&x.de>0?Math.round(x.t/(x.de/1000)):null,fc:x.hc?Math.round(x.h/x.hc):null}:null;});
    if(S.montee.t>=120&&S.montee.dz>0)vam=Math.round(S.montee.dz/(S.montee.t/3600));
    /* dérive : hors départ et hors descentes, 1re moitié contre 2e moitié (FC et allure équivalente plat) */
    const tt=seg.reduce((s,x)=>s+x[0],0);
    /* D-101 : partie utile (après le départ, hors descentes) : vitesse équivalente plat et FC moyennes */
    {let de=0,h=0,hc=0;seg.forEach(x=>{de+=x[1];if(x[2]>0){h+=x[2];hc++;}});if(tt>=60&&de>0&&hc)util={min:Math.round(tt/60),v:Math.round(1000*de/tt)/1000,fc:Math.round(10*h/hc)/10};}
    if(tt>=FLUX.deriveMin){let c=0,k=0;while(k<seg.length&&c<tt/2){c+=seg[k][0];k++;}
      const m=q=>{let t=0,de=0,h=0,hc=0;q.forEach(x=>{t+=x[0];de+=x[1];if(x[2]>0){h+=x[2];hc++;}});return {fc:Math.round(h/hc),allure:Math.round(t/(de/1000)),e:(h/hc)/(de/t)};};
      const m1=m(seg.slice(0,k)),m2=m(seg.slice(k));
      derive={fc1:m1.fc,fc2:m2.fc,eq1:m1.allure,eq2:m2.allure,pct:Math.round(1000*(m2.e/m1.e-1))/10};}}
  return {v:3,min:Math.round(tm/60),zones:zonesOut,croisiere:crois,tranches,terrain,vam,derive,util};
}
function bilan(inp,sid){
  const all=inp.sessions||[],s=all.find(x=>x.id===sid);if(!s)return null;
  const isR=inp.isRun||(x=>['ef','long','qual','desc'].includes(x.type));
  const today=inp.today||s.date,horizon=today>s.date?today:add(s.date,1);
  /* effet sur le plan : moteur avec et sans la séance */
  const avec=build(Object.assign({},inp,{today:horizon})),sans=build(Object.assign({},inp,{today:horizon,sessions:all.filter(x=>x.id!==sid)}));
  const prochaine=o=>o.sessions.filter(x=>x.type==='long'&&x.date>=horizon).sort((a,b)=>a.date<b.date?-1:1)[0]||null;
  const pA=prochaine(avec),pS=prochaine(sans);
  const prevu=avec.sessions.find(x=>x.id===s.plannedId)||null;
  /* référence : plus longue course des 30 jours avant la séance */
  const ref=Math.max(0,...all.filter(x=>x.id!==sid&&isR(x)&&x.date<s.date&&x.date>=add(s.date,-30)).map(x=>x.dur||0));
  const derSL=all.filter(x=>x.id!==sid&&x.type==='long'&&x.date<s.date).sort((a,b)=>a.date<b.date?1:-1)[0]||null;
  const veille=all.find(x=>x.type==='cf'&&x.date===add(s.date,-1))||null;
  /* temps par zone (zones d'intervals.icu, D-98) ; « au-dessus de la base » = au-delà de la zone BILAN.baseZ */
  let zones=null,dessus=null,zonesKO=null;
  const PP=inp.profile||{},zk=zonesKarvonen(PP.fcMax,PP.fcRepos),F=s.flux&&s.flux.v?s.flux:null;
  /* D-100 : zones de l'appli (Karvonen) appliquées aux données seconde par seconde ; prioritaires sur celles d'intervals.icu */
  if(F&&F.zones){zones=F.zones.pct.map((p,i)=>({z:i+1,haut:F.zones.bornes[i]!=null?F.zones.bornes[i]:null,pct:p}));dessus=F.zones.dessusBase/100;}
  /* garde-fou (v58) : intervals.icu fige les zones à l'import de l'activité. Si la borne haute de la zone de base n'est pas celle réglée, les temps par zone ne sont pas fiables : on ne les affiche pas. */
  const hautBase=zk?zk[BILAN.baseZ-1]:(PP.fcBase||BILAN.baseHaut),bornes=s.hrZ&&s.hrZ.b,bAct=bornes?bornes[BILAN.baseZ-1]:null;
  if(!zones&&s.hrZ&&bAct!=null&&Math.abs(bAct-hautBase)>1)zonesKO={act:bAct,att:hautBase};
  if(!zones&&!zonesKO&&s.hrZ&&Array.isArray(s.hrZ.t)){const t=s.hrZ.t.map(x=>+x||0),tot=t.reduce((a,b)=>a+b,0);
    if(tot>0){zones=t.map((x,i)=>({z:i+1,haut:s.hrZ.b&&s.hrZ.b[i]!=null?s.hrZ.b[i]:null,pct:Math.round(100*x/tot)}));
      dessus=t.slice(BILAN.baseZ).reduce((a,b)=>a+b,0)/tot;}}
  const SYM={'fc-haute':'▲','fc-basse':'▲','30j':'▲','depart':'▲','descente':'▲'},msgs=[],m=(code,txt,sym)=>msgs.push({code,txt,sym:sym||SYM[code]||'○'});
  if(zonesKO)m('zones-decalees','Les zones de FC de cette activité ne sont pas celles que tu as réglées (zone de base jusqu\'à '+zonesKO.act+' bpm au lieu de '+zonesKO.att+') : le temps par zone n\'est pas fiable pour cette séance.');
  if(dessus!=null&&s.rpe!=null&&s.rpe<=BILAN.rpeBas&&dessus>BILAN.haut)m('fc-haute','Ta FC a travaillé plus que ton ressenti : '+Math.round(dessus*100)+' % du temps au-dessus de ton allure facile.');
  if(dessus!=null&&s.rpe!=null&&s.rpe>=BILAN.rpeHaut&&dessus<BILAN.bas&&s.type!=='qual')m('fc-basse','Ressenti dur mais FC basse : fatigue des jambes ou fatigue générale probable.');
  if(prevu&&prevu.dur&&s.dur){const e=s.dur/prevu.dur-1;if(e>BILAN.ecart)m('plus-long','Plus long que prévu (+'+Math.round(e*100)+' %).');else if(e<-BILAN.ecart)m('plus-court','Plus court que prévu ('+Math.round(e*100)+' %).');}
  if(F&&F.croisiere&&F.croisiere.fc){const c=F.croisiere,ec=c.fc-hautBase;
    m('croisiere','FC stabilisée : '+c.fc+' bpm'+(c.depart?' (départ à '+c.depart+')':'')+(c.montee_s!=null?', atteint en '+Math.max(1,Math.round(c.montee_s/60))+' min':'')+' — '+(ec>0?ec+' bpm au-dessus':ec<0?(-ec)+' bpm en dessous':'pile à la limite')+' de ton allure facile ('+hautBase+').');}
  if(F&&F.terrain&&F.terrain.montee&&F.terrain.descente&&F.terrain.montee.fc&&F.terrain.descente.fc&&F.terrain.descente.fc>=F.terrain.montee.fc-FLUX.ecartTerrain)
    m('descente','FC presque aussi haute en descente ('+F.terrain.descente.fc+') qu\'en montée ('+F.terrain.montee.fc+') : peu de récupération dans les descentes.');
  if(F&&F.derive){const d=F.derive,at=x=>Math.floor(x/60)+':'+String(x%60).padStart(2,'0');
    if(Math.abs(d.pct)<FLUX.deriveSeuil)m('derive','Pas de dérive : à pente corrigée, ta FC et ton allure tiennent du début à la fin ('+(d.pct>0?'+':'')+d.pct+' %).','✓');
    else if(d.pct>0&&d.fc2>=d.fc1)m('derive','Dérive cardiaque : à allure égale (pente corrigée), ta FC monte en 2e partie ('+d.fc1+' → '+d.fc2+'). Souvent chaleur ou hydratation.','▲');
    else if(d.pct>0)m('derive','Fatigue des jambes : ta FC baisse ('+d.fc1+' → '+d.fc2+') mais ton allure équivalente plat chute davantage ('+at(d.eq1)+' → '+at(d.eq2)+' /km). Ce sont les muscles qui limitent, pas le cardio.','▲');
    else m('derive','Meilleure efficacité en 2e partie ('+d.pct+' %) : départ prudent ou échauffement long.');}
  if(veille&&isR(s)&&veille.cfJ&&veille.cfJ!=='non')m('veille-cf','CrossFit la veille ('+(veille.cfJ==='fort'?'jambes très sollicitées':'jambes un peu sollicitées')+') : jambes déjà entamées au départ.');
  if(isR(s)&&ref>0&&s.dur>ref*SEUIL+5)m('30j','Au-delà de +10 % de ta plus longue sortie des 30 jours ('+ref+' min) : la prochaine sortie longue en tiendra compte.');
  /* un indicateur expliqué (texte fixe) */
  const ind=F&&F.terrain?'terrain':zones?'zones':(s.dplus&&s.dur)?'dplus-h':'charge';
  const effet={prochaine:pA?{date:pA.date,dur:pA.dur,dplus:pA.dplus||null}:null,sans:pS?{date:pS.date,dur:pS.dur}:null,
    change:!!(pA&&pS&&(pA.date!==pS.date||pA.dur!==pS.dur)),ecarts:(avec.ecarts||[]).map(e=>e.obj)};
  return {id:s.id,date:s.date,type:s.type,dur:s.dur||null,durTot:s.durTot||null,dist:s.dist||null,dplus:s.dplus||null,dminus:s.dminus||null,
    hrAvg:s.hrAvg||null,hrMax:s.hrMax||null,rpe:s.rpe!=null?s.rpe:null,zones,dessusBase:dessus!=null?Math.round(dessus*100):null,
    prevu:prevu?{type:prevu.type,dur:prevu.dur,dplus:prevu.dplus||null}:null,ref30:ref||null,
    joursDepuisSL:derSL?Math.round((D(s.date)-D(derSL.date))/864e5):null,veilleCF:veille?(veille.cfJ||'?'):null,
    dplusH:s.dplus&&s.dur?Math.round(s.dplus/(s.dur/60)):null,hautBase,flux:F?{croisiere:F.croisiere,terrain:F.terrain,vam:F.vam,tranches:F.tranches,derive:F.derive||null}:null,msgs,indicateur:ind,effet};
}
return {build,bilan,flux,minetti,progression,repSeance,PROGR,zonesKarvonen,FLUX,BILAN,CONV,arrondi,Calendrier,dureeCourse,tranche_de,_t:{Modele,ajuste,atteint,max30,ref30,relachesPrevues}};
})();
if(typeof module!=='undefined')module.exports=ENGINE;
