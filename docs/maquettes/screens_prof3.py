from base import *
from screens_prof2 import sub
def kv(rows):
    return ''.join('<div style="display:flex;justify-content:space-between;gap:14px;padding:10px 0;border-top:%s"><span style="color:var(--mut);font-size:14px">%s</span><b style="font-size:14.5px;text-align:right">%s</b></div>' % ('0' if i == 0 else '1px solid var(--line)', a, b) for i, (a, b) in enumerate(rows))
def block(title, rows, note='', act='Modifier'):
    return ('<div class="card" style="padding:14px 16px"><div style="display:flex;justify-content:space-between;align-items:center"><div class="h2">%s</div><div class="chip" style="height:34px;padding:0 12px;font-size:13px;font-weight:700">%s</div></div>'
            '%s<div style="margin-top:6px">%s</div></div>') % (title, act, '<div class="mini" style="margin-top:4px;line-height:1.4">%s</div>' % note if note else '', kv(rows))
def phase(name, dates, rows, badge=''):
    return ('<div style="padding:14px 0;border-top:1px solid var(--line)"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><div style="font-weight:800;font-size:15.5px">%s %s</div><span style="font-size:13px;font-weight:700;color:var(--mintT)">Modifier</span></div>'
            '<div class="mini" style="margin-top:2px">%s</div><div style="margin-top:4px">%s</div></div>') % (name, badge, dates, kv(rows))
B_CUR = '<span class="pill today" style="font-size:11.5px;vertical-align:2px">en cours</span>'
B_OWN = '<span class="pill ok" style="font-size:11.5px;vertical-align:2px">jours propres</span>'
def semaine_v2():
    inner = (block('Ta semaine type', [('Jours de course', 'mercredi, dimanche'), ('Sortie longue', 'dimanche'), ('Renforcement', 'mardi, vendredi')],
                   'Elle vaut pour toute la préparation, sauf pour une phase qui a ses propres jours.')
        + '<div class="card" style="padding:14px 16px"><div class="h2">Tes jours selon la phase</div>'
          '<div class="btn sec" style="height:44px;margin:10px 0 4px;font-size:14px">Bilan de la phase en cours</div>'
        + phase('Reprise', 'du 21 septembre au 15 novembre', [('Course', 'mercredi, dimanche'), ('Renforcement', 'mardi, vendredi')], B_CUR)
        + phase('Base', 'du 16 novembre au 28 mars', [('Course', 'mercredi, dimanche'), ('Renforcement', 'mardi, vendredi')])
        + phase('Endurance musculaire', 'du 29 mars au 23 mai', [('Course', 'mercredi, samedi, dimanche'), ('Week-end enchaîné', 'oui'), ('Renforcement', 'mardi')], B_OWN)
        + '<div style="text-align:center;padding-top:12px;border-top:1px solid var(--line);font-size:14px;font-weight:700;color:var(--mintT)">Voir les 4 phases suivantes</div></div>')
    return sub('Ta semaine', inner, ('3', 'Ta semaine, version structurée'), h=1240)
def toi_v2():
    inner = (block('Ton identité', [('Prénom', 'Antoine'), ('Poids', '91 kg')], 'Ton poids sert à doser la charge des montées lestées.')
        + block('Ton point de départ', [('Sorties par semaine', '1'), ('Durée moyenne', '45 minutes'), ('Plus longue sortie récente', '1 h 47'), ('Son dénivelé', '500 m de D+'), ('Course de référence', '42 km en 6 h 32')],
                'Il cale tes premières semaines. Dès que tu enregistres tes séances, l\'appli se base sur elles.')
        + block('Ton terrain', [('Longueur de tes montées', '1 à 5 minutes'), ('Accès à la montagne', 'occasionnel')],
                'Ce qui compte, c\'est la longueur de tes montées, pas le dénivelé total.'))
    return sub('Toi', inner, ('4', 'Toi, version structurée'), h=1000)
EXPORT = ['semaine_v2', 'toi_v2']
