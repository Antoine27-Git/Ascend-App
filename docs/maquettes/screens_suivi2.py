"""Suivi D-92 : maquettes sur les questions validées le 17/10/2026 (prêt ? / je fais ce qu'il faut ? / j'encaisse ? / progrès / temps).

Produit suivi2.html (page de comparaison) et suivi2/*.png. Lancer : cd docs/maquettes && python3 screens_suivi2.py
Mêmes données que screens_suivi.py (profil reconstitué, semaine du 12/10 supposée faite, samedi 17/10 9 h) ;
état « dimanche soir » : sortie longue du 18/10 supposée faite en 1 h 50, 320 m de D+, effort 4.
Chiffres tirés du moteur actuel : projection de sortie longue jusqu'à 6 h (8 août 2027), aucun écart ;
densité de D+ de départ 149 m/h (rampe jusqu'à 298 m/h) ; nutrition 15 g/h, +6 g/h par semaine tolérée ; durée estimée 15 h.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from base import ic
from screens_suivi import MK_CSS, PAGE_CSS, WEEKS, nav, ln, dots, LEGEND, sl_chart, fr_typo

CSS2 = r"""
.mk .ok{background:var(--mint)}.mk .late{background:#f5a623}.mk .neu{background:#9fb0a6}
.mk .brk summary{padding:12px 0}
.mk .bt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
.mk .bt b{font-size:15px;font-weight:700}
.mk .bt span{font-size:12.5px;color:var(--mut);display:flex;align-items:center;gap:6px}
.mk .bv{text-align:right;white-space:nowrap;display:flex;align-items:center;gap:8px}
.mk .bv b{font-size:16px;font-weight:800;font-variant-numeric:tabular-nums;display:block}
.mk .bv small{display:block;font-size:11.5px;color:var(--mut);font-weight:600}
.mk .cardt{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:14px 0 4px}
.mk .cardt .h2{font-size:16px}
.mk .verdict{font-size:14.5px;line-height:1.45;padding:2px 0 12px}
.mk .lever{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:12px 0;border-top:1px solid var(--line);font-size:14px;font-weight:700;color:var(--mintT)}
.mk .lever span{color:var(--ink);font-weight:600;font-size:13.5px}
.mk .proof{display:flex;gap:12px;align-items:center;margin:10px 14px;padding:12px 14px;border-radius:18px;background:var(--deep);color:#fff}
.mk .proof b{display:block;font-size:14.5px}.mk .proof span{font-size:12.5px;opacity:.85}
.mk .proof .x{margin-left:auto;opacity:.7;font-size:16px}
.mk .tl{position:relative;margin:12px 4px 2px;height:44px}
.mk .tl .ln0{position:absolute;left:0;right:0;top:20px;height:3px;background:#e3e9e4;border-radius:2px}
.mk .tl .done{position:absolute;left:0;top:20px;height:3px;background:var(--mintT);border-radius:2px}
.mk .tl .pt2{position:absolute;top:13px;width:17px;height:17px;margin-left:-8.5px;border-radius:50%;box-shadow:0 0 0 3px #fff;display:flex;align-items:center;justify-content:center;color:#fff;font-size:10px;font-weight:800}
.mk .tl .lab2{position:absolute;top:34px;font-size:10.5px;color:var(--mut);transform:translateX(-50%);white-space:nowrap}
.mk .tl .lab2.l{transform:none}.mk .tl .lab2.r{transform:translateX(-100%)}
.mk .story{font-size:15px;line-height:1.5;padding:14px 0 6px}
.mk .story p{margin:0 0 8px}
.mk .story b{font-weight:800}
.mk .story .k2{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mintT);display:block;margin-bottom:4px}
"""


def phone(inner, sub='Semaine 4 sur 53 · Reprise · J−343'):
    return ('<div class="mk phone"><div class="halo"><i class="a"></i><i class="b"></i></div>'
            '<header><h1>Suivi</h1><div class="sub">%s</div></header>' % sub + inner + nav()
            + '<div class="fold" aria-hidden="true"></div></div>')


def brick(icon, cls, title, verdict, vcls, val, small, body, open_=False, first=False):
    return ('<details class="brk%s"%s><summary><span class="qi %s">%s</span><span class="bt"><b>%s</b><span><i class="pt %s"></i>%s</span></span>'
            '<span class="bv"><span><b>%s</b><small>%s</small></span><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details>') % (
        ' first' if first else '', ' open' if open_ else '', cls, ic(icon), title, vcls, verdict, val, small, body)


# ---------------------------------------------------------------- contenus dépliés (communs aux variantes)
def body_duree():
    return (sl_chart()
            + '<div class="legend"><span><i class="d" style="background:#d1601a"></i>faite</span><span><i class="d" style="box-shadow:inset 0 0 0 2px #d1601a"></i>déclarée</span>'
              '<span><i class="d" style="background:#087a49;height:3px;border-radius:2px;width:14px"></i>niveau prévu</span><span><i class="d" style="background:#e4f6ec;box-shadow:inset 0 0 0 1px #9fdcbc;border-radius:3px"></i>sortie clé visée</span></div>'
            + '<div style="margin-top:6px">' + ln('Plus longue tenue', '1 h 47', '6 sept. · déclarée au départ', True)
            + ln('Dans les 30 derniers jours', '30 min', '27 sept.')
            + ln('Visée', '5 h à 6 h', 'avant fin août 2027') + '</div>'
            + '<div class="note">Le plan y arrive à ce rythme. Ce qui le ferait déraper : des dimanches sans sortie longue.</div>')


def body_dplus():
    return (ln('Plus grand D+ en une sortie', '500 m', '6 sept.', True)
            + ln('Repère à cette date', '≈ 300 m', 'monte avec ta sortie longue')
            + ln('Visé', '≈ 1 800 m', 'sur ta plus longue sortie, août 2027')
            + '<div class="note">Ta course : 4 500 m sur 80 km. Le D+ de tes sorties longues monte jusqu\'à la densité de la course à la fin de la phase de fond.</div>')


def body_ventre():
    return (ln('Toléré aujourd\'hui', '15 g/h', 'point de départ', True)
            + ln('Visé', '60 à 90 g/h', 'sur les sorties de plus de 2 h')
            + ln('Il te faut', '≈ 8 semaines', 'de sorties longues nourries et bien digérées pour 60 g/h')
            + '<div class="note">Nausées et vomissements : première cause d\'abandon sur 160 km. Teste ce que tu prendras en course.</div>')


def body_plan():
    rows = ''.join('<div class="wk"><span class="wn">S%d<small>%s</small></span>%s<span class="wv">%s<small>%s</small></span></div>' % (
        w['n'], w['mon'], dots(w['sess']),
        '%d sur %d' % (sum(1 for s in w['sess'] if s[3] == 'f'), sum(1 for s in w['sess'] if s[3] != 'v')),
        'en cours' if w.get('cur') else ('aucune course' if not any(s[1] == 'c' and s[3] == 'f' for s in w['sess']) else ''))
        for w in WEEKS)
    return (ln('Sorties longues', '1 sur 3', '4 et 11 oct. manquées · 18 oct. à venir', True)
            + ln('Endurances', '1 sur 4') + ln('Renforcements', '6 sur 8')
            + '<div style="margin-top:4px">' + rows + '</div>' + LEGEND)


def body_encaisse(dim=False):
    return (ln('Effort de tes endurances', 'pas encore', '1 notée sur 4 pour avoir ton repère', True)
            + ln('Manquées pour fatigue', '0')
            + ln('Au-delà du prévu', 'aucune', 'séance faite plus longue que prévu et que la règle des 30 jours')
            + '<div class="note">C\'est ce que le plan lit pour ralentir ou accélérer. Tu n\'as rien à faire de plus que noter ton effort après chaque séance.</div>')


LEVER_PLAN = '<div class="lever">Ne rattrape pas<span>dimanche : la sortie prévue, pas plus</span></div>'
TEMPS = ('<div class="card"><details class="first"><summary><span class="qi c">%s</span><span class="bt"><b>Ton temps estimé</b><span>80 km · 4 500 m D+</span></span>'
         '<span class="bv"><span><b>≈ 15 h</b><small>Ton objectif ›</small></span></span></summary></details></div>') % ic('timer')


# ---------------------------------------------------------------- V1 : verdicts en lignes
def v1(open_=(), dim=False):
    o = lambda k: k in open_
    proof = ('<div class="proof"><span class="qi" style="background:rgba(255,255,255,.12);color:#ecd08f">%s</span><span><b>Record depuis le 6 sept.</b>'
             '<span>1 h 50 et 320 m de D+ aujourd\'hui</span></span><span class="x">×</span></div>') % ic('terrain') if dim else ''
    ready = ('<div class="card"><div class="cardt"><span class="h2">Prêt pour le jour J ?</span><span class="mini">3 sur 3</span></div>'
             + brick('terrain', 's', 'La durée', 'dans les temps', 'ok', '1 h 50' if dim else '1 h 47', 'sur 5 à 6 h', body_duree(), o('duree'), True)
             + brick('terrain', 'k', 'Le dénivelé', 'dans les temps', 'ok', '500 m', 'sur ≈ 1 800 m', body_dplus(), o('dplus'))
             + brick('nutrition', 'c', 'Le ventre', 'dans les temps', 'ok', '15 g/h', 'sur 60 à 90', body_ventre(), o('ventre')) + '</div>')
    plan = ('<div class="card"><details class="first brk"%s><summary><span class="qi c">%s</span><span class="bt"><b>Tu fais ce qu\'il faut ?</b><span><i class="pt late"></i>Sortie longue en retard</span></span>'
            '<span class="bv"><span><b>%s</b><small>séances</small></span><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details>%s'
            '<details class="brk"%s><summary><span class="qi k">%s</span><span class="bt"><b>Tu encaisses ?</b><span><i class="pt neu"></i>Rien d\'anormal, repère en cours</span></span>'
            '<span class="bv"><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details></div>') % (
        ' open' if o('plan') else '', ic('calendar'), '9 sur 16' if dim else '8 sur 15', body_plan(), (LEVER_PLAN.replace('dimanche : la sortie prévue, pas plus', 'mercredi : l\'endurance prévue, 28 min') if dim else LEVER_PLAN), ' open' if o('enc') else '', ic('monitoring'), body_encaisse(dim))
    return phone(proof + ready + plan + TEMPS, sub=('Dimanche 18 oct. · Semaine 4 sur 53 · J−342' if dim else 'Semaine 4 sur 53 · J−343'))


# ---------------------------------------------------------------- V2 : frise du jour J
def v2():
    P = lambda frac: '%.1f%%' % (frac * 100)
    # 21 sept. 2026 -> 25 sept. 2027 : 369 jours ; aujourd'hui j 26 ; 50 km j 229
    tl = ('<div class="tl"><div class="ln0"></div><div class="done" style="width:%s"></div>'
          '<div class="pt2" style="left:%s;background:var(--mintT)"></div><div class="pt2" style="left:%s;background:#25c37e">2</div><div class="pt2" style="left:100%%;background:#10251c">★</div>'
          '<span class="lab2 l" style="left:0">21 sept.</span><span class="lab2" style="left:%s;display:none"></span><span class="lab2" style="left:%s">8 mai</span><span class="lab2 r" style="left:100%%">25 sept.</span></div>') % (
        P(26 / 369), P(26 / 369), P(229 / 369), P(26 / 369 + .04), P(229 / 369))
    row = lambda t, v, s, cls, first=False: '<div class="ln%s"><span class="l"><i class="pt %s" style="margin-right:7px"></i>%s</span><span class="v">%s<small style="display:block;font-size:11.5px;color:var(--mut);font-weight:600">%s</small></span></div>' % (' first' if first else '', cls, t, v, s)
    ready = ('<div class="card pad"><div class="sb"><span class="h2">Prêt pour le jour J ?</span><b style="font-size:14px;color:var(--mintT)">dans les temps</b></div>' + tl
             + sl_chart()
             + '<div style="margin-top:2px">' + row('Durée', '1 h 47', 'sur 5 à 6 h', 'ok', True) + row('Dénivelé', '500 m', 'sur ≈ 1 800 m', 'ok') + row('Ventre', '15 g/h', 'sur 60 à 90', 'ok') + '</div></div>')
    plan = ('<div class="card"><details class="first brk"><summary><span class="qi c">%s</span><span class="bt"><b>Tu fais ce qu\'il faut ?</b><span><i class="pt late"></i>Sortie longue en retard</span></span>'
            '<span class="bv"><span><b>8 sur 15</b><small>séances</small></span><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details>'
            '<details class="brk"><summary><span class="qi k">%s</span><span class="bt"><b>Tu encaisses ?</b><span><i class="pt neu"></i>Rien d\'anormal, repère en cours</span></span>'
            '<span class="bv"><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details></div>') % (ic('calendar'), body_plan(), ic('monitoring'), body_encaisse())
    return phone(ready + plan + TEMPS)


# ---------------------------------------------------------------- V3 : le bilan écrit
def v3():
    story = ('<div class="card"><div class="story"><span class="k2">Ton point au 17 oct.</span>'
             '<p><b>Tu es dans les temps</b> pour le 25 sept. : durée, dénivelé et ventre.</p>'
             '<p><b>Ce qui freine :</b> 2 dimanches sans sortie longue. Tes renforcements sont faits.</p>'
             '<p><b>Côté fatigue,</b> rien d\'anormal. Ton repère d\'effort se construit (1 endurance notée sur 4).</p></div>'
             '<div class="lever">Dimanche : ta sortie longue<span>1 h 49, pas plus ›</span></div></div>')
    detail = ('<div class="lab">Le détail</div><div class="card">'
              + brick('terrain', 's', 'Prêt ?', '3 sur 3 dans les temps', 'ok', '', '', '<div class="note" style="margin-top:0">Durée, dénivelé, ventre : mêmes blocs que la variante 1.</div>', first=True)
              + brick('calendar', 'c', 'Tu fais ce qu\'il faut ?', 'Sortie longue en retard', 'late', '8 sur 15', 'séances', body_plan())
              + brick('monitoring', 'k', 'Tu encaisses ?', 'Rien d\'anormal, repère en cours', 'neu', '', '', body_encaisse()) + '</div>')
    return phone(story + detail + TEMPS)


VARIANTS = [
    ('1', 'Verdicts en lignes', 'Un bloc « Prêt ? » à trois lignes (durée, dénivelé, ventre), puis « Tu fais ce qu\'il faut ? » et « Tu encaisses ? ». Tout se déplie.',
     [('suivi2_1', v1, {}), ('suivi2_1_duree', v1, {'open_': ('duree',)}), ('suivi2_1_plan', v1, {'open_': ('plan',)}), ('suivi2_1_dim', v1, {'dim': True})],
     'Les 5 réponses sur le premier écran. Le graphique de C est rangé dans « La durée ». La preuve de progrès apparaît en haut quand elle existe (état du dimanche soir).',
     'Aucun graphique visible sans toucher.'),
    ('2', 'Frise du jour J', 'Ta variante C, élargie : la frise jusqu\'au 25 sept. et la courbe de sortie longue en tête, les trois briques dessous, puis les deux autres questions.',
     [('suivi2_2', v2, {})],
     'Le chemin jusqu\'au jour J d\'un coup d\'œil, la course de mai placée.',
     'La courbe ne parle que de la durée : le dénivelé et le ventre sont des lignes. « Tu fais ce qu\'il faut ? » passe sous la ligne de flottaison.'),
    ('3', 'Le bilan écrit', 'Trois phrases qui répondent aux questions, un levier, puis le détail replié.',
     [('suivi2_3', v3, {})],
     'Lisible en 5 secondes, sans aucun chiffre à interpréter. Le plus proche d\'un coach qui te parle.',
     'Les phrases doivent être générées par des règles (H-53 à H-55) : si elles sont mal calibrées, elles mentent avec aplomb.'),
]


def page(fragment=False):
    parts = ['<title>Maquettes Suivi Ascend</title><meta name="claude:viewport-fit-sides" content="cover"><style>' + PAGE_CSS + MK_CSS + CSS2 + '</style>']
    body = ['<div class="wrap"><div class="eyebrow">Ascend · chantier interface · D-92</div><h1>Suivi : les questions d\'abord</h1>'
            '<div class="meta">Maquettes du 17 oct. 2026, 2e tour · à valider avant tout code · index.html non modifié</div>'
            '<div class="box"><h3>Ce qui a changé depuis le 1er tour</h3><ul>'
            '<li>L\'écran répond aux questions de D-92 : <b>prêt ?</b> (durée, dénivelé, ventre), <b>tu fais ce qu\'il faut ?</b>, <b>tu encaisses ?</b>, progrès en message ponctuel, temps estimé en lien.</li>'
            '<li>La charge brute et la « zone habituelle » ont disparu.</li>'
            '<li>Chaque bloc finit par un verdict en mots ; un levier quand il y en a un.</li>'
            '<li>Mêmes données que le 1er tour (semaine du 12 oct. supposée faite) ; état « dimanche soir » : sortie longue supposée faite en 1 h 50, 320 m de D+.</li></ul></div>']
    for L, name, idea, shots, shows, leaves in VARIANTS:
        frames = ''.join('<div class="frame">%s</div>%s' % (fn(**kw), '<p class="meta" style="text-align:center">%s</p>' % cap if cap else '') for (nm, fn, kw), cap in zip(shots, ['', 'Durée dépliée', 'Plan déplié', 'Dimanche soir, après la sortie longue'] if L == '1' else ['']))
        body.append('<section id="v%s"><div class="vhead"><span class="vletter">%s</span><h2>%s</h2></div><p class="idea">%s</p>%s<dl><dt>Montre</dt><dd>%s</dd><dt>Laisse</dt><dd>%s</dd></dl></section>' % (L, L, name, idea, frames, shows, leaves))
    body.append(COMPARE + '</div>')
    html = parts[0] + fr_typo(''.join(body))
    if fragment:
        return html
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + html.replace('</style>', '</style></head><body>', 1) + '</body></html>'


COMPARE = """
<section id="reco"><div class="eyebrow">Recommandation</div><h2>1, avec le bilan écrit de 3 en en-tête plus tard</h2>
<p>La variante 1 répond aux 5 questions sur un seul écran et garde tes critères (blocs fins, valeurs à droite, détail qui se déplie). La courbe de ta variante C n'est pas perdue : elle est dans « La durée », là où elle répond à sa question.</p>
<p>J'écarte 2 en tête d'écran : sa courbe ne parle que de la durée, et pousse « Tu fais ce qu'il faut ? » hors du premier écran alors que c'est ton vrai sujet du moment.</p>
<p>3 est la plus utile à terme, mais c'est la plus risquée : trois phrases fausses font plus de dégâts que trois chiffres. À ajouter au-dessus de 1 une fois les règles H-53 à H-55 éprouvées sur tes vraies semaines.</p>
<div class="box warn"><h3>Ce que ces maquettes révèlent</h3><ul>
<li><b>Tout est vert</b> alors que tu n'as presque pas couru depuis 4 semaines. C'est exact (il reste 49 semaines et le plan rattrape), mais ça doit se lire : « dans les temps » ne veut pas dire « tout va bien ». D'où le verdict orange sur la régularité.</li>
<li><b>Ta durée « tenue » est la sortie déclarée du 6 sept. (1 h 47)</b>, pas ce que tu as fait depuis (30 min). C'est le point ouvert de D-92 (f) : à trancher avant de coder.</li>
<li><b>« Tu encaisses ? » reste muet</b> tant que 4 endurances ne sont pas notées. Avec une endurance par semaine, il faudra environ un mois.</li></ul></div>
</section>
<section id="sources"><div class="eyebrow">Sources</div>
<p class="src">Hoffman et Fogard, IJSPP 2011 (nausées et vomissements, 23 % des abandons sur 161 km) · Corrion et al., PLoS ONE 2018 (sentiment d'efficacité et abandon en ultra-trail) · Frandsen et al., BJSM 2025 (règle des 30 jours, S-BLE-004).</p></section>
"""

if __name__ == '__main__':
    open(os.path.join(HERE, 'suivi2.html'), 'w', encoding='utf-8').write(page())
    if '--fragment' in sys.argv:
        open(sys.argv[sys.argv.index('--fragment') + 1], 'w', encoding='utf-8').write(page(fragment=True))
    from playwright.sync_api import sync_playwright
    d = os.path.join(HERE, 'suivi2'); os.makedirs(d, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 420, 'height': 2600}, device_scale_factor=2)
        for L, name, idea, shots, shows, leaves in VARIANTS:
            for nm, fn, kw in shots:
                f = os.path.join(d, nm + '.html')
                open(f, 'w', encoding='utf-8').write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>body{margin:0;background:#fff}#cnv{padding:14px;display:inline-block;background:#fff}' + MK_CSS + CSS2 + '</style></head><body><div id="cnv">' + fr_typo(fn(**kw)) + '</div></body></html>')
                pg.goto('file://' + f); pg.wait_for_timeout(120)
                pg.locator('#cnv').screenshot(path=os.path.join(d, nm + '.png')); os.remove(f); print('ok', nm)
        b.close()
