# v59 : « Refaire l'analyse » indique « Analyse en cours… » et se désactive pendant le calcul (fonction simulée, réponse retenue)
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v59');os.makedirs(OUT,exist_ok=True)
SES=[{"id":"c1","date":"2026-11-10","type":"cf","dur":60,"rpe":6,"cfJ":"fort"},
     {"id":"x1","date":"2026-11-11","type":"long","dur":60,"dist":8.7,"dplus":164,"dminus":150,"hrAvg":158,"hrMax":174,"rpe":3,"src":"intervals","ext":"icu:i1",
      "note":"Marcilly-d'Azergues - 20261111_SL_D50","ia":{"txt":"Ancien texte d'analyse.","model":"claude-sonnet-5-5","at":"2026-11-11T18:00:00Z","retour":None,"com":None},"hrZ":{"t":[400,300,1200,1300,400,10,0],"b":[140,155,160,165,170,180,200]}}]
st=state(manques={},extra_sessions=SES);P=st['profile'];P['planStart']='2026-11-02';P['planFrom']='2026-11-02';P['decal']={'2026-11-11':'2026-11-15','2026-11-15':'2026-11-11'}
errs=[];ok=True;sent=[];held=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def ia(route):
    held.append(route)   # réponse retenue : on vérifie l'écran pendant l'attente
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
    btn=pg.locator('#sheet button',has_text='Analyse en cours')
    chk(btn.count()==1 and btn.first.is_disabled(),'pendant le calcul : bouton « Analyse en cours… » désactivé')
    pg.locator('#sheet h3',has_text='Analyse').scroll_into_view_if_needed();pg.screenshot(path=OUT+'/en_cours.png')
    chk(pg.get_by_text("Refaire l'analyse").count()==0,'pendant le calcul : plus de second bouton à presser')
    held[0].fulfill(status=200,content_type='application/json',body=json.dumps({"texte":"Nouveau texte.","model":"claude-sonnet-5-5"}));pg.wait_for_timeout(800)
    t=pg.locator('#sheet').inner_text()
    chk('Nouveau texte' in t and "Refaire l'analyse" in t and 'Analyse en cours' not in t,'après la réponse : nouveau texte et bouton de retour')
    chk(len(held)==1,'une seule demande envoyée')
    b.close()
print('errs',errs);ok=ok and not errs
sys.exit(0 if ok else 1)
