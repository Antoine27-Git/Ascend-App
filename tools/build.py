#!/usr/bin/env python3
"""Génère index.html à partir de deux sources :
  - tests/engine.js : le moteur de plan (source unique, testée) ;
  - sw.js           : le numéro de version (const C='ascend-vNN').

Usage :
  python3 tools/build.py            met index.html à jour
  python3 tools/build.py --check    échoue si index.html n'est pas à jour (utilisé par les tests et la CI)
  python3 tools/build.py --bump     passe de vNN à vNN+1 dans sw.js, puis met index.html à jour

On ne modifie JAMAIS le moteur directement dans index.html (entre les repères ENGINE:BEGIN et ENGINE:END) :
on modifie tests/engine.js, puis on relance ce script.
"""
import pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML, SW, ENG = ROOT / 'index.html', ROOT / 'sw.js', ROOT / 'tests' / 'engine.js'
BEGIN = "/* ENGINE:BEGIN — copie générée depuis tests/engine.js par tools/build.py. Ne pas modifier ici : modifier tests/engine.js puis relancer tools/build.py. */"
END = "/* ENGINE:END */"
IIFE_OPEN, IIFE_CLOSE = "const ENGINE=(function(){", "\n})();"


def engine_source():
    s = ENG.read_text(encoding='utf-8')
    i = s.index(IIFE_OPEN)
    j = s.index(IIFE_CLOSE, i) + len(IIFE_CLOSE)
    reste = s[j:].lstrip('\n')
    if not reste.startswith("if(typeof module!=='undefined')module.exports=ENGINE;"):
        sys.exit("tests/engine.js : la fin du moteur n'a pas la forme attendue (module.exports).")
    return s[:j]


def sw_version():
    m = re.search(r"const C='ascend-v(\d+)'", SW.read_text(encoding='utf-8'))
    if not m:
        sys.exit("sw.js : const C='ascend-vNN' introuvable.")
    return int(m.group(1))


def render(html):
    block = BEGIN + "\n" + engine_source() + "\n" + END
    if BEGIN in html and END in html:
        a = html.index(BEGIN)
        b = html.index(END) + len(END)
    else:  # première exécution : repère l'ancien bloc et le remplace
        k = html.index(IIFE_OPEN)
        a = html.rfind("/* ---------- moteur de plan", 0, k)
        b = html.index(IIFE_CLOSE, k) + len(IIFE_CLOSE)
        if a < 0:
            sys.exit("index.html : entête du moteur introuvable.")
    html = html[:a] + block + html[b:]
    v = sw_version()
    html, n = re.subn(r"const APP_VERSION='v\d+';[^\n]*",
                      "const APP_VERSION='v%d';   /* généré depuis sw.js par tools/build.py */" % v, html)
    if n != 1:
        sys.exit("index.html : const APP_VERSION introuvable (ou en double).")
    return html


def syntax_ok(html):
    node = shutil.which('node')
    if not node:
        print("  (node absent : vérification de syntaxe ignorée)")
        return True
    ok = True
    for k, s in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
        p = ROOT / ('.syntax_%d.js' % k)
        p.write_text(s, encoding='utf-8')
        r = subprocess.run([node, '--check', str(p)], capture_output=True, text=True)
        p.unlink()
        if r.returncode != 0:
            print("  erreur de syntaxe JavaScript (script %d) :\n%s" % (k, r.stderr[:600]))
            ok = False
    return ok


def main():
    args = sys.argv[1:]
    if '--bump' in args:
        sw = SW.read_text(encoding='utf-8')
        v = sw_version()
        SW.write_text(sw.replace("ascend-v%d" % v, "ascend-v%d" % (v + 1)), encoding='utf-8')
        print("Version : v%d → v%d" % (v, v + 1))
    cur = HTML.read_text(encoding='utf-8')
    new = render(cur)
    if '--check' in args:
        if cur != new:
            print("✗ index.html n'est pas à jour : lance « python3 tools/build.py » (moteur ou version modifiés).")
            sys.exit(1)
        if not syntax_ok(cur):
            sys.exit(2)
        print("✓ index.html à jour (moteur identique à tests/engine.js, version v%d, syntaxe JavaScript valide)" % sw_version())
        return
    if cur != new:
        HTML.write_text(new, encoding='utf-8')
        print("index.html mis à jour (moteur + version v%d)." % sw_version())
    else:
        print("index.html déjà à jour (version v%d)." % sw_version())
    if not syntax_ok(new):
        sys.exit(2)


main()
