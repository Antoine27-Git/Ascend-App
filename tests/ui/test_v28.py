import json, os, sys, copy
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); OUT=os.path.join(ROOT,'captures','ui','v28'); os.makedirs(OUT,exist_ok=True)
base=json.load(open(ROOT+'/tests/t_prof.json',encoding='utf-8')); base.update({'name':'Test','onboarded':True,'introSeen':True})
auth={'access_token':'x','refresh_token':'y','expires_at':9999999999999,'email':'t@l','user_id':'u'}
ACTS=[{"id":"a15","date":"2026-10-15","name":"Footing","type":"Run","dur_s":2400,"dist_m":6500,"dplus":40,"hr_avg":138,"hr_max":152},
      {"id":"a13","date":"2026-10-13","name":"Footing","type":"Run","dur_s":2280,"dist_m":6100,"dplus":30,"hr_avg":140,"hr_max":155}]
def run(name, day='2026-10-15', hour='07:30', sessions=(), daily=None, mods=None, acts=ACTS, steps=None):
    prof=copy.deepcopy(base)
    if mods: prof.setdefault('modules',{}).update(mods)
    state={'v':2,'profile':prof,'daily':daily or {},'sessions':list(sessions),'plan':[]}
    errs=[];logs=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
        ctx.route('**/functions/v1/intervals-activities',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps({"activities":acts})))
        ctx.route('**/functions/v1/intervals-event',lambda r:r.fulfill(status=200,content_type='application/json',body=json.dumps({"ok":True,"result":"created","id":1})))
        ctx.route('**/*supabase.co/rest/**',lambda r:r.abort()); ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
        ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(state)),json.dumps(json.dumps(auth))))
        pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.clock.set_fixed_time('%sT%s:00+02:00'%(day,hour))
        pg.goto('file://'+ROOT+'/index.html'); pg.wait_for_timeout(1700)
        pg.screenshot(path=OUT+'/%s.png'%name,full_page=True)
        if steps: steps(pg,logs)
        b.close()
    print(name,'| erreurs JS:',errs,'|',' ; '.join(logs))
def flow(pg,logs):
    btn=pg.get_by_role('button',name='Vers ma montre').first
    btn.click(); pg.wait_for_timeout(600)
    logs.append('après envoi: '+str(pg.get_by_role('button',name='Sur la montre ✓').count()))
    pg.get_by_role('button',name='Noter mon effort').nth(1).click(); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+'/flow_saisie.png')
    pg.locator('.scale.r10 button').nth(3).click(); pg.wait_for_timeout(150)
    pg.get_by_role('button',name='Enregistrer',exact=True).click(); pg.wait_for_timeout(900)
    pg.screenshot(path=OUT+'/flow_apres.png')
    logs.append('toast: '+pg.locator('#toast').inner_text().replace('\n',' / '))
    st=json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
    logs.append('séances: '+json.dumps([(x['date'],x['type'],x['dur'],x.get('rpe'),x.get('ext'),x.get('plannedId')) for x in st['sessions']]))
    pg.screenshot(path=OUT+'/flow_apres_full.png',full_page=True)
which=sys.argv[1:] or ['montre','fait','repos','malade','journal','flow']
done=[{"id":"s1","date":"2026-10-15","type":"ef","dur":40,"dist":6.5,"dplus":40,"rpe":3,"plannedId":"g2026-10-15-ef"}]
if 'montre' in which: run('montre')
if 'fait' in which: run('fait',sessions=done,acts=[])
if 'repos' in which: run('repos',day='2026-10-16',acts=[])
if 'malade' in which: run('malade',daily={'2026-10-15':{'status':'sick'}},acts=[])
if 'journal' in which: run('journal',mods={'journal':True},acts=[])
if 'flow' in which: run('flow0',steps=flow)
