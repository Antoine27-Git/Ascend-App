/* Vérifie que le déroulé de chaque séance de course prescrite fait exactement sa durée (toutes les semaines du plan). */
const fs=require('fs'),E=require('./engine.js'),prof=require('./t_prof.json');
const h=fs.readFileSync(__dirname+'/../index.html','utf8');
const i=h.indexOf("const FC_NOTE"),j=h.indexOf("function planText");
const S={profile:prof};const sessionSteps=new Function('S',h.slice(i,j)+';return sessionSteps;')(S);
const isRun=s=>['ef','long','qual','desc'].includes(s.type);
const tot=st=>st.reduce((a,s)=>a+(s.rep?s.rep*(s.on.sec+s.off.sec)/60:s.min),0);
let n=0,bad=[];
for(const today of ['2026-09-27','2027-03-01','2027-07-15']){
  const o=E.build({profile:prof,today,sessions:[],isRun});
  o.sessions.filter(s=>['ef','long','qual'].includes(s.type)).forEach(s=>{n++;const t=tot(sessionSteps(s).steps);if(Math.abs(t-s.dur)>1)bad.push(s.date+' '+s.type+' '+s.dur+' → '+Math.round(t));});}
console.log(n+' séances, '+bad.length+' écarts de durée');bad.slice(0,8).forEach(b=>console.log('  '+b));
if(bad.length)process.exitCode=1;
