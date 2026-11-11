/* Audit — charge une COPIE du moteur avec une constante interne modifiée, pour chiffrer une proposition de spec
   sans toucher tests/engine.js (aucune règle du moteur n'est modifiée dans le dépôt).
   Exemple : require('./variante.js')({MARGE:8}) → moteur identique, marge de la rampe de sortie longue à 8 semaines. */
const fs=require('fs'),path=require('path'),Module=require('module');
module.exports=function(subs){
  let src=fs.readFileSync(path.join(__dirname,'..','engine.js'),'utf8');
  /* __patch : liste de [texte exact du moteur, texte de remplacement] — pour chiffrer une correction proposée */
  for(const [a,b] of (subs&&subs.__patch)||[]){if(!src.includes(a))throw new Error('fragment introuvable : '+a.slice(0,60));src=src.replace(a,b);}
  for(const [k,v] of Object.entries(subs||{})){if(k==='__patch')continue;
    const re=new RegExp('([,\\s]'+k+'=)[^,;]+');if(!re.test(src))throw new Error('constante introuvable : '+k);
    src=src.replace(re,'$1'+v);}
  const m=new Module('engine-variante');m._compile(src,path.join(__dirname,'engine-variante.js'));return m.exports;
};
