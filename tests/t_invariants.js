/* Invariants du moteur v2 sur des scénarios tirés au hasard (audit de novembre 2026, tests/audit/fuzz.js).
   Garde-fou de non-régression : ne garde que les invariants VERTS sur main (v54), en fuseau UTC
   (en Europe/Paris, le défaut d'heure d'été du lundi les fait échouer : tests/audit/t_audit_heure_ete.js).
   Vérifie sur 120 scénarios rejoués jour après jour : aucune exception, plan déterministe, durées entières positives,
   une course par jour, endurance ≤ 90 min, déroulé = durée, et sortie longue du jour ≤ +10 % de la référence D-94
   (ou multiple de 5 min supérieur, D-96) calculée ici à partir des séances réellement faites. */
process.env.TZ='UTC';
const F=require('./audit/fuzz.js');
const V={};let n=0;for(let i=1;i<=120;i++){const r=F.rejoue(F.scenario(i),V);if(r.ok)n++;}
const GARDES=['I0 exception','I0 plan refusé en cours de route','I2 déterminisme','I2 plan instable dans la semaine','I6 durée invalide','I6 deux courses le même jour','I6 endurance > 90 min','I6 déroulé ≠ durée','I1 règle des 30 jours (sortie longue)'];
let ko=0;GARDES.forEach(k=>{const v=V[k]||[];console.log((v.length?'✗ ':'✓ ')+k+(v.length?' : '+v.length+' cas, graine '+v[0].seed+' — '+v[0].msg:''));ko+=v.length;});
console.log(n+' scénarios rejoués, '+(ko?ko+' violation(s)':'0 violation'));if(ko||n<100)process.exitCode=1;
