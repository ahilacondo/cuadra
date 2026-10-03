import sys; sys.path.insert(0,'/home/claude/lab4/figs')
from common import *
G='#1E6B52';GS='#DDEFE7';R='#BC3E17';RS='#FBE3DA';B='#3B6FB6';BS='#E6EEF8';Y='#A8650A';YS='#FCF0D5';INK='#1D2B26';SOFT='#5B6B64';LINE='#9AA6A0'
CSS='''
svg text{font-family:"Inter","DejaVu Sans",sans-serif}
'''
def svg(w,h,inner): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker><marker id="r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>'%(SOFT,R)+inner+'</svg>'
K=1.22
def box(x,y,w,h,lines,fill=GS,stroke=G,title=None,rx=14,fs=17,tfs=18,sw=2):
    fs=int(fs*K); tfs=int(tfs*K)
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    allm=([('b',title)] if title else [])+[('n',l) for l in lines]
    lh=fs+7; tot=len(allm)*lh; y0=y+(h-tot)/2+fs
    for i,(k,t) in enumerate(allm):
        s+=f'<text x="{x+w/2}" y="{y0+i*lh-3}" text-anchor="middle" font-size="{tfs if k=="b" else fs}" font-weight="{700 if k=="b" else 400}" fill="{INK}">{t}</text>'
    return s
def arrow(x1,y1,x2,y2,col=SOFT,dash=False,m='a',w=2.2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" {"stroke-dasharray=\"8 6\"" if dash else ""} marker-end="url(#{m})"/>'
def path(d,col=SOFT,dash=False,m='a',w=2.2):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" {"stroke-dasharray=\"8 6\"" if dash else ""} marker-end="url(#{m})"/>'
def txt(x,y,t,fs=15,col=SOFT,anchor='middle',w=400):
    fs=int(fs*K)
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" font-weight="{w}" fill="{col}">{t}</text>'

# 1 metodologia -------------------------------------------------
def metodologia():
    W,H=1780,700
    ph=[('1. Empatizar',['Datos públicos','Mapa de experiencia']),('2. Definir',['Candidatos y matriz AHP','Sensibilidad · Enunciado']),('3. Idear',['Historias MoSCoW','Algoritmo y datos']),('4. Prototipar',['Sistema de diseño','Wireframes · App']),('5. Probar',['Unitarias · E2E','Simulación · Heurísticas'])]
    cw,gap=290,40; x0=50; y=70; s=''
    s+=txt(x0,38,'DESIGN THINKING',15,SOFT,'start',700)
    for i,(t,l) in enumerate(ph):
        x=x0+i*(cw+gap); s+=box(x,y,cw,140,l,GS,G,t)
        if i<4: s+=arrow(x+cw+4,y+65,x+cw+gap-4,y+65)
    inc=[('Incremento 1',['Núcleo de cálculo','+ pruebas unitarias']),('Incremento 2',['Pantallas y','persistencia local']),('Incremento 3',['Liquidación, resumen','y pruebas E2E'])]
    s+=txt(x0+2*(cw+gap),330,'SCRUM LIGERO',15,SOFT,'start',700)
    for j,(t,l) in enumerate(inc):
        i=2+j; x=x0+i*(cw+gap); s+=box(x,360,cw,120,l,YS,Y,t)
        s+=f'<line x1="{x+cw/2}" y1="{y+146}" x2="{x+cw/2}" y2="354" stroke="{LINE}" stroke-width="2" stroke-dasharray="3 6"/>'
        if j<2: s+=arrow(x+cw+4,420,x+cw+gap-4,420)
    # iterate arrow from Probar back to Definir
    xp=x0+4*(cw+gap)+cw/2; xd=x0+1*(cw+gap)+cw/2
    s+=path(f'M {x0+4*(cw+gap)+cw+4} {y+65} H 1736 V 600 H {xd} V {y+146}',R,True,'r')
    s+=txt((1736+xd)/2,640,'Si una prueba falla se vuelve a «Definir» (p. ej., la auditoría de contraste)',16,R,'middle',600)
    shot('metodologia',svg(W,H,s),CSS,pad=10)

# 2 flujo ---------------------------------------------------------
def flujo():
    W,H=1540,1060; s=''
    cx=650
    s+=box(cx-250,20,500,84,['monto, pagador y reparto de cada gasto'],GS,G,'Gastos y pagos registrados')
    s+=arrow(cx,104,cx,150)
    s+=box(cx-250,150,500,100,['saldo = pagado − le corresponde','(ajustado por pagos ya registrados)'],GS,G,'Saldo neto por persona')
    s+=box(40,160,300,80,['siempre suman cero'],YS,Y,'Invariante Σ = 0',fs=16)
    s+=f'<line x1="340" y1="200" x2="{cx-250}" y2="200" stroke="{Y}" stroke-width="2" stroke-dasharray="3 5"/>'
    s+=arrow(cx,250,cx,296)
    s+=box(cx-250,296,500,84,['k = personas con saldo ≠ 0'],'#F7F3EC',LINE,'Descartar saldos en cero')
    s+=arrow(cx,380,cx,430)
    # diamond
    s+=f'<polygon points="{cx},430 {cx+120},480 {cx},530 {cx-120},480" fill="{RS}" stroke="{R}" stroke-width="2"/>'+txt(cx,488,'¿k ≤ 16?',20,INK,'middle',700)
    lx,rx_=300,1000
    s+=path(f'M {cx-120} 480 H {lx} V 580',SOFT)+txt(cx-200,468,'sí',16,SOFT,'middle',600)
    s+=path(f'M {cx+120} 480 H {rx_} V 580',SOFT)+txt(cx+200,468,'no',16,SOFT,'middle',600)
    s+=box(lx-230,580,460,110,['programación dinámica sobre subconjuntos','máx. subgrupos de saldo 0 → pagos = k − G'],BS,B,'Búsqueda exacta')
    s+=arrow(lx,690,lx,740)
    s+=box(lx-230,740,460,100,['dentro de cada subgrupo:','tamaño − 1 pagos (codicioso)'],BS,B,'Pagos por subgrupo')
    s+=box(rx_-230,580,460,110,['el mayor deudor paga al mayor acreedor','(máx. k − 1 pagos)'],BS,B,'Heurística codiciosa')
    s+=path(f'M {lx} 840 V 885 H {cx-30} V 905',SOFT)
    s+=path(f'M {rx_} 690 V 885 H {cx+30} V 905',SOFT)
    s+=box(cx-250,905,500,80,['«A paga S/ x a B»'],GS,G,'Lista de transferencias')
    s+=path(f'M {cx+250} 945 H 1260 V 200 H {cx+254}',R,True,'r')
    for i,t in enumerate(['Registrar un pago crea','un Settlement y se','recalculan los saldos']): s+=txt(1276,520+i*22,t,16,R,'start',600)
    shot('flujo_algoritmo',svg(W,H,s),CSS,pad=10)

# 3 arquitectura ------------------------------------------------
def arquitectura():
    W,H=1400,720; s=''
    # presentación
    s+=f'<rect x="20" y="20" width="1360" height="190" rx="18" fill="#EDF6F1" stroke="{G}" stroke-width="2"/>'+txt(44,52,'PRESENTACIÓN · Expo Router + React Native',16,G,'start',700)
    items=[('index',['Mis grupos']),('group/new',['Nuevo grupo']),('group/[id]',['Gastos · Saldos','Liquidar · Resumen']),('group/[id]/expense',['Nuevo / editar gasto']),('ui/kit',['Button · Card · Chip','Segmented · Field'])]
    x=44
    for i,(t,l) in enumerate(items):
        w=245
        s+=box(x,72,w,110,l,YS if t=='ui/kit' else '#fff',Y if t=='ui/kit' else LINE,t,fs=15,tfs=16)
        x+=w+17
    # estado + núcleo
    s+=f'<rect x="20" y="300" width="600" height="190" rx="18" fill="#FBF1EC" stroke="{R}" stroke-width="2"/>'+txt(44,332,'ESTADO',16,R,'start',700)
    s+=box(44,350,552,120,['createGroup · saveExpense','addSettlement · loadDemo'],'#fff',LINE,'StoreProvider (React Context)',fs=15,tfs=16)
    s+=f'<rect x="680" y="300" width="700" height="190" rx="18" fill="{BS}" stroke="{B}" stroke-width="2"/>'+txt(704,332,'NÚCLEO DE DOMINIO · TypeScript puro, sin interfaz',16,B,'start',700)
    core=[('money.ts',['Parseo y','formato S/']),('split.ts',['Reparto','mayor resto']),('balances.ts',['Saldos','netos']),('settle.ts',['Liquidación','(3 estrategias)'])]
    x=704
    for t,l in core:
        s+=box(x,350,155,120,l,'#fff',LINE,t,fs=14,tfs=15); x+=163
    # persistencia
    s+=f'<rect x="20" y="580" width="600" height="120" rx="18" fill="#F3F0F8" stroke="#8A5CC2" stroke-width="2"/>'+txt(44,612,'PERSISTENCIA',16,'#6C45A3','start',700)
    s+=box(44,628,552,56,['AsyncStorage (localStorage en la web) · JSON'],'#fff',LINE,fs=15)
    s+=arrow(320,210,320,296)+txt(335,262,'acciones y estado',14,SOFT,'start')
    s+=arrow(1030,210,1030,296)+txt(1045,262,'llama al cálculo',14,SOFT,'start')
    s+=arrow(320,490,320,576)+txt(335,538,'serializa JSON',14,SOFT,'start')
    s+=arrow(624,420,676,420,SOFT,True)
    shot('arquitectura',svg(W,H,s),CSS,pad=10)

# 4 modelo de datos ----------------------------------------------
def card(x,y,w,title,col,rows):
    h=54+len(rows)*34+14
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="{col}" stroke-width="2"/><path d="M{x} {y+54}V{y+10}Q{x} {y} {x+10} {y}H{x+w-10}Q{x+w} {y} {x+w} {y+10}V{y+54}Z" fill="{col}"/>'
    s+=txt(x+w/2,y+36,title,20,'#fff','middle',700)
    for i,(n,t) in enumerate(rows):
        s+=f'<text x="{x+18}" y="{y+54+34*(i+1)-8}" font-size="{int(16*K)}" fill="{INK}" style="font-family:\'DejaVu Sans Mono\',monospace"><tspan font-weight="700">{n}</tspan><tspan fill="{SOFT}"> : {t}</tspan></text>'
    return s,h
def modelo():
    W,H=1480,690; s=''
    gx,gy=620,20
    c,gh=card(gx,gy,360,'Group',G,[('id','string'),('name','string'),('emoji','string'),('meId','string → Member'),('createdAt','date')]);s+=c
    mx,my=620,330
    c,mh=card(mx,my,360,'Member',B,[('id','string'),('name','string')]);s+=c
    ex,ey=20,250
    c,eh=card(ex,ey,420,'Expense',R,[('id','string'),('title','string'),('amountCents','int'),('paidBy','string → Member'),('category','enum'),('date','yyyy-mm-dd'),('mode','equal|percent|exact|shares'),('owed','Map&lt;Member, int&gt;')]);s+=c
    sx,sy=1080,250
    c,sh=card(sx,sy,380,'Settlement',Y,[('id','string'),('from','string → Member'),('to','string → Member'),('amountCents','int'),('date','yyyy-mm-dd')]);s+=c
    # Group - Member
    s+=f'<line x1="800" y1="{gy+gh}" x2="800" y2="{my}" stroke="{SOFT}" stroke-width="2.2"/>'+txt(814,gy+gh+26,'1',16,INK,'start',700)+txt(814,my-10,'2..n',16,INK,'start',700)
    # Group - Expense elbow
    s+=path(f'M {gx} 120 H 230 V {ey}',SOFT,False,'a').replace(' marker-end="url(#a)"','')
    s+=txt(gx-12,108,'1',16,INK,'end',700)+txt(242,ey-10,'0..*',16,INK,'start',700)
    s+=path(f'M {gx+360} 120 H 1270 V {sy}',SOFT,False,'a').replace(' marker-end="url(#a)"','')
    s+=txt(gx+372,108,'1',16,INK,'start',700)+txt(1258,sy-10,'0..*',16,INK,'end',700)
    # Expense -> Member, Settlement -> Member dashed
    s+=arrow(ex+420,my+55,mx-4,my+55,SOFT,True)+txt((ex+420+mx)/2,my+36,'paidBy / owed',14,SOFT,'middle',600)
    s+=arrow(sx,my+55,mx+360+4,my+55,SOFT,True)+txt((sx+mx+360)/2,my+36,'from / to',14,SOFT,'middle',600)
    s+=txt(740,650,'Línea continua: composición dentro del grupo · Línea punteada: referencia a un Member por su id',15,SOFT,'middle',500)
    shot('modelo_datos',svg(W,H,s),CSS,pad=10)
if __name__=='__main__':
    metodologia();flujo();arquitectura();modelo()

def navegacion():
    W,H=1480,560; s=''
    # nodes
    s+=box(30,240,250,100,['Mis grupos'],GS,G,'Inicio')
    s+=box(360,40,260,90,['nombre, ícono, integrantes'],'#F7F3EC',LINE,'Nuevo grupo',fs=15)
    # detalle container
    s+=f'<rect x="460" y="190" width="520" height="210" rx="18" fill="{GS}" stroke="{G}" stroke-width="2.4"/>'+txt(720,226,'Detalle del grupo',21,INK,'middle',700)
    tabs=['Gastos','Saldos','Liquidar','Resumen']
    for i,t in enumerate(tabs):
        s+=f'<rect x="{482+i*122}" y="262" width="112" height="56" rx="28" fill="#fff" stroke="{LINE}" stroke-width="2"/>'+txt(538+i*122,296,t,17,INK,'middle',600)
    s+=txt(720,364,'cuatro pestañas internas',15,SOFT,'middle',500)
    s+=box(1130,240,320,100,['monto, pagador, categoría, reparto'],'#F7F3EC',LINE,'Nuevo / editar gasto',fs=15)
    # arrows
    s+=path('M 155 236 V 85 H 356',SOFT)+txt(170,160,'Nuevo grupo',15,SOFT,'start',600)
    s+=path('M 624 85 H 720 V 186',SOFT)+txt(735,140,'Crear',15,SOFT,'start',600)
    s+=arrow(284,275,456,275)+txt(370,262,'Tocar grupo o demo',15,SOFT,'middle',600)
    s+=arrow(456,330,284,330)+txt(370,356,'Volver / eliminar',15,SOFT,'middle',600)
    s+=arrow(984,270,1126,270)+txt(1055,254,'Añadir gasto',15,SOFT,'middle',600)
    s+=arrow(1126,320,984,320)+txt(1055,344,'Guardar',15,SOFT,'middle',600)
    s+=txt(740,470,'Tres niveles como máximo: Inicio → Detalle del grupo → Formulario de gasto',16,SOFT,'middle',500)
    shot('navegacion',svg(W,500,s),CSS,pad=10)
