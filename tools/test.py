#!/usr/bin/env python3
"""Lance toute la batterie de tests.
  python3 tools/test.py        moteur et outils (environ 1 min)
  python3 tools/test.py --ui   en plus, tous les tests d'interface tests/ui/test_v*.py (Playwright, environ 8 min)
Code de sortie 0 si tout est vert, 1 sinon. Pas de CI : la batterie se lance à la main avant chaque PR."""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / 'tests'
PY = sys.executable
ETAPES = [
    ("index.html à jour (moteur, version, syntaxe)", [PY, 'tools/build.py', '--check'], ROOT, None),
    ("Propriétés du plan sur les profils", ['node', 't_profils.js'], T, None),
    ("Déroulé = durée de chaque séance", ['node', 't_steps.js'], T, None),
    ("Réaction au ressenti (gel de la sortie longue, séances manquées)", ['node', 't_react3.js'], T, None),
    ("Décalage d'une séance dans la semaine", ['node', 't_decal.js'], T, None),
    ("Repère de reprise sans effet de seuil (D-94)", ['node', 't_reprise.js'], T, None),
    ("Arrondi supérieur de la séance qui bute sur +10 % (D-96)", ['node', 't_arrondi.js'], T, None),
    ("Bilan de séance, étage A (D-99)", ['node', 't_bilan.js'], T, None),
    ("D+ calé sur la course intermédiaire la plus proche (D-102)", ['node', 't_densite.js'], T, None),
    ("Fin de préparation : sorties clés, niveau tenu, affûtage (D-103)", ['node', 't_fin.js'], T, None),
    ("Week-end choc selon les avis d'experts (D-105)", ['node', 't_choc.js'], T, None),
    ("Indicateurs seconde par seconde et zones de Karvonen (D-100)", ['node', 't_flux.js'], T, None),
    ("Un saut ne relève la référence que de +10 % (D-107)", ['node', 't_plafond.js'], T, None),
    ("Numéro de semaine juste le lundi en heure d'été (P-07)", ['node', 'audit/t_audit_heure_ete.js'], T, None),
    ("Déplacer un renforcement dans sa semaine (v80)", ['node', 't_renfo_decal.js'], T, None),
    ("Sortie longue manquée : la semaine ne compte pas comme semaine de sortie longue (P-08)", ['node', 't_fantome.js'], T, None),
    ("Invariants sur 120 scénarios tirés au hasard (audit, fuseau UTC)", ['node', 't_invariants.js'], T, None),
]
if '--ui' in sys.argv:
    for f in sorted((T / 'ui').glob('test_v*.py'), key=lambda x: int(x.stem[6:]) if x.stem[6:].isdigit() else 0):
        ETAPES.append(("Interface : " + f.name, [PY, f.name], T / 'ui', None))   # certains tests lisent un voisin par chemin relatif
echecs = 0
for nom, cmd, cwd, verdict in ETAPES:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    sortie = (r.stdout + r.stderr).strip()
    ok = r.returncode == 0 and (verdict(sortie) if verdict else True)
    print(('✓ ' if ok else '✗ ') + nom)
    if not ok:
        echecs += 1
        print('\n'.join('    ' + l for l in sortie.splitlines()[-15:]))
print('\n' + ('Tout est vert.' if not echecs else '%d étape(s) en échec.' % echecs))
sys.exit(1 if echecs else 0)
