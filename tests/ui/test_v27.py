import json, os, sys
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); OUT=os.path.join(ROOT,'captures','ui')
prof=json.load(open(ROOT+'/tests/t_prof.json',encoding='utf-8')); prof.update({'name':'Test','onboarded':True,'introSeen':True})
state={'v':2,'profile':prof,'daily':{},'sessions':[],'plan':[]}
auth={'access_token':'x','refresh_token':'y','expires_at':9999999999999,'email':'t@l','user_id':'u'}
mode=sys.argv[1] if len(sys.argv)>1 else 'ok'
calls=[];errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    def ev(r):
        body=json.loads(r.request.post_data or '{}'); calls.append(body)
        if mode=='404': return r.fulfill(status=404,body='{}')
        if mode=='err': return r.fulfill(status=502,content_type='application/json',body=json.dumps({"error":"intervals.icu a répondu 422","detail":"workout invalide"}))
        r.fulfill(status=200,content_type='application/json',body=json.dumps({"ok":True,"result":"removed" if body['action']=='remove' else "created","id":123}))
    ctx.route('**/functions/v1/intervals-event',ev)
    ctx.route('**/*supabase.co/rest/**',lambda r:r.abort()); ctx.route('**/*supabase.co/auth/**',lambda r:r.abort())
    ctx.add_init_script('localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);'%(json.dumps(json.dumps(state)),json.dumps(json.dumps(auth))))
    pg=ctx.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time('2026-10-15T07:30:00+02:00')
    pg.goto('file://'+ROOT+'/index.html'); pg.wait_for_timeout(1500)
    for sid in ['g2026-10-18-long','g2026-10-16-ef']:
        pg.evaluate('app.openSess("%s")'%sid); pg.wait_for_timeout(400)
        print(sid,'bouton envoi:',pg.get_by_role('button',name='Envoyer sur ma montre').count())
        if pg.get_by_role('button',name='Envoyer sur ma montre').count(): break
    pg.get_by_role('button',name='Envoyer sur ma montre').scroll_into_view_if_needed()
    pg.screenshot(path=OUT+'/v27_a_avant_%s.png'%mode)
    pg.get_by_role('button',name='Envoyer sur ma montre').click(); pg.wait_for_timeout(700)
    pg.get_by_text('Ma montre').first.scroll_into_view_if_needed()
    pg.screenshot(path=OUT+'/v27_b_apres_%s.png'%mode)
    print('requête:',json.dumps(calls[0],ensure_ascii=False) if calls else None)
    print('P.sent =',pg.evaluate('JSON.stringify(JSON.parse(localStorage.getItem("trail-state-v1")).profile.sent||null)'))
    if mode=='ok':
        pg.get_by_role('button',name='Retirer').click(); pg.wait_for_timeout(700)
        print('après retrait: sent =',pg.evaluate('JSON.stringify(JSON.parse(localStorage.getItem("trail-state-v1")).profile.sent||null)'),'| bouton envoi:',pg.get_by_role('button',name='Envoyer sur ma montre').count())
    b.close()
print('erreurs JS:',errs)
