import sys,json
sys.argv=[sys.argv[0],'none']
exec(open('test_v28.py').read().split("which=sys.argv")[0].replace("v28'","v31'").replace("/v28","/v31"))
sess=[{"id":"s9","date":"2026-10-11","type":"long","dur":100,"dplus":300,"rpe":5,"note":"Boue au km 6","nutri":"oui","carbs":40,"nutriNote":"2 compotes","plannedId":None}]
def f(pg,logs):
    pg.wait_for_timeout(800); pg.evaluate("app.edit('s9')"); pg.wait_for_timeout(400)
    logs.append('titre: '+pg.locator('#sheet h3').first.inner_text())
    logs.append('textareas: '+str([pg.locator('#sheet textarea').nth(i).input_value() for i in range(pg.locator('#sheet textarea').count())]))
run('edit',sessions=sess,acts=[],mods={'nutrition':True},steps=f)
