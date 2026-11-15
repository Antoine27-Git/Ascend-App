# v75 (D-107) : saisie en 3 étapes (source, confirmation, bilan), effet sur le plan, « Pour comprendre » en blocs, aucune analyse IA automatique
import json, math, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v75');os.makedirs(OUT,exist_ok=True)
JOUR='2026-11-15'
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
    elif 'analyze-session' in u:ia.append(u);r.fulfill(status=200,content_type='application/json',body=json.dumps({'interpretation':'Lecture de test.','conseil':'Conseil de test.'}))
    else:r.fulfill(status=200,content_type='application/json',body='{}')
with sync_playwright() as p:
    b=p.chromium.launch()
    c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    c.route('**/functions/v1/**',route);c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
    c.add_init_script('if(!sessionStorage.getItem("ini")){sessionStorage.setItem("ini","1");localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(profil())),json.dumps(json.dumps(AUTH))))
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(JOUR+'T17:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(4000)
    chk(pg.locator('#view button',has_text='Ajouter').count()>=1,'la montre est lue en silence à l\'ouverture (activité proposée sur l\'accueil)')
    # étape 1
    chk('Noter mon effort' in pg.locator('#view').inner_text(),'accueil : la séance du jour propose la sortie de la montre')
    pg.locator('#view button',has_text="Ajouter une autre séance").first.click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/1-source.png')
    chk('Étape 1 sur 3 · Source' in t and 'SÉANCE DÉTECTÉE SUR TA MONTRE' in t.upper(),'étape 1 : source')
    chk('Lozanne Trail' in t and '1 h 15' in t and '11,6 km' in t and '180 m' in t and '160 bpm' in t,'étape 1 : nom de la sortie et mesures')
    chk('Utiliser' in t and 'Saisir à la main' in t and 'renforcement, vélo' in t,'étape 1 : Utiliser, ou Saisir à la main')
    # saisie à la main puis retour
    pg.locator('#sheet button',has_text='Saisir à la main').click();pg.wait_for_timeout(300)
    t=pg.locator('#sheet').inner_text();chk('Étape 2 sur 3 · Saisie' in t and 'Durée (min)' in t and 'Retour' in t,'« Saisir à la main » : formulaire habituel, étape 2')
    pg.locator('#sheet button',has_text='Retour').click();pg.wait_for_timeout(300)
    chk('Étape 1 sur 3' in pg.locator('#sheet').inner_text(),'« Retour » revient à la source')
    # étape 2
    pg.locator('#sheet button',has_text='Utiliser').click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/2-confirmation.png')
    chk('Étape 2 sur 3 · Confirmation' in t and 'LU SUR TA MONTRE' in t.upper() and 'TA PERCEPTION' in t.upper(),'étape 2 : confirmation, « Lu sur ta montre », « Ta perception »')
    chk('Compte pour' in t and 'Sortie longue' in t and 'Changer' in t,'étape 2 : rattachée seule à la séance prévue du jour, « Changer »')
    chk(pg.locator('#sheet input[placeholder=min]').count()==0 and pg.locator('#sheet input[placeholder=km]').count()==0 and pg.locator('#sheet input[type=date]').count()==0,'étape 2 : mesures en lecture seule (aucun champ)')
    chk('Corriger' in t and 'Corriger à la main' not in t,'étape 2 : lien « Corriger »')
    chk(pg.locator('#sheet textarea').first.input_value()=='','étape 2 : la note est vide (le nom de la montre n\'y est pas recopié)')
    pg.locator('#sheet .scale button, #sheet .r10 button').nth(2).click();pg.wait_for_timeout(200)
    pg.locator('#sheet button',has_text='Valider').click();pg.wait_for_timeout(2500)
    # étape 3
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/3-bilan.png')
    S=json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"));r=[x for x in S['sessions'] if x.get('ext')=='icu:i900']
    chk(len(r)==1 and r[0]['rpe']==3 and r[0]['dur']==75 and '_conf' not in r[0] and r[0].get('plannedId'),'séance enregistrée (effort 3, 75 min, rattachée, sans champ temporaire)')
    chk('Séance enregistrée' in t and 'Étape 3 sur 3 · Bilan' in t,'étape 3 : le bilan s\'ouvre tout de suite')
    chk('FC stabilisée' in t and 'Hors allure facile' in t and 'Effort ressenti' in t and 'Vitesse de montée' in t,'bilan : les 4 tuiles')
    chk('LES CONSTATS D\'ASCEND' in t.upper() and 'CE QUE ÇA DIT' not in t.upper(),'bilan : titre « Les constats d\'Ascend »')
    chk('EFFET SUR LE PLAN' in t.upper() and 'Prochaine sortie longue' in t,'bilan : bloc « Effet sur le plan »')
    chk('dépasse de 25 %' in t and 'garde-fou pour limiter le risque de blessure' in t and 'Éric Lacroix' in t,'effet : saut de 25 %, phrase du garde-fou, citation')
    pg.locator('#effet summary').click();pg.wait_for_timeout(200);t2=pg.locator('#effet').inner_text()
    chk('Retenue comme référence' in t2 and '1\u00a0h\u00a006' in t2 and '+10 % au max' in t2 and 'convention' in t2,'effet : « Le calcul » (référence retenue 1 h 06, convention dite)')
    chk('Souvent chaleur' not in t,'dérive : plus de « Souvent chaleur ou hydratation »')
    chk('Analyser la séance' in t and 'seulement si tu appuies' in t,'bouton « Analyser la séance »')
    chk(len(ia)==0,'aucun appel à l\'IA sans appui (%d)'%len(ia))
    chk('POUR COMPRENDRE' in t.upper() and pg.locator('#sheet .pc details').count()==5,'« Pour comprendre » : 5 blocs repliables')
    pg.locator('#sheet .pc summary').first.click();pg.wait_for_timeout(200)
    chk('plus de +3 %' in pg.locator('#sheet .pc').inner_text() and 'Minetti' in t,'bloc Pente : mini-tableau ; sources en bas')
    # rien ne dépasse
    w=pg.evaluate("Math.max(...[...document.querySelectorAll('#sheet .in *')].map(e=>e.getBoundingClientRect().right))")
    chk(w<=360.5,'rien ne dépasse de l\'écran (%.0f px)'%w)
    pg.locator('#sheet button',has_text='Analyser la séance').click();pg.wait_for_timeout(1500)
    chk(len(ia)==1 and 'Lecture de test.' in pg.locator('#sheet').inner_text(),'appui sur « Analyser la séance » : un appel, analyse affichée dans le bilan')
    pg.locator('#sheet .in').screenshot(path=OUT+'/3-bilan-ia.png')
    pg.locator('#sheet button',has_text='Terminer').click();pg.wait_for_timeout(300)
    print('   url',pg.url[-40:]);chk(pg.evaluate("!!document.querySelector('#sheet')&&!document.querySelector('#sheet').firstElementChild"),'« Terminer » ferme le bilan')
    # sans montre lue : saisie directe, comme avant
    c2=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    c2.route('**/functions/v1/**',lambda r:r.fulfill(status=500,content_type='application/json',body='{"error":"x"}'));c2.route('**/*supabase.co/rest/**',lambda r:r.abort());c2.route('**/*supabase.co/auth/**',lambda r:r.abort())
    c2.add_init_script('if(!sessionStorage.getItem("ini")){sessionStorage.setItem("ini","1");localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(profil())),json.dumps(json.dumps(AUTH))))
    p2=c2.new_page();p2.on('pageerror',lambda e:errs.append(str(e)))
    p2.clock.set_fixed_time(JOUR+'T17:00:00+01:00');p2.goto('file://'+ROOT+'/index.html');p2.wait_for_timeout(4000)
    p2.locator('#view button',has_text="J'ai fait ma séance").first.click();p2.wait_for_timeout(400)
    t=p2.locator('#sheet').inner_text();chk('Nouvelle séance' in t and 'Étape' not in t and 'Enregistrer' in t,'sans lecture de montre : formulaire direct, sans étapes')
    chk(not errs,'aucune erreur JavaScript %s'%errs[:2])
    b.close()
sys.exit(0 if ok else 1)
