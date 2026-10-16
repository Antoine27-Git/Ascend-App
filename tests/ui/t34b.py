import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v34.py').read().split("run('prof'")[0])
def f(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); pg.evaluate("app.psub('objectif')")
    for p,v in [('goalDate','2027-05-30'),('goalDist','160')]:
        pg.evaluate("app.psetS('%s','%s','%s')"%(p,v,'s' if p=='goalDate' else 'n')); pg.wait_for_timeout(500)
        logs.append(p+': '+pg.locator('#sheet').inner_text().replace('\n',' | ')[:250]+' / toast '+pg.locator('#toast').inner_text())
        if p=='goalDate': vshot(pg,'objectif_confirm')
        pg.evaluate("app.pconfNo()")
run('conf',steps=f,acts=[])
