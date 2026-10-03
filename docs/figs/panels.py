import sys; sys.path.insert(0,'/home/claude/lab4/figs')
from common import *
CSS='''
.row{display:flex;gap:34px;justify-content:center;align-items:flex-start}
.col{display:flex;flex-direction:column;align-items:center;gap:14px}
.col img{width:__W__px;border-radius:26px;border:1px solid #D9D3C7;box-shadow:0 6px 18px rgba(29,43,38,.12);display:block}
.lab{font-size:19px;font-weight:600;color:#1D2B26;text-align:center;max-width:__W__px;line-height:1.25}
.lab b{display:inline-block;width:28px;height:28px;border-radius:50%;background:#1E6B52;color:#fff;font-size:15px;line-height:28px;margin-right:8px;text-align:center}
.sep{width:2px;background:#E6E0D4;align-self:stretch;margin:0 8px}
.grp{display:flex;gap:22px;align-items:flex-start}
.top{font-size:17px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#5B6B64;text-align:center;margin-bottom:6px}
'''
def panel(name, items, w=330):
    cols=''
    for i,(f,l) in enumerate(items):
        cols+=f'<div class="col"><img src="file://{IMG}{f}"><div class="lab"><b>{chr(97+i)}</b>{l}</div></div>'
    shot(name, f'<div class="row">{cols}</div>', CSS.replace('__W__',str(w)), pad=22)
def pairs(name, pairs_, w=265):
    g=''
    for i,((f1,f2),t) in enumerate(pairs_):
        g+=f'<div><div class="top">{t}</div><div class="grp"><div class="col"><img src="file://{IMG}{f1}"><div class="lab">Wireframe</div></div><div class="col"><img src="file://{IMG}{f2}"><div class="lab">Aplicación</div></div></div></div>'
        if i<len(pairs_)-1: g+='<div class="sep"></div>'
    shot(name, f'<div class="row">{g}</div>', CSS.replace('__W__',str(w)), pad=22)
if __name__=='__main__':
    panel('p_wf1',[('wf01_inicio_vacio.png','Inicio sin grupos'),('wf02_inicio_grupos.png','Inicio con grupos'),('wf03_nuevo_grupo.png','Nuevo grupo')])
    panel('p_wf2',[('wf04_gastos.png','Detalle: Gastos'),('wf05_nuevo_gasto.png','Nuevo gasto'),('wf06_montos_error.png','Montos con error')])
    panel('p_wf3',[('wf07_saldos.png','Detalle: Saldos'),('wf08_liquidar.png','Detalle: Liquidar'),('wf09_resumen.png','Detalle: Resumen')])
    panel('p_r1',[('app_s01_vacio.png','Estado inicial'),('app_s02_grupo_validacion.png','Validación'),('app_s03_grupo_lleno.png','Grupo completo')])
    panel('p_r2',[('app_s04_grupo_sin_gastos.png','Grupo sin gastos'),('app_s05_form_igual.png','Reparto igual'),('app_s06_form_montos_error.png','Montos que no cuadran')])
    panel('p_r3',[('app_s07_form_porcentaje_error.png','Porcentajes inválidos'),('app_s08_form_partes.png','Reparto por partes'),('app_s09_gastos_grupo_nuevo.png','Gastos registrados')])
    panel('p_r4',[('app_s10_saldos_grupo_nuevo.png','Saldos'),('app_s11_inicio_con_grupo.png','Inicio tras recargar'),('app_s12_confirmar_eliminar.png','Confirmar eliminar')])
    panel('p_r5',[('app_s13_demo_gastos.png','Gastos'),('app_s14_demo_saldos.png','Saldos'),('app_s15_demo_liquidar.png','Liquidar')])
    panel('p_r6',[('app_s16_copiado.png','Copiar resumen'),('app_s17_pago_registrado.png','Pago registrado'),('app_s18_todos_al_dia.png','Todos al día')])
    panel('p_r7',[('app_s19_historial_pagos.png','Historial'),('app_s20_demo_resumen.png','Resumen')])
    pairs('p_fid1',[(('wf04_gastos.png','app_s13_demo_gastos.png'),'Detalle del grupo'),(('wf08_liquidar.png','app_s15_demo_liquidar.png'),'Liquidar')])
    pairs('p_fid2',[(('wf05_nuevo_gasto.png','app_s05_form_igual.png'),'Formulario de gasto'),(('wf06_montos_error.png','app_s06_form_montos_error.png'),'Error de reparto')])
