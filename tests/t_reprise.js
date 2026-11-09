/* D-94 : repère de reprise sans effet de seuil (H-40, H-48). Lance : node t_reprise.js */
const E=require('./engine.js');const base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const DEP='2026-11-02';
function sl1(start,ses,depart){
  const P=Object.assign({},base,{planStart:depart||DEP,planFrom:depart||DEP,races:[],start});
  const o=E.build({profile:P,today:depart||DEP,sessions:ses||[],isRun});
  const L=o.sessions.find(s=>s.type==='long');return L?L.dur:0;}
const LL=(date,dur)=>({lastLong:{date,dur,dist:12,dplus:500}});
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};

const rien=sl1(LL('2026-09-06',107)),un30=sl1(LL('2026-09-06',107),[{date:'2026-10-20',type:'ef',dur:30}]);
t('une course de 30 min dans le mois ne change pas la 1re sortie longue',rien===un30,rien+' contre '+un30+' min');
t('reprise après 30 j sans course : au plus 1 h',[107,180,300].every(d=>sl1(LL('2026-09-06',d))<=60),[107,180,300].map(d=>sl1(LL('2026-09-06',d))).join(', ')+' min');
const j85=sl1(LL('2026-08-09',120)),j87=sl1(LL('2026-08-07',120));
t('pas de saut quand la sortie déclarée vieillit (85 j / 87 j)',Math.abs(j85-j87)<=5,j85+' / '+j87+' min');
const peu=sl1(LL('2026-09-20',120),[{date:'2026-10-22',type:'ef',dur:40}]),plus=sl1(LL('2026-09-20',120),[{date:'2026-10-22',type:'ef',dur:40},{date:'2026-10-29',type:'ef',dur:50}]);
t('courir plus ne baisse jamais la 1re sortie longue',plus>=peu,peu+' puis '+plus+' min');
const apres=sl1(LL('2026-09-06',107),[{date:'2026-11-08',type:'long',dur:76}],'2026-11-09');
t('après une sortie réelle, règle des 30 jours stricte (+10 %)',apres<=Math.floor(76*1.1),'76 min faites → '+apres+' min');
const long=sl1(LL('2026-10-15',200),[{date:'2026-10-15',type:'long',dur:200}]);
t('une sortie longue dans les 30 jours garde son plein effet',long>=200,'200 min il y a 18 j → '+long+' min');
const decl=sl1(Object.assign(LL('2026-09-06',107),{freq4w:1,dur4w:120}));
t('la plus longue déclarée du mois vaut au moins la durée moyenne déclarée',decl>=110,'1 × 2 h par semaine → '+decl+' min');
if(!ok)process.exitCode=1;
