"""Suivi, 3e tour (03/11/2026) : « Prêt pour le jour J ? » compare le réel au plan à la date du jour.

Retour d'Antoine sur la v49 : « la forme est bien, le fond est mauvais » — « 1 h 47 sur 5 à 6 h » incompréhensible
(sortie déclarée de septembre face à une cible d'entraînement non expliquée), pas de courbe du réel, courbe trop petite,
verdicts sans données (« dans les temps » sans avoir couru), verdict qui répète la question.

Produit suivi3.html et suivi3/*.png. Lancer : cd docs/maquettes && python3 screens_suivi3.py
Données : plan redémarré le lundi 2 nov. 2026 (projection du moteur actuel, sans course dans les 30 jours avant :
1re sortie longue 1 h 16). Trois moments : mardi 3 nov. (semaine 1), jeudi 26 nov. (semaine 4, une sortie longue
manquée), mardi 16 mars 2027 (semaine 20). Les séances réelles des semaines 4 et 20 sont inventées pour l'exemple.
"""
import os, sys, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from base import ic
from screens_suivi import MK_CSS, PAGE_CSS, nav, ln, fr_typo
from screens_suivi2 import CSS2

D = dt.date.fromisoformat
START, GOAL, RACE2 = '2026-11-02', '2027-09-25', '2027-05-08'
# sorties longues prévues à la reprise (moteur, 03/11/2026) : date, minutes, D+
PLAN = [('2026-11-08', 76, 150), ('2026-11-15', 83, 200), ('2026-11-22', 90, 200), ('2026-11-29', 99, 250), ('2026-12-06', 65, 150),
        ('2026-12-13', 108, 250), ('2026-12-20', 118, 300), ('2026-12-27', 129, 350), ('2027-01-03', 85, 250), ('2027-01-10', 140, 400),
        ('2027-01-17', 154, 450), ('2027-01-24', 169, 500), ('2027-01-31', 110, 350), ('2027-02-07', 185, 600), ('2027-02-14', 120, 400),
        ('2027-02-21', 200, 650), ('2027-02-28', 130, 450), ('2027-03-07', 220, 800), ('2027-03-14', 150, 550), ('2027-03-21', 240, 900),
        ('2027-03-28', 155, 600), ('2027-04-04', 264, 1000), ('2027-04-11', 175, 700), ('2027-04-18', 290, 1150), ('2027-04-25', 200, 800),
        ('2027-05-02', 160, 650), ('2027-05-16', 100, 450), ('2027-05-23', 160, 700), ('2027-05-30', 220, 1000), ('2027-06-06', 290, 1350),
        ('2027-06-13', 180, 850), ('2027-06-20', 180, 850), ('2027-06-27', 290, 1400), ('2027-07-04', 180, 900), ('2027-07-11', 319, 1600),
        ('2027-07-18', 180, 900), ('2027-07-25', 350, 1750), ('2027-08-01', 180, 900), ('2027-08-08', 360, 1800), ('2027-08-15', 180, 900),
        ('2027-08-22', 180, 900), ('2027-08-29', 180, 900), ('2027-09-05', 180, 900), ('2027-09-12', 198, 1000), ('2027-09-19', 200, 1000)]
REAL20 = [(d, m, p) for d, m, p in PLAN if d <= '2027-03-14' and d not in ('2026-12-20', '2027-02-07')]
REAL20 = [(d, 200, 650) if d == '2027-03-07' else (d, m, p) for d, m, p in REAL20]
STATES = {
    's1': dict(today='2026-11-03', label='Mardi 3 nov.', wk='Semaine 1 sur 47 · Reprise · J−326', real=[], next=('2026-11-08', 76, 150),
               ventre=None, plan=(1, 1, []), enc=('neu', 'Repère en cours : 0 endurance notée sur 4')),
    's4': dict(today='2026-11-26', label='Jeudi 26 nov.', wk='Semaine 4 sur 47 · Reprise · J−303',
               real=[('2026-11-08', 76, 150), ('2026-11-15', 83, 200)], next=('2026-11-29', 91, 250),
               ventre=None, plan=(9, 11, ['22 nov.']), enc=('neu', 'Repère en cours : 3 endurances notées sur 4')),
    's20': dict(today='2027-03-16', label='Mardi 16 mars', wk='Semaine 20 sur 47 · Base aérobie · J−193', real=REAL20, next=('2027-03-21', 240, 900),
                ventre=(39, 60), plan=(50, 54, ['20 déc.', '7 févr.']), enc=('ok', 'Tu encaisses')),
}


def hm(m):
    h, mn = divmod(int(round(m)), 60)
    return ('%d h %02d' % (h, mn) if mn else '%d h' % h) if h else '%d min' % mn


def level(lst, today):
    v = [m for d, m, p in lst if d <= today]
    return max(v) if v else 0


def levelp(lst, today):
    v = [p for d, m, p in lst if d <= today]
    return max(v) if v else 0


def verdict(real, plan):
    """H à écrire (convention) : ≥ 95 % du prévu à cette date = dans le plan ; 80–95 % = un peu en retard ; < 80 % = en retard."""
    if plan == 0:
        return ('neu', 'à construire')
    r = real / plan
    return ('ok', 'dans le plan') if r >= .95 else ('late', 'un peu en retard') if r >= .8 else ('bad', 'en retard')


def chart(st, h=190, big=True):
    W, x0, x1, yt, yb = 320, 6, 288, 18, h - 22
    t0, t1 = D(START), D(GOAL)
    X = lambda d: x0 + (D(d) - t0).days / (t1 - t0).days * (x1 - x0)
    Y = lambda m: yb - m / 360 * (yb - yt)
    tday = st['today']
    s = '<svg viewBox="0 0 %d %d" width="100%%" role="img" style="display:block;margin-top:10px">' % (W, h)
    s += '<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="#e4f6ec"/>' % (x0, Y(360), x1 - x0, Y(300) - Y(360))
    s += '<text x="%d" y="%.1f" font-size="10" fill="#087a49" font-weight="700">ta plus longue sortie visée</text>' % (x0 + 4, Y(300) + 12)
    for m in (60, 120, 180, 240, 300, 360):
        s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#e9eee9"/>' % (x0, x1, Y(m), Y(m))
        if m % 120 == 0:
            s += '<text x="%d" y="%.1f" font-size="10" fill="#5b6961">%d h</text>' % (x1 + 5, Y(m) + 3.5, m // 60)
    s += '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#c9d1cb"/>' % (x0, x1, yb, yb)
    # prévu : niveau en escalier pointillé
    mx, pts = 0, []
    for d, m, p in PLAN:
        mx = max(mx, m); pts.append((X(d), Y(mx)))
    s += '<path d="M%.1f,%.1f L%s" fill="none" stroke="#087a49" stroke-width="2" stroke-dasharray="5 4" opacity=".75"/>' % (X(START), Y(0), ' L'.join('%.1f,%.1f' % p for p in pts))
    # réel : niveau atteint, trait plein, jusqu'à aujourd'hui
    real = st['real']
    if real:
        mx, rp = 0, [(X(START), Y(0))]
        for d, m, p in real:
            mx = max(mx, m); rp.append((X(d), Y(mx)))
        rp.append((X(tday), Y(mx)))
        s += '<path d="M%s" fill="none" stroke="#d1601a" stroke-width="3" stroke-linejoin="round"/>' % ' L'.join('%.1f,%.1f' % p for p in rp)
        for d, m, p in real:
            s += '<circle cx="%.1f" cy="%.1f" r="2.6" fill="#d1601a"/>' % (X(d), Y(m))
    nd, nm, npl = st['next']
    s += '<circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#087a49" stroke-width="2.4"/>' % (X(nd), Y(nm))
    xt = X(tday)
    s += '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#0f1c16" stroke-dasharray="2 3" opacity=".5"/>' % (xt, xt, yt - 8, yb)
    s += '<text x="%.1f" y="%d" font-size="10" fill="#0f1c16" font-weight="700" text-anchor="%s">auj.</text>' % (xt + (3 if xt < 160 else -3), yt - 8 + 8, 'start' if xt < 160 else 'end')
    for d, lab, anc in ((RACE2, '50 km', 'start'), (GOAL, '★ 80 km', 'end')):
        xx = X(d)
        s += '<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#10251c" stroke-width="1.2"/>' % (xx, xx, yt - 8, yb)
        s += '<text x="%.1f" y="%d" font-size="10" fill="#10251c" font-weight="800" text-anchor="%s">%s</text>' % (xx + (3 if anc == 'start' else -3), yt, anc, lab)
    for d, lab in (('2026-12-01', 'déc.'), ('2027-02-01', 'févr.'), ('2027-04-01', 'avr.'), ('2027-06-01', 'juin'), ('2027-08-01', 'août')):
        s += '<text x="%.1f" y="%d" font-size="10" text-anchor="middle" fill="#5b6961">%s</text>' % (X(d), h - 6, lab)
    s += '</svg><div class="legend"><span><i class="d" style="background:#d1601a;height:3px;border-radius:2px;width:16px"></i>ton réel</span>' \
         '<span><i class="d" style="border-top:2px dashed #087a49;height:0;border-radius:0;width:16px"></i>prévu</span>' \
         '<span><i class="d" style="box-shadow:inset 0 0 0 2px #087a49"></i>prochaine</span></div>'
    return s


CSS3 = r"""
.mk .pt.bad{background:var(--coralT)}
.mk .why{background:#f4f7f4;border-radius:14px;padding:10px 12px;margin-top:10px;font-size:13px;line-height:1.45}
.mk .why b{font-weight:800}
.mk .sum{display:flex;gap:8px;flex-wrap:wrap;padding:2px 0 10px}
.mk .chip2{font-size:12px;font-weight:700;padding:4px 9px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;box-shadow:inset 0 0 0 1px var(--line)}
"""

WHY = ('<div class="why"><b>Pourquoi 5 à 6 h et pas 15 h ?</b> Ta course durera environ 15 h, mais on ne court jamais cette durée à l\'entraînement : '
       'trop de fatigue pour trop peu de gain. La fin de course se prépare en répétant des sorties longues de 5 à 6 h et des week-ends enchaînés, en juillet-août.</div>')


def rows(st, chart_inside):
    t = st['today']
    pl, rl = level(PLAN, t), level(st['real'], t)
    vc, vt = verdict(rl, pl)
    nd, nm, npl = st['next']
    ndl = dt.date.fromisoformat(nd).strftime('%d').lstrip('0')
    mois = {'11': 'nov.', '12': 'déc.', '01': 'janv.', '02': 'févr.', '03': 'mars'}[nd[5:7]]
    first = not st['real']
    dur_val = 'aucune' if first else hm(rl)
    dur_small = 'dim. : %s' % hm(nm) if first else 'prévu %s' % hm(pl)
    dur_body = ((chart(st) if chart_inside else '')
                + ln('Ta plus longue depuis la reprise', dur_val, '' if first else 'sortie longue, même terrain qu\'en course', True)
                + ln('Prévu à cette date', hm(pl) if pl else '—', 'niveau que le plan visait')
                + ln('Prochaine', hm(nm), 'dimanche %s %s' % (ndl, mois))
                + ln('Visée', '5 h à 6 h', 'ta plus longue sortie, juillet-août')
                + (ln('Avant la reprise', '1 h 47', 'déclarée le 6 sept.') if first else '') + WHY)
    pp, rp = levelp(PLAN, t), levelp(st['real'], t)
    dc, dtv = verdict(rp, pp)
    dpl_body = (ln('Ton plus gros D+ en une sortie', '%d m' % rp if rp else 'aucun', '', True) + ln('Prévu à cette date', '%d m' % pp if pp else '—')
                + ln('Prochaine', '≈ %d m' % npl, 'avec ta sortie longue') + ln('Visé', '≈ 1 800 m', 'sur ta plus longue sortie, août')
                + '<div class="note">Ta course : 4 500 m de D+. Le D+ de tes sorties longues monte avec leur durée.</div>')
    if st['ventre']:
        v, vp = st['ventre']
        vc2, vt2 = verdict(v, vp)
        ventre = ('Ton ventre', vt2, vc2, '%d g/h' % v, 'prévu %d g/h' % vp,
                  ln('Toléré sur ta dernière sortie nourrie', '%d g/h' % v, '', True) + ln('Prévu à cette date', '%d g/h' % vp, '+6 g/h par semaine bien digérée')
                  + ln('Visé en course', '60 à 90 g/h') + '<div class="note">Nausées et vomissements : première cause d\'abandon sur 160 km. Mange à chaque sortie de plus de 1 h 30.</div>')
    else:
        ventre = ('Ton ventre', 'à construire', 'neu', 'pas commencé', 'dès 1 h 30 de sortie',
                  ln('Toléré', '—', 'aucune sortie nourrie saisie', True) + ln('Visé en course', '60 à 90 g/h')
                  + '<div class="note">Le plan te demandera de manger dès que tes sorties dépasseront 1 h 30 : c\'est ce qui entraîne ton ventre.</div>')
    return [('duree', 'terrain', 's', 'Ta sortie longue', vt if not first else 'à construire', vc if not first else 'neu', dur_val, dur_small, dur_body),
            ('dplus', 'terrain', 'k', 'Ton dénivelé', dtv if not first else 'à construire', dc if not first else 'neu', '%d m' % rp if rp else 'aucun', ('prévu %d m' % pp) if pp else 'dim. : %d m' % npl, dpl_body),
            ('ventre', 'nutrition', 'c') + ventre]


def brick(k, icon, cls, title, verdict_, vcls, val, small, body, open_, first):
    return ('<details class="brk%s"%s><summary><span class="qi %s">%s</span><span class="bt"><b>%s</b><span><i class="pt %s"></i>%s</span></span>'
            '<span class="bv"><span><b>%s</b><small>%s</small></span><i class="chev">⌄</i></span></summary><div class="qb">%s</div></details>') % (
        ' first' if first else '', ' open' if open_ else '', cls, ic(icon), title, vcls, verdict_, val, small, body)


def plan_card(st):
    f, n, miss = st['plan']
    vc = 'late' if miss else ('neu' if n <= 1 else 'ok')
    vt = ('%s manquée%s : %s' % ('sortie longue' if len(miss) == 1 else '%d sorties longues' % len(miss), '' if len(miss) == 1 else 's', ', '.join(miss))) if miss else ('rien de manqué' if n > 1 else '1re séance faite')
    lev = ('<div class="lever">Ne rattrape pas<span>dimanche : la sortie prévue, pas plus</span></div>' if miss else '')
    enc_c, enc_t = st['enc']
    return ('<div class="card"><details class="first brk"><summary><span class="qi c">%s</span><span class="bt"><b>Tu suis le plan ?</b><span><i class="pt %s"></i>%s</span></span>'
            '<span class="bv"><span><b>%d sur %d</b><small>séances</small></span><i class="chev">⌄</i></span></summary><div class="qb"></div></details>%s'
            '<details class="brk"><summary><span class="qi k">%s</span><span class="bt"><b>Tu encaisses ?</b><span><i class="pt %s"></i>%s</span></span>'
            '<span class="bv"><i class="chev">⌄</i></span></summary><div class="qb"></div></details></div>') % (ic('calendar'), vc, vt, f, n, lev, ic('monitoring'), enc_c, enc_t)


TEMPS = ('<div class="card"><details class="first"><summary><span class="qi c">%s</span><span class="bt"><b>Ton temps estimé</b><span>80 km · 4 500 m D+</span></span>'
         '<span class="bv"><span><b>≈ 15 h</b><small>Ton objectif ›</small></span></span></summary></details></div>') % ic('timer')


def phone(st, variant, open_=()):
    R = rows(st, chart_inside=(variant == 'A'))
    head = '<div class="cardt"><span class="h2">Prêt pour le jour J ?</span><span class="mini">25 sept. 2027</span></div>'
    top = ('<div style="margin-top:-4px">' + chart(st) + '</div>') if variant == 'B' else ''
    bricks = ''.join(brick(*r, open_=(r[0] in open_), first=(i == 0 and variant == 'A')) for i, r in enumerate(R))
    inner = '<div class="card">' + head + top + bricks + '</div>' + plan_card(st) + TEMPS
    return ('<div class="mk phone"><div class="halo"><i class="a"></i><i class="b"></i></div>'
            '<header><h1>Suivi</h1><div class="sub">%s</div></header>' % st['wk'] + inner + nav() + '<div class="fold" aria-hidden="true"></div></div>')


SHOTS = [('B', 's1', ()), ('B', 's4', ()), ('B', 's20', ()), ('B', 's20', ('duree',)), ('A', 's4', ()), ('A', 's4', ('duree',))]


def page(fragment=False):
    head = '<title>Maquettes Suivi Ascend</title><meta name="claude:viewport-fit-sides" content="cover"><style>' + PAGE_CSS + MK_CSS + CSS2 + CSS3 + '</style>'
    b = ['<div class="wrap"><div class="eyebrow">Ascend · chantier interface · D-92, 3e tour</div><h1>Prêt pour le jour J : le réel face au plan</h1>'
         '<div class="meta">Maquettes du 3 nov. 2026 · à valider avant tout code · la v49 en ligne n\'est pas modifiée</div>'
         '<div class="box"><h3>Ce qui change par rapport à la v49</h3><ul>'
         '<li><b>Le chiffre affiché est ton réel depuis la reprise</b>, comparé à ce que le plan prévoyait à la même date. La sortie déclarée de septembre passe dans le détail.</li>'
         '<li><b>Verdict = écart au plan à cette date</b> : dans le plan (≥ 95 % du prévu), un peu en retard (80 à 95 %), en retard (moins de 80 %). « À construire » tant qu\'il n\'y a pas de vraie séance. Convention, à écrire en hypothèse.</li>'
         '<li><b>La courbe montre ton réel</b> (trait plein orange) face au prévu (pointillés), en grand, de la reprise au jour J.</li>'
         '<li><b>La cible est expliquée</b> : pourquoi 5 à 6 h et pas 15 h.</li>'
         '<li><b>Plus de verdict qui répète la question</b> : « Tu suis le plan ? » dit ce qui a été manqué, et quand.</li></ul></div>'
         '<div class="box warn"><h3>Données</h3><p style="margin:0">Plan redémarré le 2 nov. (projection du moteur actuel, sans course dans les 30 jours avant la reprise : 1re sortie longue 1 h 16). '
         'Les séances des semaines 4 et 20 sont inventées pour l\'exemple (une sortie longue manquée le 22 nov. ; deux en hiver ; 3 h 20 au lieu de 3 h 40 le 7 mars).</p></div>']
    b.append('<section id="b"><div class="vhead"><span class="vletter">B</span><h2>Courbe en tête de carte</h2></div><p class="idea">La courbe réel / prévu est visible sans toucher, en haut de « Prêt pour le jour J ? », les trois briques dessous. Recommandée.</p>')
    caps = {('B', 's1', ()): 'Semaine 1, mardi 3 nov. : rien de couru, tout est « à construire ».', ('B', 's4', ()): 'Semaine 4 : une sortie longue manquée.',
            ('B', 's20', ()): 'Semaine 20 : un peu en retard sur la durée, en retard sur le ventre.', ('B', 's20', ('duree',)): 'Semaine 20, « Ta sortie longue » dépliée.'}
    for v, s, o in SHOTS[:4]:
        b.append('<div class="frame">%s</div><p class="meta" style="text-align:center">%s</p>' % (phone(STATES[s], v, o), caps[(v, s, o)]))
    b.append('</section><section id="a"><div class="vhead"><span class="vletter">A</span><h2>Courbe dans le détail</h2></div><p class="idea">Même fond, la courbe n\'apparaît qu\'en dépliant « Ta sortie longue ». Plus compact.</p>')
    for v, s, o in SHOTS[4:]:
        b.append('<div class="frame">%s</div><p class="meta" style="text-align:center">%s</p>' % (phone(STATES[s], v, o), 'Semaine 4, fermée.' if not o else 'Semaine 4, « Ta sortie longue » dépliée.'))
    b.append('</section>' + RECO + '</div>')
    html = head + fr_typo(''.join(b))
    if fragment:
        return html
    return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + html.replace('</style>', '</style></head><body>', 1) + '</body></html>'


RECO = """
<section id="reco"><div class="eyebrow">Recommandation</div><h2>B : la courbe en tête</h2>
<p>Ta remarque sur la courbe était juste : c'est l'élément qui répond le mieux à « où j'en suis ? ». Repliée, personne ne la voit. En tête de carte, elle montre d'un coup d'œil ton réel face au plan, et les trois lignes dessous donnent les chiffres.</p>
<p>Prix à payer : la carte prend plus de hauteur, et « Tu suis le plan ? » descend vers le bas du premier écran.</p>
<div class="box warn"><h3>Ce que la simulation a révélé (hors maquettes)</h3><ul>
<li><b>Une seule course de 30 min dans le mois précédant la reprise fait tomber ta 1re sortie longue de 1 h 16 à 33 min</b>, et place tes deux objectifs en retard : le repère de septembre n'est utilisé que s'il n'y a aucune course dans les 30 jours. C'est le chantier moteur mis de côté (D-92 f) : il pèse plus lourd que prévu.</li>
<li><b>Le seuil « 95 % / 80 % » est une convention</b> à écrire (nouvelle hypothèse), comme les autres verdicts.</li></ul></div>
</section>
"""

if __name__ == '__main__':
    open(os.path.join(HERE, 'suivi3.html'), 'w', encoding='utf-8').write(page())
    if '--fragment' in sys.argv:
        open(sys.argv[sys.argv.index('--fragment') + 1], 'w', encoding='utf-8').write(page(fragment=True))
    from playwright.sync_api import sync_playwright
    d = os.path.join(HERE, 'suivi3'); os.makedirs(d, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': 420, 'height': 2600}, device_scale_factor=2)
        for v, s, o in SHOTS:
            nm = 'suivi3_%s_%s%s' % (v, s, '_' + '_'.join(o) if o else '')
            f = os.path.join(d, nm + '.html')
            open(f, 'w', encoding='utf-8').write('<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>body{margin:0;background:#fff}#cnv{padding:14px;display:inline-block;background:#fff}' + MK_CSS + CSS2 + CSS3 + '</style></head><body><div id="cnv">' + fr_typo(phone(STATES[s], v, o)) + '</div></body></html>')
            pg.goto('file://' + f); pg.wait_for_timeout(120)
            pg.locator('#cnv').screenshot(path=os.path.join(d, nm + '.png')); os.remove(f); print('ok', nm)
        br.close()
