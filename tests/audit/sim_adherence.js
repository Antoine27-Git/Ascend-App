/* Audit mission 1 — faisabilité sous adhérence réelle (pré-mortem chiffré).
   Rejoue le moteur v2 semaine après semaine : le plan de la semaine est calculé le lundi avec les séances
   réellement faites jusque-là, puis des semaines sont « perturbées » au hasard (une ou toutes les sorties perdues).
   Ne modifie pas le moteur : les variantes (D-94, D-96) passent par la table CONV exportée, remise en état après.
   Usage : node tests/audit/sim_adherence.js [essais=400] [graine=1] [filtre] [i/k]
   Sortie : un tableau par scénario + tests/audit/out/adherence.json */
let E=require('../engine.js');const E0=E,fs=require('fs'),path=require('path'),variante=require('./variante.js');
/* même définition que l'appli (index.html, TYPES[...].run) : une course enregistrée compte comme une sortie.
   Les tests du dépôt (t_profils.js, t_react3.js) utilisent une liste sans 'race' : sans effet chez eux (aucune course réelle rejouée). */
const isRun=s=>['ef','long','qual','race','desc'].includes(s.type);
const add=(d,n)=>{const x=new Date(d+'T12:00:00Z');x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10);};
const days=(a,b)=>Math.round((new Date(b+'T12:00:00Z')-new Date(a+'T12:00:00Z'))/864e5);
function rng(seed){let a=seed>>>0;return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
/* Profil d'Antoine au 10/11/2026 : tests/ui/state.py, plan redémarré le 02/11, sortie longue de 1 h 16 faite le 08/11 */
const ANTOINE=()=>({goalName:'80 km',goalDate:'2027-09-25',goalDist:80,goalDplus:4500,planStart:'2026-11-02',planFrom:'2026-11-02',stMode:'libre',
  modules:{nutrition:true,strength:true},days:{run:[3,0],long:0,cf:[2,5],time:{}},orgs:[],terrain:{dplusMax:900},
  start:{lastLong:{date:'2026-09-06',dur:107,dist:12,dplus:500},pastRaces:[],freq4w:1,dur4w:45,lastGoal:{date:'2025-09-20',dur:390,dist:42,dplus:1300}},
  races:[{name:'50 km',date:'2027-05-08',dist:50,dplus:2000,prio:'B'}],manques:{}});
const SES0=()=>[{date:'2026-09-27',type:'long',dur:30,rpe:2},{date:'2026-11-08',type:'long',dur:76,rpe:3}];
const PROFILS={
  '2 jours':p=>{},
  '2 j → 3 j enchaîné dès F3':p=>{p.orgs=[{from:'F3',enchaine:true,days:{run:[3,6,0],long:0,cf:[2]}}];},
  '2 jours, sans 50 km':p=>{p.races=[];},
  '2 jours, 50 km en course-entraînement (C)':p=>{p.races[0].prio='C';},
};
/* une trajectoire. opt : {p, grappe, both, politique, repli, mercMax, rpe} */
function trajectoire(profil,opt,rand){
  const P=ANTOINE();PROFILS[profil](P);if(opt.goalDate)P.goalDate=opt.goalDate;
  const ses=SES0(),debut='2026-11-09';   /* S2 : première semaine à simuler */
  const o0=E.build({profile:P,today:debut,sessions:ses,isRun});const N=o0.info.N,cal=o0.info.cal;
  let pert=false;const log=[];let niv=76,effondrements=0,minPerdues=0,sautes=0,faites=0,slFaites=0,slPrevues=0,semPert=0;
  const L=opt.grappe||1,pIn=opt.p>0?Math.min(1,opt.p/(L*(1-opt.p))):0;
  for(let w=2;w<=N;w++){
    const mon=add('2026-11-02',(w-1)*7);
    /* le plan de la semaine est lu le MARDI : le lundi, en heure d'été, le moteur se croit encore la semaine précédente
       pour un plan démarré en heure d'hiver (défaut de calcul de todayW, voir docs/audit/02 et t_audit_heure_ete.js).
       Le coureur lit son plan le jour de la séance (mercredi, dimanche) : même résultat que le mardi. */
    const o=E.build({profile:P,today:add(mon,1),sessions:ses,isRun});
    const sem=o.sessions.filter(s=>s.date>=mon&&s.date<add(mon,7)&&s.type!=='cf');
    const runs=sem.filter(s=>s.type!=='race'),k=o.weeks.find(x=>x.w===w);
    /* tirage de la perturbation (indépendante, ou en grappes de longueur moyenne L : chaîne de Markov de même fréquence) */
    pert=L>1?(pert?rand()<1-1/L:rand()<pIn):rand()<opt.p;
    let perdues=new Set();
    if(pert&&runs.length&&w<N){semPert++;
      if(rand()<(opt.both==null?0.5:opt.both))runs.forEach(s=>perdues.add(s.id));
      else{const c=opt.politique==='chargee'?runs.filter(s=>s.type!=='long'):runs;if(c.length)perdues.add(c[Math.floor(rand()*c.length)].id);}}
    const L0=runs.find(s=>s.type==='long');
    /* effondrement : le jour de la sortie longue, la fenêtre des 30 jours ne porte plus le niveau atteint */
    if(L0){slPrevues++;const ref=Math.max(0,...ses.filter(s=>isRun(s)&&days(s.date,L0.date)>0&&days(s.date,L0.date)<=30).map(s=>s.dur));
      if(1.1*ref<0.8*niv&&k.type==='charge'){effondrements++;minPerdues=Math.max(minPerdues,niv-1.1*ref);}}
    sem.forEach(s=>{
      if(s.type==='race'){ses.push({date:s.date,type:'race',dur:s.dur,rpe:6});return;}   /* les courses sont courues */
      if(perdues.has(s.id)){sautes++;P.manques[s.date]='autre';
        /* séance de repli : à la place d'une sortie longue perdue, une sortie courte (durée fixe, plafonnée à la séance prévue) */
        if(opt.repli&&s.type==='long'){const d=Math.min(s.dur,opt.repli);ses.push({date:s.date,type:'long',dur:d,rpe:3,dplus:0});}
        return;}
      let d=s.dur;if(opt.mercMax&&s.type!=='long'&&new Date(s.date+'T12:00:00Z').getUTCDay()===3)d=Math.min(d,opt.mercMax);
      /* rpeBruit : ressenti de 3/10 ± 1 tiré au hasard (bruit de saisie, aucune fatigue réelle) */
      ses.push({date:s.date,type:s.type==='qual'?'qual':s.type,dur:d,rpe:opt.rpeBruit?(opt.rpeBruit===true||rand()<opt.rpeBruit?3+Math.floor(rand()*3)-1:3):(opt.rpe||3),dplus:s.dplus||0});faites++;
      if(s.type==='long'){slFaites++;niv=Math.max(niv,d);}});
    log.push({w,ph:k.sous||k.phase,type:k.type,L:L0?L0.dur:null,fait:L0&&!perdues.has(L0.id)});
  }
  const fin=E.build({profile:P,today:P.goalDate,sessions:ses,isRun});
  const longs=ses.filter(s=>s.type==='long'),T0=add('2026-11-02',(cal.fond)*7),T1=add('2026-11-02',(cal.T-1)*7);   /* bloc + pic */
  const bloc=longs.filter(s=>s.date>=T0&&s.date<T1),maxBloc=Math.max(0,...bloc.map(s=>s.dur));
  const sec=(P.races||[])[0],secLim=sec?add(sec.date,-14):null;
  const jalon=m=>{const s=longs.filter(x=>x.dur>=m).sort((a,b)=>a.date<b.date?-1:1)[0];return s?s.date:null;};
  return {maxBloc,cles:bloc.filter(s=>s.dur>=270).length,maxTout:Math.max(0,...longs.map(s=>s.dur)),
    maxSec:sec?Math.max(0,...longs.filter(s=>s.date<secLim).map(s=>s.dur)):null,
    dplusMax:Math.max(0,...longs.map(s=>s.dplus||0)),j120:jalon(120),j180:jalon(180),j240:jalon(240),j300:jalon(300),
    slPerduesFin:log.filter(l=>l.w>=cal.fond-4&&l.w<cal.T&&l.L!=null&&!l.fait).length,
    effondrements,minPerdues,sautes,faites,slFaites,slPrevues,semPert,N,
    volH:ses.filter(s=>isRun(s)&&s.date>='2026-11-02').reduce((a,s)=>a+s.dur,0)/60,
    arrets:fin.weeks.filter(k=>k.type==='arret').length,semFatigue:fin.weeks.filter(k=>k.sympt).length,ecartP:fin.ecarts.some(e=>e.obj==='principal'),ecartS:fin.ecarts.some(e=>e.obj==='secondaire'),log};
}
const q=(a,p)=>{const b=a.filter(x=>x!=null).slice().sort((x,y)=>x<y?-1:x>y?1:0);return b.length?b[Math.min(b.length-1,Math.floor(p*b.length))]:null;};
function serie(profil,opt,n,seed,conv,subs){
  E=subs?variante(subs):E0;   /* subs : copie du moteur avec une constante interne modifiée (chiffrage d'une proposition, moteur du dépôt intact) */
  const sauv={};Object.keys(conv||{}).forEach(k=>{sauv[k]=E.CONV[k];E.CONV[k]=conv[k];});
  const R=[];try{for(let i=0;i<n;i++)R.push(trajectoire(profil,opt,rng(seed*100003+i)));}finally{Object.keys(sauv).forEach(k=>{E.CONV[k]=sauv[k];});}
  const pc=f=>Math.round(100*R.filter(f).length/R.length);
  return {n,p300:pc(r=>r.maxBloc>=300),p270:pc(r=>r.maxBloc>=270),p240:pc(r=>r.maxBloc>=240),cles3:pc(r=>r.cles>=3),cles2:pc(r=>r.cles>=2),cles1:pc(r=>r.cles>=1),
    maxBloc:[q(R.map(r=>r.maxBloc),0.1),q(R.map(r=>r.maxBloc),0.5),q(R.map(r=>r.maxBloc),0.9)],
    sec219:R[0].maxSec==null?null:pc(r=>r.maxSec>=219),maxSec:R[0].maxSec==null?null:[q(R.map(r=>r.maxSec),0.1),q(R.map(r=>r.maxSec),0.5),q(R.map(r=>r.maxSec),0.9)],
    dplus1350:pc(r=>r.dplusMax>=1350),j180:[q(R.map(r=>r.j180),0.5),q(R.map(r=>r.j180),0.9)],j240:[q(R.map(r=>r.j240),0.5),q(R.map(r=>r.j240),0.9)],j300:[q(R.map(r=>r.j300),0.5),q(R.map(r=>r.j300),0.9)],
    sans300:pc(r=>!r.j300),effond:pc(r=>r.effondrements>0),minPerdues:q(R.filter(r=>r.effondrements).map(r=>Math.round(r.minPerdues)),0.5),
    parPertesFin:[0,1,2,3].map(k=>{const g=R.filter(r=>k<3?r.slPerduesFin===k:r.slPerduesFin>=3);return g.length?[g.length,Math.round(100*g.filter(r=>r.maxBloc>=300).length/g.length)]:[0,null];}),
    slTenues:Math.round(100*R.reduce((a,r)=>a+r.slFaites,0)/R.reduce((a,r)=>a+r.slPrevues,0)),volH:Math.round(q(R.map(r=>r.volH),0.5)),semFatigue:[q(R.map(r=>r.semFatigue),0.1),q(R.map(r=>r.semFatigue),0.5),q(R.map(r=>r.semFatigue),0.9)],arrets:q(R.map(r=>r.arrets),0.5),ecartP:pc(r=>r.ecartP)};
}
module.exports={trajectoire,serie,rng,add,days,ANTOINE,SES0,PROFILS,isRun};
if(require.main===module){
  const n=+process.argv[2]||400,seed=+process.argv[3]||1,filtre=process.argv[4]||'',part=(process.argv[5]||'0/1').split('/').map(Number);   /* part i/k : un scénario sur k (calcul en parallèle) */
  const SC=[];
  for(const profil of Object.keys(PROFILS))for(const p of [0,0.10,0.25,0.40])SC.push({nom:profil+' | '+Math.round(p*100)+' % | hasard',profil,opt:{p}});
  for(const p of [0.10,0.25,0.40]){
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | grappes de 3 sem.',profil:'2 jours',opt:{p,grappe:3}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | semaine chargée (sortie longue protégée)',profil:'2 jours',opt:{p,politique:'chargee'}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | repli 45 min',profil:'2 jours',opt:{p,repli:45}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | repli 90 min',profil:'2 jours',opt:{p,repli:90}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | chargée + repli 90 min',profil:'2 jours',opt:{p,politique:'chargee',repli:90}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | grappes + chargée + repli 90',profil:'2 jours',opt:{p,grappe:3,politique:'chargee',repli:90}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | sans D-96 (arrondiSup=false)',profil:'2 jours',opt:{p},conv:{arrondiSup:false}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | mémoire 2 h (memSeance=120)',profil:'2 jours',opt:{p},conv:{memSeance:120}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | mémoire sans plafond (memSeance=1e9)',profil:'2 jours',opt:{p},conv:{memSeance:1e9}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | mercredi tenu à 60 min',profil:'2 jours',opt:{p,mercMax:60}});
    for(const dec of [4,8,12])SC.push({nom:'2 jours | '+Math.round(p*100)+' % | course décalée de +'+dec+' sem.',profil:'2 jours',opt:{p,goalDate:add('2027-09-25',7*dec)}});
  }
  for(const p of [0,0.10,0.25,0.40])for(const mg of [6,10,99])for(const profil of ['2 jours','2 jours, sans 50 km'])
    SC.push({nom:profil+' | '+Math.round(p*100)+' % | VARIANTE marge de rampe '+mg+' sem.',profil,opt:{p},subs:{MARGE:mg}});
  for(const p of [0.25,0.40])for(const mg of [10,99])SC.push({nom:'2 jours | '+Math.round(p*100)+' % | VARIANTE marge '+mg+' + course décalée de +8 sem.',profil:'2 jours',opt:{p,goalDate:add('2027-09-25',56)},subs:{MARGE:mg}});
  for(const p of [0.25,0.40])SC.push({nom:'2 jours | '+Math.round(p*100)+' % | VARIANTE marge 10 + chargée + repli 90',profil:'2 jours',opt:{p,politique:'chargee',repli:90},subs:{MARGE:10}});
  const COR=require('./corrections.js');
  for(const p of [0,0.10,0.25,0.40]){
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | CORRECTION P-08 (séance fantôme)',profil:'2 jours',opt:{p},subs:{__patch:COR.P08}});
    SC.push({nom:'2 jours | '+Math.round(p*100)+' % | CORRECTION P-08 + P-09',profil:'2 jours',opt:{p},subs:{__patch:COR.P08.concat(COR.P09)}});
    if(p)SC.push({nom:'2 jours | '+Math.round(p*100)+' % | CORRECTION P-08 + P-09 + repli 45 min',profil:'2 jours',opt:{p,repli:45},subs:{__patch:COR.P08.concat(COR.P09)}});
    if(p)SC.push({nom:'2 jours | '+Math.round(p*100)+' % | CORRECTION P-08 + P-09 + sortie longue protégée',profil:'2 jours',opt:{p,politique:'chargee'},subs:{__patch:COR.P08.concat(COR.P09)}});
    if(p)SC.push({nom:'2 jours | '+Math.round(p*100)+' % | CORRECTION P-08 + P-09 + grappes',profil:'2 jours',opt:{p,grappe:3},subs:{__patch:COR.P08.concat(COR.P09)}});
  }
  for(const p of [0,0.25])SC.push({nom:'2 jours | '+Math.round(p*100)+' % | BRUIT ressenti 3 ± 1 (aucune fatigue réelle)',profil:'2 jours',opt:{p,rpeBruit:true}});
  for(const p of [0,0.25])SC.push({nom:'2 jours | '+Math.round(p*100)+' % | BRUIT léger : 3/10, et 2 ou 4 une fois sur cinq',profil:'2 jours',opt:{p,rpeBruit:0.3}});
  SC.push({nom:'2 j → 3 j enchaîné dès F3 | 0 % | BRUIT ressenti 3 ± 1 (aucune fatigue réelle)',profil:'2 j → 3 j enchaîné dès F3',opt:{p:0,rpeBruit:true}});
  const out={};let idx=0;
  for(const sc of SC){if(filtre&&!sc.nom.includes(filtre))continue;if((idx++)%part[1]!==part[0])continue;const r=serie(sc.profil,sc.opt,(sc.opt.p===0&&!sc.opt.rpeBruit)?1:n,seed,sc.conv,sc.subs);out[sc.nom]=r;
    console.log(sc.nom.padEnd(62),'SL≥5h',String(r.p300).padStart(3)+'%','≥4h30',String(r.p270).padStart(3)+'%','3 clés',String(r.cles3).padStart(3)+'%','max bloc P10/50/90',r.maxBloc.join('/'),'| 50 km',r.sec219==null?'—':r.sec219+'%','| effondr.',r.effond+'%','| SL tenues',r.slTenues+'%','| 5h le',r.j300[0]||'jamais');}
  const dir=path.join(__dirname,'out');fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,'adherence'+(filtre?'-'+filtre.replace(/[^a-z0-9]+/gi,'_'):'')+'-'+seed+(part[1]>1?'-'+part[0]:'')+'.json'),JSON.stringify(out,null,1));
}
