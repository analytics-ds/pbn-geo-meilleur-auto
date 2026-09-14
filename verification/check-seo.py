"""Check rendered Hugo outputs. Usage: python3 verification/check-seo.py ROOT preview|production|articles"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys, json, xml.etree.ElementTree as ET
root=Path(sys.argv[1]).resolve(); mode=sys.argv[2]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta={}; self.links=[]; self.refs=[]; self.ids=set(); self.ld=[]; self.capture=None; self.h1=0; self.title=''
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='h1': self.h1+=1
        if 'id' in a:self.ids.add(a['id'])
        if t=='meta':self.meta.setdefault(a.get('name',a.get('property','')),[]).append(a.get('content',''))
        if t=='link':self.links.append(a)
        if t=='a' and a.get('href'):self.refs.append(a['href'])
        if t in ['img','script'] and a.get('src'):self.refs.append(a['src'])
        if t=='link' and a.get('rel') in ['stylesheet','icon']:self.refs.append(a['href'])
        if t=='script' and a.get('type')=='application/ld+json':self.capture=''
        if t=='title':self.in_title=True
    def handle_data(self,s):
        if self.capture is not None:self.capture+=s
        if getattr(self,'in_title',False):self.title+=s
    def handle_endtag(self,t):
        if t=='script' and self.capture is not None:
            item=json.loads(self.capture);self.ld.extend(item.get('@graph',[item]));self.capture=None
        if t=='title':self.in_title=False
pages={}
for f in root.rglob('*.html'):
    item=Page();item.feed(f.read_text());
    if item.h1:pages[f]=item
assert len(pages)>=6
home=pages[root/'index.html']
basepath=urlsplit(next(x['href'] for x in home.links if x.get('rel')=='canonical')).path

def local_path(path):
    decoded=unquote(path)
    if basepath!='/' and decoded.startswith(basepath):decoded=decoded[len(basepath):]
    return root/decoded.lstrip('/')
for f,page in pages.items():
    assert page.h1==1,(f,'H1')
    assert len(page.meta.get('description',[]))==1 and page.meta['description'][0],(f,'description')
    expected='index, follow' if mode=='production' and f.name!='404.html' else 'noindex, nofollow'
    assert page.meta.get('robots')==[expected],(f,'robots',page.meta.get('robots'))
    canon=[x['href'] for x in page.links if x.get('rel')=='canonical'];assert len(canon)==1
    host=urlsplit(canon[0]).hostname
    alts=[x for x in page.links if x.get('hreflang')]
    if f.name!='404.html':
        assert {a['hreflang'] for a in alts}=={'fr','en','x-default'},(f,'hreflang')
        assert '/en/' not in next(a['href'] for a in alts if a['hreflang']=='x-default'),(f,'x-default')
        for a in alts:
            dest=local_path(urlsplit(a['href']).path)/'index.html'
            assert dest in pages,(f,a)
            assert any(x.get('href')==canon[0] and x.get('hreflang') for x in pages[dest].links),(f,'reciprocity')
    types={x['@type'] for x in page.ld};assert {'Organization','WebSite'}<=types
    for crumb in [x for x in page.ld if x['@type']=='BreadcrumbList']:
        items=crumb['itemListElement'];assert [i['position'] for i in items]==list(range(1,len(items)+1))
        assert items[-1]['item']==canon[0]
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme and (u.scheme not in ['http','https'] or u.hostname!=host):continue
        target=local_path(u.path) if u.path.startswith('/') else f.parent/unquote(u.path)
        if not u.path:target=f
        elif target.is_dir() or u.path.endswith('/'):target=target/'index.html'
        target=target.resolve()
        if not target.exists() and mode=='articles' and len(sys.argv)>3:
            target=Path(sys.argv[3]).resolve()/target.relative_to(root)
        assert target.exists(),(f,'link',ref)
        if u.fragment and target in pages:assert u.fragment in pages[target].ids,(f,'fragment',ref)
for f in root.rglob('*.xml'):ET.parse(f)
for lang,prefix in [('fr',''),('en','en/')]:
    feed=ET.parse(root/prefix/'index.xml')
    entries=feed.findall('./channel/item')
    article_urls={next(x['href'] for x in page.links if x.get('rel')=='canonical') for file,page in pages.items() if 'BlogPosting' in {x['@type'] for x in page.ld} and (file.relative_to(root).parts[0]=='en')==(lang=='en')}
    assert len(entries)==min(30,len(article_urls)),(lang,'RSS count',len(entries),len(article_urls))
    assert {e.findtext('link') for e in entries}<=article_urls,(lang,'RSS non-article')
    assert (root/prefix/'llms.txt').exists()
if mode=='articles':
    for prefix in ['', 'en/']:
        page=pages[root/prefix/'blog/gabarit/index.html'];types={x['@type'] for x in page.ld}
        assert {'BlogPosting','FAQPage','BreadcrumbList'}<=types
else:
    assert not (root/'mentions-legales/index.html').exists()
    assert not (root/'verification').exists()
assert ('Allow: /' if mode=='production' else 'Disallow: /') in (root/'robots.txt').read_text()
print(f'{mode}: {len(pages)} pages, liens, métadonnées, schémas, hreflang, XML/RSS et robots : OK')
