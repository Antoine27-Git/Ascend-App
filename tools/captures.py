#!/usr/bin/env python3
"""Captures d'écran de l'appli à 360 px de large, pour vérifier une version avant de la publier.

Usage : python3 tools/captures.py [AAAA-MM-JJ] [HH:MM]
  Date et heure figées (défaut : aujourd'hui 07:30, heure de Paris).
  Écrit les PNG dans captures/ (dossier à ne pas versionner).

Le profil vient de tests/t_prof.json (onboarded, plan démarré). L'appli est ouverte en file://,
sans réseau (Supabase est bloqué) : on ne teste que l'interface. Toute erreur JavaScript fait
échouer le script. Prérequis : pip install playwright (Chromium déjà installé).
"""
import json, os, sys, datetime
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'captures')

def main():
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    hour = sys.argv[2] if len(sys.argv) > 2 else '07:30'
    when = '%sT%s:00+02:00' % (day, hour)
    prof = json.load(open(os.path.join(ROOT, 'tests', 't_prof.json'), encoding='utf-8'))
    prof.update({'name': 'Test', 'onboarded': True, 'introSeen': True})
    state = {'v': 2, 'profile': prof, 'daily': {}, 'sessions': [], 'plan': []}
    auth = {'access_token': 'x', 'refresh_token': 'y', 'expires_at': 9999999999999, 'email': 'test@local', 'user_id': 'u'}
    os.makedirs(OUT, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 360, 'height': 800}, device_scale_factor=2, is_mobile=True,
                            has_touch=True, timezone_id='Europe/Paris', locale='fr-FR')
        ctx.route('**/*supabase.co/**', lambda r: r.abort())
        ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'
                            % (json.dumps(json.dumps(state)), json.dumps(json.dumps(auth))))
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.clock.set_fixed_time(when)
        pg.goto('file://' + os.path.join(ROOT, 'index.html'))
        pg.wait_for_timeout(1500)  # écran de démarrage
        for view in ['home', 'jour', 'seances', 'suivi', 'profil']:
            pg.evaluate('app.go("%s")' % view); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(OUT, view + '.png'), full_page=True)
        # fiche et saisie de la première séance de course de la semaine
        pg.evaluate('app.go("seances")'); pg.wait_for_timeout(300)
        cards = pg.locator('.sc')
        if cards.count():
            cards.first.click(); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(OUT, 'fiche.png'))
            pg.evaluate('app.close()'); pg.wait_for_timeout(200)
        pg.evaluate('app.go("jour")'); pg.evaluate('app.newSession()'); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(OUT, 'saisie.png'))
        b.close()
    print('Captures écrites dans', OUT)
    if errors:
        print('Erreurs JavaScript :'); [print(' ', e) for e in errors]; sys.exit(1)

if __name__ == '__main__':
    main()
