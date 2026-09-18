# Skill : Mode SEO

Ce skill active un mode conversationnel pour effectuer des modifications SEO techniques sur le site.

## Declenchement

L'utilisateur tape `/seo` ou demande de modifier/ajouter des elements SEO.

## Comportement

Ce skill n'est PAS un workflow lineaire comme les autres. C'est un mode interactif :

1. Claude lit l'etat actuel du site (hugo.toml, templates, fichiers SEO existants)
2. Claude demande a l'utilisateur ce qu'il veut faire
3. Claude execute la modification
4. Claude reste en mode SEO pour d'autres demandes

## Actions possibles

### Fichiers SEO techniques

| Action | Fichiers concernes |
|--------|-------------------|
| Creer/modifier robots.txt | `static/robots.txt` |
| Creer/modifier llms.txt | `static/llms.txt` — lire le template dans `.claude/templates/seo/robots.txt` et `.claude/templates/seo/llms.txt` |
| Configurer le sitemap | `hugo.toml` section `[sitemap]` |
| Configurer le RSS | `hugo.toml` section `[outputs]` |

### Meta tags et balises

| Action | Fichiers concernes |
|--------|-------------------|
| Modifier les meta tags | `themes/[theme]/layouts/partials/seo-head.html` |
| Ajouter Open Graph / Twitter Card | `themes/[theme]/layouts/partials/seo-head.html` |
| Modifier la balise canonical | `themes/[theme]/layouts/partials/seo-head.html` |
| Ajouter des hreflang (multilingue) | `themes/[theme]/layouts/partials/seo-head.html` |

### Donnees structurees (JSON-LD)

Les schemas disponibles sont dans `.claude/templates/seo/structured-data/`. Pour ajouter un nouveau schema :

1. Lire le template JSON-LD dans `.claude/templates/seo/structured-data/`
2. L'adapter avec les donnees du site
3. L'integrer dans `seo-head.html` avec les conditions Hugo appropriees

**Schemas disponibles par defaut :**

| Schema | Fichier template | Utilise sur |
|--------|-----------------|-------------|
| BlogPosting | `article.json` | Pages articles (`single.html`) |
| Organization | `organization.json` | Toutes les pages |
| Person (auteur) | `author.json` | Pages articles |
| FAQPage | `faq.json` | Articles avec section FAQ |
| BreadcrumbList | `breadcrumb.json` | Toutes les pages sauf accueil |
| WebSite | `website.json` | Page d'accueil uniquement |

**Pour ajouter un schema custom :** l'utilisateur peut creer un fichier `.json` dans `.claude/templates/seo/structured-data/` puis demander via `/seo` de l'integrer. Claude lit le fichier et l'ajoute au partial `seo-head.html`.

### Cocon semantique

Le cocon semantique est la strategie d'architecture de contenu du site. Les categories du blog sont les piliers du cocon.

#### Creation et gestion du cocon

| Action | Description |
|--------|------------|
| Creer une categorie | Creer le dossier `content/blog/[categorie]/` avec un fichier `_index.md` optimise (title, meta description, contenu d'introduction). Ajouter la categorie dans le menu principal (`hugo.toml` section `[[menus.main]]`). Mettre a jour le CLAUDE.md section "Contexte du site" > Categories |
| Renommer une categorie | Renommer le dossier, mettre a jour le `_index.md`, le menu dans `hugo.toml`, les frontmatters des articles concernes et le CLAUDE.md |
| Supprimer une categorie | Deplacer les articles vers une autre categorie (demander laquelle), supprimer le dossier, retirer du menu et du CLAUDE.md. Ne jamais supprimer une categorie qui contient des articles sans les redistribuer |
| Reorganiser le cocon | Revoir l'architecture des categories. Lister les categories actuelles avec le nombre d'articles, proposer des fusions, des scissions ou de nouvelles categories en fonction de la couverture semantique |

#### Audit du cocon

| Action | Description |
|--------|------------|
| Audit cocon complet | Lister toutes les categories, compter les articles par categorie, identifier les categories sous-alimentees et les desequilibres |
| Couverture semantique | Pour chaque categorie, lister les mots-cles couverts par les articles existants et identifier les trous (sujets manquants) |
| Matrice de maillage | Generer une matrice montrant les liens internes entre articles. Identifier les articles orphelins (0 lien entrant) et les articles sans lien sortant |

#### Optimisation des pages categories

| Action | Description |
|--------|------------|
| Optimiser une page categorie | Verifier/ajouter le title, la meta description et le contenu d'introduction de la page categorie (`content/blog/[categorie]/_index.md`). Le title doit contenir le mot-cle principal de la categorie |
| Creer une page categorie | Si `_index.md` n'existe pas pour une categorie, le creer avec un contenu optimise (description, introduction, maillage vers les articles cles) |

#### Maillage interne du cocon

| Action | Description |
|--------|------------|
| Verifier le maillage | Lister tous les articles et leurs liens internes. Verifier que chaque article a au minimum 3 liens internes. Identifier les opportunites manquantes |
| Maillage intra-categorie | Verifier que les articles d'une meme categorie se linkent entre eux. Proposer les liens manquants avec les ancres optimisees (ancre = mot-cle de l'article cible) |
| Maillage inter-categories | Identifier les articles de categories differentes qui ont des sujets complementaires et proposer des liens croises |
| Liens vers la page categorie | Verifier que les articles contiennent un lien vers leur page categorie parente. Proposer les ajouts si manquants |
| Corriger les articles orphelins | Identifier les articles qui ne recoivent aucun lien entrant et proposer des liens depuis d'autres articles pertinents |

#### Suggestions de contenu

| Action | Description |
|--------|------------|
| Suggerer des articles | Analyser le cocon actuel et proposer des sujets d'articles manquants pour renforcer la couverture semantique de chaque categorie |
| Prioriser les contenus | Classer les suggestions par impact SEO potentiel (volume de recherche estime, complementarite avec l'existant, renforcement du cocon) |

### Optimisations on-page

| Action | Description |
|--------|------------|
| Auditer un article | Verifier la structure Hn, la densite de mots-cles, les meta tags, les liens internes |
| Optimiser les images | Verifier les attributs alt, title, les formats, le lazy loading |
| Verifier le maillage interne | Lister les articles et identifier les opportunites de liens manquants |
| Ajouter des breadcrumbs | Integrer un fil d'Ariane avec schema BreadcrumbList |

### Configuration Hugo liee au SEO

| Action | Detail |
|--------|--------|
| Ajouter une redirection | Via `aliases` dans le frontmatter d'un article |
| Modifier les URLs | Configurer `[permalinks]` dans `hugo.toml` |
| Ajouter un fichier custom | Creer dans `static/` (ex: ads.txt, security.txt) |
| Configurer noindex | Via frontmatter ou meta tag conditionnel |

## Regles

- Toujours lire l'etat actuel du fichier avant de le modifier (ne jamais ecraser sans verifier)
- Toujours expliquer a l'utilisateur ce qui va etre modifie et pourquoi
- Proposer un build de verification apres chaque modification (`hugo`)
- Si une modification impacte plusieurs fichiers, les lister avant d'agir
- Les templates dans `.claude/templates/seo/` font reference. Si l'utilisateur a modifie un template, utiliser sa version.

## Sortie du mode

L'utilisateur sort du mode SEO en changeant de sujet ou en demandant autre chose. Pas besoin de commande explicite de sortie.
