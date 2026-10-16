const E=require('./engine.js');const prof=require('./t_prof.json');
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
function simulate(today,rpeFor,skip,raison){ // exécute le plan prescrit semaine par semaine ; renvoie {semaine: {type, sympt, long}}
  let ses=[];const manques={};const prof0=prof;{const prof=Object.assign({},prof0,{manques});const add=(d,n)=>{const x=new Date(d);x.setDate(x.getDate()+n);return x.toISOString().slice(0,10);};
  for(let w=1;w<=15;w++){const mon=add('2026-09-28',(w-1)*7);if(mon>=today)break;
    const o=E.build({profile:prof,today:mon,sessions:ses,isRun});
    o.sessions.filter(s=>s.date>=mon&&s.date<add(mon,7)&&s.type!=='cf'&&s.type!=='race').forEach(s=>{
      if(skip&&skip(w,s)){if(raison)manques[s.date]=raison;return;}ses.push({date:s.date,dur:s.dur,rpe:rpeFor(w,s),type:s.type});});}
  const o=E.build({profile:prof,today,sessions:ses,isRun});const out={};
  o.weeks.slice(5,16).forEach(k=>{const L=o.sessions.find(s=>s.type==='long'&&s.date>=k.mon&&s.date<add(k.mon,7));out[k.w]={type:k.type,sympt:!!k.sympt,long:L?L.dur:0};});return out;}}
const fmt=r=>Object.keys(r).map(w=>'S'+w+':'+r[w].type.slice(0,3)+(r[w].sympt?'!':'')+(r[w].long||'-')).join(' ');
const T='2027-01-11';
/* v2 (D-67) : la sortie longue ne progresse plus après un signal de fatigue */
const R={stable:simulate(T,()=>3),rpe5:simulate(T,(w)=>w===11?5:3),rpe4:simulate(T,(w)=>w===11?4:3),manq:simulate(T,()=>3,(w,s)=>w===11&&s.type==='ef','fatigue'),agenda:simulate(T,()=>3,(w,s)=>w===11&&s.type==='ef','autre'),sansRep:simulate(T,()=>3,(w,s)=>w===11&&s.type==='ef'),none:simulate(T,()=>null)};
console.log('stable        ',fmt(R.stable));console.log('S11 RPE 5     ',fmt(R.rpe5));console.log('S11 RPE 4     ',fmt(R.rpe4));
console.log('S11 manq. fat.',fmt(R.manq));console.log('S11 manq. agd.',fmt(R.agenda));console.log('S11 sans rép. ',fmt(R.sansRep));console.log('sans ressenti ',fmt(R.none));
/* Verdict : après un signal de fatigue (RPE 5 ou séances manquées en S11), la sortie longue ne dépasse pas son niveau de S11 (+5 min d'arrondi) pendant 3 semaines,
   alors que le plan stable continue de monter ; et une semaine à RPE 4 ne déclenche rien. */
const ok=[['RPE 5',R.rpe5],['séances manquées',R.manq]].every(([n,r])=>[12,13,14].every(w=>r[w].long<=r[11].long+5))&&R.stable[15].long>R.rpe5[14].long&&!R.rpe4[11].sympt;
console.log(ok?'gel de la sortie longue après fatigue : ✓':'gel de la sortie longue après fatigue : ✗');if(!ok)process.exitCode=1;
/* D-72 : une séance manquée pour une autre raison (ou sans réponse) n'est pas un signal de fatigue */
const ok2=[R.agenda,R.sansRep].every(r=>fmt(r)===fmt(R.stable));
console.log(ok2?'séance manquée sans fatigue ignorée : ✓':'séance manquée sans fatigue ignorée : ✗');if(!ok2)process.exitCode=1;
