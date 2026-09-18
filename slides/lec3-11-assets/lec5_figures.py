"""Illustrative default/recovery values reproduced from Lecture 5 notes."""
from build_figures import *
f,aa=plt.subplots(1,2,figsize=(14,5.5))
years=np.arange(1,11)
aa[0].plot(years,[.1,.2,.4,.7,1,1.4,1.8,2.2,2.6,3],color=GREEN,label='Investment grade')
aa[0].plot(years,[2,4.5,7,9.5,12,14,16,18,20,22],color=GOLD,label='High yield')
aa[0].set(xlabel='Years',ylabel='Cumulative default rate (%)',title='Default frequency',ylim=(0,25));aa[0].legend();aa[0].grid(alpha=.2)
x=np.arange(3);aa[1].bar(x,[65,40,25],color=[GREEN,GOLD,BLUE]);aa[1].set(xticks=x,xticklabels=['Senior\nsecured','Senior\nunsecured','Subordinated'],ylabel='Illustrative recovery (%)',title='Recovery after default',ylim=(0,100))
for i,v in enumerate([65,40,25]):aa[1].text(i,v+3,f'{v}%',ha='center')
f.tight_layout();save(f,'lec5-default-recovery')
