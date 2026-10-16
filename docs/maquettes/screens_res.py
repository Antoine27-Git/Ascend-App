from base import *
from screens_v2 import fact3, line
H = 1190
def top(extra=''):
    return ('<div style="display:flex;justify-content:space-between;align-items:center"><div class="chip" style="width:40px;height:40px;font-size:20px;background:var(--card)">×</div>%s</div>'
            '<div class="row" style="margin-top:12px"><div class="ic sl">%s</div><div><div class="ttl" style="font-size:21px">Sortie longue</div><div class="meta">Aujourd\'hui · dimanche 18 oct.</div></div></div>') % (extra, ic('terrain'))
CARD = lambda inner, st='': '<div class="card" style="margin:12px 0 0;%s">%s</div>' % (st, inner)
FACTS = CARD(fact3([('1 h 50', 'durée'), ('200–300', 'm de D+'), ('Facile', 'effort')]), 'padding:13px 16px')
AFAIRE = CARD('<div class="h2">À faire</div><div style="font-size:17px;font-weight:800;margin-top:8px">1 h 50 d\'endurance continue</div>'
    + line('run', 'Tu peux parler tout du long. Départ tranquille : les premières minutes servent d\'échauffement.')
    + line('terrain', 'D+ : environ 200 à 300 m, sans le chercher. Montées raides marchées.')
    + line('monitoring', 'FC : zone facile. Le ressenti décide, la FC confirme.'))
WHY = CARD('<div class="h2">Pourquoi</div><div style="font-size:14px;line-height:1.4;margin-top:4px;color:var(--mut)">La seule séance qui progresse cette semaine (+10 % au plus sur ta plus longue des 30 derniers jours).</div>', 'padding:13px 16px')
NUT = CARD('<div class="row"><div class="ic nut" style="width:40px;height:40px;border-radius:12px">%s</div><div><div style="font-weight:800;font-size:15px">35 g de glucides par heure</div><div class="mini">≈ 64 g sur la séance · boisson ≈ 1,1 l</div></div></div>' % ic('nutrition'), 'padding:12px 16px')
SEC = lambda t, n='': '<div style="display:flex;align-items:center;gap:8px;margin:22px 4px 0"><span style="width:22px;height:22px;border-radius:50%%;background:var(--deep);color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center">%s</span><span style="font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)">%s</span></div>' % (n, t)
def opt(icon, t, sub, pri=False, bg='var(--card)'):
    return ('<div style="display:flex;align-items:center;gap:12px;padding:13px 14px;border-radius:16px;background:%s;%s;margin-top:8px">'
            '<div class="small-ic" style="background:%s;color:%s">%s</div><div style="flex:1"><div style="font-weight:800;font-size:15px;%s">%s</div><div class="mini">%s</div></div><span class="chev">›</span></div>') % (
            'var(--accent)' if pri else bg, 'box-shadow:var(--shadow)' if not pri else '', 'rgba(255,255,255,.55)' if pri else 'var(--mintBg)', 'var(--accentInk)' if pri else 'var(--mintT)', ic(icon), 'color:var(--accentInk)' if pri else '', t, sub)
WATCH = CARD('<div style="display:flex;align-items:center;gap:12px"><div class="small-ic" style="background:var(--skyBg);color:var(--sky)">%s</div><div style="flex:1"><div style="font-weight:800;font-size:15px">Ta Fenix 7</div><div class="mini">Pas encore envoyée</div></div><div class="btn sec" style="height:40px;padding:0 18px;font-size:14px;flex:none;width:auto;display:flex;align-items:center">Envoyer</div></div>' % ic('timer'), 'padding:12px 14px')
LINKS = '<div style="display:flex;justify-content:center;gap:22px;margin:20px 0 10px;font-size:13.5px;font-weight:700;color:var(--mut)"><span>Déplacer</span><span>Fichier Garmin</span></div>'
def scroll(inner, tag, reco=False, h=H):
    body = '<div class="halo"><i class="a"></i><i class="b"></i></div><div style="position:relative;z-index:1;padding:16px 16px 30px;height:%dpx;overflow:hidden">%s</div>' % (h, inner)
    return page(body, 'light', tag, reco=reco, h=h)

# A : sections dans le fil — Avant / Résultat
def res_A():
    res = (opt('timer', 'Récupérer depuis ta montre', 'Sortie trouvée : 1 h 52 · 11,8 km · 280 m D+', pri=True)
           + opt('person', 'Saisir à la main', 'Durée, D+, effort')
           + opt('calendar', 'Pas faite', 'Empêchement ou fatigue : le plan s\'adapte'))
    inner = (top('<div class="chip" style="height:40px;padding:0 14px;font-size:13.5px;font-weight:700;background:var(--card)">Déplacer</div>') + FACTS + SEC('Ta séance', '1') + WATCH + AFAIRE + WHY + NUT
             + SEC('Résultat de la séance', '2') + res)
    return scroll(inner, ('A', 'Ta séance / Résultat, Déplacer en haut'), reco=True)

# B : une barre fixe avec un seul bouton, qui ouvre un choix
def res_B():
    foot = ('<div style="position:absolute;z-index:2;left:0;right:0;bottom:0;padding:12px 16px 18px;background:var(--bg);border-top:1px solid var(--line)">'
            '<div class="btn pri" style="height:54px">Résultat de la séance</div></div>')
    inner = top('<div class="chip" style="height:40px;padding:0 14px;font-size:13.5px;font-weight:700;background:var(--card)">Déplacer</div>') + FACTS + WATCH + AFAIRE + WHY + NUT + '<div style="height:90px"></div>'
    body = '<div class="halo"><i class="a"></i><i class="b"></i></div><div style="position:relative;z-index:1;padding:16px 16px 0;height:760px;overflow:hidden">%s</div>%s' % (inner, foot)
    return page(body, 'light', ('B1', 'Un seul bouton fixe en bas…'), h=760)
def res_B2():
    sheet = ('<div class="dim" style="z-index:2"></div><div class="sheet" style="top:330px;z-index:3"><div class="grab"></div><div style="padding:10px 16px 20px">'
             '<div class="ttl" style="font-size:19px">Résultat de la séance</div><div class="mini">Sortie longue · dimanche 18 oct.</div>'
             + opt('timer', 'Récupérer depuis ta montre', 'Sortie trouvée : 1 h 52 · 11,8 km · 280 m D+', pri=True)
             + opt('person', 'Saisir à la main', 'Durée, D+, effort')
             + opt('calendar', 'Pas faite', 'Empêchement ou fatigue : le plan s\'adapte') + '</div></div>')
    inner = top() + FACTS + AFAIRE
    body = '<div class="halo"><i class="a"></i><i class="b"></i></div><div style="position:relative;z-index:1;padding:16px;height:760px;overflow:hidden">%s</div>%s' % (inner, sheet)
    return page(body, 'light', ('B2', '… qui ouvre un choix en 3 lignes'), h=760)

# C : onglets Prévu / Résultat
def res_C():
    seg = '<div class="seg" style="margin-top:14px"><div>Prévu</div><div class="on">Résultat</div></div>'
    inner = (top() + seg
             + CARD('<div class="mini" style="font-weight:700">Ta montre a enregistré, aujourd\'hui à 9 h 05</div><div style="font-size:20px;font-weight:800;margin-top:4px">1 h 52 · 11,8 km · 280 m D+</div><div class="mini">prévu : 1 h 50 · 200 à 300 m</div><div class="btn pri" style="height:50px;margin-top:12px">Noter mon effort</div>', 'padding:14px 16px')
             + '<div style="display:flex;gap:8px;margin-top:10px"><div class="btn sec" style="flex:1;height:46px;font-size:14px">Saisir à la main</div><div class="btn sec" style="flex:1;height:46px;font-size:14px">Pas faite</div></div>'
             + '<div class="mini" style="text-align:center;margin-top:16px">L\'onglet Prévu garde l\'envoi à la montre, À faire, Pourquoi et la nutrition.</div>')
    return scroll(inner, ('C', 'Onglets Prévu / Résultat'), h=760)
EXPORT = ['res_A', 'res_B', 'res_B2', 'res_C']
