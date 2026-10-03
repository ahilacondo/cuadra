import sys
from playwright.sync_api import sync_playwright
BASE='http://localhost:8123'
OUT='/home/claude/lab4/shots/'
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,locale='es-PE')
    pg=ctx.new_page()
    errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(BASE); pg.wait_for_timeout(1500)
    pg.screenshot(path=OUT+'x01_home_vacio.png')
    pg.click('[data-testid=btn-demo]'); pg.wait_for_timeout(800)
    pg.screenshot(path=OUT+'x02_gastos.png')
    for t in ['saldos','liquidar','resumen']:
        pg.click(f'[data-testid=seg-{t}]'); pg.wait_for_timeout(400)
        pg.screenshot(path=OUT+f'x03_{t}.png',full_page=True)
    pg.click('[data-testid=seg-gastos]'); pg.click('[data-testid=btn-add-expense]'); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+'x04_form.png',full_page=True)
    print('errors:',errs)
    b.close()
