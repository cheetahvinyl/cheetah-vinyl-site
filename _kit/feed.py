"""Génère feed.xml (RSS 2.0) à partir des cartes Histoires + Cheetah Africa de l'accueil.
Usage : python3 _kit/feed.py  (depuis la racine du site). Ajoute aussi le lien <link rel=alternate> dans index.html."""
import re,os,html,subprocess,datetime,email.utils
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"; os.chdir(ROOT)
s=open("index.html",encoding="utf-8").read()
def strip(x): return html.unescape(re.sub(r"<[^>]+>","",x)).strip()
def fr(x):
    m=re.search(r'<span data-l="fr">(.*?)</span>',x,re.S); return strip(m.group(1)) if m else strip(x)
items=[]
for sec in ("histoires","africa"):
    part=s[s.index(f'id="{sec}"'):]; part=part[:part.index("</section>")]
    for href,body in re.findall(r'<a class="story[^"]*" href="([^"]+)">(.*?)</a>',part,re.S):
        if href.startswith("http") or not os.path.exists(href): continue
        who=strip(re.search(r'<div class="who">(.*?)</div>',body,re.S).group(1))
        meta=re.search(r'<div class="meta">(.*?)</div>',body,re.S); meta=fr(meta.group(1)) if meta else ""
        hook=re.search(r'<p class="hook">(.*?)</p>',body,re.S); hook=fr(hook.group(1)) if hook else ""
        img=re.search(r'<img src="([^"]+)"',body)
        d=subprocess.run(["git","log","--diff-filter=A","--format=%cI","--",href],capture_output=True,text=True).stdout.strip().splitlines()
        dt=datetime.datetime.fromisoformat(d[-1]) if d else datetime.datetime.now(datetime.timezone.utc)
        items.append((dt,href,f"{who} – {meta.split(' · ')[0]}",hook,img.group(1) if img else None,"Cheetah Africa" if sec=="africa" else "Histoires"))
items.sort(key=lambda x:x[0],reverse=True)
E=html.escape; out=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/"><channel>',
 '<title>cheetah vinyl · Un disque, une histoire</title><link>https://cheetahvinyl.com/</link>',
 '<atom:link href="https://cheetahvinyl.com/feed.xml" rel="self" type="application/rss+xml"/>',
 '<description>Les histoires cachées derrière les disques soul, funk, disco, boogie et africains.</description><language>fr</language>']
for dt,href,t,h,img,cat in items[:60]:
    u="https://cheetahvinyl.com/"+href
    out.append(f'<item><title>{E(t)}</title><link>{u}</link><guid>{u}</guid><category>{cat}</category><pubDate>{email.utils.format_datetime(dt)}</pubDate><description>{E(h)}</description>'+(f'<media:content url="https://cheetahvinyl.com/{img}" medium="image"/>' if img else '')+'</item>')
out.append('</channel></rss>'); open("feed.xml","w",encoding="utf-8").write("\n".join(out))
tag='<link rel="alternate" type="application/rss+xml" title="cheetah vinyl" href="https://cheetahvinyl.com/feed.xml">'
if tag not in s: s=s.replace("</head>",tag+"\n</head>",1); open("index.html","w",encoding="utf-8").write(s)
print("feed.xml :",len(items),"histoires")
