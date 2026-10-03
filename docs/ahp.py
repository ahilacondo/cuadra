import numpy as np, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
R='/home/claude/lab4/report/'
INK='#1D2B26'; SOFT='#5B6B64'; GRID='#E6E0D4'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.edgecolor':GRID,'axes.labelcolor':SOFT,'xtick.color':SOFT,'ytick.color':SOFT,
  'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.color':GRID,'grid.linewidth':.6,'axes.axisbelow':True,'figure.dpi':200,'savefig.bbox':'tight'})

crit=['Frecuencia\ndel problema','Viabilidad\ntécnica','Evidencia\nverificable','Impacto en\nel estudiante','Valor\ndemostrable']
crit1=['Frecuencia','Viabilidad','Evidencia','Impacto','Valor']
A=np.array([[1,1/2,2,1,2],
            [2,1,3,2,3],
            [1/2,1/3,1,1/2,1],
            [1,1/2,2,1,2],
            [1/2,1/3,1,1/2,1]])
w,v=np.linalg.eig(A); i=np.argmax(w.real); lam=w[i].real
wt=np.abs(v[:,i].real); wt/=wt.sum()
n=5; CI=(lam-n)/(n-1); RI=1.12; CR=CI/RI
alts=['Gastos compartidos','Entregas y labs\nacadémicos','Menú del día\ncerca del campus','Transporte urbano\nen Arequipa','Cortes de agua\n(SEDAPAR)']
alts1=['Gastos compartidos','Entregas y labs académicos','Menú del día cerca del campus','Transporte urbano en Arequipa','Cortes de agua (SEDAPAR)']
S=np.array([[4,5,5,4,5],
            [5,5,5,3,2],
            [4,3,1,3,2],
            [5,2,1,4,3],
            [3,2,2,3,1]],float)
score=S@wt
order=np.argsort(-score)

rng=np.random.default_rng(2026)
# sensibilidad 1: pesos Dirichlet(1,...,1)
W=rng.dirichlet(np.ones(5),20000)
sc=W@S.T
ranks=(-sc).argsort(1).argsort(1)+1
p1=(ranks==1).mean(0); meanrank=ranks.mean(0)
# sensibilidad 2: ruido en puntajes (-1,0,+1 con prob .25,.5,.25), pesos AHP fijos
noise=rng.choice([-1,0,1],size=(20000,5,5),p=[.25,.5,.25])
S2=np.clip(S[None]+noise,1,5)
sc2=S2@wt
r2=(-sc2).argsort(1).argsort(1)+1
p1b=(r2==1).mean(0)

out=dict(weights=dict(zip(crit1,wt.round(4))),lam=lam,CI=CI,CR=CR,score=dict(zip(alts1,score.round(3))),p1_dirichlet=dict(zip(alts1,p1.round(3))),meanrank=dict(zip(alts1,meanrank.round(2))),p1_noise=dict(zip(alts1,p1b.round(3))))
json.dump(out,open('/home/claude/lab4/data/ahp.json','w'),indent=1,default=float)
print(json.dumps(out,indent=1,default=float))

# tablas tex
fr=lambda x:('%g'%x) if x>=1 else ('1/%d'%round(1/x))
rows=[]
for i_,nm in enumerate(crit1):
    rows.append(nm+' & '+' & '.join(fr(x) for x in A[i_])+f' & {wt[i_]:.3f} \\\\')
open(R+'tables/ahp_matrix.tex','w').write('\n'.join(rows))
rows=[]
for j in order:
    rows.append(alts1[j]+' & '+' & '.join('%d'%x for x in S[j])+f' & {score[j]:.2f} & {int(np.where(order==j)[0][0])+1} \\\\')
open(R+'tables/ahp_scores.tex','w').write('\n'.join(rows))
rows=[]
for j in order:
    rows.append(alts1[j]+f' & {100*p1[j]:.1f}\\% & {meanrank[j]:.2f} & {100*p1b[j]:.1f}\\% \\\\')
open(R+'tables/ahp_sens.tex','w').write('\n'.join(rows))

# figura: pesos + puntaje apilado + P(rank1)
fig,ax=plt.subplots(1,2,figsize=(7.2,3.2),gridspec_kw={'width_ratios':[1,1.5]})
ordw=np.argsort(wt)
ax[0].barh([crit1[i] for i in ordw],wt[ordw]*100,color='#2a78d6',height=.6)
for y,i in enumerate(ordw): ax[0].text(wt[i]*100+.6,y,f'{wt[i]*100:.1f}%',va='center',color=INK,fontsize=8.5)
ax[0].set_xlim(0,45); ax[0].set_xlabel('Peso AHP (%)'); ax[0].grid(axis='y',visible=False)
shades=['#cfe0f5','#9cc3ee','#5b9be3','#2a78d6','#1c4f94']
left=np.zeros(5)
alts_o=[alts1[j] for j in order][::-1]
for c in range(5):
    vals=np.array([S[j,c]*wt[c] for j in order])[::-1]
    ax[1].barh(alts_o,vals,left=left,color=shades[c],height=.6,edgecolor='white',linewidth=1.2,label=crit1[c])
    left+=vals
for y,j in enumerate(order[::-1]): ax[1].text(left[y]+.04,y,f'{score[j]:.2f}',va='center',color=INK,fontsize=8.5,fontweight='bold')
ax[1].set_xlim(0,5); ax[1].set_xlabel('Puntaje ponderado (1–5)'); ax[1].grid(axis='y',visible=False)
ax[1].legend(frameon=False,fontsize=7,ncol=3,loc='lower center',bbox_to_anchor=(.4,1.0))
fig.tight_layout(); fig.savefig(R+'img/ahp_resultados.png'); plt.close(fig)

fig,ax=plt.subplots(figsize=(5.4,2.6))
y=np.arange(5)[::-1]
ax.barh(y+.18,p1[order]*100,.34,color='#2a78d6',label='Pesos aleatorios (Dirichlet, 20 000)')
ax.barh(y-.18,p1b[order]*100,.34,color='#9cc3ee',label='Puntajes con ruido ±1 (20 000)')
ax.set_yticks(y); ax.set_yticklabels([alts1[j] for j in order]); ax.set_xlabel('Probabilidad de quedar en 1.er lugar (%)')
for yy,j in zip(y,order):
    ax.text(p1[j]*100+1,yy+.18,f'{100*p1[j]:.0f}%',va='center',fontsize=8,color=INK)
    ax.text(p1b[j]*100+1,yy-.18,f'{100*p1b[j]:.0f}%',va='center',fontsize=8,color=INK)
ax.set_xlim(0,105); ax.grid(axis='y',visible=False); ax.legend(frameon=False,fontsize=7.5,loc='lower right')
fig.savefig(R+'img/ahp_sensibilidad.png'); plt.close(fig)

# datos públicos: universitarios en Arequipa
fig,ax=plt.subplots(figsize=(5.4,1.5))
tot=94870; ext=28461; loc=tot-ext
ax.barh([0],[loc],color='#9cc3ee',height=.5,label=f'Residentes de Arequipa: {loc:,}')
ax.barh([0],[ext],left=[loc],color='#e87ba4' if False else '#eb6834',height=.5,label=f'De otras provincias/regiones: {ext:,} (30%)')
ax.set_yticks([]); ax.set_xlim(0,tot); ax.set_xlabel('Universitarios matriculados en Arequipa (total 94 870)')
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,p:f'{int(x/1000)} mil'))
ax.grid(axis='y',visible=False); ax.legend(frameon=False,fontsize=8,loc='upper center',bbox_to_anchor=(.5,1.5),ncol=1)
fig.savefig(R+'img/dato_universitarios.png'); plt.close(fig)
