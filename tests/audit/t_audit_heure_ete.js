/* Audit mission 2 — défaut reproductible : numéro de semaine le lundi en heure d'été.
   todayW et runsW utilisent Math.floor((D(a)-D(start))/(7*DAY)) : pour un plan démarré en heure d'hiver,
   un lundi d'heure d'été est à (7k jours − 1 h) du départ → floor donne k−1. Tout le lundi, le moteur se croit
   encore la semaine précédente : la semaine écoulée n'est pas « passée » (séances manquées et ressenti ignorés),
   et une course faite un lundi est comptée dans la semaine d'avant.
   ATTENDU ROUGE sur main (v54). Passe au vert avec Math.round sur le lundi de la date (proposition P-07, docs/audit/propositions.md).
   Lancer : node tests/audit/t_audit_heure_ete.js   (le fuseau Europe/Paris est forcé ici) */
process.env.TZ='Europe/Paris';
const E=require('../engine.js');
const isRun=s=>['ef','long','qual','race','desc'].includes(s.type);
const P={goalDate:'2027-09-25',goalDist:80,goalDplus:4500,planStart:'2026-11-02',days:{run:[3,0],long:0,cf:[]},modules:{},
  start:{lastLong:{date:'2026-10-25',dur:107,dist:12,dplus:500},freq4w:1,dur4w:45},races:[]};
let ko=0;const ok=(c,t)=>{console.log((c?'✓ ':'✗ ')+t);if(!c)ko++;};
/* 1. semaine du 5 au 11 juillet 2027 sans aucune course : le lundi 12 comme le mardi 13, elle doit être une semaine « arrêt » */
const ses=[{date:'2027-06-27',type:'long',dur:120,rpe:3}];
const typ=today=>{const o=E.build({profile:P,today,sessions:ses,isRun});return o.weeks.find(k=>k.mon==='2027-07-05').type;};
ok(typ('2027-07-13')==='arret','mardi 13/07/2027 : la semaine du 05/07 sans course est « arrêt » ('+typ('2027-07-13')+')');
ok(typ('2027-07-12')==='arret','lundi 12/07/2027 (heure d\'été) : même verdict attendu ('+typ('2027-07-12')+')');
/* 2. même test en hiver : pas de défaut */
const typH=today=>{const o=E.build({profile:P,today,sessions:[],isRun});return o.weeks.find(k=>k.mon==='2027-01-04').type;};
ok(typH('2027-01-11')===typH('2027-01-12'),'lundi 11/01/2027 (heure d\'hiver) : même verdict que le mardi ('+typH('2027-01-11')+')');
/* 3. une course faite un lundi d'été compte dans SA semaine : la semaine du 05/07 ne doit pas être « arrêt » */
const ses3=[{date:'2027-07-05',type:'ef',dur:40,rpe:3}];
const o3=E.build({profile:P,today:'2027-07-20',sessions:ses3,isRun});
ok(o3.weeks.find(k=>k.mon==='2027-07-05').type!=='arret','course du lundi 05/07/2027 comptée dans la semaine du 05/07 ('+o3.weeks.find(k=>k.mon==='2027-07-05').type+' ; semaine du 28/06 : '+o3.weeks.find(k=>k.mon==='2027-06-28').type+')');
console.log(ko?ko+' défaut(s) reproduit(s)':'0 défaut');if(ko)process.exitCode=1;
