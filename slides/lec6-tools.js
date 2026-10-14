/* Lecture 6 teaching tools: local calculations, fixed illustrative inputs. */
(() => {
  'use strict';
  const sqrt = x => Math.sqrt(Math.max(0, x));
  const fmt = (x, n = 2) => Number(x).toFixed(n);
  const ns = 'http://www.w3.org/2000/svg';
  const colors = ['#41694e', '#936724', '#486d8c', '#865c76', '#777777'];
  function chart(svg, names, values, unit) {
    svg.replaceChildren();
    const add = (tag, attrs, content = '') => {
      const node = document.createElementNS(ns, tag);
      Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
      node.textContent = content; svg.appendChild(node);
    };
    const lo = Math.min(0, ...values), hi = Math.max(0, ...values);
    const span = Math.max(hi - lo, 0.01), left = 260, width = 680;
    const X = x => left + (x - lo) / span * width;
    svg.setAttribute('viewBox', '0 0 1200 280');
    add('line', { x1: X(0), y1: 15, x2: X(0), y2: 245, stroke: '#879b86' });
    names.forEach((name, i) => {
      const y = 30 + i * 210 / Math.max(names.length, 1);
      add('text', { x: left - 12, y: y + 22, 'text-anchor': 'end', 'font-size': 25, fill: '#183b32' }, name);
      add('rect', { x: Math.min(X(0), X(values[i])), y, width: Math.abs(X(values[i]) - X(0)), height: 28, fill: colors[i % colors.length] });
      add('text', { x: 1190, y: y + 22, 'text-anchor': 'end', 'font-size': 25, fill: '#183b32' }, fmt(values[i]) + ' ' + unit);
    });
  }
  function initialize(root) {
    const kind = root.dataset.tool;
    const controls = root.querySelector('.lec6-controls');
    const result = root.querySelector('.lec6-results');
    const svg = root.querySelector('svg');
    const hint = root.querySelector('.lec6-hint');
    const fields = {};
    controls.addEventListener('keydown', event => {
      if (/^(Arrow|Home|End|PageUp|PageDown|Enter| )/.test(event.key)) event.stopPropagation();
    });
    const number = (key, label, min, max, step, initial, unit = '', type = 'range') => {
      const wrap = document.createElement('label');
      const title = document.createElement('span');
      const input = document.createElement('input');
      input.id = root.id + '-' + key; input.type = type;
      input.min = min; input.max = max; input.step = step; input.value = initial;
      input.defaultValue = initial; input.setAttribute('aria-label', label);
      wrap.htmlFor = input.id;
      wrap.append(title, input); controls.append(wrap);
      fields[key] = input;
      const updateTitle = () => { title.textContent = label + ': ' + input.value + (unit ? ' ' + unit : ''); };
      input.addEventListener('input', updateTitle); updateTitle();
      input.refreshTitle = updateTitle;
    };
    const select = (key, label, options) => {
      const wrap = document.createElement('label'); wrap.textContent = label;
      const input = document.createElement('select'); input.id = root.id + '-' + key;
      input.setAttribute('aria-label', label);
      options.forEach(name => { const option = document.createElement('option'); option.textContent = name; input.append(option); });
      wrap.htmlFor = input.id; wrap.append(input); controls.append(wrap); fields[key] = input;
    };
    const v = key => Number(fields[key].value);
    const report = pairs => {
      result.replaceChildren();
      pairs.forEach(([label, value]) => {
        const span = document.createElement('span'), strong = document.createElement('strong');
        span.append(label + ': '); strong.textContent = value; span.append(strong); result.append(span);
      });
    };
    let update;
    if (kind === 'historical') {
      select('sample', 'Monthly active-return sample', ['Six-month mandate', 'Portfolio A', 'Portfolio B', 'Constant +10 bp']);
      number('offset', 'Add to every observation', -100, 100, 5, 0, 'bp');
      number('scale', 'Multiply deviations', 0, 2, .1, 1, '×');
      const samples = [[12,-8,5,22,-18,4],[-2,4,4,7,-5,-3,8,3,-7,5,4,-26],[101,59,37,47,68,27,112,3,141,90,109,4],Array(6).fill(10)];
      update = () => {
        const base = samples[fields.sample.selectedIndex], mean = base.reduce((a,b) => a+b,0)/base.length;
        const values = base.map(x => mean + v('scale') * (x-mean) + v('offset'));
        const avg = values.reduce((a,b) => a+b,0)/values.length;
        const te = sqrt(values.reduce((s,x) => s+(x-avg)**2,0)/(values.length-1));
        report([['Mean active return',fmt(avg)+' bp/month'],['Monthly sample TE',fmt(te)+' bp'],['Annualized TE',fmt(te*Math.sqrt(12))+' bp']]);
        chart(svg,['Mean active return','Monthly TE','Annual TE'],[avg,te,te*Math.sqrt(12)],'bp');
        hint.textContent = 'Shift the mean: TE stays fixed. Scale deviations: TE changes. A constant excess return has zero historical TE.';
      };
    } else if (kind === 'cells') {
      number('tilt', 'Treasury → BBB credit', -5, 5, .5, 2, 'percentage points');
      number('issuers', 'Issuers in the 20% cell', 1, 40, 1, 4);
      update = () => {
        const tilt = v('tilt'), issuers = v('issuers');
        report([['Treasury cell',fmt(18-tilt)+'%'],['BBB cell',fmt(10+tilt)+'%'],['Issuer weight in 20% cell',fmt(20/issuers)+'%'],['Active weights sum', '0.00 pp']]);
        chart(svg,['Treasury active','BBB credit active'],[-tilt,tilt],'pp');
        hint.textContent = 'The 72-cell example shifts weight between two cells; all other weights stay fixed. The separate 20% issuer example isolates concentration.';
      };
    } else if (kind === 'factor') {
      number('rate', 'Active Treasury duration', -1, 1, .05, .2, 'years');
      number('credit', 'Active IG spread duration', -1, 1, .05, .6, 'years');
      number('rho', 'Rate / IG shock correlation', -1, 1, .05, 0);
      number('idio', 'Independent residual TE', 0, 20, 1, 8, 'bp/month');
      update = () => {
        const a = -v('rate')*30, b = -v('credit')*18;
        const fixed = 2.5**2+5.25**2+4**2;
        const systematic = sqrt(a*a+b*b+2*v('rho')*a*b+fixed);
        const total = sqrt(systematic**2+v('idio')**2);
        report([['Systematic TE',fmt(systematic)+' bp/month'],['Total TE',fmt(total)+' bp/month'],['Annualized total',fmt(total*Math.sqrt(12))+' bp']]);
        chart(svg,['Treasury isolated','IG spread isolated','Systematic TE','Total TE'],[Math.abs(a),Math.abs(b),systematic,total],'bp');
        hint.textContent = 'Other isolated risks stay at 2.5, 5.25 and 4 bp and are independent. Covariance retains signed exposures; flip one exposure and compare correlations.';
      };
    } else if (kind === 'correlation') {
      number('rho', 'Active-return correlation', -1, 1, .05, 0);
      update = () => {
        const te = sqrt(6**2+10.8**2+2*v('rho')*6*10.8);
        report([['Treasury isolated TE','6.00 bp'],['Credit isolated TE','10.80 bp'],['Combined monthly TE',fmt(te)+' bp']]);
        chart(svg,['Treasury','Credit','Combined'],[6,10.8,te],'bp');
        hint.textContent = 'Only two factors here. This correlation is between signed active-return contributions, not necessarily the raw yield and spread shocks.';
      };
    } else if (kind === 'curve') {
      [2,5,10,30].forEach((tenor,i) => number('k'+tenor,tenor+'Y yield shock',-100,100,5,[-20,0,40,0][i],'bp'));
      update = () => {
        const active = [-.3,.05,.4,-.15], names = ['2Y','5Y','10Y','30Y'];
        const impacts = names.map((name,i) => -active[i]*v('k'+name.slice(0,-1)));
        report([['Active total duration','0.00 years'],['Active scenario return',fmt(impacts.reduce((a,b)=>a+b,0))+' bp']]);
        chart(svg,names,impacts,'bp'); hint.textContent = 'Default: −22 bp despite matched total duration. Set all four shocks to +40 bp: first-order active return becomes zero.';
      };
    } else if (kind === 'scenario') {
      const names = ['Treasury level','2Y key rate','10Y key rate','IG spread','Securitized spread'];
      names.forEach((name,i)=>number('s'+i,name,-100,100,5,[40,20,50,25,15][i],'bp'));
      update = () => {
        const active = [.2,-.1,.15,.6,-.25], impacts = active.map((x,i)=>-x*v('s'+i));
        report([['Active scenario return',fmt(impacts.reduce((a,b)=>a+b,0))+' bp']]); chart(svg,names,impacts,'bp');
        hint.textContent = 'Each shock is an independent model factor. The level shock must not be counted again as a parallel move in the key-rate shocks.';
      };
    } else if (kind === 'toy') {
      const names = ['Treasury 5Y','Treasury 10Y','Agency MBS','A industrial','BBB financial'];
      names.forEach((name,i)=>number('w'+i,name,0,100,1,[25,15,25,20,15][i],'%', 'number'));
      update = () => {
        const raw = names.map((_,i)=>v('w'+i));
        if (raw.some(x=>!Number.isFinite(x)||x<0||x>100)||Math.abs(raw.reduce((a,b)=>a+b,0)-100)>1e-8) {
          report([['Weights','Enter 0–100% per bond, summing to 100%']]);svg.replaceChildren();hint.textContent='No exposures are reported for an invalid portfolio.';return;
        }
        const w=raw.map(x=>x/100), dot=a=>a.reduce((s,x,i)=>s+x*w[i],0);
        const d=dot([4.6,8.2,4.1,5.7,6.1]), sd=dot([0,0,3.2,5.4,5.8]), yieldPct=dot([4.3,4.6,5.1,5.4,6]);
        const treasury=raw[0]+raw[1], credit=raw[3]+raw[4];
        report([['Duration',fmt(d)+' years'],['Spread duration',fmt(sd)+' years'],['Weighted yield proxy',fmt(yieldPct)+'%'],['Sector limits',treasury>=30&&credit<=40?'PASS':'BREACH']]);
        chart(svg,['Treasury','MBS','Corporate'],[treasury,raw[2],credit],'%');
        hint.textContent='Targets: duration near 5, spread duration near 3; Treasury ≥30%, corporate ≤40%. This is a manual allocation tool; it does not run an optimizer.';
      };
    } else if (kind === 'rebalance') {
      number('trades','Number of trades',0,20,1,5);
      update = () => {
        const n=v('trades'), after=12-4*(1-Math.exp(-n/5)), cost=1.2*n+.04*n*n;
        report([['Predicted TE after trades',fmt(after)+' bp/month'],['TE reduction',fmt(12-after)+' bp/month'],['One-time cost',fmt(cost)+' bp'],['Cost on $100m','$'+fmt(cost*10000,0)]]);
        chart(svg,['TE before','TE after','One-time cost'],[12,after,cost],'bp');
        hint.textContent='These illustrative curves are from the notes. A one-time cost and monthly return dispersion are different quantities; their ratio is not a payback period.';
      };
    } else if (kind === 'demo' || kind === 'demo-credit') {
      const data = JSON.parse(document.getElementById('lec6-demo-data').textContent);
      if (kind === 'demo') {
        number('rate','Parallel Treasury shock',-150,150,5,50,'bp');
        number('spread','Corporate spread shock',-50,200,5,25,'bp');
      } else { number('spread','Corporate spread shock',-50,200,5,0,'bp'); }
      select('plan','Corporate-sector cap',['45% cap','35% cap']);
      update = () => {
        const rate=kind==='demo'?v('rate')/10000:0, spread=v('spread')/10000;
        const plan=fields.plan.selectedIndex===0?'Optimized':'35% cap';
        const names=['Current','Cell sampled',plan], portfolios=names.map(name=>data.portfolios[name]);
        const impacts=portfolios.map(p=>data.value*(-p.duration*rate+.5*p.convexity*rate**2-p.spread*spread)/1e6);
        const chosen=portfolios[2];
        report([['Optimized corporate',fmt(chosen.corporate)+'%'],['Annual predicted TE',fmt(chosen.te)+' bp'],['Implementation cost','$'+fmt(chosen.cost,0)]]);
        chart(svg,names,impacts,'$m');
        hint.textContent='Exact portfolio weights from the existing demo. Gross instantaneous P&L excludes carry and costs; agency spreads move ¼ of corporate spreads. Changing the cap selects a precomputed optimized plan.';
      };
    } else { throw new Error('Unknown Lecture 6 tool: '+kind); }
    const reset=document.createElement('button');reset.type='button';reset.textContent='Reset example';controls.append(reset);
    Object.values(fields).forEach(input=>{input.addEventListener('input',update);input.addEventListener('change',update);});
    reset.addEventListener('click',()=>{
      Object.values(fields).forEach(input=>{if(input.tagName==='SELECT')input.selectedIndex=0;else{input.value=input.defaultValue;input.refreshTitle();}});update();
    });
    update();
  }
  const start=()=>document.querySelectorAll('.lec6-lab[data-tool]').forEach(initialize);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
