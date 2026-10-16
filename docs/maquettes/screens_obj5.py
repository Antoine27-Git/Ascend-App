from base import *
from screens_prof2 import sub
from screens_prof6 import LN, fr, pick
R=[('1','#c9d1cb','Trail de la Croix-Rousse','14 mars','23 km · 800 m D+','entraînement','≈ 3 h 20'),
   ('2','#25c37e','Trail des Coursières 2027','8 mai','50 km · 1 900 m D+','objectif','≈ 8 h 15'),
   ('★','#10251c','Objectif Perso 80kms','25 sept.','80 km · 5 000 m D+','course objectif','≈ 16 h 30')]
def frise():
    pos=[(0,'#087a49','',10),(149/344*100,'#c9d1cb','1',22),(204/344*100,'#25c37e','2',22),(100,'#10251c','★',26)]
    return ('<div class="card" style="padding:14px 16px 12px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT)">Jusqu\'au jour J</div><b style="font-size:15px">344 jours</b></div>'
      '<div style="position:relative;height:30px;margin:12px 12px 0"><div style="position:absolute;left:0;right:0;top:14px;height:3px;background:#e3e9e4;border-radius:2px"></div>'
      +''.join('<div style="position:absolute;left:%.1f%%;top:%dpx;transform:translateX(-50%%);width:%dpx;height:%dpx;border-radius:50%%;background:%s;color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #fff">%s</div>'%(p,15-s//2,s,s,c,t) for p,c,t,s in pos)
      +'</div><div style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px;color:var(--mut);font-weight:600"><span>aujourd\'hui</span><span>25 sept. 2027</span></div></div>')
def row(r,open_=False,body=''):
    return ('<div style="%s"><div style="display:flex;gap:12px;align-items:flex-start;padding:13px 0"><div style="width:26px;height:26px;border-radius:50%%;background:%s;color:#fff;font-size:12.5px;font-weight:800;display:flex;align-items:center;justify-content:center;flex:none;margin-top:1px">%s</div>'
      '<div style="flex:1;min-width:0"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font-size:15.5px;line-height:1.3">%s</b><span style="color:var(--mut)">%s</span></div>'
      '<div style="display:flex;justify-content:space-between;gap:8px;margin-top:3px"><span class="mini" style="margin:0">%s · %s</span><b style="font-size:14px;white-space:nowrap">%s</b></div></div></div>%s</div>')%(LN,r[1],r[0],r[2],'⌃' if open_ else '⌄',r[3],r[4],r[6],body)
def objF():
    inner=frise()+'<div class="card" style="padding:0 16px">'+''.join(row(r) for r in R).replace(LN,'',1)+'<div style="padding:14px 0;%s;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div></div>'%LN
    return sub('Ton objectif',inner,('F','Frise numérotée + blocs fins qui se déplient'),reco=True,h=760)
def chart():
    # semaines 0..26 (illustration jusqu'en mars) : estimation et fourchette
    import math
    W,H=290,110;pts=[(0,1030,860,1200),(4,1030,860,1200),(8,1015,870,1170),(12,1000,880,1140),(16,995,885,1120),(21,985,900,1090),(25,990,905,1085)]
    x=lambda w:8+w/25*(W-16); y=lambda v:8+(1220-v)/(1220-840)*(H-16)
    band='M'+' L'.join('%.1f,%.1f'%(x(p[0]),y(p[3])) for p in pts)+' L'+' L'.join('%.1f,%.1f'%(x(p[0]),y(p[2])) for p in reversed(pts))+' Z'
    line='M'+' L'.join('%.1f,%.1f'%(x(p[0]),y(p[1])) for p in pts)
    rc=x(21)
    return ('<svg width="100%%" viewBox="0 0 %d %d" style="display:block;margin-top:8px"><path d="%s" fill="#e4f6ec"/><path d="%s" fill="none" stroke="#087a49" stroke-width="2.5"/>'
      '<line x1="%.1f" x2="%.1f" y1="4" y2="%d" stroke="#c9d1cb" stroke-dasharray="3 3"/><circle cx="%.1f" cy="%.1f" r="4.5" fill="#10251c"/>'
      '<text x="%.1f" y="%d" font-size="10.5" fill="#5b6961" text-anchor="middle">Croix-Rousse</text></svg>'
      '<div style="display:flex;justify-content:space-between;font-size:11.5px;color:var(--mut)"><span>sept.</span><span>déc.</span><span>mars</span></div>')%(W,H+14,band,line,rc,rc,H,x(25),y(990),rc,H+12)
def objF_open():
    est=('<div style="background:#f4f7f4;border-radius:16px;padding:14px;margin:0 0 6px">'
      '<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:10px"><div><div class="mini" style="font-weight:700;margin:0">Durée estimée</div><b style="font-size:28px;letter-spacing:-.02em;white-space:nowrap">≈ 16 h 30</b></div>'
      '<div style="text-align:right"><div class="mini" style="margin:0">fourchette</div><b style="font-size:14px;white-space:nowrap">15 h – 18 h</b></div></div>'
      '<span class="pill ok" style="font-size:12px;margin-top:8px;display:inline-block">− 40 min depuis le départ</span>'
      +chart()+
      '<div class="mini" style="margin-top:8px;line-height:1.45">La fourchette se resserre à chaque course et à chaque sortie longue enregistrée. Elle ne change pas ton plan.</div></div>')
    body='<div style="padding:0 0 4px 38px">'+est+fr('Date','',True).replace('<span style="font-size:16.5px;font-weight:800;padding:4px 2px;"></span>','')+'</div>'
    body=('<div style="padding:0 0 6px">'+est+pick('Date','25 sept. 2027',True)+fr('Distance','80','km')+fr('Dénivelé','5 000','m D+')+'</div>')
    inner=frise()+'<div class="card" style="padding:0 16px">'+row(R[0]).replace(LN,'',1)+row(R[1])+row(R[2],True,body)+'<div style="padding:14px 0;%s;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div></div>'%LN
    return sub('Ton objectif',inner,('F2','Objectif déplié : durée estimée qui évolue (illustration en mars)'),h=1300)
EXPORT=['objF','objF_open']
