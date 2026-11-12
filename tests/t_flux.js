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
t('11/11 : pente sur 200 m, FC en descente 4 bpm sous la montée',r.terrain.montee.fc-r.terrain.descente.fc===4,r.terrain.descente.fc+' / '+r.terrain.montee.fc);
t('11/11 : 5 catégories, faux plat montant ~15 min (le début de la sortie)',['montee','fpm','plat','fpd','descente'].every(k=>r.terrain[k])&&Math.abs(r.terrain.fpm.min-15)<=2,JSON.stringify(r.terrain.fpm));
t('11/11 : équivalent plat de la montée ~6:08 (Minetti), plus rapide que l\'allure réelle',r.terrain.montee.eq<r.terrain.montee.allure&&Math.abs(r.terrain.montee.eq-368)<=10,r.terrain.montee.allure+' → '+r.terrain.montee.eq);
t('11/11 : plat ≈ équivalent plat ; pas d\'équivalent en descente',Math.abs(r.terrain.plat.eq-r.terrain.plat.allure)<=3&&r.terrain.descente.eq===null);
t('11/11 : pas de dérive calculée (moins de 40 min utiles)',r.derive===null);
t('synthétique : minetti(0)=3,6, montée plus chère',E.minetti(0)===3.6&&E.minetti(0.1)>E.minetti(0)&&E.minetti(-0.1)<E.minetti(0));
t('42 km : FC en descente au-dessus de la montée',q0().terrain.descente.fc>q0().terrain.montee.fc,q0().terrain.descente.fc+' / '+q0().terrain.montee.fc);
/* trace réelle du trail de 42 km (6 h 53) : tranches par 5 km */
const q=E.flux(require('./data/flux_42km.json'),E.zonesKarvonen(205,50));
t('42 km : tranches regroupées par 5 km',q.tranches.length===9&&q.tranches[1].de===5,q.tranches.length);
t('42 km : vitesse de montée calculée',q.vam>300&&q.vam<900,q.vam);
t('42 km : dérive ~+21 %, FC qui baisse (fatigue des jambes)',q.derive&&q.derive.pct>15&&q.derive.pct<27&&q.derive.fc2<q.derive.fc1,JSON.stringify(q.derive));
/* bilan : le flux prend le pas sur les zones figées d'intervals.icu (v58) */
const base=require('./t_prof.json'),isRun=s=>['ef','long','qual','desc'].includes(s.type);
const P=Object.assign({},base,{planStart:'2026-11-02',planFrom:'2026-11-02',races:[],fcMax:200,fcRepos:50});
const ses=[{id:'x',date:'2026-11-11',type:'long',dur:60,rpe:3,dplus:164,hrAvg:158,hrZ:{t:[1110,1969,524,0,0,0,0],b:[157,166,175,185,190,196,205]},flux:r}];
const b=E.bilan({profile:P,today:'2026-11-12',sessions:ses,isRun},'x');
t('bilan : zones de l\'appli malgré les zones figées',b.dessusBase===76&&!b.msgs.some(m=>m.code==='zones-decalees'),b.dessusBase);
t('bilan 11/11 : constat croisière (162, 7 au-dessus de 155) et constat descente (écart 4 < 5)',b.msgs.some(m=>m.code==='croisiere'&&/162/.test(m.txt)&&/7 bpm au-dessus/.test(m.txt))&&b.msgs.some(m=>m.code==='descente'));
const b42=E.bilan({profile:P,today:'2026-11-12',sessions:[Object.assign({},ses[0],{flux:q0()})],isRun},'x');
t('bilan 42 km : constat descente, symbole ▲',b42.msgs.some(m=>m.code==='descente'&&m.sym==='▲'));
t('bilan 42 km : constat « fatigue des jambes »',b42.msgs.some(m=>m.code==='derive'&&/Fatigue des jambes/.test(m.txt)&&m.sym==='▲'),(b42.msgs.find(m=>m.code==='derive')||{}).txt);
t('bilan : RPE 3 et 76 % au-dessus → « FC plus haute que le ressenti »',b.msgs.some(m=>m.code==='fc-haute'));
t('bilan : résumé du flux transmis (sans trace brute)',b.flux&&b.flux.terrain&&!b.flux.time,JSON.stringify(b.flux).length+' o');
const b2=E.bilan({profile:Object.assign({},P,{fcMax:205}),today:'2026-11-12',sessions:[Object.assign({},ses[0],{flux:null})],isRun},'x');
t('sans flux, FC max 205 : garde-fou sur la borne 158',b2.msgs.some(m=>m.code==='zones-decalees'&&/158/.test(m.txt)));
/* D-101 : repères de progression (FC de référence 159, repos 52) */
{const z=E.zonesKarvonen(205,52),a=E.flux(require('./data/flux_20261111.json'),z),k=E.flux(require('./data/flux_42km.json'),z);
 const ra=E.repSeance(a,60,159,52),rk=E.repSeance(k,413,159,52);
 t('11/11 : allure facile ~6:34/km à 159 bpm, montée ~377 m/h, pas de tenue (1 h)',Math.abs(ra.allure-394)<=4&&Math.abs(ra.montee-377)<=6&&ra.tenue==null,JSON.stringify(ra));
 t('42 km : tenue 21 %, allure facile plus lente que le 11/11',rk.tenue>15&&rk.allure>ra.allure,JSON.stringify(rk));
 const P1=E.progression([{date:'2026-11-11',dur:60,flux:a}],{start:'2026-11-02',today:'2026-11-12',ref:159,repos:52});
 t('une seule sortie : départ provisoire, 1re mesure',P1.allure.provisoire&&P1.allure.verdict==='premiere'&&P1.allure.now==null&&P1.tenue===null);
 const fake=(d,al)=>({date:d,dur:60,flux:Object.assign({},a,{util:Object.assign({},a.util,{v:1000/al*(a.util.fc-52)/107})})});
 const P2=E.progression([fake('2026-09-01',420),fake('2026-09-05',420),fake('2026-10-01',410),fake('2026-10-04',410),fake('2026-11-05',395),fake('2026-11-10',395)],{start:'2026-08-31',today:'2026-11-12',ref:159,repos:52});
 t('progression : 7:00 → 6:50 → 6:35, « en progrès »',P2.allure.depart===420&&P2.allure.s6===410&&P2.allure.now===395&&P2.allure.verdict==='progres',JSON.stringify(P2.allure));
 const P3=E.progression([fake('2026-10-01',400),fake('2026-10-04',400),fake('2026-11-05',405),fake('2026-11-10',405)],{start:'2026-08-31',today:'2026-11-12',ref:159,repos:52});
 t('écart de 1,25 % : « stable »',P3.allure.verdict==='stable',P3.allure.ecart);
 t('avant le début du plan : ignoré',E.progression([fake('2026-08-20',420)],{start:'2026-08-31',today:'2026-11-12',ref:159,repos:52}).allure===null);}
process.exit(ok?0:1);
