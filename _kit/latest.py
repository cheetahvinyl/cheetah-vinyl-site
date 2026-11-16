"""Met à jour le bandeau « Nouvelle histoire » de la page d'accueil
avec la première carte de la section #histoires (la plus récente).
Usage : python3 _kit/latest.py   (depuis la racine du site)"""
import re,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
s=open(ROOT+"index.html",encoding="utf-8").read()
sec=s[s.index('id="histoires"'):]
c=re.search(r'<a class="story" href="([^"]+)"><div class="art"><img src="([^"]+)" alt="([^"]*)".*?<div class="who">(.*?)</div><div class="meta">(.*?) · (\d{4})</div><p class="hook">(.*?)</p>',sec,re.S)
href,img,alt,who,song,year,hook=c.groups()
page=open(ROOT+href,encoding="utf-8").read()
v=re.search(r'<div class="watch"><a href="([^"]+)"',page)
vid=v.group(1) if v else "https://www.tiktok.com/@cheetah_vinyl"
band=(f'<section class="newband" aria-labelledby="h-new"><a class="nb-cover" href="{href}"><img src="{img}" alt="{alt}"></a><div>'
 f'<div class="k"><span data-l="fr">Nouvelle histoire</span><span data-l="en">New story</span></div>'
 f'<h2 id="h-new">{song}<br><em>{who}</em></h2><p>{hook}</p>'
 f'<div class="btns"><a class="p" href="{href}"><span data-l="fr">Lire l’histoire</span><span data-l="en">Read the story</span></a>'
 f'<a class="g" href="{vid}" target="_blank" rel="noopener"><span data-l="fr">Voir la vidéo</span><span data-l="en">Watch the video</span></a></div></div></section>')
s=re.sub(r'<section class="newband".*?</section>',lambda m:band,s,count=1,flags=re.S)
open(ROOT+"index.html","w",encoding="utf-8").write(s)
print("Nouvelle histoire :",who,"–",song,year)

# --- Dernière histoire Cheetah Africa (première carte numérotée de #africa), juste après le bandeau précédent
s=open(ROOT+"index.html",encoding="utf-8").read()
sec=s[s.index('id="africa"'):]
c=re.search(r'<a class="story[^"]*" href="([^"]+)"><div class="art"><img src="([^"]+)" alt="([^"]*)"[^>]*><span class="badge">(Nº \d+)</span></div><div class="txt"><div class="who">(.*?)</div><div class="meta">(.*?) · (\d{4})</div><p class="hook">(.*?)</p>',sec,re.S)
href,img,alt,num,who,song,year,hook=c.groups()
page=open(ROOT+href,encoding="utf-8").read()
v=re.search(r'<div class="watch"><a href="([^"]+)"',page)
vid=v.group(1) if v else "https://www.instagram.com/cheetah_vinyl_africa/"
band=(f'<section class="newband afnew" aria-labelledby="h-newaf"><a class="nb-cover" href="{href}"><img src="{img}" alt="{alt}"></a><div>'
 f'<div class="k"><span data-l="fr">Nouveau · Cheetah Africa {num}</span><span data-l="en">New · Cheetah Africa {num}</span></div>'
 f'<h2 id="h-newaf">{who}<br><em>{song}</em></h2><p>{hook}</p>'
 f'<div class="btns"><a class="p" href="{href}"><span data-l="fr">Lire l’histoire</span><span data-l="en">Read the story</span></a>'
 f'<a class="g" href="{vid}" target="_blank" rel="noopener"><span data-l="fr">Voir la vidéo</span><span data-l="en">Watch the video</span></a>'
 f'<a class="g" href="#africa"><span data-l="fr">Toute la série</span><span data-l="en">The whole series</span></a></div></div></section>')
if '<section class="newband afnew"' in s:
    s=re.sub(r'<section class="newband afnew".*?</section>',lambda m:band,s,count=1,flags=re.S)
else:
    i=s.index('<section class="newband"'); j=s.index('</section>',i)+len('</section>'); s=s[:j]+"\n"+band+s[j:]
CSS=('.newband.afnew{background:var(--green-deep,#123222);color:var(--cream)}.newband.afnew h2{color:var(--cream)}.newband.afnew h2 em{color:var(--ochre)}'
     '.newband.afnew .k{background:var(--ochre);color:var(--ink,#121812)}.newband.afnew .btns a.p{background:var(--ochre);color:var(--ink,#121812)}'
     '.newband.afnew .btns a.g{border:1.5px solid var(--cream);color:var(--cream)}')
if '.newband.afnew{' not in s: s=s.replace('</style>',CSS+'</style>',1)
open(ROOT+"index.html","w",encoding="utf-8").write(s)
print("Dernier Cheetah Africa :",num,who,"–",song)
