# v76 (P-23) : navigateur vidé puis connexion, le profil du compte n'est jamais écrasé par un profil vide.
# Faux serveur Supabase en mémoire (aucun appel réseau réel). Repris de tests/audit/sync_scenarios.py.
import json, os, re, sys, urllib.parse, datetime as dt
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL='file://'+os.path.join(ROOT,'index.html')
H=3600*1000;T0=int(dt.datetime(2026,11,24,8,0,tzinfo=dt.timezone.utc).timestamp()*1000)
def iso(t):return dt.datetime.fromtimestamp(t/1000,dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.')+'%03dZ'%(t%1000)
PROFIL=json.load(open(os.path.join(ROOT,'tests','t_prof.json'),encoding='utf8'))
PROFIL.update({'onboarded':True,'introSeen':True,'planStart':'2026-11-02','name':'Test','goalName':'Objectif test'})
def seance(i,date,dur):return {'id':'s'+str(i),'date':date,'type':'ef','dur':dur,'rpe':3}

class Faux:
    def __init__(s):s.rows={}
    def handle(s,route,req):
        u=urllib.parse.urlparse(req.url);q=urllib.parse.parse_qs(u.query)
        if u.path.startswith('/auth/v1/'):
            return route.fulfill(status=200,content_type='application/json',body=json.dumps({'access_token':'jeton','refresh_token':'r','expires_in':3600,'user':{'id':'u1','email':'t@e.fr'}}))
        if u.path.startswith('/rest/v1/trail_items'):
            if req.method=='GET':
                since=next((v[3:] for v in q.get('updated_at',[]) if v.startswith('gt.')),None)
                rows=sorted(s.rows.values(),key=lambda r:r['updated_at'])
                if since:rows=[r for r in rows if r['updated_at']>since]
                return route.fulfill(status=200,content_type='application/json',body=json.dumps(rows[:500]))
            for r in json.loads(req.post_data or '[]'):s.rows[(r['kind'],r['key'])]={k:r[k] for k in ('kind','key','payload','deleted','updated_at')}
            return route.fulfill(status=201,body='')
        return route.fulfill(status=200,content_type='application/json',body='{}')

def serveur(avec=True):
    s=Faux()
    if avec:
        s.rows[('profile','me')]={'kind':'profile','key':'me','payload':PROFIL,'deleted':False,'updated_at':iso(T0-48*H)}
        for i in range(1,4):s.rows[('session','s%d'%i)]={'kind':'session','key':'s%d'%i,'payload':seance(i,'2026-11-1%d'%i,30+i),'deleted':False,'updated_at':iso(T0-48*H+i)}
    return s

errs=[];ok=True
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def appareil(b,srv,etat=None,sync=None,connecte=False):
    c=b.new_context(viewport={'width':360,'height':800})
    c.route(re.compile(r'https://[a-z]+\.supabase\.co/.*'),srv.handle)
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)[:120]))
    pg.clock.install(time=dt.datetime.fromtimestamp(T0/1000,dt.timezone.utc))
    init={}
    if etat is not None:init['trail-state-v1']=json.dumps(etat)
    if sync is not None:init['trail-sync-v1']=json.dumps(sync)
    if connecte:init['trail-auth-v1']=json.dumps({'access_token':'jeton','refresh_token':'r','expires_at':T0+365*24*H,'email':'t@e.fr','user_id':'u1'})
    pg.add_init_script("(()=>{if(sessionStorage.getItem('_i'))return;sessionStorage.setItem('_i','1');const d=%s;for(const k in d)localStorage.setItem(k,d[k]);})()"%json.dumps(init))
    pg.goto(URL);pg.wait_for_timeout(300);avance(pg)
    return c,pg
def avance(pg,ms=4000):pg.clock.run_for(ms);pg.wait_for_timeout(250);pg.clock.run_for(ms);pg.wait_for_timeout(250)
def lire(pg):
    st=pg.evaluate("JSON.parse(localStorage.getItem('trail-state-v1')||'null')") or {'profile':{},'sessions':[]}
    return st.get('profile') or {},[x['id'] for x in st.get('sessions',[])]
def connexion(pg):pg.evaluate("app.setAuthF('email','t@e.fr');app.setAuthF('password','x');app.signIn()");avance(pg)

with sync_playwright() as p:
    b=p.chromium.launch()
    # 1. Navigateur vidé, puis connexion : le compte est relu, rien n'est écrasé
    srv=serveur();c,pg=appareil(b,srv);connexion(pg)
    pr,ses=lire(pg);d=srv.rows[('profile','me')]['payload']
    chk(pr.get('goalDate')==PROFIL['goalDate'] and len(ses)==3,'navigateur vidé puis connexion : profil et 3 séances relus (%s, %d)'%(pr.get('goalDate'),len(ses)))
    chk(d.get('goalDate')==PROFIL['goalDate'] and d.get('onboarded'),'… et le profil du serveur n\'est pas écrasé par un profil vide')
    chk('Bienvenue' not in pg.locator('body').inner_text() or pr.get('onboarded'),'… pas de parcours de démarrage relancé')
    c.close()
    # 2. Nouveau compte sur un téléphone déjà utilisé sans compte : ce qui est local part sur le serveur vide
    srv=serveur(False);local={'v':2,'profile':PROFIL,'daily':{},'sessions':[seance(7,'2026-11-20',40)],'plan':[]}
    c,pg=appareil(b,srv,etat=local);connexion(pg)
    chk(('profile','me') in srv.rows and srv.rows[('profile','me')]['payload'].get('goalDate')==PROFIL['goalDate'],'serveur vide : le profil local est envoyé')
    chk(('session','s7') in srv.rows,'serveur vide : la séance locale est envoyée')
    c.close()
    # 3. Appareil déjà synchronisé : une modification locale plus récente gagne toujours (règle inchangée)
    srv=serveur();plein={'v':2,'profile':dict(PROFIL,name='Nouveau'),'daily':{},'sessions':[seance(i,'2026-11-1%d'%i,30+i) for i in range(1,4)],'plan':[]}
    sh={'profile|me':json.dumps(PROFIL)}
    for i in range(1,4):sh['session|s%d'%i]=json.dumps(seance(i,'2026-11-1%d'%i,30+i))
    c,pg=appareil(b,srv,etat=plein,sync={'shadow':sh,'ts':{},'del':{},'lastPull':iso(T0-24*H)},connecte=True)
    pg.evaluate('app.syncNow()');avance(pg)
    chk(srv.rows[('profile','me')]['payload'].get('name')=='Nouveau' and lire(pg)[0].get('name')=='Nouveau','appareil déjà synchronisé : la modification locale (prénom) est envoyée, pas écrasée')
    c.close()
    b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs[:2]))
print('OK' if ok else 'ÉCHEC');sys.exit(0 if ok else 1)
