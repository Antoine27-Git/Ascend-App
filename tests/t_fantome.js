/* v82 (P-08) : une semaine passée sans sortie longue ne compte pas comme une semaine de sortie longue, même si une autre course a été faite.
   Cas B2 de l'audit du 11/11 : sortie longue manquée en S18, endurance faite. */
process.env.TZ='Europe/Paris';
const E=require('./engine.js'),S=require('./audit/sim_adherence.js'),{add,isRun}=S;
const START='2026-11-02',mon=w=>add(START,(w-1)*7);
let ok=true;const t=(n,c,d)=>{console.log((c?'✓ ':'✗ ')+n+(d?' ('+d+')':''));if(!c)ok=false;};
function rejoue(garde){const P=S.ANTOINE(),ses=S.SES0().slice();
  for(let w=2;w<=18;w++){const o=E.build({profile:P,today:add(mon(w),1),sessions:ses,isRun});
    o.sessions.filter(s=>s.date>=mon(w)&&s.date<add(mon(w),7)&&s.type!=='cf').forEach(s=>{
      if(w===18&&s.type!=='race'&&!garde(s)){P.manques[s.date]='autre';return;}ses.push({date:s.date,type:s.type,dur:s.dur,rpe:3});});}
  const o=E.build({profile:P,today:add(mon(19),1),sessions:ses,isRun});
  const sl=w=>(o.sessions.find(s=>s.type==='long'&&s.date>=mon(w)&&s.date<add(mon(w),7))||{}).dur||0;
  return [sl(19),sl(20),ses];}
const [a19,a20]=rejoue(()=>false),[b19,b20,ses]=rejoue(s=>s.type!=='long');
t('S18 : l\'endurance a bien été faite, pas la sortie longue',ses.some(s=>s.date>=mon(18)&&s.date<mon(19)&&s.type!=='long')&&!ses.some(s=>s.date>=mon(18)&&s.date<mon(19)&&s.type==='long'));
t('S19 : même sortie longue que si rien n\'avait été couru',b19===a19,b19+' contre '+a19+' min');
t('S19 : pas de semaine légère après une semaine sans sortie longue',b19>=180,b19+' min');
t('S20 : la suite est la même',b20===a20,b20+' contre '+a20+' min');
process.exit(ok?0:1);
