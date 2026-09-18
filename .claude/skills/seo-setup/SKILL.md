# Skill : SEO Setup

Ce skill met en place le socle SEO technique du site. Il se lance une fois a la creation, et peut etre relance pour mettre a jour les fichiers.

## Declenchement

L'utilisateur tape `/seo-setup` ou ce skill est appele automatiquement par `/create-site`.

## Sources des templates

Tous les fichiers de reference sont dans `.claude/templates/seo/`. **Toujours lire les templates a jour dans ce dossier avant de generer les fichiers.** Si l'utilisateur a modifie un template, utiliser sa version.

## Fichiers generes

### 1. robots.txt

- **Template** : `.claude/templates/seo/robots.txt`
- **Destination** : `static/robots.txt`
- Remplacer `{{BASE_URL}}` par le baseURL du site (lire `hugo.toml`)

### 2. llms.txt

- **Template** : `.claude/templates/seo/llms.txt`
- **Destination** : `static/llms.txt`
- Remplacer les variables avec les informations du site (lire le CLAUDE.md et les articles existants dans `content/blog/`)
- Variables a remplacer : `{{SITE_NAME}}`, `{{SITE_DESCRIPTION}}`, `{{SITE_ABOUT}}`, `{{CATEGORIES_LIST}}`, `{{RECENT_ARTICLES}}`, `{{BASE_URL}}`

### 3. Configuration sitemap

Dans `hugo.toml`, verifier/ajouter :

```toml
[sitemap]
  changefreq = 'weekly'
  filename = 'sitemap.xml'
  priority = 0.5
```

Hugo genere automatiquement le `sitemap.xml` au build. La balise `<lastmod>` de chaque page utilise le champ `lastmod` du frontmatter (ou `date` si absent).

**IMPORTANT pour le sitemap XML :**
- Hugo utilise le champ `lastmod` du frontmatter pour la balise `<lastmod>` dans le sitemap XML
- Si `lastmod` est absent, Hugo utilise `date`
- Quand on modifie un article, il faut mettre a jour le champ `lastmod` dans le frontmatter

### 4. Sitemap HTML

- **Template** : `.claude/templates/layouts/sitemap-html.html`
- **Destination** : `themes/[theme]/layouts/_default/sitemap-html.html`
- **Page de contenu** : `content/plan-du-site.md`

Le sitemap HTML est une page visible du site qui liste toutes les pages par categorie avec la date de derniere modification. Utile pour :
- Les visiteurs qui cherchent une page
- Le maillage interne (chaque page du site est linkee)
- Le crawl des bots (point d'entree vers toutes les pages)

Pour le mettre en place :

1. Copier le template dans le theme :
```bash
cp .claude/templates/layouts/sitemap-html.html themes/[theme]/layouts/_default/sitemap-html.html
```

2. Creer la page de contenu :
```markdown
---
title: "Plan du site"
layout: "sitemap-html"
description: "Retrouvez toutes les pages et articles de [NOM DU SITE]"
---
```
Ecrire ce fichier dans `content/plan-du-site.md`.

3. Ajouter un lien dans le footer vers `/plan-du-site/`

Le sitemap HTML se met a jour automatiquement a chaque build Hugo (il boucle sur toutes les pages du site). La date affichee utilise `lastmod` si present, sinon `date`.

### 5. Configuration RSS

Dans `hugo.toml`, verifier/ajouter :

```toml
[outputs]
  home = ['html', 'rss']
  section = ['html', 'rss']
```

### 6. Partial SEO head

- **Template** : `.claude/templates/partials/seo-head.html`
- **Destination** : `themes/[theme]/layouts/partials/seo-head.html`
- Doit etre inclus dans `baseof.html` via `{{ partial "seo-head.html" . }}`

Ce partial genere automatiquement :
- Balise canonical
- Open Graph (og:title, og:description, og:type, og:url, og:image, article:author, article:tag)
- Twitter Card
- JSON-LD BlogPosting avec auteur (sur les articles)
- JSON-LD BreadcrumbList (sur les articles)
- JSON-LD WebSite (sur l'accueil)
- JSON-LD Organization (sur l'accueil)

### 7. Configuration auteur et parametres SEO avances

Dans `hugo.toml`, section `[params]`, verifier/ajouter les informations auteur et les parametres SEO :

```toml
[params]
  # ... autres params ...
  author_name = "[Nom de l'auteur]"
  author_url = "[URL profil/site de l'auteur]"
  author_job_title = "[Titre/fonction]"
  default_og_image = "/images/og-default.jpg"
  logo = "/favicon.svg"
  founding_year = "[ANNEE]"
  expertise = ["[DOMAINE 1]", "[DOMAINE 2]", "[DOMAINE 3]"]
  # og_locale_alternate = "en_US"  # decommenter si site multilingue
```

Ces valeurs sont utilisees par le partial `seo-head.html` pour generer :
- Le schema Person (auteur) dans le JSON-LD des articles
- Le schema Organization avec `@id` pour referencement croise entre schemas
- Les meta tags `og:image` (avec dimensions 1200x630) et `og:locale:alternate`
- La meta `article:section` pour la categorie
- Le schema FAQPage JSON-LD automatiquement depuis le frontmatter `faq` des articles

### 8. Page 404

Verifier que le layout 404 est en place :
- `themes/[theme]/layouts/404.html` existe
- Il contient des liens vers l'accueil et le blog

### 9. Favicon

Verifier que `static/favicon.svg` existe. Le partial `seo-head.html` le reference automatiquement via `<link rel="icon" type="image/svg+xml">`.

### 10. Configuration articles similaires

Dans `hugo.toml`, verifier/ajouter la configuration des articles similaires :

```toml
[related]
  includeNewer = true
  threshold = 80
  [[related.indices]]
    name = "categories"
    weight = 100
  [[related.indices]]
    name = "tags"
    weight = 80
```

### 11. Configuration table des matieres

Dans `hugo.toml`, verifier/ajouter :

```toml
[markup]
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 3
    ordered = true
```

## Donnees structurees additionnelles

Les templates JSON-LD sont dans `.claude/templates/seo/structured-data/`. Schemas disponibles :

| Schema | Fichier | Integre par defaut |
|--------|---------|-------------------|
| BlogPosting | `article.json` | Oui (dans seo-head.html) |
| Organization | `organization.json` | Oui (dans seo-head.html) |
| Person (auteur) | `author.json` | Oui (dans seo-head.html) |
| BreadcrumbList | `breadcrumb.json` | Oui (dans seo-head.html) |
| WebSite | `website.json` | Oui (dans seo-head.html) |
| FAQPage | `faq.json` | Non — a integrer via `/seo` si besoin |

Pour ajouter un nouveau schema :
1. Creer le fichier `.json` dans `.claude/templates/seo/structured-data/`
2. Utiliser `/seo` pour demander l'integration dans le partial `seo-head.html`

## Mise a jour

Ce skill peut etre relance pour :
- Mettre a jour le `llms.txt` avec les nouveaux articles
- Verifier la coherence du `robots.txt` avec le baseURL
- Ajouter les outputs RSS si manquants
- Mettre a jour les informations auteur

## Verification

Apres execution :
- [ ] `static/robots.txt` existe, contient le bon sitemap URL
- [ ] `static/llms.txt` existe, decrit correctement le site et liste les articles
- [ ] `hugo.toml` contient la config sitemap, RSS, auteur, articles similaires, TOC et params SEO avances
- [ ] Le sitemap HTML est en place (`content/plan-du-site.md` + layout)
- [ ] Le partial `seo-head.html` est present et inclus dans `baseof.html`
- [ ] Le layout `404.html` est present dans le theme
- [ ] `static/favicon.svg` existe
- [ ] Le `baseof.html` contient le lien skip-to-content et le `main#main-content`
- [ ] Les Google Fonts sont charges en non-bloquant (`media="print"` + swap JS)
- [ ] Build Hugo OK (`hugo`)
