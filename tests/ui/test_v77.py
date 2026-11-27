# v77 : étape 2 en cases, un seul champ « Ta perception » (multi-ligne, envoyé à l'IA), pastille de 2e séance, calendrier pour déplacer, montre relue à l'étape 1
# repris du test v75 ; : saisie en 3 étapes (source, confirmation, bilan), effet sur le plan, « Pour comprendre » en blocs, aucune analyse IA automatique
import json, math, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v77');os.makedirs(OUT,exist_ok=True)
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
    elif 'analyze-session' in u:ia.append(r.request.post_data);r.fulfill(status=200,content_type='application/json',body=json.dumps({'interpretation':'Lecture de test.','conseil':'Conseil de test.'}))
    else:r.fulfill(status=200,content_type='application/json',body='{}')
VIDE={'activities':[]}
with sync_playwright() as p:
    b=p.chromium.launch()
    def ctx(acts=None,decal=None):
        c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
        def rt(r):
            if acts is not None and 'intervals-activities' in r.request.url:return r.fulfill(status=200,content_type='application/json',body=json.dumps(acts))
            return route(r)
        c.route('**/functions/v1/**',rt);c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
        st=profil()
        if decal:st['profile']['decal']=decal
        c.add_init_script('if(!sessionStorage.getItem("ini")){sessionStorage.setItem("ini","1");localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
        pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.clock.set_fixed_time(JOUR+'T17:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(4000)
        return c,pg
    c,pg=ctx()
    v=pg.locator('#view').inner_text()
    chk("J'ai fait ma séance" not in v and 'Valider ma séance' in v,'accueil : un seul libellé, « Valider ma séance »')
    pg.locator('#view .sc.today button',has_text='Valider ma séance').first.click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text()
    chk(t.startswith('Valider ma séance') and 'Lozanne Trail' in t,'étape 1 : titre « Valider ma séance », sortie trouvée')
    pg.locator('#sheet button',has_text='Utiliser').click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/2-cases.png')
    tl=pg.locator('#sheet .wt4 > div').all_inner_texts()
    chk(len(tl)==4 and 'Durée' in tl[0] and '1 h 15' in tl[0] and '11,6' in tl[1] and '180' in tl[2] and '160' in tl[3],'étape 2 : 4 cases (durée, distance, D+, FC) '+str([x.replace(chr(10),' ') for x in tl]))
    chk(pg.locator('#sheet .wok').count()==1 and 'Lozanne Trail' in pg.locator('#sheet .wok').inner_text(),'étape 2 : ✓ et nom de la sortie')
    chk(pg.locator('#sheet textarea.pta').count()==1 and pg.locator('#sheet textarea.pta').get_attribute('maxlength')=='600','étape 2 : un seul champ « Ce que tu as ressenti », 600 caractères')
    ta=pg.locator('#sheet textarea.pta');ta.click();ta.fill('Jambes lourdes au début.\nMieux dans la 2e montée.');ta.dispatch_event('input');ta.blur();pg.wait_for_timeout(200)
    chk('49 / 600' in pg.locator('#sheet').inner_text(),'compteur de caractères')
    pg.locator('#sheet .scale button, #sheet .r10 button').nth(2).click();pg.wait_for_timeout(200)
    pg.locator('#sheet button',has_text='Valider').click();pg.wait_for_timeout(2500)
    q=pg.locator('#sheet .pquote')
    chk(q.count()==1 and q.inner_text()=='Jambes lourdes au début.\nMieux dans la 2e montée.','bilan : ta perception affichée, retours à la ligne gardés')
    chk('L\'IA confronte ta perception aux données.' in pg.locator('#sheet').inner_text() and pg.locator('#sheet input:not([type])').count()==0,'bilan : plus de second champ de texte ; texte d\'aide adapté')
    pg.locator('#sheet .in').screenshot(path=OUT+'/3-bilan.png',)
    pg.locator('#sheet .pquote').scroll_into_view_if_needed();pg.wait_for_timeout(200);pg.locator('#sheet .in').screenshot(path=OUT+'/3b-perception.png')
    pg.locator('#sheet button',has_text='Analyser la séance').click();pg.wait_for_timeout(1500)
    bl=json.loads(ia[0])['bilan'] if ia else {}
    chk(bl.get('perception')=='Jambes lourdes au début.\nMieux dans la 2e montée.' and bl.get('note') is None,'IA : la perception est envoyée, en entier, avec ses retours à la ligne')
    chk(pg.locator('#sheet .pquote').count()==1,'après l\'analyse : ta perception reste affichée')
    c.close()
    # étape 1 sans sortie arrivée
    c,pg=ctx(acts=VIDE)
    pg.locator('#view .sc.today button',has_text='Valider ma séance').first.click();pg.wait_for_timeout(400)
    t=pg.locator('#sheet').inner_text();pg.locator('#sheet .in').screenshot(path=OUT+'/1-pas-arrivee.png')
    chk('Pas encore arrivée' in t and 'Réessayer' in t and 'Saisir à la main' in t,'étape 1 : « Pas encore arrivée », Réessayer, Saisir à la main')
    pg.locator('#sheet button',has_text='Saisir à la main').click();pg.wait_for_timeout(400)
    pg.locator('#sheet input[placeholder=min]').fill('40');pg.locator('#sheet input[placeholder=min]').dispatch_event('change')
    pg.locator('#sheet .scale button, #sheet .r10 button').nth(2).click();pg.wait_for_timeout(200)
    pg.locator('#sheet button',has_text='Valider').click();pg.wait_for_timeout(2000)
    t=pg.locator('#sheet').inner_text()
    chk('non renseignée' in t and 'Ajouter' in t and 'L\'IA analyse les données et ton effort ressenti.' in t,'sans perception : « Ta perception : non renseignée · Ajouter »')
    pg.locator('#sheet button.lk',has_text='Ajouter').scroll_into_view_if_needed();pg.wait_for_timeout(200);pg.locator('#sheet .in').screenshot(path=OUT+'/3c-sans-perception.png')
    pg.locator('#sheet button.lk',has_text='Ajouter').click();pg.wait_for_timeout(300)
    chk(pg.locator('#sheet #percEdit textarea.pta').count()==1,'« Ajouter » ouvre le champ dans le bilan')
    c.close()
    # course et renforcement le même jour : pastille
    c,pg=ctx(decal={'2026-11-11':'2026-11-10'})
    chk(pg.locator('#view .wk .st:not(.one) .d').count()>=2,'semaine : la 2e séance du jour s\'affiche sous la première (v86)')
    pg.locator('#view .wk').first.screenshot(path=OUT+'/4-semaine.png')
    c.close()
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs[:2]))
print('OK' if ok else 'ÉCHEC');sys.exit(0 if ok else 1)
