from base import *
from screens_v2 import head, fact3, legend, line, sheet, FOOT
from screens_profil import sw
from screens_log import BEHIND, rpe_grid
NUT_CARD = ('<div class="card" style="margin:10px 0 0;padding:12px 16px"><div class="row"><div class="ic nut" style="width:40px;height:40px;border-radius:12px">%s</div><div style="flex:1"><div style="font-weight:800;font-size:15px">35 g de glucides par heure</div><div class="mini">≈ 64 g sur la séance · boisson ≈ 1,1 l</div></div></div></div>') % ic('nutrition')
WHY = '<div class="card" style="margin:10px 0 0;padding:13px 16px"><div class="h2">Pourquoi</div><div style="font-size:14px;line-height:1.4;margin-top:4px;color:var(--mut)">La seule séance qui progresse cette semaine (+10 % au plus sur ta plus longue des 30 derniers jours).</div></div>'

def fiche_long():
    inner = (head('Sortie longue', 'Aujourd\'hui · dimanche 18 oct.')
      + '<div class="card" style="margin:12px 0 0;padding:13px 16px">' + fact3([('1 h 50', 'durée'), ('200–300', 'm de D+'), ('Facile', 'effort')]) + '</div>'
      + '<div class="card" style="margin:10px 0 0"><div class="h2">À faire</div>'
      + '<div style="font-size:17px;font-weight:800;margin-top:8px">1 h 50 d\'endurance continue</div>'
      + line('run', 'Tu peux parler tout du long. Départ tranquille : les premières minutes servent d\'échauffement.')
      + line('terrain', 'D+ : environ 200 à 300 m, sans le chercher. Montées raides marchées.')
      + line('monitoring', 'FC : zone facile. Le ressenti décide, la FC confirme.') + '</div>'
      + WHY + NUT_CARD)
    return page(sheet(inner, FOOT), 'light', ('1', 'Sortie longue : un seul bloc, sans échauffement ni retour au calme'), reco=True)

def fiche_cotes():
    segs = [(15, '#f3c9a6'), (14, '#ff7a3d'), (11, '#f3c9a6')]
    b = '<div style="display:flex;gap:3px;height:12px;margin:12px 0 10px">' + ''.join('<div style="flex:%s;background:%s;border-radius:6px"></div>' % s for s in segs) + '</div>'
    inner = (head('Côtes courtes 6 × 30 s', 'Mardi 20 oct.', 'terrain', 'cf')
      + '<div class="card" style="margin:12px 0 0;padding:13px 16px">' + fact3([('45 min', 'durée'), ('100–200', 'm de D+'), ('Soutenu', 'effort')]) + '</div>'
      + '<div class="card" style="margin:10px 0 0"><div class="h2">À faire</div>' + b
      + legend([('#f3c9a6', '15 min', 'Échauffement progressif'), ('#ff7a3d', '6 × 30 s', 'Montée vive, redescente en marchant'), ('#f3c9a6', '10 min', 'Retour au calme')])
      + line('terrain', 'Côte raide, vite mais relâché. Récupération complète en redescendant.') + '</div>'
      + WHY)
    return page(sheet(inner, FOOT), 'light', ('2', 'Côtes ou fractionné : échauffement et retour au calme gardés'))

def saisie(on):
    fields = ('<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px"><div><div class="f">Glucides pris</div><div class="field">30<span class="mut" style="margin-left:auto;font-size:14px">g</span></div></div>'
              '<div><div class="f">Boisson</div><div class="field">800<span class="mut" style="margin-left:auto;font-size:14px">ml</span></div></div></div>'
              '<div class="lbl" style="margin-top:14px"><span>Inconfort digestif</span></div><div class="grid5" style="grid-template-columns:repeat(4,1fr)">'
              + ''.join('<div class="n%s" style="height:44px;font-size:13.5px">%s</div>' % (' on' if i == 0 else '', t) for i, t in enumerate(['Aucun', 'Léger', 'Gênant', 'Arrêt'])) + '</div>'
              '<div class="f" style="margin-top:14px">Détail de ce que tu as pris</div><div class="field" style="height:64px;align-items:flex-start;padding-top:10px;font-size:14.5px;line-height:1.35">2 compotes Pom\'Potes, 1 purée patate douce, 1 gel Maurten à 1 h 20</div>') if on else \
             '<div class="mini" style="margin-top:10px;line-height:1.45">Cette sortie ne compte pas dans la progression de ta cible.</div>'
    sh = ('<div class="sheet" style="top:70px"><div class="grab"></div><div style="padding:8px 16px 0">'
          '<div class="sb" style="align-items:center"><div><div class="ttl" style="font-size:20px">Sortie longue</div><div class="meta">Aujourd\'hui · prévue 1 h 50</div></div><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>'
          '<div class="lbl" style="margin-top:12px"><span>Effort ressenti</span><small>à froid, 30 min après</small></div>'
          + '<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:4px">' + ''.join('<div class="n%s" style="height:40px;font-size:14.5px">%d</div>' % (' on' if i == 4 else '', i) for i in range(1, 11)) + '</div>'
          + '<div class="mini" style="display:flex;justify-content:space-between;margin-top:6px"><span>1 très facile</span><b style="color:var(--mintT)">4 · Assez dur</b><span>10 maximal</span></div>'
          + '<div class="lbl"><span>Nutrition</span><small>cible 35 g/h, soit 64 g</small></div>'
          '<div class="card" style="margin:0;padding:12px 14px;box-shadow:inset 0 0 0 1.5px var(--line)"><div style="display:flex;align-items:center;gap:12px"><div style="flex:1"><div style="font-weight:700;font-size:15px">J\'ai suivi ma nutrition</div><div class="mini">sur cette séance</div></div>' + sw(on) + '</div>' + fields + '</div>'
          '</div><div class="foot"><div class="btn pri">Enregistrer</div></div></div>')
    return page(BEHIND + '<div class="dim"></div>' + sh, 'light', ('3' if on else '4', 'Saisie : nutrition suivie' if on else 'Saisie : nutrition non suivie sur cette séance'))
def saisie_on(): return saisie(True)
def saisie_off(): return saisie(False)
EXPORT = ['fiche_long', 'fiche_cotes', 'saisie_on', 'saisie_off']
