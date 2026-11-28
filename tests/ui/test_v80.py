# v80 : jour à deux séances (liste), déplacer un renforcement (calendrier), « Pas faite » sur un renforcement (deux choix)
# repris de v78 ; le renforcement se saisit à la main directement ; « Pas faite » aussi pour le renforcement, sans effet sur le plan de course
# repris de v77 ; étape 2 en cases, un seul champ « Ta perception » (multi-ligne, envoyé à l'IA), pastille de 2e séance, calendrier pour déplacer, montre relue à l'étape 1
# repris du test v75 ; : saisie en 3 étapes (source, confirmation, bilan), effet sur le plan, « Pour comprendre » en blocs, aucune analyse IA automatique
import json, math, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v80');os.makedirs(OUT,exist_ok=True)
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
def ouvrir(b,jour,decal=None):
    c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    c.route('**/functions/v1/**',route);c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
    st=profil()
    if decal:st['profile']['decal']=decal
    c.add_init_script('if(location.protocol==="file:"&&window.name!=="__test_ini"){window.name="__test_ini";localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(jour+'T08:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(4000)
    return c,pg
def etat(pg):return json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))
with sync_playwright() as p:
    b=p.chromium.launch()
    # 1. jour à deux séances : l'endurance de mercredi déplacée sur le renforcement de mardi
    c,pg=ouvrir(b,'2026-11-24',decal={'2026-11-25':'2026-11-24'})
    pg.locator('#view .wk button[aria-label^="mar. 24"]').first.click();pg.wait_for_timeout(500)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/1-jour.png')
    chk(pg.locator('#sheet .fopt').count()==2 and 'Renforcement' in t and 'Endurance' in t,'jour à deux séances : la liste des deux séances')
    pg.locator('#sheet .fopt',has_text='Renforcement').click();pg.wait_for_timeout(600)
    t=pg.locator('#sheet').inner_text()
    chk('Renforcement' in t and 'Valider ma séance' in t,'la liste ouvre la fiche du renforcement')
    c.close()
    # 2. déplacer le renforcement de mardi depuis sa fiche
    c,pg=ouvrir(b,'2026-11-24')
    pg.locator('#view .wk button[aria-label^="mar. 24"]').first.click();pg.wait_for_timeout(600)
    btn=pg.locator('#sheet button',has_text='Déplacer')
    chk(btn.count()>=1,'fiche du renforcement : bouton « Déplacer »')
    if btn.count():
        btn.first.click();pg.wait_for_timeout(400)
        pick=lambda l:pg.locator('#sheet .wk.pick button[aria-label="%s"]'%l)
        chk(pick('Vendredi').get_attribute('class').startswith('no'),'vendredi (déjà un renforcement) n\'est pas proposé')
        pick('Samedi').click();pg.wait_for_timeout(300);t=pg.locator('#sheet').inner_text()
        chk('veille de ta sortie longue' in t and 'épargne les jambes' in t,'samedi : veille de ta sortie longue, renforcement qui épargne les jambes')
        pick('Dimanche').click();pg.wait_for_timeout(300);t=pg.locator('#sheet').inner_text()
        chk('le jour de ta sortie longue' in t,'dimanche : le jour de ta sortie longue')
        pick('Demain').click();pg.wait_for_timeout(300);t=pg.locator('#sheet').inner_text()
        chk('jour de ton endurance' in t and 'si tu t\'en sens capable' in t,'mercredi : jour de ton endurance, les deux si tu t\'en sens capable')
        pick('Jeudi').click();pg.wait_for_timeout(300)
        pg.locator('#sheet .wk.pick').scroll_into_view_if_needed();pg.locator('#sheet .in').screenshot(path=OUT+'/2-deplacer.png')
        pg.locator('#sheet button',has_text='Déplacer à jeudi').click();pg.wait_for_timeout(800)
        d=etat(pg)['profile'].get('decal',{})
        chk(d.get('x:2026-11-24')=='2026-11-26','enregistré sous la clé du renforcement : '+json.dumps(d))
        chk(pg.locator('#view .wk button[aria-label^="jeu. 26"]').get_attribute('aria-label').endswith('Renforcement'),'la semaine montre le renforcement jeudi')
    c.close()
    # 3. « Pas faite » sur un renforcement : deux choix
    c,pg=ouvrir(b,'2026-11-24')
    carte=pg.locator('#view .sc',has_text='Renforcement').first
    carte.locator('button',has_text='Pas faite').click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/3-pas-faite.png')
    chk('La faire un autre jour' in t and 'Je ne la ferai pas cette semaine' in t,'deux choix : un autre jour, ou pas cette semaine')
    pg.locator('#sheet .fopt',has_text='La faire un autre jour').click();pg.wait_for_timeout(600)
    chk(pg.locator('#sheet .wk.pick').count()==1,'« La faire un autre jour » ouvre le calendrier de la fiche')
    pg.evaluate('app.close()');pg.wait_for_timeout(400)
    carte=pg.locator('#view .sc',has_text='Renforcement').first
    carte.locator('button',has_text='Pas faite').click();pg.wait_for_timeout(400)
    pg.locator('#sheet .fopt',has_text='Je ne la ferai pas').click();pg.wait_for_timeout(800)
    chk(etat(pg)['profile'].get('manques',{}).get('x:2026-11-24')=='autre','« Je ne la ferai pas » : noté en un appui')
    c.close()
    # 4. plus aucun jour possible : renforcement placé dimanche, ouvert dimanche : noté directement, sans fenêtre
    c,pg=ouvrir(b,'2026-11-29',decal={'x:2026-11-27':'2026-11-29'})
    carte=pg.locator('#view .sc',has_text='Renforcement').first
    chk(carte.count()==1,'dimanche : la carte du renforcement déplacé')
    if carte.count():
        carte.locator('button',has_text='Pas faite').click();pg.wait_for_timeout(900)
        m=etat(pg)['profile'].get('manques',{})
        chk(pg.locator('#sheet .fopt').count()==0 and m.get('x:2026-11-27')=='autre','aucun autre jour possible : noté directement, sans fenêtre '+json.dumps(m))
    c.close()
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs[:2]))
print('OK' if ok else 'ÉCHEC');sys.exit(0 if ok else 1)
