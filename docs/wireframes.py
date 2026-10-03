from playwright.sync_api import sync_playwright
OUT = '/home/claude/lab4/report/img/'
CSS = '''
*{box-sizing:border-box;margin:0;padding:0;font-family:"Inter","DejaVu Sans",sans-serif}
body{background:#fff;width:390px;height:844px;position:relative;color:#444;overflow:hidden}
.phone{position:absolute;inset:0;background:#F6F6F4;padding:22px 16px}
.bar{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.back{width:36px;height:36px;border:2px solid #999;border-radius:50%;position:relative}
.t{flex:1}.t b{display:block;height:20px;width:60%;background:#BDBDBD;border-radius:4px}
.t i{display:block;height:9px;width:38%;background:#D5D5D5;border-radius:3px;margin-top:6px}
.box{border:2px solid #9a9a9a;border-radius:12px;background:#fff;padding:12px;position:relative}
.ln{height:9px;background:#D5D5D5;border-radius:3px;margin:6px 0;position:relative}
.ln.s{width:55%}.ln.m{width:75%}.ln.b{height:13px;background:#B5B5B5}
.btn{border:2px solid #666;background:#CFCFCF;border-radius:30px;height:46px;display:flex;align-items:center;justify-content:center;font-weight:700;color:#444;font-size:14px;position:relative}
.btn.o{background:#fff}
.row{display:flex;align-items:center;gap:10px}
.ic{width:38px;height:38px;border:2px solid #9a9a9a;border-radius:10px;background:#EEE;flex:none}
.av{width:30px;height:30px;border-radius:50%;background:#BDBDBD;flex:none}
.seg{display:flex;border:2px solid #9a9a9a;border-radius:30px;font-size:12px;font-weight:700;position:relative}
.seg div{flex:1;text-align:center;padding:9px 0;color:#777;border-radius:30px}.seg .on{background:#CFCFCF;color:#333}
.chip{display:inline-block;border:2px solid #9a9a9a;border-radius:20px;padding:6px 12px;font-size:12px;margin:0 6px 6px 0;background:#fff}
.chip.on{background:#CFCFCF;border-color:#666}
.in{height:44px;border:2px solid #9a9a9a;border-radius:10px;background:#fff;margin-bottom:12px;display:flex;align-items:center;padding:0 12px;font-size:12px;color:#999;position:relative}
.lbl{font-size:11px;font-weight:700;color:#888;margin:2px 0 6px}
.bar2{height:9px;border-radius:5px;background:#E2E2E2;position:relative}.bar2 i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:#9a9a9a}
.cb{width:22px;height:22px;border:2px solid #777;border-radius:6px;flex:none}.cb.on{background:#999}
.foot{position:absolute;left:16px;right:16px;bottom:22px}
.x{font-size:11px;color:#999;white-space:nowrap}.amt{width:70px;height:12px;background:#B5B5B5;border-radius:3px}
.hero{background:#BDBDBD;border-radius:14px;padding:14px;height:96px;border:2px solid #888;position:relative}
.big{height:26px;width:55%;background:#8f8f8f;border-radius:5px;margin:8px 0}
.tile{flex:1;background:#E4E4E4;border-radius:12px;padding:12px;border:2px solid #aaa;position:relative}
.err{color:#b33;font-weight:700;font-size:12px;margin-top:8px;position:relative}
.rel{position:relative}
.pin{position:absolute;left:-9px;top:-11px;width:24px;height:24px;border-radius:50%;background:#E4572E;color:#fff;font-weight:800;font-size:12.5px;font-style:normal;display:flex;align-items:center;justify-content:center;border:2px solid #fff;z-index:9;box-shadow:0 1px 4px rgba(0,0,0,.3)}
'''
P = lambda n: f'<i class="pin">{n}</i>'
LAB = ['Gastos', 'Saldos', 'Liquidar', 'Resumen']
SPL = ['Igual', '%', 'Montos', 'Partes']


def seg(on, labels=LAB, n=None):
    return '<div class="seg">' + (P(n) if n else '') + ''.join(f'<div class="{"on" if i == on else ""}">{t}</div>' for i, t in enumerate(labels)) + '</div>'


def hero(n=None):
    return '<div class="hero">' + (P(n) if n else '') + '<div class="ln s"></div><div class="big"></div><div class="ln m"></div></div>'


def bar(back=True, n=None):
    return '<div class="bar">' + (f'<div class="back">{P(n) if n else ""}</div>' if back else '') + '<div class="t"><b></b><i></i></div></div>'


def field(lbl, ph, n=None, color=None):
    st = f' style="color:{color}"' if color else ''
    return f'<div class="lbl">{lbl}</div><div class="in"{st}>' + (P(n) if n else '') + ph + '</div>'


def exprow(n=None):
    return ('<div class="box row" style="margin-bottom:9px">' + (P(n) if n else '') +
            '<div class="ic"></div><div style="flex:1"><div class="ln b" style="width:70%"></div><div class="ln s"></div></div>'
            '<div style="width:64px"><div class="ln b"></div><div class="ln"></div></div></div>')


def member(on=True, val=None, amt=True, n=None):
    v = f'<div class="in" style="height:32px;width:64px;margin:0;font-size:11px">{val}</div>' if val is not None else ''
    return (f'<div class="row rel" style="margin-bottom:10px">{P(n) if n else ""}<div class="cb {"on" if on else ""}"></div><div class="av"></div>'
            f'<div class="ln b" style="flex:1;width:auto;margin:0"></div>{v}' + ('<div class="amt"></div>' if amt else '') + '</div>')


def sbar(w, n=None):
    return (f'<div style="margin-bottom:14px" class="rel">{P(n) if n else ""}<div class="row"><div class="av"></div><div class="ln b" style="flex:1;width:auto;margin:0"></div>'
            f'<div class="amt"></div></div><div class="bar2" style="margin-top:8px"><i style="width:{w}%"></i></div></div>')


W = {}
W['wf01_inicio_vacio'] = (f'<div class="phone">{bar(False)}<div style="text-align:center;margin-top:60px"><div class="ic" style="width:68px;height:68px;border-radius:50%;margin:0 auto 16px"></div>'
                          '<div class="ln b" style="width:60%;margin:0 auto 12px"></div><div class="ln" style="width:85%;margin:6px auto"></div><div class="ln" style="width:75%;margin:6px auto"></div>'
                          f'<div class="ln" style="width:55%;margin:6px auto 24px"></div></div><div class="btn" style="margin-bottom:12px">{P(1)}Crear mi primer grupo</div><div class="btn o">{P(2)}Probar con datos de ejemplo</div></div>')
W['wf02_inicio_grupos'] = ('<div class="phone">' + bar(False) + ''.join(
    f'<div class="box row" style="margin-bottom:11px;gap:14px">{P(1) if k == 0 else ""}<div class="ic" style="width:52px;height:52px"></div><div style="flex:1"><div class="ln b" style="width:75%"></div><div class="ln s"></div>'
    f'<div class="ln b" style="width:45%;background:#9a9a9a">{P(2) if k == 0 else ""}</div></div><div style="font-size:18px;color:#999">›</div></div>' for k in range(3)) +
    f'<div class="foot"><div class="btn">{P(3)}+ Nuevo grupo</div></div></div>')
W['wf03_nuevo_grupo'] = (f'<div class="phone">{bar(True, 1)}' + field('Nombre del grupo', 'Ej. Cuarto compartido', 2) +
                         '<div class="lbl">Ícono</div><div class="row rel" style="margin-bottom:16px">' + P(3) + ''.join('<div class="ic" style="width:44px;height:44px;border-radius:12px"></div>' for _ in range(6)) +
                         '</div><div class="lbl">Integrantes (3)</div><div class="box" style="margin-bottom:12px">' + P(4) +
                         ''.join('<div class="row" style="margin-bottom:8px"><div class="av"></div><div class="ln b" style="flex:1;width:auto;margin:0"></div><span class="x">✕</span></div>' for _ in range(3)) +
                         f'</div><div class="row" style="align-items:flex-end"><div style="flex:1"><div class="lbl">Agregar persona</div><div class="in" style="margin:0">{P(5)}Nombre</div></div><div class="av" style="width:48px;height:48px"></div></div>'
                         f'<div class="foot"><div class="btn">{P(6)}✓ Crear grupo</div></div></div>')
W['wf04_gastos'] = (f'<div class="phone">{bar(True, 1)}{hero(2)}<div style="height:12px"></div>{seg(0, n=3)}<div style="height:12px"></div>' + exprow(4) + exprow() * 3 +
                    f'<div class="foot"><div class="btn">{P(5)}+ Añadir gasto</div></div></div>')
W['wf05_nuevo_gasto'] = (f'<div class="phone">{bar()}' + field('¿Qué se pagó?', 'Ej. Luz de octubre', 1) + field('Monto (S/)', '0.00', 2) +
                         f'<div class="lbl">Categoría</div><div class="rel">{P(3)}<span class="chip on">Comida</span><span class="chip">Alquiler</span><span class="chip">Servicios</span><span class="chip">Transp.</span><span class="chip">Salidas</span></div>'
                         f'<div class="lbl" style="margin-top:6px">¿Quién pagó?</div><div class="rel">{P(4)}<span class="chip on">Yo</span><span class="chip">Camila</span><span class="chip">Diego</span></div>'
                         f'<div class="lbl" style="margin-top:6px">¿Cómo se reparte?</div>{seg(0, SPL, 5)}<div class="lbl" style="margin-top:12px">¿Entre quiénes?</div>'
                         f'<div class="box" style="padding-top:16px">{P(6)}{member()}{member()}{member(False, amt=False)}</div>'
                         f'<div class="foot"><div class="btn">{P(7)}✓ Guardar gasto</div></div></div>')
W['wf06_montos_error'] = (f'<div class="phone">{bar()}' + field('Monto (S/)', '120.00', 1, '#444') +
                          f'<div class="lbl">¿Cómo se reparte?</div>{seg(2, SPL, 2)}<div class="lbl" style="margin-top:12px">¿Entre quiénes?</div>'
                          f'<div class="box" style="padding-top:16px">{P(3)}{member(True, "50.00")}{member(True, "40.00")}{member(True, "20.00")}</div>'
                          f'<div class="err">{P(4)}&nbsp;&nbsp;&nbsp;⚠ Faltan S/ 10.00 por asignar</div><div class="foot"><div class="btn" style="opacity:.6">{P(5)}✓ Guardar gasto</div></div></div>')
W['wf07_saldos'] = (f'<div class="phone">{bar()}{hero()}<div style="height:12px"></div>{seg(1)}<div style="height:12px"></div><div class="box" style="padding-top:16px">{P(1)}' +
                    sbar(28, 2) + sbar(100) + sbar(40) + sbar(36) + '</div></div>')
W['wf08_liquidar'] = (f'<div class="phone">{bar()}{hero()}<div style="height:12px"></div>{seg(2)}<div style="height:12px"></div>'
                      f'<div class="box" style="margin-bottom:10px">{P(1)}<div class="ln b" style="width:55%"></div><div class="row" style="margin-top:8px"><div class="tile"><div class="ln s"></div><div class="big" style="width:30%"></div></div>'
                      '<div class="tile" style="background:#CFCFCF"><div class="ln s"></div><div class="big" style="width:30%"></div></div></div></div>'
                      f'<div class="box" style="margin-bottom:10px">{P(2)}<div class="row"><div class="av"></div><span class="x">→</span><div class="av"></div><div style="flex:1"><div class="ln b"></div><div class="ln b s" style="background:#888"></div></div></div>'
                      f'<div class="btn o" style="height:38px;margin-top:10px;font-size:12px">{P(3)}✓ Registrar como pagado</div></div>'
                      '<div class="box" style="margin-bottom:10px"><div class="row"><div class="av"></div><span class="x">→</span><div class="av"></div><div style="flex:1"><div class="ln b"></div><div class="ln b s" style="background:#888"></div></div></div></div>'
                      f'<div class="row"><div class="btn o" style="flex:1;font-size:12px">{P(4)}Copiar resumen</div><div class="btn o" style="flex:1;font-size:12px">WhatsApp</div></div></div>')
W['wf09_resumen'] = (f'<div class="phone">{bar()}{hero()}<div style="height:12px"></div>{seg(3)}<div style="height:12px"></div><div class="row" style="margin-bottom:10px"><div class="tile">{P(1)}<div class="ln s"></div><div class="big" style="width:60%"></div></div>'
                     '<div class="tile"><div class="ln s"></div><div class="big" style="width:60%"></div></div></div>'
                     f'<div class="box" style="margin-bottom:10px;padding-top:16px">{P(2)}<div class="ln b" style="width:50%"></div>' +
                     ''.join(f'<div style="margin:10px 0"><div class="row"><div class="ln" style="flex:1;width:auto;margin:0"></div><div class="amt" style="width:90px"></div></div><div class="bar2" style="margin-top:6px"><i style="width:{w}%"></i></div></div>' for w in (100, 40, 14, 7)) +
                     f'</div><div class="box" style="padding-top:16px">{P(3)}<div class="ln b" style="width:60%"></div>' +
                     ''.join('<div class="row" style="margin-top:9px"><div class="av" style="width:24px;height:24px"></div><div class="ln" style="flex:1;width:auto;margin:0"></div><div class="amt" style="width:56px"></div><div class="amt" style="width:56px"></div></div>' for _ in range(4)) + '</div></div>')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    for k, html in W.items():
        pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>')
        pg.wait_for_timeout(150)
        pg.screenshot(path=OUT + k + '.png')
    b.close()
print(list(W))
