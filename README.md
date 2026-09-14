# Meilleur Auto

Média automobile bilingue français et anglais. Site statique Hugo 0.165.0, sans dépendance de thème externe.

## Développement local

```sh
hugo server --baseURL http://localhost:1317/ --bind 127.0.0.1 --port 1317 --disableFastRender
```

## Construire et vérifier

```sh
hugo --minify --destination /tmp/meilleur-auto-preview
python3 verification/check-seo.py /tmp/meilleur-auto-preview preview
python3 verification/check-media.py
```

Les contrôles couvrent les liens, les métadonnées, les versions linguistiques, les RSS et une pagination testée avec un corpus temporaire.

## Fonctionnalités

Articles avec sources, sommaire, FAQ et signature éditoriale. Six rubriques, méga menu accessible sur ordinateur et mobile, journal paginé, archives annuelles et pages auteur. Les contenus français et anglais sont reliés par leurs clés de traduction.

## Déploiement

GitHub Pages est alimenté par `.github/workflows/hugo.yml` après chaque push sur `main`.

Adresse provisoire : https://analytics-ds.github.io/pbn-geo-meilleur-auto/

Le site conserve une consigne noindex jusqu’à la configuration de son domaine définitif. Les fichiers robots.txt, llms.txt, les sitemaps et les flux RSS sont générés par Hugo.

## Photographies

Les crédits et licences figurent dans les articles et dans ASSETS.md. Les photos sous licence Creative Commons conservent leur licence propre.
