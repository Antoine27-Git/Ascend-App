/* D-107 : une séance ne relève la référence des 30 jours que de +10 % au plus (H-71). Lance : node t_plafond.js */
const E=require('./engine.js');const base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const DEP='2026-11-02';
const P=Object.assign({},base,{planStart:DEP,planFrom:DEP,races:[],start:{lastLong:{date:'2026-10-25',dur:60,dist:9,dplus:150}}});
const plan=(ses,today,conv)=>{const old=E.CONV.plafondSaut;if(conv!=null)E.CONV.plafondSaut=conv;const o=E.build({profile:P,today,sessions:ses,isRun});E.CONV.plafondSaut=old;return o;};
const sl=(o,from)=>(o.sessions.filter(s=>s.type==='long'&&s.date>=from).sort((a,b)=>a.date<b.date?-1:1)[0]||{}).dur||0;
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};
const S=d=>[{id:'a',date:'2026-11-08',type:'long',dur:d}];
const prevu=sl(plan([], '2026-11-02'),'2026-11-02');
const n66=sl(plan(S(66),'2026-11-09'),'2026-11-09'),n75=sl(plan(S(75),'2026-11-09'),'2026-11-09'),n180=sl(plan(S(180),'2026-11-09'),'2026-11-09');
t('une sortie faite comme prévu n\'est pas plafonnée',plan(S(prevu),'2026-11-09').info.plafonds.length===0,'prévu '+prevu+' min');
t('un saut (75 min pour 60 de référence) ne donne rien de plus que la hausse permise (66 min)',n75===n66,'suivante : '+n75+' min, comme après 66 min ('+n66+')');
t('un gros saut (3 h) non plus',n180===n66,'suivante : '+n180+' min');
t('la suivante reste dans +10 % de la référence retenue (66 min), arrondi D-96 compris',n180<=75,n180+' min');
const pf=plan(S(180),'2026-11-09').info.plafonds[0];
t('le saut est signalé avec ses chiffres',pf&&pf.date==='2026-11-08'&&pf.dur===180&&pf.retenu===66&&pf.ref===60,JSON.stringify(pf));
t('sans le réglage, la séance compte en entier (ancien comportement)',sl(plan(S(180),'2026-11-09',false),'2026-11-09')>n180);
t('une sortie plus courte que la référence ne change rien au plafonnement',plan(S(40),'2026-11-09').info.plafonds.length===0);
/* bilan : effet sur le plan */
const b=E.bilan({profile:P,today:'2026-11-08',sessions:S(180),isRun},'a');
t('bilan : raison « saut », pourcentage et phrase',b.effet.raison==='saut'&&b.effet.saut.pct===200&&/garde-fou/.test(b.effet.txt),b.effet.txt);
t('bilan : le constat des 30 jours renvoie à l\'effet sur le plan',b.msgs.some(m=>m.code==='30j'&&/effet sur le plan/.test(m.txt)));
const b2=E.bilan({profile:P,today:'2026-11-08',sessions:S(prevu),isRun},'a');
t('bilan : séance prévue → jamais « saut »',b2.effet.raison!=='saut',b2.effet.raison+' · '+b2.effet.txt);
const b3=E.bilan({profile:P,today:'2026-11-05',sessions:[{id:'e',date:'2026-11-05',type:'ef',dur:30}],isRun},'e');
t('bilan : petite endurance → « dans les clous »',b3.effet.raison==='clous'&&/dans les clous/.test(b3.effet.txt),b3.effet.raison);
if(!ok)process.exitCode=1;
