from base import *
from screens_today import week_strip

def fact3(a):
    return '<div class="stat3">' + ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in a) + '</div>'

def fiche_A():
    sheet = ('<div class="sheet" style="top:34px"><div class="grab"></div><div style="padding:8px 16px 0">'
      '<div class="sb" style="align-items:center"><div class="row"><div class="ic sl">%s</div><div><div class="ttl" style="font-size:20px">Sortie longue</div><div class="meta">Aujourd\'hui · dimanche 18 oct.</div></div></div><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>' % ic('terrain') +
      '<div class="card" style="margin:12px 0 0;padding:13px 16px">' + fact3([('1 h 50', 'durée'), ('≈ 300 m', 'D+ repère'), ('Facile', 'effort')]) + '</div>'
      '<div class="card" style="margin:10px 0 0"><div class="h2">À faire</div>'
      '<div style="font-size:14px;line-height:1.45;margin-top:6px">Tu peux parler tout du long. Montées raides marchées.</div>'
      '<div style="font-size:14px;line-height:1.45;margin-top:6px">D+ : environ 300 m, sans le chercher.</div>'
      '<div style="font-size:14px;line-height:1.45;margin-top:6px">FC : reste en zone facile. Le ressenti décide, la FC confirme.</div></div>'
      '<div class="card" style="margin:10px 0 0"><div class="h2">Pourquoi</div><div style="font-size:14px;line-height:1.45;margin-top:6px">Sortie longue : la seule séance qui progresse cette semaine (+10&nbsp;&#37; au plus sur la plus longue des 30 derniers jours).</div><div class="mini" style="margin-top:6px;font-weight:700">En savoir plus ›</div></div>'
      '<div class="card" style="margin:10px 0 0;padding:12px 16px"><div class="row"><div class="ic nut" style="width:40px;height:40px;border-radius:12px">%s</div><div><div style="font-weight:800;font-size:15px">15 g de glucides par heure</div><div class="mini">≈ 28 g sur la sortie · boisson ≈ 1,5 l</div></div></div></div>' % ic('nutrition') +
      '</div><div class="foot"><div class="links" style="margin:0 0 4px"><a>Pas faite</a><a>Déplacer</a></div><div style="display:grid;grid-template-columns:1fr 2.2fr;gap:8px"><div class="btn sec" style="height:52px">Garmin</div><div class="btn pri">J\'ai fait ma séance</div></div></div></div>')
    body = '<div class="halo"><i class="a"></i><i class="b"></i></div>' + '<div class="dim"></div>' + sheet
    return page(body, 'light', ('A', 'Fiche : à faire, pourquoi, nutrition'), reco=True)

def fiche_B():
    steps = ''.join('<div style="display:grid;grid-template-columns:64px 1fr;gap:10px;padding:9px 0;border-top:%s"><b style="color:var(--ember)">%s</b><span style="font-size:14.5px">%s</span></div>' % ('0' if i == 0 else '1px solid var(--line)', a, b) for i, (a, b) in enumerate([('15 min', 'Échauffement, facile'), ('90 min', 'Endurance, facile'), ('5 min', 'Retour au calme')]))
    sheet = ('<div class="sheet" style="top:34px"><div class="grab"></div><div style="padding:8px 16px 0">'
      '<div class="sb" style="align-items:center"><div class="row"><div class="ic sl">%s</div><div><div class="ttl" style="font-size:20px">Sortie longue</div><div class="meta">dimanche 18 oct.</div></div></div><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>' % ic('terrain') +
      '<div class="card" style="margin:12px 0 0;padding:13px 16px">' + fact3([('110 min', 'durée'), ('300 m', 'D+ repère'), ('Facile', 'effort')]) + '</div>'
      '<div class="card" style="margin:10px 0 0"><div class="h2">Déroulé</div><div style="margin-top:6px">' + steps + '</div></div>'
      '<div class="card" style="margin:10px 0 0"><div class="h2">Pourquoi cette séance</div><div style="font-size:14px;line-height:1.45;margin-top:6px;color:var(--mut)">Sortie longue : la seule séance qui progresse cette semaine (+10&nbsp;&#37; au plus sur la plus longue des 30 derniers jours).</div></div>'
      '<div class="card" style="margin:10px 0 0;padding:12px 16px"><div class="row"><div class="ic nut" style="width:40px;height:40px;border-radius:12px">%s</div><div><div style="font-weight:800;font-size:15px">15 g de glucides par heure</div><div class="mini">≈ 28 g · 1,5 l de boisson</div></div></div></div>' % ic('nutrition') +
      '<div class="card" style="margin:10px 0 0;background:var(--deep);color:#fff"><div class="h2" style="color:#fff">Le conseil</div><div style="font-size:14px;opacity:.88;margin-top:6px">Environ 300 m de D+, sans le chercher. Effort facile…</div></div>'
      '</div></div>')
    body = '<div class="halo"><i class="a"></i><i class="b"></i></div><div class="dim"></div>' + sheet
    return page(body, 'light', ('B', 'Fiche actuelle, corrigée'))

def lrow(dw, d, k, t, m, right='', cls=''):
    col = {'cf': 'background:var(--violetBg);color:var(--violet)', 'sl': 'background:var(--emberBg);color:var(--ember)', 'ef': 'background:var(--mintBg);color:var(--mintT)'}
    icn = {'cf': 'fitness', 'ef': 'run', 'sl': 'terrain'}
    icon = '<div class="small-ic" style="%s">%s</div>' % (col[k], ic(icn[k])) if k else '<div class="small-ic"></div>'
    return '<div class="listrow %s"><div class="dd"><span>%s</span><b>%s</b></div>%s<div style="flex:1;min-width:0"><div class="t">%s</div>%s</div>%s</div>' % (cls, dw, d, icon, t, '<div class="m">%s</div>' % m if m else '', right)

def week_A():
    rows = (lrow('Lun', '12', None, 'Repos', '', '', 'rest')
            + lrow('Mar', '13', 'cf', 'Renforcement', '45 min · effort 5', '<span class="pill ok">Fait</span>')
            + lrow('Mer', '14', 'ef', 'Endurance facile', 'aujourd\'hui · 30 min', '<span class="chev">›</span>', 'today')
            + lrow('Jeu', '15', None, 'Repos', '', '', 'rest')
            + lrow('Ven', '16', 'cf', 'Renforcement', '45 min · séance libre', '<span class="chev">›</span>')
            + lrow('Sam', '17', None, 'Repos', '', '', 'rest')
            + lrow('Dim', '18', 'sl', 'Sortie longue', '1 h 50 · environ 300 m de D+', '<span class="chev">›</span>'))
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            '<header><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">‹</div><div style="text-align:center"><h1 style="font-size:21px">Semaine 4</h1><div class="sub">12 – 18 oct. · Reprise</div></div><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">›</div></header>'
            '<div class="card" style="padding:13px 16px">' + fact3([('1/4', 'séances'), ('0/140', 'min de course'), ('0/300', 'm de D+')]) + '</div>'
            '<div class="card" style="padding:6px 16px">' + rows + '</div>'
            '<div style="margin:4px 14px"><div class="btn ghost" style="font-weight:700">+ Ajouter une séance prévue</div></div>'
            '</div>' + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], 'Semaine'))
    return page(body, 'light', ('A', 'Semaine : les 7 jours sur un écran'), reco=True)

def week_B():
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            '<header><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">‹</div><div style="text-align:center"><h1 style="font-size:21px">Semaine 4</h1><div class="sub">12 – 18 oct. · 1/4 séances</div></div><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">›</div></header>'
            '<div class="card" style="padding:8px 10px">' + week_strip(today_idx=6).replace('class="day today"', 'class="day today"') + '</div>'
            '<div class="card"><div class="row"><div class="ic sl">%s</div><div style="flex:1"><div class="ttl">Sortie longue</div><div class="meta">dimanche 18 oct. · 1 h 50 · ≈ 300 m de D+</div></div></div>'
            '<div class="eff"><b>Facile, tu peux parler.</b> Montées raides marchées.</div>'
            '<div class="why"><span>Pourquoi · </span>Sortie longue : la seule séance qui progresse cette semaine.</div>'
            '<div style="margin-top:14px"><div class="btn sec">Voir la fiche</div></div></div>' % ic('terrain')
            + '</div>' + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], 'Semaine'))
    return page(body, 'light', ('B', 'Semaine : bande de 7 jours + jour choisi'))

def bars(vals, mx, cur=None, band=None, labels=None, h=70):
    b = ''
    if band:
        lo, hi = band
        b = '<div class="band" style="bottom:%.0f%%;height:%.0f%%"></div>' % (lo / mx * 100, (hi - lo) / mx * 100)
    bb = ''.join('<i class="%s" style="height:%.0f%%"></i>' % ('cur' if i == len(vals) - 1 else 'v', max(3, v / mx * 100)) for i, v in enumerate(vals))
    ax = '<div class="axis">' + ''.join('<span>%s</span>' % l for l in labels) + '</div>' if labels else ''
    return '<div class="bars" style="height:%dpx">%s%s</div>%s' % (h, b, bb, ax)

def track(vals, mx, labels):
    cols = ''.join('<div style="flex:1;height:100%%;background:var(--chip);border-radius:6px;display:flex;align-items:flex-end;overflow:hidden"><i style="display:block;width:100%%;height:%.0f%%;background:%s;border-radius:6px"></i></div>' % (v / mx * 100, 'var(--mintT)' if i == len(vals) - 1 else 'var(--mint)') for i, v in enumerate(vals))
    return '<div style="display:flex;gap:6px;height:46px;margin-top:12px">' + cols + '</div><div class="axis">' + ''.join('<span>%s</span>' % l for l in labels) + '</div><div class="mini" style="margin-top:4px">gris : prévu · vert : fait</div>'

def suivi_A():
    lab = ['5/10', '', '19/10', '', '2/11', '', '16/11', '23/11']
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Suivi', 'Semaine 10 · Base · 8 dernières semaines', logo=False)
            + '<div class="card" style="padding:14px 16px"><div class="sb"><div class="h2">Tu suis le plan ?</div><div class="mini">27 séances sur 32</div></div>'
              '<div style="font-size:20px;font-weight:800;margin-top:4px">Oui, 3 sur 4 cette semaine</div>' + track([2, 3, 4, 4, 3, 4, 4, 3], 4, labels=lab) + '</div>'
            + '<div class="card" style="padding:14px 16px"><div class="sb"><div class="h2">Ta sortie longue</div><div class="mini">+10&nbsp;&#37; max par sortie</div></div>'
              '<div style="font-size:20px;font-weight:800;margin-top:4px">2 h 15 <span style="font-size:13px;font-weight:600;color:var(--mut)">dim. 22 nov., ta plus longue</span></div>' + bars([110, 120, 120, 132, 100, 132, 145, 135], 150, labels=lab, h=46) + '</div>'
            + '<div class="card" style="padding:14px 16px"><div class="sb"><div class="h2">Ta charge</div><div class="mini">zone habituelle en vert</div></div>'
              '<div style="font-size:20px;font-weight:800;margin-top:4px">Normale pour toi</div><div class="mini">1 850 cette semaine · habituel : 1 500 à 2 100</div>' + bars([1300, 1500, 1700, 1650, 1200, 1800, 1950, 1850], 2400, band=(1500, 2100), labels=lab, h=46) + '</div>'
            + '</div>' + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], 'Suivi'))
    return page(body, 'light', ('A', 'Suivi : 3 questions (données d\'exemple)'), reco=True)

def suivi_B():
    tiles = ''.join('<div class="card" style="margin:0;padding:13px 14px"><div style="font-size:24px;font-weight:800;letter-spacing:-.02em">%s<small style="font-size:13px;color:var(--mut);margin-left:3px">%s</small></div><div class="mini">%s</div><div style="font-size:12px;font-weight:800;margin-top:4px;color:var(--mut)">%s</div></div>' % t for t in [
        ('0', 'min', 'course', 'prévu : 140'), ('0', 'm', 'D+', 'prévu : 300'), ('390', '', 'charge', 'moyenne des 4 sem. avant : 98'), ('2', '', 'séances', 'sur 4 prévues')])
    sess = ''.join('<div class="listrow"><div style="flex:1"><div class="t">%s</div><div class="m">%s</div></div><div style="text-align:right"><b style="font-size:17px">%s</b><div class="m mini">charge</div></div></div>' % x for x in [
        ('Renforcement', 'mer. 7 oct. · 30 min · effort 5', '150'), ('Renforcement', 'ven. 9 oct. · 30 min · effort 8', '240')])
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            '<header><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">‹</div><div style="text-align:center"><h1 style="font-size:21px">Suivi</h1><div class="sub">Semaine du 5 oct.</div></div><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">›</div></header>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 14px">' + tiles + '</div>'
            '<div class="card"><div class="h2">Séances</div>' + sess + '</div>'
            '<div class="card"><div class="h2">Charge par semaine</div>' + bars([0, 0, 0, 0, 0, 60, 330, 390], 420, labels=['17/8', '', '31/8', '', '14/9', '', '28/9', '5/10'], h=60) + '</div>'
            '</div>' + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], 'Suivi'))
    return page(body, 'light', ('B', 'Suivi actuel, corrigé (tes données du 11 oct.)'))

def alerte():
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Mercredi 14 octobre', 'Semaine 4 · Reprise')
            + '<div class="card" style="box-shadow:inset 0 0 0 2px #f5a623,var(--shadow)"><div class="row" style="gap:8px"><span style="width:9px;height:9px;border-radius:50%;background:#f5a623"></span><div class="h2">Point d\'attention</div></div>'
              '<div style="font-size:14.5px;line-height:1.45;margin-top:8px">Moins de 3 jours de course par semaine jusqu\'à ta phase « Endurance musculaire », où tu passes à 3 jours.</div>'
              '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px"><div class="btn sec" style="height:46px">Modifier mes jours</div><div class="btn pri" style="height:46px;font-size:15px">J\'ai compris</div></div>'
              '<div class="mini" style="margin-top:8px">Elle ne reviendra que si ta situation change.</div></div>'
            + '<div class="card" style="height:200px;opacity:.5"><div class="k">Aujourd\'hui</div><div class="ttl" style="margin-top:10px">Endurance facile</div></div>'
            + '</div>')
    return page(body, 'light', ('A', 'Alerte acquittable, montrée une fois'), reco=True, h=470)

EXPORT = ['fiche_A', 'fiche_B', 'week_A', 'week_B', 'suivi_A', 'suivi_B', 'alerte']
