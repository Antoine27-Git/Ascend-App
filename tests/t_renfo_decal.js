/* v80 : un renforcement se déplace dans sa semaine (clé « x:date ») ; jamais deux renforcements le même jour ; les courses ne bougent pas. */
const E=require('./engine.js'),base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
let ok=true;const t=(nom,c,d)=>{console.log((c?'✓ ':'✗ ')+nom+(d?' ('+d+')':''));if(!c)ok=false;};
const sem=(decal)=>{const P=Object.assign({},base,{planStart:'2026-11-02',decal});const o=E.build({profile:P,today:'2026-11-24',sessions:[],isRun});
  return o.sessions.filter(s=>s.date>='2026-11-23'&&s.date<='2026-11-29');};
const ref=sem({}),runsRef=JSON.stringify(ref.filter(isRun));
const a=sem({'x:2026-11-26':'2026-11-25'}),cfA=a.find(s=>s.id==='g2026-11-26-cf');
t('le renforcement de jeudi passe mercredi',cfA&&cfA.date==='2026-11-25'&&cfA.decale==='2026-11-26');
t('les courses ne bougent pas',JSON.stringify(a.filter(isRun))===runsRef);
const b=sem({'x:2026-11-26':'2026-11-23'});
t('refusé si un autre renforcement est déjà ce jour-là',b.find(s=>s.id==='g2026-11-26-cf').date==='2026-11-26');
const c=sem({'x:2026-11-26':'2026-11-28'}),cfC=c.find(s=>s.id==='g2026-11-26-cf');
t('veille de la sortie longue : contenu haut du corps et gainage',cfC.date==='2026-11-28'&&/Haut du corps|sans jambes lourdes/.test(cfC.note),cfC.note);
const d=sem({'x:2026-11-26':'2026-12-02'});
t('jamais hors de la semaine',d.find(s=>s.id==='g2026-11-26-cf').date==='2026-11-26');
const e=sem({'2026-11-26':'2026-11-27'});
t('la clé d\'une course ne déplace pas le renforcement du même jour',e.find(s=>s.id==='g2026-11-26-cf').date==='2026-11-26');
process.exit(ok?0:1);
