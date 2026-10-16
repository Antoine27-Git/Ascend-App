from base import *
from screens_prof2 import sub
from screens_prof3 import kv, block
D = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
def squares(on, kind='run'):
    col = {'run': ('var(--mintBg)', 'var(--mintT)'), 'long': ('var(--mintT)', '#fff'), 'cf': ('var(--violetBg)', 'var(--violet)')}[kind]
    return '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:5px">' + ''.join(
        '<div style="height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;%s">%s</div>' % (
            ('background:%s;color:%s;box-shadow:inset 0 0 0 1.5px %s' % (col[0], col[1], col[1] if kind != 'long' else col[0])) if i in on else 'background:var(--chip);color:#a3ada7', d)
        for i, d in enumerate(D)) + '</div>'
def drow(label, on, kind='run'):
    return '<div style="margin-top:12px"><div style="font-size:13.5px;color:var(--mut);margin-bottom:6px">%s</div>%s</div>' % (label, squares(on, kind))
def semaine_v3():
    typ = ('<div class="card" style="padding:14px 16px"><div style="display:flex;justify-content:space-between;align-items:center"><div class="h2">Ta semaine type</div><div class="chip" style="height:34px;padding:0 12px;font-size:13px;font-weight:700">Modifier</div></div>'
           '<div class="mini" style="margin-top:4px;line-height:1.4">Elle vaut pour toute la préparation, sauf pour une phase qui a ses propres jours.</div>'
           + drow('Jours de course', [2, 6]) + drow('Sortie longue', [6], 'long') + drow('Renforcement', [1, 4], 'cf') + '</div>')
    def ph(name, dates, badge='', open_=False, body=''):
        chev = '<span class="chev" style="transform:rotate(%s);margin-left:0">›</span>' % ('90deg' if open_ else '0')
        return ('<div style="padding:14px 0;border-top:1px solid var(--line)"><div style="display:flex;align-items:center;gap:10px"><div style="flex:1"><div style="font-weight:800;font-size:15.5px">%s %s</div><div class="mini">%s</div></div>%s</div>%s</div>') % (name, badge, dates, chev, body if open_ else '')
    cur = ('<div style="margin-top:12px;font-size:14px;line-height:1.5">Réhabituer le corps : endurance facile, quelques accélérations, force générale légère.</div>'
           '<div style="margin-top:10px;padding:10px 12px;border-radius:12px;background:var(--chip);font-size:13.5px;line-height:1.45"><b>Logique du plan</b> · La sortie longue progresse de 10 % au plus par rapport à ta plus longue des 30 derniers jours. Le reste du volume reste facile.</div>'
           + drow('Jours de course', [2, 6]) + drow('Sortie longue', [6], 'long') + drow('Renforcement', [1, 4], 'cf')
           + '<div class="mini" style="margin-top:10px">Mêmes jours que ta semaine type.</div>'
           '<div class="btn sec" style="height:44px;margin-top:12px;font-size:14px">Modifier les jours de cette phase</div>'
           '<div style="text-align:center;margin-top:10px;font-size:13.5px;font-weight:700;color:var(--mintT)">Bilan de la phase en cours</div>')
    B_CUR = '<span class="pill today" style="font-size:11.5px;vertical-align:2px">en cours</span>'
    B_OWN = '<span class="pill ok" style="font-size:11.5px;vertical-align:2px">jours propres</span>'
    phases = ('<div class="card" style="padding:14px 16px 2px"><div class="h2">Tes phases</div><div class="mini" style="margin-top:4px">Touche une phase pour voir ce qu\'elle travaille et ses jours.</div>'
              + ph('Reprise', 'du 21 septembre au 15 novembre', B_CUR, True, cur)
              + ph('Base', 'du 16 novembre au 28 mars')
              + ph('Endurance musculaire', 'du 29 mars au 23 mai', B_OWN)
              + ph('Intensité en côte', 'du 24 mai au 4 juillet')
              + ph('Bloc spécifique', 'du 5 juillet au 15 août')
              + ph('Pic', 'du 16 août au 5 septembre')
              + ph('Affûtage', 'du 6 septembre au 26 septembre') + '</div>')
    return sub('Ta semaine', typ + phases, ('3', 'Ta semaine : carrés de jours, phases dépliables'), reco=True, h=1720)
def toi_v3():
    races = ('<div class="card" style="padding:14px 16px"><div style="display:flex;justify-content:space-between;align-items:center"><div class="h2">Tes courses passées</div><div class="chip" style="height:34px;padding:0 12px;font-size:13px;font-weight:700">Modifier</div></div>'
             '<div class="mini" style="margin-top:4px;line-height:1.4">Le plan prend comme référence la course la plus proche de ton objectif pour estimer ta durée de course.</div>'
             '<div style="margin-top:10px;padding:12px;border-radius:14px;box-shadow:inset 0 0 0 1.5px var(--mintT);background:var(--mintBg)"><div style="display:flex;justify-content:space-between"><b>Trail · 42 km</b><span class="pill ok" style="font-size:11.5px">référence</span></div>'
             '<div style="font-size:14px;margin-top:4px">6 h 32 · 1 300 m de D+</div><div class="mini">avril 2026</div></div>'
             '<div style="margin-top:8px;font-size:13.5px;font-weight:700;color:var(--mintT)">+ Ajouter une course</div></div>')
    inner = (block('Ton identité', [('Prénom', 'Antoine'), ('Poids', '91 kg')], 'Ton poids sert à doser la charge des montées lestées.')
        + block('Ton historique', [('Sorties par semaine', '1'), ('Durée moyenne', '45 minutes'), ('Plus longue sortie récente', '1 h 47'), ('Son dénivelé', '500 m de D+')],
                'Tes 4 dernières semaines avant le plan. Elles calent tes premières semaines ; ensuite, l\'appli se base sur les séances que tu enregistres.')
        + races
        + block('Ton terrain', [('Longueur de tes montées', '1 à 5 minutes'), ('Accès à la montagne', 'occasionnel')],
                'Ce qui compte, c\'est la longueur de tes montées, pas le dénivelé total.'))
    return sub('Toi', inner, ('4', 'Toi : historique et courses passées'), h=1340)
EXPORT = ['semaine_v3', 'toi_v3']
