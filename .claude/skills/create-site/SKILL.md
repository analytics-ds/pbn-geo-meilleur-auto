# Skill : Creer un site

Ce skill genere un site Hugo complet a partir des reponses de l'utilisateur.

## Declenchement

L'utilisateur tape `/create-site` ou demande de creer un nouveau site.

## Etape 1 — Collecter les informations

Poser les questions suivantes a l'utilisateur. Attendre ses reponses avant de continuer.

### Questions obligatoires

1. **Nom du site** : Comment s'appelle le site ? (ex: "Mamie-The", "Mon Blog Voyage")
2. **Description courte** : En une phrase, de quoi parle le site ? (ex: "Un blog sur l'univers du the")
3. **Categories du blog** : Quelles sont les grandes categories d'articles ? (ex: "Thes verts, Thes noirs, Tisanes, Rituels et Conseils")
   - **IMPORTANT :** Ne JAMAIS utiliser le caractere `&` dans les noms de categories. Toujours le remplacer par "et". Hugo supprime le `&` lors de la generation du slug URL mais laisse un double espace, ce qui cree un double tiret `--` dans l'URL. Les liens du menu pointent vers un slug avec un seul tiret → 404. Si l'utilisateur propose un nom avec `&`, le remplacer automatiquement par "et".
   - **Les categories seront AUTOMATIQUEMENT traduites en anglais** par Claude pour alimenter la version EN du site (voir etape 5)
4. **Charte graphique** : Deux options :
   - L'utilisateur fournit un screenshot ou une URL de reference → s'en inspirer
   - L'utilisateur decrit l'ambiance → proposer une palette de couleurs adaptee
5. **Langue principale** : Francais (fr), Anglais (en), autre ?
   - **IMPORTANT — multilingue automatique** : quelle que soit la langue principale choisie, le site sera TOUJOURS bilingue avec une version anglaise en sous-dossier `/en/`. Si la langue principale est deja l'anglais, c'est l'anglais qui reste principal (pas de duplication). Si c'est une autre langue (ex: francais), un cocon EN complet est genere automatiquement en parallele (catégories traduites, articles placeholder traduits, language switcher, hreflang). Ne JAMAIS demander de confirmation pour la version EN, c'est systematique

### Questions optionnelles

6. **Domaine cible** : Y a-t-il deja un nom de domaine prevu ? (pour configurer le baseURL)
7. **Logo** : Y a-t-il un logo a integrer ?
8. **Pages supplementaires** : Au-dela du blog, faut-il des pages statiques ? (A propos, Contact, etc.)
9. **Design Figma** : As-tu un design Figma (URL ou code HTML exporte) a utiliser comme base pour le layout du site ?
   - Si oui, recuperer le code via le MCP Figma (`get_design_context`) ou demander a l'utilisateur de coller le HTML exporte
   - Ce HTML servira de **reference visuelle et structurelle** a l'etape 4 pour creer les templates Hugo

## Etape 2 — Scaffolder Hugo et nettoyer les fichiers par defaut

Une fois les reponses collectees :

```bash
hugo new site . --force
hugo new theme [nom-du-theme-en-slug]
```

Le `--force` permet de scaffolder dans le repertoire courant (qui contient deja `.claude/`).

**IMPORTANT — Nettoyage obligatoire apres le scaffold :**

La commande `hugo new theme` genere des fichiers par defaut (templates quasi vides, config parasite) qui **entrent en conflit** avec nos templates custom. Il faut les supprimer AVANT de copier nos fichiers.

```bash
# Supprimer TOUS les layouts par defaut generes par le scaffold
rm -rf themes/[nom-du-theme]/layouts/*
rm -rf themes/[nom-du-theme]/assets/*

# Supprimer le hugo.toml du theme (il interfere avec le hugo.toml principal)
rm -f themes/[nom-du-theme]/hugo.toml

# Supprimer le archetype par defaut du theme (on utilise celui a la racine)
rm -f themes/[nom-du-theme]/archetypes/default.md
```

Apres ce nettoyage, le dossier du theme doit etre quasiment vide. On va le remplir avec nos propres fichiers a l'etape 4.

**Pourquoi :** Hugo a un systeme de priorite pour les templates. Si un fichier `index.html` existe dans le theme, il prend la priorite sur notre `home.html`. Si le `hugo.toml` du theme existe, il peut ecraser des parametres du `hugo.toml` principal. Le nettoyage elimine toute ambiguite.

## Etape 3 — Configurer hugo.toml (multilingue FR + EN obligatoire)

Creer le fichier `hugo.toml` **a la racine du projet** (PAS dans le theme) avec la configuration multilingue Hugo native.

**Structure obligatoire :**

```toml
baseURL = "https://..."
title = "[NOM_DU_SITE]"
theme = "[slug-du-theme]"

defaultContentLanguage = "[LANGUE_PRINCIPALE_CODE]"   # ex: "fr"
defaultContentLanguageInSubdir = false                 # langue principale a la racine, pas dans un sous-dossier

[languages]
  [languages.fr]   # OU la langue principale choisie
    locale = "fr-FR"          # NB: "locale" (pas "languageCode", deprecie depuis Hugo 0.158)
    label = "Francais"        # NB: "label" (pas "languageName", deprecie depuis Hugo 0.158)
    weight = 1
    title = "[NOM_DU_SITE]"
    contentDir = "content/fr" # langue principale dans content/fr/ : evite que content/en soit avale par la langue par defaut
    [languages.fr.params]
      description = "[DESCRIPTION_FR]"

  [languages.en]   # TOUJOURS present, meme si la langue principale est autre chose que FR
    locale = "en-US"
    label = "English"
    weight = 2
    title = "[NOM_DU_SITE]"   # peut rester le meme ou etre traduit
    contentDir = "content/en"
    [languages.en.params]
      description = "[DESCRIPTION_EN — traduction automatique de DESCRIPTION_FR]"

[taxonomies]
  category = "categories"
  tag = "tags"

# Menu langue principale (ex: FR)
[[languages.fr.menus.main]]
  name = "Accueil"
  url = "/"
  weight = 1
[[languages.fr.menus.main]]
  name = "[Categorie 1 en FR]"
  url = "/categories/[slug-fr]/"
  weight = 2
# ... repeter pour chaque categorie
[[languages.fr.menus.main]]
  name = "Le Blog"
  url = "/blog/"
  weight = 99

# Menu EN (TOUJOURS present)
[[languages.en.menus.main]]
  name = "Home"
  url = "/en/"
  weight = 1
[[languages.en.menus.main]]
  name = "[Category 1 en EN — traduit]"
  url = "/en/categories/[slug-en]/"
  weight = 2
# ... repeter pour chaque categorie
[[languages.en.menus.main]]
  name = "The Blog"
  url = "/en/blog/"
  weight = 99

[params]
  # Parametres globaux (non lies a une langue)
  # couleurs, polices, etc.
```

**Regles importantes :**
- `defaultContentLanguage` = la langue choisie par le consultant (cette langue est servie a la racine du domaine `/`)
- La langue EN est **TOUJOURS** configuree, meme si la principale est autre chose que FR
- Si la langue principale est deja EN, ne pas dupliquer (pas besoin de `[languages.en]` en plus)
- Pour chaque categorie, generer le slug FR **et** le slug EN traduit
- Il ne doit y avoir qu'UN SEUL `hugo.toml`, a la racine. Jamais dans le dossier du theme

**Traduction automatique des categories** : Claude traduit les noms de categories du francais (ou autre) vers l'anglais, avec un vocabulaire SEO approprie. Exemples :
- "Thes verts" → "Green teas"
- "Rituels et Conseils" → "Rituals and Tips"
- "Sante naturelle" → "Natural health"

## Etape 4 — Creer le theme

Recreer la structure de dossiers dans le theme nettoye :

```bash
mkdir -p themes/[nom-du-theme]/layouts/_default
mkdir -p themes/[nom-du-theme]/layouts/partials
mkdir -p themes/[nom-du-theme]/assets/css
```

Lire les templates dans `.claude/templates/` et les adapter avec les informations de l'utilisateur.

### Si un design Figma a ete fourni (etape 1, question 9)

Le HTML Figma sert de **reference visuelle** pour la creation des templates Hugo. Le workflow est :

1. **Analyser le HTML Figma** : identifier la structure (header, footer, grille, typographie, couleurs, espacement)
2. **Extraire les styles** : couleurs, polices, tailles, spacings → les reporter dans les variables CSS de `main.css`
3. **Traduire la structure en templates Hugo** : adapter le HTML statique de Figma en templates dynamiques Hugo en remplacant le contenu statique par les variables Hugo (`{{ .Title }}`, `{{ .Content }}`, `{{ range }}`, etc.)
4. **Ne PAS copier le HTML Figma tel quel** : il faut le decomposer en `baseof.html`, `header.html`, `footer.html`, `home.html`, `single.html`, `list.html` selon la logique Hugo

Les templates dans `.claude/templates/layouts/` servent toujours de **base structurelle** (variables Hugo, boucles, logique conditionnelle). Le design Figma vient **habiller** cette base.

Si aucun design Figma n'a ete fourni, utiliser les templates tels quels avec les couleurs/polices choisies par l'utilisateur.

### CSS (main.css)

Lire `.claude/templates/main.css`, remplacer les variables CSS custom properties avec les couleurs choisies, puis ecrire le resultat dans `themes/[nom-du-theme]/assets/css/main.css` :

- `--primary` : couleur principale
- `--primary-light` : variante claire de la couleur principale
- `--background` : couleur de fond
- `--background-alt` : variante du fond (sections alternees)
- `--accent` : couleur d'accent
- `--cta` : couleur des boutons/CTA
- `--cta-hover` : couleur hover des boutons
- `--text` : couleur du texte
- `--text-light` : couleur du texte secondaire
- `--border` : couleur des bordures

Choisir les polices Google Fonts adaptees a l'univers du site et mettre a jour les variables `--font-heading`, `--font-body`, `--font-ui` :
- Police titres : serif bold (Playfair Display, Merriweather, Lora...)
- Police corps : serif lisible (Lora, Source Serif Pro, Libre Baskerville...)
- Police UI : sans-serif (Inter, DM Sans, Work Sans...)

### Layouts

Lire chaque template depuis `.claude/templates/layouts/` et `.claude/templates/partials/`, les adapter, puis les ecrire aux bons emplacements :

| Source (template) | Destination (theme) |
|-------------------|-------------------|
| `.claude/templates/layouts/baseof.html` | `themes/[theme]/layouts/_default/baseof.html` |
| `.claude/templates/layouts/home.html` | `themes/[theme]/layouts/_default/home.html` |
| `.claude/templates/layouts/list.html` | `themes/[theme]/layouts/_default/list.html` |
| `.claude/templates/layouts/single.html` | `themes/[theme]/layouts/_default/single.html` |
| `.claude/templates/layouts/sitemap-html.html` | `themes/[theme]/layouts/_default/sitemap-html.html` |
| `.claude/templates/partials/header.html` | `themes/[theme]/layouts/partials/header.html` |
| `.claude/templates/partials/footer.html` | `themes/[theme]/layouts/partials/footer.html` |
| `.claude/templates/partials/seo-head.html` | `themes/[theme]/layouts/partials/seo-head.html` |
| `.claude/templates/layouts/404.html` | `themes/[theme]/layouts/404.html` |

**IMPORTANT :** Le fichier `home.html` doit etre place dans `layouts/_default/home.html`. NE PAS creer de fichier `index.html` dans `layouts/` — cela causerait un conflit de priorite avec Hugo.

Adapter dans chaque fichier :
- Le contenu du hero de la homepage (titre, description, badge, CTA)
- Les URLs des polices Google Fonts dans baseof.html (chargement non-bloquant via `media="print"` + swap JS)
- Le footer (nom du site, description)
- Le lien skip-to-content dans baseof.html (adapter le texte si site en anglais)
- Le layout 404.html (adapter le texte si site en anglais)

### SEO Head partial
Le partial `seo-head.html` genere automatiquement :
- Balise canonical
- Open Graph (og:title, og:description, og:type, og:url, og:image)
- Twitter Card
- JSON-LD (schema.org) pour les articles de blog (BlogPosting)

## Etape 4.5 — Installer les auteurs par defaut

Tous les sites crees a partir de ce template partagent les memes auteurs fictifs (6 personas unifies avec bios, expertises, topics).

### Copier le fichier authors.yaml

```bash
mkdir -p data
cp .claude/templates/data/authors.yaml data/authors.yaml
```

Ce fichier contient les 6 auteurs : Thomas Durand (tech), Magalie Ergoz (mode/beaute), Claire Beaumont (maison), Laura Verdier (sante), Kevin Moreau (transport), Sophie Martin (finance). Hugo le lit nativement via `.Site.Data.authors`.

### Copier les avatars

Les avatars sont des illustrations WebP 512x512 placees dans `static/images/authors/`. Les prompts de generation sont documentes dans `.claude/templates/data/avatar-prompts.md`.

```bash
mkdir -p static/images/authors
# Copier les avatars s'ils existent deja dans le template
if [ -d ".claude/templates/images/authors" ]; then
    cp .claude/templates/images/authors/*.webp static/images/authors/ 2>/dev/null || true
fi
```

Si les fichiers avatars ne sont pas encore presents dans le template, informer le consultant :
> "Les avatars des 6 auteurs sont a generer manuellement via un generateur AI (Midjourney, DALL-E). Les prompts sont dans `.claude/templates/data/avatar-prompts.md`. Une fois generes, placer les fichiers WebP dans `static/images/authors/[id].webp`."

Le site fonctionne meme sans les avatars (fallback placeholder avec 1ere lettre du nom), mais les avatars renforcent l'E-E-A-T et la credibilite aupres des LLMs et des lecteurs.

## Etape 5 — Creer le contenu initial (FR + EN en parallele)

Tout le contenu est genere **dans les deux langues en parallele**, via des dossiers de langue declares par `contentDir` dans `hugo.toml`.

**Structure choisie** : un dossier par langue sous `content/`.
- Langue principale (ex: FR) : `content/fr/` (servi a la racine du domaine `/` grace a `defaultContentLanguageInSubdir = false`)
- Langue EN : `content/en/` (servi sous `/en/`)

**IMPORTANT** : la langue principale va dans `content/fr/`, **PAS** directement dans `content/`. Sinon Hugo considere `content/en/` comme faisant partie de la langue par defaut (les pages EN n'apparaissent pas comme une vraie langue, et sont absentes des sitemaps). C'est pour cela que chaque langue declare explicitement son `contentDir`.

**Regle de liaison** : chaque article/page a un champ `translationKey` identique entre les versions FR et EN. C'est ce qui permet a Hugo de generer les liens hreflang et le language switcher.

### Page d'accueil
Creer :
- `content/fr/_index.md` avec frontmatter FR + `translationKey: "home"`
- `content/en/_index.md` avec frontmatter EN traduit + `translationKey: "home"`

### Page liste blog
Creer :
- `content/fr/blog/_index.md` avec `translationKey: "blog-index"`
- `content/en/blog/_index.md` avec `translationKey: "blog-index"` + traduction

### Pages categories
Pour **chaque categorie**, creer :
- `content/fr/categories/[slug-fr]/_index.md` (si nommage taxonomy manuel) OU laisser Hugo gerer auto
- La version EN est creee automatiquement par Hugo via la config `[languages.en]`
- Les `_index.md` de categorie peuvent contenir une description optimisee (SEO)

### Page plan du site (sitemap HTML)
Creer les deux versions :
```markdown
---
title: "Plan du site"
layout: "sitemap-html"
description: "Retrouvez toutes les pages et articles de [NOM DU SITE]"
translationKey: "sitemap"
---
```
Et la version EN `content/en/plan-du-site.md` (ou `site-map.md` avec slug traduit).

### Page 404
Copier `.claude/templates/layouts/404.html` vers `themes/[theme]/layouts/404.html`. Hugo utilise automatiquement ce layout pour les pages introuvables. Le template 404 doit detecter la langue via `{{ .Site.Language.Lang }}` pour afficher le message en FR ou EN.

### Favicon
Creer ou copier un fichier `static/favicon.svg` (logo du site en SVG). Si l'utilisateur n'a pas de logo, generer un simple SVG avec la premiere lettre du nom du site sur un fond colore.

### Articles placeholder (FR + EN en parallele)

Pour chaque categorie, creer **2-3 articles placeholder en FR ET leur traduction EN**. Structure :
- FR : `content/fr/blog/slug-fr.md`
- EN : `content/en/blog/slug-en.md` (slug traduit)

Chaque paire FR/EN partage le meme `translationKey` (ex: `translationKey: "article-bienfaits-the-vert"`).

Les articles doivent etre courts (300-500 mots) mais correctement structures :
- Frontmatter complet (`date`, `lastmod`, `categories` dans la langue de l'article, `tags` traduits, `translationKey`, `faq` avec 3+ questions, `image` + `imageAlt` + `imageCredit`)
- `author: [ID-AUTEUR]` (slug qui correspond a une cle de `data/authors.yaml`, ex: `thomas-durand`). Selectionner l'auteur le plus pertinent selon la thematique du site (ex: blog tech → Thomas Durand, blog maison → Claire Beaumont). Voir la regle de selection automatique documentee dans `/create-article-geo`
- H2/H3 descriptifs
- Un tableau ou une liste
- `draft: false`
- **En bref en liste numerotee** (regle GEO)
- **1ere question FAQ = mot-cle principal reformule**

Les articles EN sont des **traductions fideles** des FR, pas des textes differents. Claude traduit avec un vocabulaire SEO anglais approprie et adapte les exemples culturels si necessaire.

## Etape 6 — Fichiers SEO techniques

Lancer le skill `/seo-setup` pour generer :
- `static/robots.txt`
- `static/llms.txt`
- Configuration du sitemap XML dans `hugo.toml`
- Sitemap HTML (layout + page de contenu deja crees aux etapes 4 et 5)
- Le partial `seo-head.html` est deja dans le theme

## Etape 7 — Configurer le deploiement

Copier `.claude/templates/hugo-workflow.yml` vers `.github/workflows/hugo.yml`.

Creer le `.gitignore` :
```
public/
resources/
.hugo_build.lock
.DS_Store
```

## Etape 8 — Configurer hugo.toml avec les parametres SEO avances

Ajouter dans la section `[params]` de `hugo.toml` les parametres SEO supplementaires :

```toml
[params]
  # ... params existants ...
  default_og_image = "/images/og-default.jpg"
  logo = "/favicon.svg"
  founding_year = "[ANNEE]"
  expertise = ["[DOMAINE 1]", "[DOMAINE 2]", "[DOMAINE 3]"]
  # og_locale_alternate = "en_US"  # decommmenter si site multilingue
```

Creer une image OG par defaut `static/images/og-default.jpg` (1200x630px) avec le nom du site et le slogan. Si pas possible, noter dans le CLAUDE.md qu'il faut en ajouter une.

Activer les articles similaires dans hugo.toml :

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

Activer la table des matieres :

```toml
[markup]
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 3
    ordered = true
```

## Etape 9 — Mettre a jour le CLAUDE.md

Remplir la section "Contexte du site" du CLAUDE.md avec toutes les informations collectees :
- Nom du site
- Description (FR + EN)
- URL (GitHub Pages ou domaine custom)
- Couleurs (codes hex)
- Polices choisies
- Categories (mapping FR ↔ EN obligatoire, ex: "Thes verts / Green teas")
- Langue principale (la langue secondaire EN est toujours active)
- **Auteur principal du site** : ID de l'auteur (dans `data/authors.yaml`) le plus pertinent pour la thematique du site. Ex: pour un blog tech, `thomas-durand`. Cet auteur sera utilise par defaut pour les articles, mais `/create-article-geo` peut selectionner dynamiquement un autre auteur selon le sujet specifique de chaque article

## Etape 10 — Build de verification

```bash
hugo
```

Verifier qu'il n'y a aucune erreur. Afficher le nombre de pages generees.

Proposer a l'utilisateur de lancer le serveur local pour voir le resultat :
```bash
hugo server
```

## Etape 11 — Recapitulatif

Afficher a l'utilisateur :
- Le resume de ce qui a ete cree (nombre de fichiers, articles, categories)
- L'URL locale pour voir le site (`http://localhost:1313/`)
- Les prochaines etapes (push sur GitHub, activer GitHub Pages)
- Comment creer de nouveaux articles (`/create-article-geo`)
