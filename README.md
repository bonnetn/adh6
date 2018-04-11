# ADH 2000

## How to setup the project
- Create a virtualenv ```virtualenv ./```
- Enter the virtualenv ```source bin/activate```
- Install the requirements ```pip3 install -r requirements.txt```
- Fill the settings files (there are some examples provided) ``` vim settings.py ``` & ``` vim unit_test_settings.py```
- Run the tests ```pytest```
- Launch the server ```python3 app.py```

## What the hell is this mess?
Ce projet consiste juste en l'implémentation des différents méthodes définies
dans la spécification de l'API. 

Si vous êtes un PGM et que vous voulez juste lire le code, sachez juste que tout
le code est dans le dossier *adh/*.

Pour que python se comporte en serveur   Web on utilise *Flask*, et pour pas 
avoir à faire de trucs compliqués on utilise *connexion* qui fait le binding 
entre *Flask* et les fonctions en python qui sont appelées presque magiquement.

La spécification de l'API est stockée dans swagger.yaml à la racine du projet,
ce fichier est automatiquement exporté de swaggerhub.
https://app.swaggerhub.com/apis/insolentbacon/adherents/

*En gros*, les fonctions importantes sont juste celles dans *adh/controller/*,
qui sont appelées quand on fait des requêtes vers le serveur web.

Maintenant, parce qu'on veut pas faire de requêtes directement dans la BDD SQL
(pour des raisons de sécurité et de flemme), on utilise *SQLAlchemy*. C'est en
fait une bibliothèque qui permet de manipuler des objets dans la BDD comme des
objets python (allez chercher ce qu'est un *ORM*).

En résumé on a:

- **controller/**: Le plus important, c'est là où sont les fonctions qui sont
appelées lorsque une requête HTTP est effectuée sur l'API.
- **model/**: C'est là où on définit ce qu'il y a dans la base de données (c'est
à dire les noms des tables, des colonnes, les contraintes qu'il y a sur les
champs [genre une IP doit être valide]). On importe ensuite les modèles dans les
controllers pour manipuler la BDD
- **settings/**: Euh, ben c'est là où y'a les settings de l'application...
j'vais pas vous faire un dessin
- **exceptions/**: c'est là où on met les erreurs custom qu'on a défini, c'est
peu important
- **test/**: c'est là où il y a des les tests. C'est super important. On teste
chacune des lignes de code des fichiers .py (on vise un *code coverage* de 100%)
Les cas normaux et extrêmes doivent être testés. C'est ce qui est executé
lorsque on lance pytest.


## Code coverage report generation:
> pytest --cov=adh --cov-report html

## On committing...
Your commit must pass all the tests
If you add a piece of code you should write a test to test it
