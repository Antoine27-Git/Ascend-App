from base import *
from screens_prof2 import sub
def fld(label, val, unit='', w=None):
    return ('<div style="flex:1;min-width:0"><div style="font-size:13px;color:var(--mut);margin-bottom:5px">%s</div>'
            '<div style="height:46px;border-radius:12px;background:var(--chip);box-shadow:inset 0 0 0 1px var(--line);display:flex;align-items:center;padding:0 12px;gap:6px">'
            '<b style="font-size:16px;flex:1">%s</b><span style="font-size:13.5px;color:var(--mut)">%s</span></div></div>') % (label, val, unit)
def row(*f): return '<div style="display:flex;gap:10px;margin-top:12px">%s</div>' % ''.join(f)
def seg(label, opts, on):
    return ('<div style="margin-top:12px"><div style="font-size:13px;color:var(--mut);margin-bottom:5px">%s</div><div style="display:flex;gap:6px">%s</div></div>') % (label, ''.join(
        '<div style="flex:1;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;%s">%s</div>' % (
            'background:var(--mintBg);color:var(--mintT);box-shadow:inset 0 0 0 1.5px var(--mintT)' if o == on else 'background:var(--chip);color:var(--mut)', o) for o in opts))
def card(title, note, body):
    return '<div class="card" style="padding:14px 16px"><div class="h2">%s</div><div class="mini" style="margin-top:4px;line-height:1.4">%s</div>%s</div>' % (title, note, body)
def course(name, dist, dur, dp, date, ref):
    b = '<span class="pill ok" style="font-size:11.5px">référence</span>' if ref else ''
    st = 'box-shadow:inset 0 0 0 1.5px var(--mintT);background:var(--mintBg)' if ref else 'box-shadow:inset 0 0 0 1px var(--line)'
    return ('<div style="margin-top:12px;padding:12px;border-radius:14px;%s"><div style="display:flex;justify-content:space-between;align-items:center"><b>%s</b>%s</div>'
            '%s%s<div style="margin-top:10px;font-size:13px;font-weight:700;color:#b3261e">Supprimer cette course</div></div>') % (
        st, name, b, row(fld('Distance', dist, 'km'), fld('Durée', dur, '')), row(fld('Dénivelé', dp, 'm D+'), fld('Date', date, '')))
def toi_v4():
    inner = (card('Ton identité', 'Ton poids sert à doser la charge des montées lestées.', row(fld('Prénom', 'Antoine'), fld('Poids', '91', 'kg')))
        + card('Ton historique', 'Tes 4 dernières semaines avant le plan. Elles calent tes premières semaines ; ensuite, l\'appli se base sur les séances que tu enregistres.',
               row(fld('Sorties par semaine', '1'), fld('Durée moyenne', '45', 'min')) + row(fld('Plus longue sortie', '1 h 47'), fld('Son dénivelé', '500', 'm D+')))
        + card('Tes courses passées', 'Le plan prend comme référence la course la plus proche de ton objectif pour estimer ta durée de course.',
               course('Trail · 42 km', '42', '6 h 32', '1 300', 'avril 2026', True)
               + '<div style="margin-top:12px;font-size:14px;font-weight:700;color:var(--mintT)">+ Ajouter une course</div>')
        + card('Ton terrain', 'Ce qui compte, c\'est la longueur de tes montées, pas le dénivelé total.',
               seg('Longueur de tes montées', ['< 1 min', '1 à 5 min', '> 5 min'], '1 à 5 min') + seg('Accès à la montagne', ['jamais', 'occasionnel', 'régulier'], 'occasionnel'))
        + '<div class="mini" style="text-align:center;margin:4px 0 0">Chaque champ s\'enregistre dès que tu quittes la case.</div>')
    return sub('Toi', inner, ('4', 'Toi : champs modifiables directement'), h=1560)
EXPORT = ['toi_v4']
