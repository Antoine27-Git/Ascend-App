#!/usr/bin/env python3
"""Audit mission 4 — fiabilité des données : scénarios de synchronisation rejoués sur la VRAIE appli (index.html)
dans Chrome sans écran, face à un faux serveur Supabase en mémoire (aucun appel réseau réel, aucune donnée réelle).

Le faux serveur imite ce que l'appli utilise : jeton d'authentification, lecture de trail_items filtrée par
updated_at, écriture par upsert sans condition (« merge-duplicates »). HYPOTHÈSE : le serveur garde le updated_at
envoyé par le téléphone (aucun déclencheur côté base). Le schéma réel n'est pas dans le dépôt : à confirmer.
Variante : SERVEUR_HORODATE=1 simule un déclencheur qui écrit l'heure du serveur.

Usage : python3 tests/audit/sync_scenarios.py        (Playwright + /usr/bin/google-chrome)
"""
import json, os, sys, re, urllib.parse, datetime as dt
from playwright.sync_api import sync_playwright

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
URL = 'file://' + os.path.join(RACINE, 'index.html')
SERVEUR_HORODATE = os.environ.get('SERVEUR_HORODATE') == '1'

class FauxSupabase:
    def __init__(self): self.rows = {}; self.journal = []; self.horloge = None
    def handle(self, route, request):
        u = urllib.parse.urlparse(request.url); q = urllib.parse.parse_qs(u.query)
        if u.path.startswith('/auth/v1/token'):
            return route.fulfill(status=200, content_type='application/json', body=json.dumps(
                {'access_token': 'jeton', 'refresh_token': 'rafraichir', 'expires_in': 3600, 'user': {'id': 'u1', 'email': 'test@exemple.fr'}}))
        if u.path.startswith('/rest/v1/trail_items'):
            if request.method == 'GET':
                since = None
                for v in q.get('updated_at', []):
                    if v.startswith('gt.'): since = v[3:]
                rows = sorted(self.rows.values(), key=lambda r: r['updated_at'])
                if since: rows = [r for r in rows if r['updated_at'] > since]
                return route.fulfill(status=200, content_type='application/json', body=json.dumps(rows[:500]))
            if request.method == 'POST':
                for r in json.loads(request.post_data or '[]'):
                    if SERVEUR_HORODATE and self.horloge: r['updated_at'] = self.horloge
                    self.rows[(r['kind'], r['key'])] = {k: r[k] for k in ('kind', 'key', 'payload', 'deleted', 'updated_at')}
                    self.journal.append((r['kind'], r['key'], r['deleted'], r['updated_at']))
                return route.fulfill(status=201, body='')
        return route.fulfill(status=404, body='')

def iso(t): return dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.') + '%03dZ' % (t % 1000)
T0 = int(dt.datetime(2026, 11, 10, 8, 0, tzinfo=dt.timezone.utc).timestamp() * 1000)
H = 3600 * 1000

PROFIL = json.load(open(os.path.join(RACINE, 'tests', 't_prof.json'), encoding='utf8'))
PROFIL.update({'onboarded': True, 'introSeen': True, 'planStart': '2026-11-02', 'name': 'Test', 'goalName': 'Objectif test'})
def seance(i, date, dur): return {'id': 's' + str(i), 'date': date, 'type': 'ef', 'dur': dur, 'rpe': 3}

def appareil(pw_browser, serveur, t, etat=None, connecte=True, erreurs=None):
    ctx = pw_browser.new_context(viewport={'width': 360, 'height': 800})
    ctx.reseau = {'coupe': False}   # réseau coupé pour cet appareil : les appels au serveur échouent (l'appli garde ses modifications en attente)
    ctx.route(re.compile(r'https://[a-z]+\.supabase\.co/.*'), lambda route, request: route.abort() if ctx.reseau['coupe'] else serveur.handle(route, request))
    page = ctx.new_page(); page.clock.install(time=dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc))
    if erreurs is not None: page.on('pageerror', lambda e: erreurs.append(str(e)[:120]))
    init = {}
    if etat is not None: init['trail-state-v1'] = json.dumps(etat)
    if connecte: init['trail-auth-v1'] = json.dumps({'access_token': 'jeton', 'refresh_token': 'rafraichir', 'expires_at': t + 365 * 24 * H, 'email': 'test@exemple.fr', 'user_id': 'u1'})
    page.add_init_script("(()=>{if(sessionStorage.getItem('_init'))return;sessionStorage.setItem('_init','1');const d=%s;for(const k in d)localStorage.setItem(k,d[k]);})()" % json.dumps(init))
    page.goto(URL); page.wait_for_timeout(300); avance(page, 4000)
    return ctx, page

def avance(page, ms=4000):
    page.clock.run_for(ms); page.wait_for_timeout(250); page.clock.run_for(ms); page.wait_for_timeout(250)
def synchro(page): page.evaluate("app.syncNow()"); avance(page, 500)
def lire(page):
    st = page.evaluate("JSON.parse(localStorage.getItem('trail-state-v1')||'null')") or {'profile': {}, 'sessions': []}
    sy = page.evaluate("JSON.parse(localStorage.getItem('trail-sync-v1')||'{}')")
    pr = st.get('profile') or {}
    return {'nom': pr.get('name'), 'goal': pr.get('goalDate'), 'manques': list((pr.get('manques') or {}).keys()),
            'ses': [x['id'] + ':' + str(x.get('dur')) for x in st.get('sessions', [])], 'att': len(sy.get('ts', {})) + len(sy.get('del', {})), 'lastPull': sy.get('lastPull')}
etat = lire
def modifie(page, js, t=None):
    """Une modification = l'état local change puis l'appli redémarre (elle détecte l'écart à son dernier état synchronisé).
    js reçoit l'état S et le modifie. L'horodatage de la modification est l'heure de l'appareil à ce moment."""
    if t is not None: page.clock.set_system_time(dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc))
    page.evaluate("(()=>{const S=JSON.parse(localStorage.getItem('trail-state-v1'));(%s)(S);localStorage.setItem('trail-state-v1',JSON.stringify(S));Storage.prototype.setItem=function(){};})()" % js)   # l'ancienne page ne peut plus réécrire l'état avant le rechargement
    page.reload(); page.wait_for_timeout(300); avance(page, 4000)
def quand(t): return dt.datetime.fromtimestamp(t / 1000, dt.timezone.utc)
def heure(page, t): page.clock.set_system_time(quand(t))
RES = []
def verdict(nom, ok, detail): RES.append((nom, ok, detail)); print(('✓ ' if ok else '✗ ') + nom + '\n     ' + detail)

def base_serveur():
    s = FauxSupabase()
    s.rows[('profile', 'me')] = {'kind': 'profile', 'key': 'me', 'payload': PROFIL, 'deleted': False, 'updated_at': iso(T0 - 48 * H)}
    for i in range(1, 6):
        s.rows[('session', 's%d' % i)] = {'kind': 'session', 'key': 's%d' % i, 'payload': seance(i, '2026-11-0%d' % i, 30 + i), 'deleted': False, 'updated_at': iso(T0 - 48 * H + i)}
    return s

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    erreurs = []

    # ---- 1. Navigateur vidé (ou nouveau téléphone), puis connexion : le profil du compte survit-il ? ----
    srv = base_serveur()
    ctx, p = appareil(br, srv, T0, etat=None, connecte=False, erreurs=erreurs)
    p.evaluate("app.setAuthF('email','test@exemple.fr');app.setAuthF('password','x');app.signIn()"); avance(p, 4000)
    e = etat(p); distant = srv.rows[('profile', 'me')]['payload']
    verdict('1. Données du navigateur effacées puis connexion : le profil du compte est conservé',
            e['goal'] == PROFIL['goalDate'] and distant.get('goalDate') == PROFIL['goalDate'],
            'local : objectif %s, %d séances ; serveur : objectif %s (attendu %s)' % (e['goal'], len(e['ses']), distant.get('goalDate'), PROFIL['goalDate']))
    ctx.close()

    # ---- 2. Deux appareils : une modification faite hors ligne plus tôt arrive-t-elle sur l'autre ? ----
    srv = base_serveur(); plein = {'v': 2, 'profile': PROFIL, 'daily': {}, 'sessions': [seance(i, '2026-11-0%d' % i, 30 + i) for i in range(1, 6)], 'plan': []}
    cA, A = appareil(br, srv, T0, etat=plein, erreurs=erreurs); cB, B = appareil(br, srv, T0, etat=plein, erreurs=erreurs)
    synchro(A); synchro(B)
    cB.reseau['coupe'] = True; srv.horloge = iso(T0 + 1 * H)
    modifie(B, "S=>S.sessions.push({id:'sB',date:'2026-11-10',type:'ef',dur:41,rpe:3})", T0 + 1 * H)          # B hors ligne à 9 h
    srv.horloge = iso(T0 + 2 * H)
    modifie(A, "S=>S.sessions.push({id:'sA',date:'2026-11-10',type:'ef',dur:42,rpe:3})", T0 + 2 * H); synchro(A)   # A en ligne à 10 h
    if os.environ.get('DETAIL'): print('   B hors ligne :', etat(B)['ses'], 'en attente', etat(B)['att'], '| A :', etat(A)['ses'])
    cB.reseau['coupe'] = False; heure(B, T0 + 3 * H); srv.horloge = iso(T0 + 3 * H); synchro(B)                                 # B retrouve le réseau à 11 h
    if os.environ.get('DETAIL'): print('   B après synchro :', etat(B)['ses'], 'en attente', etat(B)['att'], B.evaluate("document.querySelector('#syncline')?document.querySelector('#syncline').textContent:'(pas de ligne)'"), B.evaluate('navigator.onLine'))
    heure(A, T0 + 4 * H); synchro(A); synchro(A)
    a, b = etat(A), etat(B)
    if os.environ.get('DETAIL'): print('   journal serveur :', [(k, u[11:19]) for (_, k, d, u) in srv.journal], '| lastPull A', a['lastPull'], '| lastPull B', b['lastPull'])
    verdict('2. Séance saisie hors ligne sur B (9 h), synchronisée après une saisie de A (10 h) : A la reçoit',
            any(x.startswith('sB') for x in a['ses']),
            'A voit %d séances (%s) ; B voit %d séances ; serveur : %d lignes' % (len(a['ses']), 'sB présente' if any(x.startswith('sB') for x in a['ses']) else 'sB ABSENTE', len(b['ses']), len(srv.rows)))
    cA.close(); cB.close()

    # ---- 2b. Même chose, mais l'horloge de B retarde de 3 h ----
    srv = base_serveur()
    cA, A = appareil(br, srv, T0, etat=plein, erreurs=erreurs); cB, B = appareil(br, srv, T0 - 3 * H, etat=plein, erreurs=erreurs)
    synchro(A); synchro(B)
    srv.horloge = iso(T0 + 2 * H); modifie(A, "S=>S.sessions.push({id:'sA',date:'2026-11-10',type:'ef',dur:42,rpe:3})", T0 + 2 * H); synchro(A)   # A à 10 h, en ligne
    srv.horloge = iso(T0 + 3 * H); modifie(B, "S=>S.sessions.push({id:'sB',date:'2026-11-10',type:'ef',dur:41,rpe:3})", T0 + 3 * H - 3 * H); synchro(B)   # B à 11 h réelles, sa montre dit 8 h
    heure(A, T0 + 4 * H); synchro(A); synchro(A)
    a = etat(A)
    verdict('2b. Horloge de B en retard de 3 h : A reçoit quand même la séance de B',
            any(x.startswith('sB') for x in a['ses']), 'A voit %d séances (%s)' % (len(a['ses']), 'sB présente' if any(x.startswith('sB') for x in a['ses']) else 'sB ABSENTE, sans message'))
    cA.close(); cB.close()

    # ---- 3. Profil : deux appareils modifient deux réglages différents ----
    srv = base_serveur()
    cA, A = appareil(br, srv, T0, etat=plein, erreurs=erreurs); cB, B = appareil(br, srv, T0, etat=plein, erreurs=erreurs)
    synchro(A); synchro(B)
    cA.reseau['coupe'] = True
    modifie(A, "S=>{S.profile.manques=Object.assign({},S.profile.manques,{'2026-11-04':'fatigue'})}", T0 + 1 * H)   # A : raison d'un manque, hors ligne
    srv.horloge = iso(T0 + 2 * H)
    modifie(B, "S=>{S.profile.name='Nouveau prénom'}", T0 + 2 * H); synchro(B)                                      # B : autre réglage, en ligne
    cA.reseau['coupe'] = False; heure(A, T0 + 3 * H); srv.horloge = iso(T0 + 3 * H); synchro(A); synchro(B); synchro(A)
    a = etat(A); d = srv.rows[('profile', 'me')]['payload']
    verdict('3. Profil modifié sur deux appareils (réglages différents) : les deux changements survivent',
            '2026-11-04' in a['manques'] and a['nom'] == 'Nouveau prénom',
            'A après synchro : prénom « %s », manques %s ; serveur : prénom « %s », manques %s' % (a['nom'], a['manques'], d.get('name'), list((d.get('manques') or {}).keys())))
    cA.close(); cB.close()

    # ---- 4. Restauration d'une sauvegarde JSON ancienne : que deviennent les séances plus récentes du compte ? ----
    srv = base_serveur(); cA, A = appareil(br, srv, T0, etat=plein, erreurs=erreurs); synchro(A)
    vieux = {'v': 2, 'profile': PROFIL, 'daily': {}, 'sessions': plein['sessions'][:2], 'plan': []}
    A.evaluate("(o)=>{const t=document.createElement('textarea');t.id='jin';t.value=JSON.stringify(o);document.querySelectorAll('#jin').forEach(x=>x.remove());document.body.appendChild(t);app.importJSON();}", vieux)   # la vraie fonction de restauration
    avance(A, 4000); synchro(A)
    suppr = [k for k, r in srv.rows.items() if r['deleted']]
    verdict('4. Restaurer une sauvegarde de 2 séances sur un compte de 5 : les 3 autres restent sur le serveur',
            len(suppr) == 0, '%d séances marquées supprimées sur le serveur, contenu effacé : %s' % (len(suppr), all(srv.rows[k]['payload'] is None for k in suppr)))
    cA.close()

    br.close()

print('\n%d scénario(s) sur %d conformes à l\'attendu%s' % (sum(1 for r in RES if r[1]), len(RES), ' — serveur horodateur' if SERVEUR_HORODATE else ' — horodatage du téléphone conservé (hypothèse)'))
if erreurs: print('erreurs JavaScript :', erreurs[:3])
