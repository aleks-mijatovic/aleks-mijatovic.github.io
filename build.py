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
videos_by_paper={}
for video in videos:
 videos_by_paper.setdefault(video['paper_id'],[]).append(video)
def video_links(paper_id,include_slides=False):
 parts=videos_by_paper.get(paper_id,[])
 links=[]
 for i,v in enumerate(parts):
  suffix=' '+str(i+1) if len(parts)>1 else ''
  links.append(link(v['url'],'YouTube'+suffix))
  if include_slides:
   for slide in v['slides']:links.append(link(slide['url'],'Slides'+suffix))
 return links
items=[]
for p in papers:
 refs=[]
 for resource in p['links']:
  if 'arxiv.org' in resource['url']:
   refs.append(link(resource['url'],'arXiv:'+resource['url'].split('/abs/')[-1]))
 published=[l for l in p['links'] if l['label']=='Published version']
 if p['citation']:
  refs.append(link(published[0]['url'],p['citation']) if published else e(p['citation']))
 for resource in published[(1 if p['citation'] else 0):]:refs.append(link(resource['url'],'Journal'))
 refs.extend(video_links(p['id']))
 for resource in p['links']:
  url=resource['url']
  if 'arxiv.org' in url or resource['label']=='Published version':continue
  if 'youtu' in url:
   if p['id'] in videos_by_paper:continue
   refs.append(link(url,'YouTube' if resource['label'] in ['Video','YouTube'] else resource['label']))
  else:refs.append(link(url,resource['label']))
 authors='<span class="authors">'+e(p['authors'])+'</span>' if p['authors'] else ''
 citation=' · '.join(([authors] if authors else [])+refs)
 items.append(f'''<article class="paper" id="{p['id']}" data-year="{p['year']}" data-section="{e(p['section'])}" data-topics="{' '.join(p['topics'])}" data-topic-names="{e(' '.join(topics[t] for t in p['topics']))}" data-primary-topic="{e(topics[p['topics'][0]])}"><span class="paper-year">{p['year']}</span><div class="paper-body"><h3>{e(p['title'])}</h3><p class="citation">{citation}</p></div></article>''')
page('research','Research',f'''<div class="page-heading compact-heading"><h1>Research</h1></div><form class="filters" id="filters" role="search"><div class="filter-row"><label>Topic<select id="topic"><option value="all">All topics</option>{''.join('<option value="'+k+'">'+e(t)+'</option>' for k,t in topics.items())}</select></label><label>Type<select id="section"><option value="all">All research</option>{''.join('<option>'+e(s)+'</option>' for s in sections)}</select></label><label>Sort<select id="sort"><option value="newest">Newest first</option><option value="oldest">Oldest first</option><option value="title">Title A–Z</option><option value="topic">Topic A–Z</option></select></label><label class="search-label">Search<input type="search" id="query" placeholder="Title or author" autocomplete="off"></label></div><div class="filter-summary"><span id="result-count" role="status" aria-live="polite">{len(papers)} research entries</span><button type="reset" class="reset">Reset</button></div></form><noscript><p>All research is listed below. Enable JavaScript to filter and sort.</p></noscript><div id="papers">{''.join(items)}</div><p id="empty" class="empty" hidden>No papers match. Try another topic or reset.</p>''')
for name,title in [('cv','Curriculum vitae')]:
 content=(out/(name+'-content.html')).read_text()
 content=content[content.index('<h2'):]
 content=re.sub(r'<a href="https://sites.google.com#.*?</a>','',content)
 # Add local anchors and a compact contents navigation.
 def heading(m):
  text=re.sub('<[^>]+>','',m[1]);slug=re.sub('[^a-z0-9]+','-',text.lower()).strip('-');return f'<h2 id="{slug}">{m[1]}</h2>'
 content=re.sub(r'<h2>(.*?)</h2>',heading,content)
 headings=re.findall(r'<h2 id="([^"]+)">(.*?)</h2>',content)
 toc='<nav class="contents" aria-label="On this page">'+''.join(link('#'+i,re.sub('<[^>]+>','',h)) for i,h in headings)+'</nav>'
 page(name,title,f'<div class="page-heading"><p class="eyebrow">'+'Background & experience'+f'</p><h1>{title}</h1></div>{toc}<div class="prose">{content}</div>')
groups=json.loads((out/'group.json').read_text())['groups']
group_sections=[]
for group in groups:
 members=[]
 for person in group['members']:
  name=link(person['profile_url'],person['name']) if person['profile_url'] else e(person['name'])
  metadata=person['metadata_html'].replace('Brownain','Brownian')
  if person.get('image'):
   members.append(f'<article class="member"><img src="{e(person["image"])}" alt="{e(person["name"])}" width="160" height="180" loading="lazy"><div><h3>{name}</h3><p>{metadata}</p></div></article>')
  else:
   members.append('<article class="alumnus">'+metadata+'</article>')
 slug=re.sub('[^a-z0-9]+','-',group['title'].lower()).strip('-')
 layout='member-grid' if any(p.get('image') for p in group['members']) else 'alumni-grid'
 group_sections.append(f'<section id="{slug}" class="group-section"><h2>{e(group["title"])}</h2><div class="{layout}">'+''.join(members)+'</div></section>')
page('group','Research group','<div class="page-heading compact-heading"><h1>Research group</h1></div>'+''.join(group_sections))
papers_by_id={p['id']:p for p in papers}
rows=[]
for paper_id,parts in videos_by_paper.items():
 paper=papers_by_id[paper_id]
 watches=[];slides=[]
 for i,video in enumerate(parts):
  watches.append(link(video['url'],video['part_label']))
  for slide in video['slides']:
   label='Slides' if len(parts)==1 or sum(len(v['slides']) for v in parts)==1 else 'Part '+str(i+1)
   slides.append(link(slide['url'],label))
 rows.append(f'<tr data-paper="{paper_id}"><th scope="row">{link("research.html#"+paper_id,paper["title"])}</th><td>'+ ' · '.join(watches)+'</td><td>'+' · '.join(slides)+'</td></tr>')
page('videos','Research videos','<div class="page-heading compact-heading"><h1>Videos & presentations</h1>'+link('https://www.youtube.com/channel/UCXSoLS_uKebYZ9GzgAF0ZsA','Prob-AM on YouTube ↗')+'</div><table class="video-table"><thead><tr><th scope="col">Paper</th><th scope="col">YouTube</th><th scope="col">Presentation PDFs</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>')
(out/'.nojekyll').touch()
print(f'Built 5 pages; {len(papers)} research entries; {len(videos)} videos grouped under {len(videos_by_paper)} papers.')
