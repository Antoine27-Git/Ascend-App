"""Bibliothèque (25/11/2026) : articles et études, classés par thème, avec niveau de preuve et lien vers les règles d'Ascend.
python3 render.py screens_biblio
"""
from screens_sauvegarde import *
import screens_bilan2 as B2

X7 = r"""
.chips2{display:flex;gap:7px;overflow:hidden;margin:10px 0 4px}
.chips2 span{flex:none;background:var(--chip);border-radius:999px;padding:8px 12px;font-size:13.5px;font-weight:700;white-space:nowrap}
.chips2 .on{background:var(--deep);color:#fff}
.art{background:var(--card);border-radius:18px;box-shadow:var(--shadow);padding:13px 14px;margin-top:10px}
.art .t{font-size:16px;font-weight:800;line-height:1.3}
.art .src{font-size:12.5px;color:var(--mut);margin-top:3px}
.art .ret{font-size:14px;line-height:1.45;margin-top:7px}
.lvl{display:inline-block;font:800 11px/1 Inter,sans-serif;border-radius:6px;padding:4px 7px;margin-right:6px;vertical-align:1px}
.lvl.e{background:#dcf7e8;color:#0b8f56}.lvl.x{background:#e0edfd;color:#2c6fb8}.lvl.n{background:#f1eee6;color:#7a6d52}
.use{display:inline-block;font-size:12.5px;font-weight:700;color:var(--mintT);margin-top:8px}
.nav5{position:absolute;left:12px;right:12px;bottom:12px;background:#fff;border-radius:22px;box-shadow:0 6px 20px rgba(16,32,26,.12);display:grid;grid-template-columns:repeat(5,1fr);gap:2px;padding:8px 6px}
.nav5 div{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10px;letter-spacing:-.15px;white-space:nowrap;padding-left:3px!important;padding-right:3px!important;font-weight:700;color:var(--mut);padding:6px 0;border-radius:14px}
.nav5 .mi{width:21px;height:21px}
.nav5 .on{background:#e3f5ec;color:var(--mintT)}
.dt h2{font-size:22px;font-weight:800;line-height:1.25;margin:6px 0 4px;letter-spacing:-.01em}
.dt p{font-size:15px;line-height:1.5;margin:8px 0}
.box{background:var(--card);border-radius:16px;box-shadow:var(--shadow);padding:12px 14px;margin-top:12px}
.box b.h{display:block;font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT);margin-bottom:6px}
"""
B2.X = B2.X + X7

BOOK = '<svg class="mi" style="fill:none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.5C10.2 5.2 7.6 4.6 4 4.8v13.4c3.6-.2 6.2.4 8 1.7 1.8-1.3 4.4-1.9 8-1.7V4.8c-3.6-.2-6.2.4-8 1.7z"/><path d="M12 6.5v13.4"/></svg>'


def nav(lab):
    return ('<div class="nav5"><div>' + ic('home') + 'Aujourd\'hui</div><div>' + ic('calendar') + 'Semaine</div><div>' + ic('monitoring') + 'Suivi</div>'
            '<div class="on">' + BOOK + lab + '</div><div>' + ic('person') + 'Profil</div></div>')


NAV = nav('Bibliothèque')


def art(t, src, lvl, ret, use=None):
    L = {'e': 'Étude', 'x': 'Avis d\'expert', 'n': 'Non vérifié'}
    return ('<div class="art"><div class="t">' + t + '</div><div class="src"><span class="lvl ' + lvl + '">' + L[lvl] + '</span>' + src + '</div>'
            '<div class="ret">' + ret + '</div>' + ('<span class="use">Utilisé par Ascend : ' + use + ' ›</span>' if use else '') + '</div>')


def s6_1():
    s = ('<div class="ph"><h1>Bibliothèque</h1><div class="mini">Ce que disent les études, en clair. 24 articles.</div></div>'
         '<div class="chips2"><span class="on">Tout</span><span>Sortie longue</span><span>Descente</span><span>Nutrition</span><span>Cœur</span></div>'
         + art('Augmenter trop vite sa plus longue sortie augmente le risque de blessure', 'Frandsen et al. · BJSM · 2025', 'e',
               'Dépasser de plus de 10 % sa plus longue sortie du mois est lié à plus de blessures. La hausse de la semaine compte moins.', 'règle des 30 jours')
         + art('Les meilleurs ultra-traileurs perdent moins de vitesse en descente en fin de course', 'Genitrini et al. · 2022', 'e',
               'Ce qui sépare les finishers rapides : tenir la descente quand les jambes sont fatiguées.')
         + art('Pourquoi le cœur monte pendant une sortie à allure constante', 'Coyle et González-Alonso · 2001', 'e',
               'La chaleur et la perte d\'eau font monter la fréquence cardiaque même si l\'allure ne change pas.', 'dérive cardiaque')
         + NAV)
    return pg('<div class="pad">' + s + '</div>', ('1', 'Un 5e onglet « Bibliothèque » : des fiches courtes, par thème'), h=900)


def s6_2():
    s = ('<div class="mini" style="padding:6px 4px 0">‹ Bibliothèque</div><div class="dt" style="padding:0 4px">'
         '<div class="src" style="margin-top:8px"><span class="lvl e">Étude</span><span class="mini">Sortie longue · Blessures</span></div>'
         '<h2>Augmenter trop vite sa plus longue sortie augmente le risque de blessure</h2>'
         '<div class="mini">Frandsen et al. · British Journal of Sports Medicine · 2025</div>'
         '<div class="box"><b class="h">Ce qu\'il faut retenir</b>Sur plus de 5 000 coureurs suivis pendant 18 mois, ce qui pèse le plus sur les blessures n\'est pas le volume de la semaine, '
         'mais la plus longue sortie : la dépasser de plus de 10 % par rapport au mois précédent augmente le risque.</div>'
         '<div class="box"><b class="h">Ce que ça change pour toi</b>Ascend ne te fait jamais dépasser ta plus longue sortie du mois de plus de 10 %. '
         'Si tu le fais quand même, le plan n\'en tient compte qu\'à +10 %.</div>'
         '<div class="box"><b class="h">Limites</b>Coureurs sur route, pas en trail. Étude d\'observation : elle montre un lien, pas une preuve de cause.</div>'
         '<div class="btn pri" style="margin-top:14px">Lire l\'article ›</div>'
         '<div class="mini" style="margin-top:8px;text-align:center">Ouvre le site de la revue. Parfois payant : le résumé reste gratuit.</div></div>')
    return pg('<div class="pad">' + s + '</div>', ('2', 'La fiche : ce qu\'il faut retenir, ce que ça change pour toi, les limites'), h=900)


def s6_3():
    h = title('3', 'La barre du bas : textes à 10 px (11 avant), « Bibliothèque » tient dans le fond vert')
    for lab in ['Bibliothèque']:
        h += cas('·', lab) + '<div class="fr" style="position:relative;height:84px;margin-bottom:6px">' + nav(lab) + '</div>'
    return B2.doc(h)


EXPORT = ['s6_1', 's6_2', 's6_3']
