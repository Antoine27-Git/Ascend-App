"""Pastille de la semaine quand un jour a deux séances (27/11/2026). python3 render.py screens_pastille"""
from screens_renfo import *
import screens_bilan2 as B2
B2.X = B2.X + r"""
.wk3{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;margin-top:10px;text-align:center}
.wk3>div{display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 0 7px;border-radius:14px}
.wk3 .l{font-size:11.5px;color:var(--mut);font-weight:700}.wk3 .nm{font-size:15px;font-weight:800}
.wk3 .on{box-shadow:inset 0 0 0 1.5px var(--mintT);background:#eefaf3}
.wk3 .d{width:30px;height:30px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--mut);font-weight:800;position:relative}
.wk3 .d .mi{width:18px;height:18px}
.wk3 .ef{background:#dcf7e8;color:#0b8f56}.wk3 .sl{background:#ffeedd;color:#d1601a}.wk3 .cf{background:#ece7fe;color:#6a4fd0}
.wk3 .done{background:var(--mintT);color:#fff}.wk3 .miss{background:#fff;box-shadow:inset 0 0 0 1.5px #c33a32;color:#c33a32}
.wk3 .bdg{position:absolute;right:-9px;top:-8px;width:19px;height:19px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 2px #fff}
.wk3 .bdg .mi{width:12px;height:12px}.wk3 .bdg.miss{background:#fde9e7;box-shadow:0 0 0 2px #fff}
.wk3 .pr{display:flex;gap:2px}.wk3 .pr .d{width:20px;height:28px;border-radius:8px}.wk3 .pr .d .mi{width:14px;height:14px}
.wk3 .st{display:flex;flex-direction:column;gap:2px;height:48px;justify-content:center}.wk3 .st .d{width:30px;height:23px;border-radius:8px}.wk3 .st .d .mi{width:14px;height:14px}
.wk3 .st.one .d{width:30px;height:30px;border-radius:10px}.wk3 .st.one .d .mi{width:18px;height:18px}
.lg{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--mut);margin-top:10px}.lg i{display:inline-block;width:12px;height:12px;border-radius:4px;vertical-align:-1px;margin-right:4px}
"""
R, F, T = ic('run'), ic('fitness'), ic('terrain')
def cell(l, n, inner, on=False):
    return '<div class="%s"><span class="l">%s</span><span class="nm">%s</span>%s</div>' % ('on' if on else '', l, n, inner)
def one(c, i): return '<span class="d %s">%s</span>' % (c, i)
def week(mode):
    if mode == 'A':
        tue = '<span class="d done">%s<span class="bdg miss">%s</span></span>' % (R, F)
        fri = '<span class="d ef">%s<span class="bdg cf" style="background:#ece7fe;color:#6a4fd0">%s</span></span>' % (R, F)
        w = lambda x: x
    elif mode == 'B':
        tue = '<span class="pr">' + one('done', R) + one('miss', F) + '</span>'
        fri = '<span class="pr">' + one('ef', R) + one('cf', F) + '</span>'
        w = lambda x: x
    else:
        tue = '<span class="st">' + one('done', R) + one('miss', F) + '</span>'
        fri = '<span class="st">' + one('ef', R) + one('cf', F) + '</span>'
        w = lambda x: '<span class="st one">' + x + '</span>'
    dot = '<span class="d">·</span>'
    return ('<div class="wk3">' + cell('L', 23, w(dot)) + cell('M', 24, tue) + cell('M', 25, w(dot)) + cell('J', 26, w(dot))
            + cell('V', 27, fri, True) + cell('S', 28, w(dot)) + cell('D', 29, w(one('sl', T))) + '</div>')
def bloc(mode, t, sub):
    return (cas(mode, t) + '<div class="fr">' + card('<div class="sb"><div class="h2">Cette semaine</div><div class="mini">1/5 séances</div></div>' + week(mode)
            + '<div class="mini" style="margin-top:8px">' + sub + '</div>', 'p') + '</div>')
def p1():
    h = title('1', 'Deux séances le même jour : trois façons de l\'afficher')
    h += '<div class="mini" style="margin:0 4px 6px">Exemple : mardi, endurance faite et renforcement pas fait. Vendredi (aujourd\'hui), footing et renforcement à venir.</div>'
    h += bloc('A', 'Pastille (actuel), en rouge si pas faite', 'Le plus compact. La pastille reste petite : le rouge se voit, mais le logo est minuscule.')
    h += bloc('B', 'Les deux logos côte à côte', 'Chaque séance a sa case et sa couleur. Les cases sont plus étroites : ça reste lisible sur ton téléphone, plus serré sur un petit écran.')
    h += bloc('C', 'L\'un au-dessus de l\'autre', 'Le plus lisible. La bande de la semaine devient un peu plus haute, tous les jours.')
    return B2.doc(h)
EXPORT = ['p1']

def p2():
    h = title('2', 'C ajusté : la bande ne grandit que les semaines où un jour a deux séances')
    dot = '<span class="d">·</span>'
    simple = ('<div class="wk3">' + cell('L', 30, dot) + cell('M', 1, one('ef', R)) + cell('M', 2, dot) + cell('J', 3, one('cf', F))
              + cell('V', 4, one('cf', F), True) + cell('S', 5, dot) + cell('D', 6, one('sl', T)) + '</div>')
    h += cas('1', 'Semaine normale : bande comme aujourd\'hui')
    h += '<div class="fr">' + card('<div class="sb"><div class="h2">Cette semaine</div><div class="mini">0/4 séances</div></div>' + simple, 'p') + '</div>'
    h += cas('2', 'Semaine avec deux séances le même jour : la bande grandit')
    h += '<div class="fr" style="margin-bottom:4px">' + card('<div class="sb"><div class="h2">Cette semaine</div><div class="mini">1/5 séances</div></div>' + week('C'), 'p') + '</div>'
    return B2.doc(h)
EXPORT = ['p1', 'p2']
