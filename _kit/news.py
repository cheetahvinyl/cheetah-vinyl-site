"""Rubrique News de cheetahvinyl.com.
- render_list / render_teaser : HTML des news (utilisés par gen.py).
- En ligne de commande : met à jour directement un clone du site (news.html + index.html)
  à partir de news.json, sans tout régénérer :
      python3 news.py /chemin/news.json /chemin/clone_du_site
  Les blocs sont délimités par <!--NEWS-->…<!--/NEWS--> et <!--NEWSTEASER-->…<!--/NEWSTEASER-->.
"""
import html, json, sys, re, datetime

def L(fr, en): return f'<span data-l="fr">{fr}</span><span data-l="en">{en}</span>'
E = html.escape
MOIS = ['janv.','févr.','mars','avr.','mai','juin','juil.','août','sept.','oct.','nov.','déc.']
MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
TAG = {'africa': ('Afrique', 'Africa'), 'soul': ('Soul · Funk · Disco', 'Soul · Funk · Disco')}

def _d(s):
    d = datetime.date.fromisoformat(s)
    return L(f'{d.day} {MOIS[d.month-1]} {d.year}', f'{MON[d.month-1]} {d.day}, {d.year}')

def load(p):
    items = json.load(open(p, encoding='utf-8'))
    items.sort(key=lambda x: x['date'], reverse=True)   # stable : garde l'ordre du fichier à date égale
    return items[:60]

def card(n, img=''):
    tg = TAG.get(n['cat'], TAG['soul'])
    st = (f' · <a href="{n["story"]}">{L("Lire notre histoire →", "Read our story →")}</a>' if n.get('story') else '')
    return (f'<article class="nw" data-cat="{n["cat"]}"><div class="nw-top"><span class="nw-tag nw-{n["cat"]}">{L(*tg)}</span>'
            f'<time datetime="{n["date"]}">{_d(n["date"])}</time></div>'
            f'<h3>{L(E(n["title_fr"]), E(n["title_en"]))}</h3>'
            f'<p>{L(E(n["text_fr"]), E(n["text_en"]))}</p>'
            f'<p class="nw-src">Source : <a href="{E(n["url"])}" target="_blank" rel="noopener">{E(n["source"])}</a>{st}</p></article>\n')

def render_list(items):
    return '<!--NEWS--><div class="nwlist">\n' + ''.join(card(n) for n in items) + '</div><!--/NEWS-->'

def render_teaser(items):
    top = items[:3]
    li = ''.join(f'<a class="nwt" href="news.html"><span class="nw-tag nw-{n["cat"]}">{L(*TAG.get(n["cat"], TAG["soul"]))}</span>'
                 f'<b>{L(E(n["title_fr"]), E(n["title_en"]))}</b><time datetime="{n["date"]}">{_d(n["date"])}</time></a>' for n in top)
    return f'<!--NEWSTEASER--><div class="nwts">{li}</div><!--/NEWSTEASER-->'

CSS = '''
.nwhero .wrap{grid-template-columns:1fr!important}.nwhero h1{font-size:clamp(44px,8vw,76px)}.nwfilt{margin-top:26px!important}
.mbar a:nth-child(2){border:1.5px solid var(--cream);color:var(--cream)}
.nwfilt{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 22px}
.nwfilt button{font:inherit;font-weight:700;font-size:14px;border-radius:999px;padding:9px 16px;border:1.5px solid var(--green,#1c4630);background:transparent;color:var(--green,#1c4630);cursor:pointer}
.nwfilt button[aria-pressed="true"]{background:var(--green,#1c4630);color:var(--cream)}
.nwlist{display:grid;gap:16px;max-width:820px}
.nw{background:var(--card,#fffaf0);border:1.5px solid rgba(0,0,0,.08);border-radius:18px;padding:20px 22px}
.nw-top{display:flex;justify-content:space-between;align-items:center;gap:10px;font-size:13px;opacity:.85}
.nw-tag{display:inline-block;border-radius:999px;padding:4px 11px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#fff;background:var(--green,#1c4630)}
.nw-tag.nw-africa{background:var(--rust)}
.nw h3{font-size:clamp(21px,2.6vw,26px);line-height:1.2;margin:.5em 0 .35em}
.nw p{margin:.3em 0;line-height:1.55}.nw-src{font-size:14px;opacity:.85}.nw-src a{color:var(--rust);font-weight:600}
.nwband{background:var(--card,#fffaf0);border:2px solid var(--green,#1c4630);border-radius:24px;padding:26px 28px;margin:0 0 28px}
.nwband .row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}
.nwband h2{margin:0;font-size:clamp(28px,4vw,40px)}.nwband .all{color:var(--rust);font-weight:700;text-decoration:none}
.nwts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px}
.nwt{display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit;border-top:2px solid var(--ochre);padding-top:12px}
.nwt b{font-size:17px;line-height:1.3}.nwt time{font-size:13px;opacity:.75}.nwt .nw-tag{align-self:flex-start}
@media (max-width:760px){.nwts{grid-template-columns:1fr}.nwband{padding:20px 18px}.nw{padding:18px}}
'''

JS = '''<script>(function(){var b=document.querySelectorAll('.nwfilt button');b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.setAttribute('aria-pressed',y===x)});var c=x.dataset.c;document.querySelectorAll('.nw').forEach(function(a){a.style.display=(c==='all'||a.dataset.cat===c)?'':'none'})})})})();</script>'''

def page_body(items, LANG):
    return (f'<header class="hero st-hero nwhero"><div class="wrap"><div class="top"><a class="back" href="/">← cheetah vinyl</a>{LANG}</div>'
            f'<div><div class="kicker">{L("Mis à jour chaque jour", "Updated daily")}</div><h1>News</h1>'
            f'<p class="read">{L("L’actualité de la musique africaine, de la soul, du funk et du disco : rééditions, hommages, anniversaires, documentaires. Chaque info est résumée par nos soins et renvoie à sa source.", "News on African music, soul, funk and disco: reissues, tributes, anniversaries, documentaries. Every item is summarised by us and links to its source.")}</p></div></div></header><main class="wrap">'
            f'<div class="nwfilt" role="group" aria-label="Filtre"><button type="button" data-c="all" aria-pressed="true">{L("Tout", "All")}</button>'
            f'<button type="button" data-c="africa" aria-pressed="false">{L("Afrique", "Africa")}</button>'
            f'<button type="button" data-c="soul" aria-pressed="false">Soul · Funk · Disco</button></div>'
            + render_list(items) + '</main>\n' + JS)

def band(items):
    return (f'<section class="nwband" aria-labelledby="h-nw"><div class="row"><h2 id="h-nw">News</h2>'
            f'<a class="all" href="news.html">{L("Toutes les news →", "All news →")}</a></div>' + render_teaser(items) + '</section>\n ')

if __name__ == '__main__':
    items = load(sys.argv[1]); root = sys.argv[2].rstrip('/')
    for f, tag, new in [('news.html', 'NEWS', render_list(items)), ('index.html', 'NEWSTEASER', render_teaser(items))]:
        p = f'{root}/{f}'; t = open(p, encoding='utf-8').read()
        t2 = re.sub(rf'<!--{tag}-->.*?<!--/{tag}-->', lambda m: new.replace('img/', 'img-'), t, count=1, flags=re.S)
        assert t2 != t or new in t, f'bloc {tag} introuvable dans {f}'
        open(p, 'w', encoding='utf-8').write(t2); print('ok', f)
    sm = f'{root}/sitemap.xml'; s = open(sm, encoding='utf-8').read()
    s = re.sub(r'(<loc>https://cheetahvinyl.com/news.html</loc><lastmod>)[^<]+', r'\g<1>' + datetime.date.today().isoformat(), s)
    open(sm, 'w', encoding='utf-8').write(s)
