"""Rebuild Lecture 3–11 teaching figures from the values and formulas in the notes."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
GREEN, GOLD, BLUE = '#214b3e', '#a36d22', '#517fa0'
plt.rcParams.update({'font.family':'sans-serif','font.size':17,'axes.titlesize':20,'axes.labelsize':18,'legend.fontsize':15,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#809586','axes.labelcolor':GREEN,'text.color':GREEN,'xtick.color':GREEN,'ytick.color':GREEN,'figure.facecolor':'#fffdf5','axes.facecolor':'#fffdf5','svg.fonttype':'none','lines.linewidth':3})

def save(fig, name):
    fig.savefig(OUT / (name+'.svg'), bbox_inches='tight')
    plt.close(fig)

def bond(coupon, years, y, m=1):
    t = np.arange(1,years*m+1)
    cf = np.full(len(t),100*coupon/m); cf[-1]+=100
    pv = cf/(1+np.asarray(y)[...,None]/m)**t
    p = pv.sum(axis=-1)
    d = (pv*t).sum(axis=-1)/p/m/(1+np.asarray(y)/m)
    return p,d

def axis():
    f,a=plt.subplots(figsize=(13,5.4)); a.grid(alpha=.2);return f,a

def lecture3():
    y=np.linspace(.06,.12,200);f,a=axis()
    for j,c in enumerate([.09,.06,0]):
        for n,ls in [(5,'--'),(25,'-')]:
            a.plot(y*100,bond(c,n,y,2)[0],color=[GREEN,GOLD,BLUE][j],ls=ls,label=f'{c:.0%} coupon, {n} years')
    a.set(xlabel='Required nominal annual yield (%)',ylabel='Price per $100 par');a.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.23));save(f,'lec3-six')
    for name,shock in [('local',.0001),('asymmetry',.02)]:
        p0=bond(.06,25,.09,2)[0]; y=np.array([.09-shock,.09,.09+shock]);v=100*(bond(.06,25,y,2)[0]/p0-1)
        f,a=axis();a.bar(['Yield falls','Unchanged','Yield rises'],v,color=[GREEN,BLUE,GOLD]);a.axhline(0,color=GREEN,lw=1)
        for i,x in enumerate(v):a.text(i,x+(max(abs(v))*.06)*(1 if x>=0 else -1),f'{x:+.3f}%',ha='center',va='bottom' if x>=0 else 'top')
        a.set(ylabel='Price change (%)',title=f'25-year 6% coupon bond: equal {shock*10000:.0f} bp shocks from 9%');a.margins(y=.25);save(f,'lec3-'+name)
    f,a=axis(); ns=np.arange(1,101)
    for c,col in [(.01,GREEN),(.02,GOLD)]:a.plot(ns,[bond(c,int(n),.1)[1]*1.1 for n in ns],color=col,label=f'{c:.0%} coupon: Macaulay duration')
    a.plot([1,100],[1,100],ls='--',color=BLUE,label='Zero: Macaulay duration = maturity');a.set(xlabel='Maturity (years)',ylabel='Macaulay duration (years)',ylim=(0,45));a.legend();save(f,'lec3-long-duration')
    y=np.linspace(.02,.12,200);p,d=bond(.06,10,.06);f,a=axis();a.plot(y*100,bond(.06,10,y)[0],color=GREEN,label='Actual price');a.plot(y*100,p-d*p*(y-.06),color=GOLD,ls='--',label='Duration tangent');a.scatter([6],[p],color=BLUE,s=65,zorder=5)
    for z in [.035,.095]:a.vlines(z*100,p-d*p*(z-.06),bond(.06,10,z)[0],color=BLUE,lw=4)
    a.set(xlabel='Annual yield (%)',ylabel='Price per $100 par',title='10-year, 6% annual coupon bond; initial yield 6%');a.legend();save(f,'lec3-tangent')
    y=np.linspace(.015,.105,200);f,a=axis()
    for c,col,lbl in [(90,GOLD,'A: convexity 90'),(260,GREEN,'B: convexity 260')]:a.plot(y*100,100*(1-6*(y-.06)+.5*c*(y-.06)**2),color=col,label=lbl)
    a.scatter([6],[100],color=BLUE);a.set(xlabel='Yield (%)',ylabel='Illustrative price',title='Same initial price 100, yield 6%, and modified duration 6');a.legend();save(f,'lec3-value')
    f,axs=plt.subplots(1,3,figsize=(15,5));t=np.array([2,5,10,30]);base=np.array([3,3.4,3.8,4.2])
    for a,delta,title in zip(axs,[np.ones(4)*.6,np.array([-.4,-.2,.1,.5]),np.array([-.3,.5,.2,-.3])],['Level: parallel rise','Slope: steepening twist','Curvature: middle rises']):
        a.plot(t,base,color=GREEN,label='Initial');a.plot(t,base+delta,color=GOLD,label='After');a.set(title=title,xlabel='Maturity (years)',ylim=(2.5,5),xticks=t);a.grid(alpha=.2)
    axs[0].set_ylabel('Illustrative yield (%)');axs[-1].legend();f.tight_layout();save(f,'lec3-curve-moves')
    A=np.array([1.4,.3,.6,2]);B=np.array([.2,3.5,.5,.1]);f,a=axis();x=np.arange(4)
    a.bar(x-.2,A,.4,color=GREEN,label='A: barbell');a.bar(x+.2,B,.4,color=GOLD,label='B: bullet');a.set(xticks=x,xticklabels=['2Y','5Y','10Y','30Y'],ylabel='Key rate duration');a.legend();save(f,'lec3-krd')
    shocks=np.array([[1,1,1,1],[0,1,0,0],[0,0,0,1],[.25,.5,.75,1]]);f,a=axis()
    a.bar(x-.2,-shocks@A,.4,color=GREEN,label='A: barbell');a.bar(x+.2,-shocks@B,.4,color=GOLD,label='B: bullet');a.set(xticks=x,xticklabels=['Parallel +100 bp','5Y +100 bp','30Y +100 bp','Steepening'],ylabel='Estimated price change (%)');a.legend();save(f,'lec3-krd-loss')

if __name__ == '__main__':
    lecture3()
