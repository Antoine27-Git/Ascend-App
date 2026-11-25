"""Lot « renforcement » (25/11/2026) : un jour à deux séances, déplacer un renforcement, « Pas faite » utile.
python3 render.py screens_renfo
"""
from screens_saisie3 import *
import screens_bilan2 as B2

X4 = r"""
.lst .it{display:flex;align-items:center;gap:12px;padding:12px 0;border-top:1px solid var(--line)}
.lst .it:first-child{border-top:0}
.lst .ico{flex:none;width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center}
.lst .ico .mi{width:22px;height:22px}
.lst .ef{background:#dcf7e8;color:#0b8f56}.lst .cf{background:#ece7fe;color:#6a4fd0}
.lst b{font-size:16px;font-weight:800}.lst .chev{margin-left:auto;color:var(--mut);font-size:20px}
.pill{display:inline-block;font:700 12px/1 Inter,sans-serif;border-radius:999px;padding:5px 9px;background:var(--mintBg);color:var(--mintT);margin-left:6px;vertical-align:2px}
"""
B2.X = B2.X + X4


def s4_1():
    h = title('1', 'Un jour à deux séances : toucher le jour ouvre la liste du jour')
    h += cas('A', 'Tu touches mardi 24 dans « Cette semaine »')
    deux = '<div class="two"><span class="d done">' + ic('run') + '</span><span class="bdg">' + ic('fitness') + '</span></div>'
    h += '<div class="fr">' + card(semaine(jour('M', 24, None, deux, True)), 'p') + '</div>'
    h += cas('B', 'Une petite fenêtre liste les deux séances ; chacune ouvre sa fiche')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="h2">Mardi 24 nov.</div><div class="lst" style="margin-top:6px">'
          '<div class="it"><span class="ico ef">' + ic('run') + '</span><div><b>Endurance</b><span class="pill">Fait</span><div class="mini">37 min · 26 m D+ · effort 4</div></div><span class="chev">›</span></div>'
          '<div class="it"><span class="ico cf">' + ic('fitness') + '</span><div><b>Renforcement</b><div class="mini">45 min · prévu</div></div><span class="chev">›</span></div>'
          '</div>', 'p') + '</div>')
    h += '<div class="mini" style="margin:0 4px">Un jour avec une seule séance ouvre directement sa fiche, comme aujourd\'hui.</div>'
    return B2.doc(h)


def s4_2():
    h = title('2', 'Déplacer un renforcement : le même calendrier que pour une course')
    cal = ('<div class="wk2 pick">'
           + jp('L', 23, '', '·', 'no') + jp('M', 24, 'done', ic('run'), 'no') + jp('M', 25, '', '·', 'sel') + jp('J', 26, '', '·')
           + jp('V', 27, 'cf', ic('fitness')) + jp('S', 28, '', '·') + jp('D', 29, 'sl', ic('terrain')) + '</div>')
    h += cas('A', 'Fiche du renforcement de vendredi : « Déplacer cette séance », tu touches mercredi')
    h += ('<div class="fr">' + card('<div class="h2">Déplacer cette séance</div><div class="mini" style="margin-top:6px">Un autre jour de cette semaine. Touche le jour voulu.</div>'
          + cal + '<div class="res"><b>Aujourd\'hui</b> : jour libre.</div><div class="btn pri" style="margin-top:12px">Déplacer à aujourd\'hui</div>', 'p') + '</div>')
    h += cas('B', 'Ce que dit la ligne selon le jour choisi')
    h += ('<div class="fr" style="margin-bottom:4px">' + card(
          '<div class="res" style="border-top:0;margin-top:0;padding-top:0"><b>Samedi</b> : veille de ta sortie longue. Fais-le sans jambes lourdes (haut du corps, gainage).</div>'
          '<div class="res"><b>Dimanche</b> : le jour de ta sortie longue. Possible, mais après la sortie.</div>'
          '<div class="res"><b>Jeudi</b> : jour libre.</div>'
          '<div class="res"><b>Un jour de course</b> : avec ta course. Possible, les deux le même jour.</div>', 'p') + '</div>')
    h += '<div class="mini" style="margin:0 4px">Même règle que pour une course : seulement dans la semaine en cours. Deux renforcements ne se mettent pas le même jour.</div>'
    return B2.doc(h)


def s4_3():
    h = title('3', '« Pas faite » sur un renforcement : deux choix utiles, un seul appui')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="h2">Renforcement pas fait</div><div class="mini" style="margin-top:4px">mar. 24 nov. · 45 min</div>'
          '<div class="opt" style="margin-top:14px;background:var(--card);border-radius:14px;box-shadow:var(--shadow);padding:12px 14px"><b>La faire un autre jour</b><div class="mini">Ouvre le calendrier de la semaine.</div></div>'
          '<div class="opt" style="margin-top:10px;background:var(--card);border-radius:14px;box-shadow:var(--shadow);padding:12px 14px"><b>Je ne la ferai pas cette semaine</b><div class="mini">Noté tout de suite. Ton plan de course n\'est pas modifié.</div></div>', 'p') + '</div>')
    h += '<div class="mini" style="margin:0 4px">S\'il n\'y a plus aucun jour possible dans la semaine, la fenêtre ne s\'ouvre pas : « Pas faite » est noté directement.</div>'
    return B2.doc(h)


EXPORT = ['s4_1', 's4_2', 's4_3']
