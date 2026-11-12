# v60 (D-100) : données seconde par seconde (fonction simulée avec la trace réelle du 11/11, sans position), zones de Karvonen, blocs du bilan
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v60');os.makedirs(OUT,exist_ok=True)
FLUX=json.load(open(os.path.join(ROOT,'tests','data','flux_20261111.json')));del FLUX['_']
SES=[{"id":"c1","date":"2026-11-10","type":"cf","dur":60,"rpe":6,"cfJ":"un peu"},
     {"id":"x1","date":"2026-11-11","type":"long","dur":60,"dist":8.7,"dplus":164,"dminus":130,"hrAvg":158,"hrMax":174,"rpe":3,"src":"intervals","ext":"icu:i1",
      "note":"Marcilly-d'Azergues - 20261111_SL_D50","nomMontre":"Marcilly-d'Azergues - 20261111_SL_D50","hrZ":{"t":[1110,1969,524,0,0,0,0],"b":[157,166,175,185,190,196,205]}}]
st=state(manques={},extra_sessions=SES);P=st['profile'];P['planStart']='2026-11-02';P['planFrom']='2026-11-02';P['decal']={'2026-11-11':'2026-11-15','2026-11-15':'2026-11-11'}
P['fcMax']=205;P['fcRepos']=50
errs=[];ok=True;req=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def streams(route):
    req.append(route.request.post_data or '');route.fulfill(status=200,content_type='application/json',body=json.dumps(dict(FLUX,altSource='altitude')))
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/functions/v1/intervals-streams',streams)
    ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body='{"activities":[]}'))
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort());ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-11-11T21:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(5000)
    pg.locator('nav').get_by_text('Semaine').click();pg.wait_for_timeout(500);pg.locator('.wd:not(.rest)').filter(has_text='Sortie longue').first.click();pg.wait_for_timeout(1500)
    t=pg.locator('#sheet').inner_text()
    chk(len(req)==1 and json.loads(req[0]).get('id')=='i1','une seule lecture du détail, identifiant sans « icu: »')
    chk('Terrain' in t and 'Ce que ça dit' in t and 'Pour la suite' in t,'blocs : Terrain, Ce que ça dit, Pour la suite')
    chk('FC stabilisée' in t and '162' in t,'FC stabilisée (162) au lieu de la moyenne')
    chk('65' in t and 'Hors allure facile' in t,'65 % au-dessus de 158 (zones de l\'appli, pas celles figées d\'intervals.icu)')
    chk('ne sont pas celles' not in t,'plus d\'avertissement sur les zones figées')
    chk('Faux plat montant' in t and 'Éq. plat' in t,'Terrain : 5 catégories et allure équivalente plat')
    chk('384' in t,'vitesse de montée affichée')
    chk(pg.locator('#sheet details summary',has_text='Par km').count()==1 and not pg.locator('#sheet details',has_text='Par km').first.evaluate('e=>e.open'),'détail par km replié')
    pg.locator('#sheet div',has_text='Hors allure facile').last.scroll_into_view_if_needed();pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/seance.png')
    pg.locator('#sheet details summary',has_text='Par km').click();pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/km.png')
    pg.locator('#sheet h3',has_text='Ce que ça dit').scroll_into_view_if_needed();pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/constats.png')
    s=json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'));x=[z for z in s['sessions'] if z['id']=='x1'][0]
    chk(x.get('flux',{}).get('v')==3 and 'time' not in x['flux'],'résumé enregistré avec la séance, sans la trace brute (%d o)'%len(json.dumps(x.get('flux'))))
    pg.evaluate('app.close()');pg.wait_for_timeout(300);pg.locator('.wd:not(.rest)').filter(has_text='Sortie longue').first.click();pg.wait_for_timeout(800)
    chk(len(req)==1,'réouverture : pas de nouvelle lecture')
    pg.evaluate('app.close()');pg.locator('nav').get_by_text('Profil').click();pg.wait_for_timeout(400);pg.evaluate("app.psub('toi')");pg.wait_for_timeout(500);pt=pg.locator('main').first.inner_html() if pg.locator('main').count() else pg.content()
    pg.get_by_text('Ta fréquence cardiaque').first.scroll_into_view_if_needed();pg.wait_for_timeout(200);pg.screenshot(path=OUT+'/profil.png')
    chk('Ta fréquence cardiaque' in pt and 'jusqu\'à <b>158 bpm' in pt,'Profil : carte « Ta fréquence cardiaque », allure facile jusqu\'à 158')
    b.close()
print('errs',errs);ok=ok and not errs
sys.exit(0 if ok else 1)
