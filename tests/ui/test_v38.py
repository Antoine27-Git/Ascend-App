import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v38'").replace("/v28","/v38"))
import os;os.makedirs(OUT,exist_ok=True)
def S(pg):return pg.evaluate("({tab:(document.querySelector('#tabs .on')||{}).textContent,sousEcran:!!document.querySelector('.pfback'),fenetre:!!document.querySelector('#sheet>*'),histD:(history.state||{}).d||0})")
def back(pg,logs,tag):
    pg.go_back();pg.wait_for_timeout(350);logs.append(tag+' → '+json.dumps(S(pg)))
def tab(pg,name):pg.locator('nav').get_by_text(name).click();pg.wait_for_timeout(250)
def f(pg,logs):
    logs.append('départ '+json.dumps(S(pg)))
    tab(pg,'Semaine');tab(pg,'Suivi');tab(pg,'Profil');pg.evaluate("app.psub('toi')");pg.wait_for_timeout(250)
    pg.locator('.pr').filter(has_text='Durée').nth(1).click();pg.wait_for_timeout(400);logs.append('Aujourd\'hui>Semaine>Suivi>Profil>Toi>roue '+json.dumps(S(pg)))
    for t in ['roue','Toi','Profil','Suivi','Semaine']:back(pg,logs,'retour (quitte: %s)'%t)
    # même onglet deux fois : pas d'entrée en double
    tab(pg,'Semaine');tab(pg,'Semaine');back(pg,logs,'Semaine x2 puis retour → Aujourd\'hui')
    # fenêtre fermée par un bouton : pas de retour fantôme
    tab(pg,'Profil');pg.evaluate("app.psub('toi')");pg.wait_for_timeout(250)
    pg.locator('.pr').filter(has_text='Durée').nth(1).click();pg.wait_for_timeout(300);pg.evaluate("app.wheelClose()");pg.wait_for_timeout(350)
    logs.append('roue fermée par le bouton '+json.dumps(S(pg)))
    back(pg,logs,'retour (quitte Toi)');back(pg,logs,'retour (quitte Profil)')
run('back',steps=f)
