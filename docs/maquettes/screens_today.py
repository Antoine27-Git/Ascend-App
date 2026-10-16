from base import *

def week_strip(today_idx=2, done=(1,)):
    days = [('L', '12', None), ('M', '13', 'cf'), ('M', '14', 'ef'), ('J', '15', None), ('V', '16', 'cf'), ('S', '17', None), ('D', '18', 'sl')]
    icons = {'cf': 'fitness', 'ef': 'run', 'sl': 'terrain'}
    out = []
    for i, (l, d, k) in enumerate(days):
        if k:
            cls = 'dot done' if i in done else 'dot ' + k
            dot = '<div class="%s">%s</div>' % (cls, ic(icons[k]))
        else:
            dot = '<div class="dot rest">·</div>'
        out.append('<div class="day%s">%s<span class="d">%s</span>%s</div>' % (' today' if i == today_idx else '', l, d, dot))
    return '<div class="week">' + ''.join(out) + '</div>'

TODAY_CARD = (
    '<div class="card" style="padding-bottom:8px">'
    '<div class="k">Aujourd\'hui</div>'
    '<div class="row" style="margin-top:10px"><div class="ic ef">%s</div><div><div class="ttl">Endurance facile</div><div class="meta">30 min · moins de 50 m de D+</div></div></div>'
    '<div class="eff"><b>Facile, tu peux parler.</b> Si ça monte, marche.<br><span class="mut">+ 4 × 15 s d\'accélérations à la fin</span></div>'
    '<div class="why"><span>Pourquoi · </span>Endurance facile : elle construit le volume sans fatigue.</div>'
    '<div style="margin-top:14px"><div class="btn pri">J\'ai fait ma séance</div></div>'
    '<div class="links"><a>Détail</a><a>Pas faite</a></div>'
    '</div>') % ic('run')

def today_A(theme='light'):
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Mercredi 14 octobre', 'Semaine 4 · Reprise')
            + TODAY_CARD
            + '<div class="card"><div class="sb"><div class="h2">Cette semaine</div><div class="mini"><b style="color:var(--ink)">1/4</b> séances · <b style="color:var(--ink)">0/140</b> min</div></div>'
            + week_strip() + '</div>'
            + '<div class="card objline" style="padding:10px 14px"><div class="ic" style="width:40px;height:40px;border-radius:12px;background:var(--deep);color:#e9c46a">%s</div><div style="flex:1;min-width:0"><div style="font-weight:800;font-size:14.5px">Objectif Perso 80kms · J−346</div><div class="mini">Jalon : Trail des coursières · J−206</div></div></div>' % ic('terrain')
            + '</div>' + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], "Aujourd'hui"))
    return page(body, theme, ('A', "Aujourd'hui : Accueil + Jour, 4 onglets"), reco=True)

def today_B():
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Mercredi 14 octobre', 'Semaine 4 · Reprise · J−346')
            + TODAY_CARD
            + '<div class="card" style="padding:12px 16px;display:flex;align-items:center;gap:10px;background:var(--sunBg);box-shadow:none"><span style="width:9px;height:9px;border-radius:50%;background:#f5a623;flex:none"></span><div style="flex:1;font-size:13.5px;line-height:1.35"><b>Point d\'attention</b> · 2 jours de course jusqu\'au 28 mars</div><span class="chev">›</span></div>'
            + '<div class="card" style="padding:14px 16px"><div class="stat3"><div><b>1/4</b><span>séances</span></div><div><b>0/140</b><span>min de course</span></div><div><b>0/300</b><span>m de D+</span></div></div></div>'
            + '</div>' + nav(['Accueil', 'Jour', 'Séances', 'Suivi', 'Profil'], 'Accueil'))
    return page(body, 'light', ('B', 'Accueil réordonné, 5 onglets gardés'))

def today_C():
    rows = [
        ('Lun', '12', None, 'Repos', '', ''),
        ('Mar', '13', 'cf', 'Renforcement', '45 min · effort 5', '<span class="pill ok">Fait</span>'),
    ]
    def r(dw, d, k, t, m, right, cls=''):
        icn = {'cf': 'fitness', 'ef': 'run', 'sl': 'terrain'}
        icon = '<div class="small-ic %s" style="%s">%s</div>' % ('', {'cf': 'background:var(--violetBg);color:var(--violet)', 'sl': 'background:var(--emberBg);color:var(--ember)', 'ef': 'background:var(--mintBg);color:var(--mintT)'}.get(k, ''), ic(icn[k]) if k else '') if k else '<div class="small-ic"></div>'
        return '<div class="listrow %s"><div class="dd"><span>%s</span><b>%s</b></div>%s<div style="flex:1;min-width:0"><div class="t">%s</div><div class="m">%s</div></div>%s</div>' % (cls, dw, d, icon, t, m, right)
    top = r('Lun', '12', None, 'Repos', '', '', 'rest') + r('Mar', '13', 'cf', 'Renforcement', '45 min · effort 5', '<span class="pill ok">Fait</span>')
    today = ('<div style="margin:6px -6px;padding:12px;border-radius:18px;background:var(--mintBg);box-shadow:inset 0 0 0 1.5px var(--mintT)">'
             '<div class="row"><div class="dd" style="width:40px;text-align:center"><span class="mini" style="font-weight:700">Mer</span><b style="display:block;font-size:17px">14</b></div><div style="flex:1"><div class="t" style="font-size:17px;font-weight:800">Endurance facile</div><div class="m mini">30 min · moins de 50 m de D+</div></div></div>'
             '<div class="mini" style="margin:8px 0 10px 52px;color:var(--ink)">Facile, tu peux parler. + 4 × 15 s d\'accélérations.</div>'
             '<div class="btn pri" style="height:48px">J\'ai fait ma séance</div></div>')
    bottom = (r('Jeu', '15', None, 'Repos', '', '', 'rest') + r('Ven', '16', 'cf', 'Renforcement', '45 min · séance libre', '')
              + r('Sam', '17', None, 'Repos', '', '', 'rest') + r('Dim', '18', 'sl', 'Sortie longue', '1 h 50 · environ 300 m de D+', ''))
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Semaine 4', '12 – 18 oct. · Reprise · 1/4 séances')
            + '<div class="card" style="padding:8px 14px">' + top + today + bottom + '</div>'
            + '</div>' + nav(['Plan', 'Suivi', 'Profil'], 'Plan'))
    return page(body, 'light', ('C', 'Semaine en agenda, aujourd\'hui déplié, 3 onglets'))

def today_A_dark():
    return today_A('dark').replace('<b>A</b>Aujourd\'hui : Accueil + Jour, 4 onglets<span class="reco">recommandée</span>', '<b>A</b>Même écran en mode sombre')
EXPORT = ['today_A', 'today_B', 'today_C', 'today_A_dark']
