import sys,re,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v31'").replace("/v28","/v31"))
def full(pg,name):
    h=pg.evaluate("(()=>{const s=document.querySelector('.sheet .in');return s?s.scrollHeight+60:1200})()")
    pg.set_viewport_size({'width':360,'height':int(h)}); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT+'/'+name+'.png'); pg.set_viewport_size({'width':360,'height':800})
def fiche(pid,name):
    def f(pg,logs):
        pg.wait_for_timeout(800); pg.evaluate("app.openSess('%s')"%pid); pg.wait_for_timeout(500)
        logs.append(pg.locator('#sheet').inner_text().replace('\n',' | ')[:700]); full(pg,name)
    return f
def saisie(pg,logs):
    pg.wait_for_timeout(800); pg.evaluate("app.newSession('g2026-10-18-long')"); pg.wait_for_timeout(400)
    pg.locator('.scale.r10 button').nth(3).click(); pg.wait_for_timeout(200)
    logs.append('rpeh: '+pg.locator('#rpeh').inner_text())
    full(pg,'saisie')
    pg.locator('.nsw>label:first-child').click(); pg.wait_for_timeout(300)
    logs.append('off: '+pg.locator('.nsw').inner_text().replace('\n',' / '))
    pg.locator('.nsw>label:first-child').click(); pg.wait_for_timeout(300)
    pg.locator('textarea').last.fill('2 compotes, 1 gel'); pg.locator('textarea').last.dispatch_event('change')
    pg.locator('input[placeholder="g"]').fill('30'); pg.locator('input[placeholder="g"]').dispatch_event('change')
    pg.get_by_role('button',name='Enregistrer',exact=True).click(); pg.wait_for_timeout(600)
    st=json.loads(pg.evaluate('localStorage.getItem("trail-state-v1")'))
    logs.append('saved: '+json.dumps([(x['date'],x.get('rpe'),x.get('nutri'),x.get('carbs'),x.get('nutriNote')) for x in st['sessions']]))
def sem(pg,logs):
    pg.wait_for_timeout(1500); pg.locator('nav').get_by_text('Semaine').click(); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+'/semaine.png',full_page=True)
run('f_long',day='2026-10-18',steps=fiche('g2026-10-18-long','fiche_long'),acts=[{"id":"a18","date":"2026-10-18","name":"Trail","type":"Run","dur_s":6720,"dist_m":11800,"dplus":280,"hr_avg":140,"hr_max":160}],mods={'nutrition':True})
run('f_ef_futur',day='2026-10-14',steps=fiche('g2026-10-15-ef','fiche_ef'),acts=[])
run('saisie',day='2026-10-18',steps=saisie,acts=[],mods={'nutrition':True})
run('sem',steps=sem,acts=[])
