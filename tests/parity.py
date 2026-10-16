import sys, json, subprocess, datetime as dt
sys.path.insert(0, '..')   # dossier contenant sim8.py et sim3.py
import sim8 as S
S.v1(True)
def sim_run(N, n, vol0, sec=None, graine=0):
    p = ("parite", 50.0, vol0, 0.0, 50.0, n, "8-20h")   # coureur parfait : tolerance enorme
    sc = dict(N=N, bruit=0.0, tranche="8-20h")
    if sec: sc["secondaire"] = sec
    J, cal = S.prepare(p, "apres", graine, scen=sc)
    out = []
    for s in J[1:]:
        ses = s["seances"]
        sl = [d for j, d, t in ses if t in ("longue", "cle")]
        aut = sorted(d for j, d, t in ses if t == "autre")
        out.append(dict(w=s["sem"], type=s["type"], V=round(s["V"], 4), sl=sl[0] if sl else 0, aut=aut, cle=bool(s.get("cle"))))
    return out
def js_run(N, n, vol0, sec=None):
    start = dt.date(2026, 9, 28)
    offs = {1: [], 2: [3], 3: [1, 3], 4: [1, 3, 4], 5: [0, 1, 3, 4], 6: [0, 1, 2, 3, 4]}[n]   # JOURS[n-1]
    run = [((o + 1) % 7) for o in offs] + [0]
    goal = start + dt.timedelta(days=(N - 1) * 7 + 5)
    prof = dict(goalDate=str(goal), goalDist=80, goalDplus=4500, days=dict(run=run, long=0, cf=[], time={}),
                start=dict(freq4w=n, dur4w=vol0 * 60 / n, pastRaces=[dict(date='2025-09-01', dist=50, dplus=2000, dur=390)], lastLong={}),
                modules=dict(strength=False), races=[], planStart=str(start), terrain={})
    if sec:
        d = start + dt.timedelta(days=(sec[0] - 1) * 7 + 5)
        prof["races"] = [dict(name="50k", date=str(d), dist=50, dplus=2000, prio="B" if sec[2] == "objectif" else "C")]
    inp = dict(profile=prof, today=str(start - dt.timedelta(days=1)), sessions=[], regles='v1')   # socle v1 prouvé contre sim8
    js = r"""const E=require('./engine.js');const inp=JSON.parse(process.argv[1]);
inp.isRun=s=>['ef','long','qual','desc'].includes(s.type);const o=E.build(inp);
const ses=o.sessions;const res=o.weeks.map(k=>{const d0=k.mon;const inW=ses.filter(s=>s.date>=d0&&s.date<new Date(new Date(d0).getTime()+7*864e5).toISOString().slice(0,10));
 const sl=inW.filter(s=>s.type==='long').map(s=>s.dur);const aut=inW.filter(s=>s.type==='ef'||s.type==='qual').map(s=>s.dur).sort((a,b)=>a-b);
 return {w:k.w,type:k.type,V:Math.round(k.V*1e4)/1e4,sl:sl[0]||0,aut,cle:!!k.cle};});
console.log(JSON.stringify({res,garde:o.garde,info:{N:o.info.N,tr:o.info.trName}}));"""
    r = subprocess.run(["node", "-e", js, json.dumps(inp)], capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    return json.loads(r.stdout)
cases = [(52, 4, 2.0, None), (52, 4, 2.0, (32, 390.0, "objectif")), (40, 5, 3.5, None), (52, 3, 0.0, None), (36, 4, 1.0, (20, 390.0, "entrainement"))]
tot = 0
for N, n, v, sec in cases:
    a = sim_run(N, n, v, sec); b = js_run(N, n, v, sec)
    bad = [(x, y) for x, y in zip(a, b["res"]) if x["type"] != y["type"] or abs(x["V"] - y["V"]) > 1e-3 or x["sl"] != y["sl"] or x["aut"] != y["aut"] or x["cle"] != y["cle"]]
    tot += len(bad)
    print(f"N={N} n={n} vol0={v} sec={sec}: {len(a)} sem., écarts {len(bad)}  tranche JS {b['info']['tr']}")
    for x, y in bad[:4]: print("   sim", x, "\n   js ", y)
print("TOTAL ECARTS", tot)
