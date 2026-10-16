import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v35.py').read().split("run('obj'")[0])
def m(pg,logs):
    pg.locator('nav').get_by_text('Profil').click(); pg.evaluate("app.psub('objectif')"); pg.wait_for_timeout(300)
    logs.append(json.dumps(pg.evaluate("""(()=>{const o=document.querySelector('.obs');const r=e=>Math.round(e.getBoundingClientRect().width);return {obs:r(o),span:r(o.children[0]),sw:o.children[0].scrollWidth,b:r(o.children[1]),tx:r(o.parentNode),ah:r(o.closest('.ah')),fs:getComputedStyle(o.children[0]).fontSize}})()""")))
run('m',steps=m,acts=[])
