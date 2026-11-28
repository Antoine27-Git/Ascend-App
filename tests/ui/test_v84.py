# v84 : 5e onglet « Bibliothèque » (icône livre ouvert, textes de la barre à 10 px), fiches par thème, retour par le geste
import json, os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from state import state, AUTH
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));OUT=os.path.join(ROOT,'captures','ui','v84');os.makedirs(OUT,exist_ok=True)
JOUR='2026-11-26'
errs=[];ok=True
def chk(c,m):
    global ok;print(('✓ ' if c else '✗ ')+m);ok=ok and c
def ouvrir(b,w):
    st=state(manques={})
    c=b.new_context(viewport={'width':w,'height':800},device_scale_factor=2,is_mobile=True,has_touch=True,timezone_id='Europe/Paris',locale='fr-FR')
    c.route('**/functions/v1/**',lambda r:r.fulfill(status=200,content_type='application/json',body='{}'))
    c.route('**/*supabase.co/rest/**',lambda r:r.abort());c.route('**/*supabase.co/auth/**',lambda r:r.abort())
    c.add_init_script('if(location.protocol==="file:"&&window.name!=="__test_ini"){window.name="__test_ini";localStorage.setItem("trail-state-v1",%s);localStorage.setItem("trail-auth-v1",%s);}'%(json.dumps(json.dumps(st)),json.dumps(json.dumps(AUTH))))
    pg=c.new_page();pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.clock.set_fixed_time(JOUR+'T08:00:00+01:00');pg.goto('file://'+ROOT+'/index.html');pg.wait_for_timeout(2500)
    return c,pg
DEBORDE="""Array.from(document.querySelectorAll('nav button')).filter(b=>{const r=b.getBoundingClientRect();
  const s=document.createRange();s.selectNodeContents(b);const t=Array.from(b.childNodes).filter(n=>n.nodeType===3).map(n=>{const g=document.createRange();g.selectNodeContents(n);return g.getBoundingClientRect();})[0];
  return t&&(t.left<r.left-0.5||t.right>r.right+0.5);}).map(b=>b.textContent)"""
with sync_playwright() as p:
    b=p.chromium.launch()
    c,pg=ouvrir(b,360)
    labs=pg.locator('nav button').all_inner_texts()
    chk([x.strip() for x in labs]==['Aujourd\'hui','Semaine','Suivi','Bibliothèque','Profil'],'barre du bas : 5 onglets, Bibliothèque avant Profil')
    fs=pg.evaluate("getComputedStyle(document.querySelector('nav button')).fontSize")
    chk(fs=='10px','textes de la barre à 10 px')
    chk(pg.locator('nav button',has_text='Bibliothèque').locator('svg path').count()==2,'icône livre ouvert (2 traits)')
    for w in (360,340,320):
        pg.set_viewport_size({'width':w,'height':800});pg.wait_for_timeout(200)
        d=pg.evaluate(DEBORDE)
        chk(d==[],'largeur %d px : aucun texte de la barre ne déborde de son fond (%s)'%(w,d))
    pg.set_viewport_size({'width':360,'height':800})
    pg.locator('nav button',has_text='Bibliothèque').click();pg.wait_for_timeout(300)
    pg.locator('nav').screenshot(path=OUT+'/0-barre.png')
    t=pg.locator('#view').inner_text()
    n=pg.locator('.bart').count()
    chk(n==16 and '16 fiches' in t,'liste : 16 fiches, nombre annoncé')
    chk(pg.locator('nav button.on').inner_text().strip()=='Bibliothèque','onglet Bibliothèque en vert')
    chk(pg.locator('.bart .lvl').count()==n and 'Utilisé par Ascend : règle des 30 jours' in t,'niveau sur chaque fiche, règle d\'Ascend en texte')
    pg.screenshot(path=OUT+'/1-liste.png',full_page=True)
    pg.locator('.bchips button',has_text='Descente').click();pg.wait_for_timeout(200)
    chk(pg.locator('.bart').count()==2 and pg.locator('.bchips button.on').inner_text()=='Descente','filtre Descente : 2 fiches')
    pg.screenshot(path=OUT+'/2-descente.png')
    pg.locator('.bchips button',has_text='Mesures').scroll_into_view_if_needed();x0=pg.evaluate("document.querySelector('.bchips').scrollLeft")
    pg.locator('.bchips button',has_text='Mesures').click();pg.wait_for_timeout(200)
    x1=pg.evaluate("document.querySelector('.bchips').scrollLeft")
    chk(x0>0 and abs(x1-x0)<2,'v87 : la rangée de thèmes ne revient pas au début (%d → %d)'%(x0,x1))
    pg.locator('.bchips button',has_text='Tout').click();pg.wait_for_timeout(200)
    pg.locator('.bart').first.click();pg.wait_for_timeout(300)
    t=pg.locator('#view').inner_text();T=t.upper()
    chk('CE QU\'IL FAUT RETENIR' in T and 'CE QUE ÇA CHANGE POUR TOI' in T and 'LIMITES' in T and 'Frandsen' in t,'fiche : retenir, ce que ça change, limites, source')
    a=pg.locator('a.blire')
    chk(a.get_attribute('href')=='https://doi.org/10.1136/bjsports-2024-109380' and a.get_attribute('target')=='_blank','lien vers l\'article, nouvel onglet')
    pg.screenshot(path=OUT+'/3-fiche.png',full_page=True)
    pg.go_back();pg.wait_for_timeout(400)
    chk(pg.locator('.bart').count()==16,'geste retour : revient à la liste')
    pg.locator('.bart',has_text='Le ventre').click();pg.wait_for_timeout(200)
    pg.locator('.pfback').click();pg.wait_for_timeout(200)
    chk(pg.locator('.bart').count()==16,'« ‹ Bibliothèque » revient à la liste')
    pg.locator('.bart',has_text='Le ventre').click();pg.wait_for_timeout(200)
    pg.locator('nav button',has_text='Profil').click();pg.wait_for_timeout(200)
    chk('Bibliothèque' not in pg.locator('#view').inner_text()[:40],'Profil s\'ouvre normalement après une fiche')
    pg.locator('nav button',has_text='Bibliothèque').click();pg.wait_for_timeout(200)
    chk(pg.locator('.bart').count()==16,'revenir sur l\'onglet rouvre la liste, pas la dernière fiche')
    for w in (390,320):
        pg.set_viewport_size({'width':w,'height':800});pg.wait_for_timeout(200);pg.screenshot(path=OUT+'/4-liste-%d.png'%w)
    c.close();b.close()
chk(not errs,'aucune erreur JavaScript '+str(errs))
sys.exit(0 if ok else 1)
