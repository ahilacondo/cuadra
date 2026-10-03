"""Mide el tamaño real (px CSS) de los elementos interactivos en un viewport de 390 px."""
import json
from playwright.sync_api import sync_playwright
BASE='http://localhost:8123'
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},locale='es-PE'); pg=ctx.new_page()
    pg.goto(BASE); pg.wait_for_timeout(1000)
    def grab(screen, sel, label):
        for i,h in enumerate(pg.locator(sel).element_handles()):
            bb=h.bounding_box()
            if bb and bb['width']>0: out.append((screen,label,round(bb['width']),round(bb['height'])))
            break
    grab('Inicio','[data-testid=btn-new-group]','Botón principal')
    grab('Inicio','[data-testid=btn-demo]','Botón secundario')
    pg.locator('[data-testid=btn-demo]').click(); pg.wait_for_timeout(700)
    grab('Grupo','[data-testid=btn-back]','Botón volver')
    grab('Grupo','[data-testid=seg-gastos]','Pestaña segmentada')
    grab('Grupo','[data-testid=btn-add-expense]','Botón «Añadir gasto»')
    grab('Grupo','[data-testid^=expense-]','Fila de gasto')
    pg.locator('[data-testid=btn-add-expense]').click(); pg.wait_for_timeout(500)
    grab('Formulario','[data-testid^=cat-]','Chip de categoría')
    grab('Formulario','[data-testid^=paid-]','Chip de pagador')
    grab('Formulario','[data-testid^=part-]','Fila de participante')
    grab('Formulario','[data-testid=seg-equal]','Modo de reparto')
    grab('Formulario','[data-testid=btn-save-expense]','Botón guardar')
    b.close()
json.dump(out,open('/home/claude/lab4/data/targets.json','w'),ensure_ascii=False)
for o in out: print(o)
open('/home/claude/lab4/report/tables/targets.tex','w').write('\n'.join(f"{s} & {l} & {w}$\\times${h} & {'Sí' if h>=40 else 'No'} \\\\" for s,l,w,h in out))
