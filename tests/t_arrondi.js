/* D-96 : arrondi supérieur de la séance de progression qui bute sur +10 % (H-58). Lance : node t_arrondi.js */
const E=require('./engine.js');const base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
function sl(sup,regles,mod){
  E.CONV.arrondiSup=sup;const p=JSON.parse(JSON.stringify(base));if(mod)mod(p);
  const o=E.build({profile:p,today:'2026-09-27',sessions:[],isRun,regles});
  return o.sessions.filter(s=>s.type==='long').map(s=>s.dur);}
let ok=true;const t=(nom,cond,detail)=>{console.log((cond?'✓ ':'✗ ')+nom+(detail?' ('+detail+')':''));if(!cond)ok=false;};
const sans=p=>{p.start={};};
const off=sl(false,undefined,sans),on=sl(true,undefined,sans);
const i=off.findIndex((d,k)=>d!==on[k]);
t('l\'arrondi supérieur modifie la progression',i>=0,'1re différence : semaine '+(i+1)+', '+off[i]+' → '+on[i]+' min');
t('la 1re séance modifiée passe au multiple de 5 min supérieur, de moins de 5 min',i>=0&&on[i]%5===0&&on[i]>off[i]&&on[i]-off[i]<5);
t('la sortie longue maximale n\'est jamais plus basse',Math.max(...on)>=Math.max(...off),Math.max(...off)+' → '+Math.max(...on)+' min');
const v1a=sl(true,'v1',sans),v1b=sl(false,'v1',sans);
t('règles v1 inchangées (réglage sans effet)',JSON.stringify(v1a)===JSON.stringify(v1b));
E.CONV.arrondiSup=true;
if(!ok)process.exitCode=1;
