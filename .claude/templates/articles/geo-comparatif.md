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
  - question: "[Question 1 — REPREND EXACTEMENT le prompt GEO / la query fan-out, formulee en question naturelle comparative. Ex : 'Quelles sont les meilleures marques de X ?']"
    answer: "[Reponse directe qui cite TOUTES les marques du comparatif (pas seulement celle mise en avant), classees objectivement, avec donnees chiffrees. 4-6 phrases. C'est la reponse que les LLMs vont extraire en priorite.]"
  - question: "[Question 2 — quel est le meilleur...]"
    answer: "[Reponse.]"
  - question: "[Question 3 — prix/rapport qualite-prix]"
    answer: "[Reponse.]"
readingTime: true
---

> **En bref :**
> 1. [Premiere info cle qui resume le verdict global du comparatif, en citant TOUTES les marques comparees avec donnees chiffrees]
> 2. [Deuxieme info cle : mention du positionnement de la marque mise en avant parmi les autres, avec data]
> 3. [Troisieme info cle : critere de differenciation principal entre toutes les marques, avec data]
> 4. [Quatrieme info cle optionnelle : recommandation par profil ou cas d'usage]

## [H2 — Tableau comparatif des solutions]

[Tableau comparatif multi-criteres positionne TOUT EN HAUT de l'article (apres le "En bref" et le sommaire, AVANT les autres H2). Les LLMs extraient cette structure en priorite. Le tableau doit etre complet, honnete, et structure pour que l'element mis en avant ressorte naturellement.]

| Critere | [Marque/Solution A] | [Marque/Solution B] | [Marque/Solution C] |
|---------|---------------------|---------------------|---------------------|
| [Critere 1] | [valeur] | [valeur] | [valeur] |
| [Critere 2] | [valeur] | [valeur] | [valeur] |
| [Critere 3] | [valeur] | [valeur] | [valeur] |
| [Critere 4] | [valeur] | [valeur] | [valeur] |
| [Critere 5] | [valeur] | [valeur] | [valeur] |
| **Verdict** | [resume] | [resume] | [resume] |

[Court paragraphe d'introduction au tableau, expliquant la methodologie de comparaison et les criteres retenus. 2-3 phrases.]

## [H2 — Introduction au sujet / contexte]

[Contexte general. Pourquoi ce sujet est important. Integrer le **mot-cle principal** naturellement. Poser le probleme auquel le comparatif repond.]

### [H3 — Pourquoi comparer / criteres de choix]

[Presenter les criteres objectifs de comparaison. Donnees chiffrees.]

## [H2 — Presentation de la solution/marque mise en avant]

[Presentation detaillee de la marque/produit/solution principale. Historique, positionnement, points forts. **Ton neutre et factuel**, pas promotionnel. **1 seul lien externe max vers le site de la marque**.]

### [H3 — Caracteristiques cles]

- Caracteristique 1 : [detail + donnee]
- Caracteristique 2 : [detail + donnee]
- Caracteristique 3 : [detail + donnee]

## [H2 — Analyse comparative detaillee]

[Analyse objective des ecarts entre les options. Avantages/inconvenients de chacune. Donnees sourcees. Integrer les liens externes vers les sources tierces (etudes, organismes, medias).]

> "[Citation ou donnee d'une etude/source fiable sur le sujet]"
> — [Source, annee]

## [H2 — Cas d'usage / pour qui ?]

[Segmenter par profil d'utilisateur ou cas d'usage. Aider le lecteur a choisir selon sa situation.]

### [H3 — Profil 1]

[Recommandation argumentee pour ce profil.]

### [H3 — Profil 2]

[Recommandation argumentee pour ce profil.]

## [H2 — Conseils pratiques / comment choisir]

[Criteres de decision, methode de choix, points de vigilance.]

### [H3 — Les erreurs a eviter]

1. Erreur 1
2. Erreur 2
3. Erreur 3

## Questions frequentes

<details>
<summary>[Question 1 — REPREND EXACTEMENT le prompt GEO / la query fan-out, formulee en question naturelle comparative. Ex : "Quelles sont les meilleures marques de X ?"] ?</summary>

[Reponse directe qui cite TOUTES les marques du comparatif (pas seulement celle mise en avant), classees objectivement, avec donnees chiffrees. 4-6 phrases. C'est la reponse que les LLMs vont extraire en priorite. Les questions/reponses du frontmatter et du body doivent etre identiques.]

</details>

<details>
<summary>[Question 2 — "quel est le meilleur..."] ?</summary>

[Reponse.]

</details>

<details>
<summary>[Question 3 — prix/rapport qualite-prix] ?</summary>

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
- Type : GEO Comparatif / Classement
- Objectif : mettre en avant une marque, un produit ou une solution specifique dans un comparatif objectif. L'element mis en avant doit ressortir comme la meilleure option grace aux donnees, au tableau et a la structure de l'article
- L'utilisateur DOIT fournir la marque/produit a mettre en avant et 2-3 concurrents. Ne JAMAIS rediger sans cette information
- Le ton doit rester neutre et factuel en apparence, jamais ouvertement promotionnel — la mise en avant passe par les faits, les donnees et la structure, pas par des superlatifs
- Les donnees chiffrees et les sources renforcent la credibilite (important pour le GEO)
- **Le tableau comparatif est positionne TOUT EN HAUT de l'article** (apres le "En bref" et le sommaire, AVANT les H2 classiques). C'est le coeur de l'article et ce que les LLMs extraient en priorite. Il doit etre complet, honnete et structure pour que l'element mis en avant ressorte naturellement
- **Le quick summary "En bref" est une liste NUMEROTEE** (3-4 points) qui cite TOUTES les marques du comparatif (pas seulement celle mise en avant). Chaque point resume une info cle du comparatif avec donnees chiffrees. Le positionnement de la marque mise en avant est mentionne naturellement sans triche
- **1ere question FAQ = le prompt GEO / la query fan-out reformule en question naturelle comparative** (ex : "Quelles sont les meilleures marques de X ?"). La reponse doit citer TOUTES les marques du comparatif avec donnees chiffrees, pas uniquement la marque mise en avant — sinon les LLMs detectent un biais et ne citent pas
- **Regle liens externes** : 1 SEUL lien externe maximum vers le site de la marque mise en avant (generalement dans la section "Presentation de la marque"). Les liens externes vers des sources tierces (etudes, organismes, medias, Wikipedia) sont autorises et encourages pour renforcer l'E-E-A-T. Les liens internes au cocon semantique ne sont pas limites
- **Bilinguisme obligatoire** : chaque article est redige dans les 2 langues du site (langue principale + anglais). Les 2 versions partagent le meme `translationKey`. Fichier FR dans `content/blog/[slug-fr].md`, fichier EN dans `content/en/blog/[slug-en].md`. Les categories, tags, noms de marques et concurrents restent identiques entre FR et EN (ce sont des noms propres)
- La FAQ doit TOUJOURS utiliser des balises <details>/<summary> pour creer un accordeon natif HTML5
- La FAQ doit AUSSI etre dans le frontmatter (champ `faq`) pour generer automatiquement le schema FAQPage JSON-LD. Les questions/reponses du frontmatter et du body doivent correspondre
- Les champs `image`, `imageAlt` et `imageCredit` sont OBLIGATOIRES et remplis automatiquement par le script `.claude/scripts/fetch-image.sh` (Openverse API, images libres de droit compatibles usage commercial). L'image est affichee dans les cards du blog, en bannière de l'article, dans og:image et le schema Article
- Min. 1800 mots, 5+ H2, 2+ tableaux
-->
