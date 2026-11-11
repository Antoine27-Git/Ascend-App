# D-97 : échange de deux séances (sortie longue du dimanche ↔ endurance du mercredi), le mercredi 11/11/2026
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v55');os.makedirs(OUT,exist_ok=True)
st=state(manques={});st['profile']['planStart']='2026-11-02';st['profile']['planFrom']='2026-11-02'
errs=[];ok=True
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    ctx.route('**/*supabase.co/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-11-11T08:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(1800)
    pg.locator('nav').get_by_text('Semaine').click();pg.wait_for_timeout(500)
    pg.locator('.wd:not(.rest)').filter(has_text='Sortie longue').first.click();pg.wait_for_timeout(500)
    pg.locator('#sheet').get_by_text('Déplacer').first.click();pg.wait_for_timeout(400)
    pg.screenshot(path=OUT+'/deplacer.png',full_page=True)
    btn=pg.locator('#sheet button').filter(has_text='échange')
    chk(btn.count()==1,'le mercredi (déjà couru) est proposé en échange')
    if btn.count():btn.first.click();pg.wait_for_timeout(600)
    d=json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))['profile'].get('decal',{})
    chk(d=={'2026-11-15':'2026-11-11','2026-11-11':'2026-11-15'},'décalages enregistrés dans les deux sens : '+json.dumps(d))
    pg.keyboard.press('Escape');pg.wait_for_timeout(300);pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(1800)
    pg.screenshot(path=OUT+'/aujourdhui.png',full_page=True)
    chk('Sortie longue' in pg.locator('main').inner_text(),'Aujourd\'hui affiche la sortie longue')
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs))
sys.exit(0 if ok else 1)
