# v74 (D-106) : carte « Passer à N courses par semaine ? » — avant un week-end choc et avant le bloc spécifique ; refus définitif ; ajout du jour
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v74');os.makedirs(OUT,exist_ok=True)
def profil(org_bloc=None):
    st=state(manques={});P=st['profile']
    P.update({'planStart':'2026-11-02','planFrom':'2026-11-02','goalDist':80,'goalDplus':5000,'goalDate':'2027-09-25',
      'races':[{'name':'Trail 50','date':'2027-05-08','dist':50,'dplus':1900,'prio':'B'}],
      'days':{'run':[0,3],'long':0,'cf':[2,5],'time':{}},
      'orgs':[{'from':'F3','enchaine':True,'days':{'run':[0,3,6],'long':0,'cf':[2],'time':{}}}]})
    P.setdefault('modules',{})['strength']=True
    return st
errs=[];ok=True
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def page(ctx,st,quand):
    ctx.add_init_script('if(!sessionStorage.getItem("ini")){sessionStorage.setItem("ini","1");localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(quand+'T08:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(3000)
    pg.add_script_tag(content='(function(){var module={exports:{}};'+open(os.path.join(ROOT,'tests','engine.js'),encoding='utf-8').read()+';window.ENG_T=module.exports;})();')
    # historique réaliste : chaque semaine passée, les courses prévues sont faites (ressenti facile)
    pg.evaluate('''q=>{const st=JSON.parse(localStorage.getItem("trail-state-v1"));let d=st.profile.planStart;const runs=new Set(["ef","long","qual","desc"]);let n=0;
      while(d<q){const E=ENG_T.build({profile:st.profile,today:d,sessions:st.sessions,isRun:s=>runs.has(s.type),isOff:()=>false});
        const f=new Date(new Date(d).getTime()+7*864e5).toISOString().slice(0,10);
        E.sessions.filter(x=>runs.has(x.type)&&x.date>=d&&x.date<f&&x.date<q).forEach(x=>st.sessions.push({id:"h"+(n++),date:x.date,type:x.type,dur:x.dur,dplus:x.dplus||0,rpe:3,planId:x.id}));d=f;}
      localStorage.setItem("trail-state-v1",JSON.stringify(st));}''',quand)
    pg.reload();pg.wait_for_timeout(3500)
    try:pg.wait_for_selector('#view .sc, #view .cj',timeout=15000);pg.wait_for_timeout(800)   # ménage 25/11 : l'historique de 7 mois peut dépasser 3,5 s (test instable)
    except Exception:pass
    return pg
with sync_playwright() as p:
    b=p.chromium.launch()
    def ctx():
        c=b.new_context(viewport={'width':360,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
        c.route('**/functions/v1/**',lambda r:r.fulfill(status=200,content_type='application/json',body='{"activities":[]}'))
        c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort());return c
    # 1. Trop tôt : pas de carte
    pg=page(ctx(),profil(),'2026-11-16')
    chk(pg.locator('.cj').count()==0,'mi-novembre : pas de carte (week-end choc à plus de 8 semaines)')
    # 2. 8 semaines avant le week-end choc d'avant le 50 km
    c1=ctx();pg=page(c1,profil(),'2027-02-08')
    n=pg.locator('.cj').count();chk(n==1,'début février : carte présente')
    if n:
        t=pg.locator('.cj').inner_text();print('   ---\n   '+t.replace('\n','\n   ')+'\n   ---')
        chk('Passer à 3 courses par semaine ?' in t,'titre : 3 courses, point d\'interrogation insécable')
        chk('Oui, dès cette semaine.' in t,'avis du coach')
        chk('Ce que tu y gagnes' in t and 'Volume hebdo moyen' in t and 'Volume hebdo max' in t,'gain et volumes')
        chk('Jour ajouté proposé : le samedi' in t,'jour proposé : samedi, veille de la sortie longue')
        chk('Durée estimée pour ton 50 kms' in t,'durée estimée du 50 km')
        bx=[pg.locator('.cj .btn').nth(i).bounding_box() for i in range(2)];cb=pg.locator('.cj').bounding_box()
        chk(all(x['x']>=cb['x'] and x['x']+x['width']<=cb['x']+cb['width']+0.5 for x in bx),'boutons dans la carte, sans débordement')
        h1=pg.locator('.cjt').bounding_box()['height'];chk(h1<30,'titre sur une seule ligne (%.0f px)'%h1)
        pg.locator('.cj').screenshot(path=OUT+'/choc.png')
        pg.locator('.cj .btn.p').click();pg.wait_for_timeout(1500)
        P=json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))['profile']
        org=[o for o in P.get('orgs',[]) if o['days']['run'] and 6 in o['days']['run'] and o['from']!='F3']
        chk(len(org)==1 and P['conseilJours'].get('choc:2027-03-29')=='oui','« Passer à 3 jours » : samedi ajouté à la phase en cours (%s)'%(org[0]['from'] if org else '?'))
        chk(pg.locator('.cj').count()==0,'carte disparue après le choix')
    # 3. Refus définitif
    c2=ctx();pg=page(c2,profil(),'2027-02-08')
    if pg.locator('.cj').count():
        pg.locator('.cj .cjno').click();pg.wait_for_timeout(1200)
        P=json.loads(pg.evaluate("localStorage.getItem('trail-state-v1')"))['profile']
        chk(P['conseilJours'].get('choc:2027-03-29')=='non' and pg.locator('.cj').count()==0,'« Garder 2 jours » : refus mémorisé, carte fermée')
        pg.reload();pg.wait_for_timeout(3000);chk(pg.locator('.cj').count()==0,'pas de rappel après rechargement')
    # 4. Avant le bloc spécifique
    pg=page(ctx(),profil(),'2027-06-14')
    try:pg.wait_for_selector('.cj',timeout=10000)
    except Exception:pass
    n=pg.locator('.cj').count();chk(n==1,'mi-juin, 3 semaines avant le bloc : carte du bloc spécifique')
    if n:
        t=pg.locator('.cj').inner_text();print('   ---\n   '+t.replace('\n','\n   ')+'\n   ---')
        chk('Passer à 4 courses par semaine' in t and 'Oui, si ton agenda le permet.' in t and 'Volume total sur les 9 semaines avant ta course' in t,'titre, avis, volume total')
        chk('Durée estimée pour ton 80 kms' in t,'durée estimée du 80 km')
        pg.locator('.cj').screenshot(path=OUT+'/bloc.png')
    chk(not errs,'aucune erreur JavaScript %s'%errs[:2])
    b.close()
sys.exit(0 if ok else 1)
