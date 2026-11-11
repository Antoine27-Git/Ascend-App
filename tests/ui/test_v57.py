# D-99 : bilan de séance (étage A) et bouton « Analyser la séance » (étage B, fonction simulée)
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v57');os.makedirs(OUT,exist_ok=True)
SES=[{"id":"c1","date":"2026-11-10","type":"cf","dur":60,"rpe":6,"cfJ":"fort"},
     {"id":"x1","date":"2026-11-11","type":"long","dur":60,"dist":8.7,"dplus":164,"dminus":150,"hrAvg":158,"hrMax":174,"rpe":3,"src":"intervals","ext":"icu:i1",
      "note":"Marcilly-d'Azergues - 20261111_SL_D50","hrZ":{"t":[400,300,1200,1300,400,10,0],"b":[140,155,160,165,170,180,200]}}]
st=state(manques={},extra_sessions=SES);P=st['profile'];P['planStart']='2026-11-02';P['planFrom']='2026-11-02';P['decal']={'2026-11-11':'2026-11-15','2026-11-15':'2026-11-11'}
errs=[];ok=True;sent=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def ia(route):
    sent.append(route.request.post_data or '');route.fulfill(status=200,content_type='application/json',body=json.dumps({"texte":"Sortie d'une heure, 164 m de D+.\n\nTon cœur a travaillé plus que ton ressenti.\n\nLa prochaine fois, marche dans les côtes.","model":"claude-sonnet-5-5"}))
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/functions/v1/analyze-session',ia)
    ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body='{"activities":[]}'))
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort());ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:print('CONSOLE',m.type,m.text[:300]) if m.type=='error' else None)
    pg.clock.set_fixed_time('2026-11-11T15:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(5000)
    pg.locator('nav').get_by_text('Semaine').click();pg.wait_for_timeout(500);pg.locator('.wd:not(.rest)').filter(has_text='Sortie longue').first.click();pg.wait_for_timeout(700);print(pg.locator('#sheet').inner_text()[-900:].replace('\n',' | '))
    txt=pg.locator('#sheet').inner_text()
    chk('Temps au-dessus de ta zone de base' in txt and '81 %' in txt,'étage A : temps au-dessus de la zone de base')
    chk('CrossFit la veille' in txt,'étage A : CrossFit la veille')
    chk('Prochaine sortie longue' in txt,'étage A : effet sur le plan')
    pg.screenshot(path=OUT+'/bilan.png',full_page=True)
    pg.locator('#sheet input[placeholder^="Ex. :"]').fill('sortie facile');pg.locator('#sheet input[placeholder^="Ex. :"]').blur()
    pg.get_by_text('Analyser la séance').click();pg.wait_for_timeout(900)
    txt=pg.locator('#sheet').inner_text()
    chk('marche dans les côtes' in txt,'étage B : texte affiché')
    chk(sent and 'Marcilly' not in sent[0] and 'sortie facile' in sent[0],'envoyé sans nom de lieu, avec la lecture d\'Antoine')
    pg.get_by_text('Pas vraiment').click();pg.wait_for_timeout(400)
    chk(pg.locator('#sheet input[placeholder^="Qu\'est-ce"]').count()==1,'« Pas vraiment » ouvre le champ de commentaire')
    pg.locator('#sheet h3',has_text='Bilan').scroll_into_view_if_needed();pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/analyse.png')
    s=json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
    x=[z for z in s['sessions'] if z['id']=='x1'][0]
    chk(x.get('ia',{}).get('retour')=='non' and x['ia'].get('txt'),'analyse et retour enregistrés avec la séance')
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs))
sys.exit(0 if ok else 1)
