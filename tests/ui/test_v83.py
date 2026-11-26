# v83 : date du dernier export, rappel après 30 jours, restauration (ajouter ce qui manque / remplacer tout avec copie de sécurité)
# repris de v78 ; le renforcement se saisit à la main directement ; « Pas faite » aussi pour le renforcement, sans effet sur le plan de course
# repris de v77 ; étape 2 en cases, un seul champ « Ta perception » (multi-ligne, envoyé à l'IA), pastille de 2e séance, calendrier pour déplacer, montre relue à l'étape 1
# repris du test v75 ; : saisie en 3 étapes (source, confirmation, bilan), effet sur le plan, « Pour comprendre » en blocs, aucune analyse IA automatique
import json, math, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v83');os.makedirs(OUT,exist_ok=True)
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
def ouvrir(b,st):
    c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR',accept_downloads=True)
    c.route('**/functions/v1/**',route);c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
    c.add_init_script('if(!sessionStorage.getItem("ini")){sessionStorage.setItem("ini","1");localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(JOUR+'T17:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(3500)
    return c,pg
def etat(pg):return json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))
def seance(i,d):return {'id':'r%d'%i,'date':d,'type':'ef','dur':40,'rpe':3}
with sync_playwright() as p:
    b=p.chromium.launch()
    st=profil();st['sessions']=[seance(i,'2026-11-%02d'%(3+i)) for i in range(8)];st['profile']['lastExport']='2026-10-10'
    c,pg=ouvrir(b,st)
    pg.locator('nav button',has_text='Profil').click();pg.wait_for_timeout(400)
    t=pg.locator('#view').inner_text()
    chk('Dernier export il y a 45 jours' in t,'Profil : rappel après 30 jours sans export')
    pg.locator('#view').screenshot(path=OUT+'/1-profil.png')
    pg.evaluate("app.psub('donnees')");pg.wait_for_timeout(400);t=pg.locator('#view').inner_text()
    T=t.upper();chk('DERNIER EXPORT' in T and 'IL Y A 45 JOURS' in T and 'EXPORTER MES DONNÉES' in T and 'RESTAURER UNE SAUVEGARDE' in T,'Données : date du dernier export, export, restauration')
    chk(pg.locator('#jin').count()==0,'plus de texte à coller pour restaurer')
    with pg.expect_download() as dl:pg.locator('#view button',has_text='Exporter mes données').click()
    pg.wait_for_timeout(400)
    chk(dl.value.suggested_filename=='ascend-'+JOUR+'.json' and etat(pg)['profile'].get('lastExport')==JOUR,'export : fichier téléchargé et date retenue')
    chk('aujourd\'hui' in pg.locator('#view').inner_text() and 'Plus de 30 jours' not in pg.locator('#view').inner_text(),'après export : « aujourd\'hui », plus de rappel')
    pg.locator('#view').screenshot(path=OUT+'/2-donnees.png')
    # fichier : 6 séances dont 2 absentes de l'appli ; l'appli en a 8 dont 4 absentes du fichier
    fic={'v':2,'profile':dict(st['profile'],name='Ancien'),'daily':{},'plan':[],'sessions':[seance(i,'2026-11-%02d'%(3+i)) for i in range(4)]+[seance(20,'2026-10-20'),seance(21,'2026-10-22')]}
    pf='/tmp/ascend-test-resto.json';json.dump(fic,open(pf,'w'))
    pg.locator('#view input[type=file]').set_input_files(pf);pg.wait_for_timeout(600)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/3-restaurer.png')
    chk('6' in t and '8' in t and '2 séances du fichier manquent' in t and '4 séances de l\'appli ne sont pas dans le fichier' in t,'résumé chiffré avant de restaurer')
    pg.locator('#sheet .fopt',has_text='Ajouter ce qui manque').click();pg.wait_for_timeout(600)
    e=etat(pg);ids={s['id'] for s in e['sessions']}
    chk(len(e['sessions'])==10 and 'r20' in ids and 'r7' in ids and e['profile'].get('name')!='Ancien','« Ajouter » : 2 séances ajoutées, rien supprimé, profil gardé')
    # remplacer tout
    pg.locator('#view input[type=file]').set_input_files(pf);pg.wait_for_timeout(600)
    pg.locator('#sheet .fopt',has_text='Remplacer tout').click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/4-remplacer.png')
    chk('Remplacer tout ?' in t and '4 séances seront supprimées' in t,'« Remplacer tout » : confirmation avec le nombre de séances supprimées')
    with pg.expect_download() as dl:pg.locator('#sheet button',has_text='Télécharger puis remplacer').click()
    pg.wait_for_timeout(500);e=etat(pg)
    chk(dl.value.suggested_filename.endswith('-avant-restauration.json') and len(e['sessions'])==6 and e['profile'].get('name')=='Ancien','copie de sécurité téléchargée, puis remplacement')
    c.close()
    # nouveau coureur (moins de 5 séances) : pas de rappel
    st2=profil();st2['sessions']=[];st2['profile'].pop('lastExport',None)
    c,pg=ouvrir(b,st2);pg.locator('nav button',has_text='Profil').click();pg.wait_for_timeout(400)
    chk('Aucun export' not in pg.locator('#view').inner_text(),'moins de 5 séances : pas de rappel')
    c.close();b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs[:2]))
print('OK' if ok else 'ÉCHEC');sys.exit(0 if ok else 1)
