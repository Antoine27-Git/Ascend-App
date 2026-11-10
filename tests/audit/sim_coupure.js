/* Audit mission 1 — une seule coupure totale de k semaines (aucune course), placée à chaque semaine possible,
   adhérence parfaite le reste du temps. Répond à : « à partir de quand une coupure est-elle fatale ? »
   Usage : node tests/audit/sim_coupure.js [profil] */
const S=require('./sim_adherence.js'),E=require('../engine.js');
const profil=process.argv[2]||'2 jours';
function essai(k,w0,subs){
  /* on réutilise trajectoire() avec un tirage déterministe : semaine perturbée (tout perdu) si w0 ≤ w < w0+k */
  let w=1;const seq=[];for(let x=2;x<=60;x++){const dans=x>=w0&&x<w0+k;seq.push(dans?0:0.999);if(dans)seq.push(0);}
  let i=0;const rand=()=>seq[i++]!==undefined?seq[i-1]:0.999;
  return S.trajectoire(profil,{p:0.5,both:1},rand);
}
console.log('Profil : '+profil+' — sortie longue max du bloc (min) selon la semaine de début de la coupure');
for(const k of [2,3,4,6,8]){
  const res=[];for(let w0=2;w0<=44;w0++){const r=essai(k,w0);res.push([w0,r.maxBloc,r.maxSec]);}
  const ko=res.filter(r=>r[1]<300).map(r=>r[0]),ko270=res.filter(r=>r[1]<270).map(r=>r[0]),koSec=res.filter(r=>r[2]!=null&&r[2]<219).map(r=>r[0]);
  const plage=a=>{if(!a.length)return 'aucune';const out=[];let d=a[0],p=a[0];for(let i=1;i<=a.length;i++){if(a[i]===p+1){p=a[i];continue;}out.push(d===p?'S'+d:'S'+d+'–S'+p);d=p=a[i];}return out.join(', ');};
  console.log('coupure de '+k+' sem. : 5 h manquées si elle commence en '+plage(ko)+' | 4 h 30 manquées : '+plage(ko270)+' | cible du 50 km manquée : '+plage(koSec));
  console.log('   détail (début:max bloc) '+res.map(r=>r[0]+':'+r[1]).join(' '));
}
