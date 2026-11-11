# D-98 : import montre — le type vient du plan ; D− et zones de FC lus ; la trace complète sans écraser
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v56');os.makedirs(OUT,exist_ok=True)
TCX=sys.argv[1] if len(sys.argv)>1 else None
st=state(manques={});P=st['profile'];P['planStart']='2026-11-02';P['planFrom']='2026-11-02';P['decal']={'2026-11-11':'2026-11-15','2026-11-15':'2026-11-11'};P['hasWatch']=True
ACT=[{"id":"i1","date":"2026-11-11","name":"Marcilly-d'Azergues - 20261111_SL_D50","type":"Run","dur_s":3610,"elapsed_s":3669,"dist_m":8682,"dplus":164,"dminus":150,"hr_avg":158,"hr_max":174,"hr_zone_times":[400,300,1200,1300,400,10,0],"hr_zones":[140,150,160,165,170,180,200],"device":"Fenix 7"}]
errs=[];ok=True
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def val(pg,lbl):return pg.locator('#sheet label.f',has_text=lbl).locator('xpath=following-sibling::input[1]').first.input_value() if pg.locator('#sheet label.f',has_text=lbl).count() else None
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps({"activities":ACT})))
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort());ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-11-11T13:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(5000);print(pg.locator('main').inner_text().replace('\n',' | ')[:600])
    pg.screenshot(path=OUT+'/aujourdhui.png',full_page=True)
    pg.get_by_text('Noter mon effort').first.click();pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+'/fiche.png',full_page=True)
    txt=pg.locator('#sheet').inner_text()
    chk('Type : Sortie longue' in txt,'type de la séance prévue (Sortie longue), pas déduit de la durée')
    vals=pg.locator('#sheet input[type=number]').evaluate_all('l=>l.map(x=>x.value)')
    chk('150' in vals,'D− lu dans intervals.icu : '+str(vals))
    if TCX:
        pg.locator('#sheet input[type=file]').set_input_files(TCX);pg.wait_for_timeout(800)
        v2=pg.locator('#sheet input[type=number]').evaluate_all('l=>l.map(x=>x.value)')
        chk(v2[:4]==vals[:4],'la trace ne remplace pas les données de la montre : '+str(v2[:4]))
        pg.screenshot(path=OUT+'/fiche_trace.png',full_page=True)
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs))
sys.exit(0 if ok else 1)
