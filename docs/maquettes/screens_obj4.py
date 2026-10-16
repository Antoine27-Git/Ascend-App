from base import *
from screens_prof2 import sub
from screens_prof6 import LN
R=[('Trail de la Croix-Rousse','14','mars','2027','23','800','≈ 3 h 20','entraînement','#c9d1cb',149),
   ('Trail des Coursières 2027','8','mai','2027','50','1 900','≈ 8 h 15','objectif','#25c37e',204),
   ('Objectif Perso 80kms','25','sept.','2027','80','5 000','≈ 16 h 30','course objectif','#10251c',344)]
CSS='<style>.st3{display:grid;grid-template-columns:1fr 1.2fr 1.2fr;gap:6px;margin-top:8px}.st3 b{font-size:17px;white-space:nowrap}.st3 span{display:block;font-size:12px;color:var(--mut);margin-top:1px}.st3.big b{font-size:21px}</style>'
def st3(r,big=False):
    return '<div class="st3%s"><div><b>%s</b><span>km</span></div><div><b>%s</b><span>m D+</span></div><div><b>%s</b><span>durée estimée</span></div></div>'%(' big' if big else '',r[4],r[5],r[6])
def pill(r):
    if r[7]=='course objectif': return '<span class="pill" style="font-size:11.5px;background:#10251c;color:#fff">course objectif</span>'
    return '<span class="pill %s" style="font-size:11.5px">%s</span>'%('ok' if r[7]=='objectif' else 'grey',r[7])
# C : frise verticale
def objC():
    def node(r,last=False):
        big=r[7]=='course objectif'
        dot='<div style="width:%dpx;height:%dpx;border-radius:50%%;background:%s;flex:none;margin-top:%dpx;position:relative;z-index:1;box-shadow:0 0 0 4px #fff"></div>'%((18,18,r[8],2) if big else (12,12,r[8],5))
        rail='' if last else '<div style="position:absolute;left:%dpx;top:22px;bottom:-6px;width:2px;background:#e3e9e4"></div>'%(8 if big else 5)
        return ('<div style="position:relative;display:flex;gap:14px;padding:12px 0 16px">%s<div style="width:18px;display:flex;justify-content:center;flex:none">%s</div><div style="flex:1;min-width:0">'
          '<div style="font-size:12.5px;color:var(--mut);font-weight:700">%s %s %s · dans %d jours</div>'
          '<div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start;margin-top:3px"><b style="font-size:%dpx;line-height:1.25">%s</b><span style="color:var(--mut)">⌄</span></div>'
          '<div style="margin-top:6px">%s</div>%s</div></div>')%(rail,dot,r[1],r[2],r[3],r[9],19 if big else 16.5,r[0],pill(r),st3(r,big))
    today=('<div style="position:relative;display:flex;gap:14px;padding:4px 0 8px"><div style="position:absolute;left:8px;top:16px;bottom:-12px;width:2px;background:var(--mintT)"></div><div style="width:18px;display:flex;justify-content:center;flex:none"><div style="width:10px;height:10px;border-radius:50%;background:var(--mintT);margin-top:5px;box-shadow:0 0 0 4px #e4f6ec"></div></div><div style="font-size:14px;font-weight:800;color:var(--mintT)">Aujourd\'hui · 16 oct. 2026</div></div>')
    inner=CSS+'<div class="mini" style="margin:0 4px 8px">Tes courses jusqu\'au jour J. Touche une course pour la modifier.</div><div class="card" style="padding:14px 16px 4px">'+today+node(R[0])+node(R[1])+node(R[2],True)+'</div>'
    inner+='<div style="padding:4px;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div>'
    return sub('Ton objectif',inner,('C','Frise verticale : chaque course sous son point, chiffres alignés'),reco=True,h=1000)
# D : frise horizontale sans texte + liste numérotée
def objD():
    pos=[(0,'#087a49','',10),(149/344*100,'#c9d1cb','1',22),(204/344*100,'#25c37e','2',22),(100,'#10251c','★',26)]
    bar=('<div style="position:relative;height:30px;margin:10px 12px 0"><div style="position:absolute;left:0;right:0;top:14px;height:3px;background:#e3e9e4;border-radius:2px"></div>'
      +''.join('<div style="position:absolute;left:%.1f%%;top:%dpx;transform:translateX(-50%%);width:%dpx;height:%dpx;border-radius:50%%;background:%s;color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #fff">%s</div>'%(p,15-s//2,s,s,c,t) for p,c,t,s in pos)
      +'</div><div style="display:flex;justify-content:space-between;margin:8px 0 0;font-size:12px;color:var(--mut);font-weight:600"><span>auj.</span><span>8 mois</span><span>25 sept.</span></div>')
    def row(r,n,c):
        big=r[7]=='course objectif'
        return ('<div style="display:flex;gap:12px;padding:14px 0;%s"><div style="width:26px;height:26px;border-radius:50%%;background:%s;color:#fff;font-size:12.5px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none">%s</div><div style="flex:1;min-width:0">'
          '<div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:16px;line-height:1.25">%s</b><span style="color:var(--mut)">⌄</span></div><div class="mini" style="margin-top:2px">%s %s %s · %s</div>%s</div></div>')%(LN,c,n,r[0],r[1],r[2],r[3],r[7],st3(r,big))
    inner=CSS+'<div class="card" style="padding:14px 16px 4px"><div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT)">Jusqu\'au jour J · 344 jours</div>'+bar+row(R[0],'1','#c9d1cb')+row(R[1],'2','#25c37e')+row(R[2],'★','#10251c')+'</div>'
    inner+='<div style="padding:4px;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div>'
    return sub('Ton objectif',inner,('D','Frise sans texte (numéros) + liste détaillée dessous'),h=1000)
# E : liste façon Semaine (bloc date à gauche)
def objE():
    def row(r):
        big=r[7]=='course objectif'
        return ('<div style="display:flex;gap:14px;padding:14px 0;%s"><div style="width:52px;flex:none;text-align:center;border-radius:14px;padding:8px 0;background:%s;color:%s"><div style="font-size:20px;font-weight:800;line-height:1">%s</div><div style="font-size:12px;font-weight:700;margin-top:3px">%s</div><div style="font-size:11px;opacity:.7">%s</div></div>'
          '<div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:16px;line-height:1.25">%s</b><span style="color:var(--mut)">⌄</span></div><div style="margin-top:4px">%s</div>%s</div></div>')%(LN,'#10251c' if big else '#f1f4f1','#fff' if big else 'var(--ink)',r[1],r[2],r[3],r[0],pill(r),st3(r))
    inner=CSS+'<div class="card" style="padding:4px 16px">'+row(R[0]).replace(LN,'',1)+row(R[1])+row(R[2])+'</div><div style="padding:4px;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div>'
    return sub('Ton objectif',inner,('E','Liste façon Semaine : date en bloc, chiffres alignés'),h=900)
EXPORT=['objC','objD','objE']
