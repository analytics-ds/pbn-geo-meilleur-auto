# Prompts avatars des auteurs

Style unifie pour tous les avatars : **flat illustration portrait, vector style, soft pastel palette, centered headshot, clean neutral background, friendly professional expression, shoulders up, 1:1 square ratio**.

Conventions :
- Taille cible : 512x512 px
- Format final : WebP (convertir avec `cwebp -q 85`)
- Chemin de destination : `static/images/authors/[id].webp`

## Thomas Durand — Tech

```
Flat vector illustration portrait, headshot of a confident man in his mid-30s, short dark brown hair neatly styled, rectangular glasses, slight smile, wearing a dark navy blazer over a light grey shirt, soft pastel palette with muted blue tones, clean neutral background with subtle tech patterns (circuit lines) faintly visible, centered composition, shoulders up, 1:1 square ratio, modern editorial style, friendly professional expression.
```

Destination : `static/images/authors/thomas-durand.webp`

## Magalie Ergoz — Mode & beaute

```
Flat vector illustration portrait, headshot of a stylish woman in her late 20s, long wavy auburn hair, subtle makeup, confident smile, wearing an elegant cream-colored silk blouse with a delicate gold necklace, soft pastel palette with blush pink and rose gold tones, clean neutral background with very faint floral motifs, centered composition, shoulders up, 1:1 square ratio, modern fashion editorial style, warm friendly expression.
```

Destination : `static/images/authors/magalie-ergoz.webp`

## Claire Beaumont — Maison & renovation

```
Flat vector illustration portrait, headshot of a creative woman in her mid-30s, medium-length wavy brown hair in a casual bun, confident gentle smile, wearing a mustard-yellow loose cardigan over a white t-shirt with a simple geometric pendant, soft pastel palette with warm terracotta and sage green tones, clean neutral background with very subtle architectural line patterns, centered composition, shoulders up, 1:1 square ratio, modern editorial style, approachable artistic expression.
```

Destination : `static/images/authors/claire-beaumont.webp`

## Laura Verdier — Sante & bien-etre

```
Flat vector illustration portrait, headshot of a radiant woman in her early 30s, shoulder-length straight blonde hair, natural minimal makeup, calm warm smile, wearing a soft sage-green linen shirt, soft pastel palette with mint green and cream tones, clean neutral background with very subtle leaf or herb motifs, centered composition, shoulders up, 1:1 square ratio, modern wellness editorial style, serene friendly expression.
```

Destination : `static/images/authors/laura-verdier.webp`

## Kevin Moreau — Transport & mobilite

```
Flat vector illustration portrait, headshot of a dynamic man in his late 30s, short brown hair with a modern side part, light stubble, confident smile, wearing a navy blue zip-up sweater over a white collared shirt, soft pastel palette with steel blue and slate grey tones, clean neutral background with very faint road or route line patterns, centered composition, shoulders up, 1:1 square ratio, modern editorial style, energetic friendly expression.
```

Destination : `static/images/authors/kevin-moreau.webp`

## Sophie Martin — Finance & patrimoine

```
Flat vector illustration portrait, headshot of a poised woman in her early 40s, chin-length straight dark brown bob haircut, subtle professional makeup, composed confident smile, wearing a charcoal grey structured blazer over a white blouse with a simple silver earring visible, soft pastel palette with deep blue and warm beige tones, clean neutral background with very subtle geometric patterns, centered composition, shoulders up, 1:1 square ratio, modern financial editorial style, trustworthy professional expression.
```

Destination : `static/images/authors/sophie-martin.webp`

## Workflow de generation

1. Generer chaque image via un generateur AI (Midjourney, DALL-E, Stable Diffusion) avec le prompt ci-dessus
2. Sauvegarder en PNG ou JPG 512x512 (ou plus)
3. Convertir en WebP : `cwebp -q 85 input.png -o static/images/authors/[id].webp`
4. Verifier la coherence visuelle : tous les avatars doivent avoir le meme style graphique (flat illustration, palette pastel, fond neutre) pour une identite editoriale unifiee
