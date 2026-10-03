import json, numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

R='/home/claude/lab4/report/'
INK='#1D2B26'; SOFT='#5B6B64'; GRID='#E6E0D4'
C1,C2,C3='#2a78d6','#eb6834','#1baf7a'   # slots 1-3 del palette validado (todas las parejas)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':GRID,'axes.labelcolor':SOFT,
  'xtick.color':SOFT,'ytick.color':SOFT,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,
  'grid.color':GRID,'grid.linewidth':0.6,'axes.axisbelow':True,'figure.dpi':200,'savefig.bbox':'tight'})

d=json.load(open('/home/claude/lab4/data/sim.json')); df=pd.DataFrame(d['rows'])
df['same']=(df.greedy==df.optimal)
def ci(s):
    m=s.mean(); h=1.96*s.std(ddof=1)/np.sqrt(len(s)); return m,h
sizes=d['sizes']; T=d['trials']

# ---------- Fig 1: transferencias vs n (m=10, escenario continuo)
sub=df[(df.scenario=='continuo')&(df.m==10)]
fig,ax=plt.subplots(figsize=(6.2,3.5))
for col,c,lab in [('naive',C1,'Sin simplificar (por pares)'),('greedy',C2,'Codicioso'),('optimal',C3,'Óptimo (búsqueda exacta)')]:
    ms=[];hs=[]
    for n in sizes:
        m,h=ci(sub[sub.n==n][col]); ms.append(m); hs.append(h)
    ms=np.array(ms);hs=np.array(hs)
    ax.plot(sizes,ms,'-o',color=c,lw=2,ms=5,label=lab,mec='white',mew=1.2)
    ax.fill_between(sizes,ms-hs,ms+hs,color=c,alpha=.18,lw=0)
ax.plot(sizes,[n-1 for n in sizes],ls=(0,(4,3)),color=SOFT,lw=1,label='Cota superior n−1')
ax.set_xlabel('Integrantes del grupo (n)'); ax.set_ylabel('Transferencias necesarias (media)')
ax.set_xticks(sizes)
ax.annotate(f"{sub[sub.n==12].naive.mean():.0f}",(12,sub[sub.n==12].naive.mean()),textcoords='offset points',xytext=(-4,7),ha='right',color=INK,fontweight='bold')
ax.annotate(f"{sub[sub.n==12].optimal.mean():.1f}",(12,sub[sub.n==12].optimal.mean()),textcoords='offset points',xytext=(-4,-14),ha='right',color=INK,fontweight='bold')
ax.legend(frameon=False,loc='upper left')
fig.savefig(R+'img/sim_transferencias.png'); plt.close(fig)

# ---------- Fig 2: reducción % por n y m
fig,ax=plt.subplots(figsize=(6.2,3.3))
w=0.26
for j,(m,c) in enumerate(zip([5,10,20],['#a9c9ee','#4f93de','#1f5fae'])):
    red=[]
    for n in sizes:
        s=df[(df.scenario=='continuo')&(df.m==m)&(df.n==n)]
        red.append(100*(1-s.optimal.mean()/s.naive.mean()))
    xs=np.arange(len(sizes))+(j-1)*w
    ax.bar(xs,red,w-0.04,color=c,label=f'{m} gastos')
ax.set_xticks(np.arange(len(sizes))); ax.set_xticklabels(sizes)
ax.set_xlabel('Integrantes del grupo (n)'); ax.set_ylabel('Reducción de pagos vs. sin simplificar (%)')
ax.legend(frameon=False,ncol=3,loc='upper left'); ax.set_ylim(0,100)
fig.savefig(R+'img/sim_reduccion.png'); plt.close(fig)

# ---------- Fig 3: P(codicioso = óptimo) + tiempos
fig,(a,b)=plt.subplots(1,2,figsize=(6.6,3.1))
for sc,c,ls in [('continuo',C2,'-'),('redondeado',C3,'-')]:
    p=[];lo=[];hi=[]
    for n in sizes:
        s=df[(df.scenario==sc)&(df.n==n)].same
        k=s.sum();N=len(s); ph=k/N; z=1.96
        den=1+z*z/N; cen=(ph+z*z/(2*N))/den; hw=z*np.sqrt(ph*(1-ph)/N+z*z/(4*N*N))/den
        p.append(100*ph);lo.append(100*(cen-hw));hi.append(100*(cen+hw))
    a.plot(sizes,p,'-o',color=c,lw=2,ms=5,mec='white',label='Montos libres' if sc=='continuo' else 'Montos redondeados (S/ 5)')
    a.fill_between(sizes,lo,hi,color=c,alpha=.2,lw=0)
a.set_ylim(90,100.5); a.set_xticks(sizes); a.set_xlabel('Integrantes (n)'); a.set_ylabel('Casos donde codicioso = óptimo (%)')
a.legend(frameon=False,loc='lower left',fontsize=8)
tm=pd.DataFrame(d['timing'])
b.semilogy(tm.k,tm.median_ms,'-o',color=C1,lw=2,ms=5,mec='white')
b.axvline(16,color=SOFT,ls=(0,(4,3)),lw=1); b.text(15.8,tm.median_ms.min()*1.6,'límite de la app\n(k = 16)',color=SOFT,fontsize=8,ha='right')
b.set_xlabel('Personas con saldo ≠ 0 (k)'); b.set_ylabel('Tiempo mediano (ms, escala log)')
b.set_xticks(tm.k)
fig.tight_layout(); fig.savefig(R+'img/sim_gap_tiempo.png'); plt.close(fig)

# ---------- Tablas LaTeX
def f1(x): return f'{x:.1f}'
rows=[]
for n in sizes:
    s=df[(df.scenario=='continuo')&(df.m==10)&(df.n==n)]
    nm,nh=ci(s.naive); gm,gh=ci(s.greedy); om,oh=ci(s.optimal)
    red=100*(1-om/nm)
    w1=stats.wilcoxon(s.naive,s.optimal).pvalue
    rows.append(f"{n} & {nm:.1f} $\\pm$ {nh:.2f} & {gm:.2f} $\\pm$ {gh:.2f} & {om:.2f} $\\pm$ {oh:.2f} & {red:.1f}\\% & {'$<0{,}001$' if w1<0.001 else f'{w1:.3f}'} \\\\")
open(R+'tables/sim_main.tex','w').write('\n'.join(rows))

rows=[]
for n in sizes:
    line=[str(n)]
    for m in [5,10,20]:
        s=df[(df.scenario=='continuo')&(df.m==m)&(df.n==n)]
        line.append(f"{s.naive.mean():.1f} / {s.optimal.mean():.1f} ({100*(1-s.optimal.mean()/s.naive.mean()):.0f}\\%)")
    rows.append(' & '.join(line)+' \\\\')
open(R+'tables/sim_m.tex','w').write('\n'.join(rows))

rows=[]
for n in sizes:
    a=df[(df.scenario=='continuo')&(df.n==n)]; b_=df[(df.scenario=='redondeado')&(df.n==n)]
    gapA=(a.greedy-a.optimal); gapB=(b_.greedy-b_.optimal)
    rows.append(f"{n} & {100*a.same.mean():.1f}\\% & {gapA.max()} & {100*b_.same.mean():.1f}\\% & {gapB.max()} \\\\")
open(R+'tables/sim_gap.tex','w').write('\n'.join(rows))

rows=[f"{int(r.k)} & {2**int(r.k):,} & {r.median_ms:.2f} \\\\".replace(',','\\,') for r in tm.itertuples()]
open(R+'tables/sim_time.tex','w').write('\n'.join(rows))

# valores para el texto
n6=df[(df.scenario=='continuo')&(df.m==10)&(df.n==6)]
n12=df[(df.scenario=='continuo')&(df.m==10)&(df.n==12)]
summary=dict(total=len(df),n6_naive=n6.naive.mean(),n6_opt=n6.optimal.mean(),n12_naive=n12.naive.mean(),n12_opt=n12.optimal.mean(),
  overall_eq=df.same.mean(),worst_eq=df.groupby(['scenario','n']).same.mean().min(),max_gap=int((df.greedy-df.optimal).max()),
  opt_le_greedy=bool((df.optimal<=df.greedy).all()), greedy_le_k1=bool((df.greedy<=np.maximum(df.k-1,0)).all()),
  opt_le_naive=bool((df.optimal<=df.naive).all()), tm=d['timing'])
json.dump(summary,open('/home/claude/lab4/data/sim_summary.json','w'),indent=1,default=float)
print(json.dumps(summary,indent=1,default=float))
