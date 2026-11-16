"""Intègre la vidéo (TikTok ou Reel Instagram) en haut de chaque histoire, juste sous l'en-tête.
Lit le premier lien de <div class="watch">. Lecteur chargé au clic (page légère, pas de cookies TikTok/Instagram avant le clic).
Idempotent. Usage : python3 _kit/embed.py  (depuis la racine du site)"""
import glob,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
CSS=('<style>'
 '.vtop{margin:34px 0 10px;background:var(--green);color:var(--cream);border-radius:28px;padding:30px 26px;display:grid;grid-template-columns:1fr;gap:26px;align-items:center;position:relative;overflow:hidden}'
 '.vtop:before{content:"";position:absolute;inset:0;background:repeating-radial-gradient(circle at 85% 50%,rgba(255,255,255,.035) 0 26px,transparent 26px 52px);pointer-events:none}'
 '.vtop .vt{position:relative}.vtop .vk{color:var(--ochre);font-weight:600;letter-spacing:.2em;text-transform:uppercase;font-size:12px}'
 '.vtop h2{font-family:var(--display);font-weight:400;color:var(--cream);font-size:clamp(30px,4.4vw,44px);line-height:1.05;margin:.25em 0 .35em}'
 '.vtop p{margin:0;line-height:1.55;opacity:.9;max-width:34ch}'
 '.vtop .vlink{display:inline-block;margin-top:16px;color:var(--ochre);font-weight:700;text-decoration:none}'
 '.vtop .vframe{position:relative;justify-self:center;width:min(300px,82%);border:10px solid var(--cream);border-radius:6px;box-shadow:0 22px 44px rgba(0,0,0,.4);transform:rotate(2deg);transition:transform .3s}'
 '.vtop .vframe:hover{transform:rotate(0)}'
 '.vtop .vbox{position:relative;aspect-ratio:9/16;background:#0f241a;overflow:hidden}'
 '.vtop button{all:unset;cursor:pointer;position:absolute;inset:0;display:block}'
 '.vtop button img{position:absolute;left:0;right:0;top:12%;width:100%;aspect-ratio:1;object-fit:cover}'
 '.vtop button:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,36,26,.55),rgba(15,36,26,0) 22%,rgba(15,36,26,0) 60%,rgba(15,36,26,.85))}'
 '.vtop .pl{position:absolute;z-index:1;left:50%;top:44%;transform:translate(-50%,-50%);width:74px;height:74px;border-radius:50%;background:var(--rust);display:grid;place-items:center;box-shadow:0 8px 22px rgba(0,0,0,.4);transition:transform .2s}'
 '.vtop button:hover .pl{transform:translate(-50%,-50%) scale(1.08)}'
 '.vtop .pl:after{content:"";margin-left:6px;border-left:22px solid var(--cream);border-top:14px solid transparent;border-bottom:14px solid transparent}'
 '.vtop .vh{position:absolute;z-index:1;left:14px;top:12px;font-size:12px;font-weight:700;letter-spacing:.06em}'
 '.vtop .vb{position:absolute;z-index:1;left:14px;right:14px;bottom:14px;font-size:14px;font-weight:600;line-height:1.3}'
 '.vtop iframe{position:absolute;inset:0;width:100%;height:100%;border:0}'
 '@media(min-width:760px){.vtop{grid-template-columns:1.1fr .9fr;padding:40px 46px}}'
 '</style>')
def src_of(u):
    m=re.match(r'https://www\.tiktok\.com/@[^/]+/video/(\d+)',u)
    if m: return 'tiktok',f'https://www.tiktok.com/player/v1/{m.group(1)}?autoplay=1&music_info=1&description=1&rel=0'
    m=re.match(r'https://www\.instagram\.com/reel/([A-Za-z0-9_-]+)',u)
    if m: return 'instagram',f'https://www.instagram.com/reel/{m.group(1)}/embed/'
    return None,None
n=0
for f in sorted(glob.glob(ROOT+"*.html")):
    s=open(f,encoding="utf-8").read()
    s=re.sub(r'<section class="vtop".*?</section>\n?','',s,flags=re.S)
    w=re.search(r'<div class="watch"><a href="([^"]+)"',s)
    if w and '<main class="wrap">' in s:
        kind,src=src_of(w.group(1))
        if kind:
            img=re.search(r'<div class="cover"><img src="([^"]+)"',s)
            poster=f'<img src="{img.group(1)}" alt="">' if img else ''
            h1=re.search(r'<h1>(.*?)<br><em>(.*?)</em></h1>',s)
            title=re.sub('<[^>]+>','',h1.group(1)) if h1 else ''
            who=re.sub('<[^>]+>','',h1.group(2)) if h1 else ''
            net='TikTok' if kind=='tiktok' else 'Instagram'
            acc='@cheetah_vinyl' if kind=='tiktok' else ('@cheetah_vinyl_africa' if 'africa-' in f else '@cheetah_vinyl')
            L=lambda fr,en:f'<span data-l="fr">{fr}</span><span data-l="en">{en}</span>'
            txt=(f'<div class="vt"><div class="vk">{L("La vidéo","The video")}</div>'
                 f'<h2>{L("L’histoire en vidéo","The story on video")}</h2>'
                 f'<p>{L(f"La version courte de cette histoire, telle qu’on l’a racontée sur {net} : les images, le son, et les infos clés.",f"The short version of this story, as we told it on {net}: the footage, the sound and the key facts.")}</p>'
                 f'<a class="vlink" href="{w.group(1)}" target="_blank" rel="noopener">{L(f"Ouvrir sur {net} →",f"Open on {net} →")}</a></div>')
            sec=(f'<section class="vtop" aria-label="Vidéo">{CSS}{txt}<div class="vframe"><div class="vbox"><button type="button" aria-label="Lire la vidéo / Play the video" data-src="{src}" '
                 f'onclick="var f=document.createElement(\'iframe\');f.src=this.dataset.src;f.allow=\'autoplay; encrypted-media; fullscreen; picture-in-picture\';f.allowFullscreen=true;f.title=\'Vidéo\';this.replaceWith(f)">'
                 f'{poster}<span class="vh">{net} · {acc}</span><span class="pl"></span><span class="vb">{who}<br>{title}</span></button></div></div></section>\n')
            s=s.replace('<main class="wrap">\n','<main class="wrap">\n'+sec,1) if '<main class="wrap">\n' in s else s.replace('<main class="wrap">','<main class="wrap">'+sec,1)
            n+=1
    open(f,"w",encoding="utf-8").write(s)
print(n,"vidéos intégrées")
