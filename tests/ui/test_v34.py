import sys,re,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v34'").replace("/v28","/v34"))
import os;os.makedirs(OUT,exist_ok=True)
def shot(pg,name):pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/'+name+'.png',full_page=True)
def vshot(pg,name):pg.wait_for_timeout(300);pg.screenshot(path=OUT+'/'+name+'.png')
def st(pg):return json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
def prof(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); shot(pg,'home')
    pg.evaluate("app.psub('objectif')"); shot(pg,'objectif')
    d=pg.get_by_label('Date').first; d.fill('2027-10-02'); d.dispatch_event('change'); pg.wait_for_timeout(600)
    vshot(pg,'objectif_confirm'); logs.append('confirm: '+pg.locator('#sheet').inner_text().replace('\n',' | ')[:300])
    logs.append('toast: '+pg.locator('#toast').inner_text()); (pg.get_by_role('button',name='Confirmer').click() if pg.get_by_role('button',name='Confirmer').count() else None); pg.wait_for_timeout(300)
    logs.append('goalDate='+st(pg)['profile']['goalDate'])
    pg.locator('.acc .ah').first.click(); shot(pg,'objectif_ir')
    pg.evaluate("app.psub('semaine')"); shot(pg,'semaine')
    pg.get_by_role('button',name='Modifier mes jours').click(); pg.wait_for_timeout(400); vshot(pg,'jours_sheet')
    logs.append('sheet: '+pg.locator('#sheet').inner_text().replace('\n',' | ')[:200])
    pg.evaluate("app.secCancel()")
    for k in ['toi','modules','materiel','donnees','avances']: pg.evaluate("app.psub('%s')"%k); shot(pg,k)
    pg.locator('nav').get_by_text('Semaine').click(); shot(pg,'tab_semaine')
    pg.locator('nav').get_by_text("Aujourd'hui").click(); shot(pg,'tab_home')
base['start']={'freq4w':1,'dur4w':45,'lastLong':{'date':'2026-08-20','dur':107,'dist':14,'dplus':500},'pastRaces':[{'name':'Trail du Beaujolais','date':'2026-04-12','dur':392,'dist':42,'dplus':1300}]}
base['terrain']={'climb':'1-5','mountain':'reg'}
run('prof',steps=prof,acts=[],mods={'strength':True,'nutrition':True})
def bil(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); pg.evaluate("app.psub('semaine')"); shot(pg,'semaine_fin')
    pg.get_by_role('button',name='Préparer la phase suivante').click(); pg.wait_for_timeout(400); vshot(pg,'bilan')
    logs.append(pg.locator('#sheet').inner_text().replace('\n',' | ')[:400])
run('bilan',day='2026-11-12',steps=bil,acts=[],mods={'strength':True})
