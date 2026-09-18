# Skill : Lancer le serveur Hugo local

Ce skill lance le serveur Hugo en local pour previsualiser le site.

## Declenchement

L'utilisateur tape `/serve`.

## Actions

1. Verifier que Hugo est installe (`hugo version`)
2. Lancer le serveur en arriere-plan :

```bash
hugo server --port 1313
```

3. Afficher a l'utilisateur :
   - L'URL locale : `http://localhost:1313/`
   - Rappeler que le site se met a jour automatiquement a chaque modification de fichier

## Arreter le serveur

Pour arreter le serveur, l'utilisateur peut :
- Demander a Claude de l'arreter (Claude utilise `TaskStop` sur la tache en cours)
- Faire `Ctrl+C` dans son terminal
