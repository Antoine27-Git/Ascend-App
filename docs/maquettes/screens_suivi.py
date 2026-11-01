"""Suivi en 3 questions : maquettes (17/10/2026), à valider avant tout code.

Produit :
  - suivi.html            page de comparaison (4 variantes, comparatif, recommandation), lisible sur téléphone
  - suivi/*.png           une image par variante et par état (360 px, pour relire depuis GitHub)
Lancer : cd docs/maquettes && python3 screens_suivi.py

Données (lecture retenue, à corriger si besoin) :
  - profil d'Antoine reconstitué depuis ses captures (tests/ui/state.py) : plan démarré le 21/09/2026,
    course mer. + dim. (sortie longue), renforcement mar. + ven., objectif 25/09/2027 (80 km, 4 500 m D+) ;
  - séances réelles jusqu'au 11/10 (captures) ; semaine du 12/10 SUPPOSÉE faite comme prévue
    (renforcement mar. 30 min effort 5, endurance mer. 30 min effort 3, renforcement ven. 30 min effort 6) ;
  - horloge figée au samedi 17/10/2026, 9 h ; plan calculé par le moteur actuel (règles v2) sur ces données.
Ces maquettes ne touchent ni au moteur ni à index.html.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from base import ic

# ---------------------------------------------------------------- données
# Séances dues / faites, semaine par semaine (c = course, r = renforcement)
# statut : f = faite, m = manquée, v = à venir
WEEKS = [
    dict(n=4, mon='12 oct.', cur=True, charge=420, course=90,
         sess=[('mar. 13', 'r', 'Renforcement', 'f', 'fait · effort 5'),
               ('mer. 14', 'c', 'Endurance', 'f', '30 min · effort 3'),
               ('ven. 16', 'r', 'Renforcement', 'f', 'fait · effort 6'),
               ('dim. 18', 'c', 'Sortie longue', 'v', 'prévue · 1 h 49')],
         sl=('1 h 49', 'prévue dim.')),
    dict(n=3, mon='5 oct.', charge=390, course=0,
         sess=[('mar. 6', 'r', 'Renforcement', 'f', 'fait mer. 7 · effort 5'),
               ('mer. 7', 'c', 'Endurance', 'm', 'manquée · « autre »'),
               ('ven. 9', 'r', 'Renforcement', 'f', 'fait · effort 8'),
               ('dim. 11', 'c', 'Sortie longue', 'm', 'manquée · « autre »')],
         sl=('—', 'manquée')),
    dict(n=2, mon='28 sept.', charge=330, course=0,
         sess=[('mar. 29', 'r', 'Renforcement', 'f', 'fait · effort 5'),
               ('mer. 30', 'c', 'Endurance', 'm', 'manquée'),
               ('ven. 2', 'r', 'Renforcement', 'f', 'fait · effort 6'),
               ('dim. 4', 'c', 'Sortie longue', 'm', 'manquée')],
         sl=('—', 'sans course')),
    dict(n=1, mon='21 sept.', charge=60, course=60,
         sess=[('mar. 22', 'r', 'Renforcement', 'm', 'manquée'),
               ('mer. 23', 'c', 'Endurance', 'm', 'manquée'),
               ('ven. 25', 'r', 'Renforcement', 'm', 'manquée'),
               ('dim. 27', 'c', 'Sortie longue', 'f', '30 min sur 1 h 50')],
         sl=('30 min', 'sur 1 h 50')),
]
# Sorties longues prévues par le moteur (projection au 17/10, minutes) ; course de mai et objectif à part
SL_PLAN = [('2026-10-18', 109), ('2026-10-25', 110), ('2026-11-01', 110), ('2026-11-08', 70), ('2026-11-15', 110), ('2026-11-22', 110),
           ('2026-11-29', 110), ('2026-12-06', 70), ('2026-12-13', 120), ('2026-12-20', 130), ('2026-12-27', 140), ('2027-01-03', 90),
           ('2027-01-10', 154), ('2027-01-17', 169), ('2027-01-24', 185), ('2027-01-31', 120), ('2027-02-07', 200), ('2027-02-14', 130),
           ('2027-02-21', 220), ('2027-02-28', 140), ('2027-03-07', 240), ('2027-03-14', 160), ('2027-03-21', 264), ('2027-03-28', 170),
           ('2027-04-04', 265), ('2027-04-11', 180), ('2027-04-18', 290), ('2027-04-25', 200), ('2027-05-02', 160), ('2027-05-16', 100),
           ('2027-05-23', 160), ('2027-05-30', 220), ('2027-06-06', 290), ('2027-06-13', 180), ('2027-06-20', 180), ('2027-06-27', 290),
           ('2027-07-04', 180), ('2027-07-11', 319), ('2027-07-18', 180), ('2027-07-25', 350), ('2027-08-01', 180), ('2027-08-08', 360),
           ('2027-08-15', 180), ('2027-08-22', 180), ('2027-08-29', 180), ('2027-09-05', 180), ('2027-09-12', 198), ('2027-09-19', 200)]
SL_DONE = [('2026-09-06', 107, 'déclarée'), ('2026-09-27', 30, 'faite')]
ZONE = (250, 410)          # médiane des semaines précédentes du plan (60, 330, 390) = 330, ± 25 %, arrondi à 10 (convention proposée)

# ---------------------------------------------------------------- CSS des maquettes (écran clair de l'appli, isolé sous .mk)
MK_CSS = r"""
.mk{--bg:#f6f7f4;--card:#fff;--ink:#0f1c16;--mut:#5b6961;--line:#e9eee9;--chip:#eef2ee;--mint:#25c37e;--mintT:#087a49;--mintBg:#e4f6ec;
--deep:#10251c;--ember:#d1601a;--emberBg:#ffeedd;--violet:#6a4fd0;--violetBg:#ece7fe;--sky:#2c6fb8;--skyBg:#e0edfd;--sunBg:#fff1d9;--sunT:#8a5a0a;
--coralT:#b8352d;--coralBg:#fde9e7;--nav:rgba(255,255,255,.97);--shadow:0 1px 2px rgba(15,28,22,.04),0 10px 26px rgba(15,28,22,.06);
font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased;color-scheme:light;text-align:left}
.mk *,.mk *::before,.mk *::after{box-sizing:border-box}
.mk.phone{width:360px;max-width:100%;margin:0 auto;background:var(--bg);border-radius:28px;position:relative;overflow:clip;box-shadow:0 0 0 1px #d9dfda,0 12px 30px rgba(0,0,0,.10);padding-bottom:10px}
.mk .halo{position:absolute;inset:0 0 auto;height:230px;overflow:hidden;pointer-events:none}
.mk .halo i{position:absolute;border-radius:50%;filter:blur(48px);opacity:.45}
.mk .halo .a{width:240px;height:180px;background:#b9f5d6;left:-60px;top:-70px}
.mk .halo .b{width:220px;height:170px;background:#ffe0b8;right:-60px;top:-50px}
.mk header{position:relative;padding:20px 20px 4px}
.mk h1{font-size:23px;font-weight:800;letter-spacing:-.03em;margin:0;line-height:1.1;color:var(--ink)}
.mk .sub{font-size:13px;color:var(--mut);margin-top:4px}
.mk .lab{position:relative;font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mintT);margin:14px 20px 0}
.mk .card{background:var(--card);border-radius:22px;padding:4px 16px;margin:10px 14px;box-shadow:var(--shadow);position:relative}
.mk .card.pad{padding:14px 16px}
.mk .mi{width:20px;height:20px;fill:currentColor;flex:none}
.mk .h2{font-size:15.5px;font-weight:800;letter-spacing:-.01em}
.mk .mini{font-size:12.5px;color:var(--mut);line-height:1.4}
.mk .sb{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
/* lignes qui se déplient */
.mk details{border-top:1px solid var(--line)}
.mk .card>details:first-child,.mk .card>.first{border-top:0}
.mk summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:12px;padding:13px 0;-webkit-tap-highlight-color:transparent}
.mk summary::-webkit-details-marker{display:none}
.mk summary:focus-visible{outline:2px solid var(--mintT);outline-offset:2px;border-radius:8px}
.mk .qi{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;flex:none}
.mk .qi.c{background:var(--mintBg);color:var(--mintT)}.mk .qi.s{background:var(--emberBg);color:var(--ember)}.mk .qi.k{background:var(--skyBg);color:var(--sky)}
.mk .qt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.mk .qt b{font-size:15px;font-weight:700}
.mk .qv{font-size:13px;color:var(--mut);display:flex;align-items:center;gap:6px}
.mk .qn{display:flex;align-items:center;gap:8px;white-space:nowrap}
.mk .qn b{font-size:17px;font-weight:800;letter-spacing:-.01em;font-variant-numeric:tabular-nums}
.mk .chev{color:var(--mut);font-size:13px;display:inline-block;width:12px;text-align:center;transition:transform .2s}
.mk details[open]>summary .chev{transform:rotate(180deg)}
.mk .qb{padding:0 0 12px}
.mk .ln{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:9px 0;border-top:1px solid var(--line)}
.mk .ln.first{border-top:0}
.mk .ln .l{font-size:14.5px;min-width:0}
.mk .ln .l small{display:block;font-size:12.5px;color:var(--mut);margin-top:1px}
.mk .ln .v{font-size:15.5px;font-weight:800;white-space:nowrap;font-variant-numeric:tabular-nums;text-align:right}
.mk .note{font-size:12.5px;color:var(--mut);line-height:1.45;margin-top:8px}
.mk .pt{width:8px;height:8px;border-radius:50%;flex:none;display:inline-block}
.mk .pt.w{background:#f5a623}.mk .pt.o{background:var(--mint)}.mk .pt.n{background:#9fb0a6}
/* pastilles de séance */
.mk .dots{display:flex;gap:4px;align-items:center}
.mk .d{width:11px;height:11px;border-radius:50%;flex:none;display:inline-block}
.mk .d.cf{background:var(--mint)}.mk .d.rf{background:var(--violet)}
.mk .d.cm,.mk .d.rm{box-shadow:inset 0 0 0 1.6px var(--coralT)}
.mk .d.cv{border:1.6px dashed var(--mintT)}
.mk .dsep{width:1px;height:12px;background:#d5ddd7;margin:0 3px}
.mk .legend{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:11.5px;color:var(--mut);margin-top:8px}
.mk .legend span{display:inline-flex;align-items:center;gap:5px}
.mk .wk{display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid var(--line)}
.mk .wk .wn{width:70px;flex:none;font-size:13.5px;font-weight:700}
.mk .wk .wn small{display:block;font-size:11.5px;color:var(--mut);font-weight:600}
.mk .wk .wv{margin-left:auto;font-size:13.5px;font-weight:800;white-space:nowrap;text-align:right;font-variant-numeric:tabular-nums}
.mk .wk .wv small{display:block;font-size:11.5px;color:var(--mut);font-weight:600}
.mk .chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.mk .chip{font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px;white-space:nowrap;box-shadow:inset 0 0 0 1px var(--line);color:var(--ink)}
.mk .chip.m{color:var(--coralT);box-shadow:inset 0 0 0 1px #f3c9c5}
/* tableau semaine par semaine */
.mk .tb .d{width:9px;height:9px}.mk .tb{display:grid;grid-template-columns:56px 62px minmax(0,1fr) 52px;column-gap:8px;align-items:center}
.mk .th{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);padding:12px 0 6px}
.mk .tr summary{display:grid;grid-template-columns:56px 62px minmax(0,1fr) 52px;column-gap:8px;align-items:center;padding:11px 0}
.mk .tr.cur summary{background:var(--mintBg);margin:0 -10px;padding:11px 10px;border-radius:14px}
.mk .tr.cur{border-top-color:transparent}
.mk .tc{font-size:13.5px;font-weight:700;min-width:0}
.mk .tc small{display:block;font-size:11.5px;color:var(--mut);font-weight:600}
.mk .tc.r{text-align:right;font-weight:800;font-variant-numeric:tabular-nums}
.mk .tr .d{width:9px;height:9px}.mk .tr .qb .ln .l{font-size:13.5px}.mk .tr .qb .ln .v{font-size:13px;font-weight:700}
/* frise et jauges */
.mk .rib{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-top:12px}
.mk .cell{display:flex;flex-direction:column;gap:3px;align-items:stretch}
.mk .cell i{display:block;height:14px;border-radius:5px;background:#f1f4f1;position:relative;overflow:hidden}
.mk .cell i b{position:absolute;inset:0 auto 0 0;display:block;border-radius:5px}
.mk .cell i.fut{background:transparent;box-shadow:inset 0 0 0 1px #d5ddd7}
.mk .cell span{font-size:10.5px;color:var(--mut);text-align:center;font-weight:700}
.mk .cell.now span{color:var(--mintT)}
.mk .gauge{position:relative;height:40px;margin:14px 6px 0}
.mk .gauge .track{position:absolute;left:0;right:0;top:13px;height:4px;border-radius:2px;background:#e4eae5}
.mk .gauge .band{position:absolute;top:7px;height:16px;border-radius:5px}
.mk .gauge .mk1{position:absolute;top:6px;width:18px;height:18px;margin-left:-9px;border-radius:50%;box-shadow:0 0 0 3px #fff}
.mk .gauge .tick{position:absolute;top:27px;font-size:10.5px;color:var(--mut);transform:translateX(-50%);white-space:nowrap}
.mk .segbar{display:flex;gap:3px;margin-top:12px}
.mk .segbar i{flex:1;height:14px;border-radius:4px;display:block}
.mk svg text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
/* barre d'onglets (collante, comme dans l'appli) */
.mk nav{position:sticky;bottom:10px;margin:14px 12px 0;height:66px;background:var(--nav);border-radius:24px;display:flex;padding:7px;box-shadow:0 12px 30px rgba(16,32,26,.16);z-index:2}
.mk nav div{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:11.5px;font-weight:700;color:var(--mut);border-radius:18px}
.mk nav div.on{background:var(--mintBg);color:var(--mintT)}
.mk nav .mi{width:23px;height:23px}
.mk .fold{position:absolute;left:0;right:0;top:668px;height:0;z-index:3;pointer-events:none}
.mk .fold::before,.mk .fold::after{content:"";position:absolute;top:-1px;width:11px;border-top:2px solid var(--coralT);opacity:.75}
.mk .fold::before{left:0}.mk .fold::after{right:0}
"""

NAV = [("Aujourd'hui", 'home'), ('Semaine', 'calendar'), ('Suivi', 'monitoring'), ('Profil', 'person')]


def nav():
    return '<nav>' + ''.join('<div class="%s">%s%s</div>' % ('on' if l == 'Suivi' else '', ic(k), l) for l, k in NAV) + '</nav>'


def phone(inner, fold=True):
    return ('<div class="mk phone"><div class="halo"><i class="a"></i><i class="b"></i></div>'
            '<header><h1>Suivi</h1><div class="sub">Semaine 4 sur 53 · Reprise</div></header>'
            + inner + nav() + ('<div class="fold" aria-hidden="true"></div>' if fold else '') + '</div>')


def ln(label, val, small='', first=False):
    return '<div class="ln%s"><span class="l">%s%s</span><span class="v">%s</span></div>' % (
        ' first' if first else '', label, '<small>%s</small>' % small if small else '', val)


def dots(sess):
    c = [s for s in sess if s[1] == 'c']
    r = [s for s in sess if s[1] == 'r']
    return ('<span class="dots">' + ''.join('<i class="d c%s"></i>' % s[3] for s in c) + '<i class="dsep"></i>'
            + ''.join('<i class="d r%s"></i>' % s[3] for s in r) + '</span>')


LEGEND = ('<div class="legend"><span><i class="d cf"></i>course faite</span><span><i class="d rf"></i>renforcement fait</span>'
          '<span><i class="d cm"></i>manquée</span><span><i class="d cv"></i>à venir</span></div>')


def summ(icon, cls, title, verdict, dot, value):
    return ('<summary><span class="qi %s">%s</span><span class="qt"><b>%s</b><span class="qv"><i class="pt %s"></i>%s</span></span>'
            '<span class="qn"><b>%s</b><i class="chev">⌄</i></span></summary>') % (cls, ic(icon), title, dot, verdict, value)


def fmt(m):
    h, mn = divmod(int(round(m)), 60)
    return ('%d h %02d' % (h, mn) if mn else '%d h' % h) if h else '%d min' % mn


# ---------------------------------------------------------------- mini-graphiques
def charge_bars(w=300, h=96):
    """4 semaines, barres empilées (course en bas, renforcement au-dessus), zone en pointillés, semaine en cours prolongée par la sortie longue."""
    mx, x0, gap = 800, 34, 14
    bw = (w - x0 - gap * 3) / 4
    y = lambda v: 8 + (h - 8) * (1 - v / mx)
    s = '<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Charge des 4 semaines" style="display:block;margin-top:10px">' % (w, h + 18)
    s += '<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="#e0edfd" opacity=".75"/>' % (x0 - 6, y(ZONE[1]), w - x0 + 6, y(ZONE[0]) - y(ZONE[1]))
    for v in ZONE:
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#2c6fb8" stroke-dasharray="3 3" stroke-width="1"/>' % (x0 - 6, w, y(v), y(v))
        s += '<text x="0" y="%.1f" font-size="10" fill="#2c6fb8" font-weight="700">%d</text>' % (y(v) + 3.5, v)
    for i, wk in enumerate(reversed(WEEKS)):
        x = x0 + i * (bw + gap)
        tot, co = wk['charge'], wk['course']
        if wk.get('cur'):
            s += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="none" stroke="#087a49" stroke-dasharray="4 3" stroke-width="1.4"/>' % (x + .7, y(750), bw - 1.4, y(tot) - y(750) - 2)
            s += '<text x="%.1f" y="%.1f" font-size="10" text-anchor="middle" fill="#087a49" font-weight="700">≈ 750</text>' % (x + bw / 2, y(750) - 4)
        if co:
            s += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#25c37e"/>' % (x, y(co), bw, y(0) - y(co))
        if tot > co:
            s += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#6a4fd0"/>' % (x, y(tot), bw, y(co) - y(tot) - (2 if co else 0))
        s += '<text x="%.1f" y="%.1f" font-size="10.5" text-anchor="middle" fill="%s" font-weight="800">%d</text>' % (
            x + bw / 2, (y(tot) + 14) if tot >= 200 else (y(tot) - 5), '#fff' if tot >= 200 else '#0f1c16', tot)
        s += '<text x="%.1f" y="%d" font-size="10" text-anchor="middle" fill="#5b6961">S%d · %s</text>' % (x + bw / 2, h + 15, wk['n'], wk['mon'])
    return s + '</svg>'


def sl_chart(w=300, h=150):
    """Sortie longue prévue jusqu'au jour J (projection du moteur) et sorties faites."""
    import datetime as dt
    D = lambda s: dt.date.fromisoformat(s)
    t0, t1 = D('2026-09-01'), D('2027-09-30')
    x0, x1, yt, yb = 6, w - 34, 14, h - 22
    X = lambda s: x0 + (D(s) - t0).days / (t1 - t0).days * (x1 - x0)
    Y = lambda m: yb - m / 360 * (yb - yt)
    s = '<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Sortie longue jusqu\'au jour J" style="display:block;margin-top:10px">' % (w, h)
    s += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#e4f6ec"/>' % (x0, Y(360), x1 - x0, Y(300) - Y(360))
    for m in (120, 240, 360):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#e9eee9"/>' % (x0, x1, Y(m), Y(m))
        s += '<text x="%d" y="%.1f" font-size="10" fill="#5b6961">%d h</text>' % (x1 + 6, Y(m) + 3.5, m // 60)
    s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#c9d1cb"/>' % (x0, x1, yb, yb)
    # points prévus
    for d, m in SL_PLAN:
        s += '<circle cx="%.1f" cy="%.1f" r="1.9" fill="#25c37e" opacity=".45"/>' % (X(d), Y(m))
    # enveloppe : niveau de sortie longue atteint (maximum courant)
    env, mx = [], 0
    for d, m in SL_PLAN:
        mx = max(mx, m)
        env.append((X(d), Y(mx)))
    s += '<path d="M%s" fill="none" stroke="#087a49" stroke-width="2.2" stroke-linejoin="round"/>' % ' L'.join('%.1f,%.1f' % p for p in env)
    # aujourd'hui
    xt = X('2026-10-17')
    s += '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#0f1c16" stroke-dasharray="2 3" opacity=".5"/>' % (xt, xt, yt - 4, yb)
    # 50 km et objectif
    for d, lab in (('2027-05-08', '50 km'), ('2027-09-25', '★')):
        xx = X(d)
        s += '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#10251c" stroke-width="1.2"/>' % (xx, xx, yt - 4, yb)
        s += '<text x="%.1f" y="%d" font-size="10" text-anchor="%s" fill="#10251c" font-weight="800">%s</text>' % (xx + (-3 if lab == '★' else 3), yt - 5 + 9, 'end' if lab == '★' else 'start', lab)
    # sorties faites
    for d, m, k in SL_DONE:
        if k == 'déclarée':
            s += '<circle cx="%.1f" cy="%.1f" r="4" fill="#fff" stroke="#d1601a" stroke-width="2"/>' % (X(d), Y(m))
        else:
            s += '<circle cx="%.1f" cy="%.1f" r="4.5" fill="#d1601a" stroke="#fff" stroke-width="1.5"/>' % (X(d), Y(m))
    s += '<circle cx="%.1f" cy="%.1f" r="4.5" fill="#fff" stroke="#087a49" stroke-width="2.2"/>' % (X('2026-10-18'), Y(109))
    for d, lab in (('2026-10-01', 'oct.'), ('2027-01-01', 'janv.'), ('2027-04-01', 'avr.'), ('2027-07-01', 'juil.')):
        s += '<text x="%.1f" y="%d" font-size="10" text-anchor="middle" fill="#5b6961">%s</text>' % (X(d), h - 6, lab)
    s += '<text x="%.1f" y="%d" font-size="10" text-anchor="end" fill="#5b6961">25 sept.</text>' % (x1 + 30, h - 6)
    return s + '</svg>'


# ---------------------------------------------------------------- variante A : trois réponses
def plan_body():
    rows = ''.join('<div class="wk"><span class="wn">S%d<small>%s</small></span>%s<span class="wv">%s<small>%s</small></span></div>' % (
        w['n'], w['mon'], dots(w['sess']),
        '%d sur %d' % (sum(1 for s in w['sess'] if s[3] == 'f'), sum(1 for s in w['sess'] if s[3] != 'v')),
        'en cours' if w.get('cur') else ('aucune course' if not any(s[1] == 'c' and s[3] == 'f' for s in w['sess']) else ''))
        for w in WEEKS)
    return ('<div class="qb">' + ln('Course', '2 sur 7', 'sortie longue de dimanche à venir', True) + ln('Renforcement', '6 sur 8')
            + '<div style="margin-top:4px">' + rows + '</div>' + LEGEND
            + '<div class="note">7 séances manquées : 5 de course (3 endurances, 2 sorties longues) et 2 renforcements la 1re semaine. Deux semaines sans course : le plan a recalé ta reprise.</div></div>')


def sl_body():
    return ('<div class="qb">' + ln('Dernière faite', '30 min', '27 sept. · prévue 1 h 50', True)
            + ln('Prochaine', '1 h 49', 'dim. 18 oct. · 250 à 350 m de D+')
            + ln('Repère de reprise', '1 h 40', '1 h 47 du 6 sept., − 7 % (convention)')
            + ln('Sortie clé visée', '5 h à 6 h', 'juillet et août 2027')
            + '<div class="chips"><span class="chip">27 sept. · 30 min</span><span class="chip m">4 oct. · sans course</span><span class="chip m">11 oct. · manquée</span></div>'
            + '<div class="note">1 h 49 = repère de reprise + 10 % : la séance de progression de la semaine.</div></div>')


def charge_body():
    return ('<div class="qb">' + charge_bars()
            + '<div class="legend"><span><i class="d cf"></i>course</span><span><i class="d rf"></i>renforcement</span><span><i class="d" style="background:#e0edfd;box-shadow:inset 0 0 0 1px #2c6fb8"></i>ta zone (provisoire)</span></div>'
            + '<div style="margin-top:6px">' + ln('Cette semaine', '420', '≈ 750 avec la sortie longue', True)
            + ln('Ta zone', '250 à 410', 'provisoire : 3 semaines sur 4')
            + ln('Part de la course', '21 %', 'le reste vient du renforcement') + '</div>'
            + '<div class="note">Un repère, pas une limite. La limite de sécurité porte sur chaque séance (règle des 30 jours).</div></div>')


def variant_A(open_=()):
    o = lambda k: ' open' if k in open_ else ''
    inner = ('<div class="lab">Depuis le début du plan · 4 semaines</div><div class="card">'
             '<details%s>%s%s</details>' % (o('plan'), summ('calendar', 'c', 'Le plan est suivi ?', 'Renforcement oui, course non', 'w', '8 sur 15'), plan_body())
             + '<details%s>%s%s</details>' % (o('sl'), summ('terrain', 's', 'Ta sortie longue', '2 dimanches sans, reprise demain', 'w', '1 h 49'), sl_body())
             + '<details%s>%s%s</details>' % (o('ch'), summ('monitoring', 'k', 'Ta charge', 'Juste au-dessus de ta zone', 'n', '420'), charge_body())
             + '</div><div class="card"><details class="first"><summary><span class="qt"><b>Autres suivis</b><span class="qv">Poids, force, WOD refaits</span></span><span class="qn"><i class="chev">⌄</i></span></summary>'
               '<div class="qb"><div class="note" style="margin-top:0">Ce que l\'écran actuel affiche en plus, regroupé ici. Rien n\'est supprimé.</div></div></details>'
               '<details><summary><span class="qt"><b>Comment c\'est calculé</b></span><span class="qn"><i class="chev">⌄</i></span></summary>'
               '<div class="qb"><div class="note" style="margin-top:0">Plan suivi : séances faites sur séances dues, d\'après tes jours. Charge : effort × minutes, toutes séances (Foster). Zone : médiane de tes semaines précédentes ± 25 % (convention).</div></div></details></div>')
    return phone(inner)


# ---------------------------------------------------------------- variante B : semaine par semaine
def variant_B(open_=()):
    def row(w):
        f = sum(1 for s in w['sess'] if s[3] == 'f')
        due = sum(1 for s in w['sess'] if s[3] != 'v')
        body = '<div class="qb">' + ''.join(ln('%s · %s' % (s[0], s[2]), '<span style="color:%s">%s</span>' % (
            {'f': 'var(--ink)', 'm': 'var(--coralT)', 'v': 'var(--mintT)'}[s[3]], s[4]), first=(i == 0)) for i, s in enumerate(w['sess'])) + '</div>'
        return ('<details class="tr%s"%s><summary><span class="tc">S%d <i class="chev">⌄</i><small>%s</small></span><span class="tc">%s<small>%d sur %d</small></span>'
                '<span class="tc r">%s<small>%s</small></span><span class="tc r">%d<small>%s</small></span></summary>%s</details>') % (
            ' cur' if w.get('cur') else '', ' open' if w['n'] in open_ else '', w['n'], w['mon'], dots(w['sess']), f, due,
            w['sl'][0], w['sl'][1], w['charge'], 'en cours' if w.get('cur') else '&nbsp;', body)
    inner = ('<div class="lab">Semaine par semaine</div><div class="card">'
             '<div class="tb"><span class="th">Semaine</span><span class="th">Plan</span><span class="th" style="text-align:right">Sortie longue</span><span class="th" style="text-align:right">Charge</span></div>'
             + ''.join(row(w) for w in WEEKS)
             + '<div style="border-top:1px solid var(--line);padding:4px 0 10px">' + LEGEND + '</div></div>'
             '<div class="card">' + ln('Course', '2 sur 7', 'depuis le 21 sept.', True) + ln('Renforcement', '6 sur 8')
             + ln('Ta zone de charge', '250 à 410', 'provisoire : 3 semaines sur 4') + '</div>')
    return phone(inner)


# ---------------------------------------------------------------- variante C : cap sur le jour J
def ribbon():
    cells = ''
    for i in range(1, 9):
        w = next((x for x in WEEKS if x['n'] == i), None)
        if w:
            c = [s for s in w['sess'] if s[1] == 'c']
            r = [s for s in w['sess'] if s[1] == 'r']
            fc = sum(1 for s in c if s[3] == 'f') / max(1, sum(1 for s in c if s[3] != 'v'))
            fr_ = sum(1 for s in r if s[3] == 'f') / max(1, len(r))
            cells += '<div class="cell%s"><i><b style="width:%d%%;background:var(--mint)"></b></i><i><b style="width:%d%%;background:var(--violet)"></b></i><span>S%d</span></div>' % (
                ' now' if w.get('cur') else '', fc * 100, fr_ * 100, i)
        else:
            cells += '<div class="cell"><i class="fut"></i><i class="fut"></i><span>S%d</span></div>' % i
    return '<div class="rib">' + cells + '</div>'


def variant_C(open_=()):
    inner = ('<div class="card pad"><div class="sb"><span class="h2">Ta sortie longue</span><span class="mini">jusqu\'au 25 sept.</span></div>'
             '<div class="sb" style="margin-top:6px;align-items:flex-end"><span><b style="font-size:24px;letter-spacing:-.02em">1 h 49</b> <span class="mini">dim. 18 oct.</span></span>'
             '<span class="mini" style="text-align:right">cible <b style="color:var(--ink);font-size:14px">5 h à 6 h</b></span></div>'
             + sl_chart()
             + '<div class="legend"><span><i class="d" style="background:#d1601a"></i>faite</span><span><i class="d" style="box-shadow:inset 0 0 0 2px #d1601a"></i>déclarée</span><span><i class="d" style="background:#087a49;height:3px;border-radius:2px;width:14px"></i>niveau prévu</span><span><i class="d" style="background:#e4f6ec;box-shadow:inset 0 0 0 1px #9fdcbc;border-radius:3px"></i>sortie clé visée</span></div>'
             + '<div style="margin-top:4px">' + ln('Dernière faite', '30 min', '27 sept. · prévue 1 h 50', True) + ln('Dimanches manqués', '2', '4 et 11 oct.') + '</div></div>'
             '<div class="card pad"><div class="sb"><span class="h2">Ta régularité</span><span class="mini">Reprise · 8 semaines</span></div>' + ribbon()
             + '<div class="legend"><span><i class="d cf"></i>course</span><span><i class="d rf"></i>renforcement</span><span>barre pleine = tout fait</span></div>'
             + '<div style="margin-top:4px">' + ln('Course', '2 sur 7', '', True) + ln('Renforcement', '6 sur 8') + '</div></div>'
             '<div class="card"><details class="first"%s>%s%s</details></div>' % (' open' if 'ch' in open_ else '', summ('monitoring', 'k', 'Ta charge', 'Juste au-dessus de ta zone', 'n', '420'), charge_body()))
    return phone(inner)


# ---------------------------------------------------------------- variante D : trois règles graduées
def variant_D(open_=()):
    seg = ''
    order = [('cf', 2), ('rf', 6), ('m', 7), ('v', 1)]
    col = {'cf': 'var(--mint)', 'rf': 'var(--violet)', 'm': 'transparent;box-shadow:inset 0 0 0 1.5px #e3a8a2', 'v': 'transparent;box-shadow:inset 0 0 0 1.5px var(--mintT);opacity:.5'}
    for k, n in order:
        seg += ''.join('<i style="background:%s"></i>' % col[k] for _ in range(n))
    g1 = ('<div class="card pad"><div class="sb"><span class="h2">Le plan</span><b style="font-size:17px">8 sur 15</b></div>'
          '<div class="segbar">' + seg + '</div>'
          '<div class="legend"><span><i class="d cf"></i>course 2 sur 7</span><span><i class="d rf"></i>renforcement 6 sur 8</span><span><i class="d cm"></i>manquées 7</span><span><i class="d cv"></i>à venir 1</span></div></div>')
    P = lambda m: m / 360 * 100
    g2 = ('<div class="card pad"><div class="sb"><span class="h2">Ta sortie longue</span><b style="font-size:17px">1 h 49</b></div>'
          '<div class="gauge"><div class="track"></div><div class="band" style="left:%.1f%%;width:%.1f%%;background:#e4f6ec;box-shadow:inset 0 0 0 1px #9fdcbc"></div>'
          '<div class="mk1" style="left:%.1f%%;background:#d1601a"></div><div class="mk1" style="left:%.1f%%;background:#fff;box-shadow:0 0 0 3px #fff,inset 0 0 0 2.5px #087a49"></div>'
          '%s</div>'
          '<div class="legend" style="margin-top:10px"><span><i class="d" style="background:#d1601a"></i>dernière : 30 min</span><span><i class="d" style="box-shadow:inset 0 0 0 2px #087a49"></i>prévue dim. : 1 h 49</span><span><i class="d" style="background:#e4f6ec;box-shadow:inset 0 0 0 1px #9fdcbc"></i>cible : 5 h à 6 h</span></div></div>') % (
        P(300), P(60), P(30), P(109), ''.join('<span class="tick" style="left:%.1f%%">%s</span>' % (P(m), '%d h' % (m // 60) if m else '0') for m in (0, 60, 120, 180, 240, 300, 360)))
    K = lambda v: v / 800 * 100
    g3 = ('<div class="card pad"><div class="sb"><span class="h2">Ta charge</span><b style="font-size:17px">420</b></div>'
          '<div class="gauge"><div class="track"></div><div class="band" style="left:%.1f%%;width:%.1f%%;background:#e0edfd;box-shadow:inset 0 0 0 1px #8fb6e3"></div>'
          '<div class="mk1" style="left:%.1f%%;background:#2c6fb8"></div><div class="mk1" style="left:%.1f%%;background:#fff;box-shadow:0 0 0 3px #fff,inset 0 0 0 2px #2c6fb8;opacity:.8"></div>'
          '%s</div>'
          '<div class="legend" style="margin-top:10px"><span><i class="d" style="background:#2c6fb8"></i>cette semaine : 420</span><span><i class="d" style="box-shadow:inset 0 0 0 2px #2c6fb8"></i>avec la sortie longue : ≈ 750</span><span><i class="d" style="background:#e0edfd;box-shadow:inset 0 0 0 1px #8fb6e3"></i>ta zone : 250 à 410</span></div></div>') % (
        K(ZONE[0]), K(ZONE[1] - ZONE[0]), K(420), K(750), ''.join('<span class="tick" style="left:%.1f%%">%d</span>' % (K(v), v) for v in (0, 200, 400, 600, 800)))
    inner = '<div class="lab">Depuis le début du plan · 4 semaines</div>' + g1 + g2 + g3
    return phone(inner)


VARIANTS = [
    ('A', 'Trois réponses', variant_A, ('plan',),
     'Trois lignes fines : une question, un verdict en mots, le chiffre à droite. Le détail se déplie.',
     'Les 3 réponses sur un seul écran sans défiler ; le détail (semaines, dimanches, graphique de charge) à la demande.',
     'Aucune tendance visible fermée ; le verdict en mots doit être bien calibré, sinon il ment.'),
    ('B', 'Semaine par semaine', variant_B, (3,),
     'Un tableau : une ligne par semaine, une colonne par question. Une semaine se déplie en séances.',
     'L\'évolution semaine après semaine, et le motif de chaque séance manquée.',
     'Aucun verdict : tu lis et tu conclus. Quatre colonnes à 360 px, c\'est le maximum.'),
    ('C', 'Cap sur le jour J', variant_C, (),
     'La sortie longue sur le chemin jusqu\'au 25 sept. 2027, puis ta régularité semaine par semaine.',
     'Où tu en es par rapport à la cible, la course de mai et le jour J ; la phase en cours.',
     'La charge passe au second plan (repliée). La courbe est une projection recalculée chaque jour.'),
    ('D', 'Trois règles graduées', variant_D, (),
     'Chaque question devient une jauge : un repère sur une règle, sans dépli.',
     'Les 3 réponses d\'un coup d\'œil, avec la distance à la cible de sortie longue.',
     'Aucun détail, aucune semaine. La jauge de charge se lit comme une limite à ne pas dépasser.'),
]


# ---------------------------------------------------------------- page de comparaison
PAGE_CSS = r"""
:root{--pg-bg:#f2f4f1;--pg-ink:#14211b;--pg-mut:#56645c;--pg-line:#dde3de;--pg-card:#ffffff;--pg-acc:#087a49;--pg-deep:#10251c;--pg-warn:#8a5a0a;--pg-warnBg:#fff1d9;
--f-body:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;--f-disp:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--pg-bg:#0f1513;--pg-ink:#e3ebe6;--pg-mut:#9eaea5;--pg-line:#27312c;--pg-card:#19211d;--pg-acc:#5fe0a3;--pg-deep:#e3ebe6;--pg-warn:#f3c46a;--pg-warnBg:#3a2f14;color-scheme:dark}}
:root[data-theme="dark"]{--pg-bg:#0f1513;--pg-ink:#e3ebe6;--pg-mut:#9eaea5;--pg-line:#27312c;--pg-card:#19211d;--pg-acc:#5fe0a3;--pg-deep:#e3ebe6;--pg-warn:#f3c46a;--pg-warnBg:#3a2f14;color-scheme:dark}
body{background:var(--pg-bg);color:var(--pg-ink);font:15px/1.55 var(--f-body);margin:0}
.wrap{max-width:720px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 56px}
h1{font:800 30px/1.1 var(--f-disp);letter-spacing:-.03em;margin:0;text-wrap:balance}
h2{font:800 21px/1.2 var(--f-disp);letter-spacing:-.02em;margin:0;text-wrap:balance}
h3{font-size:15px;font-weight:800;margin:0}
.eyebrow{font-size:11.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--pg-acc)}
.meta{font-size:13px;color:var(--pg-mut);margin-top:6px}
section{margin-top:40px}
p{margin:8px 0 0;max-width:65ch}
.box{background:var(--pg-card);border-radius:16px;padding:14px 16px;margin-top:14px;box-shadow:0 0 0 1px var(--pg-line)}
.box ul{margin:6px 0 0;padding-left:18px}.box li{margin:4px 0}
.warn{background:var(--pg-warnBg);box-shadow:none}
.vhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.vletter{font:800 28px/1 var(--f-disp);color:var(--pg-acc)}
.idea{font-size:15.5px;margin-top:6px}
.frame{margin:16px calc(-1 * max(16px,env(safe-area-inset-left,0px))) 0;display:flex;justify-content:center}
@media (min-width:420px){.frame{margin-inline:0}}
dl{display:grid;grid-template-columns:auto minmax(0,1fr);gap:6px 12px;margin:14px 0 0}
dt{font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--pg-mut);padding-top:2px}
dd{margin:0}
.cmp{display:grid;gap:10px;margin-top:14px}
.cmp .box{margin:0}
.cmp .box b{font-size:15px}
.reco{box-shadow:0 0 0 2px var(--pg-acc)}
.tag{display:inline-block;font-size:11.5px;font-weight:800;padding:3px 8px;border-radius:999px;background:var(--pg-acc);color:var(--pg-bg);margin-left:6px;vertical-align:2px}
ol{padding-left:20px}ol li{margin:8px 0}
a{color:var(--pg-acc)}
.src{font-size:13px;color:var(--pg-mut)}
"""


def page(fragment=False):
    parts = []
    parts.append('<title>Maquettes Suivi Ascend</title><meta name="claude:viewport-fit-sides" content="cover">'
                 '<style>' + PAGE_CSS + MK_CSS + '</style>')
    parts.append('<div class="wrap"><div class="eyebrow">Ascend · chantier interface</div><h1>Suivi en 3 questions</h1>'
                 '<div class="meta">Maquettes du 17 oct. 2026 · à valider avant tout code · index.html non modifié</div>')
    parts.append('<div class="box"><h3>Lecture retenue</h3><ul>'
                 '<li><b>Données</b> : ton profil reconstitué depuis tes captures (plan démarré le 21 sept.), séances réelles jusqu\'au 11 oct. ; '
                 'semaine du 12 oct. <b>supposée</b> faite comme prévue (renforcement mar. et ven., endurance 30 min mer.) ; vue du samedi 17 oct. à 9 h.</li>'
                 '<li><b>Plan suivi</b> = séances faites sur séances dues depuis le début du plan, course et renforcement séparés.</li>'
                 '<li><b>Zone habituelle</b> = médiane de tes semaines précédentes ± 25 %, provisoire sous 4 semaines. Proposition de ma part, à valider (convention).</li>'
                 '<li>Les maquettes sont interactives : touche une ligne pour la déplier. Les deux traits rouges sur les bords marquent le bas de ton premier écran (au-dessus de la barre d\'onglets).</li></ul></div>')
    parts.append('<section><div class="eyebrow">Aujourd\'hui</div><h2>Ce que l\'écran Suivi montre</h2>'
                 '<p>Quatre tuiles de la semaine, la charge par jour, la liste des séances, le poids, les minutes et la charge sur 12 semaines, les sorties longues. '
                 'Aucune des trois questions n\'a de réponse directe : la charge mélange course et CrossFit, la sortie longue n\'a ni prévu ni cible, et rien ne compare au plan.</p>'
                 '<div class="box"><h3>Ce que le moteur sait déjà calculer</h3><ul>'
                 '<li><b>Plan</b> : séances prévues et rattachement des séances faites (comme l\'onglet Semaine), motifs « Pas faite ».</li>'
                 '<li><b>Sortie longue</b> : la prochaine, et toute la projection jusqu\'au jour J (cible de sortie clé 5 h à 6 h).</li>'
                 '<li><b>Charge</b> : effort × minutes par semaine (déjà affichée).</li></ul></div>'
                 '<div class="box warn"><h3>Trois limites qui pèsent sur les maquettes</h3><ul>'
                 '<li>Le moteur recalcule le passé : une semaine sans aucune course devient « arrêt » et <b>ses séances prévues disparaissent</b> (tes semaines du 28 sept. et du 5 oct.). '
                 'Pour compter les séances dues, il faut partir de tes jours de la période (course mer. et dim., renforcement mar. et ven.). Les durées prévues de ces semaines sont perdues.</li>'
                 '<li>Le <b>repère de reprise</b> (1 h 40) est calculé par le moteur mais pas transmis à l\'écran. L\'afficher demande d\'ajouter une sortie au moteur, sans changer ses règles.</li>'
                 '<li>La <b>zone habituelle</b> n\'existe nulle part : c\'est une règle nouvelle (décision et hypothèse à écrire).</li></ul></div></section>')
    for L, name, fn, op, idea, shows, leaves in VARIANTS:
        parts.append('<section id="%s"><div class="vhead"><span class="vletter">%s</span><h2>%s</h2></div><p class="idea">%s</p>'
                     '<div class="frame">%s</div><dl><dt>Montre</dt><dd>%s</dd><dt>Laisse</dt><dd>%s</dd></dl></section>' % (
                         L.lower(), L, name, idea, fn(op), shows, leaves))
    parts.append(COMPARE)
    parts.append('</div>')
    html = ''.join(parts[:1]) + fr_typo(''.join(parts[1:]))
    if fragment:
        return html
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + html.replace('</style>', '</style></head><body>', 1) + '</body></html>'


COMPARE = """
<section id="comparatif"><div class="eyebrow">Comparatif</div><h2>Ce que chacune fait bien, et mal</h2>
<div class="cmp">
<div class="box reco"><b>A · Trois réponses</b><span class="tag">recommandée</span><p>Répond aux 3 questions en 3 secondes et suit tes critères (blocs fins, valeurs à droite, détail qui se déplie). Défaut : fermée, elle ne montre aucune tendance, et un verdict en mots mal calibré trompe plus qu'un chiffre.</p></div>
<div class="box"><b>B · Semaine par semaine</b><p>La plus fidèle aux faits : on voit que la course décroche dès la semaine 1. Mais c'est un tableau à décoder, sans réponse écrite, et quatre colonnes à 360 px ne laissent aucune marge.</p></div>
<div class="box"><b>C · Cap sur le jour J</b><p>La plus motivante. Mais la courbe est une projection recalculée chaque jour : elle bougera sans explication tant que le fil « ce qui a changé et pourquoi » n'existe pas. Et elle met en vedette un objectif lointain quand ton problème du moment est la régularité.</p></div>
<div class="box"><b>D · Trois règles graduées</b><p>La plus compacte. Mais la jauge de charge transforme une convention en limite : dimanche, faire ta sortie longue te mettrait « hors zone ». Sur une règle de 0 à 6 h, 30 min et 1 h 49 se touchent presque.</p></div>
</div></section>
<section id="recommandation"><div class="eyebrow">Recommandation</div><h2>A, nourrie de B et de C</h2>
<p>Garde la structure de A. Mets dans ses blocs dépliés le meilleur des autres : les lignes de semaines de B dans « Le plan est suivi ? » (déjà le cas dans la maquette), et la courbe de C dans « Ta sortie longue », à la place des pastilles de dimanches. J'écarte D : une jauge de charge avec une zone à respecter promet une protection que la science ne soutient pas, et elle te découragerait de faire ce que le plan demande.</p>
<div class="box warn"><h3>Je te challenge sur la 3e question</h3>
<p>Une « zone habituelle » de charge n'a pas de preuve de protection chez le coureur. Le rapport charge aiguë / chronique est contesté depuis 2020, et la grande cohorte de 2025 qui fonde ta règle des 30 jours ne trouve aucun lien entre la hausse d'une semaine à l'autre et la blessure. En reprise, le plan te fait sortir de la zone par le haut : c'est voulu. Et cette semaine, 79 % de ta charge vient du CrossFit (88 % sur 4 semaines) : un seul chiffre cache que tu cours peu.</p>
<p>Ma proposition : garder la question, mais repliée, en couleur neutre, présentée comme un repère (convention), jamais comme une alerte, avec la part course / renforcement. Si tu veux aller au bout de la logique, remplace-la plus tard par « ta course par rapport à ce que le plan prévoit ».</p></div>
<div class="box"><h3>À trancher avant de coder</h3><ol>
<li><b>Séances dues</b> : compter d'après tes jours de la période quand le moteur a recalé une semaine en « arrêt » (décision à écrire). L'historique exact du plan viendra avec le fil « ce qui a changé et pourquoi ».</li>
<li><b>Repère de sortie longue</b> : le moteur doit le transmettre à l'écran (sortie en plus, règles inchangées, tests à relancer).</li>
<li><b>Zone de charge</b> : valider la définition (médiane ± 25 %, 4 semaines) ou en choisir une autre ; hypothèse à créer.</li>
<li><b>Autres suivis</b> (poids, force, WOD, sommeil) : regroupés dans un bloc replié en bas, ou déplacés dans les modules du Profil.</li>
</ol></div>
<div class="box"><h3>Observation sur le moteur, hors maquettes</h3>
<p>Ta sortie longue de dimanche (1 h 49) repose sur le repère de reprise (ton 1 h 47 du 6 sept., − 7 %), une convention. Si ta plus longue sortie des 30 derniers jours est bien celle de 30 min du 27 sept., 1 h 49 fait + 263 % : la tranche où l'étude de 2025 trouve le risque le plus élevé (au-delà de + 100 %, sur route et en distance). Le texte de cette convention manque toujours dans les documents. L'écran Suivi rendra ce décalage visible : à trancher avant de coder le bloc sortie longue.</p></div>
</section>
<section id="sources"><div class="eyebrow">Sources</div>
<p class="src">Frandsen et al., How much running is too much?, British Journal of Sports Medicine, 2025 (docs/SOURCES.md, S-BLE-004). ·
<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC7534938/" target="_blank" rel="noopener">Impellizzeri et al. 2020, limites conceptuelles du rapport aigu / chronique</a> ·
<a href="https://iris.univr.it/retrieve/e34cfb98-e922-4c2f-aab5-18583ab7e31b/Impellizzeri_What%20Role%20Do%20Chronic%20Workloads%20Play_SportMed_2021.pdf" target="_blank" rel="noopener">Impellizzeri et al., What role do chronic workloads play in the ACWR?, Sports Medicine 2021</a> ·
<a href="https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2021.669687/full" target="_blank" rel="noopener">Editorial : ACWR, is there scientific evidence?, Frontiers in Physiology 2021</a></p></section>
"""


# ---------------------------------------------------------------- rendu
def fr_typo(h):
    for a, b in ((' :', '\u00a0:'), ('« ', '«\u00a0'), (' »', '\u00a0»'), (' %', '\u00a0%'), (' ?', '\u00a0?')):
        h = h.replace(a, b)
    return h


def standalone(inner):
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>body{margin:0;background:#fff}#cnv{padding:14px;display:inline-block;background:#fff}'
            + MK_CSS + '</style></head><body><div id="cnv">' + fr_typo(inner) + '</div></body></html>')


EXPORTS = [('suivi_A', variant_A, ()), ('suivi_A_plan', variant_A, ('plan',)), ('suivi_A_sl', variant_A, ('sl',)), ('suivi_A_charge', variant_A, ('ch',)),
           ('suivi_B', variant_B, ()), ('suivi_B_S3', variant_B, (3,)), ('suivi_C', variant_C, ()), ('suivi_D', variant_D, ())]

if __name__ == '__main__':
    open(os.path.join(HERE, 'suivi.html'), 'w', encoding='utf-8').write(page())
    if '--fragment' in sys.argv:
        out = sys.argv[sys.argv.index('--fragment') + 1]
        open(out, 'w', encoding='utf-8').write(page(fragment=True))
    if '--no-png' not in sys.argv:
        from playwright.sync_api import sync_playwright
        d = os.path.join(HERE, 'suivi'); os.makedirs(d, exist_ok=True)
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 420, 'height': 2600}, device_scale_factor=2)
            for name, fn, op in EXPORTS:
                f = os.path.join(d, name + '.html')
                open(f, 'w', encoding='utf-8').write(standalone(fn(op)))
                pg.goto('file://' + f); pg.wait_for_timeout(120)
                pg.locator("#cnv").screenshot(path=os.path.join(d, name + '.png'))
                os.remove(f)
                print('ok', name)
            b.close()
