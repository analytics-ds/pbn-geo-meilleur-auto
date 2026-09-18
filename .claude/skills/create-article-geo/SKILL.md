# Skill : Creer un article

Ce skill genere un article de blog optimise SEO et GEO (Generative Engine Optimization) selon le type choisi. **Chaque article est systematiquement genere dans les deux langues du site (langue principale + anglais)**, jamais uniquement dans une seule langue.

## Declenchement

L'utilisateur tape `/create-article-geo` ou demande de creer/rediger un article.

## Bilinguisme automatique (FR + EN)

Tous les blogs generes par ce template sont bilingues (langue principale + anglais en sous-dossier `/en/`). Chaque article cree est donc systematiquement produit dans les deux langues, en parallele :
- Version langue principale : `content/blog/[slug-fr].md`
- Version anglaise : `content/en/blog/[slug-en].md`

Les deux versions partagent un `translationKey` identique dans le frontmatter, ce qui permet a Hugo de generer automatiquement les liens hreflang et le language switcher.

Ne JAMAIS demander au consultant s'il veut la version anglaise. C'est systematique.

## Etape 0 — Pull du repo (sync obligatoire)

**Standard reseau PBN GEO datashake** : plusieurs consultants travaillent sur le meme repo. Avant toute modif, toujours synchroniser le local avec GitHub pour recuperer les changements des collegues.

```bash
git pull
```

Si le pull echoue (conflit de merge, divergence, etc.) : **STOP**. Ne pas tenter de resoudre automatiquement. Avertir l'utilisateur du probleme et lui demander de resoudre a la main avant de relancer `/create-article-geo`.

Si le repo n'a pas de remote configure (site encore en local, pas encore passe par `/github-setup`), passer cette etape et continuer.

## Etape 0.5 — Repere indicatif quota hebdomadaire (warning soft, jamais bloquant)

Apres le pull, lire le fichier `MEMORY.md` a la racine du projet. Ce fichier contient l'historique des articles publies, classe par semaine.

Compter le nombre d'articles publies dans la **semaine en cours** (lundi a dimanche). Si **4 articles ou plus** sont deja enregistres cette semaine :
- Afficher un **simple warning** : "Note : 4 articles ou plus deja publies cette semaine. Pour etaler la publication, il est recommande de patienter. Tu veux quand meme continuer ? (oui/non)"
- Si l'utilisateur confirme, continuer normalement. Sinon, arreter.

**Important** : c'est un repere indicatif, pas un blocage. Ne jamais refuser de continuer de soi-meme. La decision revient toujours a l'utilisateur.

Si le fichier `MEMORY.md` n'existe pas encore, le creer vide (il sera rempli a l'etape 7).

## Etape 0.6 — Garde-fou cannibalisation (si ajout d'un KW a la roadmap)

Cette skill ne fait pas elle-meme d'ajout dans `roadmap.yaml`, mais si l'utilisateur demande plus tard "ajoute ce KW a la roadmap" en parallele d'une session de creation, appliquer la regle decrite dans le `CLAUDE.md` du blog (section "Garde-fou cannibalisation a l'ajout dans la roadmap"). Avertir si overlap >= 50% des tokens significatifs avec un KW existant, ou si un KW est sous-string de l'autre. Soft, jamais bloquant.

## Etape 1 — Collecter les informations

### Prompt GEO et query fan-out

Demander a l'utilisateur :
- **Prompt GEO cible** : la question naturelle que les utilisateurs posent aux moteurs IA generatifs (ChatGPT, Perplexity, Google AI Overviews). Ce prompt deviendra le **H1 de l'article affiche dans la page (= frontmatter `h1`), reformule naturellement si besoin**. Si le prompt est deja une question bien formee, le garder tel quel. S'il est maladroit, le reformuler en question naturelle qui conserve le sens et les mots-cles porteurs. Exemple : prompt "huile essentielle stress et anxiete" -> H1 "Quelle huile essentielle utiliser contre le stress et l'anxiete ?"
- **Query fan-out (mot-cle SEO)** : le terme SEO sur lequel l'article se positionne dans Google. Il decoule du prompt mais s'en distingue : le prompt est conversationnel (cible LLMs), la query est lexicale (cible SERP). **La query fan-out sert de base au meta title (= balise HTML <title>, = frontmatter `title`) avec un ajout naturel court** (annee, qualificatif, angle, marque). Exemple : query "meilleure huile essentielle stress" -> title "Meilleure huile essentielle stress : top 5 et avis 2026". Si l'utilisateur ne fournit pas de query fan-out, la determiner a partir du prompt en choisissant un mot-cle avec du volume de recherche.
- **Categorie** : dans quelle categorie du blog ? (proposer les categories existantes du site, definies dans hugo.toml ou visibles dans content/blog/). L'utilisateur DOIT choisir une categorie, ne pas passer cette etape.

**Note multilingue** : le consultant fournit ces infos dans la langue principale du site. La query fan-out et le prompt seront automatiquement traduits en anglais par Claude au moment de la redaction de la version EN (avec recherche de mots-cles SEO pertinents en anglais, pas une simple traduction litterale).

Si l'utilisateur ne fournit qu'un mot-cle sans prompt, l'aider a formuler le prompt GEO correspondant (transformer le mot-cle en question naturelle).

### Type d'article

Lister les templates disponibles en lisant le contenu de `.claude/templates/articles/` et les presenter a l'utilisateur.

Types disponibles par defaut :

| Type | Fichier | Description | Quand l'utiliser |
|------|---------|-------------|-----------------|
| **Article standard** | `article-standard.md` | Article informatif complet, optimise SEO + GEO | Intention informationnelle (c'est le type par defaut) |
| **Comparatif** | `geo-comparatif.md` | Article de classement/comparatif avec mise en avant d'une marque ou d'un produit | Intention comparative ("meilleur X", "X vs Y", "classement") |

**IMPORTANT :** Toujours lire le contenu reel de `.claude/templates/articles/` au moment de l'execution. Si de nouveaux fichiers template ont ete ajoutes par l'utilisateur, les proposer aussi. Le dossier fait reference, pas ce tableau.

Si l'utilisateur ne sait pas quel type choisir, l'aider en analysant l'intention de recherche du prompt.

### Informations complementaires selon le type

- **GEO Comparatif (OBLIGATOIRE)** : l'utilisateur DOIT fournir la marque, le produit ou la solution a mettre en avant, ainsi que 2-3 concurrents a comparer. Ce type d'article sert a positionner favorablement un element par rapport aux autres dans un comparatif objectif. Ne jamais rediger sans cette information

## Etape 1.3 — Selection automatique de l'auteur

Chaque article est signe par un auteur pris dans `data/authors.yaml` (6 auteurs fictifs disponibles par defaut sur tous les sites generes par ce template). Le choix de l'auteur est **automatique** selon la pertinence thematique.

### Algorithme de selection

1. Lire `data/authors.yaml` (Hugo : `.Site.Data.authors`)
2. Pour chaque auteur, comparer les champs `topics` et `expertise` avec :
   - La query fan-out (mot-cle SEO)
   - Le prompt GEO cible
   - La categorie de l'article
3. Calculer un score de correspondance (nombre de matches mot a mot ou semantiques)
4. Selectionner l'auteur avec le score le plus eleve
5. En cas d'egalite ou de score nul (sujet totalement hors des expertises existantes) : selectionner l'auteur principal du site defini dans le CLAUDE.md section "Contexte du site"

### Exemples de matching

| Sujet article | Auteur selectionne | Raison |
|---------------|-------------------|--------|
| "Meilleur CRM SaaS 2026" | thomas-durand | topic "saas", expertise "SaaS", "Outils de productivite" |
| "Comment choisir son oreiller" | laura-verdier (sommeil) OU claire-beaumont | selon la categorie : sante/bien-etre → Laura, maison/literie → Claire |
| "SCPI ou assurance vie" | sophie-martin | topics "scpi", "assurance vie" |
| "Meilleure trottinette electrique" | kevin-moreau | topics "trottinette", "mobilite" |
| "Parfums pour l'ete" | magalie-ergoz | expertise "Parfums" |
| "Travaux renovation cuisine" | claire-beaumont | expertise "Renovation" |

### Confirmation au consultant

Apres selection, afficher au consultant :

```
Auteur selectionne automatiquement : [nom] ([ID])
Raison : [liste des topics/expertises matches]

Confirmer ? (oui par defaut / changer pour [liste des autres auteurs])
```

Le consultant peut override manuellement en indiquant un autre ID d'auteur. Si plusieurs auteurs ont des scores proches, les proposer en choix.

### Injection dans le frontmatter

Utiliser l'ID (slug) de l'auteur, pas son nom complet :

```yaml
author: thomas-durand
```

Hugo resoudra automatiquement les infos (nom, avatar, bio, role) depuis `data/authors.yaml` dans les templates (`seo-head.html` pour le JSON-LD, `single.html` pour le bloc auteur en bas d'article).

**Meme auteur pour FR et EN** : les deux versions d'un article (FR + EN) utilisent le meme `author: [id]`. Les libelles (jobTitle, role, bio) sont automatiquement traduits via les champs bilingues de `data/authors.yaml`.

## Etape 1.5 — Recuperation automatique de l'image hero

> **Cascade des sources d'image, revue le 2026-09-04.** Le script `.claude/scripts/fetch-image.sh`
> essaie dans cet ordre : **Pexels**, puis **Unsplash**, puis **Openverse**, puis un visuel de
> charte genere en local par `.claude/scripts/make-placeholder.py`. Il ne rend jamais la main
> sans visuel. **Openverse n'est plus la source nominale, il est le dernier recours** : mesure
> sur les 45 heros de journal-marketing, il n'avait produit que 15 photos pertinentes, contre
> 10 franchement hors sujet, 15 generiques et 5 degrades de secours, et il sert aussi des URLs
> mortes. Les cles `PEXELS_API_KEY` et `UNSPLASH_ACCESS_KEY` viennent du **prompt de la routine**
> ou du `.env` local, **jamais du repo** : les repos du reseau sont publics. Sans cle, la cascade
> demarre a Openverse et l'article sort quand meme. Le script tient un registre
> `.claude/hero-sources.json` qui **empeche deux articles de porter la meme photo**.
> **Le controle visuel de l'image reste obligatoire avant publication, quelle que soit la banque.**



Chaque article doit obligatoirement avoir une image hero (utilisee dans les cards du blog, la bannière de l'article, og:image et le schema Article JSON-LD). Le systeme recupere automatiquement une image libre de droit compatible usage commercial via la cascade Pexels puis Unsplash puis Openverse (voir la note ci-dessous). Aucune cle API, aucune action manuelle du consultant.

### Determiner la query image

Par defaut, la query image = la **query fan-out** (mot-cle SEO) traduite en anglais, car les banques d'images sont majoritairement indexees en anglais et retournent plus de resultats pertinents.

Exemples :
- Query fan-out "huile essentielle anti moustique" → query image "anti mosquito essential oil"
- Query fan-out "bienfaits the vert" → query image "green tea benefits" (ou simplement "green tea")
- Query fan-out "bois de chauffage densite" → query image "firewood"

Privilegier des queries courtes et visuelles (2-3 mots). Si la query fan-out est deja en anglais ou tres generique, la reutiliser telle quelle.

### Appeler le script

Le script `.claude/scripts/fetch-image.sh` gere toute la chaine : recherche dans la cascade Pexels/Unsplash/Openverse, telechargement, conversion en WebP (si cwebp dispo), ecriture dans `static/images/blog/[slug].webp`.

```bash
bash .claude/scripts/fetch-image.sh "<query image en anglais>" "<slug-de-l-article>" "static/images/blog"
```

Le script affiche sur stdout 3 lignes :
- Ligne 1 : chemin Hugo de l'image (ex: `/images/blog/mon-slug.webp`)
- Ligne 2 : titre de l'image (a utiliser comme base pour `imageAlt`)
- Ligne 3 : credit photo (ex: `Photo par John Doe via Wikimedia (CC BY-SA 3.0)`)

### Injection dans le frontmatter

Utiliser les 3 sorties pour remplir les champs suivants du frontmatter :

```yaml
image: "/images/blog/mon-slug.webp"
imageAlt: "[Reformuler le titre retourne en un alt descriptif en francais, adapte au sujet de l'article]"
imageCredit: "Photo par John Doe via Wikimedia (CC BY-SA 3.0)"
```

**Regles pour `imageAlt`** :
- Reformuler en francais (le titre peut etre en anglais)
- Descriptif du contenu visuel, pas du sujet de l'article
- Max 125 caracteres
- Integrer le mot-cle principal si c'est naturel

### Fallback en cas d'echec

Si le script renvoie un exit code non-zero (aucune image trouvee) :
1. Proposer au consultant une query alternative (plus large, plus generique, categorie de l'article)
2. Relancer le script avec la nouvelle query
3. Si toujours echec apres 2 tentatives, demander au consultant de fournir manuellement une URL d'image ou continuer sans image (deconseille)

### Verification visuelle

Afficher au consultant le chemin de l'image telechargee et proposer de la visualiser (ex: `open static/images/blog/slug.webp`). Si l'image ne convient pas visuellement, reessayer avec une query differente.

## Etape 2 — Audit des contenus existants et maillage interne

### Analyse du site

Lister tous les articles existants dans `content/blog/` en lisant le sitemap (`content/plan-du-site.md` ou directement les fichiers dans `content/blog/`). Pour chaque article existant, noter :
- Le titre
- Le mot-cle principal (visible dans le title et le nom du fichier)
- La categorie

### Verification de cannibalisation

Verifier qu'aucun article existant ne cible deja le meme mot-cle principal ou le meme prompt GEO. Si cannibalisation detectee, prevenir l'utilisateur et proposer un angle different.

### Identification des liens internes

Identifier **au minimum 3 articles existants** thematiquement proches du nouvel article pour le maillage interne. Privilegier :
1. Les articles de la **meme categorie**
2. Les articles qui partagent des **tags communs**
3. Les articles dont le sujet est **complementaire** (pas identique, mais lie)

**Regles de maillage interne :**
- **Minimum 3 liens internes** vers d'autres articles du blog, inseres de maniere contextuelle dans le corps de l'article
- L'**ancre du lien** (le texte cliquable) doit contenir le **mot-cle principal de l'article cible**, pas de "cliquez ici" ou "lire aussi"
- Les liens doivent etre **naturels et contextuels** : inseres dans une phrase qui a du sens, pas en liste en bas de page
- Repartir les liens dans differentes sections de l'article (pas tous au meme endroit)
- **Maillage intra-langue uniquement** : un article FR ne mail QUE vers des articles FR (`/blog/...`), un article EN ne mail QUE vers des articles EN (`/en/blog/...`). Jamais de maillage cross-langue dans le corps de l'article. Le language switcher du header gere le lien vers la traduction

Exemple :
- Si l'article cible s'appelle "Les bienfaits du the vert", l'ancre doit etre quelque chose comme : "Comme nous l'avons vu dans notre article sur les **[bienfaits du the vert](/blog/bienfaits-the-vert/)**, ..."
- PAS : "Pour en savoir plus, [cliquez ici](/blog/bienfaits-the-vert/)"

Si le site a moins de 3 articles, faire le maximum avec ce qui existe. Si le site est vide (premier article), noter dans un commentaire les futurs liens a ajouter quand d'autres articles seront publies.

## Etape 3 — Redaction bilingue (FR + EN)

Lire le template correspondant dans `.claude/templates/articles/[type-choisi].md` et l'utiliser comme squelette **pour chaque langue**.

### Production en deux passes

1. **Passe 1 — Langue principale (ex: FR)** :
   - Rediger l'article complet dans la langue principale selon les regles ci-dessous
   - Fichier : `content/blog/[slug-fr].md`
2. **Passe 2 — Anglais** :
   - Traduire l'article en anglais avec un vocabulaire SEO approprie (pas une traduction litterale, mais une adaptation SEO : rechercher les mots-cles anglais pertinents pour le sujet)
   - Adapter les exemples culturels si necessaire (ex: marques locales, references culturelles)
   - Rediger la version EN dans le template, avec **le meme `translationKey`** que la version FR pour lier les deux
   - Fichier : `content/en/blog/[slug-en].md`

### Frontmatter

Les deux versions ont le meme schema de frontmatter, avec le champ `translationKey` identique.

| Champ | Regle |
|-------|-------|
| `translationKey` | **OBLIGATOIRE**. Identique entre FR et EN. Format : slug-article-generique (ex: `bienfaits-the-vert`). Ce champ permet a Hugo de lier les 2 versions et de generer le hreflang et le language switcher |
| `title` | **= meta title HTML (balise <title>) = query fan-out + ajout naturel** dans la langue de l'article (annee, qualificatif, angle, marque). Cible la SERP classique. Max ~60 caracteres / 580px (cf skill `/tech-title`). Exemple : "Meilleure huile essentielle stress : top 5 et avis 2026" |
| `h1` | **= H1 affiche dans la page = prompt GEO cible reformule naturellement si besoin** dans la langue de l'article (FR : question naturelle en francais, EN : question naturelle en anglais). Garder le prompt tel quel s'il est deja une question bien formee, le reformuler en question naturelle s'il est maladroit. Le layout Hugo doit afficher `h1` en titre principal de l'article (et fallback sur `title` si `h1` non renseigne) |
| `description` | Meta description optimisee pour la SERP dans la langue de l'article. Max 140 caracteres, contient la query fan-out de la langue |
| `date` | Date du jour (YYYY-MM-DD). Identique entre FR et EN |
| `lastmod` | Date du jour (YYYY-MM-DD), identique a `date` a la creation |
| `categories` | La categorie choisie, **dans la langue de l'article** (FR : "Thes verts", EN : "Green teas"). Le mapping FR↔EN est documente dans le CLAUDE.md du site |
| `tags` | 3-6 tags pertinents, **dans la langue de l'article** (traduits en EN) |
| `author` | **ID-slug de l'auteur** (ex: `thomas-durand`), cle de `data/authors.yaml`. Selectionne automatiquement a l'etape 1.3 selon la pertinence thematique. Meme ID pour les 2 versions FR et EN (les libelles jobTitle/role/bio sont automatiquement bilingues via le YAML) |
| `image` | Chemin vers l'image hero (OBLIGATOIRE, rempli automatiquement a l'etape 1.5 par `fetch-image.sh`). **Meme image pour FR et EN** (on ne double pas le telechargement) |
| `imageAlt` | Texte alt de l'image (OBLIGATOIRE). **Traduit dans la langue de l'article** (FR : en francais, EN : en anglais). Max 125 caracteres |
| `imageCredit` | Credit photo (OBLIGATOIRE, rempli automatiquement). Meme credit dans les 2 langues |
| `faq` | Liste de questions/reponses pour le schema FAQPage JSON-LD (min. 3). **Traduites dans la langue de l'article**. Les questions doivent correspondre a celles de la section FAQ dans le body |
| Nom du fichier | Slug = query fan-out en minuscules, tirets, sans accents, **dans la langue de l'article** (FR : `bienfaits-the-vert.md`, EN : `green-tea-benefits.md`) |

### Regles GEO (Generative Engine Optimization)

Ces regles sont fondamentales pour que l'article soit cite par les moteurs IA generatifs :

| Regle | Detail |
|-------|--------|
| **H1 = prompt cible reformule** | Le H1 affiche dans la page (frontmatter `h1`) reprend le prompt cible reformule naturellement si besoin. Garder le prompt tel quel s'il est deja une question bien formee. Reformuler en question naturelle s'il est maladroit. Jamais transforme en mot-cle SEO. Cible les LLMs |
| **Meta title (HTML <title>) = query + ajout naturel** | Le meta title (frontmatter `title`) commence par la query fan-out (telle quelle ou tres legerement reformulee pour la fluidite) suivie d'un ajout naturel court (annee, qualificatif, angle, marque). Cible la SERP, distinct du H1 |
| **Query fan-out dans le body** | La query fan-out (mot-cle SEO) doit apparaitre dans le premier paragraphe et dans les variations des H2 |
| **1 paragraphe = 1 idee** | Chaque paragraphe traite d'une seule idee distincte. Ne jamais melanger plusieurs concepts dans un meme paragraphe. Cela facilite l'extraction par les LLMs |
| **Quick summary auto-suffisant** | Le bloc "En bref" est le bloc le plus critique : les LLMs l'extraient en priorite. Il doit etre auto-suffisant (comprehensible seul) et contenir les faits cles avec des donnees chiffrees |
| **H2 explicites et descriptifs** | Pas de titres vagues. Chaque H2 doit etre auto-suffisant et comprehensible hors contexte de l'article |
| **Donnees chiffrees obligatoires** | Integrer des donnees chiffrees dans chaque section (prix, pourcentages, statistiques, durees). Les LLMs extraient les faits verifiables en priorite |
| **Tableaux extractibles** | Au moins 1 tableau structurant les informations cles. Les tableaux sont extraits en priorite par les IA generatives |
| **Citation sourcee obligatoire** | Au moins 1 citation d'une etude, d'un organisme ou d'un expert, avec source et annee. Renforce la credibilite et la citabilite |

### Regles communes a tous les types

| Spec | Valeur |
|------|--------|
| H1 | Jamais dans le body (genere par Hugo depuis le title) |
| Densite mot-cle | 1-2% (query fan-out) |
| Mots-cles en gras | Oui, `**mot-cle**` |
| Ton | Impersonnel (pas de je/tu/nous/vous) sauf si precise autrement dans le CLAUDE.md |
| Liens internes | Min. 3 liens contextuels vers des articles existants (ancre = mot-cle de l'article cible) |
| FAQ | 3-5 questions en fin d'article |
| Separateurs | JAMAIS de separateur horizontal (---) entre les sections |
| Tirets | JAMAIS de tiret cadratin ni demi-cadratin. Utiliser des virgules, des points ou reformuler |

### Regles specifiques par type

Lire les commentaires HTML `<!-- NOTES POUR CLAUDE -->` en bas du template choisi. Ils contiennent les specs propres a ce type d'article :
- Nombre de mots minimum
- Blocs obligatoires (quick summary, tableaux, citations, etc.)
- Objectif editorial
- Ton specifique eventuel

**Toujours suivre ces notes.** Elles priment sur les regles communes si conflit.

## Etape 4 — Verification (checklist) — a appliquer aux DEUX versions FR + EN

- [ ] Les 2 versions sont creees (FR dans `content/blog/`, EN dans `content/en/blog/`)
- [ ] Les 2 versions partagent le meme `translationKey` dans le frontmatter
- [ ] Slug = query fan-out en minuscules, tirets, sans accents, dans la langue de l'article
- [ ] Frontmatter `title` (= meta title HTML) = query fan-out + ajout naturel court, < 60 caracteres / 580px
- [ ] Frontmatter `h1` (= H1 affiche) = prompt GEO cible reformule naturellement si besoin (question naturelle dans la langue de l'article)
- [ ] Meta description <= 140 caracteres, contient la query fan-out (mot-cle SEO dans la langue)
- [ ] Auteur renseigne dans le frontmatter (ID slug correspondant a une cle de `data/authors.yaml`, meme ID pour FR et EN)
- [ ] H1 = prompt cible reformule (verifie que c'est bien une question naturelle, pas un mot-cle)
- [ ] `title` et `h1` sont distincts (le `h1` vise les LLMs, le `title` vise la SERP)
- [ ] Query fan-out presente dans le premier paragraphe
- [ ] Structure Hn conforme au type (voir notes du template)
- [ ] H2 explicites et auto-suffisants (comprehensibles hors contexte)
- [ ] 1 paragraphe = 1 idee distincte (pas de paragraphes multi-idees)
- [ ] Nombre de mots minimum atteint (voir notes du template)
- [ ] Donnees chiffrees presentes dans chaque section
- [ ] Mots-cles en gras
- [ ] Ton correct
- [ ] Min. 3 liens internes contextuels (ancres = mots-cles des articles cibles)
- [ ] Blocs obligatoires presents selon le type
- [ ] Quick summary "En bref" auto-suffisant avec donnees chiffrees
- [ ] Au moins 1 tableau recapitulatif
- [ ] Au moins 1 citation sourcee (source + annee)
- [ ] FAQ presente avec balises `<details>/<summary>` (accordeon) dans le body
- [ ] FAQ presente dans le frontmatter (champ `faq`, min. 3 questions) pour le schema FAQPage JSON-LD
- [ ] Les questions FAQ du frontmatter et du body correspondent
- [ ] `image`, `imageAlt` et `imageCredit` renseignes (auto via `fetch-image.sh`)
- [ ] Fichier image present dans `static/images/blog/[slug].webp`
- [ ] Pas de separateur horizontal (---) ni de tiret cadratin/demi-cadratin
- [ ] Build Hugo OK (`hugo`)

## Etape 5 — Sauvegarde et build

```bash
hugo
```

Afficher a l'utilisateur :
- Type d'article utilise
- Prompt GEO (H1) dans les 2 langues
- Query fan-out (mot-cle SEO) dans les 2 langues
- Nombre de mots par langue
- Nombre de H2 (identique dans les 2 langues)
- Liens internes ajoutes (en preciser la langue)
- URLs des 2 versions (FR : `/blog/slug-fr/`, EN : `/en/blog/slug-en/`)
- Proposer de voir le resultat en local (`hugo server`)

## Etape 6 — Enregistrement dans MEMORY.md

Ajouter une ligne dans `MEMORY.md` a la racine du projet pour tracer la publication. Le fichier est organise par semaine (lundi a dimanche).

Format du fichier :

```markdown
# Journal de publication

## Semaine 16 (13/04/2026 - 19/04/2026)
- 2026-04-17 | Titre de l'article (FR+EN) | Categorie

## Semaine 15 (06/04/2026 - 12/04/2026)
- 2026-04-07 | Titre de l'article (FR+EN) | Categorie
```

Regles :
- Utiliser le numero de semaine ISO et les dates lundi-dimanche
- Creer une nouvelle section de semaine si elle n'existe pas encore
- Les semaines les plus recentes en haut du fichier
- Une ligne par article : date | titre (FR+EN) | categorie
- **1 article = 1 ligne, meme si 2 versions linguistiques** (les 2 versions comptent comme 1 article pour le quota de 4/semaine)

## Etape 7 — Push sur GitHub (direct sur main)

Si un remote git est configure (le site a ete mis en ligne via `/github-setup`), commit et push automatiquement sur `main` :

```bash
git add -A
git commit -m "Ajout article : [titre de l'article]"
git push origin main
```

**Standard reseau PBN GEO datashake** : on push toujours direct sur `main`, jamais sur une branche annexe. GitHub Actions deploie automatiquement.

Si le push est rejete (quelqu'un a push entre-temps) : faire un `git pull --rebase` puis retenter le push. Si conflit : **STOP** et avertir l'utilisateur.

Informer l'utilisateur que l'article sera en ligne dans 1-2 minutes (deploiement automatique via GitHub Actions).

Si aucun remote n'est configure, ne rien faire (le site est en local uniquement).
