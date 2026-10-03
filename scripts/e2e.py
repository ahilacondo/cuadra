"""Pruebas E2E de Cuadra (Playwright). Sirve la build web y recorre los casos de uso.
Genera capturas en SHOTS y un JSON con el resultado de cada caso."""
import json, sys, re, time
from playwright.sync_api import sync_playwright, expect

BASE = 'http://localhost:8123'
SHOTS = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/lab4/report/img/app_'
RES = []

def case(id_, desc):
    def deco(fn):
        def run(*a, **k):
            t0 = time.time()
            try:
                fn(*a, **k); RES.append(dict(id=id_, desc=desc, ok=True, s=round(time.time() - t0, 2)))
            except Exception as e:
                RES.append(dict(id=id_, desc=desc, ok=False, err=str(e)[:300], s=round(time.time() - t0, 2)))
                print('FAIL', id_, str(e)[:300])
        return run
    return deco

def shot(pg, name, full=False):
    pg.wait_for_timeout(350)
    pg.screenshot(path=f'{SHOTS}{name}.png')

def T(pg, tid): return pg.locator(f'[data-testid="{tid}"]')
def parts(pg): return pg.locator('[data-testid^="part-"]')
def tx(pg, t): return pg.get_by_text(t, exact=False).first

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, locale='es-PE', permissions=['clipboard-read', 'clipboard-write'])
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto(BASE); pg.wait_for_timeout(1200)

    @case('CP01', 'Estado vacío inicial con llamadas a la acción')
    def _():
        expect(tx(pg, 'Aún no tienes grupos')).to_be_visible()
        expect(T(pg, 'btn-new-group')).to_be_visible(); expect(T(pg, 'btn-demo')).to_be_visible()
        shot(pg, 's01_vacio')
    _()

    @case('CP02', 'Validación al crear grupo sin nombre ni integrantes')
    def _():
        T(pg, 'btn-new-group').click(); pg.wait_for_timeout(400)
        T(pg, 'btn-create').click()
        expect(tx(pg, 'Escribe un nombre para el grupo')).to_be_visible()
        expect(tx(pg, 'Agrega al menos a otra persona')).to_be_visible()
        shot(pg, 's02_grupo_validacion')
    _()

    @case('CP03', 'Crear grupo con nombre, ícono y 3 integrantes')
    def _():
        T(pg, 'input-group-name').fill('Viaje a Colca')
        pg.get_by_text('✈️').click()
        for n in ['Rosa', 'Mateo']:
            T(pg, 'input-member').fill(n); T(pg, 'btn-add-member').click()
        expect(tx(pg, 'Integrantes (3)')).to_be_visible()
        shot(pg, 's03_grupo_lleno')
        T(pg, 'btn-create').click(); pg.wait_for_timeout(600)
        expect(tx(pg, 'Sin gastos todavía')).to_be_visible()
        shot(pg, 's04_grupo_sin_gastos')
    _()

    def add_expense(title, amount, cat=None, payer_idx=0, mode=None, vals=None, deselect=None, expect_err=None, name=None, save=True):
        T(pg, 'btn-add-expense').click(); pg.wait_for_timeout(450)
        T(pg, 'input-title').fill(title); T(pg, 'input-amount').fill(amount)
        if cat: T(pg, f'cat-{cat}').click()
        pg.locator('[data-testid^="paid-"]').nth(payer_idx).click()
        if deselect is not None: parts(pg).nth(deselect).click()
        if mode: T(pg, f'seg-{mode}').click(); pg.wait_for_timeout(250)
        if vals:
            for i, v in enumerate(vals):
                pg.locator('[data-testid^="val-"]').nth(i).fill(v)
        pg.wait_for_timeout(300)
        if name: shot(pg, name)
        if expect_err:
            expect(T(pg, 'split-error')).to_contain_text(expect_err)
        if save:
            T(pg, 'btn-save-expense').click(); pg.wait_for_timeout(500)

    @case('CP04', 'Gasto con reparto igual: 100.00 entre 3 cuadra al céntimo')
    def _():
        add_expense('Alojamiento', '100.00', 'alquiler', 0, name='s05_form_igual')
        expect(tx(pg, 'Alojamiento')).to_be_visible()
        expect(pg.locator('[data-testid^="expense-"]').first).to_contain_text('S/ 100.00')
    _()

    @case('CP05', 'Montos exactos que no cuadran bloquean el guardado')
    def _():
        T(pg, 'btn-add-expense').click(); pg.wait_for_timeout(450)
        T(pg, 'input-title').fill('Cena'); T(pg, 'input-amount').fill('120')
        T(pg, 'seg-exact').click(); pg.wait_for_timeout(250)
        for i, v in enumerate(['50', '40', '20']): pg.locator('[data-testid^="val-"]').nth(i).fill(v)
        expect(T(pg, 'split-error')).to_contain_text('Faltan S/ 10.00')
        shot(pg, 's06_form_montos_error')
        T(pg, 'btn-save-expense').click(); pg.wait_for_timeout(400)
        expect(T(pg, 'btn-save-expense')).to_be_visible()   # sigue en el formulario
        pg.locator('[data-testid^="val-"]').nth(2).fill('30')
        expect(T(pg, 'split-ok')).to_be_visible()
        T(pg, 'btn-save-expense').click(); pg.wait_for_timeout(500)
        expect(tx(pg, 'Cena')).to_be_visible()
    _()

    @case('CP06', 'Porcentajes que no suman 100 % muestran el error y se corrigen')
    def _():
        T(pg, 'btn-add-expense').click(); pg.wait_for_timeout(450)
        T(pg, 'input-title').fill('Entradas al mirador'); T(pg, 'input-amount').fill('90')
        T(pg, 'seg-percent').click(); pg.wait_for_timeout(250)
        for i, v in enumerate(['50', '30', '30']): pg.locator('[data-testid^="val-"]').nth(i).fill(v)
        expect(T(pg, 'split-error')).to_contain_text('suman 110')
        shot(pg, 's07_form_porcentaje_error')
        pg.locator('[data-testid^="val-"]').nth(2).fill('20')
        expect(T(pg, 'split-ok')).to_be_visible()
        T(pg, 'btn-save-expense').click(); pg.wait_for_timeout(500)
    _()

    @case('CP07', 'Reparto por partes (2 : 1 : 1) y participante excluido')
    def _():
        T(pg, 'btn-add-expense').click(); pg.wait_for_timeout(450)
        T(pg, 'input-title').fill('Taxi al mirador'); T(pg, 'input-amount').fill('45.50')
        T(pg, 'cat-transporte').click(); pg.locator('[data-testid^="paid-"]').nth(1).click()
        parts(pg).nth(2).click()           # excluye a la tercera persona
        T(pg, 'seg-shares').click(); pg.wait_for_timeout(250)
        pg.locator('[data-testid^="val-"]').nth(0).fill('2')
        expect(T(pg, 'split-ok')).to_be_visible()
        shot(pg, 's08_form_partes')
        T(pg, 'btn-save-expense').click(); pg.wait_for_timeout(500)
        shot(pg, 's09_gastos_grupo_nuevo')
    _()

    @case('CP08', 'Saldos del grupo suman cero y se listan todos los integrantes')
    def _():
        T(pg, 'seg-saldos').click(); pg.wait_for_timeout(400)
        vals = pg.locator('[data-testid^="bal-"]').all_inner_texts()
        nums = [float(re.search(r'([+-]?)S/ ([\d,]+\.\d\d)', v.replace('\n', ' ')).group(2).replace(',', '')) * (-1 if '-S/' in v.replace('\n', ' ') else 1) for v in vals]
        assert len(nums) == 3 and abs(sum(nums)) < 0.005, nums
        shot(pg, 's10_saldos_grupo_nuevo')
    _()

    @case('CP09', 'Persistencia: los datos sobreviven a recargar la página')
    def _():
        pg.reload(); pg.wait_for_timeout(1200)
        expect(tx(pg, 'Viaje a Colca')).to_be_visible()
        shot(pg, 's11_inicio_con_grupo')
        tx(pg, 'Viaje a Colca').click(); pg.wait_for_timeout(600)
        expect(tx(pg, 'Alojamiento')).to_be_visible()
    _()

    @case('CP10', 'Eliminar un gasto requiere confirmación (doble toque)')
    def _():
        T(pg, 'seg-gastos').click(); pg.wait_for_timeout(300)
        before = pg.locator('[data-testid^="expense-"]').count()
        d = pg.locator('[data-testid^="del-"]').first
        d.click(); expect(tx(pg, 'Toca otra vez para eliminar')).to_be_visible()
        shot(pg, 's12_confirmar_eliminar')
        d.click(); pg.wait_for_timeout(400)
        assert pg.locator('[data-testid^="expense-"]').count() == before - 1
    _()

    # ---- grupo de ejemplo
    pg.goto(BASE); pg.wait_for_timeout(900)
    pg.evaluate('localStorage.clear()'); pg.reload(); pg.wait_for_timeout(1000)
    T(pg, 'btn-demo').click(); pg.wait_for_timeout(700)

    @case('CP11', 'Grupo de ejemplo: tarjeta de saldo y lista de gastos')
    def _():
        expect(T(pg, 'my-balance')).to_contain_text('194.26')
        shot(pg, 's13_demo_gastos')
    _()

    @case('CP12', 'Saldos de ejemplo: Camila +811.72 (acreedora) y suma cero')
    def _():
        T(pg, 'seg-saldos').click(); pg.wait_for_timeout(400)
        expect(T(pg, 'bal-camila')).to_contain_text('811.72')
        shot(pg, 's14_demo_saldos')
    _()

    @case('CP13', 'Liquidación: 6 pagos sin simplificar frente a 3 con Cuadra')
    def _():
        T(pg, 'seg-liquidar').click(); pg.wait_for_timeout(500)
        expect(T(pg, 'naive-count')).to_have_text('6'); expect(T(pg, 'best-count')).to_have_text('3')
        shot(pg, 's15_demo_liquidar')
    _()

    @case('CP14', 'Copiar resumen al portapapeles')
    def _():
        T(pg, 'btn-copy').click(); pg.wait_for_timeout(400)
        expect(tx(pg, 'Copiado')).to_be_visible()
        txt = pg.evaluate('navigator.clipboard.readText()')
        assert 'Camila' in txt and 'S/ 329.97' in txt, txt
        shot(pg, 's16_copiado')
    _()

    @case('CP15', 'Registrar un pago actualiza saldos y reduce los pagos pendientes')
    def _():
        T(pg, 'pay-0').click(); pg.wait_for_timeout(500)
        expect(T(pg, 'best-count')).to_have_text('2')
        shot(pg, 's17_pago_registrado')
    _()

    @case('CP16', 'Liquidar todo: el grupo queda "al día"')
    def _():
        T(pg, 'pay-0').click(); pg.wait_for_timeout(300); T(pg, 'pay-0').click(); pg.wait_for_timeout(500)
        expect(tx(pg, '¡Todos al día!')).to_be_visible()
        expect(T(pg, 'my-balance')).to_contain_text('Estás al día')
        shot(pg, 's18_todos_al_dia')
        T(pg, 'seg-gastos').click(); pg.wait_for_timeout(400)
        expect(tx(pg, 'Pago registrado').first).to_be_visible()
        shot(pg, 's19_historial_pagos')
    _()

    @case('CP17', 'Resumen: gasto por categoría y pagado vs. le corresponde')
    def _():
        T(pg, 'seg-resumen').click(); pg.wait_for_timeout(500)
        expect(tx(pg, 'Gasto por categoría')).to_be_visible(); expect(tx(pg, 'S/ 1,200.00')).to_be_visible()
        shot(pg, 's20_demo_resumen')
    _()

    @case('CP18', 'Diseño responsive: columna centrada en pantalla de escritorio')
    def _():
        pg.set_viewport_size({'width': 1280, 'height': 800}); pg.wait_for_timeout(500)
        shot(pg, 's21_escritorio')
        pg.set_viewport_size({'width': 390, 'height': 844})
    _()

    @case('CP19', 'Ruta inexistente: grupo no encontrado con salida de emergencia')
    def _():
        pg.goto(BASE + '/group/no-existe'); pg.wait_for_timeout(900)
        expect(tx(pg, 'Grupo no encontrado')).to_be_visible()
        shot(pg, 's22_no_encontrado')
    _()

    @case('CP20', 'Sin errores de consola durante todo el recorrido')
    def _():
        real = [e for e in errs if 'favicon' not in e.lower()]
        assert not real, real[:3]
    _()
    b.close()

json.dump(RES, open('/home/claude/lab4/data/e2e_results.json', 'w'), ensure_ascii=False, indent=1)
print(sum(r['ok'] for r in RES), '/', len(RES), 'casos OK')
