from playwright.sync_api import sync_playwright
OUT='/home/claude/lab4/report/img/'
base='''*{box-sizing:border-box;margin:0;padding:0;font-family:"Inter","DejaVu Sans",sans-serif}body{background:#fff;color:#1D2B26;padding:26px;width:1100px}
h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:#5B6B64;margin:0 0 12px}
.sw{display:flex;gap:12px;flex-wrap:wrap}.c{width:122px}.c div{height:62px;border-radius:12px;border:1px solid #E6E0D4}.c b{display:block;font-size:12.5px;margin-top:6px}.c i{font-style:normal;font-size:11px;color:#5B6B64}
.sec{margin-bottom:26px}.row{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.btn{border-radius:99px;padding:13px 22px;font-weight:700;font-size:15px}.chip{border:1.5px solid #E6E0D4;border-radius:99px;padding:8px 13px;font-weight:600;font-size:13.5px;background:#fff}
.seg{display:flex;background:#EAE4D8;border-radius:99px;padding:3px;width:340px}.seg div{flex:1;text-align:center;padding:9px 0;font-size:13.5px;font-weight:600;color:#5B6B64;border-radius:99px}.seg .on{background:#fff;color:#1D2B26;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,.08)}
.card{background:#fff;border-radius:16px;padding:14px;box-shadow:0 4px 12px rgba(29,43,38,.08);width:300px}.av{width:36px;height:36px;border-radius:50%;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center}
.ty div{margin:5px 0}.in{border:1.5px solid #E6E0D4;border-radius:10px;padding:12px 14px;width:260px;font-size:16px;color:#9AA6A0}.in.e{border-color:#BC3E17}
'''
ds=f'''<html><head><meta charset=utf-8><style>{base}</style></head><body>
<div class=sec><h3>Paleta · inspirada en Arequipa (sillar, campiña, rocoto)</h3><div class=sw>
<div class=c><div style="background:#F7F3EC"></div><b>Sillar</b><i>#F7F3EC · fondo</i></div>
<div class=c><div style="background:#FFFFFF"></div><b>Tarjeta</b><i>#FFFFFF · superficie</i></div>
<div class=c><div style="background:#1D2B26"></div><b>Tinta</b><i>#1D2B26 · texto</i></div>
<div class=c><div style="background:#5B6B64"></div><b>Tinta suave</b><i>#5B6B64 · secundario</i></div>
<div class=c><div style="background:#1E6B52"></div><b>Campiña</b><i>#1E6B52 · primario / "te deben"</i></div>
<div class=c><div style="background:#DDEFE7"></div><b>Campiña suave</b><i>#DDEFE7 · fondos</i></div>
<div class=c><div style="background:#BC3E17"></div><b>Rocoto</b><i>#BC3E17 · acento / "debes"</i></div>
<div class=c><div style="background:#E6E0D4"></div><b>Línea</b><i>#E6E0D4 · bordes</i></div></div></div>
<div class=sec><h3>Avatares de integrantes (orden fijo por persona)</h3><div class=row>'''+''.join(f'<div class=av style="background:{c}">{l}</div>' for c,l in zip(['#1E6B52','#BC3E17','#3B6FB6','#8A5CC2','#A8650A','#1D7A70','#B5446E','#5C6B73'],'YCDVMRAL'))+'''</div></div>
<div class=sec><h3>Tipografía · fuente del sistema (rendimiento y coherencia nativa)</h3><div class=ty>
<div style="font-size:24px;font-weight:800;letter-spacing:-.4px">Título de pantalla · 24 / 800</div><div style="font-size:19px;font-weight:800">Título de estado vacío · 19 / 800</div><div style="font-size:17px;font-weight:700">Encabezado de tarjeta · 17 / 700</div><div style="font-size:15px">Cuerpo · 15 / 400 — Pagó Camila · 10 oct</div><div style="font-size:13px;color:#5B6B64">Texto de apoyo · 13 / 400</div><div style="font-size:30px;font-weight:800;color:#1E6B52">S/ 194.26 · cifras destacadas 30 / 800</div></div></div>
<div class=sec><h3>Componentes</h3><div class=row style="margin-bottom:14px">
<div class=btn style="background:#1E6B52;color:#fff">Primario</div><div class=btn style="background:#DDEFE7;color:#14503D">Suave</div><div class=btn style="border:1.5px solid #1E6B52;color:#1E6B52">Contorno</div><div class=btn style="background:#BC3E17;color:#fff">Peligro</div>
<div class=chip>Comida</div><div class=chip style="background:#BC3E17;border-color:#BC3E17;color:#fff">Comida</div></div>
<div class=row style="margin-bottom:14px"><div class=seg><div class=on>Gastos</div><div>Saldos</div><div>Liquidar</div><div>Resumen</div></div>
<div><div class=in>Ej. Luz de octubre</div></div><div><div class="in e" style="color:#1D2B26">abc</div><div style="color:#BC3E17;font-size:12.5px;font-weight:600;margin-top:5px">Ingresa un monto válido, ej. 45.50</div></div></div>
<div class=row><div class=card><div class=row style="gap:12px"><div class=av style="background:#1E6B52">C</div><div><b style="font-size:15px">Alquiler de octubre</b><div style="font-size:13px;color:#5B6B64">Pagó Camila · 1 oct · 4 pers.</div></div></div></div>
<div class=card style="background:#BC3E17;color:#fff"><div style="font-size:13px;opacity:.85">Tu saldo en el grupo</div><div style="font-size:28px;font-weight:800">S/ 194.26</div><div style="font-weight:600">debes en total</div></div></div></div>
<div class=sec style="margin-bottom:0"><h3>Medidas</h3><div style="font-size:14px;line-height:1.7">Radios: 10 (campos) · 16 (tarjetas) · 22 · píldora 999 &nbsp;|&nbsp; Espaciado base: 4 px (12–16 px entre elementos) &nbsp;|&nbsp; Ancho máximo de contenido: 560 px &nbsp;|&nbsp; Áreas táctiles ≥ 40 px</div></div>
</body></html>'''
jm=f'''<html><head><meta charset=utf-8><style>{base}
table{{border-collapse:separate;border-spacing:8px;width:100%;table-layout:fixed}}th{{background:#1E6B52;color:#fff;border-radius:12px;padding:12px;font-size:14px}}td{{background:#F7F3EC;border-radius:12px;padding:12px;font-size:13px;vertical-align:top;line-height:1.45}}td.h{{background:#fff;font-weight:800;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#5B6B64;width:110px;border:1.5px solid #E6E0D4}}
.pain{{background:#FBE3DA}}.op{{background:#DDEFE7}}</style></head><body>
<table><tr><th></th><th>1. Ocurre un gasto común</th><th>2. Se anota (o no)</th><th>3. Se acumulan deudas</th><th>4. Llega el momento de cuadrar</th><th>5. Se paga</th></tr>
<tr><td class=h>¿Qué hace?</td><td>Alguien paga alquiler, luz, mercado o una salida con su propio dinero.</td><td>Lo recuerda de memoria, escribe en el chat del grupo o en una libreta.</td><td>Los gastos se mezclan: no todos participan en todo.</td><td>Intenta reconstruir quién puso qué y calcula a mano o con calculadora.</td><td>Transfiere o paga en efectivo a cada persona, gasto por gasto.</td></tr>
<tr><td class=h>Dolor</td><td class=pain>Nadie sabe cuánto lleva puesto cada quien.</td><td class=pain>Registros dispersos o inexistentes; se pierden recibos.</td><td class=pain>Reparto desigual difícil de seguir (¿quién comió qué?).</td><td class=pain>Errores de redondeo y discusiones; cuentas largas.</td><td class=pain>Muchos pagos cruzados (A→B, B→C, C→A).</td></tr>
<tr><td class=h>Cómo ayuda Cuadra</td><td class=op>Registro en segundos: monto, pagador, categoría.</td><td class=op>Un solo lugar, guardado en el dispositivo.</td><td class=op>Reparto igual, por %, montos o partes; valida que cuadre al céntimo.</td><td class=op>Saldos netos al instante y resumen por categoría.</td><td class=op>Mínimo de pagos (búsqueda exacta) + «Registrar como pagado» + compartir por WhatsApp.</td></tr></table>
<div style="font-size:12px;color:#5B6B64;margin:6px 8px">Mapa de experiencia elaborado como hipótesis del autor a partir del contexto descrito; no resume entrevistas ni encuestas.</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1152,'height':800},device_scale_factor=2)
    for name,h in [('sistema_diseno',ds),('mapa_experiencia',jm)]:
        pg.set_content(h); pg.wait_for_timeout(250)
        pg.locator('body').screenshot(path=OUT+name+'.png')
    b.close()
