/* D-99 : bilan de séance, étage A (calculé ; ne modifie pas le plan). Lance : node t_bilan.js */
const E=require('./engine.js');const base=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
let ok=true;const t=(nom,c,d)=>{console.log((c?'✓ ':'✗ ')+nom+(d?' ('+d+')':''));if(!c)ok=false;};
const P=Object.assign({},base,{planStart:'2026-11-02',planFrom:'2026-11-02',races:[]});
const Z={t:[400,300,1200,1300,400,10,0],b:[140,155,160,165,170,180,200]};
const mk=extra=>{const ses=[{id:'c',date:'2026-11-10',type:'cf',dur:60,rpe:6,cfJ:'fort'},Object.assign({id:'x',date:'2026-11-11',type:'long',dur:60,rpe:3,dplus:164,dminus:150,hrAvg:158,hrZ:Z},extra)];
  const o=E.build({profile:P,today:'2026-11-11',sessions:ses,isRun});const pl=o.sessions.find(x=>x.date==='2026-11-11'&&isRun(x));if(pl)ses[1].plannedId=pl.id;
  return {ses,b:E.bilan({profile:P,today:'2026-11-12',sessions:ses,isRun},'x')};};
const {ses,b}=mk({});
t('temps au-dessus de la zone de base calculé',b.dessusBase===81,b.dessusBase+' %');
t('RPE bas et FC haute : message',b.msgs.some(m=>m.code==='fc-haute'));
t('CrossFit la veille : message',b.msgs.some(m=>m.code==='veille-cf'));
t('effet sur le plan : prochaine sortie longue donnée',b.effet.prochaine&&b.effet.prochaine.dur>0,JSON.stringify(b.effet.prochaine));
const avant=JSON.stringify(E.build({profile:P,today:'2026-11-12',sessions:ses,isRun}).sessions);E.bilan({profile:P,today:'2026-11-12',sessions:ses,isRun},'x');
t('le bilan ne modifie pas le plan',JSON.stringify(E.build({profile:P,today:'2026-11-12',sessions:ses,isRun}).sessions)===avant);
/* v58 : zones figées par intervals.icu à l'import (zone de base jusqu'à 166 au lieu de 155) : temps par zone refusé, message explicite */
const vieux=mk({hrZ:{t:[1110,1969,524,0,0,0,0],b:[157,166,175,185,190,196,205]}}).b;
t('zones périmées : pas de « temps au-dessus de la base »',vieux.dessusBase===null&&!vieux.zones,String(vieux.dessusBase));
t('zones périmées : message explicite',vieux.msgs.some(m=>m.code==='zones-decalees'&&/166/.test(m.txt)&&/155/.test(m.txt)));
t('zones périmées : pas de faux message « cœur haut »',!vieux.msgs.some(m=>m.code==='fc-haute'));
const sansZ=mk({hrZ:null}).b;t('sans zones : pas de message FC, indicateur de repli',!sansZ.msgs.some(m=>m.code==='fc-haute')&&sansZ.indicateur!=='zones');
const fort=mk({rpe:8,hrZ:{t:[2000,1500,100,0,0,0,0],b:Z.b}}).b;t('RPE haut et FC basse : message',fort.msgs.some(m=>m.code==='fc-basse'));
t('séance inconnue : null',E.bilan({profile:P,today:'2026-11-12',sessions:ses,isRun},'zz')===null);
if(!ok)process.exitCode=1;
