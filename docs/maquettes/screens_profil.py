from base import *
NAV = ["Aujourd'hui", 'Semaine', 'Suivi', 'Profil']
def row(icon, t, m, right='<span class="chev">›</span>', style=''):
    return ('<div class="listrow" style="%s"><div class="small-ic" style="background:var(--mintBg);color:var(--mintT)">%s</div>'
            '<div style="flex:1;min-width:0"><div class="t">%s</div><div class="m">%s</div></div>%s</div>') % (style, ic(icon), t, m, right)
def sw(on=True):
    c = 'var(--mintT)' if on else 'var(--line)'
    x = '18px' if on else '2px'
    return '<span style="width:40px;height:24px;border-radius:12px;background:%s;position:relative;flex:none;display:inline-block"><i style="position:absolute;top:2px;left:%s;width:20px;height:20px;border-radius:50%%;background:#fff"></i></span>' % (c, x)
def sec(title, sub, inner, open_=True):
    return ('<div class="card" style="padding:14px 16px"><div class="sb"><div class="h2">%s</div><span class="chev" style="transform:rotate(%s)">›</span></div>'
            '<div class="mini">%s</div>%s</div>') % (title, '90deg' if open_ else '0', sub, inner if open_ else '')
def fld(l, v, hint=''):
    return '<div style="margin-top:10px"><div class="lbl">%s</div><div class="field" style="display:flex;align-items:center;padding:0 12px;height:44px">%s</div>%s</div>' % (l, v, '<div class="mini" style="margin-top:4px">%s</div>' % hint if hint else '')

def profil_A():
    watch = (fld('Ta montre', 'Garmin Fenix 7', 'Reconnue depuis tes sorties intervals.icu. Tu peux la corriger.')
             + '<div style="margin-top:12px;display:flex;align-items:center;gap:10px"><div style="flex:1"><b>Envoi des séances à la montre</b><div class="mini">via intervals.icu</div></div><span class="pill ok">Connecté</span></div>')
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + header('Ton profil', 'Antoine · Objectif 80 km · plan depuis le 31 août', logo=False)
        + sec('Toi · 1 à compléter', 'Objectif, FC, allures', row('terrain', 'Objectif Perso 80kms', '1er août 2027 · 80 km · 3 000 à 6 000 m D+') + row('person', 'FC et allures', 'FC max 187 · seuil 168 · à compléter', '<span class="pill today">1 à compléter</span>'), False)
        + sec('Ton plan', 'Ce que le plan prend en compte',
              row('fitness', 'Renforcement / CrossFit', 'Séances prescrites ou libres', sw(True))
              + row('nutrition', 'Nutrition', 'Glucides et boisson, séances longues', sw(True))
              + row('injury', 'Blessure en cours', 'Suivi quotidien de la douleur', sw(False))
              + row('calendar', 'Journal du matin', 'Sommeil, énergie, FC repos, poids', sw(False)), True)
        + sec('Matériel', 'Montre et chaussures', watch + row('run', 'Chaussures', '2 paires · 312 km sur la paire principale'), False)
        + sec('Données', 'Synchronisation, export, sauvegarde', '', False)
        + sec('Réglages avancés', 'Redémarrer le plan, effacer les données', '', False)
        + '<div class="mini" style="text-align:center;margin:6px 0 90px">Ascend v28 · sources et hypothèses</div>'
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('A', 'Profil en 5 blocs repliables'), reco=True)

def profil_B():
    items = (row('terrain', 'Toi', 'Objectif, FC, allures', '<span class="pill today">1 à compléter</span>')
             + row('calendar', 'Ton plan', 'Renforcement, nutrition, blessure, journal')
             + row('run', 'Ton matériel', 'Garmin Fenix 7 · 2 paires de chaussures')
             + row('monitoring', 'Données et synchro', 'Connecté · dernière synchro 22:31')
             + row('person', 'Réglages avancés', 'Redémarrer le plan, effacer'))
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + header('Ton profil', 'Antoine', logo=False)
        + '<div class="card" style="padding:14px 16px"><div class="k">Objectif</div><div class="ttl" style="margin-top:4px">Perso 80kms · J−290</div><div class="mini">Plan démarré le 31 août · semaine 7</div></div>'
        + '<div class="card" style="padding:6px 16px">' + items + '</div>'
        + '<div class="mini" style="text-align:center;margin:6px 0 90px">Ascend v28</div>'
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('B', 'Profil en liste, un sous-écran par thème'))

def materiel():
    opt = lambda t, on: '<div class="opt%s" style="flex:1;text-align:center">%s</div>' % (' on' if on else '', t)
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + header('Ton matériel', 'Pour adapter ce qu\'Ascend te propose', logo=False)
        + '<div class="card" style="padding:14px 16px"><div class="h2">Tu cours avec une montre ?</div><div style="display:flex;gap:8px;margin-top:10px">' + opt('Oui', True) + opt('Non', False) + '</div>'
        + fld('Modèle', 'Garmin Fenix 7', 'Détecté dans intervals.icu. Corrige-le ou écris le tien.')
        + '<div class="mini" style="margin-top:12px"><b style="color:var(--ink)">Si tu réponds Non :</b> pas d\'envoi à la montre ni de lecture d\'activités ; tu notes tes séances à la main (durée, D+, effort).</div></div>'
        + '<div class="card" style="padding:6px 16px">' + row('run', 'Chaussures', '2 paires · 312 km') + '</div>'
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('C', 'Matériel : montre oui/non, modèle auto ou saisi'))
EXPORT = ['profil_A', 'profil_B', 'materiel']

def mcard(icon, t, on, short, blocks=None):
    head = ('<div style="display:flex;align-items:center;gap:12px"><div class="small-ic" style="background:var(--mintBg);color:var(--mintT)">%s</div>'
            '<div style="flex:1;min-width:0"><div class="t" style="font-size:16px">%s</div><div class="m mini">%s</div></div>%s</div>') % (ic(icon), t, short, sw(on))
    body = ''
    for lab, txt in (blocks or []):
        body += '<div style="margin-top:20px"><div class="k" style="font-size:11px">%s</div><div style="font-size:14px;line-height:1.55;margin-top:6px">%s</div></div>' % (lab, txt)
    return '<div class="card" style="padding:14px 16px">%s%s</div>' % (head, body)

def plan_B():
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><div class="mini" style="font-weight:700;color:var(--mintT)">‹ Ton profil</div><h1>Ton plan</h1></div></header>'
        + mcard('fitness', 'Renforcement', True, 'Tes séances de force dans la semaine', [
            ('Pourquoi', 'La force des jambes améliore l\'économie de course et la tenue en descente.'),
            ('Ce que ça change', 'Le plan place tes séances dans la semaine et compte leur charge. Avec 2 séances ou plus, il ne propose plus de côtes courtes.'),
            ('Qui décide du contenu ?', '<div style="display:flex;gap:8px;margin:10px 0 14px"><div class="opt on" style="flex:1;text-align:center;font-size:13px">Prescrit par l\'app</div><div class="opt" style="flex:1;text-align:center;font-size:13px">Je gère moi-même</div></div>'
              '<b>Prescrit :</b> l\'app te donne les exercices de chaque séance.<br><b>Je gère moi-même :</b> tu fais ta séance (salle, CrossFit…). L\'app ne la détaille pas : elle la compte dans ta charge et te prévient si elle tombe trop près de ta sortie longue.')])
        + mcard('nutrition', 'Nutrition à l\'effort', True, 'Glucides et boisson sur les longues sorties')
        + mcard('injury', 'Blessure en cours', False, 'Douleur au réveil, alertes adaptées')
        + mcard('calendar', 'Journal du matin', False, 'Sommeil, énergie, FC repos, poids')
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('B', 'Ton plan : une carte par module, avec explication'))

def materiel2():
    opt = lambda t, on: '<div class="opt%s" style="flex:1;text-align:center">%s</div>' % (' on' if on else '', t)
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><div class="mini" style="font-weight:700;color:var(--mintT)">‹ Ton profil</div><h1>Ton matériel</h1></div></header>'
        + '<div class="card" style="padding:14px 16px"><div class="h2">Tu cours avec une montre ?</div><div style="display:flex;gap:8px;margin-top:10px">' + opt('Oui', True) + opt('Non', False) + '</div>'
        + fld('Modèle', 'Garmin Fenix 7', 'Détecté dans intervals.icu, modifiable.')
        + '<div style="margin-top:12px"><div class="k" style="font-size:11px">Ce que ça change</div><div style="font-size:13.5px;line-height:1.4;margin-top:2px">Avec une montre : envoi des séances et lecture des sorties. Sans : tu notes tes séances à la main.</div></div></div>'
        + '<div class="card" style="padding:14px 16px"><div class="h2">Chaussures</div><div class="mini">2 paires · 312 km sur la principale</div><div class="mini" style="margin-top:8px"><b style="color:var(--ink)">Ce que ça change :</b> le kilométrage par paire, pour savoir quand la changer.</div></div>'
        + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', ('C', 'Ton matériel : uniquement ce que l\'appli utilise'))
EXPORT = ['profil_A', 'profil_B', 'materiel', 'plan_B', 'materiel2']

def acc(icon, t, on, short, blocks=None, open_=False, hl=False):
    chev = '<span class="chev" style="transform:rotate(%s);flex:none">›</span>' % ('90deg' if open_ else '0')
    head = ('<div style="display:flex;align-items:center;gap:10px"><div class="small-ic" style="background:var(--mintBg);color:var(--mintT)">%s</div>'
            '<div style="flex:1;min-width:0"><div class="t" style="font-size:16px">%s</div><div class="m mini">%s</div></div>%s%s</div>') % (ic(icon), t, short, sw(on), chev)
    body = ''
    if open_:
        for lab, txt in (blocks or []):
            body += '<div style="margin-top:20px"><div class="k" style="font-size:11px">%s</div><div style="font-size:14px;line-height:1.55;margin-top:6px">%s</div></div>' % (lab, txt)
    ring = 'box-shadow:inset 0 0 0 2px var(--mintT),var(--cardShadow);' if hl else ''
    return '<div class="card" style="padding:14px 16px;%s">%s%s</div>' % (ring, head, body)

REN = [('Pourquoi', 'La force des jambes améliore l\'économie de course et la tenue en descente.'),
       ('Ce que ça change', 'Le plan place tes séances dans la semaine et compte leur charge. Avec 2 séances ou plus, il ne propose plus de côtes courtes.')]
JOU = [('Pourquoi', 'Suivre ton sommeil, ta FC de repos et ton poids sur la durée.'),
       ('Ce que ça change', 'Une question le matin sur l\'écran Aujourd\'hui, et des moyennes dans ton suivi.'),
       ('Ce que ça ne fait pas', 'Le plan ne lit pas ces notes : il ne change pas tes séances.')]
def screen(cards, tag, name='Ton plan'):
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
        + '<header><div><div class="mini" style="font-weight:700;color:var(--mintT)">‹ Ton profil</div><h1>%s</h1></div></header>' % name
        + ''.join(cards) + '</div>' + nav(NAV, 'Profil'))
    return page(body, 'light', tag)
def acc_1():
    return screen([acc('fitness','Renforcement',True,'Tes séances de force',REN,True),acc('nutrition','Nutrition à l\'effort',True,'Glucides et boisson'),acc('injury','Blessure en cours',False,'Douleur au réveil'),acc('calendar','Journal du matin',False,'Sommeil, FC repos, poids')], ('1', 'Au départ : Renforcement ouvert'))
def acc_2():
    return screen([acc('fitness','Renforcement',True,'Tes séances de force'),acc('nutrition','Nutrition à l\'effort',True,'Glucides et boisson'),acc('injury','Blessure en cours',False,'Douleur au réveil'),acc('calendar','Journal du matin',False,'Sommeil, FC repos, poids')], ('2', 'Tout fermé : un second tap referme'))
def acc_3():
    return screen([acc('fitness','Renforcement',True,'Tes séances de force'),acc('nutrition','Nutrition à l\'effort',True,'Glucides et boisson'),acc('injury','Blessure en cours',False,'Douleur au réveil'),acc('calendar','Journal du matin',True,'Sommeil, FC repos, poids',JOU,True,True)], ('3', 'Activation du Journal : il s\'ouvre, Renforcement se replie'))
EXPORT = ['profil_A', 'profil_B', 'materiel', 'plan_B', 'materiel2', 'acc_1', 'acc_2', 'acc_3']
