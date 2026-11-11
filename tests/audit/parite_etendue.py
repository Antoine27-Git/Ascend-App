#!/usr/bin/env python3
"""Audit mission 2 — parité v1 étendue : les 5 cas de tests/parity.py + des cas tirés au hasard (graine fixe).
Réutilise sim_run / js_run de tests/parity.py sans le modifier. Usage : python3 tests/audit/parite_etendue.py [n=60]"""
import sys, os, random, io, contextlib
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(T)
src = open('parity.py', encoding='utf8').read().split('cases = [')[0]
ns = {}
exec(compile(src, 'parity.py', 'exec'), ns)
sim_run, js_run = ns['sim_run'], ns['js_run']
random.seed(20261111)
n_cas = int(sys.argv[1]) if len(sys.argv) > 1 else 60
tot = 0; faits = 0; mauvais = []; erreurs = []
for i in range(n_cas):
    N = random.choice([36, 40, 44, 48, 52, 56, 60]); n = random.randint(1, 6); v = random.choice([0.0, 0.5, 1.0, 2.0, 3.5, 5.0, 7.0])
    sec = None
    if random.random() < 0.5:
        sec = (random.randint(12, N - 16), 390.0, random.choice(['objectif', 'entrainement']))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            a = sim_run(N, n, v, sec); b = js_run(N, n, v, sec)
    except SystemExit:
        erreurs.append((N, n, v, sec)); continue
    except Exception as e:
        erreurs.append((N, n, v, sec, str(e)[:60])); continue
    bad = [(x, y) for x, y in zip(a, b['res']) if x['type'] != y['type'] or abs(x['V'] - y['V']) > 1e-3 or x['sl'] != y['sl'] or x['aut'] != y['aut'] or x['cle'] != y['cle']]
    faits += 1; tot += len(bad)
    if bad: mauvais.append((N, n, v, sec, len(bad), bad[0]))
print(f"{faits} cas comparés, {len(erreurs)} en erreur, écarts : {tot} semaines dans {len(mauvais)} cas")
for m in mauvais[:8]: print("  N=%d n=%d vol0=%s sec=%s : %d semaines ; 1er écart sim %s | js %s" % m[:5] + (m[5][0], m[5][1]) if False else "  N=%d n=%d vol0=%s sec=%s : %d sem. en écart ; premier : sim %s / js %s" % (m[0], m[1], m[2], m[3], m[4], m[5][0], m[5][1]))
for e in erreurs[:5]: print("  erreur", e)
sys.exit(1 if tot or erreurs else 0)
