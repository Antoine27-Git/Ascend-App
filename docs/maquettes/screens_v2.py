from base import *
NAV = ["Aujourd'hui", 'Semaine', 'Suivi', 'Profil']
def fact3(a):
    return '<div class="stat3">' + ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in a) + '</div>'
def head(title, sub, icon='terrain', cls='sl'):
    return ('<div class="sb" style="align-items:center"><div class="chip" style="width:40px;height:40px;font-size:20px">×</div>'
            '<div class="chip" style="width:40px;height:40px;font-size:22px;letter-spacing:1px">···</div></div>'
            '<div class="row" style="margin-top:10px"><div class="ic %s">%s</div><div><div class="ttl" style="font-size:21px">%s</div><div class="meta">%s</div></div></div>') % (cls, ic(icon), title, sub)
def bar(segs):
    tot = sum(m for m, _, _ in segs)
    b = ''.join('<div style="flex:%s;background:%s;border-radius:6px;min-width:8px"></div>' % (m, c) for m, c, _ in segs)
    leg = ''.join('<div style="display:flex;align-items:center;gap:8px;font-size:14px;padding:3px 0"><i style="width:10px;height:10px;border-radius:50%%;background:%s;flex:none"></i><b style="width:58px">%s</b><span style="color:var(--mut)">%s</span></div>' % (c, l, n) for (m, c, n), l in zip(segs, [x[2] for x in segs]) for _ in [0]) if False else ''
    return '<div style="display:flex;gap:3px;height:12px;margin:12px 0 10px">%s</div>' % b
def legend(rows):
    return ''.join('<div style="display:flex;align-items:center;gap:10px;font-size:14px;padding:4px 0"><i style="width:10px;height:10px;border-radius:50%%;background:%s;flex:none"></i><b style="min-width:62px">%s</b><span style="color:var(--mut)">%s</span></div>' % r for r in rows)
def line(icon, txt):
    return '<div style="display:flex;gap:10px;align-items:flex-start;margin-top:10px"><div class="small-ic" style="width:28px;height:28px;border-radius:9px;background:var(--mintBg);color:var(--mintT);flex:none">%s</div><div style="font-size:14px;line-height:1.4;padding-top:3px">%s</div></div>' % (ic(icon), txt)
def sheet(inner, foot):
    return '<div class="halo"><i class="a"></i><i class="b"></i></div><div class="dim"></div><div class="sheet" style="top:34px"><div class="grab"></div><div style="padding:8px 16px 0;height:690px;overflow:hidden">%s</div>%s</div>' % (inner, foot)
FOOT = '<div class="foot"><div style="display:grid;grid-template-columns:1fr 2.2fr;gap:8px"><div class="btn sec" style="height:52px">Ma montre</div><div class="btn pri">J\'ai fait ma séance</div></div></div>'
SEG = [(15, '#f3c9a6', ''), (90, '#ff7a3d', ''), (5, '#f3c9a6', '')]
NUT_ON = ('<div class="card" style="margin:10px 0 0;padding:12px 16px"><div class="row"><div class="ic nut" style="width:40px;height:40px;border-radius:12px">%s</div><div style="flex:1"><div style="font-weight:800;font-size:15px">35 g de glucides par heure</div><div class="mini">≈ 64 g sur la séance · boisson ≈ 1,1 l</div></div></div>'
          '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding-top:10px;border-top:1px solid var(--line)"><span class="mini">Pas de suivi sur cette séance ?</span><span style="font-weight:700;font-size:13.5px;color:var(--mut)">Non suivie</span></div></div>') % ic('nutrition')
NUT_OFF = ('<div class="card" style="margin:10px 0 0;padding:12px 16px;background:transparent;box-shadow:none;border:1px dashed var(--line)"><div class="row"><div class="ic" style="width:40px;height:40px;border-radius:12px;background:var(--chip);color:var(--mut)">%s</div><div style="flex:1"><div style="font-weight:700;font-size:15px;color:var(--mut)">Nutrition non suivie</div><div class="mini">Cette sortie ne compte pas dans la progression de ta cible.</div></div><span style="font-weight:700;font-size:13.5px;color:var(--mintT)">Remettre</span></div></div>') % ic('nutrition')

def fiche2_A():
    inner = (head('Sortie longue', 'Aujourd\'hui · dimanche 18 oct.')
      + '<div class="card" style="margin:12px 0 0;padding:13px 16px">' + fact3([('1 h 50', 'durée'), ('200–300', 'm de D+'), ('Facile', 'effort')]) + '</div>'
      + '<div class="card" style="margin:10px 0 0"><div class="h2">À faire</div>' + bar(SEG)
      + legend([('#f3c9a6', '15 min', 'Échauffement'), ('#ff7a3d', '1 h 30', 'Endurance, tu peux parler'), ('#f3c9a6', '5 min', 'Retour au calme')])
      + line('terrain', 'Environ 200 à 300 m de D+, sans le chercher. Montées raides marchées.')
      + line('monitoring', 'FC : zone facile. Le ressenti décide, la FC confirme.') + '</div>'
      + '<div class="card" style="margin:10px 0 0;padding:13px 16px"><div class="h2">Pourquoi</div><div style="font-size:14px;line-height:1.4;margin-top:4px;color:var(--mut)">La seule séance qui progresse cette semaine (+10 % au plus sur ta plus longue des 30 derniers jours).</div></div>'
      + NUT_ON)
    return page(sheet(inner, FOOT), 'light', ('A', 'Fiche : barre de déroulé, barre d\'action fixe'), reco=True)

def fiche2_B():
    inner = (head('Sortie longue', 'Aujourd\'hui · dimanche 18 oct.')
      + '<div style="margin:14px 2px 0;display:flex;gap:18px"><div><b style="font-size:22px">1 h 50</b><div class="mini">durée</div></div><div><b style="font-size:22px">200–300 m</b><div class="mini">de D+</div></div><div><b style="font-size:22px">Facile</b><div class="mini">effort</div></div></div>'
      + '<div style="margin:16px 2px 0"><div class="h2">À faire</div><div style="font-size:15px;line-height:1.5;margin-top:6px">15 min d\'échauffement, <b>1 h 30 d\'endurance</b>, 5 min de retour au calme.</div>'
      + '<div style="font-size:14px;line-height:1.45;margin-top:8px;color:var(--mut)">Tu peux parler tout du long. Montées raides marchées. D+ sans le chercher.<br>FC : zone facile, le ressenti décide.</div></div>'
      + '<div style="margin:16px 2px 0"><div class="h2">Pourquoi</div><div style="font-size:14px;line-height:1.45;margin-top:4px;color:var(--mut)">La seule séance qui progresse cette semaine (+10 % au plus).</div></div>'
      + NUT_OFF)
    return page(sheet(inner, FOOT), 'light', ('B', 'Fiche : texte sobre, sans cartes ; nutrition non suivie'))

def nut_states():
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><h1 style="font-size:21px">Nutrition, 2 états</h1><div class="sub">Module activé, séance par séance</div></div></header>'
        + '<div class="mini" style="margin:6px 4px 0;font-weight:700">Suivie (par défaut)</div>' + NUT_ON
        + '<div class="mini" style="margin:18px 4px 0;font-weight:700">Non suivie sur cette séance</div>' + NUT_OFF
        + '<div class="mini" style="margin:18px 4px 0;line-height:1.45">Dans la saisie, « Non suivi » est déjà présélectionné pour cette séance, et ses glucides ne comptent pas dans la progression de la cible. Le module reste activé pour les autres séances.</div>'
        + '</div>' + nav(NAV, "Aujourd'hui"))
    return page(body, 'light', ('N', 'Nutrition non suivie sur une séance'))

def lrow(dw, d, k, t, m, right='', cls=''):
    col = {'cf': 'background:var(--violetBg);color:var(--violet)', 'sl': 'background:var(--emberBg);color:var(--ember)', 'ef': 'background:var(--mintBg);color:var(--mintT)'}
    icn = {'cf': 'fitness', 'ef': 'run', 'sl': 'terrain'}
    icon = '<div class="small-ic" style="%s">%s</div>' % (col[k], ic(icn[k])) if k else '<div class="small-ic"></div>'
    return '<div class="listrow %s" style="%s"><div class="dd"><span>%s</span><b>%s</b></div>%s<div style="flex:1;min-width:0"><div class="t">%s</div>%s</div>%s</div>' % (cls, 'padding-top:9px;padding-bottom:9px' if not k else '', dw, d, icon, t, '<div class="m">%s</div>' % m if m else '', right)
def semaine2():
    rows = (lrow('Lun', '12', 'cf', 'Renforcement', '45 min · effort 5', '<span class="pill ok">Fait</span>')
            + lrow('Mar', '13', 'ef', 'Endurance', '38 min', '<span class="pill miss">Manquée</span>')
            + lrow('Mer', '14', None, 'Repos', '', '', 'rest')
            + lrow('Jeu', '15', 'ef', 'Endurance', 'aujourd\'hui · 38 min', '<span class="chev">›</span>', 'today')
            + lrow('Ven', '16', None, 'Repos', '', '', 'rest')
            + lrow('Sam', '17', None, 'Repos', '', '', 'rest')
            + lrow('Dim', '18', 'sl', 'Sortie longue', '1 h 50 · 200 à 300 m de D+', '<span class="chev">›</span>'))
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">‹</div><div style="text-align:center"><h1 style="font-size:21px">Semaine 3</h1><div class="sub">12 – 18 oct. · Reprise</div></div><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">›</div></header>'
        + '<div class="card" style="padding:13px 16px">' + fact3([('1/5', 'séances'), ('0/186', 'min de course'), ('0/250', 'm de D+')]) + '</div>'
        + '<div class="card" style="padding:6px 14px">' + rows + '</div>'
        + '<div class="mini" style="text-align:center;font-weight:700;margin-top:8px">+ Ajouter une séance prévue</div>'
        + '</div>' + nav(NAV, 'Semaine'))
    return page(body, 'light', ('S', 'Semaine : titre centré, repos compacts'))
EXPORT = ['fiche2_A', 'fiche2_B', 'nut_states', 'semaine2']
