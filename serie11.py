"""serie11.py — onzieme serie (TESTS.md, D-65), 23/09/2026. Rejoue les resultats cites.
python3 serie11.py [section]  — sections : sec, amorce, bruit, arrondi, fatigue, nr (defaut : toutes)"""
import sys
import sim8 as S

P = {p[0]: p for p in S.PROFILS}
A = P["proche d'Antoine"]


def ag(p, sc=None, n=150, **fl):
    old = {k: getattr(S, k) for k in fl}
    for k, v in fl.items():
        setattr(S, k, v)
    a, _ = S.agrege(p, "apres", n, scen=sc or {})
    for k, v in old.items():
        setattr(S, k, v)
    return a


def sec():
    print("\n[1] Objectif secondaire — 80 km, 52 sem (fond S1-40, bloc S41-49, T=S50)")
    for dur in (150, 210, 270, 390, 480):
        for sem in (12, 20, 28, 33, 36, 38, 40):
            sc = dict(tranche="8-20h", N=52, secondaire=(sem, float(dur), "objectif"))
            a = ag(A, sc, 100, SEC_REPRISE=False); b = ag(A, sc, 100, SEC_REPRISE=True)
            print(f"  S{sem:<3}{dur:4} min  cible sim7 {a['cible_ok']:.2f}  v1 {b['cible_ok']:.2f}")
    print("  Dans le bloc (cout de course compte, beta 0,5) :")
    for lab, sem, blocok in (("S33 en fond", 33, False), ("S42 traite", 42, True), ("S42 non traite", 42, False)):
        a = ag(A, dict(tranche="8-20h", N=52, secondaire=(sem, 390.0, "objectif")), 150,
               SEC_REPRISE=True, SEC_BLOC=blocok, FAT_REEL=dict(beta=0.5, course=True))
        print(f"  {lab:16} sympt bloc {a['sympt_bloc']:.2f}  fat>0,5 {a['surch']:.2f}")


def amorce():
    print("\n[2] Amorcage depuis zero (debutant trail)")
    for n in (2, 3, 4, 5):
        for am in (False, True):
            a = ag(P["debutant trail"], dict(zero=True, n=n), 200, AMORCE=am, ARRONDI="antoine_k2", SEC_REPRISE=True)
            print(f"  n={n} amorce={am!s:5} seances<30 min {a['courtes']:.2f} dep {a['dep']:.2f} fat>0,5 {a['surch']:.2f}")


def bruit():
    print("\n[3] Ressenti bruite — variantes ecartees")
    cas = [("bruit x3", P["lambda trail"], dict(bruit=0.15)), ("nominal", P["lambda trail"], {}),
           ("chute -30 % nominal", P["lambda trail"], dict(chute=0.70))]
    for nom, p, sc in cas:
        for lab, fl in (("sim7", {}), ("K=2", dict(SEUIL_ADAPT=2.0)), ("K=2,5", dict(SEUIL_ADAPT=2.5)),
                        ("repos K=2", dict(SEUIL_ADAPT=2.0, SEUIL_REPOS=True)), ("confirm.", dict(CONFIRME=True))):
            a = ag(p, sc, 200, **fl)
            print(f"  {nom:20}{lab:10} effondre {a['effondre']:.2f} fat>0,5 {a['surch']:.2f}")


def arrondi():
    print("\n[4] Arrondi")
    for mode in ("k2", "antoine_SL", "antoine_k2"):
        a = ag(A, {}, 200, ARRONDI=mode); b = ag(A, dict(tranche="8-20h", N=52), 200, ARRONDI=mode)
        print(f"  {mode:11} cible 3h30 {a['cible_ok']:.2f}  cible 5h (80 km) {b['cible_ok']:.2f}  dep {a['dep'] + b['dep']:.2f}")


def fatigue():
    print("\n[5] Cout propre sortie longue et D+ (verite simulee)")
    K = {"fond": 1.1, "bloc": 1.3}
    V = [("volume seul", None), ("SL beta 0,25", dict(beta=0.25)), ("SL beta 0,5", dict(beta=0.5)),
         ("D+ 1,1/1,3", dict(k=K)), ("D+ + choc", dict(k=K, choc=1.4)), ("D+ en rampe fond", dict(k=K, rampe_fond=8))]
    for nomc, sc in (("80 km 52 sem", dict(tranche="8-20h", N=52)), ("4-8h 33 sem", dict(N=33))):
        for nom, fr in V:
            a = ag(A, sc, 150, FAT_REEL=fr, SEC_REPRISE=True)
            print(f"  {nomc:13}{nom:18} cible {a['cible_ok']:.2f} sympt bloc {a['sympt_bloc']:.2f} fat>0,5 {a['surch']:.2f}")


def nr():
    print("\n[6] Non-regression v1 (22 scenarios + 7 profils x 200)")
    S.v1(True)
    tot = dict(dep=0, comp=0, inval=0, hors=0)
    for nom, p, sc in [(n, P[q], c) for n, q, c in S.SCENARIOS] + [(p[0], p, {}) for p in S.PROFILS]:
        _, R = S.agrege(p, "apres", 200, scen=sc)
        tot["dep"] += sum(r["dep"] for r in R); tot["comp"] += sum(r["compose7"] for r in R)
        tot["inval"] += sum(r["invalide"] for r in R)
        tot["hors"] += sum(1 for r in R if r["reduc_aff"] is not None and not 0.41 <= r["reduc_aff"] <= 0.60)
    S.v1(False)
    print("  ", tot)


if __name__ == "__main__":
    F = dict(sec=sec, amorce=amorce, bruit=bruit, arrondi=arrondi, fatigue=fatigue, nr=nr)
    for k in (sys.argv[1:] or F):
        F[k]()
