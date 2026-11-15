"""Lot « bilan 2 » (15/11/2026) : texte de dérive, saisie en 3 étapes, effet sur le plan, « Pour comprendre » structuré.
Chiffres d'exemple : séance du 15/11 (1 h 15 faite, 37 min prévues, plus longue du mois 1 h). À confirmer par le moteur.
python3 render.py screens_bilan2
"""
from base import *

X = r"""
body{background:var(--bg)}
.canvas{background:var(--bg)}
.fr{width:360px;margin-bottom:18px}
.cd{background:var(--card);border-radius:20px;box-shadow:var(--shadow);padding:4px 14px}
.cd.p{padding:14px}
.cas{font:700 12.5px/1.3 Inter,Roboto,sans-serif;color:#33413a;margin:0 4px 8px;display:flex;gap:7px;align-items:flex-start}
.cas b{background:var(--deep);color:#fff;border-radius:6px;padding:2px 7px;flex:none}
.sec{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mintT);margin:20px 4px 8px}
.msg{display:flex;gap:10px;font-size:14px;line-height:1.5;padding:10px 0;border-top:1px solid var(--line)}
.msg:first-child{border-top:0}
.msg i{flex:none;width:20px;height:20px;border-radius:50%;margin-top:1px;display:flex;align-items:center;justify-content:center;font-weight:800;font-style:normal;font-size:12px}
.msg i.w{background:var(--sunBg);color:var(--sunT)}.msg i.o{background:var(--mintBg);color:var(--mintT)}.msg i.g{background:transparent;box-shadow:inset 0 0 0 1.5px var(--line);color:var(--mut)}
.kv{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:10px 0;border-top:1px solid var(--line);font-size:14.5px}
.kv:first-child{border-top:0}
.kv span{color:var(--mut)}.kv b{font-weight:700;text-align:right}
.kv small{font-weight:500;color:var(--mut);font-size:12.5px}.kv small .lk{color:var(--mintT);font-weight:700}
.steps{display:flex;gap:6px;margin:12px 0 2px}
.steps i{flex:1;height:4px;border-radius:2px;background:#dfe6e0}
.steps i.on{background:var(--mintT)}
.stepl{font-size:12px;color:var(--mut);font-weight:700;margin-top:6px}
.det{border-top:1px solid var(--line);padding:12px 0}
.det:first-child{border-top:0}
.det .h{display:flex;justify-content:space-between;align-items:center;font-size:14.5px;font-weight:700}
.det .h span{color:var(--mut);font-size:18px;font-weight:400;line-height:1}
.det p{margin:7px 0 0;font-size:13.5px;line-height:1.5;color:var(--ink)}
.det p.c{color:var(--mut);font-size:12.5px}
.tb{margin-top:8px}
.tb div{display:flex;justify-content:space-between;font-size:13.5px;padding:7px 0;border-top:1px dashed var(--line)}
.tb b{font-weight:700;text-align:right}.tb span{padding-right:10px;color:var(--mut)}
.src{font-size:11.5px;color:var(--mut);line-height:1.5;margin:10px 4px 0}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.tile{background:var(--card);border-radius:18px;box-shadow:var(--shadow);padding:11px 14px}
.tile small{display:block;font-size:12px;color:var(--mut)}
.tile b{font-size:21px;font-weight:800;letter-spacing:-.02em}
.tile b span{font-size:13px;font-weight:500;color:var(--mut)}
.l1{font-size:15px;line-height:1.45;font-weight:600}
.l1 b{font-weight:800;color:var(--mintT)}
.l2{font-size:13.5px;color:var(--mut);line-height:1.5;margin-top:6px}
.ok{display:flex;gap:10px;align-items:center;font-size:15px;line-height:1.4;font-weight:700}
.ok i{flex:none;width:26px;height:26px;border-radius:50%;background:var(--mintBg);color:var(--mintT);display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:800}
.sheetb{position:absolute;left:0;right:0;top:44px;bottom:0;background:var(--bg);border-radius:26px 26px 0 0;overflow:hidden}
.pad{padding:8px 14px 0}
.wicon{width:44px;height:44px;border-radius:14px;background:var(--mintBg);color:var(--mintT);display:flex;align-items:center;justify-content:center;flex:none}
.or{display:flex;align-items:center;gap:10px;color:var(--mut);font-size:12.5px;font-weight:700;margin:16px 0}
.or:before,.or:after{content:"";flex:1;height:1px;background:#dfe6e0}
.btn.sec{text-transform:none;letter-spacing:0;font-size:15.5px;font-weight:700;margin:0;color:var(--ink)}
.n{background:var(--card);box-shadow:inset 0 0 0 1.5px #dfe6e0}
.xb{width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-size:24px;color:var(--mut)}
.lk{color:var(--mintT);font-weight:700}
.pl{display:inline-block;min-width:38px;text-align:center;border-radius:7px;padding:1px 4px;font-weight:700}
.pl.hi{background:#faeeda;color:#633806}.pl.lo{background:#e1f5ee;color:#085041}
.tr{display:grid;grid-template-columns:minmax(0,1fr) 44px 48px 44px;gap:8px;align-items:center;font-size:14px;padding:9px 0;border-top:1px solid var(--line)}
.tr:first-child{border-top:0;font-size:11.5px;color:var(--mut)}
.tr small{display:block;font-size:12px;color:var(--mut)}
.foot{background:linear-gradient(transparent,var(--bg) 22%)}
"""

WATCH = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="3"/><path d="M9 6l.6-3h4.8L15 6M9 18l.6 3h4.8l.6-3M12 10v2.5l1.5 1"/></svg>'


import re
def nb(h):
    h = re.sub(r'(\d) h (\d\d)', '\\1\u00a0h\u00a0\\2', h)
    h = re.sub(r'(\d) (h|min|km|m|bpm|%|nov\.|coureurs)(?![a-zA-Z])', '\\1\u00a0\\2', h)
    return h.replace('5 200', '5\u00a0200')


def page(inner, theme='light', tag=None, reco=False, w=360, h=760):
    t = '<div class="tag"><b>%s</b>%s</div>' % tag if tag else ''
    return nb('<!doctype html><html data-theme="%s"><head><meta charset="utf-8"><style>%s%s</style></head><body><div class="canvas">%s<div class="phone" style="width:%dpx;height:%dpx">%s</div></div></body></html>' % (theme, CSS, X, t, w, h, inner))


def doc(inner, w=392):
    return nb('<!doctype html><html data-theme="light"><head><meta charset="utf-8"><style>%s%s</style></head><body><div class="canvas" style="width:%dpx">%s</div></body></html>' % (CSS, X, w, inner))


def title(n, t):
    return '<div class="tag"><b>%s</b>%s</div>' % (n, t)


def cas(k, t):
    return '<div class="cas"><b>%s</b><span>%s</span></div>' % (k, t)


def msg(sym, txt):
    c = {'!': 'w', '✓': 'o', 'i': 'g'}[sym]
    return '<div class="msg"><i class="%s">%s</i><span>%s</span></div>' % (c, sym, txt)


DER = 'Dérive cardiaque : à allure égale (pente corrigée), ta FC monte en 2e partie (161 → 165). '



def card(inner, cls=''):
    return '<div class="cd %s">%s</div>' % (cls, inner)


# ---------- 1. Texte de dérive ----------
def b2_derive():
    h = title('1', 'Dérive cardiaque : deux textes')
    h += cas('A', 'Sortie plus longue que ta plus longue du mois : la cause est lisible')
    h += '<div class="fr">' + card(msg('!', DER + '<b>Cause la plus probable : une durée encore nouvelle pour toi</b> (1 h 15, contre 1 h au plus ce mois-ci).')) + '</div>'
    h += cas('B', 'Tous les autres cas : le constat, sans cause devinée')
    h += '<div class="fr" style="margin-bottom:4px">' + card(msg('i', DER + 'Une seule sortie ne dit pas pourquoi : à suivre sur les prochaines.')) + '</div>'
    return doc(h)


# ---------- 2. Saisie en 3 étapes ----------
def steps(n):
    lab = ['Source', 'Confirmation', 'Bilan'][n - 1]
    return '<div class="steps">' + ''.join('<i class="%s"></i>' % ('on' if i <= n else '') for i in (1, 2, 3)) + '</div><div class="stepl">Étape %d sur 3 · %s</div>' % (n, lab)


def head(t, sub=''):
    return ('<div class="sb" style="align-items:center;padding:0 4px"><div><div class="ttl" style="font-size:21px">%s</div>%s</div>'
            '<div class="xb">×</div></div>') % (t, '<div class="meta">%s</div>' % sub if sub else '')


BEHIND = '<div class="halo"><i class="a"></i><i class="b"></i></div><div class="dim"></div>'


def b2_saisie1():
    s = ('<div class="sheetb"><div class="grab"></div><div class="pad">' + head('Nouvelle séance') + '<div style="padding:0 4px">' + steps(1) + '</div>'
         + '<div class="sec">Séance détectée sur ta montre</div>'
         + card('<div class="row"><div class="wicon">' + WATCH + '</div>'
         '<div style="min-width:0"><div style="font-weight:800;font-size:16px">Lozanne Trail</div><div class="mini">Course à pied · aujourd\'hui, 14 h 52</div></div></div>'
         '<div style="margin-top:8px"><div class="kv"><span>Durée</span><b>1 h 15</b></div><div class="kv"><span>Distance</span><b>11,6 km</b></div>'
         '<div class="kv"><span>D+</span><b>180 m</b></div><div class="kv"><span>FC moyenne</span><b>160 bpm</b></div></div>'
         '<div class="btn pri" style="margin-top:8px">Utiliser</div>', 'p')
         + '<div class="mini" style="margin:10px 4px 0;display:flex;justify-content:space-between"><span>Lu il y a 2 min</span><span class="lk">Actualiser</span></div>'
         '<div class="or">ou</div>'
         '<div class="btn sec" style="background:var(--chip);box-shadow:none">Saisir à la main</div>'
         '<div class="mini" style="margin-top:8px;text-align:center">Sans montre, ou pour une autre activité (renforcement, vélo…).</div>'
         '</div></div>')
    return page(BEHIND + s, 'light', ('2a', 'Saisie, étape 1 : la source'), h=700)


def rpe10(sel):
    return '<div class="grid5">' + ''.join('<div class="n%s" style="height:42px">%d</div>' % (' on' if i == sel else '', i) for i in range(1, 11)) + '</div>'


def b2_saisie2():
    s = ('<div class="sheetb"><div class="grab"></div><div class="pad">' + head('Lozanne Trail', 'Course à pied · aujourd\'hui, 14 h 52') + '<div style="padding:0 4px">' + steps(2) + '</div>'
         + '<div class="sec">Lu sur ta montre</div>'
         + card('<div class="kv"><span>Durée</span><b>1 h 15</b></div><div class="kv"><span>Distance · D+</span><b>11,6 km · 180 m</b></div>'
         '<div class="kv"><span>FC moyenne · max</span><b>160 · 172 bpm</b></div>'
         '<div class="kv"><span>Compte pour</span><b>Endurance prévue<br><small>37 min, aujourd\'hui · <span class="lk">Changer</span></small></b></div>')
         + '<div class="mini" style="margin:8px 4px 0">Une donnée est fausse ? <span class="lk">Corriger</span></div>'
         '<div class="sec">Ta perception</div>'
         + card('<div class="lbl" style="margin-top:0"><span>Effort ressenti</span><small>toute la séance, 30 min après</small></div>' + rpe10(3)
         + '<div class="mini" style="margin-top:7px;display:flex;justify-content:space-between"><span>1 très facile</span><b style="color:var(--mintT)">3 · modéré</b><span>10 maximal</span></div>'
         '<div class="f" style="margin-top:16px">Note (facultative)</div><div class="field" style="height:64px;align-items:flex-start;padding-top:11px"><span class="ph">sensations, terrain, météo…</span></div>', 'p')
         + '</div><div class="foot"><div class="btn pri">Valider</div><div class="btn ghost">Retour</div></div></div>')
    return page(BEHIND + s, 'light', ('2b', 'Saisie, étape 2 : confirmation'), h=900)


EFF_SAUT = card('<div class="l1">Prochaine sortie longue, dim. 22 nov. : <b>1 h 15</b> au lieu de 1 h 05.</div>'
                '<div class="l2">Ta sortie dépasse de 25 % ta plus longue du mois. Le plan limite à +10 % l\'évolution de ta plus longue sortie : c\'est un garde-fou pour limiter le risque de blessure.</div>'
                '<div class="l2" style="font-style:italic;border-top:1px solid var(--line);padding-top:9px;margin-top:10px">« L\'entraînement trail est loin d\'être mathématique, car les transformations physiologiques et mentales sont longues. » <span style="font-style:normal">Éric Lacroix</span></div>', 'p')


def trow(l, m, a, e, fc, hi):
    return '<div class="tr"><span>%s<small>%s min</small></span><span>%s</span><span>%s</span><span><span class="pl %s">%d</span></span></div>' % (l, m, a, e, 'hi' if hi else 'lo', fc)


def b2_saisie3():
    s = ('<div class="sheetb"><div class="grab"></div><div class="pad">' + head('Séance enregistrée', 'Endurance · 1 h 15 · 11,6 km · 180 m D+') + '<div style="padding:0 4px">' + steps(3) + '</div>'
         + '<div class="tiles" style="margin-top:14px">'
         '<div class="tile"><small>FC stabilisée</small><b>161 <span>bpm</span></b><small>facile ≤ 159</small></div>'
         '<div class="tile"><small>Hors allure facile</small><b style="color:var(--sunT)">55 %</b><small>du temps</small></div>'
         '<div class="tile"><small>Effort ressenti</small><b>3 <span>/10</span></b><small>modéré</small></div>'
         '<div class="tile"><small>Vitesse de montée</small><b>520 <span>m/h</span></b><small>sur les montées</small></div></div>'
         + '<div class="cd" style="margin-top:8px"><div class="det"><div class="h">Par km<span style="font-size:13px;font-weight:500">5:05 à 8:54 /km &nbsp;⌄</span></div></div></div>'
         + '<div class="sec">Terrain</div>'
         + card('<div class="tr"><span>Allure en /km</span><span>Réelle</span><span>Éq. plat</span><span>FC</span></div>'
                + trow('Montée', 15, '9:26', '6:17', 160, 1) + trow('Faux plat montant', 10, '6:30', '5:54', 163, 1) + trow('Plat', 27, '6:10', '6:09', 162, 1)
                + trow('Faux plat descendant', 10, '5:49', '6:31', 156, 0) + trow('Descente', 13, '5:11', '–', 152, 0))
         + '<div class="sec">Les constats d\'Ascend</div>'
         + card(msg('!', 'Ta FC a travaillé plus que ton ressenti : 55 % du temps au-dessus de ton allure facile.')
                + msg('i', 'Plus long que prévu (+103 %).')
                + msg('!', 'Dérive cardiaque : ta FC monte en 2e partie (161 → 165). Cause la plus probable : une durée encore nouvelle pour toi.'))
         + '<div class="sec">Effet sur le plan</div>' + EFF_SAUT
         + '<div class="sec">L\'analyse</div>'
         '<div class="btn pri">Analyser la séance</div>'
         '<div class="mini" style="margin-top:8px;text-align:center">Rédigée par une IA, seulement si tu appuies.</div>'
         + '<div class="cd" style="margin-top:18px"><div class="det"><div class="h">Pour comprendre<span>⌄</span></div></div></div>'
         '</div></div>')
    return page(BEHIND + s, 'light', ('2c', 'Saisie, étape 3 : le bilan complet, tout de suite'), h=1560)


# ---------- 3. Effet sur le plan ----------
def b2_effet():
    h = title('3', 'Bloc « Effet sur le plan », sous les constats')
    h += cas('A', 'Saut : la séance dépasse la limite (ton cas du 15/11)')
    h += ('<div class="fr">' + EFF_SAUT
          + '<div class="cd" style="margin-top:8px"><div class="det"><div class="h">Le calcul<span>⌃</span></div>'
          '<div style="margin-top:4px"><div class="kv"><span>Ta plus longue du mois</span><b>1 h</b></div>'
          '<div class="kv"><span>Ta sortie d\'aujourd\'hui</span><b>1 h 15 <small>+25 %</small></b></div>'
          '<div class="kv"><span>Retenue comme référence</span><b>1 h 06 <small>+10 % au max</small></b></div>'
          '<div class="kv"><span>Prochaine sortie longue</span><b>1 h 15<br><small>1 h 06 + 10 %, arrondi</small></b></div></div>'
          '<p class="c">Dépasser de plus de 10 % sa plus longue sortie des 30 jours augmente le risque de blessure (étude de 2025, 5 200 coureurs). Le plafonnement de la référence est une convention de l\'appli, pas un résultat de l\'étude.</p></div></div></div>')
    h += cas('B', 'Progression normale : plus longue, mais dans la limite')
    h += ('<div class="fr">' + card('<div class="l1">Prochaine sortie longue, dim. 22 nov. : <b>1 h 10</b> au lieu de 1 h 05.</div>'
          '<div class="l2">Nouvelle plus longue sortie du mois (1 h 04), dans la limite de +10 % : règle des 30 jours.</div>', 'p') + '</div>')
    h += cas('C', 'Rien ne change')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="ok"><i>✓</i><span>Séance dans les clous : ton plan continue comme prévu.</span></div>'
          '<div class="l2" style="margin-left:36px">Prochaine sortie longue : 1 h 05, dim. 22 nov.</div>', 'p') + '</div>')
    return doc(h)


# ---------- 4. Pour comprendre ----------
def det(t, body='', op=False):
    return '<div class="det"><div class="h">%s<span>%s</span></div>%s</div>' % (t, '⌃' if op else '⌄', body if op else '')


def b2_comprendre():
    pente = ('<p>Mesurée sur 200 m (100 m avant, 100 m après), pour gommer les erreurs d\'altitude de la montre.</p>'
             '<div class="tb"><div><span>Montée</span><b>plus de +3 %</b></div><div><span>Faux plat montant</span><b>+1 à +3 %</b></div>'
             '<div><span>Plat</span><b>−1 à +1 %</b></div><div><span>Faux plat descendant</span><b>−1 à −3 %</b></div><div><span>Descente</span><b>moins de −3 %</b></div></div>'
             '<p class="c">Seuils : convention de l\'appli.</p>')
    derive = ('<p>On compare la 1re et la 2e moitié de la sortie, sans les 10 premières minutes ni les descentes.</p>'
              '<div class="tb"><div><span>FC qui monte, à allure égale</span><b>dérive cardiaque</b></div><div><span>Allure qui chute, FC qui baisse</span><b>fatigue des jambes</b></div></div>'
              '<p>Une dérive peut venir d\'une durée nouvelle pour toi, de la chaleur ou d\'un manque d\'eau. Une seule sortie ne permet pas de trancher.</p>'
              '<p class="c">Signalée au-delà de 5 % d\'écart, si la sortie fait au moins 40 min utiles (conventions).</p>')
    h = title('4', '« Pour comprendre » en blocs repliables')
    h += ('<div class="fr" style="margin-bottom:10px"><div class="sec" style="margin-top:4px">Pour comprendre</div>'
          + card(det('Pente', pente, True) + det('Allure équivalente plat') + det('Dérive cardiaque', derive, True) + det('Vitesse de montée') + det('Limites des mesures'))
          + '<div class="src">Sources : Minetti et al., 2002 (coût de la pente, mesures sur tapis) · Coyle et González-Alonso, 2001 (dérive cardiaque).</div></div>')
    h += cas('·', 'Les 3 autres blocs, une fois ouverts')
    h += ('<div class="fr" style="margin-bottom:4px">'
          + card(det('Allure équivalente plat', '<p>L\'allure qui coûterait la même énergie sur du plat. Elle permet de comparer une montée et un plat.</p><p class="c">Pas donnée en descente : là, ce sont la technique et les muscles qui limitent, pas l\'énergie.</p>', True)
          + det('Vitesse de montée', '<p>Les mètres montés par heure, sur les seules montées. Elle mesure ta capacité à grimper.</p>', True)
          + det('Limites des mesures', '<p>La FC au poignet est moins fiable qu\'une ceinture. L\'altitude de la montre varie de quelques mètres.</p><p>Une seule séance ne prouve rien : regarde la tendance sur plusieurs semaines.</p>', True))
          + '</div>')
    return doc(h)


EXPORT = ['b2_derive', 'b2_saisie1', 'b2_saisie2', 'b2_saisie3', 'b2_effet', 'b2_comprendre']
