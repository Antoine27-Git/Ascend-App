import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = json.load(open(os.path.join(HERE, 'icons.json')))

def ic(k, cls=''):
    return '<svg viewBox="0 -960 960 960" class="mi %s" aria-hidden="true">%s</svg>' % (cls, ICONS.get(k, ''))

CSS = r"""
:root{--bg:#f6f7f4;--card:#fff;--ink:#0f1c16;--mut:#5b6961;--line:#e9eee9;--chip:#eef2ee;--mint:#25c37e;--mintT:#087a49;--mintBg:#e4f6ec;
--accent:#ecd08f;--accentInk:#4a3610;--deep:#10251c;--ember:#d1601a;--emberBg:#ffeedd;--violet:#6a4fd0;--violetBg:#ece7fe;--sky:#2c6fb8;--skyBg:#e0edfd;
--sunBg:#fff1d9;--sunT:#8a5a0a;--coralT:#b8352d;--coralBg:#fde9e7;--nut:#c4487f;--nutBg:#ffe4ef;--nav:rgba(255,255,255,.97);
--shadow:0 1px 2px rgba(15,28,22,.04),0 10px 26px rgba(15,28,22,.06);--frame:#dfe4df}
[data-theme=dark]{--bg:#0f1513;--card:#19211d;--ink:#e6eee9;--mut:#9eaea5;--line:#27312c;--chip:#232d28;--mint:#3ddc92;--mintT:#5fe0a3;--mintBg:#1a3328;
--accent:#e3c47a;--accentInk:#2c2007;--deep:#0b1a14;--ember:#ff9a66;--emberBg:#3a2618;--violet:#b8a6ff;--violetBg:#2a2444;--sky:#8cc2ff;--skyBg:#1b2b40;
--sunBg:#3a2f14;--sunT:#f3c46a;--coralT:#ff8a80;--coralBg:#3b1f1d;--nut:#ff8fc0;--nutBg:#3b1f2d;--nav:rgba(30,39,35,.97);--shadow:0 0 0 1px #222c27;--frame:#2a2f2c}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#ffffff;font:15px/1.4 Inter,Roboto,"Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased;color:var(--ink)}
.canvas{padding:14px 12px 16px;background:var(--canvas,#ffffff);display:inline-block}
.tag{font:700 13px/1 Inter,Roboto,sans-serif;color:#33413a;margin:0 4px 10px;display:flex;gap:8px;align-items:center}
.tag b{background:#10251c;color:#fff;border-radius:7px;padding:4px 8px}
.tag .reco{background:#e4f6ec;color:#087a49;border-radius:7px;padding:4px 8px}
.phone{width:360px;height:760px;background:var(--bg);border-radius:30px;overflow:hidden;position:relative;box-shadow:0 0 0 1px var(--frame),0 12px 30px rgba(0,0,0,.10)}
.scroll{position:absolute;inset:0;overflow:hidden;padding-bottom:96px}
.halo{position:absolute;inset:0 0 auto;height:230px;overflow:hidden;pointer-events:none}
.halo i{position:absolute;border-radius:50%;filter:blur(48px);opacity:.45}
.halo .a{width:240px;height:180px;background:#b9f5d6;left:-60px;top:-70px}.halo .b{width:220px;height:170px;background:#ffe0b8;right:-60px;top:-50px}
[data-theme=dark] .halo{display:none}
header{position:relative;padding:18px 20px 4px;display:flex;justify-content:space-between;align-items:flex-start}
header h1{font-size:23px;font-weight:800;letter-spacing:-.03em;margin:0;line-height:1.1}
header .sub{font-size:13px;color:var(--mut);margin-top:4px}
.logo{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#0f3d2e,#1d6b4f);display:flex;align-items:center;justify-content:center;flex:none}
.logo svg{width:22px;height:22px;fill:#e9c46a}
.mi{width:24px;height:24px;fill:currentColor;flex:none}
.card{background:var(--card);border-radius:22px;padding:16px;margin:10px 14px;box-shadow:var(--shadow);position:relative}
.k{font-size:11.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mintT)}
.ic{width:48px;height:48px;border-radius:15px;display:flex;align-items:center;justify-content:center;flex:none}
.ic .mi{width:26px;height:26px}
.ic.ef{background:var(--mintBg);color:var(--mintT)}.ic.sl{background:var(--emberBg);color:var(--ember)}.ic.cf{background:var(--violetBg);color:var(--violet)}.ic.nut{background:var(--nutBg);color:var(--nut)}
.row{display:flex;align-items:center;gap:12px}
.ttl{font-size:21px;font-weight:800;letter-spacing:-.025em;line-height:1.1}
.meta{font-size:13.5px;color:var(--mut);margin-top:3px}
.eff{margin-top:12px;background:var(--chip);border-radius:14px;padding:10px 12px;font-size:14px;line-height:1.4}
.eff b{font-weight:700}
.why{margin-top:12px;font-size:13.5px;line-height:1.4;color:var(--ink)}
.why span{color:var(--mut);font-weight:700}
.btn{display:flex;align-items:center;justify-content:center;gap:8px;height:52px;border-radius:16px;font-weight:700;font-size:16px;border:0;width:100%}
.btn.pri{background:var(--accent);color:var(--accentInk)}
.btn.sec{background:var(--chip);color:var(--ink);font-size:15px;height:48px}
.btn.ghost{background:transparent;color:var(--mut);font-size:14px;height:44px}
.links{display:flex;justify-content:space-between;margin-top:6px}
.links a{flex:1;text-align:center;font-size:14px;font-weight:700;color:var(--mut);padding:12px 0}
.links a+a{border-left:1px solid var(--line)}
nav{position:absolute;left:12px;right:12px;bottom:10px;height:66px;background:var(--nav);border-radius:24px;display:flex;padding:7px;box-shadow:0 12px 30px rgba(16,32,26,.16)}
[data-theme=dark] nav{box-shadow:0 0 0 1px #2b3530}
nav div{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:11.5px;font-weight:700;color:var(--mut);border-radius:18px}
nav div.on{background:var(--mintBg);color:var(--mintT)}
nav .mi{width:23px;height:23px}
.week{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:12px}
.day{display:flex;flex-direction:column;align-items:center;gap:5px;padding:7px 0 8px;border-radius:14px;font-size:11.5px;font-weight:700;color:var(--mut)}
.day .d{font-size:15px;color:var(--ink);font-weight:800}
.day .dot{width:30px;height:30px;border-radius:10px;display:flex;align-items:center;justify-content:center}
.day .dot .mi{width:18px;height:18px}
.day .dot.rest{background:transparent;color:var(--mut)}
.day.today{background:var(--mintBg);box-shadow:inset 0 0 0 1.5px var(--mintT)}
.dot.ef{background:var(--mintBg);color:var(--mintT)}.dot.sl{background:var(--emberBg);color:var(--ember)}.dot.cf{background:var(--violetBg);color:var(--violet)}
.dot.done{background:var(--mintT);color:#fff}
.h2{font-size:15.5px;font-weight:800;letter-spacing:-.01em}
.h2 small{font-weight:600;color:var(--mut);font-size:13px;margin-left:6px}
.sb{display:flex;justify-content:space-between;align-items:baseline}
.mut{color:var(--mut)}
.mini{font-size:12.5px;color:var(--mut);line-height:1.4}
.objline{display:flex;align-items:center;gap:12px;padding:12px 16px}
.chip{display:inline-flex;align-items:center;justify-content:center;border-radius:12px;background:var(--chip);font-weight:700;color:var(--ink)}
.pill{font-size:11.5px;font-weight:800;padding:4px 9px;border-radius:999px;white-space:nowrap}
.pill.ok{background:var(--mintBg);color:var(--mintT)}.pill.today{background:var(--sunBg);color:var(--sunT)}.pill.miss{background:var(--chip);color:var(--mut)}
.dim{position:absolute;inset:0;background:rgba(8,20,14,.42)}
.sheet{position:absolute;left:0;right:0;bottom:0;background:var(--bg);border-radius:26px 26px 0 0;overflow:hidden}
.grab{width:40px;height:5px;border-radius:3px;background:#c9d1cb;margin:8px auto 0}
.lbl{display:flex;justify-content:space-between;align-items:baseline;font-size:14.5px;font-weight:800;margin:16px 0 8px}
.lbl small{font-size:12px;color:var(--mut);font-weight:600}
.grid6{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}
.grid5{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.n{height:46px;border-radius:13px;background:var(--chip);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:var(--ink)}
.n.on{background:var(--mintBg);color:var(--mintT);box-shadow:inset 0 0 0 2px var(--mintT)}
.opt{border-radius:16px;background:var(--card);box-shadow:inset 0 0 0 1.5px var(--line);padding:12px 14px}
.opt.on{box-shadow:inset 0 0 0 2px var(--mintT);background:var(--mintBg)}
.opt b{display:block;font-size:15px}.opt span{font-size:13px;color:var(--mut)}
.field{background:var(--card);border-radius:13px;box-shadow:inset 0 0 0 1.5px #cfd8d2;height:46px;display:flex;align-items:center;padding:0 12px;font-size:16px}
[data-theme=dark] .field{box-shadow:inset 0 0 0 1.5px #34403a}
.field .ph{color:#9aa59f}
.f{font-size:12.5px;color:var(--mut);font-weight:700;margin:0 0 6px}
.foot{position:absolute;left:0;right:0;bottom:0;padding:10px 16px 16px;background:linear-gradient(transparent,var(--bg) 22%)}
.listrow{display:flex;align-items:center;gap:12px;padding:10px 0;border-top:1px solid var(--line)}
.listrow:first-child{border-top:0}
.listrow .dd{width:40px;text-align:center;flex:none}
.listrow .dd b{display:block;font-size:17px;font-weight:800;line-height:1}
.listrow .dd span{font-size:11.5px;color:var(--mut);font-weight:700}
.listrow .t{font-size:15px;font-weight:700}
.listrow .m{font-size:12.5px;color:var(--mut);margin-top:1px}
.listrow.today{background:var(--mintBg);margin:0 -10px;padding:10px;border-radius:14px;border-top-color:transparent}
.listrow.rest .t{color:var(--mut);font-weight:600}
.small-ic{width:34px;height:34px;border-radius:11px;display:flex;align-items:center;justify-content:center;flex:none}
.small-ic .mi{width:20px;height:20px}
.chev{color:var(--mut);font-size:20px;margin-left:auto}
.stat3{display:flex}
.stat3 div{flex:1;border-left:1px solid var(--line);padding-left:12px}
.stat3 div:first-child{border-left:0;padding-left:0}
.stat3 b{display:block;font-size:18px;font-weight:800;letter-spacing:-.02em}
.stat3 span{font-size:12px;color:var(--mut)}
.bars{display:flex;align-items:flex-end;gap:6px;height:84px;margin-top:12px;position:relative}
.bars i{flex:1;border-radius:6px;background:var(--chip);display:block}
.bars i.v{background:var(--mint)}
.bars i.cur{background:var(--mintT)}
.band{position:absolute;left:0;right:0;background:rgba(37,195,126,.12);border-top:1.5px dashed var(--mintT);border-bottom:1.5px dashed var(--mintT)}
.axis{display:flex;gap:6px;margin-top:5px}
.axis span{flex:1;text-align:center;font-size:10.5px;color:var(--mut)}
.seg{display:flex;background:var(--chip);border-radius:13px;padding:3px}
.seg div{flex:1;text-align:center;font-size:13.5px;font-weight:700;color:var(--mut);padding:8px 0;border-radius:10px}
.seg div.on{background:var(--card);color:var(--ink);box-shadow:0 1px 3px rgba(0,0,0,.08)}
"""

def page(inner, theme='light', tag=None, reco=False, w=360, h=760):
    t = ''
    if tag:
        t = '<div class="tag"><b>%s</b>%s%s</div>' % (tag[0], tag[1], '<span class="reco">recommandée</span>' if reco else '')
    return '<!doctype html><html data-theme="%s"><head><meta charset="utf-8"><style>%s</style></head><body><div class="canvas">%s<div class="phone" style="width:%dpx;height:%dpx">%s</div></div></body></html>' % (theme, CSS, t, w, h, inner)

def nav(items, on):
    icons = {'Aujourd\'hui': 'home', 'Accueil': 'home', 'Jour': 'calendar', 'Semaine': 'calendar', 'Séances': 'run', 'Plan': 'calendar', 'Suivi': 'monitoring', 'Profil': 'person'}
    return '<nav>' + ''.join('<div class="%s">%s%s</div>' % ('on' if x == on else '', ic(icons[x]), x) for x in items) + '</nav>'

def header(title, sub, logo=True):
    return '<header><div><h1>%s</h1><div class="sub">%s</div></div>%s</header>' % (title, sub, '<div class="logo">%s</div>' % ic('terrain') if logo else '')
