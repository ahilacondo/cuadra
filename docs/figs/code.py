import sys, html, re; sys.path.insert(0,'/home/claude/lab4/figs')
from common import *
from pygments.lexers import TypeScriptLexer
from pygments.token import Token
CTRL={'if','for','while','return','else','of','in','break','continue','import','from','switch','case'}
KW={'const','let','var','function','export','type','interface','new','as','async','await','true','false','null','undefined','typeof'}
TYPES={'Balances','Transfer','Record','number','string','boolean','Int32Array','Int8Array','Group','Expense','Math','Object','Array'}
C={'ctrl':'#c586c0','kw':'#569cd6','str':'#ce9178','num':'#b5cea8','com':'#6a9955','fn':'#dcdcaa','ty':'#4ec9b0','var':'#9cdcfe','pun':'#d4d4d4'}
def hl(code):
    toks=list(TypeScriptLexer().get_tokens(code))
    out=[]
    for i,(t,v) in enumerate(toks):
        e=html.escape(v)
        if not v.strip(): out.append(e); continue
        if t in Token.Comment: out.append(f'<span style="color:{C["com"]};font-style:italic">{e}</span>'); continue
        if t in Token.Literal.String: out.append(f'<span style="color:{C["str"]}">{e}</span>'); continue
        if t in Token.Literal.Number: out.append(f'<span style="color:{C["num"]}">{e}</span>'); continue
        if v in CTRL: out.append(f'<span style="color:{C["ctrl"]}">{e}</span>'); continue
        if v in KW or t in Token.Keyword: out.append(f'<span style="color:{C["kw"]}">{e}</span>'); continue
        if v in TYPES: out.append(f'<span style="color:{C["ty"]}">{e}</span>'); continue
        if re.match(r'[A-Za-z_$][\w$]*$',v):
            nxt=''.join(x[1] for x in toks[i+1:i+3]).lstrip()
            col=C['fn'] if nxt.startswith('(') else C['var']
            out.append(f'<span style="color:{col}">{e}</span>'); continue
        out.append(f'<span style="color:{C["pun"]}">{e}</span>')
    return ''.join(out)
WCSS='''
.win{width:__W__px;background:#1e1e1e;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.28);border:1px solid #333}
.tb{height:38px;background:#323233;display:flex;align-items:center;padding:0 14px;position:relative}
.dots{display:flex;gap:8px}.dots i{width:13px;height:13px;border-radius:50%;display:block}
.ttl{position:absolute;left:0;right:0;text-align:center;color:#9d9d9d;font-size:13px}
.tabs{height:36px;background:#252526;display:flex;align-items:flex-end}
.tab{height:36px;background:#1e1e1e;color:#fff;font-size:13px;display:flex;align-items:center;gap:8px;padding:0 16px;border-top:2px solid #007acc}
.tab b{font-size:9px;background:#3178c6;color:#fff;border-radius:3px;padding:1px 3px;font-weight:700}
.crumb{height:26px;color:#a0a0a0;font-size:12px;display:flex;align-items:center;padding:0 16px;background:#1e1e1e}
.code{display:flex;padding:8px 0 14px;font-family:"DejaVu Sans Mono",monospace;font-size:14px;line-height:21px}
.gut{white-space:pre;color:#6e7681;text-align:right;padding:0 16px 0 14px;user-select:none;min-width:58px}
.src{white-space:pre;color:#d4d4d4;padding-right:24px}
.st{height:24px;background:#007acc;color:#fff;font-size:12px;display:flex;align-items:center;justify-content:space-between;padding:0 12px}
.term{width:__W__px;background:#1c1c1e;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.28);border:1px solid #3a3a3c}
.term .tb{background:#2c2c2e}
.tbody{padding:14px 18px 18px;font-family:"DejaVu Sans Mono",monospace;font-size:14px;line-height:22px;color:#e6e6e6;white-space:pre}
.p{color:#32d74b}.d{color:#64d2ff}.g{color:#8e8e93}.ok{color:#32d74b}.w{color:#fff;font-weight:700}
'''
def vscode(name, code, filename, path, start=1, w=820, lang='TypeScript'):
    lines=code.rstrip('\n').split('\n')
    gut='\n'.join(str(start+i) for i in range(len(lines)))
    body=f'''<div class="win"><div class="tb"><div class="dots"><i style="background:#ff5f56"></i><i style="background:#ffbd2e"></i><i style="background:#27c93f"></i></div><div class="ttl">{filename} — cuadra — Visual Studio Code</div></div>
<div class="tabs"><div class="tab"><b>TS</b>{filename}</div></div><div class="crumb">{path}</div>
<div class="code"><div class="gut">{gut}</div><div class="src">{hl(chr(10).join(lines))}</div></div>
<div class="st"><span>⎇ main</span><span>{lang} &nbsp; UTF-8 &nbsp; LF &nbsp; Spaces: 2</span></div></div>'''
    shot(name, body, WCSS.replace('__W__',str(w)), pad=20)
def terminal(name, rows, title, w=820):
    b=''
    for r in rows:
        k,t=r
        if k=='cmd': b+=f'<span class="p">andre@kellsitope</span> <span class="d">cuadra</span> <span class="g">%</span> <span class="w">{html.escape(t)}</span>\n'
        elif k=='ok': b+=f'<span class="ok">{html.escape(t)}</span>\n'
        elif k=='g': b+=f'<span class="g">{html.escape(t)}</span>\n'
        else: b+=html.escape(t)+'\n'
    body=f'<div class="term"><div class="tb"><div class="dots"><i style="background:#ff5f56"></i><i style="background:#ffbd2e"></i><i style="background:#27c93f"></i></div><div class="ttl">{title}</div></div><div class="tbody">{b.rstrip()}</div></div>'
    shot(name, body, WCSS.replace('__W__',str(w)), pad=20)
if __name__=='__main__':
    R='/home/claude/lab4/report/code/'
    vscode('code_split',open(R+'split.ts').read(),'split.ts','src › core › split.ts')
    vscode('code_greedy',open(R+'greedy.ts').read(),'settle.ts','src › core › settle.ts')
    opt=open(R+'optimal.ts').read().split('\n')
    # fragmento clave: líneas 1-32 (hasta cerrar el DP)
    frag='\n'.join(opt[:29])
    vscode('code_optimal',frag,'settle.ts','src › core › settle.ts › settleOptimal',start=1)
    terminal('term_tests',[('cmd','npm test -- --reporter=verbose'),('g',''),
      ('ok','✓ dinero > parsea montos con punto o coma'),('ok','✓ dinero > formatea en soles'),
      ('ok','✓ reparto > 100.00 entre 3 suma exactamente 100.00'),('ok','✓ reparto > el céntimo sobrante rota entre gastos'),
      ('ok','✓ reparto > porcentajes y partes respetan la suma'),('ok','✓ reparto > detecta montos exactos que no cuadran'),
      ('ok','✓ saldos y liquidación > ejemplo clásico: A paga 90 entre A,B,C'),('ok','✓ saldos y liquidación > cadena A→B→C se reduce a un solo pago'),
      ('ok','✓ saldos y liquidación > propiedades sobre 300 grupos aleatorios'),('ok','✓ saldos y liquidación > los pagos registrados reducen la deuda'),
      ('g',''),('t',' Test Files  1 passed (1)'),('t','      Tests  10 passed (10)'),('g','   Duration  364ms')],'andre — zsh — 96×24',w=900)
    terminal('term_cmds',[('cmd','npm install'),('g','# instala las dependencias'),
      ('cmd','npx expo start --web'),('g','# servidor de desarrollo en el navegador'),
      ('cmd','npm run export:web'),('g','# build web de producción en dist/'),
      ('cmd','npm test'),('g','# pruebas unitarias (Vitest)'),
      ('cmd','npx tsx scripts/simulate.ts'),('g','# experimento Monte Carlo'),
      ('cmd','python3 scripts/e2e.py'),('g','# pruebas E2E (dist/ servido en el puerto 8123)')],'andre — zsh — 96×24',w=900)
