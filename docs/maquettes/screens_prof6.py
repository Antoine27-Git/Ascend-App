from base import *
from screens_prof2 import sub
LN = 'border-top:1px solid var(--line)'
def fr(label, val, unit='', first=False, focus=False):
    u = '<span style="color:var(--mut);font-size:14px;margin-left:5px">%s</span>' % unit if unit else ''
    ul = 'box-shadow:inset 0 -2px 0 var(--mintT);' if focus else ''
    return ('<div style="display:flex;align-items:center;justify-content:space-between;min-height:52px;%s"><span style="font-size:15px">%s</span>'
            '<span style="font-size:16.5px;font-weight:800;padding:4px 2px;%s">%s%s</span></div>') % ('' if first else LN, label, ul, val, u)
def pick(label, val, first=False):
    return ('<div style="display:flex;align-items:center;justify-content:space-between;min-height:52px;%s"><span style="font-size:15px">%s</span>'
            '<span style="font-size:16.5px;font-weight:800;color:var(--mintT)">%s <span style="font-weight:600">⌄</span></span></div>') % ('' if first else LN, label, val)
def seg(label, opts, on):
    return ('<div style="padding:12px 0;%s"><div style="font-size:15px;margin-bottom:8px">%s</div><div style="display:flex;gap:6px">%s</div></div>') % (LN, label, ''.join(
        '<div style="flex:1;height:40px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700;%s">%s</div>' % (
            'background:var(--mintT);color:#fff' if o == on else 'background:transparent;color:var(--mut);box-shadow:inset 0 0 0 1px var(--line)', o) for o in opts))
def card(title, note, body):
    return '<div class="card" style="padding:16px 16px 6px"><div class="h2">%s</div><div class="mini" style="margin:4px 0 8px;line-height:1.45">%s</div>%s</div>' % (title, note, body)
def crs(name, sub_, open_=False, ref=False, body=''):
    b = '<span class="pill ok" style="font-size:11.5px;margin-left:8px">référence</span>' if ref else ''
    ch = '⌃' if open_ else '⌄'
    head = ('<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 0;%s"><div><div style="font-weight:800;font-size:15.5px">%s%s</div>'
            '<div class="mini" style="margin-top:2px">%s</div></div><span style="color:var(--mut);font-size:18px">%s</span></div>') % (LN, name, b, sub_, ch)
    return head + body
def toi_v5(wheel=False):
    c1 = crs('Trail du Beaujolais', '6 h 32 · 42 km · 1 300 m D+', True, True,
         pick('Durée', '6 h 32', True) + fr('Distance', '42', 'km') + fr('Dénivelé', '1 300', 'm D+') + pick('Date', 'avril 2026')
         + '<div style="padding:10px 0 14px;font-size:13.5px;font-weight:700;color:#b3261e">Supprimer cette course</div>')
    c2 = crs('Course des crêtes', '2 h 05 · 15 km · 480 m D+')
    c3 = crs('Trail des monts', '4 h 40 · 30 km · 900 m D+')
    inner = (card('Ton identité', 'Ton poids sert à doser la charge des montées lestées.', fr('Prénom', 'Antoine', '', True) + fr('Poids', '91', 'kg', False, True))
        + card('Ton historique', 'Tes 4 dernières semaines avant le plan. Elles calent tes premières semaines ; ensuite, l\'appli se base sur les séances que tu enregistres.',
               fr('Sorties par semaine', '1', '', True) + pick('Durée moyenne', '45 min') + pick('Plus longue sortie', '1 h 47') + fr('Son dénivelé', '500', 'm D+'))
        + card('Tes courses passées', 'Le plan prend comme référence la course la plus proche de ton objectif pour estimer ta durée de course.',
               c1 + c2 + c3 + '<div style="padding:14px 0;%s;font-size:14.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course</div>' % LN)
        + card('Ton terrain', 'Ce qui compte, c\'est la longueur de tes montées, pas le dénivelé total.',
               seg('Longueur de tes montées', ['< 1 min', '1 à 5 min', '> 5 min'], '1 à 5 min') + seg('Accès à la montagne', ['jamais', 'occasionnel', 'régulier'], 'occasionnel')))
    if wheel:
        def col(vals, sel, unit):
            rows = ''.join('<div style="height:40px;display:flex;align-items:center;justify-content:center;font-size:%dpx;font-weight:%d;color:%s">%s</div>' % (
                ((24, 800, '#111') if v == sel else (18, 500, '#a3ada7')) + (v,)) for v in vals)
            return '<div style="flex:1;text-align:center"><div>%s</div></div>' % rows
        sheet = ('<div style="position:absolute;inset:0;background:rgba(0,0,0,.35);z-index:20"></div>'
                 '<div style="position:absolute;left:0;right:0;bottom:0;z-index:21;background:var(--card,#fff);border-radius:24px 24px 0 0;padding:18px 20px 22px">'
                 '<div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:17px">Durée de la course</b><span style="font-weight:800;color:var(--mintT)">OK</span></div>'
                 '<div style="position:relative;margin-top:10px;display:flex;align-items:center"><div style="position:absolute;left:0;right:0;top:80px;height:40px;border-radius:12px;background:var(--mintBg);z-index:0"></div>'
                 '<div style="display:flex;width:100%;position:relative;z-index:1">'
                 + col(['4', '5', '6', '7', '8'], '6', 'h') + '<div style="width:34px;margin-top:80px;height:40px;display:flex;align-items:center;font-weight:800">h</div>'
                 + col(['30', '31', '32', '33', '34'], '32', 'min') + '<div style="width:44px;margin-top:80px;height:40px;display:flex;align-items:center;font-weight:800">min</div></div></div></div>')
        inner = card('Tes courses passées', 'Le plan prend comme référence la course la plus proche de ton objectif.', c1)
        html = sub('Toi', inner, ('4', 'Toi : roue pour la durée'), h=860)
        return html.replace('<nav>', sheet + '<nav>', 1)
    return sub('Toi', inner, ('4', 'Toi : lignes modifiables, courses dépliables'), h=1760)
def toi_v5_roue(): return toi_v5(True)
EXPORT = ['toi_v5', 'toi_v5_roue']
