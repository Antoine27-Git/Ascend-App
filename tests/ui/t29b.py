import sys,re
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v29b'").replace("/v28","/v29b"))
def f(pg,logs):
    t=pg.locator('#app, body').first.inner_text()
    logs.append(str(re.findall(r'[^\n]*de D\+[^\n]*',t)))
run('dim',day='2026-10-18',acts=[],steps=f)
