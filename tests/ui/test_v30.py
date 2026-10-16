import sys,re
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v30'").replace("/v28","/v30"))
def f(pg,logs):
    pg.wait_for_timeout(1500); pg.locator('nav').get_by_text('Semaine').click()
    pg.wait_for_timeout(500); pg.screenshot(path=OUT+'/semaine.png',full_page=True)
    logs.append(pg.locator('main').inner_text().replace('\n',' | ')[:900])
    pg.locator('.wd:not(.rest)').nth(1).click(); pg.wait_for_timeout(400)
    logs.append('fiche: '+pg.locator('#sheet h1').inner_text())
sess=[{"id":"s1","date":"2026-10-13","type":"cf","dur":45,"rpe":5,"plannedId":None},{"id":"s2","date":"2026-10-14","type":"ef","dur":38,"dplus":30,"rpe":3,"plannedId":"g2026-10-14-ef"}]
run('semaine',sessions=sess,acts=[],steps=f)
