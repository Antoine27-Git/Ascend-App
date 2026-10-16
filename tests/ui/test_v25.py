import json, os, sys
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); OUT=os.path.join(ROOT,'captures','ui'); os.makedirs(OUT,exist_ok=True)
prof=json.load(open(ROOT+'/tests/t_prof.json',encoding='utf-8')); prof.update({'name':'Test','onboarded':True,'introSeen':True})
state={'v':2,'profile':prof,'daily':{},'sessions':[],'plan':[]}
auth={'access_token':'x','refresh_token':'y','expires_at':9999999999999,'email':'t@l','user_id':'u'}
acts=[{"id":"i1","date":"2026-10-14","name":"Footing Lozanne","type":"Run","dur_s":3720,"dist_m":9800,"dplus":120,"hr_avg":142,"hr_max":165},
      {"id":"i2","date":"2026-10-12","name":"Sortie Monts du Lyonnais","type":"TrailRun","dur_s":7500,"dist_m":18200,"dplus":640,"hr_avg":151,"hr_max":172},
      {"id":"i3","date":"2026-10-13","name":"CrossFit","type":"WeightTraining","dur_s":3000,"dist_m":None,"dplus":None,"hr_avg":130,"hr_max":170}]
mode=sys.argv[1] if len(sys.argv)>1 else 'ok'
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    def fn(r):
        if mode=='404': return r.fulfill(status=404,body='{"code":"NOT_FOUND"}')
        if mode=='err': return r.fulfill(status=502,body=json.dumps({"error":"Clé d'API refusée par intervals.icu"}))
        r.fulfill(status=200,content_type='application/json',body=json.dumps({"activities":acts}))
    ctx.route('**/functions/v1/intervals-activities',fn)
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort()); ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(state)),json.dumps(json.dumps(auth))))
    pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-10-15T07:30:00+02:00')
    pg.goto('file://'+ROOT+'/index.html'); pg.wait_for_timeout(1500)
    pg.evaluate('app.go("jour")'); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT+'/v25_a_avant.png',full_page=True)
    pg.get_by_text('Récupérer mes séances').click(); pg.wait_for_timeout(600)
    pg.screenshot(path=OUT+'/v25_b_liste_%s.png'%mode,full_page=True)
    print('bouton 30 j:',pg.get_by_text('Chercher sur 30 jours').count())
    if mode=='ok':
        print('boutons Ajouter:',pg.get_by_role('button',name='Ajouter',exact=True).count())
        pg.get_by_role('button',name='Ajouter',exact=True).first.click(); pg.wait_for_timeout(500)
        pg.screenshot(path=OUT+'/v25_c_saisie.png')
        pg.locator('.scale.r10 button').nth(4).click(); pg.wait_for_timeout(200)
        pg.get_by_role('button',name='Enregistrer',exact=True).click(); pg.wait_for_timeout(1200)
        n=pg.evaluate('JSON.parse(localStorage.getItem("trail-state-v1")).sessions')
        print('sessions enregistrées:',json.dumps([{k:x.get(k) for k in ('date','type','dur','dplus','ext','src','rpe')} for x in n]))
        pg.screenshot(path=OUT+'/v25_d_apres.png',full_page=True)
        pg.get_by_text('Récupérer mes séances').click(); pg.wait_for_timeout(500)
        print('après enregistrement, restant:',pg.get_by_role('button',name='Ajouter',exact=True).count())
    b.close()
print('erreurs JS:',errs)
