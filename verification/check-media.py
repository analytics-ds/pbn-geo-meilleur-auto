"""Build an isolated editorial fixture with 13 posts per language. Never writes live content."""
from pathlib import Path
import tempfile,shutil,subprocess,json,re
p=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='meilleur-auto-media-test-') as temp:
    t=Path(temp);shutil.copytree(p/'content',t/'content',ignore=lambda directory,names: [n for n in names if n!='_index.md'] if Path(directory).name=='blog' else [])
    for lang in ['fr','en']:
        for i in range(1,14):
            (t/f'content/{lang}/blog/controle-{i:02}.md').write_text('---\n'+ '\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in dict(title=f'Article de contrôle {i:02}',description='Fixture éditoriale hors publication.',date=f'2026-08-{i:02}',lastmod=f'2026-08-{i:02}',author='redaction-meilleur-auto',translationKey=f'controle-{i:02}',categories=['Modeles et comparatifs'],image='images/route-alpine.jpg',imageAlt='Photo de contrôle').items())+'\n---\n\n## Section de contrôle\n\nTexte de test hors publication.\n')
    config=t/'fixture.toml';config.write_text(f'baseURL = "https://example.invalid/"\n[languages.fr]\ncontentDir = "{t}/content/fr"\n[languages.en]\ncontentDir = "{t}/content/en"\n')
    subprocess.run(['/opt/homebrew/bin/hugo','--source',str(p),'--config',str(p/'hugo.toml')+','+str(config),'--destination',str(t/'public'),'--minify'],check=True,capture_output=True)
    for lang,prefix,author,category in [('fr','','auteurs/la-redaction/','categories/achat/'),('en','en/','authors/editorial-team/','categories/buying/')]:
        def html(path):return (t/'public'/prefix/path/'index.html').read_text()
        archive=html('archives');assert archive.count('class=archive-row')==13,(lang,'archive')
        byline=html(author);assert byline.count('class=journal-card')==13,(lang,'author')
        for section in ['blog/',category]:
            first=html(section);second=html(section+'page/2/')
            assert first.count('class=journal-card')==12,(lang,section,'page1')
            assert second.count('class=journal-card')==1,(lang,section,'page2')
            expected='https://example.invalid/'+prefix+section+'page/2/'
            assert 'rel=canonical href='+expected in second,(lang,section,'canonical',expected)
            assert '| Page 2</title>' in second,(lang,section,'title')
        article=html('blog/controle-13');assert 'rel=author' in article and prefix+author in article
        home=(t/'public'/prefix/'index.html').read_text();assert 'Article de contrôle 13' in home
        print(lang+': une, 13 archives, 13 contributions auteur, pagination 12+1 et canonical page 2 : OK')
print('Fixtures temporaires nettoyées ; aucun article ajouté au site.')
