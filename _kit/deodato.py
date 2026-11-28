import re, json, os
ROOT = "/home/claude/cheetah-vinyl-site/"
src = open(ROOT + "giorgio-moroder.html").read()
head = src[:src.find("<body")]
tail = src[src.find('<nav class="mbar"'):]

def b(fr, en): return f'<span data-l="fr">{fr}</span><span data-l="en">{en}</span>'

TITLE = "Eumir Deodato, l’arrangeur de Kool &amp; the Gang | cheetah vinyl"
DESC = "Portrait d’Eumir Deodato : de Rio à New York, « Also Sprach Zarathustra (2001) », les tubes de Kool &amp; the Gang dont « Celebration », et Björk."
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = head.replace("https://cheetahvinyl.com/giorgio-moroder.html", "https://cheetahvinyl.com/eumir-deodato.html")
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Eumir Deodato, l’arrangeur de Kool &amp; the Gang">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', head)
head = head.replace("https://cheetahvinyl.com/img-moroder.jpg", "https://cheetahvinyl.com/img-deodato.jpg")
head = re.sub(r'<meta name="twitter:(title|description)" content="[^"]*">', lambda m: f'<meta name="twitter:{m.group(1)}" content="{"Eumir Deodato, l’arrangeur de Kool &amp; the Gang" if m.group(1)=="title" else DESC}">', head)
ld = {"@context": "https://schema.org", "@type": "Article", "headline": "Eumir Deodato : de Rio à « Celebration » | cheetah vinyl",
      "description": "Portrait d’Eumir Deodato : arrangeur à Rio, CTI à New York, « Also Sprach Zarathustra (2001) », quatre albums de Kool & the Gang et les arrangements de Björk.",
      "inLanguage": ["fr", "en"], "image": "https://cheetahvinyl.com/img-deodato.jpg", "url": "https://cheetahvinyl.com/eumir-deodato.html",
      "author": {"@type": "Organization", "name": "cheetah vinyl"}, "publisher": {"@type": "Organization", "name": "cheetah vinyl"},
      "about": {"@type": "Person", "name": "Eumir Deodato", "birthDate": "1942-06-22", "birthPlace": "Rio de Janeiro"}}
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>", head, count=1, flags=re.S)

P = lambda fr, en, cls="": f'<p{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>{b(fr, en)}</p>'
H3 = lambda fr, en: f"<h3>{b(fr, en)}</h3>"
story = "".join([
 P("New York, 1979. Les musiciens de Kool &amp; the Gang viennent frapper à la porte d’un Brésilien de 37 ans. Ils ont écouté son album Love Island et ils veulent le même son. Sa première réponse est non : « Je ne peux pas vous aider. C’est trop. » Il finit par accepter. En deux ans, il leur donne « Ladies’ Night », « Too Hot » et « Celebration ».",
   "New York, 1979. The members of Kool &amp; the Gang come knocking on the door of a 37-year-old Brazilian. They have heard his album Love Island and want that sound. His first answer is no: “I can’t help you. It’s too much.” He ends up saying yes. Within two years he gives them “Ladies’ Night”, “Too Hot” and “Celebration”.", "drop"),
 P("Il s’appelle Eumir Deodato. Son nom de famille veut dire « donné par Dieu ». Et le plus étonnant, c’est qu’il a appris presque tout seul.",
   "His name is Eumir Deodato. His surname means “God-given”. And the most surprising part is that he learned almost everything on his own."),
 H3("Un arrangement à 17 ans", "An arrangement at 17"),
 P("Il naît le 22 juin 1942 à Rio de Janeiro. À 12 ans, il commence l’accordéon, puis le piano deux ans plus tard. À 17 ans, on lui propose d’écrire les arrangements d’un disque entier. Il dit oui tout de suite, alors qu’il n’a jamais vu une partition d’orchestre et ne sait pas vraiment ce qu’est un arrangement. Pas question d’attendre cinq ans de conservatoire : il apprend en jouant dans un petit groupe et en posant des questions à ses amis.",
   "He is born on 22 June 1942 in Rio de Janeiro. He starts on accordion at 12, then piano two years later. At 17 he is asked to write the arrangements for a whole record. He says yes straight away, even though he has never seen an orchestral score and doesn’t really know what an arrangement is. No time for five years of conservatory: he learns by playing in a small band and asking his friends."),
 P("Au début des années 60, il devient arrangeur pour le label Odeon, au cœur de la bossa nova, avec Marcos Valle, Wilson Simonal ou Leny Andrade. En 1964, à 22 ans, il enregistre son premier album, Inútil Paisagem, consacré aux chansons d’Antônio Carlos Jobim. Jobim lui-même écrit le texte de la pochette et joue sur le sens de son nom. Deodato aide aussi à lancer un jeune chanteur : il choisit trois chansons de Milton Nascimento pour un festival.",
   "In the early ’60s he becomes an arranger for the Odeon label, right at the heart of bossa nova, working with Marcos Valle, Wilson Simonal and Leny Andrade. In 1964, aged 22, he records his first album, Inútil Paisagem, devoted to the songs of Antônio Carlos Jobim. Jobim himself writes the liner notes and plays on the meaning of his name. Deodato also helps launch a young singer: he picks three Milton Nascimento songs for a festival."),
 H3("New York, 1967", "New York, 1967"),
 P("En 1967, il part à New York pour travailler avec le guitariste Luiz Bonfá, avec qui il enregistre sept albums. Bonfá lui présente Astrud Gilberto et le producteur Creed Taylor. Taylor l’engage pour écrire les arrangements des artistes de son label CTI : Wes Montgomery, Jobim, Stanley Turrentine, Paul Desmond. Deodato écrit aussi les grands arrangements d’orchestre d’un disque de Frank Sinatra avec Jobim, et travaille pour Aretha Franklin et Roberta Flack.",
   "In 1967 he moves to New York to work with guitarist Luiz Bonfá, with whom he records seven albums. Bonfá introduces him to Astrud Gilberto and producer Creed Taylor. Taylor hires him to write arrangements for the artists on his CTI label: Wes Montgomery, Jobim, Stanley Turrentine, Paul Desmond. Deodato also writes the big-orchestra arrangements for a Frank Sinatra record with Jobim, and works for Aretha Franklin and Roberta Flack."),
 H3("2001, l’odyssée funk", "2001, the funk odyssey"),
 P("Pour son premier album américain, Prelude, il a une idée étrange : reprendre en version funk « Ainsi parlait Zarathoustra » de Richard Strauss, le thème que le film 2001, l’Odyssée de l’espace a rendu célèbre. L’idée lui vient en s’endormant. Il note quelques lignes sur papier, sans même écrire les accords.",
   "For his first American album, Prelude, he has a strange idea: a funk version of Richard Strauss’s “Also Sprach Zarathustra”, the theme made famous by the film 2001: A Space Odyssey. The idea comes to him as he is falling asleep. He jots a few lines on paper, without even writing out the chords."),
 P("Creed Taylor garde la prise d’origine : dix minutes et demie. Deodato ne croit pas une seconde à un succès radio. Quelqu’un en Californie la raccourcit à environ quatre minutes et demie. Un jour, le percussionniste Airto Moreira l’appelle : le morceau grimpe dans les classements. En mars 1973, « Also Sprach Zarathustra (2001) » est n°2 au Billboard Hot 100. Il lui vaut le Grammy de la meilleure interprétation pop instrumentale, et Prelude devient n°1 des ventes de jazz aux États-Unis.",
   "Creed Taylor keeps the original take: ten and a half minutes. Deodato doesn’t believe for a second it could be a radio hit. Someone in California cuts it down to about four and a half minutes. One day percussionist Airto Moreira calls him: the track is climbing the charts. In March 1973 “Also Sprach Zarathustra (2001)” reaches No. 2 on the Billboard Hot 100. It wins him the Grammy for Best Pop Instrumental Performance, and Prelude becomes the No. 1 jazz album in the US."),
 H3("Le chronomètre de « Ladies’ Night »", "The “Ladies’ Night” stopwatch"),
 P("Quand Kool &amp; the Gang vient le chercher en 1979, le groupe a un nouveau chanteur, J.T. Taylor, et cherche un nouveau son. Deodato coproduit et arrange l’album Ladies’ Night. Pour obtenir un rythme parfaitement régulier, il recopie de courtes boucles de batterie sur une bande neuve, et chronomètre chaque mesure. « Ladies’ Night » monte à la 8e place du Hot 100, « Too Hot » à la 5e.",
   "When Kool &amp; the Gang come to him in 1979, the band has a new singer, J.T. Taylor, and is looking for a new sound. Deodato co-produces and arranges the Ladies’ Night album. To get a perfectly steady groove, he copies short drum loops onto fresh tape, and times every bar with a stopwatch. “Ladies’ Night” reaches No. 8 on the Hot 100, “Too Hot” No. 5."),
 P("Les arrangements se font au fil des séances, en studio, avec le groupe. Il dira lui-même que c’était davantage de la production que de l’arrangement. L’album suivant, Celebrate!, contient « Celebration », qu’il cosigne avec les huit membres du groupe. Le 7 février 1981, la chanson est n°1 au Billboard Hot 100, pour deux semaines.",
   "The arrangements happen as the sessions go along, in the studio, with the band. He will say himself that it was more production than arranging. The next album, Celebrate!, includes “Celebration”, which he co-writes with the band’s eight members. On 7 February 1981 the song is No. 1 on the Billboard Hot 100, for two weeks."),
 '<blockquote class="q">' + b("« On a eu “Celebration”, et ce n’était pas un hasard. »", "“We got ‘Celebration’ and that was no coincidence.”") + "<cite>" + b("Eumir Deodato, Red Bull Music Academy", "Eumir Deodato, Red Bull Music Academy") + "</cite></blockquote>",
 P("Suivent Something Special et « Get Down on It », n°3 au Royaume-Uni et n°10 aux États-Unis en 1982, puis As One. De 1979 à 1982, Deodato produit quatre albums de Kool &amp; the Gang, tous vendus à plus d’un million d’exemplaires. Le groupe de jazz-funk de Jersey City est devenu une machine à tubes.",
   "Then come Something Special and “Get Down on It”, No. 3 in the UK and No. 10 in the US in 1982, followed by As One. From 1979 to 1982 Deodato produces four Kool &amp; the Gang albums, every one a million-seller. The jazz-funk band from Jersey City has become a hit machine."),
 H3("Björk et un vieux disque", "Björk and an old record"),
 P("Quinze ans plus tard, une chanteuse islandaise l’appelle. Björk a trouvé un vieux disque sorti en France, avec un arrangement qu’il avait écrit pour Milton Nascimento lors d’un festival à Rio. Il ne savait même pas que ce disque existait. De 1996 à 1998, Deodato arrange pour elle les albums Post, Telegram et Homogenic, et dirige l’orchestre de ses concerts au Brésil et aux États-Unis.",
   "Fifteen years later, an Icelandic singer calls him. Björk has found an old record released in France, with an arrangement he had written for Milton Nascimento at a festival in Rio. He didn’t even know that record existed. From 1996 to 1998 Deodato arranges the albums Post, Telegram and Homogenic for her, and conducts the orchestra at her concerts in Brazil and the US."),
 P("Plus de 500 disques arrangés ou produits, quinze albums de platine. Le garçon de Rio qui ne savait pas lire une partition d’orchestre a fait danser la planète, d’une odyssée spatiale à « Celebration ».",
   "More than 500 records arranged or produced, fifteen platinum albums. The boy from Rio who couldn’t read an orchestral score got the whole world dancing, from a space odyssey to “Celebration”."),
 '<p>' + b('<a href="kool-and-the-gang-ladies-night.html" style="color:var(--rust);font-weight:700">Lire l’histoire de « Ladies’ Night » →</a>', '<a href="kool-and-the-gang-ladies-night.html" style="color:var(--rust);font-weight:700">Read the “Ladies’ Night” story →</a>') + "</p>",
])

facts = [("500+", "disques arrangés ou produits", "records arranged or produced"), ("15", "albums de platine", "platinum albums"),
         ("N°2", "au Hot 100 avec « 2001 » (1973)", "on the Hot 100 with “2001” (1973)"), ("10 min 30", "la prise d’origine de « 2001 »", "the original take of “2001”"),
         ("4", "albums de Kool &amp; the Gang, 1979–1982", "Kool &amp; the Gang albums, 1979–1982"), ("1942", "naissance à Rio de Janeiro", "born in Rio de Janeiro")]
facts_h = "".join(f'<div class="fact"><b>{n}</b><span>{b(f, e)}</span></div>' for n, f, e in facts)

tl = [("1942", "1942", "Naissance le 22 juin à Rio de Janeiro.", "Born on 22 June in Rio de Janeiro."),
      ("Années 60", "The ’60s", "Arrangeur pour le label Odeon, au cœur de la bossa nova.", "Arranger for the Odeon label, at the heart of bossa nova."),
      ("1964", "1964", "Premier album, Inútil Paisagem, consacré à Jobim.", "First album, Inútil Paisagem, devoted to Jobim."),
      ("1967", "1967", "Départ pour New York avec Luiz Bonfá. Arrangeur pour CTI.", "Moves to New York with Luiz Bonfá. Arranger for CTI."),
      ("1973", "1973", "Prelude et « Also Sprach Zarathustra (2001) », n°2 au Hot 100.", "Prelude and “Also Sprach Zarathustra (2001)”, Hot 100 No. 2."),
      ("1974", "1974", "Grammy de la meilleure interprétation pop instrumentale.", "Grammy for Best Pop Instrumental Performance."),
      ("1979", "1979", "Kool &amp; the Gang : Ladies’ Night.", "Kool &amp; the Gang: Ladies’ Night."),
      ("1981", "1981", "« Celebration », n°1 au Hot 100 le 7 février.", "“Celebration”, Hot 100 No. 1 on 7 February."),
      ("1982", "1982", "« Get Down on It », n°3 au Royaume-Uni, n°10 aux États-Unis.", "“Get Down on It”, UK No. 3, US No. 10."),
      ("1996–1998", "1996–1998", "Arrangements pour Björk : Post, Telegram, Homogenic.", "Arrangements for Björk: Post, Telegram, Homogenic.")]
tl_h = "".join(f'<li><span class="when">{b(a, c)}</span>{b(d, e)}</li>' for a, c, d, e in tl)

def table(rows):
    body = "".join(f"<tr><td>{a}</td><td>{r}</td><td>{b(f, e)}</td></tr>" for a, r, f, e in rows)
    return ('<div class="tw"><table class="spec"><thead><tr><th>' + b("Artiste", "Artist") + "</th><th>" + b("Disque", "Record") + "</th><th>" + b("À savoir", "Worth knowing") + "</th></tr></thead><tbody>" + body + "</tbody></table></div>")
recs1 = [("Deodato", "Inútil Paisagem (1964)", "Son premier album, consacré à Jobim.", "His first album, devoted to Jobim."),
         ("Deodato", "Prelude (1973)", "N°1 des ventes jazz aux États-Unis, n°3 pop.", "US No. 1 jazz album, No. 3 pop."),
         ("Deodato", "Also Sprach Zarathustra (2001) (1973)", "N°2 au Hot 100, n°7 au Royaume-Uni. Grammy.", "Hot 100 No. 2, UK No. 7. Grammy."),
         ("Deodato", "Love Island (1978)", "« Whistle Bump », n°8 dance. L’album qui attire Kool &amp; the Gang.", "“Whistle Bump”, dance No. 8. The album that drew Kool &amp; the Gang."),
         ("Deodato", "Night Cruiser (1980)", "Nomination aux Grammys (R&amp;B instrumental).", "Grammy nomination (R&amp;B instrumental).")]
recs2 = [("Kool &amp; the Gang", "Ladies’ Night (1979)", "« Ladies’ Night » n°8, « Too Hot » n°5 au Hot 100.", "“Ladies’ Night” No. 8, “Too Hot” No. 5 on the Hot 100."),
         ("Kool &amp; the Gang", "Celebrate! (1980)", "« Celebration », n°1 au Hot 100 pendant 2 semaines.", "“Celebration”, Hot 100 No. 1 for 2 weeks."),
         ("Kool &amp; the Gang", "Something Special (1981)", "« Get Down on It », « Take My Heart ».", "“Get Down on It”, “Take My Heart”."),
         ("Kool &amp; the Gang", "As One (1982)", "Le quatrième album de la série.", "The fourth album of the run."),
         ("Björk", "Post (1995) · Homogenic (1997)", "Arrangements, puis direction de l’orchestre en concert.", "Arrangements, then conducting her orchestra on tour.")]

body = f"""<body>
<header class="hero st-hero"><div class="wrap">
<div class="top"><a class="back" href="/">← cheetah vinyl</a><div class="lang" role="group" aria-label="Langue / Language"><button id="b-fr" type="button" aria-pressed="true">FR</button><button id="b-en" type="button" aria-pressed="false">EN</button></div></div>
<div><div class="kicker">{b("Créateurs · Arrangeur et producteur", "Creators · Arranger and producer")}</div>
<h1>Eumir<br><em>Deodato</em></h1>
<p class="lede">{b("Un Brésilien qui a appris à arranger sans conservatoire, un « 2001 » funk n°2 aux États-Unis, puis les tubes de Kool &amp; the Gang, de « Ladies’ Night » à « Celebration ».", "A Brazilian who learned to arrange without a conservatory, a funk “2001” at US No. 2, then Kool &amp; the Gang’s hits, from “Ladies’ Night” to “Celebration”.")}</p>
<div class="chips"><span class="chip hot">{b("Celebration", "Celebration")}</span><span class="chip">{b("« 2001 » · Grammy", "“2001” · Grammy")}</span><span class="chip">{b("Rio · New York", "Rio · New York")}</span><span class="chip">{b("500+ disques", "500+ records")}</span></div>
<nav class="toc" aria-label="Sommaire"><a href="#recit">{b("Le récit", "The story")}</a><a href="#reperes">{b("Repères", "Timeline")}</a><a href="#disques">{b("Ses disques", "His records")}</a><a href="#fiche">{b("Fiche", "Fact file")}</a></nav></div>
<div class="cover"><img width="323" height="325" src="img-deodato.jpg" alt="Pochette de l’album Prelude de Deodato (1973)"></div>
</div></header>
<main class="wrap">
<section id="recit"><h2>{b("Le garçon de Rio", "The boy from Rio")}</h2><div class="read feature">{story}</div></section>
<section aria-label="En chiffres"><h2>{b("En chiffres", "By the numbers")}</h2><div class="facts">{facts_h}</div></section>
<section id="reperes"><h2>{b("Repères", "Timeline")}</h2><ul class="time read">{tl_h}</ul></section>
<section id="disques"><h2>{b("Ses disques", "His records")}</h2><div class="read">
<h3>{b("Sous son nom", "Under his own name")}</h3>{table(recs1)}
<h3>{b("Comme producteur et arrangeur", "As producer and arranger")}</h3>{table(recs2)}
<div class="note">{b("<b>Ils ont travaillé avec lui.</b> Wes Montgomery, Antônio Carlos Jobim, Astrud Gilberto, Luiz Bonfá, Frank Sinatra, Aretha Franklin, Roberta Flack, Stanley Turrentine, Paul Desmond, Con Funk Shun, Kleeer, Larry Graham, k.d. lang, Björk.", "<b>They worked with him.</b> Wes Montgomery, Antônio Carlos Jobim, Astrud Gilberto, Luiz Bonfá, Frank Sinatra, Aretha Franklin, Roberta Flack, Stanley Turrentine, Paul Desmond, Con Funk Shun, Kleeer, Larry Graham, k.d. lang, Björk.")}</div>
</div></section>
<section id="fiche"><h2>{b("Fiche", "Fact file")}</h2><dl class="credits">
<div><dt>{b("Nom", "Name")}</dt><dd>Eumir Deodato de Almeida</dd></div>
<div><dt>{b("Naissance", "Born")}</dt><dd>{b("22 juin 1942, Rio de Janeiro (Brésil)", "22 June 1942, Rio de Janeiro (Brazil)")}</dd></div>
<div><dt>{b("Métiers", "Roles")}</dt><dd>{b("Pianiste, arrangeur, compositeur, producteur", "Pianist, arranger, composer, producer")}</dd></div>
<div><dt>{b("Labels", "Labels")}</dt><dd>Odeon, CTI, MCA, Warner Bros.</dd></div>
<div><dt>{b("Récompense", "Award")}</dt><dd>{b("Grammy 1974, meilleure interprétation pop instrumentale", "1974 Grammy, Best Pop Instrumental Performance")}</dd></div>
<div><dt>{b("Tube", "Hit")}</dt><dd>{b("« Also Sprach Zarathustra (2001) », n°2 au Hot 100", "“Also Sprach Zarathustra (2001)”, Hot 100 No. 2")}</dd></div>
</dl></section>
<section><h2>{b("Sur nos réseaux", "On our socials")}</h2><p class="read">{b("Chaque semaine, un disque et son histoire en vidéo.", "Every week, a record and its story on video.")}</p>
<div class="watch"><a href="https://www.tiktok.com/@cheetah_vinyl" target="_blank" rel="noopener">TikTok</a><a href="https://www.instagram.com/cheetah_vinyl/" target="_blank" rel="noopener">Instagram</a></div>
<p class="src">Sources : <a href="https://en.wikipedia.org/wiki/Eumir_Deodato" target="_blank" rel="noopener">Wikipedia, Eumir Deodato</a> · <a href="https://www.redbullmusicacademy.com/lectures/eumir-deodato-just-a-boy-from-rio" target="_blank" rel="noopener">Red Bull Music Academy, conférence « Just a Boy from Rio »</a> · <a href="https://www.stereogum.com/2081505/the-number-ones-kool-the-gangs-celebration/franchises/columns/the-number-ones/" target="_blank" rel="noopener">Stereogum, The Number Ones : Celebration</a> · <a href="https://en.wikipedia.org/wiki/Get_Down_on_It" target="_blank" rel="noopener">Wikipedia, Get Down on It</a> · <a href="https://www.udiscovermusic.com/stories/kool-the-gang-get-down-on-it-song" target="_blank" rel="noopener">uDiscover Music</a></p>
<p class="src">{b("Pochette : Prelude (CTI, 1973) © ses ayants droit.", "Cover: Prelude (CTI, 1973) © its rights holders.")}</p></section>
<section id="commentaires"><h2>{b("Ton disque préféré ?", "Your favourite record?")}</h2><p class="sub">{b("Un disque préféré, une anecdote ? Raconte-nous. Pas besoin de compte : les commentaires sont relus avant d’être publiés.", "A favourite record, a story? Tell us. No account needed: comments are reviewed before they go live.")}</p><hyvor-talk-comments website-id="16866" page-id="eumir-deodato" loading="manual"></hyvor-talk-comments></section>
</main>
"""
open(ROOT + "eumir-deodato.html", "w").write(head + body + tail)

# index card + counter
s = open(ROOT + "index.html").read()
if 'href="eumir-deodato.html"' not in s:
    card = ('<a class="story" href="eumir-deodato.html"><div class="art"><img width="323" height="325" src="img-deodato.jpg" alt="Pochette de Prelude de Deodato" loading="lazy" style="object-fit:cover"></div><div class="txt"><div class="who">Eumir Deodato</div><div class="meta">'
            + b("Arrangeur et producteur · né en 1942", "Arranger and producer · born 1942") + '</div><p class="hook">'
            + b("Un « 2001 » funk n°2 aux États-Unis, puis « Ladies’ Night » et « Celebration » pour Kool &amp; the Gang.", "A funk “2001” at US No. 2, then “Ladies’ Night” and “Celebration” for Kool &amp; the Gang.")
            + '</p><span class="more">' + b("Lire le portrait →", "Read the profile →") + "</span></div></a>\n")
    i = s.index('<section id="createurs"'); j = s.index('<div class="crate">', i) + len('<div class="crate">') + 1
    s = s[:j] + card + s[j:]
    s = s.replace('<a class="xt" href="#createurs"><b>11</b>', '<a class="xt" href="#createurs"><b>12</b>', 1)
    open(ROOT + "index.html", "w").write(s)
m = open(ROOT + "sitemap.xml").read()
if "eumir-deodato.html" not in m:
    open(ROOT + "sitemap.xml", "w").write(m.replace("</urlset>", "<url><loc>https://cheetahvinyl.com/eumir-deodato.html</loc><lastmod>2026-11-28</lastmod></url>\n</urlset>"))
print("ok")
