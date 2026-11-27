"""Lot « ajouter une séance » (27/11/2026) : bouton dans Semaine, type de séance, proposition de footing par règles.
python3 render.py screens_ajout
"""
from screens_renfo import *
import screens_bilan2 as B2

X6 = r"""
.btn2{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:12px;border-radius:14px;padding:12px;font-weight:800;font-size:15px;color:var(--mintT);background:#eefaf3;box-shadow:inset 0 0 0 1.5px var(--mintBg)}
.prop{background:#eefaf3;border-radius:16px;padding:12px 14px;margin-top:12px}
.prop .pt{font-size:19px;font-weight:800;letter-spacing:-.01em}
.prop .tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.prop .tags span{background:#fff;border-radius:999px;padding:5px 10px;font-size:13px;font-weight:700}
.why{font-size:14px;line-height:1.5;margin-top:10px}
.why b{display:block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--mintT);margin-bottom:3px}
.lnk{text-align:center;margin-top:12px;font-weight:700;color:var(--mut);font-size:14px}
.wk2 .plus{position:relative}
.wk2 .plus::after{content:'+';position:absolute;right:-7px;top:-7px;width:16px;height:16px;border-radius:50%;background:var(--mintT);color:#fff;font:800 12px/16px Inter,sans-serif;text-align:center;box-shadow:0 0 0 2px #fff}
.sel1{box-shadow:inset 0 0 0 2px var(--mintT)!important;background:#eefaf3!important}
"""
B2.X = B2.X + X6
SV = '<svg class="mi" style="fill:none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">'
BIKE = SV + '<circle cx="5.5" cy="16.5" r="3.5"/><circle cx="18.5" cy="16.5" r="3.5"/><path d="M5.5 16.5L9 10h6.5l3 6.5M9 10l3 6.5h-6.5M12 16.5l3.5-6.5M15 7h2.5M8 7.5h3"/></svg>'
SWIM = SV + '<circle cx="15.5" cy="10.5" r="1.9"/><path d="M12.5 13L4.5 13.5"/><path d="M12.5 13C12.5 8.5 17 6 21 8"/><path d="M2.5 18c1.5 0 2-1.3 3.4-1.3S7.6 18 9.2 18s1.9-1.3 3.4-1.3S14.4 18 15.9 18s1.9-1.3 3.3-1.3 1.8 1.3 2.3 1.3"/></svg>'

X7 = r'''
.dl{background:var(--card);border-radius:24px;box-shadow:var(--shadow);padding:2px 14px}
.dl .r{display:flex;align-items:center;gap:12px;padding:11px 0;border-top:1px solid var(--line)}
.dl .r:first-child{border-top:0}
.dl .dj{width:34px;flex:none;line-height:1.05}.dl .dj small{display:block;font-size:12px;font-weight:700;color:var(--mut)}.dl .dj b{font-size:18px;font-weight:800}
.dl .ic{width:40px;height:40px;border-radius:12px;flex:none;display:flex;align-items:center;justify-content:center}.dl .ic .mi{width:20px;height:20px}
.dl .ic.ef{background:#dcf7e8;color:#0b8f56}.dl .ic.cf{background:#ece7fe;color:#6a4fd0}.dl .ic.sl{background:#ffeedd;color:#d1601a}
.dl .tx{flex:1;min-width:0}.dl .tx b{display:block;font-size:16px;font-weight:800}.dl .tx span{font-size:13.5px;color:var(--mut)}
.dl .rep{font-size:16px;font-weight:700;color:var(--mut)}
.dl .r.today{background:#e3f5ec;margin:0 -10px;padding:11px 10px;border-radius:16px;border-top:0}
.tg{font:700 12px/1 Inter,sans-serif;border-radius:999px;padding:6px 9px;white-space:nowrap}
.tg.ok{background:var(--mintT);color:#fff}.tg.aj{background:#dcf7e8;color:#0b8f56}.tg.pc{background:#fde4e4;color:#c4302b}
.btng{margin-top:14px;border-radius:18px;padding:14px;text-align:center;font-weight:800;font-size:16px;background:var(--card);box-shadow:var(--shadow)}
.pick .grey{opacity:.38}
.why2{font-size:13px;color:var(--mut);margin-top:6px;line-height:1.45}
'''
B2.X = B2.X + X7


def r(j, n, ic_, cls, t, sub, tag='', today=False):
    if ic_ is None:
        return '<div class="r"><div class="dj"><small>%s</small><b>%s</b></div><div style="width:40px"></div><div class="rep">Repos</div></div>' % (j, n)
    return '<div class="r%s"><div class="dj"><small>%s</small><b>%s</b></div><span class="ic %s">%s</span><div class="tx"><b>%s</b><span>%s</span></div>%s</div>' % (
        ' today' if today else '', j, n, cls, ic(ic_), t, sub, tag)


def cal(sel='V'):
    return ('<div class="wk2 pick">' + jp('L', 23, '', '·', 'no') + jp('M', 24, 'done', ic('run'), 'no') + jp('M', 25, '', '·', 'no')
            + jp('J', 26, '', '·', 'no') + jp('V', 27, 'cf', ic('fitness'), 'sel' if sel == 'V' else '')
            + jp('S', 28, '', '·', 'sel' if sel == 'S' else '') + jp('D', 29, 'sl', ic('terrain')) + '</div>')


def a1():
    h = title('1', 'Onglet Semaine : le bouton du bas devient « Ajouter une séance »')
    h += ('<div class="fr" style="margin-bottom:4px"><div class="dl">'
          + r('Lun', 23, None, '', '', '')
          + r('Mar', 24, 'run', 'ef', 'Endurance', '47 min · fait', '<span class="tg ok">Fait</span>')
          + r('Mer', 25, None, '', '', '') + r('Jeu', 26, None, '', '', '')
          + r('Ven', 27, 'fitness', 'cf', 'Renforcement', 'aujourd\'hui · 45 min', '', True)
          + r('Sam', 28, None, '', '', '')
          + r('Dim', 29, 'terrain', 'sl', 'Sortie longue', '55 min · 150 m D+')
          + '</div><div class="btn2" style="margin-top:14px;padding:14px;font-size:16px;border-radius:18px"><span style="font-size:22px;line-height:1">+</span>Ajouter une séance</div></div>')
    h += '<div class="mini" style="margin:0 4px">Il remplace « Ajouter une séance prévue » (formulaire libre d\'aujourd\'hui). Les séances déjà ajoutées avec l\'ancien bouton restent.</div>'
    return B2.doc(h)


def a2():
    bike = '<div class="fopt"><span class="foi">' + BIKE + '</span><span class="fot"><b>Vélo</b><span>Tu choisis le jour</span></span><span class="ch">›</span></div>'
    s = (head('Ajouter une séance') + '<div class="mini" style="margin:-4px 4px 16px">Cette semaine · 23 au 29 nov.</div>'
         + fopt('run', 'Course à pied', 'L\'appli te propose la séance', True)
         + fopt('fitness', 'Renforcement', 'Tu choisis le jour') + bike
         + '<div class="fopt"><span class="foi">' + SWIM + '</span><span class="fot"><b>Natation</b><span>Tu choisis le jour</span></span><span class="ch">›</span></div>'
         + fopt('plus', 'Autre', 'Marche, randonnée, ski… Tu choisis le jour'))
    return pg(sheet(s), ('2', 'Choisir le type de séance'), h=640)


def a3():
    s = (head('Course à pied') + '<div class="mini" style="margin:-4px 4px 4px">Quel jour ?</div>' + cal('V')
         + '<div class="prop"><div class="mini">Proposition pour aujourd\'hui</div><div class="pt">Footing en plus · 35 min</div>'
         '<div class="tags"><span>Endurance</span><span>Plat</span><span>Facile, tu peux parler</span></div></div>'
         '<div class="why"><b>Pourquoi</b>Ton endurance de la semaine est faite (mardi, 47 min). Une séance en plus reste plus courte : 75 % de ton endurance au plus.</div>'
         '<div style="margin-top:10px">' + msg('!', 'Sortie longue dimanche, dans 2 jours : ni descente ni accélérations. Les courbatures de descente arrivent 1 à 3 jours après.') + '</div>'
         '<div class="btn pri" style="margin-top:12px">Ajouter à ma semaine</div><div class="lnk">Annuler</div>')
    return pg(sheet(s), ('3', 'Course à pied : l\'appli propose, avec le pourquoi et les alertes'), h=800)


def a4():
    h = title('4', 'Les autres cas de la course à pied')
    h += cas('A', 'Ton endurance de la semaine n\'est pas encore faite : on la déplace plutôt')
    h += ('<div class="fr">' + card('<div class="h2">Ton endurance n\'est pas faite</div><div class="mini" style="margin-top:6px">Prévue mercredi, 47 min. Plutôt que d\'ajouter une course, fais-la aujourd\'hui.</div>'
          '<div class="btn pri" style="margin-top:12px">Déplacer l\'endurance à aujourd\'hui</div><div class="lnk">Ajouter quand même un footing en plus</div>', 'p') + '</div>')
    h += cas('B', 'Déjà une séance en plus cette semaine')
    h += '<div class="fr">' + card(msg('i', 'Tu as déjà ajouté un footing mercredi. Une seule course en plus par semaine : la prochaine, à partir de lundi.'), 'p') + '</div>'
    h += cas('C', 'Les alertes possibles (elles informent, elles ne bloquent pas)')
    h += ('<div class="fr" style="margin-bottom:4px">' + card(
          msg('!', 'Lendemain de ta sortie longue : plutôt repos ou marche. Si tu cours, reste très facile.')
          + '<div style="height:8px"></div>' + msg('!', 'Veille de ta sortie longue : la moitié de ton endurance, 30 min au plus, pour arriver frais.')
          + '<div style="height:8px"></div>' + msg('!', 'Deuxième semaine de suite où une course remplace ton renforcement. En descente, tes cuisses freinent tout ton poids à chaque pas : le renforcement les rend plus solides pour encaisser.'), 'p') + '</div>')
    return B2.doc(h)


def a5():
    s = (head('Vélo') + '<div class="mini" style="margin:-4px 4px 4px">Quel jour ?</div>' + cal('S')
         + '<div class="res"><b>Samedi</b> : veille de ta sortie longue. Plutôt facile, pour garder des jambes fraîches.</div>'
         '<div class="mini" style="margin-top:10px">À toi de gérer ta charge. Une fois faite, tu la valides comme les autres (durée, effort, jambes sollicitées). Elle compte dans ta charge de la semaine, pas dans ta course à pied.</div>'
         '<div class="btn pri" style="margin-top:12px">Ajouter à ma semaine</div><div class="lnk">Annuler</div>')
    return pg(sheet(s), ('5', 'Vélo, renforcement, autre : tu choisis le jour, l\'appli enregistre'), h=560)


def a6():
    h = title('6', 'Dans la semaine : la séance porte « Ajoutée »')
    h += ('<div class="fr" style="margin-bottom:4px"><div class="dl">'
          + r('Ven', 27, 'run', 'ef', 'Footing', 'aujourd\'hui · 35 min · plat', '<span class="tg aj">Ajoutée</span>', True)
          + r('', '', 'fitness', 'cf', 'Renforcement', '45 min', '<span class="tg pc">Pas faite</span>')
          + r('Sam', 28, None, '', '', '')
          + r('Dim', 29, 'terrain', 'sl', 'Sortie longue', '55 min · 150 m D+')
          + '</div></div>')
    h += '<div class="mini" style="margin:0 4px">Se valide comme une autre séance. Se supprime tant qu\'elle n\'est pas faite. Ne change pas le reste du plan.</div>'
    return B2.doc(h)


def a7():
    h = title('7', 'Garde-fous sur le choix du jour (course à pied)')
    calg = ('<div class="wk2 pick">' + jp('L', 23, '', '·', 'grey') + jp('M', 24, 'done', ic('run'), 'grey') + jp('M', 25, '', '·', 'grey')
            + jp('J', 26, '', '·', 'grey') + jp('V', 27, 'cf', ic('fitness'), 'sel') + jp('S', 28, '', '·') + jp('D', 29, 'sl', ic('terrain'), 'grey') + '</div>')
    h += cas('A', 'Les jours grisés ne se choisissent pas')
    h += ('<div class="fr">' + card(calg + '<div class="why2">Grisés : les jours passés, le jour de ta sortie longue et les jours où une course est déjà prévue.</div>', 'p') + '</div>')
    h += cas('B', 'Tu touches dimanche (sortie longue)')
    h += '<div class="fr">' + card(msg('i', 'Dimanche, c\'est ta sortie longue : pas de course en plus ce jour-là. Si tu veux courir plus longtemps, c\'est la sortie longue qui grandit, d\'une semaine à l\'autre.'), 'p') + '</div>'
    h += cas('C', 'Tu touches samedi (veille de la sortie longue) : possible, en plus court (50 % de l\'endurance, 30 min au plus)')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="prop" style="margin-top:0"><div class="pt">Footing · 25 min</div><div class="tags"><span>Endurance</span><span>Plat</span><span>Très facile</span></div></div>'
          '<div style="margin-top:10px">' + msg('!', 'Veille de ta sortie longue : la moitié de ton endurance, 30 min au plus, pour arriver frais.') + '</div>', 'p') + '</div>')
    return B2.doc(h)


EXPORT = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7']
