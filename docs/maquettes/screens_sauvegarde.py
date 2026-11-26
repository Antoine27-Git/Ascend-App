"""Lot « sauvegarde » (25/11/2026) : rappel d'export (P-27) et restauration sûre (P-24).
python3 render.py screens_sauvegarde
"""
from screens_renfo import *
import screens_bilan2 as B2

X6 = r"""
.ph{padding:6px 4px 0}.ph h1{font-size:26px;font-weight:800;letter-spacing:-.02em;margin:0 0 4px}
.warn{display:flex;gap:10px;align-items:flex-start;background:#fff4e0;color:#8a5a00;border-radius:14px;padding:10px 12px;font-size:14px;line-height:1.4;margin-top:10px}
.warn b{font-weight:800}
.drop{border:1.5px dashed #b9c7bf;border-radius:16px;padding:18px 14px;text-align:center;color:var(--mut);font-size:14px;margin-top:10px}
.drop b{display:block;color:var(--ink);font-size:16px;margin-bottom:4px}
.cmp{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.cmp>div{background:var(--card);border-radius:16px;box-shadow:var(--shadow);padding:10px 12px}
.cmp small{display:block;font-size:12px;color:var(--mut);font-weight:600}.cmp b{font-size:18px;font-weight:800}
.row2{display:flex;justify-content:space-between;align-items:center;font-size:14.5px;padding:9px 0;border-top:1px solid var(--line)}
.row2:first-child{border-top:0}.row2 span{color:var(--mut)}
"""
B2.X = B2.X + X6


def ecran(inner, tag, h=760):
    return pg('<div class="pad">' + inner + '</div>', tag, h=h)


def s5_1():
    s = ('<div class="ph"><div class="mini">‹ Profil</div><h1>Données et synchro</h1></div>'
         + '<div class="sec">Ta sauvegarde</div>'
         + card('<div class="row2"><span>Dernier export</span><b>16 nov. · il y a 9 jours</b></div>'
                '<div class="btn pri" style="margin-top:10px">Exporter mes données</div>'
                '<div class="mini" style="margin-top:8px">Un fichier .json à garder hors du téléphone (mail, drive). Ton compte en ligne reste ta sauvegarde principale.</div>', 'p')
         + '<div class="sec">Restaurer une sauvegarde</div>'
         + card('<div class="mini">Remet dans l\'appli le contenu d\'un fichier exporté. Tu choisis ensuite ce qui est gardé.</div>'
                '<div class="btn sec" style="margin-top:10px;background:var(--chip);box-shadow:none">Choisir un fichier…</div>', 'p'))
    return ecran(s, ('1', 'Profil › Données : la date du dernier export, en clair'), h=640)


def s5_2():
    s = ('<div class="ph"><div class="mini">‹ Profil</div><h1>Profil</h1></div>'
         + card('<div class="row2"><span>Objectifs et courses</span><b>›</b></div>'
                '<div class="row2"><span>Jours et organisation</span><b>›</b></div>'
                '<div class="row2"><span>Données et synchro</span><b>›</b></div>'
                '<div class="warn"><span>!</span><div><b>Dernier export il y a 35 jours.</b> Exporte tes données : 1 minute, en cas de souci avec ton compte.</div></div>', 'p'))
    return ecran(s, ('2', 'Plus de 30 jours sans export : un rappel discret dans Profil'), h=470)


def s5_3():
    s = (head('Restaurer une sauvegarde') + '<div class="mini" style="margin:-4px 4px 12px">ascend-2026-11-16.json</div>'
         + '<div class="cmp"><div><small>Dans le fichier (16 nov.)</small><b>12 séances</b></div><div><small>Dans ton appli</small><b>15 séances</b></div></div>'
         + '<div class="mini" style="margin:10px 4px 14px">2 séances du fichier manquent dans l\'appli. 5 séances de l\'appli sont plus récentes que le fichier.</div>'
         + fopt('plus', 'Ajouter ce qui manque', 'Ajoute les 2 séances absentes. Ne supprime rien, garde ton profil actuel.', True)
         + fopt('close', 'Remplacer tout par le fichier', '5 séances récentes seront supprimées, ici et sur ton compte.'))
    return pg(sheet(s), ('3', 'Restaurer : on voit ce qui change, « ajouter » par défaut'), h=640)


def s5_4():
    s = (head('Remplacer tout ?') + '<div class="warn" style="margin-top:0"><span>!</span><div><b>5 séances seront supprimées</b>, ici et sur ton compte : 18, 20, 22, 24 et 25 nov.</div></div>'
         + '<div class="mini" style="margin:12px 4px">Avant de remplacer, l\'appli télécharge ta version actuelle (ascend-2026-11-25.json). Tu pourras revenir en arrière.</div>'
         + '<div class="btn pri" style="background:#b8352d;color:#fff">Télécharger puis remplacer</div>'
         + '<div class="btn sec" style="margin-top:10px;background:var(--chip);box-shadow:none">Annuler</div>')
    return pg(sheet(s), ('4', '« Remplacer tout » : une confirmation, et une copie de sécurité d\'abord'), h=520)


EXPORT = ['s5_1', 's5_2', 's5_3', 's5_4']
