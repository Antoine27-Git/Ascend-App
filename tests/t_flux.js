/* D-100 : zones de Karvonen et indicateurs seconde par seconde. Lance : node t_flux.js */
const E=require('./engine.js');
let ok=true;const t=(nom,c,d)=>{console.log((c?'✓ ':'✗ ')+nom+(d!=null?' ('+d+')':''));if(!c)ok=false;};
/* Karvonen : FC repos 50, FC max 200 → 140 / 155 / 170 / 185 ; 205 → 143 / 158 / 174 / 189 */
t('Karvonen 200/50',JSON.stringify(E.zonesKarvonen(200,50))==='[140,155,170,185]');
t('Karvonen 205/50',JSON.stringify(E.zonesKarvonen(205,50))==='[143,158,174,189]');
t('Karvonen incomplet : pas de zones',E.zonesKarvonen(null,50)===null&&E.zonesKarvonen(205,null)===null&&E.zonesKarvonen(90,60)===null);
/* synthétique : 30 min à FC 150 sur le plat, 3 m/s, puis 30 min à 165 en montée à 10 % (2 m/s) */
const syn=(()=>{const T=[],H=[],D=[],A=[];let d=0,a=100;for(let i=0;i<=3600;i++){T.push(i);const mt=i>1800;H.push(mt?165:150);d+=mt?2:3;if(mt)a+=0.2;D.push(d);A.push(a);}return {time:T,hr:H,dist:D,alt:A};})();
const s1=E.flux(syn,E.zonesKarvonen(200,50));
t('synthétique : 50 % au-dessus de 155',s1.zones.dessusBase===50,s1.zones.dessusBase);
t('synthétique : montée ~30 min à FC 165, 7,2 km/h',s1.terrain.montee&&Math.abs(s1.terrain.montee.min-30)<=1&&s1.terrain.montee.fc===165&&Math.abs(s1.terrain.montee.kmh-7.2)<0.2,JSON.stringify(s1.terrain.montee));
t('synthétique : plat ~30 min à FC 150',s1.terrain.plat&&Math.abs(s1.terrain.plat.min-30)<=1&&s1.terrain.plat.fc===150,JSON.stringify(s1.terrain.plat));
t('synthétique : vitesse de montée ~720 m/h',Math.abs(s1.vam-720)<=15,s1.vam);
t('synthétique : tranches par km, 9 km',s1.tranches.length===9&&Math.abs(s1.tranches[0].allure-333)<=2,JSON.stringify(s1.tranches[0]));
/* pause > 10 s non comptée */
const pz=JSON.parse(JSON.stringify(syn));for(let i=1000;i<pz.time.length;i++)pz.time[i]+=600;
t('pause de 10 min non comptée',E.flux(pz,null).min===60,E.flux(pz,null).min);
t('données trop courtes : null',E.flux({time:[0,1,2],hr:[1,2,3]},null)===null);
const q0=()=>E.flux(require('./data/flux_42km.json'),E.zonesKarvonen(205,50));
/* trace réelle du 11/11/2026 (1 h, 8,7 km) */
const r=E.flux(require('./data/flux_20261111.json'),E.zonesKarvonen(200,50));
t('11/11 : 76 % au-dessus de 155 (le bilan v57 affichait 15 %)',r.zones.dessusBase===76,r.zones.dessusBase);
t('11/11 : FC de croisière 160-164, départ ~140',r.croisiere.fc>=160&&r.croisiere.fc<=164&&r.croisiere.depart<=145,JSON.stringify(r.croisiere));
t('11/11 : 9 tranches, km 1 à FC ~132',r.tranches.length===9&&r.tranches[0].fc<=135,r.tranches[0].fc);
t('11/11 : FC en descente 6 bpm sous la montée (pas de constat « descente »)',r.terrain.montee.fc-r.terrain.descente.fc===6,r.terrain.descente.fc+' / '+r.terrain.montee.fc);
t('42 km : FC en descente au-dessus de la montée',q0().terrain.descente.fc>q0().terrain.montee.fc,q0().terrain.descente.fc+' / '+q0().terrain.montee.fc);
/* trace réelle du trail de 42 km (6 h 53) : tranches par 5 km */
const q=E.flux(require('./data/flux_42km.json'),E.zonesKarvonen(205,50));
t('42 km : tranches regroupées par 5 km',q.tranches.length===9&&q.tranches[1].de===5,q.tranches.length);
t('42 km : vitesse de montée calculée',q.vam>300&&q.vam<900,q.vam);
/* bilan : le flux prend le pas sur les zones figées d'intervals.icu (v58) */
const base=require('./t_prof.json'),isRun=s=>['ef','long','qual','desc'].includes(s.type);
const P=Object.assign({},base,{planStart:'2026-11-02',planFrom:'2026-11-02',races:[],fcMax:200,fcRepos:50});
const ses=[{id:'x',date:'2026-11-11',type:'long',dur:60,rpe:3,dplus:164,hrAvg:158,hrZ:{t:[1110,1969,524,0,0,0,0],b:[157,166,175,185,190,196,205]},flux:r}];
const b=E.bilan({profile:P,today:'2026-11-12',sessions:ses,isRun},'x');
t('bilan : zones de l\'appli malgré les zones figées',b.dessusBase===76&&!b.msgs.some(m=>m.code==='zones-decalees'),b.dessusBase);
t('bilan 11/11 : constat croisière (162, 7 au-dessus de 155), pas de constat descente',b.msgs.some(m=>m.code==='croisiere'&&/162/.test(m.txt)&&/7 au-dessus/.test(m.txt))&&!b.msgs.some(m=>m.code==='descente'));
const b42=E.bilan({profile:P,today:'2026-11-12',sessions:[Object.assign({},ses[0],{flux:q0()})],isRun},'x');
t('bilan 42 km : constat descente, symbole ▲',b42.msgs.some(m=>m.code==='descente'&&m.sym==='▲'));
t('bilan : RPE 3 et 76 % au-dessus → « cœur plus haut que le ressenti »',b.msgs.some(m=>m.code==='fc-haute'));
t('bilan : résumé du flux transmis (sans trace brute)',b.flux&&b.flux.terrain&&!b.flux.time,JSON.stringify(b.flux).length+' o');
const b2=E.bilan({profile:Object.assign({},P,{fcMax:205}),today:'2026-11-12',sessions:[Object.assign({},ses[0],{flux:null})],isRun},'x');
t('sans flux, FC max 205 : garde-fou sur la borne 158',b2.msgs.some(m=>m.code==='zones-decalees'&&/158/.test(m.txt)));
process.exit(ok?0:1);
