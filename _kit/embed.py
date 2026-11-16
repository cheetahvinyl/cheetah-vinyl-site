"""Intègre la vidéo (TikTok ou Reel Instagram) en haut de chaque histoire, juste sous l'en-tête.
Lit le premier lien de <div class="watch">. Lecteur chargé au clic (page légère, pas de cookies TikTok/Instagram avant le clic).
Idempotent. Usage : python3 _kit/embed.py  (depuis la racine du site)"""
import glob,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
CSS=('<style>.vtop{display:flex;justify-content:center;margin:26px 0 8px}.vtop .vbox{position:relative;width:min(340px,100%);aspect-ratio:9/16;border-radius:22px;overflow:hidden;background:#123524;box-shadow:0 14px 34px rgba(0,0,0,.25)}'
 '.vtop button{all:unset;cursor:pointer;position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;color:#f3e6c8;font-weight:700;text-align:center}'
 '.vtop button img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.55) blur(2px);transform:scale(1.06)}'
 '.vtop .pl{position:relative;width:78px;height:78px;border-radius:50%;background:#c4502a;display:grid;place-items:center;box-shadow:0 6px 18px rgba(0,0,0,.35)}'
 '.vtop .pl:after{content:"";margin-left:6px;border-left:24px solid #f3e6c8;border-top:15px solid transparent;border-bottom:15px solid transparent}'
 '.vtop .lb{position:relative;font-size:16px;letter-spacing:.04em}.vtop iframe{position:absolute;inset:0;width:100%;height:100%;border:0}</style>')
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
            lab='<span data-l="fr">Regarder la vidéo</span><span data-l="en">Watch the video</span>'
            sec=(f'<section class="vtop" aria-label="Vidéo">{CSS}<div class="vbox"><button type="button" data-src="{src}" '
                 f'onclick="var f=document.createElement(\'iframe\');f.src=this.dataset.src;f.allow=\'autoplay; encrypted-media; fullscreen; picture-in-picture\';f.allowFullscreen=true;f.title=\'Vidéo\';this.replaceWith(f)">'
                 f'{poster}<span class="pl"></span><span class="lb">{lab}</span></button></div></section>\n')
            s=s.replace('<main class="wrap">\n','<main class="wrap">\n'+sec,1) if '<main class="wrap">\n' in s else s.replace('<main class="wrap">','<main class="wrap">'+sec,1)
            n+=1
    open(f,"w",encoding="utf-8").write(s)
print(n,"vidéos intégrées")
