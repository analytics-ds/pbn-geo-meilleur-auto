---
description: Initialise un repo GitHub et active GitHub Pages pour le site Hugo. Utiliser ce skill quand l'utilisateur demande de mettre le site sur GitHub, de creer un repo, ou mentionne "github-setup", "push sur github", "mettre en ligne".
user_invocable: true
---

# Skill : GitHub Setup

Ce skill initialise un depot GitHub pour le site Hugo et active le deploiement automatique via GitHub Pages.

## Declenchement

L'utilisateur tape `/github-setup` ou demande de mettre le site sur GitHub / en ligne.

## Prerequis

### GitHub CLI (gh)

Verifier que `gh` est installe :

```bash
gh --version
```

Si absent, demander a l'utilisateur de l'installer :

```bash
brew install gh
```

### Authentification GitHub

Verifier que l'utilisateur est connecte et qu'il a le scope `workflow` (necessaire pour pusher `.github/workflows/`) :

```bash
gh auth status
```

Verifier dans la sortie que `Token scopes` contient `workflow`. Si le scope `workflow` est absent, ou si l'utilisateur n'est pas connecte, lancer l'authentification avec le scope workflow :

```bash
gh auth login -s workflow
```

**IMPORTANT :** Cette commande est interactive (l'utilisateur doit ouvrir une URL dans son navigateur et saisir un code). Le systeme doit lancer la commande via Bash pour que l'utilisateur n'ait qu'a se connecter dans son navigateur. Ne PAS demander a l'utilisateur de la lancer manuellement.

## Etape 1 : Collecter les informations

Demander a l'utilisateur :

- **Nom du repo** : proposer le nom du site en slug (ex: "mon-blog-voyage"). L'utilisateur peut choisir autre chose.
- **Visibilite** : **toujours public**. GitHub Pages ne fonctionne pas sur les repos prives sans plan GitHub Pro/Team. Ne pas proposer l'option prive sauf si l'utilisateur le demande explicitement et confirme qu'il a un plan payant
- **Description** : courte description du repo (reprendre la description du site dans le CLAUDE.md)

## Etape 2 : Initialiser git

Si le dossier n'est pas deja un repo git :

```bash
git init
```

Verifier que le `.gitignore` existe (normalement cree par `/create-site`). S'il manque, le creer :

```
public/
resources/
.hugo_build.lock
.DS_Store
```

## Etape 3 : Creer le repo GitHub

```bash
gh repo create [nom-du-repo] --source=. --push --[public|private] --description "[description]"
```

Cette commande :
- Cree le repo sur GitHub
- Ajoute le remote `origin`
- Push le code

Si le code n'a pas encore ete commit, d'abord :

```bash
git add -A
git commit -m "Initial commit : site Hugo [nom du site]"
```

## Etape 4 : Configurer GitHub Pages

Activer GitHub Pages via GitHub Actions (le workflow `hugo.yml` est deja en place grace a `/create-site`) :

```bash
gh api repos/{owner}/{repo}/pages -X POST -f "build_type=workflow" 2>/dev/null || gh api repos/{owner}/{repo}/pages -X PUT -f "build_type=workflow"
```

Si l'API retourne une erreur (repo prive sans GitHub Pro, ou Pages pas encore disponible), expliquer le probleme a l'utilisateur.

## Etape 5 : Mettre a jour le baseURL

Recuperer l'URL GitHub Pages :

```bash
gh api repos/{owner}/{repo}/pages --jq '.html_url'
```

Si le `baseURL` dans `hugo.toml` est encore un placeholder ou ne correspond pas, le mettre a jour avec l'URL reelle.

Mettre aussi a jour la section "Contexte du site" du CLAUDE.md avec l'URL definitive.

## Etape 6 : Verification

Attendre que le premier deploiement se termine :

```bash
gh run list --limit 1
```

Informer l'utilisateur :
- URL du repo : `https://github.com/{owner}/{repo}`
- URL du site : `https://{owner}.github.io/{repo}/`
- Le premier deploiement peut prendre 1-2 minutes
- L'utilisateur peut suivre le deploiement dans l'onglet Actions du repo

## Etape 7 : Recapitulatif

Afficher :
- URL du repo GitHub
- URL du site en ligne
- Rappeler que chaque push sur `main` declenche un deploiement automatique
- Rappeler que `/create-article-geo` push automatiquement apres la creation d'un article
- Rappeler que `/github-deploy` permet de push manuellement a tout moment
