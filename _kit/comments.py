"""Ajoute (ou remet) le bloc de commentaires Hyvor Talk en bas de chaque page de contenu.
Idempotent. Usage : python3 _kit/comments.py  (depuis la racine du site)"""
import glob,os,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"
WID="16866"
SKIP={"index.html","news.html","404.html","linn-lm-1.html","roland-tr-808.html"}
PORTRAITS={"rod-temperton","quincy-jones","bruce-swedien","nile-rodgers-bernard-edwards","giorgio-moroder","jimmy-jam-terry-lewis","burt-bacharach","ndugu-chancler","marcus-miller","babyface"}
SEC=('<section id="commentaires"><h2><span data-l="fr">Un souvenir à partager ?</span><span data-l="en">A memory to share?</span></h2>'
 '<p class="sub"><span data-l="fr">Raconte-nous où et quand tu as découvert ce son. Pas besoin de compte : les commentaires sont relus avant d’être publiés.</span>'
 '<span data-l="en">Tell us where and when you first heard it. No account needed: comments are reviewed before they go live.</span></p>'
 f'<hyvor-talk-comments website-id="{WID}" page-id="PAGEID" loading="manual"></hyvor-talk-comments></section>\n')
JS=('<script async src="https://talk.hyvor.com/embed/embed.js" type="module"></script>\n'
 '<script id="ht-init">(function(){var c=document.querySelector("hyvor-talk-comments");if(!c)return;'
 'c.setAttribute("page-language",document.documentElement.lang==="en"?"en":"fr");'
 'function go(){if(c.load)c.load();else setTimeout(go,200)}'
 'if("IntersectionObserver" in window){var o=new IntersectionObserver(function(e){if(e[0].isIntersecting){o.disconnect();go()}},{rootMargin:"400px"});o.observe(c)}else go();})();</script>\n')
n=0
for f in sorted(glob.glob(ROOT+"*.html")):
    name=os.path.basename(f)
    s=open(f,encoding="utf-8").read()
    if name in SKIP:
        s=re.sub(r'<section id="commentaires">.*?</section>\n?','',s,flags=re.S)
        s=re.sub(r'<script async src="https://talk\.hyvor\.com/embed/embed\.js" type="module"></script>\n?<script id="ht-init">.*?</script>\n?','',s,flags=re.S)
        open(f,"w",encoding="utf-8").write(s); continue
    if "</main>" not in s: continue
    s=re.sub(r'<section id="commentaires">.*?</section>\n?','',s,flags=re.S)
    s=re.sub(r'<script async src="https://talk\.hyvor\.com/embed/embed\.js" type="module"></script>\n?<script id="ht-init">.*?</script>\n?','',s,flags=re.S)
    sec=SEC.replace("PAGEID",name[:-5])
    if name[:-5] in PORTRAITS:
        sec=sec.replace("Raconte-nous où et quand tu as découvert ce son.","Un disque préféré, une anecdote ? Raconte-nous.").replace("Tell us where and when you first heard it.","A favourite record, a story? Tell us.").replace("Un souvenir à partager ?","Ton disque préféré ?").replace("A memory to share?","Your favourite record?")
    s=s.replace("</main>",sec+"</main>",1)
    s=s.replace('<script data-goatcounter',JS+'<script data-goatcounter',1) if '<script data-goatcounter' in s else s.replace("</body>",JS+"</body>",1)
    open(f,"w",encoding="utf-8").write(s); n+=1
print(n,"pages")
