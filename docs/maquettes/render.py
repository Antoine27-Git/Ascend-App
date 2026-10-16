import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from playwright.sync_api import sync_playwright

def render(items, dpr=1.5):
    """items: list of (name, html)"""
    out = os.path.join(HERE, 'png'); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 420, 'height': 900}, device_scale_factor=dpr)
        for name, html in items:
            f = os.path.join(HERE, 'html', name + '.html'); os.makedirs(os.path.dirname(f), exist_ok=True)
            open(f, 'w', encoding='utf-8').write(html)
            pg.goto('file://' + f); pg.wait_for_timeout(150)
            pg.locator('.canvas').screenshot(path=os.path.join(out, name + '.png'))
            print('ok', name)
        b.close()

if __name__ == '__main__':
    mods = sys.argv[1:]
    items = []
    for m in mods:
        mod = importlib.import_module(m)
        for k in mod.EXPORT:
            items.append((k, getattr(mod, k)() if callable(getattr(mod, k)) else getattr(mod, k)))
    render(items)
