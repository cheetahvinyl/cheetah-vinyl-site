"""Génère ebook.html (page de vente du livre) à partir du gabarit partenariats.html.
Modifier BUY_FR / BUY_EN / PRICE puis relancer : python3 _kit/ebook_page.py"""
import json, html, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUY_FR = os.environ.get("BUY_FR", "#acheter")   # lien Payhip/Gumroad/Stan… édition française
BUY_EN = os.environ.get("BUY_EN", "#acheter")   # lien édition anglaise
PRICE = os.environ.get("PRICE", "9,90 €")
PRICE_EN = os.environ.get("PRICE_EN", "€9.90")
PLAYLIST = "https://open.spotify.com/playlist/32g8jIKeafruWyQE1fE4VB"

tpl = open(os.path.join(ROOT, "partenariats.html")).read()
head = tpl[:tpl.find("<body")]
tail = tpl[tpl.find('<nav class="mbar"'):]
T = "Tu connais la chanson. Pas l’histoire. | Le livre cheetah vinyl"
DESC = "Le livre numérique cheetah vinyl : 30 tubes disco, funk et soul de 1976 à 1989, leurs histoires cachées, 30 photos et illustrations, et un blind test avec sa playlist Spotify."
head = re.sub(r"<title>.*?</title>", f"<title>{T}</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = head.replace("https://cheetahvinyl.com/partenariats.html", "https://cheetahvinyl.com/ebook.html")
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{T}">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', head)
head = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="https://cheetahvinyl.com/ebook-cover-fr.jpg">', head)
head = re.sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="https://cheetahvinyl.com/ebook-cover-fr.jpg">', head)
head = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{T}">', head)
head = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{DESC}">', head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
ld = {"@context": "https://schema.org", "@type": "Book", "name": "Tu connais la chanson. Pas l’histoire.",
      "alternateName": "You know the song. Not the story.", "bookFormat": "https://schema.org/EBook",
      "numberOfPages": 108, "inLanguage": ["fr", "en"], "author": {"@type": "Organization", "name": "cheetah vinyl"},
      "image": "https://cheetahvinyl.com/ebook-cover-fr.jpg", "url": "https://cheetahvinyl.com/ebook.html",
      "description": DESC}
head = head.replace("</head>", "")

D = json.load(open("/home/claude/ebook/book.json")); D.sort(key=lambda d: int(d["year"]))
DE = {d["slug"]: d for d in json.load(open("/home/claude/ebook/book_en.json"))}
E = html.escape
def b(fr, en): return f'<span data-l="fr">{fr}</span><span data-l="en">{en}</span>'

toc = "".join(f'<li><span class="y">{d["year"]}</span><b>{E(d["song"])}</b><i>{E(d["artist"])}</i></li>' for d in D)

CSS = """<style>
.eb{--g:#1e5a3c;--gd:#163f2b;--o:#e3a21a;--c:#f3e6c8;--r:#c4502a}
.ebhero{background:#1e5a3c url(ebook-cover-fr.jpg) center/0 no-repeat}
.ebgrid{display:grid;grid-template-columns:minmax(240px,380px) 1fr;gap:48px;align-items:center}
.ebcov{position:relative}
.ebcov img{width:100%;border-radius:10px;box-shadow:0 24px 50px rgba(0,0,0,.45);transform:rotate(-2deg);display:block}
.ebcov img.en{display:none}
html[lang=en] .ebcov img.fr{display:none} html[lang=en] .ebcov img.en{display:block}
.ebbadge{position:absolute;right:-14px;top:-14px;background:var(--rust,#c4502a);color:#fff;font:800 13px/1.15 Poppins,sans-serif;border-radius:50%;width:92px;height:92px;display:flex;align-items:center;justify-content:center;text-align:center;transform:rotate(8deg);border:3px solid #f3e6c8;text-transform:uppercase}
.ebprice{font:800 40px Poppins,sans-serif;color:#e3a21a;margin:.2em 0 .1em}
.ebprice small{font:500 15px Poppins,sans-serif;color:#f3e6c8;opacity:.85;margin-left:8px}
.ebbtns{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 10px}
.ebbtn{display:inline-flex;align-items:center;gap:10px;background:#e3a21a;color:#14301f!important;font:800 17px Poppins,sans-serif;padding:15px 26px;border-radius:999px;text-decoration:none!important;box-shadow:0 6px 0 #a8730c}
.ebbtn.soon{background:#f3e6c8;box-shadow:none;cursor:default;opacity:.9}
.ebbtn.alt{background:#f3e6c8;box-shadow:0 6px 0 #b9a77e}
.ebbtn:hover{transform:translateY(2px);box-shadow:0 4px 0 #a8730c}
.ebsafe{font:500 13px Poppins,sans-serif;opacity:.8}
.ebchips{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0;padding:0;list-style:none}
.ebchips li{background:rgba(243,230,200,.14);border:1px solid rgba(243,230,200,.35);border-radius:999px;padding:6px 13px;font:600 13px Poppins,sans-serif}
.ebsec{margin:56px 0}
.ebsec h2{font-family:Poppins,sans-serif;font-weight:800}
.ebteas{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:18px}
.ebteas div{background:#fffaf0;border:2px solid #efe3c4;border-radius:18px;padding:20px}
.ebteas b{display:block;font:800 13px Poppins,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#c4502a;margin-bottom:6px}
.ebteas p{margin:0;font-size:17px}
.ebpages{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px}
.ebpages img{width:100%;border-radius:8px;box-shadow:0 8px 22px rgba(0,0,0,.18);display:block}
.ebtoc{columns:2;column-gap:36px;list-style:none;padding:0;margin:18px 0 0}
.ebtoc li{break-inside:avoid;display:grid;grid-template-columns:46px 1fr;padding:7px 0;border-bottom:1px dotted #cdbf9c;font-family:Poppins,sans-serif;font-size:15px}
.ebtoc .y{color:#c4502a;font-weight:700;grid-row:span 2}
.ebtoc b{color:#1c4630} .ebtoc i{font-style:normal;color:#6b6b5b;font-size:13px}
.ebquiz{background:#1e5a3c;color:#f3e6c8;border-radius:24px;padding:30px 34px;display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center}
.ebquiz h2{color:#e3a21a;margin:0 0 .3em}
.ebquiz a{color:#e3a21a}
.ebfaq details{background:#fffaf0;border:2px solid #efe3c4;border-radius:14px;padding:14px 18px;margin:10px 0}
.ebfaq summary{font:700 16px Poppins,sans-serif;cursor:pointer;color:#1c4630}
.ebfaq p{margin:.6em 0 0}
.ebfinal{text-align:center;background:#f3e6c8;border:2px solid #e3a21a;border-radius:24px;padding:34px 24px}
.ebfinal h2{margin-top:0}
@media(max-width:760px){.ebgrid{grid-template-columns:1fr;gap:28px}.ebcov{max-width:300px;margin:0 auto}.ebpages{grid-template-columns:repeat(2,1fr)}.ebtoc{columns:1}.ebquiz{grid-template-columns:1fr}.ebprice{font-size:34px}}
</style>"""

SOON = BUY_FR.startswith("#")
if SOON:
    BTN = (f'<div class="ebbtns"><span class="ebbtn soon">{b("Bientôt disponible","Coming soon")} 🐆</span></div>')
else:
  BTN = (f'<div class="ebbtns"><a class="ebbtn" href="{BUY_FR}" data-buy="fr">{b("Acheter le livre","Buy the French edition")} 🇫🇷</a>'
         f'<a class="ebbtn alt" href="{BUY_EN}" data-buy="en">{b("Édition anglaise","Buy the English edition")} 🇬🇧</a></div>')

body = f"""<body>
<header class="hero st-hero kmhero eb"><div class="wrap"><div class="top"><a class="back" href="/">← cheetah vinyl</a><div class="lang" role="group" aria-label="Langue / Language"><button id="b-fr" type="button" aria-pressed="true">FR</button><button id="b-en" type="button" aria-pressed="false">EN</button></div></div>
<div class="ebgrid">
<div class="ebcov"><img class="fr" src="ebook-cover-fr.jpg" alt="Couverture du livre Tu connais la chanson. Pas l’histoire." width="700" height="991"><img class="en" src="ebook-cover-en.jpg" alt="Cover of the book You know the song. Not the story." width="700" height="991"><div class="ebbadge">{b("Le livre","The book")}</div></div>
<div>
<div class="kicker">{b("Le livre numérique cheetah vinyl","The cheetah vinyl ebook")}</div>
<h1>{b("Tu connais la chanson. <em>Pas l’histoire.</em>","You know the song. <em>Not the story.</em>")}</h1>
<p class="read">{b("30 tubes qui vous ont fait danser, racontés comme jamais. De « Daddy Cool » à « Pump Up the Jam », les histoires cachées derrière les disques de boîte des années 70 et 80.","30 hits that made you dance, told like never before. From “Daddy Cool” to “Pump Up the Jam”, the hidden stories behind the dance-floor records of the ’70s and ’80s.")}</p>
<div class="ebprice">{b(PRICE,PRICE_EN)}<small>{b("PDF · téléchargement immédiat","PDF · instant download")}</small></div>
{BTN}
<div class="ebsafe">{b("Bientôt en vente · le livre arrivera par e-mail juste après l’achat","On sale soon · the book will arrive by email right after purchase") if SOON else b("Paiement sécurisé · le livre arrive par e-mail juste après l’achat","Secure payment · the book arrives by email right after purchase")}</div>
<ul class="ebchips"><li>{b("108 pages","108 pages")}</li><li>{b("30 histoires vérifiées","30 fact-checked stories")}</li><li>{b("30 photos et illustrations","30 photos & illustrations")}</li><li>{b("Blind test + playlist Spotify","Music quiz + Spotify playlist")}</li><li>{b("Français ou anglais","French or English")}</li></ul>
</div></div></div></header>
<main class="wrap km">

<section class="ebsec">
<h2>{b("Ce que tu vas découvrir","What you’ll discover")}</h2>
<div class="ebteas">
<div><b>Le Freak · Chic</b><p>{b("Refoulés à l’entrée du Studio 54 un soir de Nouvel An, ils rentrent furieux… et écrivent leur plus gros tube.","Turned away at Studio 54 on New Year’s Eve, they went home furious… and wrote their biggest hit.")}</p></div>
<div><b>Juicy Fruit · Mtume</b><p>{b("Un beat bouclé seul, vers 2 heures du matin, sur une boîte à rythmes. Huit semaines n°1 R&B.","A beat finished alone around 2 a.m. on a drum machine. Eight weeks at No. 1 R&B.")}</p></div>
<div><b>September · Earth, Wind & Fire</b><p>{b("Le mot le plus célèbre du disco ne veut rien dire. La parolière voulait le changer.","The most famous word in disco means nothing. The lyricist wanted to change it.")}</p></div>
<div><b>Daddy Cool · Boney M.</b><p>{b("Un flop au départ, un passage télé, et une intro jouée… avec un crayon sur les dents.","A flop at first, one TV spot, and an intro played… with a pencil against the teeth.")}</p></div>
</div>
</section>

<section class="ebsec">
<h2>{b("Feuillette quelques pages","Flip through a few pages")}</h2>
<div class="ebpages"><img src="ebook-page-1.jpg" alt="Page du chapitre Daddy Cool" loading="lazy"><img src="ebook-page-2.jpg" alt="Page du chapitre Juicy Fruit" loading="lazy"><img src="ebook-page-3.jpg" alt="Sommaire du livre" loading="lazy"><img src="ebook-page-4.jpg" alt="Page du blind test" loading="lazy"></div>
<p class="knote">{b("Chaque chapitre : l’histoire, une citation, les dates clés, les crédits et une question de blind test. Aperçu de l’édition française.","Each chapter: the story, a quote, a timeline, the credits and a quiz question. Preview of the French edition.")}</p>
</section>

<section class="ebsec">
<h2>{b("Les 30 tubes du livre","The 30 hits in the book")}</h2>
<ol class="ebtoc">{toc}</ol>
</section>

<section class="ebsec ebquiz">
<div><h2>{b("Le blind test du Cheetah Club","The Cheetah Club music quiz")}</h2>
<p>{b("30 questions pour ta prochaine soirée, avec les réponses. La playlist Spotify du jeu est prête : les 30 titres dans l’ordre du livre, en un clic depuis le PDF.","30 questions for your next party, with the answers. The quiz’s Spotify playlist is ready: all 30 tracks in book order, one tap away from the PDF.")}</p></div>
<div style="font-size:64px">🎧</div>
</section>

<section class="ebsec ebfaq">
<h2>{b("Questions fréquentes","FAQ")}</h2>
<details><summary>{b("Comment je reçois le livre ?","How do I get the book?")}</summary><p>{b("Juste après le paiement, tu reçois un lien de téléchargement par e-mail. C’est un fichier PDF.","Right after payment you receive a download link by email. It’s a PDF file.")}</p></details>
<details><summary>{b("Je peux le lire sur mon téléphone ?","Can I read it on my phone?")}</summary><p>{b("Oui : téléphone, tablette ou ordinateur. Le format est pensé pour l’écran, et tu peux aussi l’imprimer.","Yes: phone, tablet or computer. It’s designed for screens, and you can print it too.")}</p></details>
<details><summary>{b("Il existe en anglais ?","Is it available in English?")}</summary><p>{b("Oui, il y a deux éditions : française et anglaise. Le contenu est le même.","Yes, there are two editions: French and English, with the same content.")}</p></details>
<details><summary>{b("C’est une bonne idée de cadeau ?","Does it make a good gift?")}</summary><p>{b("Pour quelqu’un qui a dansé sur ces disques, oui. Et le blind test fait une animation toute prête pour un anniversaire.","For anyone who danced to these records, yes. And the music quiz is a ready-made game for a birthday party.")}</p></details>
<details><summary>{b("D’où viennent les histoires ?","Where do the stories come from?")}</summary><p>{b("Chaque histoire est vérifiée, et les sources sont listées à la fin du livre. Les photos sont libres de droits (Wikimedia Commons) et créditées.","Every story is fact-checked, and the sources are listed at the end of the book. The photos are freely licensed (Wikimedia Commons) and credited.")}</p></details>
</section>

<section class="ebsec ebfinal">
<h2>{b("Mets le disque. Monte le son.","Put the record on. Turn it up.")}</h2>
<p>{b("Et découvre ce qu’on ne t’a jamais dit.","And discover what nobody ever told you.")}</p>
{BTN}
</section>
</main>
"""
LD = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"
out = head + CSS + LD + "</head>\n" + body + tail
out = out.replace('<script async src="https://talk.hyvor.com/embed/embed.js" type="module"></script>', "")
out = re.sub(r'<script id="ht-init">.*?</script>', "", out, flags=re.S)
open(os.path.join(ROOT, "ebook.html"), "w").write(out)
print("ok", len(out))
