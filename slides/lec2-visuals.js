/* Lecture 2: editable cash-flow timelines, formula-based charts and calculators. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const colors = ['#214b3e', '#a36d22', '#517fa0'];
  function node(tag, attrs = {}, text = '') {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k,v]) => el.setAttribute(k, v));
    if (text) el.textContent = text;
    return el;
  }
  function svgFor(host, w, h, title) {
    const svg = node('svg', {viewBox:`0 0 ${w} ${h}`, role:'img', 'aria-label':title});
    svg.append(node('title', {}, title)); host.append(svg); return svg;
  }
  function label(svg,x,y,text,opts={}) {
    svg.append(node('text',{x,y,fill:'#183b32','font-family':'Avenir Next, Segoe UI, sans-serif','font-size':26,'text-anchor':'middle',...opts},text));
  }
  function line(svg,x1,y1,x2,y2,opts={}) {
    svg.append(node('line',{x1,y1,x2,y2,stroke:'#809586','stroke-width':2,...opts}));
  }
  function bond(c,r,n,f=1000) {
    if (r <= -1) return Infinity;
    const annuity = Math.abs(r) < 1e-10 ? n : -Math.expm1(-n*Math.log1p(r))/r;
    return c*annuity+f*Math.exp(-n*Math.log1p(r));
  }
  function timeline(host) {
    const times=JSON.parse(host.dataset.times), flows=JSON.parse(host.dataset.flows);
    const svg=svgFor(host,1360,230,host.dataset.label || 'Cash-flow timeline');
    line(svg,80,120,1280,120,{'stroke-width':4});
    times.forEach((t,i)=>{
      const positions=host.dataset.positions ? JSON.parse(host.dataset.positions) : times.map((_,j)=>j);
      const x=100+(positions[i]-positions[0])*1160/(positions[positions.length-1]-positions[0] || 1);
      line(svg,x,109,x,131,{'stroke-width':3});
      label(svg,x,175,t);label(svg,x,70,flows[i],{'font-size':29,fill:i===0?'#a36d22':'#214b3e','font-weight':600});
      if(flows[i]) line(svg,x,90,x,111);
    });
    if(host.dataset.caption) label(svg,680,221,host.dataset.caption,{'font-size':23,fill:'#41694e'});
  }
  function chart(host) {
    const kind=host.dataset.kind;
    const svg=svgFor(host,1320,['wealth','collateral'].includes(kind)?460:510,host.dataset.label || kind);
    const left=110,right=1270,top=30,bottom=350;
    let series=[],xmin=0,xmax=1,ymin=0,ymax=1,xticks=[],yticks=[],xlabel='',ylabel='',fmt=x=>String(x);
    const seq=(a,b,n=180)=>Array.from({length:n+1},(_,i)=>a+(b-a)*i/n);
    if(kind==='convexity') {
      xmin=1;xmax=12;ymin=0;ymax=1100;xticks=[1,2,4,6,8,10,12];yticks=[0,250,500,750,1000];xlabel='Required annual yield (%)';ylabel='Price ($)';
      series=[{name:'20-year bond · $10 annual coupon · $1,000 face',points:seq(1,12).map(y=>[y,bond(10,y/100,20)])}];
      [.025,.07,.11].forEach(y=>{
        const p=bond(10,y,20),d=(bond(10,y+.00001,20)-bond(10,y-.00001,20))/.00002;
        series.push({dash:true,points:[[Math.max(.01,y-.015)*100,p+d*(Math.max(.01,y-.015)-y)],[Math.min(.12,y+.015)*100,p+d*(Math.min(.12,y+.015)-y)]]});
      });
    } else if(kind==='pull') {
      xmin=0;xmax=20;ymin=800;ymax=1250;xticks=[0,5,10,15,20];yticks=[800,900,1000,1100,1200];xlabel='Years elapsed → maturity at year 20';ylabel='Price ($)';
      series=[{name:'8% yield · premium',points:seq(0,20,20).map(t=>[t,bond(100,.08,20-t)])},{name:'12% yield · discount',points:seq(0,20,20).map(t=>[t,bond(100,.12,20-t)])},{name:'10% yield · par',dash:true,points:[[0,1000],[20,1000]]}];
    } else if(kind==='coupons') {
      xmin=0;xmax=14;ymin=0;ymax=15;xticks=[0,3,5,7,10,12,14];yticks=[0,3,6,9,12,15];xlabel='Reference rate (%)';ylabel='Annual coupon (%)';
      series=[{name:'Floater: reference + 0.40%',points:seq(0,14).map(x=>[x,x+.4])},{name:'Inverse: max(12% − reference, 0)',points:seq(0,14).map(x=>[x,Math.max(12-x,0)])}];
    } else if(kind==='wealth') {
      const values=JSON.parse(host.dataset.values), names=JSON.parse(host.dataset.names);
      const total=values.reduce((a,b)=>a+b,0);let x=left;
      values.forEach((v,i)=>{const w=(right-left)*v/total;svg.append(node('rect',{x,y:110,width:w,height:120,fill:colors[i]}));label(svg,x+w/2,180,`$${v.toFixed(2)}m`,{fill:'#fffdf5','font-size':30,'font-weight':600});label(svg,x+w/2,280,names[i],{'font-size':23});x+=w;});
      label(svg,690,355,`Terminal wealth = $${total.toFixed(2)} million`,{'font-size':32,'font-weight':600});return;
    } else if(kind==='collateral') {
      [['SOFR = 5%',3.3,2.7],['SOFR = 7%',4.5,1.5]].forEach(([name,f,i],j)=>{const y=70+j*175;label(svg,105,y+50,name,{'font-size':25});const start=250,width=1000;[[f,colors[0],'Floater'],[i,colors[1],'Inverse']].forEach(([v,col,title],k)=>{const x=start+(k?width*f/6:0),w=width*v/6;svg.append(node('rect',{x,y,width:w,height:95,fill:col}));label(svg,x+w/2,y+56,`${title}: $${v.toFixed(2)}m`,{fill:'#fffdf5','font-size':27});});});label(svg,750,423,'Fixed collateral income: $6 million per year in both cases',{'font-size':27});return;
    } else return;
    const X=x=>left+(x-xmin)/(xmax-xmin)*(right-left),Y=y=>bottom-(y-ymin)/(ymax-ymin)*(bottom-top);
    yticks.forEach(y=>{line(svg,left,Y(y),right,Y(y),{stroke:'#d5dccc'});label(svg,left-18,Y(y)+8,fmt(y),{'text-anchor':'end','font-size':26});});
    xticks.forEach(x=>{line(svg,X(x),bottom,X(x),bottom+7);label(svg,X(x),bottom+33,String(x),{'font-size':26});});
    line(svg,left,top,left,bottom);line(svg,left,bottom,right,bottom);
    label(svg,left,20,ylabel,{'text-anchor':'start','font-size':26});label(svg,700,493,xlabel,{'font-size':26});
    series.forEach((s,i)=>svg.append(node('path',{d:s.points.map(([x,y],j)=>`${j?'L':'M'}${X(x).toFixed(2)},${Y(y).toFixed(2)}`).join(' '),fill:'none',stroke:s.dash&&kind==='convexity'?colors[1]:colors[i%3],'stroke-width':s.dash?2.5:4.5,...(s.dash?{'stroke-dasharray':'10 7'}:{})})));
    const named=series.filter(s=>s.name);
    named.forEach((s,i)=>{const x=left+i*(right-left)/named.length;line(svg,x,430,x+32,430,{stroke:colors[i%3],'stroke-width':4});label(svg,x+42,437,s.name,{'text-anchor':'start','font-size':26});});
  }
  function setupCalc(form) {
    function update(){
      const read=name=>Number(form.elements.namedItem(name).value);
      const F=read('face'),c=read('coupon')/100,T=read('years'),m=read('freq'),N=T*m;
      const output=form.querySelector('output');
      if(![F,c,T,m,N].every(Number.isFinite)||F<=0||c<0||T<=0||!Number.isInteger(m)||m<1||!Number.isInteger(N)||N>1200){output.textContent='Use positive face and maturity, and a whole number of coupon periods (maximum 1,200).';return;}
      const C=F*c/m;
      if(form.dataset.mode==='price'){
        const y=read('yield')/100;
        if(!Number.isFinite(y)||y/m<=-1){output.textContent='Periodic yield must exceed −100%.';return;}
        output.textContent=`Bond price = $${bond(C,y/m,N,F).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
      }else{
        const P=read('price');if(!Number.isFinite(P)||P<=0){output.textContent='Enter a positive bond price.';return;}
        let lo=-.999,hi=1;
        while(bond(C,hi,N,F)>P && hi<1e6) hi*=2;
        if(bond(C,hi,N,F)>P){output.textContent='Yield is outside the solver range.';return;}
        for(let i=0;i<160;i++){const mid=(lo+hi)/2;if(bond(C,mid,N,F)>P)lo=mid;else hi=mid;}
        const r=(lo+hi)/2;
        output.textContent=`Nominal annual YTM = ${(r*m*100).toFixed(3)}% · Effective annual yield = ${(Math.expm1(m*Math.log1p(r))*100).toFixed(3)}%`;
      }
    }
    form.addEventListener('input',update);form.addEventListener('submit',e=>e.preventDefault());update();
  }
  function init(){document.querySelectorAll('.cash-timeline').forEach(timeline);document.querySelectorAll('.lec2-chart').forEach(chart);document.querySelectorAll('.calc-form').forEach(setupCalc);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
