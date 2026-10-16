import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v38'").replace("/v28","/v38"))
import os;os.makedirs(OUT,exist_ok=True)
def S(pg):return pg.evaluate("({tab:(document.querySelector('#tabs .on')||{}).textContent,sousEcran:!!document.querySelector('.pfback'),fenetre:!!document.querySelector('#sheet>*'),histD:(history.state||{}).d||0})")
def back(pg,logs,tag):
    pg.go_back();pg.wait_for_timeout(350);logs.append(tag+' → '+json.dumps(S(pg)))
def f(pg,logs):
    logs.append('départ '+json.dumps(S(pg)))
    pg.locator('nav').get_by_text('Profil').click();pg.wait_for_timeout(200)
    pg.evaluate("app.psub('toi')");pg.wait_for_timeout(200);logs.append('Profil>Toi '+json.dumps(S(pg)))
    pg.locator('.pr').filter(has_text='Durée').nth(1).click();pg.wait_for_timeout(400);logs.append('roue ouverte '+json.dumps(S(pg)))
    back(pg,logs,'retour 1 (ferme la roue)')
    back(pg,logs,'retour 2 (sort de Toi)')
    back(pg,logs,'retour 3 (Profil → Aujourd\'hui)')
    # fermeture par l'interface : pas d'entrée fantôme
    pg.locator('nav').get_by_text('Semaine').click();pg.wait_for_timeout(200)
    pg.locator('nav').get_by_text('Suivi').click();pg.wait_for_timeout(200);logs.append('Semaine>Suivi '+json.dumps(S(pg)))
    pg.locator('nav').get_by_text('Aujourd').click();pg.wait_for_timeout(300);logs.append('onglet Aujourd\'hui '+json.dumps(S(pg)))
    pg.locator('nav').get_by_text('Profil').click();pg.wait_for_timeout(200);pg.evaluate("app.psub('toi')");pg.wait_for_timeout(200)
    pg.locator('.pr').filter(has_text='Durée').nth(1).click();pg.wait_for_timeout(300)
    pg.get_by_role('button',name='Annuler').first.click() if pg.get_by_role('button',name='Annuler').count() else pg.evaluate("app.wheelClose()")
    pg.wait_for_timeout(350);logs.append('roue fermée par le bouton '+json.dumps(S(pg)))
    back(pg,logs,'retour (sort de Toi, pas de retour fantôme)')
run('back',steps=f)
