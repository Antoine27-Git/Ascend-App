"""Lot « saisie 3 » (24/11/2026) : retours d'Antoine sur la v75.
Étape 1 qui relit la montre, étape 2 en cases (plus de répétition de l'étape 1), un seul champ « Ta perception »,
deux séances le même jour dans la semaine, liste « Déplacer » avec Aujourd'hui / Demain / jours.
python3 render.py screens_saisie3
"""
from screens_bilan2 import *
from screens_bilan2 import X as X2
import screens_bilan2 as B2

X3 = r"""
.spin{width:34px;height:34px;border-radius:50%;border:3.5px solid var(--mintBg);border-top-color:var(--mintT);margin:4px auto 10px}
.tl{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.tl4{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:10px}
.tc{background:var(--card);border-radius:16px;box-shadow:var(--shadow);padding:10px 12px}
.tc small{display:block;font-size:11.5px;color:var(--mut);font-weight:600}
.tc b{font-size:19px;font-weight:800;letter-spacing:-.02em;white-space:nowrap}
.tc b span{font-size:12px;font-weight:600;color:var(--mut)}
.tl4 .tc{padding:9px 6px;text-align:center}.tl4 .tc b{font-size:16px}.tl4 .tc small{font-size:11px}
.okh{display:flex;align-items:center;gap:10px}
.okh i{flex:none;width:28px;height:28px;border-radius:50%;background:var(--mintBg);color:var(--mintT);display:flex;align-items:center;justify-content:center;font-style:normal;font-weight:800}
.ta{background:var(--card);border-radius:13px;box-shadow:inset 0 0 0 1.5px var(--mintT);padding:11px 12px;font-size:15.5px;line-height:1.45;min-height:64px}
.ta .cur{display:inline-block;width:1.5px;height:17px;background:var(--mintT);vertical-align:-3px}
.cnt{font-size:11.5px;color:var(--mut);text-align:right;margin-top:5px}
.quote{border-left:3px solid var(--mintBg);padding:2px 0 2px 11px;font-size:14px;line-height:1.5}
.wk2{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;margin-top:10px;text-align:center}
.wk2 div{display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 0 7px;border-radius:14px}
.wk2 .l{font-size:11.5px;color:var(--mut);font-weight:700}.wk2 .nm{font-size:15px;font-weight:800}
.wk2 .d{width:30px;height:30px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--mut);font-weight:800}
.wk2 .d .mi{width:18px;height:18px}
.wk2 .on{box-shadow:inset 0 0 0 1.5px var(--mintT);background:#eefaf3}
.wk2 .ef{background:#dcf7e8;color:#0b8f56}.wk2 .sl{background:#ffeedd;color:#d1601a}.wk2 .cf{background:#ece7fe;color:#6a4fd0}.wk2 .done{background:var(--mintT);color:#fff}
.wk2 .two{position:relative;width:30px;height:30px}
.wk2 .two .d{position:absolute;inset:0}
.wk2 .two .bdg{position:absolute;right:-9px;top:-8px;width:19px;height:19px;border-radius:50%;background:#ece7fe;color:#6a4fd0;box-shadow:0 0 0 2px #eefaf3;display:flex;align-items:center;justify-content:center}
.wk2 .two .bdg .mi{width:12px;height:12px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.chips span{background:var(--chip);border-radius:12px;padding:9px 13px;font-size:14.5px;font-weight:700}
.chips span small{font-weight:600;color:var(--mut);font-size:12.5px}
.bad{font:700 12px/1 Inter,sans-serif;color:#b8352d;background:#fde9e7;border-radius:6px;padding:3px 7px;margin:0 4px 8px;display:inline-block}
"""
B2.X = X2 + X3


def pg(inner, tag, h=760):
    return B2.page(inner, 'light', tag, h=h)


def sheet(inner, foot=''):
    return B2.BEHIND + '<div class="sheetb"><div class="grab"></div><div class="pad">' + inner + '</div>' + foot + '</div>'


# ---------- 1. Étape 1 : la montre est relue à l'ouverture ----------
def s3_1a():
    s = (head('Valider ma séance') + '<div style="padding:0 4px">' + steps(1) + '</div>'
         + '<div class="sec">Ta montre</div>'
         + card('<div class="spin"></div><div style="text-align:center;font-weight:700">Recherche de ta sortie…</div>'
                '<div class="mini" style="text-align:center;margin-top:4px">Lecture de tes activités des 7 derniers jours.</div>', 'p')
         + '<div class="or">ou</div><div class="btn sec" style="background:var(--chip);box-shadow:none">Saisir à la main</div>'
         '<div class="mini" style="margin-top:8px;text-align:center">Sans montre, ou pour une autre activité (renforcement, vélo…).</div>')
    return pg(sheet(s), ('1a', 'Étape 1 : la montre est relue à l\'ouverture'), h=560)


def s3_1b():
    s = (head('Valider ma séance') + '<div style="padding:0 4px">' + steps(1) + '</div>'
         + '<div class="sec">Ta montre</div>'
         + card('<div class="row"><div class="wicon">' + WATCH + '</div><div><div style="font-weight:800;font-size:16px">Pas encore arrivée</div>'
                '<div class="mini">Garmin envoie tes sorties à intervals.icu en quelques minutes, parfois plus.</div></div></div>'
                '<div class="btn pri" style="margin-top:12px">Réessayer</div>', 'p')
         + '<div class="mini" style="margin:10px 4px 0">Lu à l\'instant</div>'
         '<div class="or">ou</div><div class="btn sec" style="background:var(--chip);box-shadow:none">Saisir à la main</div>'
         '<div class="mini" style="margin-top:8px;text-align:center">Sans montre, ou pour une autre activité (renforcement, vélo…).</div>')
    return pg(sheet(s), ('1b', 'Étape 1 : sortie pas encore arrivée'), h=600)


# ---------- 2. Étape 2 : les mesures en cases, puis ta perception ----------
TEXTE = 'Jambes lourdes les 20 premières minutes.<br>Bien mieux dans la 2e montée, j\'ai relancé sur le plat.<span class="cur"></span>'


def perception():
    return ('<div class="sec">Ta perception</div>'
            + card('<div class="lbl" style="margin-top:0"><span>Effort ressenti</span><small>toute la séance</small></div>' + rpe10(3)
                   + '<div class="mini" style="margin-top:7px;display:flex;justify-content:space-between"><span>1 très facile</span><b style="color:var(--mintT)">3 · modéré</b><span>10 maximal</span></div>'
                   '<div class="lbl"><span>Ce que tu as ressenti</span><small>facultatif</small></div>'
                   '<div class="ta">' + TEXTE + '</div><div class="cnt">96 / 600</div>'
                   '<div class="mini" style="margin-top:6px">Si tu demandes l\'analyse, l\'IA confronte ce que tu as écrit aux données de ta sortie.</div>', 'p'))


def entete():
    return ('<div class="sec">Lu sur ta montre</div>'
            '<div class="okh" style="padding:0 4px"><i>✓</i><div><div style="font-weight:800;font-size:16px">Lozanne Trail</div><div class="mini">Aujourd\'hui · course à pied</div></div></div>')


COMPTE = ('<div class="cd" style="margin-top:8px"><div class="kv"><span>Compte pour</span><b>Endurance prévue<br><small>37 min, aujourd\'hui · <span class="lk">Changer</span></small></b></div></div>'
          '<div class="mini" style="margin:8px 4px 0">Une donnée est fausse ? <span class="lk">Corriger</span></div>')


def s3_2a():
    s = (head('Valider ma séance') + '<div style="padding:0 4px">' + steps(2) + '</div>' + entete()
         + '<div class="tl"><div class="tc"><small>Durée</small><b>1 h 15</b></div><div class="tc"><small>Distance</small><b>11,6 <span>km</span></b></div>'
         '<div class="tc"><small>D+</small><b>180 <span>m</span></b></div><div class="tc"><small>FC moyenne</small><b>160 <span>bpm</span></b></div></div>'
         + COMPTE + perception())
    return pg(sheet(s, '<div class="foot"><div class="btn pri">Valider</div></div>'), ('2A', 'Étape 2 : 4 cases sur 2 lignes'), h=1080)


def s3_2b():
    s = (head('Valider ma séance') + '<div style="padding:0 4px">' + steps(2) + '</div>' + entete()
         + '<div class="tl4"><div class="tc"><small>Durée</small><b>1 h 15</b></div><div class="tc"><small>Distance</small><b>11,6</b><small>km</small></div>'
         '<div class="tc"><small>D+</small><b>180</b><small>m</small></div><div class="tc"><small>FC moy.</small><b>160</b><small>bpm</small></div></div>'
         + COMPTE + perception())
    return pg(sheet(s, '<div class="foot"><div class="btn pri">Valider</div></div>'), ('2B', 'Étape 2 : 4 cases sur une ligne'), h=1040)


# ---------- 3. Bilan : « L'analyse » reprend ta perception, plus de second champ ----------
def s3_3():
    h = title('3', 'Bilan : « L\'analyse », un seul texte (celui de l\'étape 2)')
    h += cas('A', 'Tu as écrit quelque chose')
    h += ('<div class="fr">' + card('<div class="mini" style="margin-bottom:6px">Ta perception</div><div class="quote">Jambes lourdes les 20 premières minutes.<br>Bien mieux dans la 2e montée, j\'ai relancé sur le plat.</div>'
          '<div class="btn pri" style="margin-top:12px">Analyser la séance</div><div class="mini" style="margin-top:8px;text-align:center">L\'IA confronte ta perception aux données. Seulement si tu appuies.</div>', 'p') + '</div>')
    h += cas('B', 'Tu n\'as rien écrit')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="kv" style="padding-top:0"><span>Ta perception</span><b style="font-weight:600;color:var(--mut)">non renseignée · <span class="lk" style="color:var(--mintT);font-weight:800">Ajouter</span></b></div>'
          '<div class="btn pri" style="margin-top:10px">Analyser la séance</div><div class="mini" style="margin-top:8px;text-align:center">L\'IA analyse les données et ton effort ressenti. Seulement si tu appuies.</div>', 'p') + '</div>')
    return B2.doc(h)


# ---------- 4. Semaine : deux séances le même jour ----------
def jour(l, n, cls, inner, on=False):
    return '<div class="%s"><span class="l">%s</span><span class="nm">%s</span>%s</div>' % ('on' if on else '', l, n, inner if cls is None else '<span class="d %s">%s</span>' % (cls, inner))


def semaine(mardi):
    return ('<div class="sb"><div class="h2">Cette semaine</div><div class="mini"><b style="color:var(--ink)">1/4</b> séances</div></div><div class="wk2">'
            + jour('L', 23, '', '·') + mardi + jour('M', 25, '', '·') + jour('J', 26, '', '·')
            + jour('V', 27, 'cf', ic('fitness')) + jour('S', 28, '', '·') + jour('D', 29, 'sl', ic('terrain')) + '</div>')


def s3_4():
    h = title('4', 'Semaine : endurance déplacée sur le jour du renforcement')
    h += '<span class="bad">Aujourd\'hui (v76)</span>'
    h += '<div class="fr">' + card(semaine(jour('M', 24, 'done', ic('run'), True)), 'p') + '</div>'
    h += cas('→', 'Le renforcement a disparu de la case')
    h += cas('P', 'Proposé : la séance de course reste en grand, le renforcement s\'ajoute en pastille')
    deux = '<div class="two"><span class="d done">' + ic('run') + '</span><span class="bdg">' + ic('fitness') + '</span></div>'
    h += '<div class="fr" style="margin-bottom:4px">' + card(semaine(jour('M', 24, None, deux, True)), 'p') + '</div>'
    h += '<div class="mini" style="margin:0 4px">Endurance faite (vert plein), renforcement prévu (violet). Un appui ouvre la journée.</div>'
    return B2.doc(h)


# ---------- 5. Déplacer : Aujourd'hui, Demain, puis les jours ----------
def s3_5():
    h = title('5', 'Déplacer : Aujourd\'hui, Demain, puis les jours, sans date')
    h += '<span class="bad">Aujourd\'hui (v76)</span>'
    h += ('<div class="fr">' + card('<div class="h2">Déplacer cette semaine</div><div class="mini" style="margin-top:8px">Choisis un jour. Un jour déjà couru échange les deux séances :</div>'
          '<div class="chips"><span>mar. 24</span><span>jeu. 26</span><span>ven. 27</span><span>sam. 28 · veille de SL</span></div>', 'p') + '</div>')
    h += cas('P', 'Proposé : ton cas (séance prévue mercredi, ouverte le mardi)')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="h2">Déplacer cette semaine</div><div class="mini" style="margin-top:8px">Choisis un jour. Un jour déjà couru échange les deux séances :</div>'
          '<div class="chips"><span>Aujourd\'hui</span><span>Jeudi</span><span>Vendredi</span><span>Samedi <small>· veille de ta sortie longue</small></span></div>'
          '<div class="mini" style="margin-top:10px">Demain n\'apparaît pas : c\'est déjà le jour de la séance.</div>', 'p') + '</div>')
    h += cas('P', 'Autre cas : séance prévue jeudi, ouverte le mardi')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="chips" style="margin-top:0"><span>Aujourd\'hui</span><span>Demain</span><span>Vendredi</span><span>Samedi <small>· veille de ta sortie longue</small></span></div>', 'p') + '</div>')
    return B2.doc(h)


EXPORT = ['s3_1a', 's3_1b', 's3_2a', 's3_2b', 's3_3', 's3_4', 's3_5']


# ---------- 6. Déplacer : choisir dans le calendrier de la semaine ----------
X3b = r"""
.pick div{cursor:pointer}
.pick .no{opacity:.38}
.pick .sel{background:var(--mintBg);box-shadow:inset 0 0 0 2px var(--mintT)}
.pick .sel .nm{color:var(--mintT)}
.res{margin-top:12px;border-top:1px solid var(--line);padding-top:10px;font-size:14px;line-height:1.45}
.res b{font-weight:800}
"""
B2.X = B2.X + X3b


def jp(l, n, cls, inner, st=''):
    return '<div class="%s"><span class="l">%s</span><span class="nm">%s</span>%s</div>' % (st, l, n, '<span class="d %s">%s</span>' % (cls, inner) if cls is not None else inner)


def s3_6():
    h = title('6', 'Déplacer : choisir dans le calendrier de la semaine')
    two = '<div class="two"><span class="d cf">' + ic('fitness') + '</span></div>'
    cal = ('<div class="wk2 pick">'
           + jp('L', 23, 'done', ic('run'), 'no') + jp('M', 24, 'cf', ic('fitness'), 'sel') + jp('M', 25, 'ef', ic('run'), 'from')
           + jp('J', 26, '', '·') + jp('V', 27, 'cf', ic('fitness')) + jp('S', 28, '', '·') + jp('D', 29, 'sl', ic('terrain')) + '</div>')
    h += cas('A', 'Endurance prévue mercredi, ouverte le mardi : tu touches mardi')
    h += ('<div class="fr">' + card('<div class="h2">Déplacer l\'endurance</div><div class="mini" style="margin-top:6px">Touche le jour voulu. Lundi est passé. Le jour choisi est cerclé vert.</div>'
          + cal + '<div class="res"><b>Mardi, aujourd\'hui</b> : avec ton renforcement. Possible, les deux le même jour.</div>'
          '<div class="btn pri" style="margin-top:12px">Déplacer à aujourd\'hui</div>', 'p') + '</div>')
    h += cas('B', 'Si tu touches un jour de course : échange · si tu touches samedi : veille de ta sortie longue')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="res" style="border-top:0;margin-top:0;padding-top:0"><b>Samedi</b> : veille de ta sortie longue. Tu l\'aborderas les jambes un peu entamées.</div>'
          '<div class="btn pri" style="margin-top:12px">Déplacer à samedi</div>', 'p') + '</div>')
    return B2.doc(h)


# ---------- 7. Bilan sans perception : le champ est déjà là, vide ----------
def s3_7():
    h = title('7', 'Bilan, rien d\'écrit à l\'étape 2 : le champ est là, vide')
    h += ('<div class="fr" style="margin-bottom:4px">' + card('<div class="lbl" style="margin-top:0"><span>Ce que tu as ressenti</span><small>facultatif</small></div>'
          '<div class="field" style="height:64px;align-items:flex-start;padding-top:11px"><span class="ph">Ex. : jambes lourdes au début, mieux en montée…</span></div>'
          '<div class="btn pri" style="margin-top:12px">Analyser la séance</div><div class="mini" style="margin-top:8px;text-align:center">Rempli : l\'IA confronte ta perception aux données. Vide : elle analyse les données et ton effort ressenti.</div>', 'p') + '</div>')
    return B2.doc(h)


EXPORT = EXPORT + ['s3_6', 's3_7']
