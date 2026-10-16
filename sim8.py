"""
sim8.py — 23/09/2026 : sim7.py + finalisation v1 (onzieme serie, TESTS.md, D-65). Drapeaux en tete
de la section « v1 ». Par defaut, TOUS les drapeaux v1 sont a False : sim8 == sim7.

sim6.py — Articulation G-PLA-002 / calendrier de blocs (D-63).

RECONSTRUCTION du 22/09/2026. Le sim6.py d'origine (nuit du 21 au 22/09/2026)
n'a jamais ete livre : il a ete perdu avec l'espace de travail. Ce fichier est
reecrit a partir du bilan de la nuit, de SPEC.md et de sim3.py. Les chiffres
qu'il produit font foi ; ceux du bilan ne servent que de point de comparaison
(sens et ordre de grandeur).

Deux jeux de regles, meme coureur, meme graine :
  AVANT : SPEC.md avant D-63 — sortie longue en part du volume (D-22) et
          +20 % max d'une sortie longue a la suivante (D-22b) ; relache 3:1
          comptee depuis le debut (D-57b) ; affutage traite en semaines de
          relache (seul mecanisme de baisse existant) ; aucune reprise apres
          coupure (D-46 disait « deja couvert »).
  APRES : D-63, voir SPEC.md.

Limite assumee : la fatigue du coureur ne depend que du volume hebdomadaire.
Le cout propre d'une sortie longue n'est pas modelise. Ce simulateur verifie
la mecanique, pas la physiologie.
"""

import math
import random
import statistics
from sim3 import ModeleCharge, CoureurCharge, simule_charge

PLANCHER = 30.0      # min : seance toujours autorisee, meme sans historique (extrapolation)
SEUIL = 1.10         # regle des 30 jours (S-BLE-004)
FENETRE = 30         # jours
EPS = 0.01           # min : tolerance de comparaison (bug flottant du bilan)
GRANDE = 180.0       # min : au-dela, alternance longue / tres longue (D-22a)
PART = {"fond": 0.325, "bloc": 0.375, "pic": 0.425, "affutage": 0.40}   # D-22
JOURS = {0: [], 1: [2], 2: [1, 3], 3: [1, 3, 4], 4: [0, 1, 3, 4],
         5: [0, 1, 2, 3, 4], 6: [0, 1, 2, 3, 4, 5]}
TRANCHES = {   # D-21, D-22, D-25 — duree d'effort attendue
    "4-8h":  dict(bloc=7, pic=3, affutage=2, n_cles=3, part_cle=0.60, aff=(0.65, 0.45),
                  cible=(210.0, 270.0), plafond_pic=10.0, course=360.0, recup=2),
    "8-20h": dict(bloc=9, pic=3, affutage=3, n_cles=3, part_cle=0.65, aff=(0.70, 0.55, 0.40),
                  cible=(300.0, 360.0), plafond_pic=11.0, course=720.0, recup=3),
}
AFF_2SEM = (0.65, 0.45)   # variante testee : 8-20h avec l'affutage de 2 semaines (jeu 8)


def tranche_de(duree):
    return "8-20h" if duree >= 480 else "4-8h" if duree >= 240 else "<4h"


def echeance(duree):
    """D-63d amende (jeu 9) : sortie longue a atteindre avant une course. Une course
    n'est pas une seance d'entrainement : on ne vise pas duree/1,1 au-dela des cibles
    de sa propre tranche (D-22), sinon un 50 km en objectif secondaire exigerait une
    sortie de 5h55 en fond."""
    plaf = 300.0 if duree >= 480 else 210.0 if duree >= 240 else 180.0
    return min(duree, plaf * SEUIL) / SEUIL

PROFILS = [
    # nom                       tol0  vol0  gain/sem tol_max seances tranche
    ("debutant trail",           3.5,  1.5,  0.015,   7.0,   3,  "4-8h"),
    ("coureur du dimanche",      3.0,  1.5,  0.005,   4.5,   2,  "4-8h"),
    ("lambda route",             5.0,  3.5,  0.010,   8.0,   4,  "4-8h"),
    ("proche d'Antoine",         6.0,  2.5,  0.006,   8.5,   4,  "4-8h"),
    ("lambda trail",             6.0,  3.5,  0.008,   9.0,   4,  "4-8h"),
    ("experimente trail",        8.5,  5.0,  0.004,  11.0,   5,  "4-8h"),
    ("tres experimente ultra",  11.0,  7.0,  0.002,  13.0,   6,  "8-20h"),
]


ARRONDI_PLAFOND_MINUTE = True    # jeu 9 : la seance de progression, bornee par le plafond, s'affiche a la minute


def arrondi5(minutes, plafond=None, fin=False):
    """Affichage aux 5 min les plus proches (1 min sous 50 min ; egalite : vers le bas), jamais
    au-dessus du plafond des 30 jours : dans ce cas, 5 min inferieures."""
    if minutes <= 0:
        return 0.0
    if ARRONDI.startswith("antoine") and minutes >= 50.0 - EPS and (fin or ARRONDI in ("antoine_tout", "antoine_k2")):
        r = regle_antoine(minutes)
        if plafond is not None and r > plafond + EPS:
            if ARRONDI == "antoine_k2" and fin:   # seance de progression bornee : a la minute (k2)
                r = math.floor(plafond + 1e-9)
            else:
                r = 5.0 * math.floor(plafond / 5.0 + 1e-9) if plafond >= 50.0 - EPS else math.floor(plafond + 1e-9)
        return max(r, 0.0)
    pas = 5.0 if minutes >= 50.0 - EPS else 1.0
    r = pas * math.floor(minutes / pas + 0.5 - 1e-9)
    if plafond is not None and r > plafond + EPS:
        pas = 5.0 if (plafond >= 50.0 - EPS and not (fin and ARRONDI_PLAFOND_MINUTE)) else 1.0
        r = pas * math.floor(plafond / pas + 1e-9)
    return max(r, 0.0)


def hm(minutes):
    return f"{int(minutes // 60)}h{int(round(minutes % 60)):02d}"


class Coureur:
    """Verite terrain. Meme dynamique de fatigue que CoureurCharge (sim3.py),
    plus une tolerance qui progresse avec l'entrainement et regresse a l'arret."""

    def __init__(self, tol0, gain, tol_max, graine, bruit=0.05, muet=False, taux_absence=0.0,
                 periode_absence=None):
        self.rng = random.Random(graine)
        self.tol0, self.tol, self.gain, self.tol_max = tol0, tol0, gain, tol_max
        self.bruit, self.muet, self.taux_absence = bruit, muet, taux_absence
        self.periode_absence, self._compte = periode_absence, 0
        self.fatigue = 0.0

    def vit(self, volume, recup, arret=False):
        if arret:
            self.fatigue = max(0.0, self.fatigue - 0.35)
            self.tol = max(0.6 * self.tol0, self.tol * 0.96)  # desentrainement, ordre de grandeur S-COU-005
            return None, 0
        exces = max(0.0, volume - self.tol) / max(self.tol, 0.1)
        if recup:
            self.fatigue = max(0.0, self.fatigue - 0.35)
        else:
            self.fatigue = min(1.5, max(0.0, self.fatigue + exces * 0.8 - 0.05))
        self.tol = min(self.tol_max, self.tol * (1 + self.gain * min(1.0, volume / max(self.tol, 0.1))))
        self._compte += 1
        sporadique = self.periode_absence and self._compte % self.periode_absence != 0
        if self.muet or sporadique or (self.taux_absence > 0 and self.rng.random() < self.taux_absence):
            # jeu 10 (D-64) : oubli occasionnel (taux_absence) ou coureur qui ne saisit jamais
            # (muet) — meme case vide au niveau du modele, seul le garde-fou d'alerte les distingue
            ressenti = None
        else:
            ressenti = 1.0 + self.fatigue * 0.8 + self.rng.gauss(0, self.bruit)
        sautees = min(3, int((self.fatigue - 0.5) * 6)) if self.fatigue > 0.5 else 0
        return ressenti, sautees


class ModeleBloc(ModeleCharge):
    """G-PLA-002 tel que sim3.py, sans la mecanique abandonnee de l'ex-G-PLA-001
    (cadence fixe 3:1, D-57b). Ajouts D-63 : consolidation (ne sonde plus sa
    limite : ni retest ni desserrage) et variante de gel au niveau d'entree."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.consolidation = False
        self.gel = None
        self.symptome = False
        self.relache_demandee = False
        self.repos = []
        self.base_init = None
        self.saisies = []
        self.derniere_alerte = None
        self.preuves = 0
        self.vals = []
        self.pendante = False

    def seuil(self):
        """v1 : seuil de derive rapporte au bruit personnel (D-49a : petit devant la dispersion
        observee). Bruit estime sur les differences successives des 12 dernieres saisies,
        robuste (MAD) : la fatigue varie lentement, le bruit de semaine en semaine."""
        if not SEUIL_ADAPT:
            return 0.12
        if SEUIL_REPOS:   # bruit estime sur l'etat repose seulement (semaines allegees)
            if len(self.repos) < 4:
                return 0.12
            v = self.repos[-8:]
            m = sorted(v)[len(v) // 2]
            sig = 1.4826 * sorted(abs(x - m) for x in v)[len(v) // 2]
            return max(0.12, SEUIL_ADAPT * sig / max(self.ressenti_base or 1.0, 0.1))
        if len(self.vals) < 6:
            return 0.12
        v = self.vals[-12:]
        d = sorted(abs(b - a) for a, b in zip(v, v[1:]))
        sig = 1.4826 * d[len(d) // 2] / math.sqrt(2)
        return max(0.12, SEUIL_ADAPT * sig / max(self.ressenti_base or 1.0, 0.1))

    def _pas_de_progression(self):
        if self.niveau_casse is None:
            return max(self.volume * (1 + self.cap), self.volume + self.pas_absolu)
        if self.cycles_sains >= 4 and not self.consolidation:
            self.niveau_casse *= 1.08
            self.cycles_sains = 0
        marge = (self.niveau_casse - self.volume) / max(self.niveau_casse, 0.1)
        if marge <= 0:
            return self.volume
        cap_f = (self.cap / 2) * min(1.0, marge * 2)
        pas_f = (self.pas_absolu / 2) * min(1.0, marge * 2)
        return max(self.volume * (1 + cap_f), self.volume + pas_f)

    def ajuste(self, ressenti, sautees, relache, execute=None):
        self.symptome = False
        manque = ressenti is None
        self.saisies.append(not manque)
        if manque:
            # jeu 9 : sans ressenti, aucune derive mesurable ; seules les seances sautees restent observables.
            # Si la moitie des 8 dernieres semaines est vide, G-PLA-002 ne sonde plus sa limite (A-05).
            if (REPLI_MUET and self.niveau_casse is None and len(self.saisies) >= 8
                    and sum(self.saisies[-8:]) <= 4):
                self.niveau_casse = self.volume
                self.muet = True
            ressenti = self.ressenti_base if self.ressenti_base is not None else 1.0
        else:
            self.base_echantillons.append(ressenti)
            self.vals.append(ressenti)
        if len(self.base_echantillons) < 4 and len(self.saisies) < 4:
            self.semaines_depuis_relache += 0 if relache else 1
            return
        if self.ressenti_base is None:
            if len(self.base_echantillons) >= 4:
                ech = sorted(self.base_echantillons[:4])
                self.ressenti_base = (ech[1] + ech[2]) / 2
            elif manque:
                self.ressenti_base = ressenti   # aucune saisie exploitable : derive nulle, seules les seances sautees comptent
            else:
                self.semaines_depuis_relache += 0 if relache else 1
                return
        derive = ressenti / self.ressenti_base - 1.0
        if relache:
            self.semaines_depuis_relache = 0
            self.relache_demandee = False
            if BASE_REPOS and not manque:   # jeu 9 : la reference se recale sur l'etat repose
                self.repos.append(ressenti)
                nb = statistics.median(sorted(self.base_echantillons[:4])[1:3] + self.repos[-6:])
                if self.base_init is None:
                    self.base_init = self.ressenti_base
                if BASE_PLAFOND is not None:   # ne peut pas monter au point de masquer un surmenage installe
                    nb = min(nb, self.base_init * (1 + BASE_PLAFOND))
                self.ressenti_base = nb
                # jeu 9 : une alerte due a la seule derive, qui ne se declencherait plus avec la
                # reference corrigee, n'a pas lieu de laisser un seuil
                if REEXAMEN and self.derniere_alerte is not None:
                    r_a, s_a, niv_avant, v_a = self.derniere_alerte
                    if s_a == 0 and r_a / nb - 1.0 <= self.seuil() and (REEXAMEN != "preuve" or self.preuves >= 2):
                        self.niveau_casse = niv_avant
                        self.derniere_alerte = None
            return
        self.semaines_depuis_relache += 1
        sl = self.seuil()
        alerte_r = derive > sl
        if CONFIRME and alerte_r and sautees == 0 and derive <= 2 * sl:
            alerte_r, self.pendante = self.pendante, True
        elif not alerte_r:
            self.pendante = False
        if sautees > 0 or alerte_r:
            self.pendante = False
            self.symptome = True
            self.derniere_alerte = (ressenti, sautees, self.niveau_casse, execute if execute else self.volume)
            self.preuves = 0
            if execute is not None and EXEC_CASSE:   # jeu 9 : le seuil est ce qui a ete couru
                self.volume = min(self.volume, execute)
            self.niveau_casse = (self.volume if self.niveau_casse is None
                                 else min(self.niveau_casse, self.volume))
            self.semaines_depuis_casse = 0
            self.volume *= 0.92
            self.semaines_depuis_relache = self.cadence   # relache avancee (D-57c)
            self.relache_demandee = True
            self.cycles_sains = 0
        elif derive < 0.05:
            if self.derniere_alerte is not None and execute is not None and execute >= 0.95 * self.derniere_alerte[3]:
                self.preuves += 1
            self.semaines_depuis_casse += 1
            if (self.niveau_casse is not None and self.semaines_depuis_casse >= 10
                    and not self.consolidation):
                self.niveau_casse *= 1.10
                self.semaines_depuis_casse = 0
            self.cycles_sains += 1
            nouveau = min(self.plafond, self._pas_de_progression())
            if self.gel is not None:
                nouveau = min(nouveau, max(self.volume, self.gel))
            self.volume = nouveau


class Calendrier:
    """D-21 : fond = duree - bloc specifique - affutage ; pic = 3 dernieres
    semaines du bloc specifique. T = premiere semaine d'affutage, N = semaine de course."""

    def __init__(self, N, tr, aff=None):
        self.N = N
        aff = aff or tr["affutage"]
        self.aff = aff
        self.bloc = min(tr["bloc"], max(0, N - aff - 2))
        self.fond = N - aff - self.bloc
        self.pic = min(tr["pic"], self.bloc)
        self.T = self.fond + self.bloc + 1
        self.cible_basse = tr["cible"][0]
        self._grille = {self.T - 4 * k for k in range(1, 40) if self.T - 4 * k >= 2}

    def phase(self, w):
        if w <= self.fond:
            return "fond"
        if w < self.T - self.pic:
            return "bloc"
        if w < self.T:
            return "pic"
        return "affutage"

    def grille(self):
        """D-63f : relaches recalees a rebours depuis l'affutage (T-4, T-8...)."""
        return self._grille


def relaches_prevues(cal, w, derniere, charges, forcees=frozenset()):
    """Relaches futures selon D-63f : grille T-4k, jamais moins de 2 semaines de
    charge entre deux relaches, au plus 4 (borne levee dans le pic). Les semaines
    forcees (affutage et recuperation d'un objectif secondaire) valent relache."""
    out = set()
    for x in range(w, cal.T):
        if x in forcees:
            derniere, charges = x, 0
            continue
        if (x in cal.grille() and x - derniere >= 3) or (charges >= 4 and cal.phase(x) != "pic"):
            out.add(x)
            derniere, charges = x, 0
        else:
            charges += 1
    return out


def atteint(mx, besoin, slots, cal, trou=None):
    """La chaine +10 % (arrondie) atteint-elle besoin sur ces semaines ?
    Alternance au-dela de 3 h pour les semaines de fond (D-22a).
    trou = (debut, fin, facteur) : affutage + recuperation d'un secondaire (v1) — la reference
    des 30 jours y est ramenee a facteur x niveau atteint."""
    v, dernier, passe = max(mx, PLANCHER), -9, False
    for x in slots:
        if trou and not passe and x > trou[1]:
            v, passe = max(PLANCHER, trou[2] * v), True
        if v >= besoin - EPS:
            return True
        nv = arrondi5(v * SEUIL, v * SEUIL, fin=True)
        if nv > GRANDE and cal.phase(x) == "fond" and x - dernier < 2:
            continue
        v = nv
        if nv > GRANDE:
            dernier = x
    return v >= besoin - EPS


def max30(hist, jour, reprise=None):
    """Plus longue seance des 30 jours precedents. reprise = (jour de reprise, valeur) :
    apres une interruption, jeu 9, la reference ne tombe pas a zero mais a une fraction
    de la plus longue seance d'avant la coupure, pendant 30 jours."""
    m = max((d for j, d, _ in hist if jour - FENETRE <= j < jour), default=0.0)
    if reprise is not None and reprise[0] <= jour < reprise[0] + FENETRE:
        m = max(m, reprise[1])
    return m


# ---- v1 (onzieme serie) -------------------------------------------------------------
ARRONDI = "k2"        # "k2" (D-63j + k2, sim7) | "antoine_SL" | "antoine_tout" | "antoine_k2" (retenu v1)
SEUIL_ADAPT = None    # None | K : seuil de derive = max(0,12 ; K x bruit personnel estime)
SEUIL_REPOS = False   # estimateur du bruit sur semaines allegees uniquement
CONFIRME = False      # alerte ressenti seule : 2 semaines consecutives (variante testee)
SEC_BLOC = False      # autorise affutage/recup d'un secondaire dans le bloc specifique
SEC_REPRISE = False   # reference des 30 jours apres affutage+recup d'un secondaire (D-63h/k5 etendu)
AMORCE = False        # amorcage depuis volume nul : min(3, n) x 30 min des la semaine 1
FAT_REEL = None       # None | dict(beta=..., k=...) : cout propre sortie longue et D+ (verite)


def v1(actif=True):
    """Active les regles retenues pour la v1 (D-65) : reprise apres secondaire, amorcage,
    arrondi hybride. SEUIL_ADAPT, SEUIL_REPOS, CONFIRME, SEC_BLOC et FAT_REEL restent des
    variantes de TEST (D-65c : ecartees ; SEC_BLOC : interdit ; FAT_REEL : verite simulee)."""
    global SEC_REPRISE, AMORCE, ARRONDI
    SEC_REPRISE, AMORCE, ARRONDI = actif, actif, ("antoine_k2" if actif else "k2")


def regle_antoine(minutes):
    """Arbitrage d'Antoine (23/09) : chiffre des minutes 1,2,3 -> 0 ; 4,5,6 -> 5 ; 7,8,9 -> 10."""
    mi = int(math.floor(minutes + 0.5 - 1e-9))
    d = mi % 10
    return float(mi - d + (0 if d <= 3 else 5 if d <= 6 else 10))


PROG = "une"      # jeu 9 : 'chaine' (glissant), 'semaine' (reference figee en debut de semaine), 'une'
EXEC_CASSE = True
GEL_EXEC = True
BASE_REPOS = True
BASE_PLAFOND = 0.05
REPLI_MUET = True
REEXAMEN = True
REPRISE_REF = True
ENTRETIEN = True
SEANCE_MIN = True
MARGE = 3   # jeu 9 (etait 1) ; semaine de marge sur la rampe (sinon la derniere sortie cle tombe pile sur le seuil)


def semaines_necessaires(depart, besoin):
    v, n, dernier = max(depart, PLANCHER), 0, -9
    while v < besoin - EPS and n < 200:
        n += 1
        nv = arrondi5(v * SEUIL, v * SEUIL, fin=True)
        if nv > GRANDE and n - dernier < 2:
            continue
        v = nv
        if nv > GRANDE:
            dernier = n
    return n


TR_COURT = dict(aff=(0.65, 0.45), recup=2)   # D-25 : 2-4 h, affutage 14 j, recuperation 10-14 j


def prepare(p, regles, graine, N=None, scen=None, conso="C", journal_detail=False):
    nom, tol0, vol0, gain, tol_max, n, tranche = p
    scen = scen or {}
    tr = TRANCHES[scen.get("tranche", tranche)]
    n = scen.get("n", n)
    rng = random.Random(graine * 7919 + 17)
    N = scen.get("N", N) or rng.randint(30, 36)
    if scen.get("zero"):
        vol0 = 0.0
    apres = regles == "apres"
    profil_aff = scen.get("aff_profil", tr["aff"]) if apres else (0.6, 0.6)
    cal = Calendrier(N, tr, len(profil_aff))
    c = Coureur(tol0, gain, tol_max, graine, bruit=scen.get("bruit", 0.05), muet=scen.get("muet", False),
                taux_absence=scen.get("taux_absence", 0.0), periode_absence=scen.get("periode_absence"))
    v_depart = vol0
    if AMORCE and vol0 * 60 < min(3, n) * PLANCHER - EPS:   # v1 : amorcage (GRONORUN : 3 seances)
        v_depart = min(3, n) * PLANCHER / 60
    m = ModeleBloc(volume_depart=v_depart, plafond_pic=tr["plafond_pic"])
    paire_active = apres and scen.get("paire", False) and tr is TRANCHES["8-20h"]

    hist = []
    if vol0 > 0:   # 4 semaines anterieures au volume de depart
        for w in range(-3, 1):
            lr = PART["fond"] * vol0 * 60
            aut = (vol0 * 60 - lr) / max(1, n - 1)
            for d in JOURS[n - 1]:
                hist.append(((w - 1) * 7 + d, aut, "anterieur"))
            hist.append(((w - 1) * 7 + 6, lr, "anterieur"))

    J = [dict(sem=0, phase="anterieur", type="histo", V=vol0, seances=list(hist), sympt=False,
              tol=c.tol, cle=False, lr=0.0, ref=None, reprises=[])]
    derniere_relache, charges = 0, 0
    cles_faites, derniere_cle, lr_prec = 0, -99, None
    arret_consec, ref, ref2 = 0, None, None
    vols_charge = []
    # course secondaire : (semaine, duree en min[, statut]) ; statut "entrainement" (defaut) ou "objectif" (D-25)
    secondaire = scen.get("secondaire")
    sec_aff, sec_rec, sec_prof = {}, set(), None
    if secondaire:
        statut = secondaire[2] if len(secondaire) > 2 else "entrainement"
        if statut == "objectif" and apres:
            t2 = TRANCHES.get(tranche_de(secondaire[1]), TR_COURT)
            sec_prof = t2["aff"]
            for k, f in enumerate(sec_prof):
                sec_aff[secondaire[0] - len(sec_prof) + 1 + k] = f
            sec_rec = {secondaire[0] + 1 + k for k in range(t2["recup"])}
    forcees = frozenset(set(sec_aff) | sec_rec)
    arret = scen.get("arret")
    if arret and isinstance(arret[0], str):
        quand, lg = arret
        deb = {"fond": max(6, cal.fond // 2 - lg // 2), "bloc": cal.fond + 2,
               "avant_aff": cal.T - lg}[quand]
        arret = (deb, lg)
    avance = scen.get("avance")
    paire_faite = False
    dernier_exec = None
    reprise, max_avant = None, 0.0

    w = 0
    while True:
        w += 1
        if avance and w == avance[0]:
            cal = Calendrier(cal.N - avance[1], tr, len(profil_aff))
        if w > cal.N:
            break
        ph = cal.phase(w)
        if scen.get("chute") and w == cal.fond + 1:
            c.tol *= scen["chute"]
        if scen.get("erosion") and w >= cal.fond - 6:
            c.tol *= 1 - scen["erosion"]
            c.fatigue = min(1.5, c.fatigue + 0.02)   # surmenage : la fatigue ne se dissipe plus completement
        if arret and arret[0] <= w < arret[0] + arret[1]:
            if arret_consec == 0:
                max_avant = max30(hist, (w - 1) * 7, reprise)
            c.vit(0.0, True, arret=True)
            arret_consec += 1
            J.append(dict(sem=w, phase=ph, type="arret", V=0.0, seances=[], sympt=False, tol=c.tol))
            continue
        if arret_consec:
            if apres:   # D-63h
                f = max(0.65, 1 - 0.07 * (arret_consec - 1))
                if REPRISE_REF:
                    reprise = ((w - 1) * 7, f * max_avant)
                    J[0]["reprises"].append(reprise)
                m.volume *= f
                if m.niveau_casse is not None and scen.get("seuil_reprise", True):
                    m.niveau_casse *= f
                elif m.niveau_casse is None and arret_consec >= 2 and scen.get("seuil_provisoire", 1.0):
                    m.niveau_casse = m.volume / f * scen.get("seuil_provisoire", 1.0)
            derniere_relache, charges = w - 1, 0
            m.semaines_depuis_relache = 0
            m.relache_demandee = False
            arret_consec = 0
        if SEC_REPRISE and forcees:
            deb_sec, fin_sec = min(forcees), max(forcees)
            if w == deb_sec:
                max_sec = max30(hist, (w - 1) * 7, reprise)
            if w == fin_sec + 1:
                n_red = fin_sec - deb_sec + 1
                f_sec = max(0.65, 1 - 0.07 * (n_red - 1))
                reprise = ((w - 1) * 7, f_sec * max_sec)
                J[0]["reprises"].append(reprise)
        # --- type de semaine et volume
        aff = ph == "affutage"
        s_aff = w in sec_aff and not aff and (ph == "fond" or SEC_BLOC)
        s_rec = w in sec_rec and not aff and (ph == "fond" or SEC_BLOC)
        if aff:
            k = w - cal.T
            if apres:   # D-63e : volume fixe, G-PLA-002 gele
                if ref is None:
                    ref = statistics.median(vols_charge[-3:]) if vols_charge else m.volume
                V = ref * profil_aff[min(k, len(profil_aff) - 1)]
            else:
                V = 0.6 * m.volume
            relache = not apres
        elif s_aff:   # affutage d'un objectif secondaire (D-25), meme regle que D-63e
            if ref2 is None:
                ref2 = statistics.median(vols_charge[-3:]) if vols_charge else m.volume
            V = ref2 * sec_aff[w]
            relache = True
        elif s_rec:   # recuperation apres objectif secondaire : relache, G-PLA-002 gele
            ref2 = None
            V = 0.6 * m.volume
            relache = True
        else:
            if apres:
                relache = m.relache_demandee or w in relaches_prevues(cal, w, derniere_relache, charges, forcees)
                m.consolidation = conso in ("B", "A", "C") and ph in ("bloc", "pic")
                if ph in ("bloc", "pic") and m.gel is None and (
                        conso == "A" or (conso == "C" and m.niveau_casse is None)):
                    # jeu 9 : gel au dernier volume reellement couru, pas a une cible jamais executee
                    m.gel = min(m.volume, dernier_exec) if (GEL_EXEC and dernier_exec) else m.volume
                    m.volume = m.gel
            else:
                relache = m.relache_cette_semaine()
            V = m.volume * (0.6 if relache else 1.0)
            if AMORCE and relache and apres:   # v1 : au plancher, une relache ne descend pas sous 2 x 30 min
                V = max(V, min(m.volume, 2 * PLANCHER / 60))
        gele = aff or s_aff or s_rec
        course_sem = w == cal.N and aff   # semaine de la course objectif

        cle = False
        if apres and not gele and not relache and ph in ("bloc", "pic"):
            cle = (tr["n_cles"] > cles_faites and w - derniere_cle >= 2 and w <= cal.T - 1)
        if not apres and not aff and not relache and ph in ("bloc", "pic"):
            cle = (tr["n_cles"] > cles_faites and w - derniere_cle >= 2)
        paire = paire_active and cle and cles_faites == 1 and not paire_faite
        if paire:   # jeu 9 : la paire n'a de sens que si le jour 1 tient au moins 3h30 sans progresser
            mx_p = max30(hist, (w - 1) * 7 + 5, reprise)
            if min(mx_p, 0.6 * tr["part_cle"] * V * 60) < 210.0 - EPS:
                paire = False
        course_ici = secondaire is not None and w == secondaire[0]
        statut_sec = (secondaire[2] if secondaire and len(secondaire) > 2 else "entrainement")

        def part(ph_):
            return max(PART[ph_], 1.0 / n)

        def cible_lr(mx):
            cap = max(PLANCHER, SEUIL * mx)
            if aff or s_aff:
                base = part("affutage") * V * 60
                return min(cap, base) if apres else (base if w == cal.T else 0.0)
            if not apres:
                base = part(ph) * V * 60
                if cle:
                    base = min(tr["cible"][1], tr["part_cle"] * V * 60)
                return base if lr_prec is None else min(base, 1.2 * lr_prec)
            if relache:
                return min(cap, part(ph) * V * 60)
            if paire:   # jour 1 : 60 % d'un total plafonne a la part des sorties cles, sans progresser
                return min(mx, 0.6 * tr["part_cle"] * V * 60)
            if cle:
                return min(cap, tr["cible"][1], tr["part_cle"] * V * 60)
            if ph == "fond" and doit_monter(mx):
                if lr_prec is not None and lr_prec > GRANDE and SEUIL * mx > GRANDE:
                    return min(cap, part(ph) * V * 60)
                return min(cap, tr["part_cle"] * V * 60)
            niv = a_entretenir(mx) if ENTRETIEN and ph == "fond" else None
            if niv and niv > part(ph) * V * 60:
                # jeu 9 : un niveau atteint trop tot sort de la fenetre des 30 jours ; on repete
                # le niveau NECESSAIRE (pas le max : une course n'est pas un niveau a entretenir),
                # une semaine sur deux au-dela de 3 h (D-22a)
                if not (lr_prec is not None and lr_prec > GRANDE and niv > GRANDE):
                    return min(niv, tr["part_cle"] * V * 60)
            return min(cap, part(ph) * V * 60)

        def a_entretenir(mx):
            jour = (w - 1) * 7 + 6
            age = jour - max((j for j, d, _ in hist if d >= mx - EPS and jour - FENETRE <= j < jour), default=jour)
            if age < 14:
                return None
            # niveau que les echeances a venir exigent (le plus haut deja atteignable depuis mx)
            besoins = []
            if tr["n_cles"] > cles_faites:
                besoins.append(tr["cible"][0] / SEUIL)
            if secondaire and secondaire[0] > w:
                besoins.append(echeance(secondaire[1]))
            ok = [b for b in besoins if b <= SEUIL * mx + EPS]
            return arrondi5(min(max(ok), mx)) if ok else None

        def doit_monter(mx):
            futur_rel = relaches_prevues(cal, w, derniere_relache, charges, forcees)
            charge = [x for x in range(w, cal.T) if x not in futur_rel and x not in forcees]
            cles_prev, dern = [], derniere_cle
            for x in charge:
                if cal.phase(x) in ("bloc", "pic") and len(cles_prev) < tr["n_cles"] - cles_faites and x - dern >= 2:
                    cles_prev.append(x)
                    dern = x
            # la paire (2e sortie cle) n'est pas une occasion de progresser
            pas_prog = set()
            if paire_active and not paire_faite:
                idx = 1 - cles_faites
                if 0 <= idx < len(cles_prev):
                    pas_prog.add(cles_prev[idx])
            ech = []
            if cles_prev:
                ech.append((cles_prev[-1], tr["cible"][0] / SEUIL))
            if secondaire and secondaire[0] >= w:
                lim = min([secondaire[0]] + list(sec_aff)) if sec_aff else secondaire[0]
                besoin = echeance(secondaire[1]) if apres else secondaire[1] / SEUIL
                ech.append((lim, besoin))
            for sem, besoin in ech:
                if mx >= besoin - EPS:
                    continue
                slots = [x for x in charge if x < sem and x not in pas_prog
                         and (cal.phase(x) == "fond" or x in cles_prev)]
                futurs = [x for x in slots if x > w]
                utiles = futurs[:max(0, len(futurs) - MARGE)]
                trou = None
                if SEC_REPRISE and forcees and w <= max(forcees):
                    d0, d1 = min(forcees), max(forcees)
                    trou = (d0, d1, max(0.65, 1 - 0.07 * (d1 - d0)))
                if not atteint(mx, besoin, utiles, cal, trou):
                    return True
            return False

        def construit(saut):
            seances, h = [], list(hist)
            jours = [d for d in JOURS[n - 1] if not (paire and d == 5)]
            if paire and 5 not in JOURS[n - 1] and jours:
                jours = jours[:-1] if len(jours) > 1 else jours
            lr0 = cible_lr(max30(h, (w - 1) * 7 + (5 if paire else 6), reprise))
            # v1 (amorcage) : a tres bas volume, la frequence passe avant la duree (S-BLE-003,
            # GRONORUN) : la sortie longue ne progresse que si les autres seances tiennent 30 min
            sl_max = (max(PLANCHER, V * 60 - len(jours) * PLANCHER)
                      if (AMORCE and apres and not gele and V * 60 <= 1.2 * (len(jours) + 1) * PLANCHER + EPS)
                      else None)   # regime d'amorcage seulement : volume a moins de 20 % du « tout au plancher »
            sl_force = None
            if sl_max is not None:
                lr0 = min(lr0, sl_max)
                if V * 60 < (len(jours) + 1) * PLANCHER - EPS:   # moins de n x 30 min : moins de seances
                    n_eff = max(1, int(V * 60 // PLANCHER + 1e-9))
                    jours = jours[:n_eff - 1]
                    cap_sl = max(PLANCHER, SEUIL * max30(hist, (w - 1) * 7 + 6, reprise))
                    sl_force = min(cap_sl, V * 60 - (n_eff - 1) * PLANCHER)
                    lr0 = sl_force
            j2_0 = min(lr0, 0.4 * tr["part_cle"] * V * 60) if paire else 0.0
            nb_aut = len(jours)
            if SEANCE_MIN and apres:   # jeu 9 : pas de seance « autre » sous 30 min ; D-35, les jours sont un plafond
                reste = V * 60 - (0 if (course_sem or (course_ici and s_aff)) else lr0 + j2_0)
                while nb_aut > 1 and reste / nb_aut < PLANCHER - EPS:
                    nb_aut -= 1
                jours = jours[:nb_aut]
            if course_sem or (course_ici and s_aff):
                aut = V * 60 / max(1, nb_aut)
            else:
                aut = max(0.0, V * 60 - lr0 - j2_0) / max(1, nb_aut)
            for i, d in enumerate(jours):
                if i < saut:
                    continue
                jour = (w - 1) * 7 + d
                # jeu 9 : une seule seance de progression par semaine, la sortie longue.
                # Les autres ne depassent pas le max des 30 jours (limite de S-BLE-004 :
                # +10 % enchaines dans la meme semaine restent excessifs).
                if apres and PROG == "une":
                    cap = max(PLANCHER, max30(h, jour, reprise))
                elif apres and PROG == "semaine":
                    cap = max(PLANCHER, SEUIL * max30(hist, (w - 1) * 7, reprise))
                else:
                    cap = max(PLANCHER, SEUIL * max30(h, jour, reprise))
                dur = arrondi5(min(aut, cap) if apres else aut, cap if apres else None)
                if dur > 0:
                    seances.append((jour, dur, "autre"))
                    h.append((jour, dur, "autre"))
            jour = (w - 1) * 7 + 6
            if course_ici:
                seances.append((jour, secondaire[1], "course_obj" if statut_sec == "objectif" else "course"))
            elif course_sem:
                seances.append((jour, tr["course"], "objectif"))
            elif paire:
                j1 = jour - 1
                mx = max30(h, j1, reprise)
                cap = max(PLANCHER, SEUIL * mx)
                d1 = arrondi5(cible_lr(mx), cap, fin=True)
                seances.append((j1, d1, "paire1"))
                h.append((j1, d1, "paire1"))
                cap2 = max(PLANCHER, SEUIL * max30(h, jour, reprise))
                d2 = arrondi5(min(d1, tr["part_cle"] * V * 60 - d1, cap2), min(d1, cap2))
                seances.append((jour, d2, "paire2"))
            else:
                # jeu 9 : sous k1, la sortie longue se reference a l'historique d'AVANT la semaine ;
                # sinon une seance « autre » hissee par le plancher de 30 min servait de marche
                # (18 -> 30 -> 33 min dans la meme semaine, trouve sur le debutant parti de zero)
                mx = max30(hist if (apres and PROG == "une") else h, jour, reprise)
                lr = cible_lr(mx)
                if sl_max is not None:
                    lr = min(lr, sl_max) if sl_force is None else sl_force
                cap = max(PLANCHER, SEUIL * mx)
                lr = arrondi5(lr, cap if apres else None, fin=True)
                if lr > 0:
                    seances.append((jour, lr, "cle" if cle else "longue"))
            return seances

        prev = construit(0)
        vol_prevu = sum(d for _, d, t in prev if not t.startswith("course") and t != "objectif") / 60
        v_vrai = vol_prevu
        if FAT_REEL:
            fr = FAT_REEL
            k = fr.get("k", {}).get(ph if ph != "pic" else "bloc", 1.0)
            if fr.get("rampe_fond") and ph == "fond" and w > cal.fond - fr["rampe_fond"]:
                k0, k1 = fr["k"]["fond"], fr["k"]["bloc"]
                k = k0 + (k1 - k0) * (w - (cal.fond - fr["rampe_fond"])) / fr["rampe_fond"]
            if fr.get("choc") and not fr.get("rampe_fond") and ph in ("bloc", "pic") and w <= cal.fond + 2:
                k *= fr["choc"]
            longues = [d for _, d, t in prev]
            v_vrai = vol_prevu * k + fr.get("beta", 0.0) * sum(max(0.0, d - 120.0) for d in longues) / 60
            if fr.get("course"):
                v_vrai += sum(d for _, d, t in prev if t.startswith("course")) / 60 * k
        ressenti, saut = c.vit(v_vrai, recup=(relache or gele) and not (FAT_REEL and FAT_REEL.get("course") and any(t.startswith("course") for _, _, t in prev)))
        seances = construit(min(saut, max(0, n - 1))) if saut else prev
        hist.extend(seances)
        hist = [s for s in hist if s[0] >= (w - 1) * 7 + 6 - FENETRE - 1]

        if not gele:
            m.ajuste(ressenti, saut, relache, execute=vol_prevu if apres else None)
            if apres and not relache and vol_prevu < V - 0.05:
                m.volume = min(m.volume, max(vol_prevu, 0.5) * (1 + m.cap))
        elif not apres:
            m.ajuste(ressenti, saut, True)
        else:   # gele : G-PLA-002 ne bouge pas, mais la semaine compte comme relache (D-57c)
            m.semaines_depuis_relache = 0
            m.relache_demandee = False
        if relache or gele:
            derniere_relache, charges = w, 0
        else:
            charges += 1
            vols_charge.append(V)
            dernier_exec = vol_prevu
        lr_obj = [d for _, d, t in seances if t in ("longue", "cle", "paire1")]
        if lr_obj:
            lr_prec = lr_obj[0]
        if cle and lr_obj:
            cles_faites += 1
            derniere_cle = w
            if paire:
                paire_faite = True
        typ = ("affutage" if aff else "aff_sec" if s_aff else "recup_sec" if s_rec
               else "relache" if relache else "charge")
        J.append(dict(sem=w, phase=ph, type=typ, V=V, Vexec=vol_prevu, seances=seances,
                      sympt=m.symptome and not gele, tol=c.tol, cle=cle, paire=paire,
                      fat=c.fatigue, saut=saut, ressenti=ressenti, base=m.ressenti_base,
                      lr=(lr_obj[0] if lr_obj else 0.0), ref=ref, repli=getattr(m, "muet", False)))
    return J, cal


# --- D-64 : garde-fou de saisie du ressenti (analyse hors modele) --------------------
# Le rattrapage a posteriori NE touche PAS ce qui precede (Coureur, ModeleBloc) : par
# decision (D-64), une saisie tardive ne nourrit jamais G-PLA-002. Cette fonction relit
# la sequence de ressenti deja produite et simule, en aval, ce que verrait le garde-fou
# de l'app : seuil d'alerte (streak consecutif), relance espacee, rattrapage qui eteint
# l'alerte sans changer l'entrainement prescrit.

def alerte_ressenti(J, seuil=3, espacement=3, proba_rattrapage=0.5, graine=0):
    rng = random.Random(graine * 104729 + 3)
    streak, semaines_alerte, relances, max_streak, temps_rattrapage = 0, 0, 0, 0, []
    en_alerte_depuis = None
    for s in J[1:]:
        if s["phase"] == "anterieur" or s["type"] == "arret":
            continue   # pas de seance : l'absence de ressenti n'est pas un oubli (D-63h)
        manque = s.get("ressenti") is None
        if manque:
            streak += 1
        else:
            streak = 0
        max_streak = max(max_streak, streak)
        if streak >= seuil:
            semaines_alerte += 1
            if en_alerte_depuis is None:
                en_alerte_depuis = s["sem"]
                relances += 1
            elif (streak - seuil) % espacement == 0:
                relances += 1
            if rng.random() < proba_rattrapage:   # le coureur repond a la relance : rattrapage
                temps_rattrapage.append(s["sem"] - en_alerte_depuis + 1)
                streak = 0
                en_alerte_depuis = None
        else:
            en_alerte_depuis = None
    return dict(semaines_alerte=semaines_alerte, relances=relances, max_streak=max_streak,
                jamais_alerte=int(semaines_alerte == 0),
                temps_rattrapage=(statistics.mean(temps_rattrapage) if temps_rattrapage else None))


def depassements(J, avec_courses=False, brut=False):
    """Seances > +10 % du max des 30 jours precedents (plancher 30 min). Hors brut, la
    reference de reprise (jeu 9) compte comme seance du passe."""
    rep_ = [] if brut else J[0].get("reprises", [])
    tout = []
    for s in J:
        tout.extend(s["seances"])
    tout.sort()
    n = 0
    for i, (jour, dur, t) in enumerate(tout):
        if t in ("anterieur", "objectif", "course_obj") or (t == "course") != avec_courses:
            continue
        mx = max((d for j, d, _ in tout[:i] if jour - FENETRE <= j < jour), default=0.0)
        for j0, v0 in rep_:
            if j0 <= jour < j0 + FENETRE:
                mx = max(mx, v0)
        if dur > max(PLANCHER, SEUIL * mx) + EPS:
            n += 1
    return n


def mesures(J, cal):
    fond = [s for s in J if s["phase"] == "fond" and s["type"] == "charge"]
    bloc = [s for s in J if s["phase"] in ("bloc", "pic") and s["type"] == "charge"]
    pic = [s for s in J if s["phase"] == "pic"]
    aff = [s for s in J if s["phase"] == "affutage"]
    charge = [s for s in J if s["type"] == "charge" and s["sem"] < cal.T]
    r = {}
    r["dep"] = depassements(J)
    r["dep_course"] = depassements(J, avec_courses=True)
    r["dep_brut"] = depassements(J, brut=True)
    ent = lambda t: not t.startswith("course") and t != "objectif"
    longues_bloc = [d for s in J if s["phase"] in ("bloc", "pic") for _, d, t in s["seances"] if ent(t)]
    longues_fond = [d for s in J if s["phase"] == "fond" for _, d, t in s["seances"] if ent(t)]
    r["cles200"] = sum(1 for d in longues_bloc if d >= 200 - EPS)
    r["cles210"] = sum(1 for d in longues_bloc if d >= 210 - EPS)
    r["cible_ok"] = bool(longues_bloc) and max(longues_bloc) >= cal.cible_basse - EPS
    r["rel_pic"] = any(s["type"] == "relache" for s in pic)
    r["sympt_bloc"] = sum(1 for s in J if s["phase"] in ("bloc", "pic") and s["sympt"])
    r["sympt_tot"] = sum(1 for s in J if s["sympt"])
    pv = [s["Vexec"] for s in pic if s["type"] == "charge"]
    r["effondre"] = bool(pv) and statistics.mean(pv) < 0.6 * statistics.mean(s["tol"] for s in pic if s["type"] == "charge")
    r["atteinte"] = (statistics.mean(pv) / statistics.mean(s["tol"] for s in pic if s["type"] == "charge")) if pv else None
    ref = statistics.median([s["V"] for s in charge][-3:]) if charge else None
    r["reduc_aff"] = (1 - statistics.mean(s["V"] for s in aff) / ref) if (aff and ref) else None
    r["bloc_sous_fond"] = (statistics.mean(s["Vexec"] for s in bloc) < statistics.mean(s["Vexec"] for s in fond[-4:]) - 0.05) if (bloc and fond) else None
    r["longue_bloc_sous_fond"] = (max(longues_bloc) < max(longues_fond) - EPS) if (longues_bloc and longues_fond) else None
    r["max_longue"] = max(longues_bloc + longues_fond) if (longues_bloc or longues_fond) else 0.0
    # Frandsen 2025 (limite des auteurs) : deux « records » (seance > max des 30 jours) a moins de 7 jours
    tout = sorted(x for s in J for x in s["seances"])
    records = []
    for i, (jour, dur, t) in enumerate(tout):
        if t == "anterieur" or not ent(t):
            continue
        mx = max((d for j, d, _ in tout[:i] if jour - FENETRE <= j < jour), default=0.0)
        if dur > mx + EPS and dur > PLANCHER + EPS:
            records.append(jour)
    r["records"] = len(records)
    r["prog7"] = sum(1 for a, b in zip(records, records[1:]) if b - a < 7)
    # hausse composee : seance > +10 % du max des 30 jours qui s'arretent 7 jours avant
    comp = 0
    for i, (jour, dur, t) in enumerate(tout):
        if t == "anterieur" or not ent(t):
            continue
        mx = max((d for j, d, _ in tout[:i] if jour - 37 <= j <= jour - 7), default=0.0)
        for j0, v0 in J[0].get("reprises", []):   # la reference de reprise (k5) vaut seance du passe
            if j0 <= jour < j0 + FENETRE:
                mx = max(mx, v0)
        if dur > max(PLANCHER, SEUIL * mx) + EPS:
            comp += 1
    r["compose7"] = comp
    # derniere sortie longue avant la course objectif (jours) et ratio course / plus longue des 30 jours
    obj = [(j, d) for j, d, t in tout if t == "objectif"]
    if obj:
        jo, do = obj[0]
        lr = [(j, d) for j, d, t in tout if ent(t) and t != "anterieur" and j < jo and d >= 0.6 * max(longues_bloc or [1])]
        r["jours_derniere_longue"] = (jo - max(j for j, _ in lr)) if lr else None
        r["plus_longue_60j"] = max((d for j, d, t in tout if ent(t) and jo - 60 <= j < jo), default=0.0)
    else:
        r["jours_derniere_longue"] = None
        r["plus_longue_60j"] = None
    paires = [s for s in J if s.get("paire")]
    r["paire"] = len(paires)
    r["paire_j1"] = max((d for s in paires for _, d, t in s["seances"] if t == "paire1"), default=None) if paires else None
    r["paire_j2"] = max((d for s in paires for _, d, t in s["seances"] if t == "paire2"), default=None) if paires else None
    # jeu 9 : indicateurs de dommage (ce que subit le coureur, pas ce que le modele detecte)
    r["courtes"] = sum(1 for s in J[1:] for _, d, t in s["seances"] if t == "autre" and 0 < d < PLANCHER - EPS)
    r["surch"] = sum(1 for s in J[1:] if s.get("fat", 0) > 0.5)
    r["fat03"] = sum(1 for s in J[1:] if s.get("fat", 0) > 0.3)
    vals = [x["V"] for x in J]
    r["invalide"] = any((v < 0 or math.isnan(v) or math.isinf(v)) for v in vals)
    return r


def agrege(p, regles, tirages, scen=None, conso="C", base=0):
    R = []
    for i in range(tirages):
        J, cal = prepare(p, regles, base + i, scen=scen, conso=conso)
        R.append(mesures(J, cal))
    def moy(k):
        v = [r[k] for r in R if r[k] is not None]
        return statistics.mean(float(x) for x in v) if v else float("nan")
    return {k: moy(k) for k in R[0]}, R


SCENARIOS = [
    ("interruption 5 sem en fond",     "proche d'Antoine", dict(arret=("fond", 5))),
    ("interruption 3 sem en bloc",     "proche d'Antoine", dict(arret=("bloc", 3))),
    ("interruption 2 sem avant aff.",  "proche d'Antoine", dict(arret=("avant_aff", 2))),
    ("debutant partant de zero",       "debutant trail",   dict(zero=True)),
    ("preparation de 8 semaines",      "lambda trail",     dict(N=8)),
    ("preparation de 4 semaines",      "lambda trail",     dict(N=4)),
    ("preparation de 52 semaines",     "lambda trail",     dict(N=52)),
    ("secondaire 2h30 en S20",         "proche d'Antoine", dict(N=33, secondaire=(20, 150.0))),
    ("secondaire 3h30 en S16 (infais.)","proche d'Antoine", dict(N=33, secondaire=(16, 210.0))),
    ("tolerance -30 % en entree bloc", "lambda trail",     dict(chute=0.70)),
    ("coureur hyper-reactif",          "lambda trail",     dict(bruit=0.15)),
    ("coureur muet (aucun ressenti)",  "lambda trail",     dict(muet=True)),
    ("2 seances par semaine",          "lambda trail",     dict(n=2)),
    ("tres gros volume, cible 8-20h",  "tres experimente ultra", dict(n=7)),
    ("course avancee de 3 sem (S12)",  "proche d'Antoine", dict(N=33, avance=(12, 3))),
    # ajouts jeu 9
    ("erosion lente 1,5 %/sem",        "proche d'Antoine", dict(erosion=0.015)),
    ("80 km, 52 sem (8-20h)",          "proche d'Antoine", dict(tranche="8-20h", N=52)),
    ("80 km, 36 sem (duree minimale)", "proche d'Antoine", dict(tranche="8-20h", N=36)),
    ("80 km + 50 km objectif S33",     "proche d'Antoine", dict(tranche="8-20h", N=52, secondaire=(33, 390.0, "objectif"))),
    ("80 km + 50 km entrainement S33", "proche d'Antoine", dict(tranche="8-20h", N=52, secondaire=(33, 390.0))),
    ("ultra, paire activee",           "tres experimente ultra", dict(paire=True)),
    ("interruption 8 sem en fond",     "lambda trail",     dict(arret=("fond", 8))),
]


def controle_d61b(graines=200):
    """Re-verification du chiffre de D-61b (ecart 7,6 % sur n=8) sur 1 600 tirages."""
    from sim5 import PROFILS as P5
    ecarts = []
    for g in range(graines):
        for i, p in enumerate(P5):
            tol = p[6]
            cc = CoureurCharge(tolerance_h=tol, volume_initial_h=max(0.5, tol * 0.4), graine=100 + i + 1000 * g)
            mc = ModeleCharge(volume_depart=max(0.5, tol * 0.4), plafond_pic=tol * 1.6)
            j = simule_charge(cc, mc, semaines=40)
            final = sum(x["prescrit"] for x in j[-6:]) / 6
            ecarts.append(abs(final - tol) / tol * 100)
    return statistics.mean(ecarts), statistics.median(ecarts), len(ecarts)


def affiche_exemple(p, graine, N=33):
    for regles in ("avant", "apres"):
        J, cal = prepare(p, regles, graine, N=N)
        print(f"\n  {regles.upper()} — {p[0]}, {N} semaines (bloc S{cal.fond + 1}-S{cal.T - 1},"
              f" pic S{cal.T - cal.pic}-S{cal.T - 1}, affutage S{cal.T}-S{cal.N})")
        lignes = []
        for s in J:
            if s["sem"] < cal.fond - 6:
                continue
            lr = s["lr"]
            tag = {"relache": "allegee", "affutage": "affutage", "arret": "arret"}.get(s["type"], "")
            if s["cle"]:
                tag = "CLE"
            if s["sympt"]:
                tag += " symptome"
            lignes.append(f"S{s['sem']:<3}{s['phase']:<9}{s['V']:5.1f} h  longue {hm(lr):>6}  {tag}")
        print("   " + "\n   ".join(lignes))
        r = mesures(J, cal)
        print(f"   depassements {r['dep']}, sorties >= 3h20 : {r['cles200']}, reduction affutage "
              f"{r['reduc_aff'] * 100:.0f} %")


if __name__ == "__main__":
    TIRAGES = 500
    print("=" * 100)
    print("SIMULATEUR ASCEND — jeu 8 (reconstruit) : G-PLA-002 et calendrier de blocs, D-63")
    print("=" * 100)

    print("\nT-B1  Exemple concret, 33 semaines")
    affiche_exemple(PROFILS[3], graine=3)

    print(f"\nT-B2  Sept profils x {TIRAGES} tirages, duree de preparation tiree entre 30 et 36 semaines")
    entetes = ["dep", "cles200", "rel_pic", "sympt_bloc", "atteinte", "reduc_aff", "bloc_sous_fond", "longue_bloc_sous_fond"]
    print(f"  {'profil':24}{'':7}" + "".join(f"{h[:12]:>13}" for h in entetes))
    for p in PROFILS:
        for regles in ("avant", "apres"):
            a, _ = agrege(p, regles, TIRAGES)
            print(f"  {p[0]:24}{regles:7}" + "".join(f"{a[h]:13.2f}" for h in entetes))

    print("\nT-B3  Consolidation : quatre variantes (APRES), 500 tirages — symptomes en bloc / atteinte du pic")
    print("      aucune ; B = ni retest ni desserrage ; C = B + gel au volume d'entree si aucun seuil connu ; A = gel toujours")
    cas_b3 = [(p[0], p, {}) for p in PROFILS] + [
        ("5 sem fond (Antoine)", PROFILS[3], dict(arret=("fond", 5))),
        ("debutant de zero", PROFILS[0], dict(zero=True)),
        ("prepa 16 sem (lambda)", PROFILS[4], dict(N=16))]
    for nom, p, sc in cas_b3:
        ligne = f"  {nom:24}"
        for v in ("aucune", "B", "C", "A"):
            a, _ = agrege(p, "apres", TIRAGES, scen=sc, conso=v)
            ligne += f" | {v:6} {a['sympt_bloc']:.2f} {a['atteinte']:.3f}"
        print(ligne)

    print(f"\nT-B4  {len(SCENARIOS)} scenarios defavorables, 200 tirages, AVANT -> APRES")
    for nom, prof, sc in SCENARIOS:
        p = next(x for x in PROFILS if x[0] == prof)
        try:
            a, Ra = agrege(p, "avant", 200, scen=sc)
            b, Rb = agrege(p, "apres", 200, scen=sc)
            inval = sum(r["invalide"] for r in Ra + Rb)
            hors = sum(1 for r in Rb if r["reduc_aff"] is not None and not (0.41 <= r["reduc_aff"] <= 0.60))
            print(f"  {nom:32} dep {a['dep']:5.2f} -> {b['dep']:4.2f} | >=3h20 {a['cles200']:4.2f} -> "
                  f"{b['cles200']:4.2f} | sympt bloc {a['sympt_bloc']:4.2f} -> {b['sympt_bloc']:4.2f} "
                  f"(total {a['sympt_tot']:4.2f} -> {b['sympt_tot']:4.2f}) | "
                  f"aff {a['reduc_aff'] * 100:4.0f} % -> {b['reduc_aff'] * 100:4.0f} % (hors 41-60 : {hors}) | "
                  f"course >+10 % {a['dep_course']:4.2f} -> {b['dep_course']:4.2f} | invalides {inval}")
        except Exception as e:   # A-06 : on veut le voir, pas le masquer
            print(f"  {nom:32} ERREUR {type(e).__name__}: {e}")

    print("\nT-B6  Cout de l'arrondi : pas de +10 % pour passer de 50 min a 110 min")
    for nom, pas in (("sans arrondi", 0), ("1 min partout", 1), ("5 min des 50 min (retenu)", 5)):
        v, k = 50.0, 0
        while v < 110 - EPS:
            v = v * SEUIL if pas == 0 else (arrondi5(v * SEUIL, v * SEUIL) if pas == 5 else math.floor(v * SEUIL + 1e-9))
            k += 1
        print(f"  {nom:28} {k} pas")

    print("\nT-B5  Re-verification de D-61b (ecart moyen du volume a la tolerance)")
    moy, med, nb = controle_d61b()
    print(f"  {nb} tirages : moyenne {moy:.1f} %, mediane {med:.1f} % (D-61b annoncait 7,6 % sur 8 tirages)")
