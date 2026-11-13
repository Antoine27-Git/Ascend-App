# v66-v67 (D-101) : Suivi — objectifs 80 km / 50 km, bouton 50 km / 80 km sur « Prêt pour le jour J ? », bloc « Ta progression » (données réelles du 11/11), lecture de l'historique
import json, os, sys, subprocess
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v67');os.makedirs(OUT,exist_ok=True)
T=os.path.join(ROOT,'tests')
FX=json.loads(subprocess.check_output(['node','-e',"const E=require('./engine.js');console.log(JSON.stringify(E.flux(require('./data/flux_20261111.json'),E.zonesKarvonen(205,52))))"],cwd=T))
RAW=json.load(open(os.path.join(T,'data','flux_20261111.json')))
SES=[{"id":"x1","date":"2026-11-11","type":"long","dur":60,"dist":8.7,"dplus":164,"hrAvg":158,"rpe":3,"src":"intervals","ext":"icu:i1","flux":FX},
     {"id":"x2","date":"2026-11-08","type":"ef","dur":60,"dist":8.5,"dplus":150,"hrAvg":158,"rpe":3,"src":"intervals","ext":"icu:i2"}]
st=state(manques={},extra_sessions=SES);P=st['profile']
P.update({'planStart':'2026-11-02','planFrom':'2026-11-02','fcMax':205,'fcRepos':52,'goalDist':80,'goalDplus':4000,'goalDate':'2027-09-25',
  'races':[{'name':'Trail 50','date':'2027-05-08','dist':50,'dplus':2000,'prio':'B'}]})
errs=[];ok=True;calls=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def streams(route):
    calls.append(json.loads(route.request.post_data));route.fulfill(status=200,content_type='application/json',body=json.dumps(RAW))
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/functions/v1/intervals-streams',streams)
    ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body='{"activities":[]}'))
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort());ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-11-12T20:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(4000)
    pg.locator('nav').get_by_text('Suivi').click();pg.wait_for_timeout(2500)
    pg.evaluate("app.svtog('duree')");pg.wait_for_timeout(400)
    t=pg.locator('main').inner_text()
    chk('Objectif' in t and '80 km' in t and 'Prochaine étape' in t and '50 km' in t and 'J−177' in t,'carte des deux objectifs (J−177)')
    chk('8 mai 2027 · J−177' in t and 'sortie longue visée : 4' in t and 'Plus longue' in t and 'Plus gros' in t,'Prêt pour le jour J : 50 km par défaut, graphique et cases')
    chk('55\u00a0% de ta course' in t,'part de la course sous la visée (50 km)')
    chk('Ton temps estimé' in t and 'Ordre de grandeur' in t,'temps estimé avec cases')
    pg.locator('.card',has_text='Ton temps estimé').scroll_into_view_if_needed();pg.screenshot(path=OUT+'/temps.png')
    chk('Ta progression' in t and 'Allure facile' in t and 'Résistance' in t and 'Montée' in t,'bloc Ta progression, 3 lignes')
    chk(len(calls)==1 and calls[0].get('id')=='i2','historique : la sortie sans données de la montre est relue (%d appel)'%len(calls))
    chk('6:34' in t and '/km à 159 bpm' in t,'allure facile 6:34 /km à 159 bpm (11/11)')
    chk('Il y a 6 sem.' in t and 'Maintenant' in t,'trois cases Départ → il y a 6 sem. → maintenant')
    ref=json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))['profile'].get('repRef')
    chk(ref=={'fc':159,'repos':52},'FC de référence figée : %s'%ref)
    pg.locator('.card',has_text='à effort égal').first.scroll_into_view_if_needed();pg.screenshot(path=OUT+'/progression.png')
    pg.locator('main .card').first.scroll_into_view_if_needed();pg.screenshot(path=OUT+'/objectifs.png')
    pg.locator('.card',has_text='Prêt pour le jour J').first.scroll_into_view_if_needed();pg.mouse.wheel(0,330);pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/pret50.png')
    pg.evaluate("app.svtog('pgallure')");pg.wait_for_timeout(300);pg.locator('.card',has_text='à effort égal').first.scroll_into_view_if_needed();pg.screenshot(path=OUT+'/progression_ouverte.png');pg.evaluate("app.svtog('pgallure')")
    pg.locator('button',has_text='80 km').first.click();pg.wait_for_timeout(500)
    t=pg.locator('main').inner_text()
    chk('sortie longue visée : 5\u00a0h à 6\u00a0h' in t and '25 sept. 2027' in t,'bouton 80 km : graphique et visée du 80 km')
    pg.locator('.card',has_text='Prêt pour le jour J').first.scroll_into_view_if_needed();pg.screenshot(path=OUT+'/pret80.png')
    b.close()
print('errs',errs);ok=ok and not errs
sys.exit(0 if ok else 1)
