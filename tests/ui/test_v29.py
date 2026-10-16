import json, os, sys, re
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v29'").replace("/v28","/v29"))
def sheet(pid):
    def f(pg,logs):
        pg.evaluate("app.openSess('%s')"%pid); pg.wait_for_timeout(500)
        t=pg.locator('#sheet').inner_text()
        logs.append('H1: '+pg.locator('#sheet h1').inner_text())
        logs.append('texte: '+t.replace('\n',' | ')[:900])
        logs.append('codes: '+str(re.findall(r'\b[DHS]\d?-\d+\b|\([A-Z]\d\)',t)))
        pg.screenshot(path=OUT+'/fiche_%s.png'%pid)
        pg.evaluate("document.querySelector('.sheet .in').scrollTop=99999"); pg.wait_for_timeout(250); pg.screenshot(path=OUT+'/fiche_%s_bas.png'%pid); pg.evaluate("document.querySelector('.sheet .in').scrollTop=0")
        if pg.locator('#fmenu').count():
            pg.locator('#fmenu').click(); pg.wait_for_timeout(300)
            logs.append('menu: '+pg.locator('#fmenulist').inner_text().replace('\n',' / '))
            pg.screenshot(path=OUT+'/fiche_%s_menu.png'%pid)
    return f
run('long',steps=sheet('g2026-10-18-long'),acts=[],mods={'nutrition':True})
run('ef',steps=sheet('g2026-10-15-ef'),acts=[])
run('long_sansnut',steps=sheet('g2026-10-18-long'),acts=[],mods={'nutrition':False})
