#!/usr/bin/env python3
"""Lance toute la batterie de tests. Usage : python3 tools/test.py
Code de sortie 0 si tout est vert, 1 sinon (utilisé par la CI GitHub Actions)."""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / 'tests'
PY = sys.executable
ETAPES = [
    ("index.html à jour (moteur, version, syntaxe)", [PY, 'tools/build.py', '--check'], ROOT, None),
    ("Parité avec sim8.py, règles v1 (0 écart)", [PY, 'parity.py'], T, lambda s: 'TOTAL ECARTS 0' in s),
    ("Propriétés du plan sur les profils", ['node', 't_profils.js'], T, None),
    ("Déroulé = durée de chaque séance", ['node', 't_steps.js'], T, None),
    ("Réaction au ressenti (gel de la sortie longue, séances manquées)", ['node', 't_react3.js'], T, None),
    ("Décalage d'une séance dans la semaine", ['node', 't_decal.js'], T, None),
]
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
