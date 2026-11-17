"""Génère search.json (toutes les cartes : Histoires, Cheetah Africa, Machines, Créateurs) et installe la recherche de l'accueil.
Usage : python3 _kit/search.py (depuis la racine du site)."""
import re,os,json,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"; os.chdir(ROOT)
s=open("index.html",encoding="utf-8").read()
def strip(x): return html.unescape(re.sub(r"<[^>]+>"," ",x)).strip()
def lang(x,l):
    m=re.search(rf'<span data-l="{l}">(.*?)</span>',x,re.S); return re.sub(r"\s+"," ",strip(m.group(1))) if m else re.sub(r"\s+"," ",strip(x))
items=[];seen=set()
for sec,lab in (("histoires",["Histoire","Story"]),("africa",["Cheetah Africa","Cheetah Africa"]),("machines",["Machine","Machine"]),("createurs",["Créateur","Creator"])):
    if f'id="{sec}"' not in s: continue
    part=s[s.index(f'id="{sec}"'):]; part=part[:part.index("</section>")]
    for href,body in re.findall(r'<a class="[^"]*" href="([^"#]+\.html)">(.*?)</a>',part,re.S):
        if href in seen or not os.path.exists(href): continue
        seen.add(href)
        who=re.search(r'<div class="who">(.*?)</div>',body,re.S) or re.search(r'<h3[^>]*>(.*?)</h3>',body,re.S)
        meta=re.search(r'<div class="meta">(.*?)</div>',body,re.S); hook=re.search(r'<p class="hook">(.*?)</p>',body,re.S) or re.search(r'<p[^>]*>(.*?)</p>',body,re.S)
        img=re.search(r'<img [^>]*?src="([^"]+)"',body); badge=re.search(r'class="badge">(Nº \d+)',body)
        items.append({"u":href,"i":img.group(1) if img else "","w":lang(who.group(1),"fr") if who else "",
          "t":[lang(meta.group(1),"fr"),lang(meta.group(1),"en")] if meta else ["",""],
          "h":[lang(hook.group(1),"fr"),lang(hook.group(1),"en")] if hook else ["",""],
          "c":lab,"n":badge.group(1) if badge else ""})
json.dump(items,open("search.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
BLOCK='''<!--SEARCH--><section class="srch" id="recherche" role="search" aria-label="Recherche"><label for="q" class="sr"><span data-l="fr">Rechercher</span><span data-l="en">Search</span></label>
<div class="sbox"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg><input id="q" type="search" autocomplete="off" placeholder="Un artiste, un titre, une année… · An artist, a song, a year…"></div>
<div id="qr" class="qr" aria-live="polite"></div></section>
<style>.srch{margin:6px 0 26px}.srch .sr{position:absolute;left:-9999px}.sbox{display:flex;align-items:center;gap:12px;background:var(--card,#fffaf0);border:2px solid var(--green,#1c4630);border-radius:999px;padding:12px 20px}
.sbox svg{width:22px;height:22px;fill:none;stroke:var(--green,#1c4630);stroke-width:2.4;flex:none}.sbox input{border:0;outline:0;background:transparent;font:inherit;font-size:17px;width:100%;color:var(--fg,#16281e)}
.qr{display:grid;gap:10px;margin-top:12px}.qr a{display:grid;grid-template-columns:64px 1fr;gap:14px;align-items:center;text-decoration:none;color:inherit;background:var(--card,#fffaf0);border:1.5px solid var(--line,#e3d6b6);border-radius:16px;padding:10px}
.qr img{width:64px;height:64px;object-fit:cover;border-radius:10px}.qr b{display:block;font-size:17px}.qr small{color:var(--muted,#5b6b5f);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.srch{scroll-margin-top:20px}.qr .tg{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--rust,#c4502a);border-radius:999px;padding:2px 9px;margin-right:6px}
.qr .none{color:var(--muted,#5b6b5f);padding:6px 4px}</style>
<script>(function(){var D=null,q=document.getElementById('q'),r=document.getElementById('qr');
function n(s){return (s||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase()}
function L(){return document.documentElement.getAttribute('lang')==='en'||document.body.classList.contains('en')?1:0}
function e(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function go(){var v=n(q.value.trim());if(v.length<2){r.innerHTML='';return}
 var w=v.split(/\\s+/),o=[];D.forEach(function(x){var hay=n([x.w,x.t[0],x.t[1],x.h[0],x.h[1],x.c[0],x.n].join(' '));
  if(w.every(function(k){return hay.indexOf(k)>-1})){var sc=(n(x.w).indexOf(v)>-1?3:0)+(n(x.t[0]).indexOf(v)>-1?2:0);o.push([sc,x])}});
 o.sort(function(a,b){return b[0]-a[0]});var l=L();
 r.innerHTML=o.length?o.slice(0,12).map(function(p){var x=p[1];return '<a href="'+e(x.u)+'">'+(x.i?'<img src="'+e(x.i)+'" alt="" loading="lazy" width="64" height="64">':'<span></span>')+'<span><span class="tg">'+e(x.n||x.c[l])+'</span><b>'+e(x.w)+'</b><small>'+e(x.t[l]||x.t[0])+(x.h[l]?' · '+e(x.h[l]):'')+'</small></span></a>'}).join('')
  :'<div class="none">'+(l?'No story found. Try another artist or year.':'Aucune histoire trouvée. Essaie un autre artiste ou une année.')+'</div>'}
q.addEventListener('input',function(){if(D)go();else fetch('search.json').then(function(x){return x.json()}).then(function(j){D=j;go()})});
var PH=['Un artiste, un titre, une année…','An artist, a song, a year…'];function ph(){q.placeholder=PH[L()];if(D&&q.value)go()}ph();
document.querySelectorAll('a[href="#recherche"]').forEach(function(a){a.addEventListener('click',function(){setTimeout(function(){q.focus({preventScroll:true})},350)})});
new MutationObserver(ph).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
q.addEventListener('focus',function(){if(!D)fetch('search.json').then(function(x){return x.json()}).then(function(j){D=j})},{once:true});})();</script><!--/SEARCH-->'''
if '<!--SEARCH-->' in s: s=re.sub(r'<!--SEARCH-->.*?<!--/SEARCH-->',lambda m:BLOCK,s,count=1,flags=re.S)
else: s=s.replace('<main class="wrap">','<main class="wrap">\n'+BLOCK,1)
TILE='<a class="xt" href="#recherche"><b><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.6" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></b><span class="xn"><span data-l="fr">Chercher</span><span data-l="en">Search</span></span><span class="xd"><span data-l="fr">Un artiste, un titre, une année</span><span data-l="en">An artist, a song, a year</span></span></a>'
if 'href="#recherche"><b>' not in s:
    s=s.replace('<span data-l="en">Soul, funk, afro news</span></span></a></div></nav>','<span data-l="en">Soul, funk, afro news</span></span></a>'+TILE+'</div></nav>',1)
open("index.html","w",encoding="utf-8").write(s)
print("search.json :",len(items),"fiches")
