# TD noté - VueJS

## Notre équipe

### Développeur 1

- Nom : BOURREAU
- Prénom : QUENTIN
- Identifiant Github : [BOURREAUQuentin](https://github.com/BOURREAUQuentin)

### Développeur 2

- Nom : RIBEROU
- Prénom : Kylian
- Identifiant Github : [KylianRIBEROU](https://github.com/KylianRIBEROU)

## Notre projet

Voici le lien vers notre GitHub : https://github.com/KylianRIBEROU/TD_NOTE_VUEJS

Notre application est une application Client/Serveur de quizz où l'on peut visionner l'ensemble des questionnaires avec leurs questions. On peut répondre à une question. De plus, nous avons respecté le CRUD, c'est-à-dire la modification, la suppression et l'ajout. Ainsi, nous pouvons modifier un questionnaire (son nom), une question spécifique (nom, choix et bonne réponse). Nous pouvons supprimer une question spécifique ou un question complet. Puis, nous pouvons ajouter un questionnaire complet ou uniquement une question spécifique à un questionnaire. De plus, nous avons géré les erreurs possibles. En effet, par exemple, lors de la modification d'une question, si l'on change la bonne réponse parmi les choix possibles sans modifier directement la bonne réponse, cela nous affiche une erreur.

## Lancement de notre projet

Pour lancer notre projet, vous devez respecter ces commandes dans l'ordre suivant. Nous précisons qu'il faut, au préalable, avoir installé le package npm.

### Lancement du serveur

Pour lancer le serveur, il faut avoir les dépendances et librairies python requises.

Vous pouvez donc lancer un environnement virtuel.

```
a
```

Ensuite vous l'activez : `source .env/bin/activate` ou `source .env/Scripts/activate` sur windows

Enfin vous pouvez installer les dépendances : `pip install -r serveur/requirements.txt`

1. Déplacer vous à la racine du projet.
2. Lancer le serveur avec la commande suivante dans un terminal (pas dans un IDE) :
```bash
flask run
```

### Lancement du client

1. Déplacer vous dans le dossier client du projet (cd ./client).
2. Lancer le client avec la commande suivante dans un autre terminal (pas dans VS Code) :
```bash
npm run dev --host
```
3. Redigirez vous vers le lien de la dernière commande : http://localhost:8000

#

BOURREAU Quentin / RIBEROU Kylian - BUT informatique 2.3.B
