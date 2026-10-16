from base import *
from screens_v3 import fiche_long
import re
def foot(left, lsub, right='J\'ai fait ma séance', lstyle=''):
    return ('<div class="foot"><div style="display:grid;grid-template-columns:1.15fr 2fr;gap:8px">'
            '<div class="btn sec" style="height:56px;flex-direction:column;line-height:1.1;display:flex;align-items:center;justify-content:center;%s"><span style="font-size:14.5px">%s</span><span style="font-size:11.5px;font-weight:600;color:var(--mut);margin-top:2px">%s</span></div>'
            '<div class="btn pri" style="height:56px">%s</div></div></div>') % (lstyle, left, lsub, right)
def swap(html, newfoot, tag):
    html = re.sub(r'<div class="foot">.*?</div></div></div>', newfoot, html, count=1, flags=re.S)
    return re.sub(r'<div class="tag">.*?</div>', '<div class="tag"><b>%s</b>%s</div>' % tag, html, count=1, flags=re.S)
def act_avant(): return swap(fiche_long(), foot('Envoyer', 'sur ta Fenix 7'), ('1', 'Pas encore envoyée'))
def act_envoyee(): return swap(fiche_long(), foot('Sur ta Fenix 7 ✓', 'envoyée à 7 h 42', lstyle='background:var(--mintBg);color:var(--mintT)'), ('2', 'Envoyée'))
def act_menu():
    html = fiche_long()
    menu = ('<div style="position:absolute;right:16px;top:96px;width:236px;background:var(--card);border-radius:18px;box-shadow:0 12px 34px rgba(0,0,0,.18);padding:6px;z-index:5">'
            + ''.join('<div style="padding:13px 14px;font-weight:700;font-size:14.5px;%s">%s</div>' % (s, t) for t, s in [
                ('Pas faite', ''), ('Déplacer', 'border-top:1px solid var(--line)'), ('Renvoyer sur ta Fenix 7', 'border-top:1px solid var(--line)'),
                ('Retirer de ta Fenix 7', 'border-top:1px solid var(--line)'), ('Exporter le fichier Garmin', 'border-top:1px solid var(--line)')]) + '</div>')
    html = html.replace('<div class="grab"></div>', '<div class="grab"></div>' + menu, 1)
    return swap(html, foot('Sur ta Fenix 7 ✓', 'envoyée à 7 h 42', lstyle='background:var(--mintBg);color:var(--mintT)'), ('3', 'Menu ⋯ ouvert'))
EXPORT = ['act_avant', 'act_envoyee', 'act_menu']
