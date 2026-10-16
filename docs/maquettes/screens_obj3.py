from base import *
from screens_prof2 import sub
from screens_prof6 import LN
def tile(v,u,l,big=True):
    return ('<div style="flex:1;background:#f4f7f4;border-radius:16px;padding:12px 12px 10px;min-width:0"><div style="font-size:12.5px;color:var(--mut);font-weight:600">%s</div>'
            '<div style="margin-top:4px"><b style="font-size:%dpx;letter-spacing:-.02em">%s</b> <span style="font-size:13px;color:var(--mut);font-weight:600">%s</span></div></div>')%(l,26 if big else 20,v,u)
def namefield(label,v,size=20):
    return '<div style="padding:4px 0 12px"><div style="font-size:12.5px;color:var(--mut);font-weight:600">%s</div><div style="font-size:%dpx;font-weight:800;margin-top:4px;line-height:1.2">%s</div></div>'%(label,size,v)
def datechip(v,j):
    return ('<div style="display:flex;gap:8px;align-items:center;margin:2px 0 12px"><span style="display:inline-flex;align-items:center;gap:6px;background:var(--mintBg);color:var(--mintT);font-weight:800;font-size:14.5px;padding:8px 12px;border-radius:12px">%s %s ⌄</span>'
            '<span style="font-size:13.5px;color:var(--mut);font-weight:600">%s</span></div>')%(ic('calendar'),v,j)
def objA():
    main=('<div class="card" style="padding:18px 16px 16px"><div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT)">Ta course objectif</div>'
      +namefield('','Objectif Perso 80kms',24).replace('<div style="font-size:12.5px;color:var(--mut);font-weight:600"></div>','')
      +datechip('25 sept. 2027','dans 344 jours')
      +'<div style="display:flex;gap:8px">'+tile('80','km','Distance')+tile('5 000','m','Dénivelé +')+'</div>'
      +'<div style="margin-top:8px;display:flex;align-items:center;gap:12px;background:#10251c;color:#fff;border-radius:16px;padding:12px 14px"><div style="flex:1"><div style="font-size:12.5px;color:#9fe3bf;font-weight:700">Durée estimée</div><div class="mini" style="color:#b9d6c7;margin-top:2px">d\'après ton Trail du Beaujolais</div></div><b style="font-size:24px;white-space:nowrap">≈ 16 h 30</b></div></div>')
    def race(name,date,km,dp,dur,prio,col,open_=False):
        return ('<div style="display:flex;gap:12px;padding:14px 0;%s"><div style="width:4px;border-radius:2px;background:%s;flex:none"></div><div style="flex:1;min-width:0">'
          '<div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start"><b style="font-size:16.5px;line-height:1.25">%s</b><span style="color:var(--mut)">⌄</span></div>'
          '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px"><span class="pill %s" style="font-size:12px">%s</span><span class="chipx">%s</span><span class="chipx">%s km</span><span class="chipx">%s m D+</span><span class="chipx">≈ %s</span></div></div></div>')%(LN,col,name,'ok' if prio=='objectif' else '',prio,date,km,dp,dur)
    css='<style>.chipx{font-size:12.5px;font-weight:700;background:#f1f4f1;border-radius:999px;padding:4px 10px;color:#3d4a43}</style>'
    inter=('<div style="font-size:20px;font-weight:800;margin:24px 4px 2px">Tes courses intermédiaires</div><div class="mini" style="margin:0 4px 8px">Facultatif. Elles s\'intègrent au plan selon leur statut.</div>'
      +'<div class="card" style="padding:2px 16px 4px">'+race('Trail des Coursières 2027','8 mai','50','1 900','8 h 15','objectif','#25c37e').replace(LN,'',1)
      +race('Trail de la Croix-Rousse','14 mars','23','800','3 h 20','entraînement','#c9d1cb')
      +'<div style="padding:14px 0;%s;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div></div>'%LN)
    return sub('Ton objectif',css+main+inter,('A','Fiche course : titre, date, chiffres en tuiles, durée estimée'),reco=True,h=1240)
def objB():
    tl=('<div class="card" style="padding:16px"><div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT)">Ta route jusqu\'au jour J</div>'
      '<div style="position:relative;margin:18px 6px 4px;height:70px"><div style="position:absolute;left:0;right:0;top:9px;height:3px;background:#e3e9e4;border-radius:2px"></div>'
      '<div style="position:absolute;left:0;width:6%;top:9px;height:3px;background:var(--mintT)"></div>'
      +''.join('<div style="position:absolute;left:%s;top:0;transform:translateX(-50%%);text-align:center;width:90px"><div style="width:%dpx;height:%dpx;border-radius:50%%;margin:%dpx auto 0;background:%s;box-shadow:0 0 0 3px #fff"></div><div style="font-size:12px;font-weight:800;margin-top:6px">%s</div><div style="font-size:11.5px;color:var(--mut)">%s</div></div>'%(l,s,s,(20-s)//2,c,t,d) for l,s,c,t,d in [('0%',12,'var(--mintT)','Aujourd\'hui','16 oct.'),('40%',12,'#c9d1cb','','14 mars'),('60%',14,'#25c37e','Coursières','8 mai'),('100%',20,'#10251c','Objectif','25 sept.')])
      +'</div></div>')
    def rc(t,name,date,km,dp,dur,big=False):
        return ('<div class="card" style="padding:16px"><div style="display:flex;justify-content:space-between"><div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:%s">%s</div><span style="color:var(--mut)">Modifier</span></div>'
          '<div style="font-size:%dpx;font-weight:800;margin-top:6px">%s</div><div style="font-size:14px;color:var(--mut);margin-top:2px">%s</div>'
          '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px">%s</div></div>')%('var(--mintT)' if big else '#8a5a0a',t,22 if big else 18,name,date,
          ''.join('<div><b style="font-size:%dpx;white-space:nowrap">%s</b><div class="mini">%s</div></div>'%(22 if big else 18,v,l) for v,l in [(km,'km'),(dp,'m D+'),(dur,'estimée')]))
    inner=tl+rc('Course objectif','Objectif Perso 80kms','samedi 25 septembre 2027 · dans 344 jours','80','5 000','≈ 16 h 30',True)+rc('Intermédiaire · objectif','Trail des Coursières 2027','samedi 8 mai 2027','50','1 900','≈ 8 h 15')
    inner+='<div style="padding:4px 4px;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div>'
    return sub('Ton objectif',inner,('B','Frise des courses + une carte par course (Modifier ouvre l\'édition)'),h=1100)
EXPORT=['objA','objB']
