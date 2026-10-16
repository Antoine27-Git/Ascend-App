import sys,re,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v32'").replace("/v28","/v32"))
import os;os.makedirs(OUT,exist_ok=True)
def shot(pg,name):pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/'+name+'.png',full_page=True)
def st(pg):return json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
def prof(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); shot(pg,'p_home')
    logs.append('home: '+pg.locator('main').inner_text().replace('\n',' | ')[:400])
    for k in ['objectif','semaine','modules','materiel','donnees','avances']:
        pg.evaluate("app.psub('%s')"%k); shot(pg,'p_'+k)
    pg.evaluate("app.psub('modules')"); pg.locator('.pmod .ah').first.click(); shot(pg,'p_modules_open')
    pg.evaluate("app.psub('toi')"); shot(pg,'p_toi')
    w=pg.get_by_label('Poids'); w.fill('88.5'); w.dispatch_event('change'); pg.wait_for_timeout(300)
    pg.get_by_role('button',name='+ Ajouter une course').click(); pg.wait_for_timeout(300)
    n=pg.get_by_label('Nom').last; n.fill('Trail des Coursières'); n.dispatch_event('change'); pg.wait_for_timeout(200)
    pg.locator('.acc.open .pr').filter(has_text='Durée').click(); pg.wait_for_timeout(400)
    shot(pg,'p_roue')
    pg.evaluate("document.getElementById('wh').scrollTop=5*40;document.getElementById('wm').scrollTop=12*40"); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT+'/p_roue_vp.png')
    pg.get_by_role('button',name='OK').click(); pg.wait_for_timeout(300)
    d=pg.get_by_label('Distance').last; d.fill('34'); d.dispatch_event('change'); pg.wait_for_timeout(200)
    pg.get_by_role('button',name='Occasionnel').click(); pg.wait_for_timeout(200)
    shot(pg,'p_toi_apres')
    s=st(pg)['profile'];logs.append('saved: weight=%s races=%s mountain=%s'%(s['weight'],json.dumps(s['start']['pastRaces']),s['terrain']))
    pg.evaluate("app.psub('materiel')"); pg.get_by_role('button',name='Non').click(); shot(pg,'p_materiel_non')
    logs.append('hasWatch=%s'%st(pg)['profile'].get('hasWatch'))
base['start']={'freq4w':1,'dur4w':45,'lastLong':{'date':'2026-08-20','dur':107,'dist':14,'dplus':500},'pastRaces':[{'name':'','date':'2026-04-12','dur':392,'dist':42,'dplus':1300},{'date':'2025-06-01','dur':125,'dist':15,'dplus':480}]}
base['terrain']={'climb':'1-5','mountain':'reg'}
acts=[{"id":"a1","date":"2026-10-14","name":"Run","type":"Run","dur_s":2700,"dist_m":7000,"dplus":80,"hr_avg":140,"hr_max":150,"device":"Garmin fēnix 7"}]
run('prof',steps=prof,acts=acts,mods={'strength':True,'nutrition':True})
def send(pg,logs):
    bodies=[]
    pg.on('request',lambda r:bodies.append(r.post_data) if 'intervals-event' in r.url else None)
    pg.wait_for_timeout(800);pg.evaluate("app.openSess('g2026-10-15-ef')");pg.wait_for_timeout(400)
    pg.locator('.fw button').first.click();pg.wait_for_timeout(800)
    logs.append('payload: '+str([json.loads(b)['name'] for b in bodies if b]))
    logs.append('watchName=%s'%st(pg)['profile'].get('watchName'))
    pg.evaluate("app.close()");pg.evaluate("app.go('profil')");shot(pg,'p_home2')
run('send',steps=send,acts=acts)
