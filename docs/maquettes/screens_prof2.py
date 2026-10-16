from base import *
from screens_profil import row, NAV
def sub(title, inner, tag, reco=False, h=760):
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><div class="mini" style="font-weight:700;color:var(--mintT)">‹ Ton profil</div><h1>%s</h1></div></header>' % title
        + inner + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', tag, reco=reco, h=h)
def cardrow(t, m, act='Modifier', extra=''):
    return ('<div class="card" style="padding:14px 16px"><div style="display:flex;gap:10px;align-items:flex-start"><div style="flex:1"><div class="k" style="font-size:11px">%s</div><div style="font-size:14.5px;line-height:1.45;margin-top:4px">%s</div>%s</div>'
            '<div class="chip" style="height:36px;padding:0 12px;font-size:13px;font-weight:700;flex:none">%s</div></div></div>') % (t, m, extra, act)
def home():
    items = (row('terrain', 'Ton objectif', 'Perso 80kms · 25 sept. 2027 · jalon le 8 mai')
             + row('calendar', 'Ta semaine', 'Mer, Dim · sortie longue le dimanche · 7 phases')
             + row('person', 'Toi', 'Point de départ, terrain, poids')
             + row('fitness', 'Tes modules', 'Renforcement, nutrition actifs')
             + row('run', 'Ton matériel', 'Ta montre · aucune paire de chaussures')
             + row('monitoring', 'Données et synchro', 'À jour · 23:25 · export, import')
             + row('injury', 'Réglages avancés', 'Redémarrer le plan, tout effacer'))
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><h1>Ton profil</h1><div class="sub">Tes réglages construisent ton plan</div></div></header>'
        + '<div class="card" style="padding:14px 16px"><div class="k">Objectif</div><div class="ttl" style="margin-top:4px">Perso 80kms · J−345</div><div class="mini">80 km · 5 000 m D+ · plan démarré le 21 sept.</div></div>'
        + '<div class="card" style="padding:6px 16px">' + items + '</div>'
        + '<div class="mini" style="text-align:center;margin:6px 0 90px">Ascend v31 · moteur de plan v2</div>'
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('1', 'Ton profil : 7 thèmes'), reco=True)
def objectif():
    inner = (cardrow('Course objectif', 'Perso 80kms · 25 sept. 2027<br>80 km · 5 000 m D+')
             + cardrow('Courses intermédiaires', 'Trail des coursières 2027 · 8 mai (jalon)', 'Modifier')
             + '<div class="mini" style="margin:4px 6px">Plan démarré la semaine du 21 sept. Pour repartir de zéro : Réglages avancés.</div>')
    return sub('Ton objectif', inner, ('2', 'Ton objectif'))
def semaine():
    ph = lambda n, d, c, on=False, own=False: ('<div style="padding:12px 0;border-top:1px solid var(--line);display:flex;gap:10px"><div style="flex:1"><div style="font-weight:800;font-size:15px">%s%s%s</div><div class="mini">%s</div><div class="mini" style="color:var(--ink)">%s</div></div><span class="chev">›</span></div>') % (
        n, ' <span class="pill today" style="font-size:11px">en cours</span>' if on else '', ' <span class="pill ok" style="font-size:11px">réglage propre</span>' if own else '', d, c)
    inner = (cardrow('Semaine type', 'Course : Mer, Dim<br>Sortie longue le dimanche')
             + '<div class="card" style="padding:14px 16px"><div class="k" style="font-size:11px">Par phase</div><div class="mini" style="margin:4px 0 6px">Tes jours peuvent changer selon la phase. Par défaut, ta semaine type vaut pour toute la préparation.</div>'
             + ph('Reprise', '21 sept. → 15 nov.', 'Mer, Dim · renfo Mar, Ven', on=True)
             + ph('Base', '16 nov. → 28 mars', 'Mer, Dim · renfo Mar, Ven')
             + ph('Endurance musculaire', '29 mars → 23 mai', 'Mer, Sam, Dim · week-end enchaîné', own=True)
             + '<div class="mini" style="text-align:center;padding-top:10px;font-weight:700;color:var(--mintT)">+ 4 phases · Bilan de la phase en cours</div></div>')
    return sub('Ta semaine', inner, ('3', 'Ta semaine : semaine type + phases'))
def toi():
    inner = (cardrow('Toi', 'Antoine · 91 kg', extra='<div class="mini" style="margin-top:4px">Ton poids sert à doser les montées lestées.</div>')
             + cardrow('Point de départ', '1 sortie par semaine, 0 h 45 en moyenne<br>Plus longue sortie : 1 h 47, 500 m D+<br>42 km en 6 h 32')
             + cardrow('Terrain', '1 à 5 min de montée · accès montagne occasionnel'))
    return sub('Toi', inner, ('4', 'Toi : identité, point de départ, terrain'))
def donnees():
    inner = ('<div class="card" style="padding:14px 16px"><div class="k" style="font-size:11px">Sauvegarde en ligne</div><div style="font-weight:700;margin-top:4px">antoine.silvent@outlook.com</div><div class="mini" style="color:var(--mintT)">À jour · 23:25</div>'
             '<div class="btn pri" style="height:46px;margin-top:10px">Synchroniser</div><div class="btn sec" style="height:44px;margin-top:8px">Changer d\'utilisateur</div></div>'
             '<div class="card" style="padding:14px 16px"><div class="k" style="font-size:11px">Exporter</div><div style="display:flex;gap:6px;margin-top:8px"><div class="chip" style="flex:1;height:38px;justify-content:center;font-weight:700;font-size:13px">JSON</div><div class="chip" style="flex:1.3;height:38px;justify-content:center;font-weight:700;font-size:13px">CSV séances</div><div class="chip" style="flex:1.4;height:38px;justify-content:center;font-weight:700;font-size:13px">CSV journal</div></div>'
             '<div class="k" style="font-size:11px;margin-top:14px">Importer</div><div class="mini" style="margin-top:6px;font-weight:700;color:var(--ink)">› Un CSV Garmin Connect<br>› Une sauvegarde JSON</div></div>')
    return sub('Données et synchro', inner, ('5', 'Données et synchro'))
def avances():
    inner = ('<div class="card" style="padding:14px 16px"><div style="font-weight:800">Redémarrer le plan cette semaine</div><div class="mini" style="margin-top:4px">Le plan repart de la semaine en cours. Tes séances enregistrées restent.</div><div class="btn sec" style="height:44px;margin-top:10px">Redémarrer</div></div>'
             '<div class="card" style="padding:14px 16px"><div style="font-weight:800;color:var(--coralT)">Effacer toutes les données</div><div class="mini" style="margin-top:4px">Efface aussi la copie en ligne, sur tous tes appareils. Exporte un JSON avant.</div><div class="btn sec" style="height:44px;margin-top:10px;color:var(--coralT)">Effacer</div></div>'
             '<div class="mini" style="margin:4px 6px">Dépannage de la synchro : ici aussi.</div>')
    return sub('Réglages avancés', inner, ('6', 'Réglages avancés : actions rares et risquées'))
EXPORT = ['home', 'objectif', 'semaine', 'toi', 'donnees', 'avances']
