/* D-67/D-68 : propriétés du moteur v2 sur 8 profils (lancer : node t_profils.js [v1] [détail <profil>]) */
const E=require('./engine.js'),base=require('./t_prof.json');
const regles=process.argv[2]==='v1'?'v1':undefined,detail=process.argv[3]==='detail'?process.argv[4]:null;
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const PROFILS={
 '4 jours':p=>{},
 '2 jours (mer. + dim.)':p=>{p.days={run:[3,0],long:0,cf:[2,5],time:{3:60}};},   /* time ignoré en v2 (D-71) */
 '3 jours':p=>{p.days={run:[3,6,0],long:0,cf:[2],time:{}};},
 '6 jours':p=>{p.days={run:[1,2,3,4,6,0],long:0,cf:[],time:{}};p.modules.strength=false;},
 'sans objectif second.':p=>{p.races=[];},
 'second. 30 km':p=>{p.races=[{name:'30k',date:'2027-04-10',dist:30,dplus:1200,prio:'B'}];},
 'sans historique':p=>{p.start={};},
 '80 km second. + 160 km':p=>{p.goalDist=160;p.goalDplus=9000;p.goalDate='2027-09-26';p.days={run:[3,6,0],long:0,cf:[2],time:{}};p.orgs=[{from:'F3',enchaine:true,days:{run:[3,6,0],long:0,cf:[2],time:{}}}];p.races=[{name:'80k',date:'2027-06-05',dist:80,dplus:4000,prio:'B'}];},
 '2 j → enchaîné dès F3':p=>{p.days={run:[3,0],long:0,cf:[2,5]};p.orgs=[{from:'F3',enchaine:true,days:{run:[3,6,0],long:0,cf:[2]}}];},
};
const fin=(k)=>new Date(new Date(k.mon).getTime()+7*864e5).toISOString().slice(0,10);
let fails=0;
for(const [nom,mod] of Object.entries(PROFILS)){
  const p=JSON.parse(JSON.stringify(base));mod(p);
  const o=E.build({profile:p,today:'2026-09-27',sessions:[],isRun,regles});
  const pb=[];const hist=[];const St=p.start||{};
  if(St.lastLong&&St.lastLong.date){const j=(new Date(St.lastLong.date)-new Date(o.info.start))/864e5;hist.push({j,d:+St.lastLong.dur,repr:true});}
  const cal=o.info.cal,secW=(p.races||[]).map(r=>Math.round((new Date(r.date)-new Date(o.info.start))/(7*864e5))+1);
  let maxAvantSec=0,maxBloc=0,prevL=null;
  o.weeks.forEach(k=>{const s=o.sessions.filter(x=>x.date>=k.mon&&x.date<fin(k)&&x.type!=='cf');
    const L=s.filter(x=>x.type==='long')[0],efs=s.filter(x=>x.type==='ef'&&x.title!=='Week-end de choc');
    if(!regles)efs.forEach(x=>{if(x.dur>90)pb.push('S'+k.w+' endurance '+x.dur);});
    if(L&&k.type==='charge'&&s.some(x=>x.type!=='long'&&x.type!=='race'&&x.dur>L.dur))pb.push('S'+k.w+' sortie longue '+L.dur+' < autre séance');
    if(L&&k.type==='relache'&&prevL&&L.dur>prevL)pb.push('S'+k.w+' semaine allégée : sortie longue '+L.dur+' > '+prevL);
    s.forEach(x=>{const j=(new Date(x.date)-new Date(o.info.start))/864e5;
      /* repère de reprise (H-40) : sortie déclarée sortie de la fenêtre depuis moins de 8 semaines, dégressive */
      const m=Math.max(0,...hist.filter(h=>h.j>=j-30&&h.j<j).map(h=>h.d),...hist.filter(h=>h.repr&&j<30&&-h.j<86).map(h=>h.d*Math.max(0.65,1-0.07*Math.max(0,Math.ceil((-h.j-23)/7)))));if(x.type!=='race'&&m&&x.dur>1.1*m+1&&x.type==='long')pb.push('S'+k.w+' règle des 30 j : '+x.dur+' > 1,1 × '+m);hist.push({j,d:x.dur});});
    if(L){if(secW.length&&k.w<secW[0]-2)maxAvantSec=Math.max(maxAvantSec,L.dur);if(k.phase==='bloc'||k.phase==='pic')maxBloc=Math.max(maxBloc,L.dur);if(k.type==='charge')prevL=L.dur;}
    if(detail===nom)console.log('S'+k.w,(k.sous||k.phase).padEnd(8),k.type.padEnd(9),(k.jours||[]).join(''),s.map(x=>(x.title==='Week-end de choc'?'m':x.type[0])+x.dur).join(' '));});
  const dS=o.sessions.find(x=>x.type==='race'&&x.date!==p.goalDate)?.dur||0,plaf=dS>=480?300:dS>=240?210:180,cibleSec=secW.length?Math.round(regles?Math.min(dS,plaf*1.1)/1.1:Math.min(0.5*dS,270)):null;
  if(!regles&&maxBloc<o.info.cal&&false);
  const res=[nom.padEnd(22),'SL max avant objectif second. : '+(secW.length?maxAvantSec+'/'+cibleSec:'—'),'· SL max bloc : '+maxBloc];
  console.log(res.join(' '),pb.length?'  ✗ '+pb.slice(0,3).join(' ; ')+(pb.length>3?' (+'+(pb.length-3)+')':''):'  ✓');fails+=pb.length;}
console.log(fails?fails+' violations':'0 violation');
if(fails)process.exitCode=1;

/* D-71 : le temps disponible par jour n'a plus d'effet en v2 (mêmes séances avec ou sans) */
if(!regles){const sig=t=>{const p=JSON.parse(JSON.stringify(base));p.days={run:[3,0],long:0,cf:[2,5],time:t};const o=E.build({profile:p,today:'2026-09-27',sessions:[],isRun});return JSON.stringify(o.sessions.map(x=>[x.date,x.type,x.dur]));};
  const ok=sig({})===sig({3:60});console.log(ok?'temps disponible ignoré : ✓':'temps disponible ignoré : ✗');if(!ok)process.exitCode=1;
  /* endurance ≤ 1 h 30 sur toute la durée du plan */
  const p=JSON.parse(JSON.stringify(base));const o=E.build({profile:p,today:'2026-09-27',sessions:[],isRun});const m=Math.max(...o.sessions.filter(x=>x.type==='ef'&&x.title!=='Week-end de choc').map(x=>x.dur));console.log('endurance max : '+m+' min '+(m<=90?'✓':'✗'));}
/* D-69 : écarts de projection — aucun pour les profils avec historique, deux pour « sans historique » */
if(!regles){const ec=m=>{const p=JSON.parse(JSON.stringify(base));m(p);return E.build({profile:p,today:'2026-09-27',sessions:[],isRun}).ecarts.map(e=>e.obj).join(',');};
  const a=ec(p=>{}),b=ec(p=>{p.start={};});const ok=a===''&&b==='secondaire,principal';
  console.log('écarts : avec historique ['+a+'] · sans historique ['+b+'] '+(ok?'✓':'✗'));if(!ok)process.exitCode=1;}

/* D-75 : le D+ de départ ne se nourrit pas des endurances plates prescrites par le plan (densité en m/h de la semaine en cours) */
{const E2=require('./engine.js'),p0=require('./t_prof.json');const isR=s=>['ef','long','qual','desc'].includes(s.type);
 const P=Object.assign({},p0,{days:{run:[3,0],long:0,cf:[2],time:{}}});
 const dz=ses=>{const o=E2.build({profile:P,today:'2026-10-09',sessions:ses,isRun:isR});return Math.round(o.weeks.find(k=>k.mon<='2026-10-09'&&k.mon>'2026-10-02').dens);};
 const plates=[{date:'2026-09-30',type:'ef',dur:60,dplus:40},{date:'2026-09-23',type:'ef',dur:60,dplus:50}];
 const a=dz([]),b=dz(plates.concat([{date:'2026-10-04',type:'long',dur:100,dplus:100}])),c=dz([{date:'2026-09-20',type:'long',dur:100,dplus:100}]);
 const ok=b===a&&c<a;
 console.log('densité de D+ (m/h) : déclaration '+a+', + séances après démarrage '+b+' (identique attendu), + SL plate avant démarrage '+c+' (plus bas attendu) → '+(ok?'✓':'✗'));
 if(!ok)process.exitCode=1;}
