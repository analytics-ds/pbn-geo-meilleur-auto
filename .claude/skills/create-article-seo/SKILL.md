# Skill : Creer des articles evergreen SEO (production locale, polyvalente)

Cette skill produit en **local** (Mac de Damien, Opus 4.7 sans limite Stream idle timeout) un **ou plusieurs articles evergreen SEO bilingues FR + EN**. Polyvalente : 3 modes de selection des KW + 3 strategies de scheduling.

C'est **la methode 2** du systeme PBN GEO datashake (alternative au CCR cloud `/create-article-auto`). Avantages :
- Opus 4.7 sans risque de Stream idle timeout
- Vraie analyse SERP avec WebFetch des concurrents (sandbox cloud bloque les domaines commerciaux)
- Maillage interne plus riche (cross-batch : articles d'un meme batch peuvent se mailler entre eux)
- Relecture humaine possible avant push
- 3 modes pour couvrir tous les cas : roadmap blog, roadmap externe, KW ponctuel

La publication reelle (mise en ligne) se fait via :
- **Push immediat** si `publishDate <= today` : article visible dans 1-2 min via le workflow `hugo.yml` declenche sur push
- **GitHub Actions cron** sinon : `schedule: '0 1 * * 2,5'` dans `hugo.yml` (mardi+vendredi 3h Paris). A chaque rebuild, les articles dont `publishDate <= today` apparaissent automatiquement

## Quand l'utiliser

- 1x/mois : production en batch des prochains articles depuis `roadmap.yaml` (mode A)
- Ponctuel : roadmap externe (Sheet d'un consultant, KW fournis par un client) (mode B)
- Ponctuel : 1 ou plusieurs KW a la demande, pas dans la roadmap (mode C)

## Pre-requis dans le blog

- `roadmap.yaml` a la racine du repo (mode A : obligatoire ; mode B et C : optionnel pour fusion eventuelle)
- `hugo.toml` configure avec `buildFuture: false` (defaut Hugo, ne pas changer)
- `data/authors.yaml` present
- `content/blog/` existe (peut etre vide pour un premier article)
- `.claude/scripts/fetch-image.sh` present (sinon copier depuis `blog-site-template`)
- `.github/workflows/hugo.yml` avec section `schedule: cron '0 1 * * 2,5'` pour le cron de publication
- Remote git `origin` configure
- MCP `serpapi` accessible via `mcp__serpapi__search`

## Etape 0 — Questions interactives initiales

### Q1 — Mode

Demander :
> "Quel mode pour ce run ?
>  (A) Suivre la `roadmap.yaml` du blog [defaut]
>  (B) Roadmap externe (fournie par toi : YAML colle ou chemin)
>  (C) KW a la demande (1 ou plusieurs, fournis dans le chat)"

### Q2 — Selon le mode choisi

#### Mode A — Roadmap du blog

1. **Combien d'articles ?** entier N
2. **Strategie de scheduling** :
   > "Comment scheduler ces N articles ?
   >  (1) Garder les `scheduled_date` actuelles de la roadmap [defaut]
   >  (2) Tout recaler a partir d'une date X (cascade : decaler en avant les entrees affectees aux prochains slots mardi/vendredi)
   >  (3) Reaffecter chaque article au prochain slot dispo (mardi/vendredi non occupe dans la cadence)"

   Si (2) : demander la date X (YYYY-MM-DD).

#### Mode B — Roadmap externe

1. **Source** :
   > "Colle le YAML de la roadmap externe OU donne le chemin d'un fichier .yaml"
   Parser et valider le format (memes champs : `kw`, `category`, `scheduled_date`, optionnellement `volume`/`kd`).
2. **Combien d'articles ?** entier N
3. **Strategie de scheduling** :
   > "Comment scheduler ?
   >  (1) Garder les `scheduled_date` de la roadmap fournie [defaut]
   >  (2) Reaffecter chaque article au prochain slot dispo de la cadence du blog (mardi/vendredi non occupe par roadmap.yaml)
   >  (3) A partir d'une date X (cascade)"
4. **Fusion dans roadmap.yaml du blog** :
   > "Ajouter ces entrees a `roadmap.yaml` du blog ? (oui [defaut] / non)"
   - Si oui : insertion dans roadmap.yaml avec `status: queued`, `queued_date: today`
   - Si non : ponctuel, roadmap.yaml du blog inchangee

#### Mode C — KW a la demande

Boucle interactive jusqu'a ce que l'utilisateur dise "fin", "stop" ou ne donne plus de KW :
- **KW** : `<mot-cle>`
- **Categorie** : (proposer la liste des categories valides du blog, lue depuis le hugo.toml ou CLAUDE.md)
- **Date de publication** :
  > "(1) Immediate (`publishDate` = today, l'article apparait des le push)
  >  (2) Date precise (YYYY-MM-DD)
  >  (3) Prochain slot dispo dans la cadence (mardi/vendredi non occupe)"

  - Si choix (2) : verifier conflits avec roadmap.yaml. Si conflit detecte (entree `todo` ou `queued` a la meme date) : demander a l'utilisateur "Conflit avec '<kw existant>' a <date>. Decaler en cascade les entrees suivantes ? (oui/non)". Si oui : appliquer cascade.
  - Si choix (3) : calculer le prochain slot dispo (algo en Etape 1).

Apres avoir collecte tous les KW :
- **Fusion dans roadmap.yaml** :
  > "Ajouter ces KW a `roadmap.yaml` du blog (statut queued) ? (oui [defaut] / non)"

### Pre-validation

Avant de demarrer le batch :
- Verifier les pre-requis fichiers (authors.yaml, fetch-image.sh, MCP serpapi, hugo binary)
- Lister les N articles qui seront produits avec leur publishDate finale (apres scheduling)

#### Garde-fou cannibalisation (mode B et C avec fusion, ou tout ajout dans roadmap.yaml)

Si le run va ajouter de **nouvelles entrees** dans `roadmap.yaml` (mode B avec fusion oui, mode C avec fusion oui), executer le check de cannibalisation **avant** confirmation finale :

1. Lire toutes les entrees existantes de `roadmap.yaml` (tous statuts).
2. Pour chaque KW propose, comparer aux KW existants :
   - Tokeniser (lowercase, retirer stop words FR/EN courants : le/la/les/de/du/des/un/une/a/au/aux/the/of/and/or/in/on/for...).
   - Calculer overlap : tokens communs / tokens du KW le plus court.
   - Drapeau "risque" si overlap >= 50% OU si un KW est sous-string de l'autre.
3. Si au moins un drapeau leve : afficher la liste des couples suspects et demander confirmation explicite ("Cannibalisation potentielle avec : [liste]. Continuer quand meme ? oui/non").
4. Si aucun risque : pas de warning, on continue.

Soft, jamais bloquant. L'utilisateur peut toujours forcer.

#### Repere indicatif quota hebdomadaire (warning soft, jamais bloquant)

Compter dans `MEMORY.md` les articles avec `publishDate` ou date de publication dans la **semaine en cours** (lundi-dimanche). Si le batch en cours (apres scheduling) va porter le total au-dela de 4 articles publies cette semaine :
- Afficher un **simple warning** : "Note : ce batch portera la semaine en cours a X articles. Repere indicatif a 4/semaine pour etaler la publication. Continuer ? (oui/non)"
- Si l'utilisateur confirme, continuer normalement.

Important : c'est un repere indicatif, jamais un blocage. Ne pas refuser de soi-meme. Ne s'applique qu'aux articles avec `publishDate` dans la semaine en cours (les articles avec `publishDate` futur dans une autre semaine ne comptent pas pour ce check).

#### Confirmation finale

Demander confirmation : "OK pour lancer ? (oui/non)"

## Etape 1 — Resolution du scheduling

Calcul effectue **avant** la rediaction, pour fixer les `publishDate` definitifs.

### Algorithme : "prochain slot dispo dans la cadence"

```
slots_occupes = [scheduled_date de chaque entree roadmap.yaml avec status in (todo, queued)]
candidats = mardis et vendredis a partir de today (inclus si today est mardi/vendredi)
pour chaque candidat dans l'ordre :
  si candidat NOT in slots_occupes : retourner candidat
```

### Algorithme : "cascade remapping a partir de date X"

```
entrees_a_decaler = [entrees de roadmap.yaml avec status in (todo, queued) ET scheduled_date >= X]
trier entrees_a_decaler par scheduled_date croissante
sequence_dates = mardis et vendredis a partir de X (inclus)
i = 0
pour chaque entree dans entrees_a_decaler :
  trouver la prochaine sequence_dates[i] qui n'est PAS occupee par une entree EN DEHORS de la liste a decaler
  entree.scheduled_date = sequence_dates[i]
  i += 1
```

L'article ponctuel (mode C) ou les nouvelles entrees (mode B) prennent la position date X.

### Algorithme : "garder les scheduled_date" (defaut mode A et B)

Aucun calcul, on prend les dates telles que dans la source.

### Application du remapping

Si scheduling option (2) ou (3) a ete choisi :
- **Avant** la production des articles, mettre a jour `roadmap.yaml` avec les nouvelles `scheduled_date`
- Commit intermediaire optionnel : `git commit -m "chore: cascade remapping des scheduled_date"` (utile pour tracer le decalage)
- Continuer ensuite avec la production

### Validation diversite des categories (obligatoire, applique APRES tout scheduling)

Une fois les `scheduled_date` finales calculees, valider l'ordre chronologique
de publication contre la regle de diversite :

```
sequence = entrees [todo, queued] de roadmap.yaml triees par scheduled_date croissante
pour chaque paire consecutive (i, i+1) :
  si sequence[i].category == sequence[i+1].category : ECHEC regle 1
pour chaque fenetre glissante de 5 entrees :
  si nb_categories_distinctes < 3 : ECHEC regle 2
```

**Regles** :
1. JAMAIS 2 articles consecutifs de la meme categorie.
2. Sur toute fenetre glissante de 5 articles consecutifs, au moins 3 categories
   distinctes doivent etre representees.
3. Cas degrade : si le blog n'a que 2 categories disponibles dans le pool,
   imposer alternance stricte 1 sur 2 (la regle 2 est alors levee).

**En cas d'echec** :
- Reordonner automatiquement les `scheduled_date` des entrees en conflit en
  les permutant avec la prochaine entree compatible (categorie differente).
- Ne JAMAIS modifier les `scheduled_date` deja `done`.
- Logguer chaque permutation a l'utilisateur dans le recap (Etape 5).
- Si aucune permutation possible (cas extreme), demander l'arbitrage humain
  avant de continuer.

Cette validation s'applique aussi a chaque ajout d'entree dans la roadmap
(mode A nouvelle entree, mode B import, mode C insertion).

## Etape 2 — Pour chaque article (boucle sur les N entrees)

La rediaction se fait en **sequence**. Apres chaque article rredige, il rejoint le pool de "articles dispo pour maillage" pour les articles suivants du meme batch (cross-batch).

### 2.1 Analyse SERP (page 1)

`mcp__serpapi__search` avec :
- `q` = `kw`
- `engine` = `google`
- `hl` = langue principale
- `gl` = pays cible
- `num` = 10
- `location` = pays

Extraire :
- `organic_results[0..9]` : URL, title, snippet
- `related_questions` (PAA) si presents
- `related_searches` si presents

### 2.2 Fetch concurrents (3-5 pertinents)

Boucler les `organic_results`. Pour chaque URL :

1. `WebFetch` HTML
2. Extraire `<title>`, `<meta name="description">`, H1, H2, H3 (dans l'ordre), longueur du body
3. **Filtre pertinence** :
   - Langue == langue principale du site
   - kw ou variante dans H1/title
   - Longueur >= 500 mots
   - Pas une page e-commerce ou un PDF
4. Pertinent -> ajouter au pool
5. Pas pertinent -> passer au suivant
6. Arreter quand 5 pertinents OU toutes URLs essayees

**Min 3 pertinents requis.** Si <3 apres tous essais : continuer en mode degrade (titles + snippets + PAA seuls), marquer dans la roadmap `error: "moins de 3 concurrents pertinents"`.

### 2.3 Synthese SERP

A partir des donnees fetched + SerpAPI :
- **Intention de recherche** : informationnelle / transactionnelle / comparative / mixte
- **Patterns Hn recurrents** : H2 chez 2+/5 concurrents
- **Longueur cible** : moyenne concurrents +/- 10% (ou 1500-2000 mots si mode degrade)
- **FAQ pertinente ?** : VRAI si 50%+ concurrents ont une FAQ OU si `related_questions` retournes
- **Tableau pertinent ?** : VRAI si 50%+ concurrents en ont OU intention comparative
- **Liste questions FAQ** (si pertinente) : 4-6 questions extraites des PAA + FAQ concurrents, dedupliquees, reformulees
- **Champ semantique** : mots recurrents

### 2.4 Title et meta description

Regles pixel inline (pas d'appel a `/tech-title` ni `/tech-meta-description`).

- **Title** : <=60 char, kw en premier tiers, format `[Kw] : [angle]`
- **Meta description** : <=155 char, contient kw, phrase descriptive

### 2.5 Structure Hn

- 4-7 H2 bases sur patterns recurrents (priorite 3+/5 puis 2+/5)
- 1-2 H2 valeur ajoutee deduits de l'angle editorial du blog (CLAUDE.md)
- Si FAQ pertinente : H2 final "Questions frequentes" en accordeon `<details><summary>`
- H3 : 1-3 par H2 si necessaire

Contraintes :
- H2 explicites et auto-suffisants
- Pas de "Introduction", "Conclusion" tels quels
- Pas de `&` dans H2/H3
- Pas de tiret cadratin (—) ni demi (–)

### 2.6 Selection auteur

1. Si `data/authors.yaml` : matching `topics`/`expertise` avec kw + category. Score max gagne. Egalite ou nul -> auteur principal du site (`default_author_id` dans hugo.toml params, ou defini dans CLAUDE.md)
2. Sinon : `default_author_id` du hugo.toml params

Injecter `author: <id-slug>` dans le frontmatter. Meme ID pour FR et EN.

### 2.7 Image hero

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



```bash
bash .claude/scripts/fetch-image.sh "<kw traduit en anglais>" "<slug-fr>" "static/images/blog"
```

- Si exit code != 0 : retenter UNE fois avec query plus generique (category traduite en anglais)
- Si toujours KO : skipper l'image et continuer (le site supporte l'absence)
- Recuperer les 3 sorties (path, alt suggere, credit)

### 2.8 Maillage interne (cross-batch inclus)

1. Lister `content/blog/*.md` (articles deja publies)
2. **Ajouter au pool les articles deja produits dans ce batch** (cross-batch : permet aux articles du meme run de se mailler entre eux)
3. Scorer chaque candidat : category identique +3, tags partages +1 chacun, mots communs kw +2
4. Garder 3-5 meilleurs scores
5. Construire les ancres : ancre = mot-cle principal de l'article cible
6. Inserts contextuels dans le body (etape 2.9), un par section pertinente, **intra-langue uniquement**

### 2.9 Redaction FR

Fichier `content/blog/<slug-fr>.md`.

Frontmatter (REGLE CLE : `publishDate` resolu a l'Etape 1) :

```yaml
---
title: "[Title]"
translationKey: "[slug-generique-FR-EN]"
date: "[date resolue par l'Etape 1]"          # IMPORTANT : alignee sur publishDate (date d'apparition publique reelle), pas sur today. Sinon l'article affiche au lecteur la date de redaction au lieu de la date de mise en ligne, ce qui cree un decalage visible.
lastmod: "[date resolue par l'Etape 1]"       # idem date
publishDate: "[date resolue par l'Etape 1]"   # CLE : Hugo masque tant que publishDate > today
description: "[Meta description <=155]"
categories: ["[Categorie FR]"]
tags: ["tag1", "tag2", "tag3", "tag4", "tag5"]
author: "[id-slug]"
image: "/images/blog/<slug>.webp"
imageAlt: "[Alt FR <=125 char]"
imageCredit: "[Credit Openverse]"
faq:                             # uniquement si pertinente
  - question: "[Q1]"
    answer: "[R1, 3-5 phrases]"
readingTime: true
---
```

Body :
- 1er paragraphe contient `kw` naturellement
- Respecter strictement la structure Hn de l'Etape 2.5
- Longueur 2.3 +/- 10%
- Densite kw 1-2%, mots-cles en **gras**
- 1 tableau si "tableau pertinent"
- 3-5 liens internes contextuels (Etape 2.8)
- Ton impersonnel
- Pas de separateur horizontal `---` dans le body
- Pas de tiret cadratin ni demi-cadratin
- Si FAQ pertinente : dernier H2 "Questions frequentes" avec accordeon `<details><summary>`. Q/R body == Q/R frontmatter.

### 2.10 Redaction EN

Fichier `content/en/blog/<slug-en>.md`.

- Meme `translationKey` que FR
- Meme `publishDate` que FR
- Trad directe FR -> EN (pas de recherche KW EN extensive)
- Slug EN traduit
- Categories et tags en EN selon le mapping CLAUDE.md du blog
- `image`, `imageCredit`, `author` identiques au FR
- `imageAlt` traduit
- FAQ traduite

### 2.11 Update roadmap.yaml (selon mode et choix fusion)

- **Mode A** : entree existante -> `status: queued`, `queued_date: today`. Si scheduling (2) ou (3) : `scheduled_date` mis a jour deja a l'Etape 1.
- **Mode B avec fusion** : nouvelle entree avec `status: queued`, `queued_date: today`, `scheduled_date` = publishDate. Inserer a la bonne place dans la liste roadmap (par scheduled_date croissante).
- **Mode B sans fusion** : aucune modif de roadmap.yaml.
- **Mode C avec fusion** : nouvelle entree (idem mode B avec fusion).
- **Mode C sans fusion** : aucune modif.

### 2.12 Mise a jour `static/llms.txt`

Conformement a la regle imperative documentee dans le CLAUDE.md du blog : ajouter une ligne `- <Titre complet> : <URL absolue FR>` dans la section approprie (FR), idem section EN si presente. Format documente dans le CLAUDE.md du blog.

## Etape 3 — Build Hugo de verification

```bash
hugo
```

Verifier exit 0. Les articles avec `publishDate > today` ne sont pas dans le rendu (attendu, masques par `buildFuture: false`). Les articles avec `publishDate <= today` (mode C immediate) sont dans le rendu.

## Etape 4 — Update MEMORY.md

Pour chaque article du batch, ajouter une ligne dans `MEMORY.md` (a la racine du blog), classees par semaine de la `publishDate` :

```markdown
- YYYY-MM-DD | <Titre FR> (FR+EN) | <Categorie> | <mode> [(queued)]
```

`<mode>` = `batch` (mode A), `roadmap-externe` (B), ou `ponctuel` (C). Suffixe `(queued)` si `publishDate > today`, rien si publication immediate.

## Etape 5 — Recap

Afficher dans le chat un tableau detaille :

```
Run termine : N articles produits.

| # | Mode | KW | Slug FR | Categorie | publishDate | Mots FR | Auteur |
|---|------|-----|---------|-----------|-------------|---------|--------|
...

Stats :
- Concurrents pertinents en moyenne : X.X / 5
- Articles en mode degrade (<3 concurrents) : N
- Image hero recuperee : N/N
- Maillage interne moyen : X.X liens / article
- Articles immediatement visibles (publishDate <= today) : N
- Articles en attente de cron (publishDate > today) : N

Roadmap apres run :
- Entrees `todo` -> `queued` : N
- Nouvelles entrees ajoutees (mode B/C avec fusion) : N
- Entrees decalees (cascade) : N
```

## Etape 6 — Commit + push (confirmation utilisateur)

Demander :
> "Commit + push maintenant ?
>  (1) oui [defaut]
>  (2) non, je relis d'abord
>  (3) commit local seulement (pas de push)"

Selon choix :
- (1) : `git add -A && git commit -m "evergreen: <N> articles produits (mode <X>)" && git pull --rebase origin main && git push origin main`
- (2) : laisser en local, message a Damien : "Articles en local, fais ton review puis commit/push manuellement"
- (3) : `git add -A && git commit -m "evergreen: <N> articles produits (mode <X>)"`, pas de push

Apres push, GitHub Actions `hugo.yml` se declenche :
- Articles avec `publishDate <= today` : visibles sur le site dans 1-2 min
- Articles avec `publishDate > today` : invisibles jusqu'au prochain cron (mardi/vendredi 3h Paris)

## Gestion erreurs (transversal)

A toute etape, si un article echoue :
1. Logger erreur dans `/tmp/evergreen-<date>.log`
2. Marquer roadmap.yaml : `status: failed` + `error: "<etape> <message>"` (uniquement si l'article etait dans roadmap, pas pour mode B/C sans fusion)
3. Supprimer fichiers article partiels
4. **Continuer le batch** sur les entrees suivantes
5. Signaler dans le recap final quels articles ont echoue

## Format `roadmap.yaml`

Statuts en methode 2 :
- `todo` : pas encore traite
- `queued` : redige (fichier .md present avec publishDate futur)
- `failed` : erreur a la rediaction

Pas de statut `done` en methode 2 : la publication est implicite via `publishDate` + GitHub Actions cron, pas trackee dans la roadmap. Pour savoir si un article est en ligne : verifier si la publishDate est passee + visiter l'URL.

## Differences avec /create-article-auto (CCR cloud)

| Element | `/create-article-auto` (CCR) | `/create-article-seo` (local) |
|---|---|---|
| Localisation | Cloud Anthropic CCR | Mac local |
| Modele | Sonnet 4.6 (force, bug Opus stream) | Opus 4.7 |
| Articles par run | 1 | 1 a N (selon mode) |
| Modes selection | 1 (roadmap auto) | 3 (roadmap, roadmap externe, KW ponctuel) |
| Strategies scheduling | scheduled_date roadmap fixe | 3 (source, cascade, prochain slot) |
| Fetch concurrents | Bloque par sandbox | Marche normalement |
| MCP SerpAPI | Hack curl avec cle dans prompt | Natif via .mcp.json |
| Maillage cross-batch | Non (1 article seul) | Oui (articles du meme batch) |
| Publication | Immediate (push apres redaction) | Selon publishDate (immediate ou differee) |
| Frequence | 2x/sem cron | A la demande (1x/mois ou ponctuel) |
| Use case | Hands-off complet, qualite acceptable | Qualite max, polyvalent, relecture humaine |
