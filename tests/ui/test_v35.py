import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v35'").replace("/v28","/v35"))
import os;os.makedirs(OUT,exist_ok=True)
def shot(pg,name):pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/'+name+'.png',full_page=True)
def vshot(pg,name):pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/'+name+'.png')
def st(pg):return json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
def f(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); pg.evaluate("app.psub('objectif')"); shot(pg,'obj')
    logs.append(pg.locator('main').inner_text().replace('\n',' | ')[:500])
    pg.locator('.ob .ah').last.click(); shot(pg,'obj_goal')
    pg.locator('.ob .ah').first.click(); shot(pg,'obj_ir')
    pg.evaluate("app.psub('toi')"); pg.locator('.pr').filter(has_text='Durée').nth(1).click(); pg.wait_for_timeout(400)
    pg.evaluate("document.getElementById('wh').scrollTop=99999;document.getElementById('wm').scrollTop=99999"); pg.wait_for_timeout(400); vshot(pg,'roue')
    pg.get_by_role('button',name='OK').click(); pg.wait_for_timeout(300)
    logs.append('lastLong.dur=%s'%st(pg)['profile']['start']['lastLong']['dur'])
    for k in ['semaine','modules','materiel','donnees','avances']: pg.evaluate("app.psub('%s')"%k); pg.wait_for_timeout(150)
    pg.evaluate("app.go('profil')"); shot(pg,'home')
    pg.locator('nav').get_by_text('Semaine').click(); shot(pg,'tab_semaine')
base['start']={'freq4w':1,'dur4w':45,'lastLong':{'date':'2026-08-20','dur':107,'dist':14,'dplus':500},'pastRaces':[{'name':'Trail du Beaujolais','date':'2026-04-12','dur':392,'dist':42,'dplus':1300}]}
base['goalDist']=80;base['goalDplus']=5000
base['races']=[{'name':'Trail des Coursières 2027','date':'2027-05-08','dist':50,'dplus':1900,'prio':'B'},{'name':'Trail de la Croix-Rousse','date':'2027-03-14','dist':23,'dplus':800,'prio':'C'}]
run('obj',steps=f,acts=[],mods={'strength':True})
