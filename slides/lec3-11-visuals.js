/* Lectures 3–11: editable timelines and source-based teaching widgets. */
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

  function widget(host) {
    const same=host.dataset.mode==='duration';
    host.innerHTML=`<div><label>Yield (%) <input name="yield" type="number" min="0.5" max="15" step="0.25" value="6"></label><label>${same?'Target modified duration':'Maturity (years)'} <input name="term" type="number" min="1" max="${same?30:40}" step="${same?.25:1}" value="${same?8:10}"></label><label>Coupon: <b class="coupon-label"></b><input name="coupon" type="range" min="0" max="12" step="0.25" value="${same?4:2}"></label><div class="metrics"></div></div><div class="graph"></div>`;
    const p=(c,n,y)=>bond(c,y,n,100);
    function metrics(c,n,y) {
      let v=0,wt=0,cv=0;
      for(let t=1;t<=n;t++){const cf=c+(t===n?100:0),pv=cf/(1+y)**t;v+=pv;wt+=t*pv;cv+=t*(t+1)*pv/(1+y)**2;}
      return {p:v,dm:wt/v,d:wt/v/(1+y),c:cv/v};
    }
    function render(){
      const y=Number(host.querySelector('[name=yield]').value)/100,c=Number(host.querySelector('[name=coupon]').value),term=Number(host.querySelector('[name=term]').value);
      if(!Number.isFinite(y)||y<.005||y>.15||!Number.isFinite(term)||term<1||term>(same?30:40))return;
      let n=Math.round(term);
      if(same){let best=Infinity;for(let j=1;j<=80;j++){let e=Math.abs(metrics(c,j,y).d-term);if(e<best){best=e;n=j;}}}
      const m=metrics(c,n,y);host.querySelector('.coupon-label').textContent=c.toFixed(2)+'%';
      host.querySelector('.metrics').innerHTML=`Maturity: <b>${n} years</b><br>Price: <b>${m.p.toFixed(2)}</b><br>Macaulay: <b>${m.dm.toFixed(2)}</b><br>Modified: <b>${m.d.toFixed(2)}</b><br>Convexity: <b>${m.c.toFixed(2)}</b>`;
      const graph=host.querySelector('.graph');graph.innerHTML='';const svg=svgFor(graph,950,510,'Bond price versus annual yield');
      const pts=Array.from({length:141},(_,i)=>[1+i*13/140,p(c,n,(1+i*13/140)/100)]);
      const lo=Math.min(...pts.map(x=>x[1]))*.9,hi=Math.max(...pts.map(x=>x[1]))*1.05;
      const X=x=>90+(x-1)*800/13,Y=v=>420-(v-lo)*370/(hi-lo);
      for(let i=0;i<=4;i++){let v=lo+(hi-lo)*i/4;line(svg,90,Y(v),890,Y(v),{stroke:'#d5dccc'});label(svg,75,Y(v)+7,v.toFixed(0),{'text-anchor':'end','font-size':23});}
      for(let x=2;x<=14;x+=2)label(svg,X(x),457,x+'%',{'font-size':23});
      svg.append(node('path',{d:pts.map(([x,v],i)=>`${i?'L':'M'}${X(x)},${Y(v)}`).join(' '),fill:'none',stroke:colors[0],'stroke-width':4}));
      if(y>=.01&&y<=.14)svg.append(node('circle',{cx:X(y*100),cy:Y(m.p),r:7,fill:colors[1]}));
      label(svg,90,27,'Price per $100 par',{'text-anchor':'start','font-size':25});label(svg,500,498,'Annual yield to maturity',{'font-size':25});
    }
    host.querySelectorAll('input').forEach(x=>x.addEventListener('input',render));render();
  }
  document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('.cash-timeline').forEach(timeline);document.querySelectorAll('.visual-widget').forEach(widget);});
})();
