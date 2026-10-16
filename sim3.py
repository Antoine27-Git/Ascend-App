"""
sim3.py — RECONSTRUCTION MINIMALE du 23/09/2026.
L'original (17/09/2026, puis retouches D-61) n'est pas dans les connaissances du projet.
sim7.py n'en utilise que : les attributs de ModeleCharge, relache_cette_semaine() (regles AVANT)
et, pour controle_d61b, CoureurCharge/simule_charge. ModeleBloc (sim7) surcharge
_pas_de_progression() et ajuste() : le coeur G-PLA-002 vient donc de sim7, pas d'ici.
Valeurs reprises du sim3 d'origine (lu dans l'historique) : cap 0,20, pas absolu 0,5 h, cadence 3.
"""
import random


class ModeleCharge:
    def __init__(self, volume_depart, plafond_pic, cap_progression=0.20, pas_absolu_h=0.5,
                 cadence_relache=3):
        self.volume = volume_depart
        self.plafond = plafond_pic
        self.cap = cap_progression
        self.pas_absolu = pas_absolu_h
        self.cadence = cadence_relache
        self.semaines_depuis_relache = 0
        self.historique = []
        self.ressenti_base = None
        self.base_echantillons = []
        self.niveau_casse = None
        self.semaines_depuis_casse = 0
        self.cycles_sains = 0

    def relache_cette_semaine(self):
        return self.semaines_depuis_relache >= self.cadence


class CoureurCharge:
    def __init__(self, tolerance_h, volume_initial_h, graine=1):
        self.rng = random.Random(graine)
        self.tolerance = tolerance_h
        self.fatigue = 0.0

    def vit_la_semaine(self, v, relache):
        if relache:
            v *= 0.6
        exces = max(0.0, v - self.tolerance) / max(self.tolerance, 0.1)
        self.fatigue = max(0.0, self.fatigue - 0.35) if relache else min(1.5, max(0.0, self.fatigue + exces * 0.8 - 0.05))
        r = 1.0 + self.fatigue * 0.8 + self.rng.gauss(0, 0.05)
        s = min(3, int((self.fatigue - 0.5) * 6)) if self.fatigue > 0.5 else 0
        return v * (1 - 0.18 * s), r, s


def simule_charge(c, m, semaines=40):
    j = []
    for _ in range(semaines):
        rel = m.relache_cette_semaine()
        real, r, s = c.vit_la_semaine(m.volume, rel)
        m.ajuste(r, s, rel)
        j.append(dict(prescrit=m.volume, relache=rel))
    return j
