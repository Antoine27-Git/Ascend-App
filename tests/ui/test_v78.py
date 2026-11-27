# v78 : le renforcement se saisit à la main directement ; « Pas faite » aussi pour le renforcement, sans effet sur le plan de course
# repris de v77 ; étape 2 en cases, un seul champ « Ta perception » (multi-ligne, envoyé à l'IA), pastille de 2e séance, calendrier pour déplacer, montre relue à l'étape 1
# repris du test v75 ; : saisie en 3 étapes (source, confirmation, bilan), effet sur le plan, « Pour comprendre » en blocs, aucune analyse IA automatique
import json, math, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v78');os.makedirs(OUT,exist_ok=True)
JOUR='2026-11-24'
def profil():
    st=state(manques={});P=st['profile']
    P.update({'planStart':'2026-11-02','planFrom':'2026-11-02','fcMax':185,'fcRepos':50,'races':[],
      'days':{'run':[0,3],'long':0,'cf':[2,5],'time':{}},'orgs':[],
      'start':{'lastLong':{'date':'2026-10-25','dur':60,'dist':9,'dplus':150},'pastRaces':[],'freq4w':1,'dur4w':45}})
    st['sessions']=[{'id':'a1','date':'2026-11-08','type':'long','dur':60,'rpe':3,'dist':9,'dplus':120}]
    return st
ACT={'activities':[{'id':'i900','date':JOUR,'type':'Run','name':'Lozanne Trail','dur_s':75*60,'elapsed_s':78*60,'dist_m':11600,'dplus':180,'dminus':180,'hr_avg':160,'hr_max':172,'device':'fenix 7'}]}
def flux():
    # 75 min, vallonné : montée puis descente répétées, FC qui monte un peu en 2e partie
    T=[];H=[];D=[];A=[];d=0;a=250
    for t in range(0,75*60+1,5):
        ph=(t//600)%3;g=[0.05,0.0,-0.05][ph];v=[1.9,2.75,3.1][ph];d+=v*5;a+=g*v*5
        T.append(t);D.append(round(d,1));A.append(round(a,1));H.append(int(150+min(10,t/60)+ (4 if t>40*60 else 0)+(3 if ph==0 else -4 if ph==2 else 0)))
    return {'time':T,'hr':H,'dist':D,'alt':A}
errs=[];ok=True;ia=[]
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def route(r):
    u=r.request.url
    if 'intervals-activities' in u:r.fulfill(status=200,content_type='application/json',body=json.dumps(ACT))
    elif 'intervals-streams' in u:r.fulfill(status=200,content_type='application/json',body=json.dumps(flux()))
    elif 'analyze-session' in u:ia.append(r.request.post_data);r.fulfill(status=200,content_type='application/json',body=json.dumps({'interpretation':'Lecture de test.','conseil':'Conseil de test.'}))
    else:r.fulfill(status=200,content_type='application/json',body='{}')
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    c.route('**/functions/v1/**',route);c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
    c.add_init_script('if(location.protocol==="file:"&&window.name!=="__test_ini"){window.name="__test_ini";localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(profil())),json.dumps(json.dumps(AUTH))))
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(JOUR+'T17:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(4000)
    carte=pg.locator('#view .sc',has_text='Renforcement').first
    chk(carte.count()==1,'accueil : la carte du renforcement du jour')
    chk('Pas faite' in carte.inner_text(),'renforcement : lien « Pas faite »')
    carte.locator('button',has_text='Valider ma séance').click();pg.wait_for_timeout(500)
    t=pg.locator('#sheet').inner_text()
    chk('Étape 1' not in t and 'Ta montre' not in t and 'Durée' in t,'renforcement : « Valider ma séance » ouvre la saisie à la main, sans la montre')
    pg.keyboard.press('Escape');pg.wait_for_timeout(300);pg.locator('#sheet .btn.x').first.click() if pg.locator('#sheet .btn.x').count() else None;pg.wait_for_timeout(300)
    ref=pg.evaluate("JSON.stringify(JSON.parse(localStorage.getItem('trail-state-v1')).profile.manques||{})")
    pg.locator('#view .sc',has_text='Renforcement').first.locator('button',has_text='Pas faite').click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/pas-faite.png')
    chk('Renforcement pas fait' in t and 'plan de course n\'est pas modifié' in t and 'Fatigue' not in t,'fenêtre courte : plan de course inchangé (v80 : deux choix)')
    pg.locator('#sheet .fopt',has_text='Je ne la ferai pas').click();pg.wait_for_timeout(900)
    m=json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))['profile'].get('manques',{})
    chk(m.get('x:'+JOUR)=='autre' and JOUR not in m,'enregistré sous sa propre clé (x:date), pas sous la date des courses : '+json.dumps(m))
    chk('Pas faite' in pg.locator('#view .sc',has_text='Renforcement').first.inner_text(),'la carte affiche « Pas faite »')
    pg.locator('#view .sc',has_text='Renforcement').first.screenshot(path=OUT+'/carte.png')
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs[:2]))
print('OK' if ok else 'ÉCHEC');sys.exit(0 if ok else 1)
