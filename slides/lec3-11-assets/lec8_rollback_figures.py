"""Focused, editable SVG lattices for the Lecture 8 rollback slides."""
from pathlib import Path
from html import escape
OUT = Path(__file__).parent

def draw(name, left, right, edges, active_right=False):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 230" role="img">',f'<title>{escape(name)}: gold nodes are the current step; blue nodes supply next-period values</title>']
    def positions(n): return [115] if n==1 else ([65,165] if n==2 else ([35,115,195] if n==3 else [25,85,145,205]))
    ly,ry=positions(len(left)),positions(len(right))
    for i,j in edges: parts.append(f'<path d="M 295 {ly[i]} L 705 {ry[j]}" stroke="#809586" stroke-width="2" fill="none"/>')
    if edges and name not in ('call', 'put-decision'): parts.append('<path d="M 600 12 H 400 l 12 -6 M 400 12 l 12 6" stroke="#936724" stroke-width="3" fill="none"/><text x="500" y="38" text-anchor="middle" font-size="17" fill="#936724">work backward</text>')
    for side,nodes,ys in [(0,left,ly),(1,right,ry)]:
        for lines,y in zip(nodes,ys):
            current=(side==1 if active_right else side==0)
            x=165 if side==0 else 835
            height=22*len(lines)+12
            parts.append(f'<rect x="{x-130}" y="{y-height/2}" width="260" height="{height}" rx="9" fill="{"#fff0ce" if current else "#e8f1fa"}" stroke="{"#936724" if current else "#809586"}" stroke-width="{3 if current else 1.5}"/>')
            for k,line in enumerate(lines): parts.append(f'<text x="{x}" y="{y+(k-(len(lines)-1)/2)*22+7}" text-anchor="middle" font-family="Arial,sans-serif" font-size="21" fill="#214b3e">{escape(line)}</text>')
    parts.append('</svg>');(OUT/f'lec8-rollback-{name}.svg').write_text('\n'.join(parts)+'\n')

if __name__=='__main__':
    draw('terminal', [['Year 2 · r = 4%'],['Year 2 · r = 8%'],['Year 2 · r = 12%']], [['Year 3 · 108']]*4, [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)], True)
    draw('year2',[['Year 2 · r = 4%','H = 111.8462'],['Year 2 · r = 8%','H = 108.0000'],['Year 2 · r = 12%','H = 104.4286']],[['Year 3 · 108']]*4,[(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)])
    draw('call',[['4% · Call','V = 108.0000'],['8% · Indifferent','V = 108.0000'],['12% · Continue','V = 104.4286']],[['Hold = 111.8462'],['Hold = 108.0000'],['Hold = 104.4286']],[(0,0),(1,1),(2,2)])
    for name,low,vals in [('straight','112.6886',['111.8462','108.0000','104.4286']),('callable','110.8571',['108.0000','108.0000','104.4286'])]:
        draw(name, [['Year 1 · r = 5%',f'V = {low}'],['Year 1 · r = 9%','V = 105.4443']],[[f'Year 2 · {v}'] for v in vals],[(0,0),(0,1),(1,1),(1,2)])
    draw('today',[['Today · r = 6%','Straight = 110.8929','Callable = 110.0290']],[['Year 1 · r = 5%','S = 112.6886','C = 110.8571'],['Year 1 · r = 9%','S = C = 105.4443']],[(0,0),(0,1)])

    draw('put-terminal', [['Year 1 · r = 4%'],['Year 1 · r = 12%']], [['Year 2 · 105']]*3, [(0,0),(0,1),(1,1),(1,2)], True)
    draw('put-hold', [['Year 1 · r = 4%','H = 105.9615'],['Year 1 · r = 12%','H = 98.7500']], [['Year 2 · 105']]*3, [(0,0),(0,1),(1,1),(1,2)])
    draw('put-decision', [['4% · Keep bond','V = 105.9615'],['12% · Exercise put','V = 100.0000']], [['Hold = 105.9615'],['Hold = 98.7500']], [(0,0),(1,1)])
    draw('put-today', [['Today · r = 6%','V = 102.1517']], [['Year 1 · Keep bond','V = 105.9615'],['Year 1 · Exercise put','V = 100.0000']], [(0,0),(0,1)])

    parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 230" role="img"><title>Putable bond setup: today at 6 percent, year one at 4 or 12 percent, and three maturity states paying 105</title>']
    nodes=[(120,115,'Today · r = 6%'),(500,65,'Year 1 · r = 4%'),(500,165,'Year 1 · r = 12%'),(880,35,'Year 2 · 105'),(880,115,'Year 2 · 105'),(880,195,'Year 2 · 105')]
    for i,j in [(0,1),(0,2),(1,3),(1,4),(2,4),(2,5)]:
        x,y,_=nodes[i];u,v,_=nodes[j];parts.append(f'<path d="M {x} {y} L {u} {v}" stroke="#809586" stroke-width="2"/>')
    for x,y,label in nodes:
        parts.append(f'<rect x="{x-115}" y="{y-24}" width="230" height="48" rx="9" fill="#e8f1fa" stroke="#809586"/><text x="{x}" y="{y+7}" text-anchor="middle" font-family="Arial,sans-serif" font-size="21" fill="#214b3e">{label}</text>')
    parts.append('</svg>');(OUT/'lec8-rollback-put-setup.svg').write_text('\n'.join(parts)+'\n')
