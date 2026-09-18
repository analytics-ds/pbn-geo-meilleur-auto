# Skill : Partager le site via ngrok

Ce skill lance le serveur Hugo + un tunnel ngrok pour rendre le site accessible a d'autres personnes via un lien public.

## Declenchement

L'utilisateur tape `/share`.

## Prerequis

- **Hugo** doit etre installe (`brew install hugo`)
- **ngrok** doit etre installe et configure (`brew install ngrok`)
- Si ngrok n'est pas installe, proposer de l'installer
- Si ngrok n'est pas configure (pas de authtoken), demander a l'utilisateur :
  1. Creer un compte sur https://dashboard.ngrok.com/signup
  2. Recuperer son authtoken sur https://dashboard.ngrok.com/get-started/your-authtoken
  3. Lancer `ngrok config add-authtoken TOKEN`

## Actions

1. Verifier que Hugo et ngrok sont installes
2. Lancer le serveur Hugo en arriere-plan sur le port 8080 :

```bash
hugo server --bind 0.0.0.0 --port 8080
```

3. Lancer ngrok en arriere-plan :

```bash
ngrok http 8080 --log stdout
```

4. Recuperer l'URL publique ngrok dans les logs (ligne `started tunnel ... url=https://xxx.ngrok-free.dev`)
5. Afficher a l'utilisateur :
   - Le lien public a partager
   - Rappeler que les visiteurs verront une page d'avertissement ngrok au premier acces (cliquer "Visit Site")
   - Le lien change a chaque relance de ngrok (version gratuite)

## Arreter

Pour tout arreter, l'utilisateur demande a Claude qui stoppe les deux taches en arriere-plan (Hugo + ngrok).
