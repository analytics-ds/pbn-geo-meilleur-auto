---
description: Push les modifications locales vers GitHub et declenche le deploiement GitHub Pages. Utiliser ce skill quand l'utilisateur demande de deployer, publier, push, ou mettre a jour le site en ligne.
user_invocable: true
---

# Skill : Deployer sur GitHub Pages

Ce skill commit et push les modifications locales vers GitHub, ce qui declenche automatiquement le deploiement via GitHub Actions.

## Declenchement

L'utilisateur tape `/github-deploy` ou demande de deployer / publier / push / mettre en ligne.

## Etape 1 : Verification

Verifier que le repo git est configure avec un remote :

```bash
git remote -v
```

Si pas de remote, rediriger l'utilisateur vers `/github-setup`.

## Etape 1.5 : Pull avant deploiement (sync obligatoire)

**Standard reseau PBN GEO datashake** : plusieurs consultants travaillent sur le meme repo. Avant de push, toujours pull pour recuperer les changements des collegues et eviter les conflits.

```bash
git pull --rebase origin main
```

Si le pull echoue (conflit de merge, divergence) : **STOP**. Ne pas tenter de resoudre automatiquement. Avertir l'utilisateur et lui demander de resoudre a la main avant de relancer `/github-deploy`.

## Etape 2 : Build de verification

```bash
hugo
```

Si le build echoue, corriger les erreurs avant de continuer.

## Etape 3 : Commit et push

```bash
git add -A
git status
```

Afficher les fichiers modifies a l'utilisateur. Creer un commit avec un message descriptif :

- Si c'est un nouvel article : "Ajout article : [titre de l'article]"
- Si c'est une modification SEO : "MAJ SEO : [description courte]"
- Si c'est plusieurs changements : "MAJ : [resume des changements]"

```bash
git commit -m "[message]"
git push origin main
```

**Standard reseau PBN GEO datashake** : on push toujours direct sur `main`. Jamais de branche annexe ni de PR.

## Etape 4 : Suivi du deploiement

```bash
gh run list --limit 1
```

Informer l'utilisateur :
- Le deploiement est en cours
- L'URL du site sera a jour dans 1-2 minutes
- Il peut suivre le deploiement dans l'onglet Actions du repo
