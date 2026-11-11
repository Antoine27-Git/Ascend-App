/* Audit mission 2 — corrections PROPOSÉES (P-08, P-09), écrites comme des remplacements de texte appliqués à une COPIE du moteur.
   Sert uniquement à chiffrer l'effet avant de décider. tests/engine.js n'est pas modifié. */
module.exports={
  /* P-08 : une semaine passée où la sortie longue n'a pas été faite ne compte ni comme sortie clé faite ni comme « longue la semaine d'avant » */
  P08:[
    ["if(cle&&lrObj.length){clesFaites++;derniereCle=w;}",
     "if(V2&&past){const rl=Math.max(0,...reels.filter(s=>s.type==='long').map(s=>s.dur||0));lrPrec=rl;}\n    if(cle&&lrObj.length&&(!V2||!past||reels.some(s=>s.type==='long'&&(s.dur||0)>=0.9*lrObj[0].dur))){clesFaites++;derniereCle=w;}"]],
  /* P-09 : le besoin de monter se juge sur le niveau de sortie longue atteint, pas sur une course présente dans la fenêtre des 30 jours */
  P09:[
    ["const dm=lrGel===0?doitMonter(mx):false;","const dm=lrGel===0?doitMonter(Math.min(mx,Math.max(niv,PLANCHER))):false;"]],
};
