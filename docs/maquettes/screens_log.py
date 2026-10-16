from base import *

BEHIND = ('<div class="halo"><i class="a"></i><i class="b"></i></div>'
          + header('Dimanche 18 octobre', 'Semaine 4 · Reprise')
          + '<div class="card" style="height:300px"></div>')

def rpe_grid(sel=None):
    r1 = ''.join('<div class="n%s">%d</div>' % (' on' if sel == i else '', i) for i in range(0, 6))
    r2 = ''.join('<div class="n%s">%d</div>' % (' on' if sel == i else '', i) for i in range(6, 11))
    return '<div class="grid6">' + r1 + '</div><div class="grid5" style="margin-top:6px">' + r2 + '</div>'

def chips5(sel=None, h=44):
    return '<div class="grid5">' + ''.join('<div class="n%s" style="height:%dpx">%d</div>' % (' on' if sel == i else '', h, i) for i in range(1, 6)) + '</div>'

def log_A():
    sheet = ('<div class="sheet" style="top:70px"><div class="grab"></div><div style="padding:8px 16px 0">'
             '<div class="sb" style="align-items:center"><div><div class="ttl" style="font-size:20px">Sortie longue</div><div class="meta">Aujourd\'hui · prévue 1 h 50 · 300 m de D+</div></div><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>'
             '<div class="lbl" style="margin-top:14px"><span>Comme prévu ?</span></div>'
             '<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:8px"><div class="opt on"><b>Oui</b><span>1 h 50 · 300 m D+</span></div><div class="opt"><b>Non</b><span>je corrige</span></div></div>'
             '<div class="lbl"><span>Effort ressenti</span><small>toute la séance, à froid</small></div>'
             + rpe_grid(4) +
             '<div class="mini" style="margin-top:7px;display:flex;justify-content:space-between"><span>0 repos</span><b style="color:var(--mintT)">4 · assez dur</b><span>10 maximal</span></div>'
             '<div class="lbl"><span>Nutrition</span><small>cible 15 g/h, soit 28 g</small></div>'
             '<div style="display:grid;grid-template-columns:1fr 1.5fr;gap:10px;align-items:end"><div><div class="f">Glucides pris</div><div class="field">30<span class="mut" style="margin-left:auto;font-size:14px">g</span></div></div>'
             '<div><div class="f">Digestion</div><div class="grid5" style="gap:4px">' + ''.join('<div class="n%s" style="height:46px;font-size:15px">%d</div>' % (' on' if i == 4 else '', i) for i in range(1, 6)) + '</div></div></div>'
             '<div class="sb" style="margin-top:14px;padding:12px 2px;border-top:1px solid var(--line)"><span style="font-weight:700;font-size:14.5px">Plus de détails</span><span class="mini">trace, distance, note ›</span></div>'
             '</div><div class="foot"><div class="btn pri">Enregistrer</div></div></div>')
    body = BEHIND + '<div class="dim"></div>' + sheet
    return page(body, 'light', ('A', 'Saisie : « Comme prévu » + effort'), reco=True)

def log_A_after():
    toast = ('<div style="position:absolute;left:14px;right:14px;bottom:88px;background:var(--deep);color:#fff;border-radius:18px;padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.25)">'
             '<div style="font-weight:800;font-size:15px">Sortie longue enregistrée</div>'
             '<div style="font-size:13.5px;opacity:.85;margin-top:3px;line-height:1.4">Effort 4 noté. Prochaine sortie longue : jusqu\'à 2 h, dimanche 25 octobre.</div></div>')
    body = ('<div class="halo"><i class="a"></i><i class="b"></i></div><div class="scroll">'
            + header('Dimanche 18 octobre', 'Semaine 4 · Reprise')
            + '<div class="card"><div class="k">Aujourd\'hui</div><div class="row" style="margin-top:10px"><div class="ic sl">%s</div><div style="flex:1"><div class="ttl">Sortie longue</div><div class="meta">1 h 50 · 300 m de D+</div></div><span class="pill ok">Fait</span></div>'
            '<div class="why"><span>Ensuite · </span>Repos lundi, renforcement mardi.</div></div>' % ic('terrain')
            + '</div>' + toast + nav(["Aujourd'hui", 'Semaine', 'Suivi', 'Profil'], "Aujourd'hui"))
    return page(body, 'light', ('A', 'Après Enregistrer : ce que le plan en fait'), h=520)

def log_B():
    sheet = ('<div class="sheet" style="top:70px"><div class="grab"></div><div style="padding:8px 16px 0">'
             '<div class="sb" style="align-items:center"><div class="ttl" style="font-size:20px">Sortie longue</div><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>'
             '<div class="mini" style="margin-top:2px">dim. 18 oct. · <u>changer</u></div>'
             '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px">'
             '<div><div class="f">Durée (min)</div><div class="field">110</div></div><div><div class="f">D+ (m)</div><div class="field">300</div></div><div><div class="f">Distance</div><div class="field"><span class="ph">km</span></div></div></div>'
             '<div class="lbl"><span>Effort ressenti</span><small>à froid, 30 min après</small></div>'
             + rpe_grid() +
             '<div class="mini" style="margin-top:7px;display:flex;justify-content:space-between"><span>0 repos · 2 facile</span><span>5 dur · 7 très dur · 10 max</span></div>'
             '<div class="lbl"><span>Jambes</span><small>1 lourdes · 5 fraîches</small></div>' + chips5() +
             '<div class="sb" style="margin-top:12px;padding:12px 2px;border-top:1px solid var(--line)"><span style="font-weight:700;font-size:14.5px">Nutrition</span><span class="mini">cible 28 g ›</span></div>'
             '<div class="sb" style="padding:12px 2px;border-top:1px solid var(--line)"><span style="font-weight:700;font-size:14.5px">Trace et note</span><span class="mini">›</span></div>'
             '</div><div class="foot"><div class="btn pri">Enregistrer</div></div></div>')
    body = BEHIND + '<div class="dim"></div>' + sheet
    return page(body, 'light', ('B', 'Saisie : formulaire actuel réorganisé'))

def log_C():
    labels = ['Repos', 'Très facile', 'Facile', 'Modéré', 'Assez dur', 'Dur', 'Dur +', 'Très dur', 'Très dur +', 'Extrême', 'Maximal']
    rows = ''.join('<div style="display:flex;align-items:center;gap:12px;height:44px;border-top:1px solid var(--line)"><div class="n" style="width:44px;height:36px;font-size:15px">%d</div><div style="font-size:15px;font-weight:%s">%s</div></div>' % (i, '700' if labels[i] else '400', labels[i] or '<span class="mut">·</span>') for i in range(11))
    sheet = ('<div class="sheet" style="top:46px"><div class="grab"></div><div style="padding:8px 16px 0">'
             '<div class="sb" style="align-items:center"><span class="mini"><b style="color:var(--ink)">2/2</b> · Sortie longue</span><div class="chip" style="width:40px;height:40px;font-size:20px">×</div></div>'
             '<div class="ttl" style="margin-top:4px">Comment c\'était ?</div><div class="meta" style="margin-bottom:8px">Toute la séance, à froid. Un toucher enregistre.</div>'
             + rows + '</div></div>')
    body = BEHIND + '<div class="dim"></div>' + sheet
    return page(body, 'light', ('C', 'Saisie en étapes : 1 question par écran'))

EXPORT = ['log_A', 'log_A_after', 'log_B', 'log_C']
