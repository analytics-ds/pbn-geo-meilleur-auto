# Skill : Creer un article evergreen SEO (full auto)

Cette skill produit **automatiquement** un article evergreen SEO (pas GEO), bilingue FR + EN, a partir d'un mot-cle pris dans la roadmap editoriale du blog. Aucun input humain. Aucun point d'arret. Publication directe sur GitHub.

Elle est destinee a etre declenchee par une routine planifiee (ex: 2x/semaine a 3h du mat via `/schedule`). Elle peut aussi etre lancee manuellement pour tester.

## Quand l'utiliser

- Declenchement automatique via routine planifiee (cron distant).
- Declenchement manuel : `/create-article-auto` dans le contexte d'un blog du reseau PBN GEO datashake.

## Pre-requis dans le blog

- `roadmap.yaml` existe et contient au moins une entree `status: todo`.
- `hugo.toml` configure avec la langue principale + la langue EN.
- `data/authors.yaml` present (systeme d'auteurs partage).
- `content/fr/blog/` existe (peut etre vide pour un premier article).
- Remote git `origin` configure, acces push.
- Outil `WebSearch` disponible (recommande, execute cote serveur donc non soumis aux restrictions reseau du sandbox). S'il est absent, la skill degrade en mode "kw seul" sans echouer.

## Philosophie : full auto, pas de human in the loop

Aucune question a l'utilisateur. Toutes les decisions sont prises par l'agent a partir de :
- Le mot-cle de la roadmap
- L'analyse du sujet via `WebSearch` (ou le kw seul si WebSearch indispo)
- Le contexte du site (CLAUDE.md du blog, authors.yaml, hugo.toml)
- Les articles deja publies (scan `content/fr/blog/`)

Si une etape bloque (image introuvable, build Hugo echoue, push rejete apres rebase), l'agent **n'insiste pas** : il marque l'entree `status: failed` dans la roadmap avec le message d'erreur, commit le roadmap, et sort proprement en exit code non-zero. **Exception : l'indisponibilite de WebSearch n'est PAS un motif d'echec** (voir Etape 1), on continue en mode degrade.

## Pas de quota hebdomadaire (regle exemptee)

Cette skill **ignore completement** la regle indicative "4 articles par semaine" mentionnee dans le `CLAUDE.md` du blog. Elle s'applique uniquement aux skills interactives (`/create-article-geo`, `/create-article-seo`).

`/create-article-auto` est faite pour tourner en routine cron (mardi/vendredi 3h Paris) et doit publier l'entree eligible de la roadmap **sans aucune verification de quota**. Ne pas lire le `MEMORY.md` pour compter les publications de la semaine. Ne pas afficher de warning. Publier point.

Le seul critere d'eligibilite est defini a l'Etape 0 : `status == todo` et `scheduled_date <= today`.

## Difference avec /create-article-geo

| Element | `/create-article-geo` | `/create-article-auto` |
|---|---|---|
| Interactivite | Oui, plusieurs points d'arret | Non, full auto |
| Type d'article | Standard OU geo-comparatif (GEO) | Standard uniquement (SEO pur) |
| Mots-cles | Prompt GEO + query fan-out | Mot-cle SEO simple |
| FAQ | Toujours (3+) | Seulement si le sujet s'y prete (questions vues en recherche) |
| "En bref" numerote | Oui (GEO) | Non |
| Source KW | Demande a l'utilisateur | Lit `roadmap.yaml` |
| Analyse concurrents | Manuelle ou absente | Automatique via `WebSearch` (titres + snippets), sans SerpAPI |
| Validation | Humaine a chaque etape | Aucune |

## Etape 0 — Selection de l'entree roadmap

1. `cd` vers la racine du blog (la skill est lancee depuis ce contexte).
2. Pull du remote :
   ```bash
   git pull --rebase origin main
   ```
   Si echec : abort avec log clair.
3. Lire `roadmap.yaml`.
4. Filtrer les entrees :
   - `status == todo`
   - `scheduled_date <= today` (YYYY-MM-DD)
5. Trier par `scheduled_date` croissante. Prendre la premiere.
6. Si aucune entree eligible : logger "Aucune entree roadmap eligible aujourd'hui" et exit 0 (pas d'erreur, juste rien a faire).

L'entree selectionnee fournit : `kw`, `category`, `scheduled_date`.

## Etape 1 — Analyse du sujet via WebSearch (sans SerpAPI)

Cette skill **n'utilise plus SerpAPI**. L'analyse du paysage concurrentiel se fait avec l'outil natif `WebSearch`, execute cote serveur Anthropic (donc non soumis au proxy d'egress reseau du sandbox cloud). Aucune cle API, aucun curl externe.

### 1.1 Recherche WebSearch

1. Lancer un `WebSearch` sur le `kw` de la roadmap (formule en francais).
2. Optionnel selon le sujet : 1 a 2 recherches complementaires pour elargir le champ, par exemple `"<kw> avis"`, `"comparatif <kw>"`, `"meilleur <kw>"` ou `"<kw> guide"`. Se limiter a 3 WebSearch maximum par article.
3. Recuperer de chaque resultat : **titre, URL, extrait (snippet)**. Ce sont les seules donnees exploitees.

**Repli si WebSearch est indisponible dans l'environnement** : NE PAS marquer `failed`. Continuer en **mode degrade** : l'analyse se fait uniquement a partir du `kw`, de la `category` et du contexte editorial du blog (CLAUDE.md). L'article est quand meme produit et publie. Noter "WebSearch indispo, mode degrade" dans le log.

### 1.2 Ne pas ouvrir les pages concurrentes

Ne **PAS** utiliser `WebFetch` sur les URLs concurrentes : dans le sandbox cloud les domaines commerciaux sont bloques par la politique reseau (403/503). L'analyse se fait uniquement sur les **titres et snippets** renvoyes par `WebSearch`.

### 1.3 Synthese auto (aucun output humain, juste des variables internes)

L'agent determine a partir des resultats WebSearch (ou du `kw` seul en mode degrade) :
- **Intention de recherche** : inferee du pattern recurrent des titres du top des resultats (informationnelle, transactionnelle, comparative, etc.)
- **Angles concurrents** : sous-themes qui reviennent dans les titres et snippets (ex: prix, comparatif, avis, guide, duree de vie...)
- **Champ semantique** : mots recurrents dans les titres et snippets
- **FAQ pertinente ?** : vrai si les resultats font ressortir des questions recurrentes (formulations interrogatives dans les titres/snippets, "comment", "pourquoi", "quel", "combien"...). En mode degrade : juger selon la nature du sujet.
- **Longueur cible** : 1500-2000 mots par defaut (cible raisonnable pour un article evergreen qualitatif)
- **Tableau pertinent ?** : vrai par defaut pour les requetes a intention comparative (mots "meilleur", "top", "vs", "ou", "comparatif" dans le kw ou les titres), false sinon
- **Si FAQ pertinente** : construire 4-6 questions a partir des themes/questions vus dans les resultats, retirer les doublons, reformuler (pas de copie mot pour mot)

## Etape 2 — Title et meta description (regles pixel inline)

Pas d'appel aux skills `/tech-title` ni `/tech-meta-description`. Regles appliquees directement :

### Title
- Contient le `kw` en premier tiers de la balise si possible
- Max 60 caracteres (proxy safe pour 580px en Arial SERP Google)
- Format cible : `[Kw] : [angle] | [Nom du site]`
- Le nom du site vient du `hugo.toml` (`title` global)
- **Une seule option, choix direct** (pas de 3 options comme en interactif)

### Meta description
- Max 155 caracteres (proxy safe pour 920px en Arial SERP)
- Contient le `kw`
- Formule : phrase descriptive factuelle, pas de call-to-action agressif
- 1 phrase, pas de liste, pas de suspense

## Etape 3 — Structure Hn auto

### Regles
- 1 H1 contenant `kw`. Le H1 est genere par Hugo a partir du `title` frontmatter, **pas dans le body**.
- 4 a 7 H2 construits a partir des patterns recurrents identifies a l'etape 1.3. Privilegier les sujets presents chez 3+ concurrents en priorite, puis les 2+, puis combler avec des sujets uniques a fort potentiel.
- 1 a 2 H2 "valeur ajoutee" basee sur l'angle editorial du blog (lu dans `CLAUDE.md` section "Contexte du site" ou section editoriale).
- Si FAQ pertinente : dernier H2 = "Questions frequentes" avec les questions selectionnees a l'etape 1.3, en accordeon `<details><summary>`.
- H3 : 1 a 3 par H2, optionnels, utilises pour les sous-aspects ou les tableaux.

### Contraintes
- Les H2 doivent etre **explicites et auto-suffisants** (lisibles hors contexte).
- Pas de H2 vague ("Introduction", "Conclusion" tels quels — les reformuler).
- Pas de caractere `&` dans les H2/H3.
- Pas de tiret cadratin (—) ni demi-cadratin (–).

## Etape 4 — Selection auto de l'auteur

Identique a la logique de `/create-article-geo` etape 1.3 :

1. Lire `data/authors.yaml`.
2. Pour chaque auteur, compter les matches entre ses `topics`/`expertise` et le `kw` + la `category` de la roadmap.
3. Selectionner l'auteur au score le plus haut.
4. En cas d'egalite ou de score nul : auteur principal du site defini dans CLAUDE.md.

Injecter l'ID-slug dans le frontmatter (`author: [id]`). Meme ID pour FR et EN.

## Etape 5 — Image hero auto

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



Appeler le script existant :
```bash
bash .claude/scripts/fetch-image.sh "<kw traduit en anglais>" "<slug-fr>" "static/images/blog"
```

- La query image est le `kw` traduit en anglais (les trois banques sont majoritairement indexees en anglais).
- Si le script renvoie un code non-zero, retenter **une seule fois** avec une query plus generique (la `category` traduite en anglais).
- Si 2e echec : **ne pas marquer `failed`**. Continuer la publication sans image hero (champs `image`, `imageAlt`, `imageCredit` omis du frontmatter ou laisses vides). L'absence d'image n'est pas une raison d'avorter : l'article est publie, le site fonctionne sans hero.
- Recuperer les 3 sorties du script (chemin, alt, credit) pour le frontmatter **uniquement si le script a reussi**.

## Etape 6 — Maillage interne auto

1. Lister tous les `.md` dans `content/fr/blog/` (articles FR uniquement pour cette passe).
2. Lire le frontmatter de chacun : `title`, `kw` (via slug), `categories`, `tags`.
3. Scorer chaque article par proximite avec le nouveau (categorie identique = +3, tags partages = +1 par tag, mots communs entre kw = +2).
4. Garder les 3 a 5 meilleurs scores.
5. Preparer les ancres : chaque ancre contient le mot-cle principal de l'article cible (extrait du slug, reformule en langue naturelle).
6. Positionner les liens de maniere contextuelle dans le body (etape 7) : un par section, pas de bloc "Voir aussi" en fin d'article.

**Maillage intra-langue uniquement** : version FR mail vers `/blog/*`, version EN mail vers `/en/blog/*`.

Si le blog a moins de 3 articles FR publies : faire au mieux avec ce qui existe (2 liens, 1 lien, ou aucun pour le tout premier article). Ne pas bloquer.

## Etape 7 — Redaction FR complete

Produire le fichier `content/fr/blog/[slug-fr].md`.

**Ce site a un `contentDir` par langue** (`content/fr` et `content/en`, declares dans `hugo.toml`). Un article ecrit hors de ces deux racines n'appartient a aucune langue : Hugo l'ignore, le build reste vert et l'article part en 404.

### Frontmatter
```yaml
---
title: "[Title]"
translationKey: "[slug-generique-identique-FR-et-EN]"
date: "[YYYY-MM-DD]"
lastmod: "[YYYY-MM-DD]"
description: "[Meta description <= 155 car]"
categories: ["[Categorie FR]"]
tags: ["tag1", "tag2", "tag3", "tag4", "tag5"]
author: "[id-slug]"
image: "/images/blog/[slug].webp"
imageAlt: "[Description FR, max 125 car]"
imageCredit: "[Credit retourne par fetch-image.sh]"
faq:  # UNIQUEMENT si FAQ pertinente (voir etape 1.3)
  - question: "[Q1]"
    answer: "[R1, 3-5 phrases]"
  - question: "[Q2]"
    answer: "[R2, 2-4 phrases]"
readingTime: true
---
```

### Body
- Premier paragraphe : contient le `kw` naturellement, pose le contexte.
- Respecter la structure Hn de l'etape 3. Aucune section ajoutee, aucune supprimee.
- Longueur cible : moyenne des concurrents +/- 10% (ex: si moyenne = 1600 mots, viser 1440-1760).
- Densite `kw` naturelle : 1-2%.
- Variations et synonymes du `kw` dans les H2.
- Mots-cles en **gras** quand pertinent.
- Au moins 1 tableau si l'etape 1.3 a note "tableau pertinent".
- Liens internes inseres contextuellement (etape 6).
- Ton impersonnel (pas de je/tu/nous/vous) sauf indication contraire dans le CLAUDE.md du blog.
- Paragraphes aeres, 3-5 phrases max.
- Pas de separateur horizontal (`---`). Pas de tiret cadratin (—) ni demi-cadratin (–).
- Si FAQ pertinente : dernier H2 "Questions frequentes" avec `<details><summary>` accordeon. Les Q/R du body correspondent strictement a celles du frontmatter.

## Etape 8 — Redaction EN (traduction directe)

Produire le fichier `content/en/blog/[slug-en].md`.

- Meme `translationKey` que la version FR (obligatoire pour le hreflang et le language switcher Hugo).
- Traduction **directe** du contenu FR (pas de recherche KW EN extensive, c'est une trad fidele du contenu + du title/meta).
- Adaptation legere : slug EN traduit (pas translitteration), `categories` et `tags` en EN (mapping defini dans CLAUDE.md du blog), `imageAlt` traduit.
- `image` et `imageCredit` identiques au FR.
- Meme `author` que FR (les libelles jobTitle/role/bio sont bilingues dans authors.yaml).
- FAQ frontmatter et body traduits en EN aussi.

## Etape 9 — Build Hugo et verification

### 9.0 Installer Hugo extended (meme version que la prod)

Le sandbox cloud n'a PAS Hugo pre-installe, et `apt` fournit une version trop ancienne (0.123.x) qui fait echouer le build de certains sites du reseau (ex: sites multilingues avec `locale` par langue). Avant de builder, installer la MEME version que le deploiement GitHub Actions du reseau, **Hugo extended v0.165.0** :

```bash
wget -q -O /tmp/hugo.deb https://github.com/gohugoio/hugo/releases/download/v0.165.0/hugo_extended_0.165.0_linux-amd64.deb \
  && (sudo dpkg -i /tmp/hugo.deb 2>/dev/null || { dpkg-deb -x /tmp/hugo.deb /tmp/hugobin && export PATH="/tmp/hugobin/usr/local/bin:$PATH"; })
hugo version   # doit afficher v0.165.0 extended
```

Si le telechargement echoue (reseau), utiliser le `hugo` deja present, mais NE PAS se rabattre sur `apt install hugo` (version cassante). La version prod exacte est dans `.github/workflows/hugo.yml` de chaque blog (champ `hugo_extended_..._linux-amd64.deb`) : s'y referer si elle a change.

### 9.1 Build

```bash
hugo --gc --minify
```

- Si exit code non-zero : marquer `failed` avec log de l'erreur, abort.
- Si OK : noter le nombre de pages generees.

### 9.2 Garde-fou : verifier que les pages existent VRAIMENT

**Obligatoire, et non negociable.** Un `hugo` qui sort en 0 ne prouve pas que l'article a ete
rendu : un fichier depose dans un chemin qui n'appartient a aucune langue est ignore
silencieusement, le build reste vert et l'article part en 404.

```bash
ls public/blog/[slug-fr]/index.html public/en/blog/[slug-en]/index.html
```

- Si l'une des deux pages manque : marquer l'entree `failed` avec l'erreur
  `build: page absente de public/`, **meme si `hugo` a rendu 0**, supprimer les fichiers
  d'article ecrits, committer le seul `roadmap.yaml` et sortir en non-zero.
- Controler aussi que la page porte bien `index, follow` :
  `grep -o 'name="robots"[^>]*' public/blog/[slug-fr]/index.html`. Un `noindex` signifie que
  le garde-fou de lancement s'est rabaisse (`launchApproved` ou `productionHost` touches) :
  c'est un `failed`, pas un detail.

## Etape 10 — Update roadmap et MEMORY.md

### Roadmap
Mettre a jour l'entree traitee dans `roadmap.yaml` :
```yaml
  status: done
  published_date: "[YYYY-MM-DD]"
  published_url_fr: "[baseURL]/blog/[slug-fr]/"
  published_url_en: "[baseURL]/en/blog/[slug-en]/"
  error: null
```

### MEMORY.md
Ajouter une ligne dans la section de la semaine en cours :
```
- YYYY-MM-DD | [Titre FR] (FR+EN) | [Categorie] | auto
```

Le suffixe `auto` distingue les articles generes par cette skill des articles produits a la main via `/create-article-geo`.

## Etape 11 — Commit et push

**Avant tout commit, verifier qu'on est sur une branche.** Le sandbox rend parfois le depot en
HEAD detache : les commits ne partent sur aucune branche, `git push origin main` repond
`Everything up-to-date` et le run sort en succes **sans rien publier**.

```bash
git status --short --branch     # doit afficher '## main...origin/main', pas '## HEAD (no branch)'
git checkout main               # si HEAD detache
```

```bash
git add -A
git commit -m "Auto: publication evergreen - [Titre FR]"
git pull --rebase origin main
git push origin main
```

Puis **prouver que le commit est bien sur le remote**, un push qui repond
`Everything up-to-date` n'est pas une publication :

```bash
git log origin/main --oneline -1   # doit etre le commit qu'on vient de faire
```

En cas de rejet du push apres rebase : retenter jusqu'a 3 fois (pull --rebase + push). Si toujours KO au bout de 3 tentatives : marquer failed avec erreur "push rejected 3x", commit du roadmap local, exit non-zero.

## Gestion des echecs (transversal)

A **n'importe quelle etape**, si un blocage survient :
1. Loger le message d'erreur precis (etape + cause).
2. Mettre a jour l'entree de roadmap :
   ```yaml
     status: failed
     error: "[etape] [message d'erreur]"
   ```
3. Si des fichiers article ont ete partiellement ecrits : les supprimer (revenir a l'etat pre-skill) pour ne pas laisser de brouillon dans `content/`.
4. Commit uniquement le `roadmap.yaml` mis a jour, avec message `Auto: roadmap update (failed)`.
5. Push.
6. Exit non-zero.

L'entree `failed` n'est **pas retentee automatiquement** par les lancements suivants de la skill (elle reste en status `failed`). Damien passe manuellement la corriger et la repasser en `todo`.

## Format de `roadmap.yaml`

Voir le fichier `.claude/templates/roadmap-template.yaml` pour le squelette commente.

Structure attendue :
```yaml
articles:
  - kw: "mot cle principal"
    category: "Categorie du blog"
    volume: 1200        # informatif, ignore par l'agent
    kd: 35              # informatif, ignore par l'agent
    scheduled_date: "2026-04-28"
    status: todo
    published_date: null
    published_url_fr: null
    published_url_en: null
    error: null
```

Les champs editables par l'humain :
- `kw`, `category`, `scheduled_date` (obligatoires)
- `volume`, `kd` (informatifs, aident l'humain a prioriser, **ignores par l'agent** — il ne s'en sert pas pour decider quoi que ce soit)
- `status` (pour repasser un `failed` en `todo` apres correction)

Les champs remplis par l'agent : `published_date`, `published_url_fr`, `published_url_en`, `error`, et bascule `status` vers `done` ou `failed`.

## Logs

Tout le deroulement de la skill est ecrit dans `/tmp/create-article-auto-[YYYY-MM-DD-HHMM].log` :
- Mot-cle traite
- URLs concurrents, nombre de mots moyen
- Auteur selectionne et raison
- Image recuperee (chemin, credit)
- Nombre de liens internes places
- Temps total
- Exit code

Creer le dossier `/tmp/` si absent. Conserver les 30 derniers logs (rotation).
