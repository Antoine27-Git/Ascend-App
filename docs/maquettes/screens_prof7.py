from base import *
from screens_prof2 import sub
from screens_prof6 import fr, pick, seg, LN
PH=[('Reprise',8,'21 sept.','15 nov.'),('Base',19,'16 nov.','28 mars'),('Endurance musculaire',8,'29 mars','23 mai'),('Intensité en côte',6,'24 mai','4 juil.'),('Bloc spécifique',6,'5 juil.','15 août'),('Pic',3,'16 août','5 sept.'),('Affûtage',3,'6 sept.','26 sept.')]
PCOL=['#7fd8a8','#3cbf7f','#1f9d63','#e9a23b','#e07a3a','#c9542e','#8a6cf0']
def hero():
    tot=sum(p[1] for p in PH)
    bar=''.join('<div style="flex:%d;height:8px;background:%s;opacity:%s"></div>'%(p[1],PCOL[i],'1' if i==0 else '.35') for i,p in enumerate(PH))
    pos=3.5/tot*100
    return ('<div class="card" style="padding:18px 18px 16px;background:linear-gradient(150deg,#10251c,#1d4a36);color:#fff">'
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px"><div><div style="font-size:11.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#9fe3bf">Ton objectif · 25 sept. 2027</div>'
      '<div style="font-size:22px;font-weight:800;margin-top:6px;line-height:1.15">Objectif Perso 80kms</div></div>'
      '<div style="text-align:right;flex:none"><div style="font-size:34px;font-weight:800;line-height:1">344</div><div style="font-size:12px;color:#b9d6c7">jours</div></div></div>'
      '<div style="display:flex;gap:8px;margin-top:12px"><span style="background:rgba(255,255,255,.12);border-radius:999px;padding:6px 12px;font-size:13px;font-weight:700">80 km</span><span style="background:rgba(255,255,255,.12);border-radius:999px;padding:6px 12px;font-size:13px;font-weight:700">5 000 m D+</span><span style="background:rgba(255,255,255,.12);border-radius:999px;padding:6px 12px;font-size:13px;font-weight:700">jalon 8 mai</span></div>'
      '<div style="position:relative;margin-top:18px"><div style="display:flex;gap:3px;border-radius:6px;overflow:hidden">%s</div>'
      '<div style="position:absolute;left:%.1f%%;top:-5px;width:4px;height:18px;border-radius:2px;background:#fff;box-shadow:0 0 0 2px #10251c"></div></div>'
      '<div style="display:flex;justify-content:space-between;margin-top:8px;font-size:12.5px;color:#b9d6c7"><span><b style="color:#fff">Reprise</b> · semaine 4 sur 53</span><span>Affûtage</span></div></div>')%(bar,pos)
def lrow(icn,t,s):
    return ('<div style="display:flex;align-items:center;gap:14px;padding:13px 0;%s"><div style="width:42px;height:42px;border-radius:13px;background:var(--mintBg);display:flex;align-items:center;justify-content:center;color:var(--mintT);flex:none">%s</div>'
            '<div style="flex:1"><b style="font-size:16px">%s</b><div style="font-size:13.5px;color:var(--mut);margin-top:2px">%s</div></div><span style="color:var(--mut)">›</span></div>')%(LN if icn!='terrain' else '',ic(icn),t,s)
def home_v3():
    body=('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll"><header><div><h1>Ton profil</h1><div class="sub">Tes réglages construisent ton plan</div></div></header>'+hero()
      +'<div class="card" style="padding:4px 18px">'+lrow('terrain','Ton objectif','Ta course et tes courses intermédiaires')+lrow('calendar','Ta semaine','Tes jours de course et les phases du plan')
      +lrow('person','Toi','Historique, courses passées, terrain, poids')+lrow('fitness','Tes modules','Renforcement, nutrition, blessure, journal')+lrow('run','Ton matériel','Ta montre et tes chaussures')
      +lrow('monitoring','Données et synchro','Sauvegarde, export, import')+lrow('person','Réglages avancés','Redémarrer le plan, tout effacer')+'</div></div>'+nav(['Aujourd\'hui','Semaine','Suivi','Profil'],'Profil'))
    return page(body,'light',('1','Accueil : objectif visuel, sous-titres = à quoi sert la rubrique'),h=1160)
def card(title,note,body):
    return '<div class="card" style="padding:16px 16px 6px"><div class="h2">%s</div>%s%s</div>'%(title,'<div class="mini" style="margin:4px 0 8px;line-height:1.45">%s</div>'%note if note else '',body)
def objectif_v2():
    pill=lambda t,c='ok':'<span class="pill %s" style="font-size:11.5px;margin-left:8px">%s</span>'%(c,t)
    inter=('<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 0;%s"><div><div style="font-weight:800;font-size:15.5px">Trail des Coursières 2027%s</div><div class="mini" style="margin-top:2px">8 mai 2027 · 50 km · 2 500 m D+</div></div><span style="color:var(--mut);font-size:18px">⌃</span></div>'%(LN,pill('objectif'))
       +seg('Statut',['Objectif','Entraînement'],'Objectif')+'<div class="mini" style="padding:0 0 10px">L\'appli allège les jours d\'avant et te laisse récupérer après.</div>'
       +fr('Nom','Trail des Coursières 2027')+pick('Date','8 mai 2027')+fr('Distance','50','km')+fr('Dénivelé','2 500','m D+')
       +'<div style="padding:10px 0 14px;font-size:13.5px;font-weight:700;color:#b3261e">Supprimer cette course</div>'
       +'<div style="padding:14px 0;%s;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course intermédiaire</div>'%LN)
    inner=(card('Ta course objectif','Le plan se construit à rebours depuis cette date.',fr('Nom','Objectif Perso 80kms','',True)+pick('Date','25 sept. 2027')+fr('Distance','80','km')+fr('Dénivelé','5 000','m D+'))
      +card('Courses intermédiaires','Facultatif. Elles s\'intègrent au plan selon leur statut.',inter)
      +'<div class="mini" style="text-align:center;margin:4px 6px">Changer une date, une distance ou un D+ modifie le plan : l\'appli te montre ce qui change avant d\'enregistrer.</div>')
    return sub('Ton objectif',inner,('2','Ton objectif : même style que Toi'),h=1250)
def objectif_confirm():
    sheet=('<div style="position:absolute;inset:0;background:rgba(0,0,0,.35);z-index:20"></div><div style="position:absolute;left:0;right:0;bottom:0;z-index:21;background:#f6f7f4;border-radius:24px 24px 0 0;padding:20px">'
      '<b style="font-size:18px">Ce que ça change</b><div class="mini" style="margin-top:4px">Date de ta course : 25 sept. → 2 oct. 2027. Sur les 14 prochains jours :</div>'
      '<div style="margin-top:10px;font-size:14.5px;line-height:1.7">~ dim. 18 oct. · Sortie longue 110 → 115 min<br>~ dim. 25 oct. · Sortie longue 115 → 120 min</div>'
      '<div style="display:flex;gap:10px;margin-top:16px"><div class="btn sec" style="flex:1;height:48px;font-size:15px">Annuler</div><div class="btn" style="flex:1;height:48px;font-size:15px;background:var(--accent);color:var(--accentInk)">Confirmer</div></div></div>')
    inner=card('Ta course objectif','Le plan se construit à rebours depuis cette date.',fr('Nom','Objectif Perso 80kms','',True)+pick('Date','2 oct. 2027')+fr('Distance','80','km')+fr('Dénivelé','5 000','m D+'))
    return sub('Ton objectif',inner,('2b','Après un changement qui touche le plan'),h=760).replace('<nav>',sheet+'<nav>',1)
D=['L','M','M','J','V','S','D']
def sq(on,kind):
    st={'run':'background:var(--mintBg);color:var(--mintT);box-shadow:inset 0 0 0 1.5px var(--mintT)','long':'background:var(--mintT);color:#fff','cf':'background:var(--violetBg);color:var(--violet);box-shadow:inset 0 0 0 1.5px var(--violet)'}[kind]
    return '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin-top:6px">'+''.join('<div style="height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;%s">%s</div>'%(st if i in on else 'color:#aab3ad;box-shadow:inset 0 0 0 1px #e3e9e4',d) for i,d in enumerate(D))+'</div>'
def drows():
    return ''.join('<div style="padding:8px 0 2px"><div style="font-size:13.5px;color:var(--mut)">%s</div>%s</div>'%(l,sq(o,k)) for l,o,k in [('Jours de course',[2,6],'run'),('Sortie longue',[6],'long'),('Renforcement',[1,4],'cf')])
def semaine_v4():
    typ=card('Ta semaine type','Elle vaut pour toute la préparation, sauf pour une phase qui a ses propres jours.',drows()+'<div class="btn sec" style="height:46px;margin:14px 0 10px;font-size:14.5px">Modifier mes jours</div>')
    def ph(i,open_=False):
        n,w,a,b=PH[i];cur=i==0
        dot='<div style="width:14px;height:14px;border-radius:50%%;flex:none;margin-top:4px;%s"></div>'%('background:#f5a623;box-shadow:0 0 0 4px #fdf0d5' if cur else 'background:#fff;box-shadow:inset 0 0 0 2px %s'%PCOL[i])
        badge='<span class="pill" style="font-size:11.5px;margin-left:6px;background:#fdf0d5;color:#8a5a0a">en cours</span>' if cur else ('<span class="pill ok" style="font-size:11.5px;margin-left:6px">jours propres</span>' if i==2 else '')
        rail='' if i==len(PH)-1 else '<div style="position:absolute;left:6px;top:24px;bottom:-14px;width:2px;background:#e3e9e4"></div>'
        body=''
        if open_: body=('<div style="padding:4px 0 6px 26px"><div style="font-size:15px;line-height:1.5">Réhabituer le corps : endurance facile, quelques accélérations, force générale légère.</div>'
                         +drows()+'<div class="mini" style="margin-top:8px">Mêmes jours que ta semaine type.</div><div class="btn sec" style="height:44px;margin-top:12px;font-size:14px">Modifier les jours de cette phase</div></div>')
        return ('<div style="position:relative;padding:12px 0">%s<div style="display:flex;gap:12px;align-items:flex-start">%s<div style="flex:1"><div style="font-weight:800;font-size:15.5px">%s%s</div><div class="mini" style="margin-top:2px">du %s au %s · %d sem.</div></div><span style="color:var(--mut)">%s</span></div>%s</div>')%(rail,dot,n,badge,a,b,w,'⌃' if open_ else '⌄',body)
    phases='<div style="font-size:20px;font-weight:800;margin:22px 4px 2px">Tes phases</div><div class="mini" style="margin:0 4px 8px">7 phases jusqu\'à ta course. Touche une phase pour voir ce qu\'elle travaille.</div><div class="card" style="padding:6px 16px">'+''.join(ph(i,i==0) for i in range(7))+'</div>'
    return sub('Ta semaine',typ+phases,('3','Ta semaine : un seul bouton, phases en frise'),h=1700)
def bilan_v2():
    tile=lambda v,l:'<div style="flex:1;background:#fff;border-radius:16px;padding:12px"><div style="font-size:20px;font-weight:800">%s</div><div class="mini" style="margin-top:2px">%s</div></div>'%(v,l)
    sheet=('<div style="position:absolute;inset:0;background:rgba(0,0,0,.35);z-index:20"></div><div style="position:absolute;left:0;right:0;bottom:0;z-index:21;background:#f6f7f4;border-radius:24px 24px 0 0;padding:20px">'
      '<div style="font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT)">Dans 12 jours</div><b style="font-size:20px;display:block;margin-top:4px">Base commence le lundi 16 nov.</b>'
      '<div style="font-size:14.5px;line-height:1.5;margin-top:8px">Volume facile et force maximale. Ta sortie longue passera de 1 h 10 à 4 h 24 sur la phase.</div>'
      '<div class="mini" style="margin:14px 0 6px;font-weight:700">Ta phase Reprise</div><div style="display:flex;gap:8px">'+tile('1 / 3','sorties faites')+tile('30 min','sortie longue, sur 1 h 50')+'</div>'
      '<div class="mini" style="margin:14px 0 2px;font-weight:700">Tes jours pour Base</div>'+drows()
      +'<div style="display:flex;gap:10px;margin-top:16px"><div class="btn sec" style="flex:1;height:48px;font-size:15px">Modifier</div><div class="btn" style="flex:1;height:48px;font-size:15px;background:var(--accent);color:var(--accentInk)">Garder ces jours</div></div></div>')
    return sub('Ta semaine','',('4','Bilan : seulement les 2 dernières semaines de la phase'),h=860).replace('<nav>',sheet+'<nav>',1)
EXPORT=['home_v3','objectif_v2','objectif_confirm','semaine_v4','bilan_v2']
