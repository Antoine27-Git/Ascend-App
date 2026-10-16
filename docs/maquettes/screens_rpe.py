from base import *
from screens_v3 import saisie
ANCH = {1: 'Très<br>facile', 3: 'Modéré', 5: 'Dur', 7: 'Très<br>dur', 10: 'Maxi&shy;mal'}
def rpe_block(sel):
    btns = '<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:4px">' + ''.join('<div class="n%s" style="height:42px;font-size:14.5px">%d</div>' % (' on' if i == sel else '', i) for i in range(1, 11)) + '</div>'
    anc = '<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:4px;margin-top:5px">' + ''.join('<div style="text-align:center;font-size:10.5px;line-height:1.15;font-weight:700;color:%s;white-space:nowrap;overflow:visible">%s</div>' % ('var(--mintT)' if i == sel else 'var(--mut)', ANCH.get(i, '<span style="opacity:.35">·</span>')) for i in range(1, 11)) + '</div>'
    lab = '<div style="margin-top:10px;text-align:center;font-size:14px;font-weight:800;color:var(--mintT);min-height:20px">%s</div>' % ('%d · Assez dur' % sel if sel else '<span style="color:var(--mut);font-weight:600">Touche le chiffre qui résume la séance</span>')
    return btns + anc + lab
def mk(sel, tag):
    html = saisie(True)
    import re
    start = html.index('<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:4px">')
    end = html.index('<div class="lbl"><span>Nutrition</span>')
    html = html[:start] + rpe_block(sel) + html[end:]
    html = re.sub(r'<div class="tag">.*?</div>', '<div class="tag"><b>%s</b>%s</div>' % tag, html, count=1, flags=re.S)
    return html
def rpe_vide(): return mk(None, ('1', 'Effort : avant le choix, repères visibles'))
def rpe_choisi(): return mk(4, ('2', 'Effort : après le choix (4)'))
EXPORT = ['rpe_vide', 'rpe_choisi']
