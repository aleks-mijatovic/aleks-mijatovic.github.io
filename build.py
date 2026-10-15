# -*- coding: utf-8 -*-
from pathlib import Path
from html import escape as e
import json,re
out=Path(__file__).resolve().parent
papers=json.loads((out/'papers.json').read_text());topics=json.loads((out/'topics.json').read_text());videos=json.loads((out/'videos.json').read_text())
nav=[('index','Home'),('research','Research'),('cv','CV'),('group','Group'),('videos','Videos')]
def page(name,title,content):
 links=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if p==name else '')+f'>{t}</a>' for p,t in nav)
 text=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Aleksandar Mijatović</title><meta name="description" content="Aleksandar Mijatović, Professor of Probability at the University of Warwick. Research, publications, CV, group and videos.">
<link rel="stylesheet" href="style.css">{('<script src="research.js" defer></script>' if name=='research' else '')}</head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><strong>Aleksandar Mijatović</strong><span>Probability and its applications</span></a><nav aria-label="Main navigation">{links}</nav></div></header>
<main id="main">{content}</main><footer><span>Aleksandar Mijatović · University of Warwick</span><a href="mailto:a.mijatovic@warwick.ac.uk">a.mijatovic@warwick.ac.uk</a></footer></body></html>'''
 (out/(name+'.html')).write_text(text)
def link(url,label,cls=''):return f'<a'+(f' class="{cls}"' if cls else '')+f' href="{e(url,quote=True)}">{e(label)}</a>'
profiles=[('https://arxiv.org/search/?searchtype=author&query=Mijatovi%C4%87%2C+A','arXiv'),('https://scholar.google.co.uk/citations?user=h6xcIUsAAAAJ&hl=en','Google Scholar'),('https://orcid.org/0000-0003-0531-3551','ORCID'),('https://www.researchgate.net/profile/Aleksandar-Mijatovic-3','ResearchGate'),('https://github.com/aleks-mijatovic','GitHub')]
page('index','Home',f'''<div class="home-layout"><div class="home-copy"><p class="eyebrow">University of Warwick</p><h1>Aleksandar Mijatović</h1><p class="lead">Professor of Probability</p><p>My research is in probability and its applications, including simulation and Monte Carlo methods, mathematical finance, numerical stochastics, and the foundations of machine learning, as well as analysis and geometry.</p><div class="actions">{link('research.html','Browse research →','button')}{link('cv.html','Curriculum vitae','button secondary')}</div><section class="home-block"><h2>Contact</h2><div class="contact-grid"><div><span class="label">Address</span><p>{link('https://warwick.ac.uk/fac/sci/statistics/','Department of Statistics')}<br>{link('https://warwick.ac.uk/','University of Warwick')}<br>Coventry, CV4 7AL, United Kingdom</p></div><div><span class="label">Email & office</span><p>{link('mailto:a.mijatovic@warwick.ac.uk','a.mijatovic@warwick.ac.uk')}<br>D0.14, Zeeman Building<br>{link('https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/mijatovic/','Warwick profile ↗')}</p></div></div></section><section class="home-block"><h2>Research in conversation</h2><p>On my YouTube channel, {link('https://www.youtube.com/channel/UCXSoLS_uKebYZ9GzgAF0ZsA','Prob-AM')}, I explain results and proofs from my research. {link('videos.html','Browse videos and slides →')}</p></section></div><aside class="profile"><img class="portrait" src="portrait.jpg" alt="Portrait of Aleksandar Mijatović" width="400" height="500"><div class="profile-links"><span class="label">Find my work</span>{''.join(link(u,t+' ↗') for u,t in profiles)}</div></aside></div><section class="topic-section"><h2>Explore by topic</h2><div class="topic-grid">{''.join(link('research.html?topic='+k,t+' →') for k,t in topics.items())}</div></section>''')
sections=list(dict.fromkeys(p['section'] for p in papers))
items=[]
for p in papers:
 tags=''.join(link('research.html?topic='+t,topics[t],'tag') for t in p['topics'])
 resources=''.join(link(l['url'],l['label']) for l in p['links'])
 items.append(f'''<article class="paper" id="{p['id']}" data-year="{p['year']}" data-section="{e(p['section'])}" data-topics="{' '.join(p['topics'])}"><div class="paper-meta"><span>{p['year']}</span><span>{e(p['section'])}</span></div><div class="paper-body"><h3>{e(p['title'])}</h3><p class="authors">{e(p['authors'])}</p>{('<p class="citation">'+e(p['citation'])+'</p>') if p['citation'] else ''}<div class="paper-links">{resources}</div><div class="tags">{tags}</div></div></article>''')
page('research','Research',f'''<div class="page-heading"><p class="eyebrow">Papers & publications</p><h1>Research</h1><p>Browse by topic, search by title or author, or explore the full list.</p></div><form class="filters" id="filters" role="search"><div class="filter-row"><label class="search-label">Search papers<input type="search" id="query" placeholder="Title, author or keyword…" autocomplete="off"></label><label>Type<select id="section"><option value="all">All research</option>{''.join('<option>'+e(s)+'</option>' for s in sections)}</select></label><label>Sort by<select id="sort"><option value="newest">Newest first</option><option value="oldest">Oldest first</option><option value="title">Title A–Z</option><option value="topic">Topic A–Z</option></select></label></div><fieldset><legend>Filter by topic</legend><div class="topic-filters"><button type="button" data-topic="all" aria-pressed="true">All topics <span>{len(papers)}</span></button>{''.join(f'<button type="button" data-topic="{k}" aria-pressed="false">{e(t)} <span>{sum(k in p["topics"] for p in papers)}</span></button>' for k,t in topics.items())}</div></fieldset><div class="filter-summary"><span id="result-count" role="status" aria-live="polite">{len(papers)} research entries</span><button type="reset" class="reset">Reset filters</button></div></form><noscript><p>All research is listed below. Enable JavaScript to search, filter and sort.</p></noscript><div id="papers">{''.join(items)}</div><p id="empty" class="empty" hidden>No papers match these filters. Try another topic or reset the filters.</p>''')
for name,title in [('cv','Curriculum vitae'),('group','Research group')]:
 content=(out/(name+'-content.html')).read_text()
 content=content[content.index('<h2' if name=='cv' else '<h3'):]
 content=re.sub(r'<a href="https://sites.google.com#.*?</a>','',content)
 if name=='group':
  content=content.replace('<h2>','<h4>').replace('</h2>','</h4>').replace('<h3>','<h2>').replace('</h3>','</h2>').replace('<h4>','<h3>').replace('</h4>','</h3>')
  content=content.replace('Brownain','Brownian')
 # Add local anchors and a compact contents navigation.
 def heading(m):
  text=re.sub('<[^>]+>','',m[1]);slug=re.sub('[^a-z0-9]+','-',text.lower()).strip('-');return f'<h2 id="{slug}">{m[1]}</h2>'
 content=re.sub(r'<h2>(.*?)</h2>',heading,content)
 headings=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',content)
 toc='<nav class="contents" aria-label="On this page">'+''.join(link('#'+i,re.sub('<[^>]+>','',h)) for i,h in headings)+'</nav>'
 page(name,title,f'<div class="page-heading"><p class="eyebrow">'+('Background & experience' if name=='cv' else 'People & collaboration')+f'</p><h1>{title}</h1></div>{toc}<div class="prose">{content}</div>')
rows=[]
for i,v in enumerate(videos):
 resources=link(v['url'],'Watch on YouTube ↗','button secondary')+''.join(link(s['url'],'Slides ↗','slide-link') for s in v['slides'])
 rows.append(f'<article class="video-row"><span class="video-index">{i+1:02}</span><div><h2>{e(v["title"])}</h2><div class="video-links">{resources}</div></div></article>')
page('videos','Research videos',f'<div class="page-heading"><p class="eyebrow">Prob-AM</p><h1>Research videos</h1><p>Results, ideas and proofs from my research, with accompanying slides.</p>{link("https://www.youtube.com/channel/UCXSoLS_uKebYZ9GzgAF0ZsA","Visit the Prob-AM channel ↗")}</div><div class="video-list">'+''.join(rows)+'</div>')
(out/'.nojekyll').touch()
print('Built 5 pages; 97 research entries; 34 videos.')
