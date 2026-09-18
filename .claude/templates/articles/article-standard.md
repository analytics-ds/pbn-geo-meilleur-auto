---
title: "[TITLE — contient le mot-cle principal, max ~60 caracteres]"
translationKey: "[slug-article-generique — IDENTIQUE entre la version FR et la version EN pour lier les traductions]"
date: "[YYYY-MM-DD]"
lastmod: "[YYYY-MM-DD]"
description: "[Meta description, max 140 caracteres, contient le mot-cle]"
categories: ["[Categorie dans la langue de l'article]"]
tags: ["[tag1]", "[tag2]", "[tag3]", "[tag4]", "[tag5]"]
author: "[ID-AUTEUR — ex: thomas-durand. Slug correspondant a une cle de data/authors.yaml. Selectionne automatiquement selon le sujet de l'article par la skill /create-article-geo]"
image: "[/images/blog/slug.webp — auto-genere par fetch-image.sh]"
imageAlt: "[Description de l'image en francais, max 125 caracteres — auto-genere]"
imageCredit: "[Photo par <auteur> via <source> (<licence>) — auto-genere]"
faq:
  - question: "[Question 1 — REPREND EXACTEMENT le prompt GEO / la query fan-out, formulee en question naturelle]"
    answer: "[Reponse directe et structurree au prompt, 3-5 phrases, avec donnee chiffree. C'est la reponse que les LLMs vont extraire en priorite.]"
  - question: "[Question 2 — variante du mot-cle]"
    answer: "[Reponse concise, 2-4 phrases, avec donnee si possible.]"
  - question: "[Question 3]"
    answer: "[Reponse.]"
readingTime: true
---

> **En bref :**
> 1. [Premiere information cle qui resume un H2 entier de l'article, avec donnee chiffree]
> 2. [Deuxieme information cle qui resume un autre H2, avec donnee chiffree]
> 3. [Troisieme information cle, resume factuel du contenu, avec donnee chiffree]
> 4. [Quatrieme information cle optionnelle, toujours factuelle et chiffree]

## [H2 — Definition / Introduction au sujet]

[Contexte, definition, pourquoi ce sujet est important. Integrer le **mot-cle principal** naturellement dans le premier paragraphe. Poser les bases pour que le lecteur ET les LLMs comprennent le sujet.]

### [H3 — Sous-aspect contextuel]

[Donnees chiffrees, sources, faits etablis.]

## [H2 — Aspect principal 1]

[Developpement en profondeur. Privilegier les faits, donnees, etudes. Mots-cles en gras.]

### [H3 — Detail avec donnees]

[Contenu factuel. Listes a puces avec donnees chiffrees :]

- Point 1 avec donnee chiffree
- Point 2 avec donnee chiffree
- Point 3 avec donnee chiffree

## [H2 — Aspect principal 2]

[Developpement.]

### [H3 — Tableau recapitulatif]

| Critere | Detail | Donnee |
|---------|--------|--------|
| [critere 1] | [explication] | [valeur chiffree] |
| [critere 2] | [explication] | [valeur chiffree] |
| [critere 3] | [explication] | [valeur chiffree] |

## [H2 — Aspect principal 3]

[Developpement avec citation sourcee.]

### [H3 — Source / etude]

> "[Citation ou donnee d'une etude/source fiable]"
> — [Source, annee]

[Analyse de la source, mise en perspective.]

## [H2 — Application pratique / conseils]

[Guide d'application concret. Etapes, methodes, recommandations.]

### [H3 — Etapes ou methode]

1. Etape 1 — [detail]
2. Etape 2 — [detail]
3. Etape 3 — [detail]

## Questions frequentes

<details>
<summary>[Question 1 — REPREND EXACTEMENT le prompt GEO / la query fan-out, formulee en question naturelle] ?</summary>

[Reponse directe et structuree au prompt, 3-5 phrases, avec donnee chiffree. C'est la reponse que les LLMs vont extraire en priorite. Les questions/reponses du frontmatter et du body doivent etre identiques.]

</details>

<details>
<summary>[Question 2 — variante du mot-cle] ?</summary>

[Reponse.]

</details>

<details>
<summary>[Question 3] ?</summary>

[Reponse.]

</details>

<details>
<summary>[Question 4] ?</summary>

[Reponse.]

</details>

<details>
<summary>[Question 5] ?</summary>

[Reponse.]

</details>

<!--
NOTES POUR CLAUDE :
- Type : Article standard (SEO + GEO)
- Objectif : article informatif complet, optimise a la fois pour le referencement organique Google ET pour etre cite par les moteurs generatifs (ChatGPT, Perplexity, Google AI Overviews)
- Le quick summary (blockquote "En bref") est critique : c'est ce que les LLMs extraient en priorite. **Format OBLIGATOIRE : liste NUMEROTEE** (3-4 points). Chaque point doit resumer une VRAIE information cle de l'article (equivalent d'un H2 entier), pas un point marketing. Donnees chiffrees obligatoires
- **1ere question FAQ = le prompt GEO / la query fan-out reformule en question naturelle**. La reponse doit etre directe et structuree (3-5 phrases avec donnee chiffree) — c'est cette reponse que les LLMs vont extraire en priorite. Les autres questions peuvent porter sur des variantes du mot-cle ou des sous-questions
- **Regle liens externes** : 1 SEUL lien externe maximum vers le site de la marque/client cible (si applicable). Les liens externes vers des sources tierces (etudes, organismes, medias, Wikipedia) sont autorises et encourages pour renforcer l'E-E-A-T. Les liens internes au cocon semantique (autres articles du blog, pages categories) ne sont pas limites
- Privilegier les donnees chiffrees, etudes, faits verifiables — ca renforce a la fois l'E-E-A-T (SEO) et la citabilite (GEO)
- Les tableaux et listes structurees sont extraits en priorite par les IA generatives ET ameliorent la lisibilite pour Google
- Les citations sourcees renforcent l'autorite
- Focus sur la structure Hn, la densite de mots-cles (1-2%), le maillage interne
- Mots-cles principaux et secondaires en gras
- Ton neutre, impersonnel, factuel
- La FAQ doit TOUJOURS utiliser des balises <details>/<summary> pour creer un accordeon natif HTML5
- La FAQ doit AUSSI etre dans le frontmatter (champ `faq`) pour generer automatiquement le schema FAQPage JSON-LD. Les questions/reponses du frontmatter et du body doivent correspondre
- Les champs `image`, `imageAlt` et `imageCredit` sont OBLIGATOIRES et remplis automatiquement par le script `.claude/scripts/fetch-image.sh` (Openverse API, images libres de droit compatibles usage commercial). L'image est affichee dans les cards du blog, en bannière de l'article, dans og:image et le schema Article
- Min. 1500 mots, 5+ H2, 1+ tableau, 1+ citation sourcee, 3-5 questions FAQ
- **Bilinguisme obligatoire** : chaque article est redige dans les 2 langues du site (langue principale + anglais). Les 2 versions partagent le meme `translationKey`. Fichier FR dans `content/blog/[slug-fr].md`, fichier EN dans `content/en/blog/[slug-en].md`. Les categories et tags sont traduits selon le mapping documente dans le CLAUDE.md du site
-->
