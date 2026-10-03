import os, pathlib
from playwright.sync_api import sync_playwright
IMG = '/home/claude/lab4/report/img/'
TMP = '/home/claude/lab4/figs/html/'
os.makedirs(TMP, exist_ok=True)
BASE = '''
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Inter","DejaVu Sans",sans-serif;color:#1D2B26;display:inline-block;padding:0}
#cap{display:inline-block;padding:__PAD__px}
.mono{font-family:"DejaVu Sans Mono","Menlo",monospace}
'''
def shot(name, body, css='', pad=16, scale=2, width=None):
    html = f'<!doctype html><meta charset="utf-8"><style>{BASE.replace("__PAD__",str(pad))}{css}</style><body><div id="cap"{" style=width:%dpx"%width if width else ""}>{body}</div>'
    p = TMP + name + '.html'
    pathlib.Path(p).write_text(html, encoding='utf-8')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(device_scale_factor=scale, viewport={'width': 1800, 'height': 1200})
        pg.goto('file://' + p)
        pg.wait_for_timeout(250)
        pg.locator('#cap').screenshot(path=IMG + name + '.png')
        b.close()
    print('ok', name)
