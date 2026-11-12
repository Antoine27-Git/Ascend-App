# v65 : analyse IA en deux blocs (« Ce que j'en lis », « Pour la prochaine ») ; le bilan envoyé contient le résumé du flux (terrain, dérive) ; ancienne analyse en texte libre toujours affichée
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v65');os.makedirs(OUT,exist_ok=True)
ROOT0=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT0)
import subprocess
FX=json.loads(subprocess.check_output(['node','-e',"const E=require('./engine.js');console.log(JSON.stringify(E.flux(require('./data/flux_20261111.json'),E.zonesKarvonen(205,52))))"],cwd=ROOT0))
SES=[{"id":"c1","date":"2026-11-10","type":"cf","dur":60,"rpe":6,"cfJ":"fort"},
     {"id":"x1","date":"2026-11-11","type":"long","dur":60,"dist":8.7,"dplus":164,"dminus":150,"hrAvg":158,"hrMax":174,"rpe":3,"src":"intervals","ext":"icu:i1","flux":FX,
      "note":"Marcilly-d'Azergues - 20261111_SL_D50","ia":{"txt":"Ancien texte d'analyse.","model":"claude-sonnet-5-5","at":"2026-11-11T18:00:00Z","retour":None,"com":None},"hrZ":{"t":[400,300,1200,1300,400,10,0],"b":[140,155,160,165,170,180,200]}}]
st=state(manques={},extra_sessions=SES);P=st['profile'];P['planStart']='2026-11-02';P['planFrom']='2026-11-02';P['decal']={'2026-11-11':'2026-11-15','2026-11-15':'2026-11-11'};P['fcMax']=205;P['fcRepos']=52
errs=[];ok=True;sent=[];held=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def ia(route):
    sent.append(json.loads(route.request.post_data));held.append(route)
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/functions/v1/analyze-session',ia)
    ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body='{"activities":[]}'))
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort());ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-11-11T15:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(5000)
    pg.locator('nav').get_by_text('Semaine').click();pg.wait_for_timeout(500);pg.locator('.wd:not(.rest)').filter(has_text='Sortie longue').first.click();pg.wait_for_timeout(700)
    chk('Ancien texte' in pg.locator('#sheet').inner_text(),'analyse existante affichée')
    pg.get_by_text("Refaire l'analyse").click();pg.wait_for_timeout(400)
    fl=(sent[0]['bilan'].get('flux') or {}) if sent else {}
    chk(bool(fl.get('terrain',{}).get('fpm')) and 'derive' in fl and fl.get('croisiere',{}).get('fc')==162,'bilan envoyé : terrain 5 catégories, dérive, FC stabilisée')
    chk(len(json.dumps(sent[0]))<8000 if sent else False,'bilan envoyé compact (%d o)'%(len(json.dumps(sent[0])) if sent else 0))
    held[0].fulfill(status=200,content_type='application/json',body=json.dumps({"interpretation":"Ta FC a grimpé dès le faux plat du début.","conseil":"Marche dans les premières montées.","texte":"","model":"claude-sonnet-5-5"}));pg.wait_for_timeout(800)
    t=pg.locator('#sheet').inner_text()
    chk("Ce que j'en lis" in t and 'Pour la prochaine' in t and 'faux plat du début' in t and 'Marche dans' in t,'deux blocs affichés')
    chk('Ancien texte' not in t,"l'ancienne analyse est remplacée")
    pg.locator('#sheet div',has_text='Pour la prochaine').last.scroll_into_view_if_needed();pg.screenshot(path=OUT+'/analyse.png')
    pg.get_by_text("Refaire l'analyse").click();pg.wait_for_timeout(400)
    held[1].fulfill(status=200,content_type='application/json',body=json.dumps({"interpretation":"","conseil":"","texte":"Réponse libre.","model":"claude-sonnet-5-5"}));pg.wait_for_timeout(800)
    chk('Réponse libre.' in pg.locator('#sheet').inner_text(),'repli : texte libre affiché si la réponse n\'est pas en deux champs')
    b.close()
print('errs',errs);ok=ok and not errs
sys.exit(0 if ok else 1)
