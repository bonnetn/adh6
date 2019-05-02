# API ADH

## Architecture du projet

Bon. 
Au sein de votre vie vous aurez l'occaion de voir beaucoup de projet fait à l'arrache, sans réelle réflexion sur la façon de construire les choses et qui sont grosso-modo dégueulasse et difficilement maintenable.

Vous aurez aussi l'occasion de voir des projets qui sont 'over-designed', où la personne responsable du projet prend 20 ans à réfléchir au bon *design pattern* a appliquer pour **chaque** fonctionnalité mineure du projet.
Résultat le projet n'aboutit jamais parce que on passe 1 semaine à faire un truc qui se code en 1 heure.

Mon objectif, pour ADH est de vous montrer ce quest un projet *backend* avec une belle architecture, mais sans aller dans l'*over-design*. 
J'espère que l'architecture choisie vous convaincra par ses qualités de maintabilité.
Vous pourrez réutiliser les principes dans d'autres projet (backend ou frontend).

## Clean/Onion architecture

Un type d'architecture qui est grosso-modo unanimement reconnu dans le monde de l'info comme un bon modèle est la *clean archi* telle que décrite par  Robert C. Martin (Uncle Bob).

C'est aussi assez connu dans le monde du développement mobile, pour l'anectode j'ai un ami qui est tombé en entretien sur une question là dessus. 

[Vous pouvez voir l'article de *Uncle bob* sur son blog pour comprendre en détail.](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

![schema des couches telles que proposés par uncle bob](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg)

Le principe est assez classique: vous divisez votre application en couches, qui ont chacun un rôle bien défini. 
Le très connu [(si vous avez fait du web) modèle MVC](https://fr.wikipedia.org/wiki/Mod%C3%A8le-vue-contr%C3%B4leur) en est un exemple.

La *clean archi* en est une généralisation. 

Pour comprendre, je vous propose d'analyser ces couches une par une en prenant l'exemple d'ADH.

Si vous regardez dans le dossier `src/` vous retrouverez le nom des différentes couches et le code associé.

### Entity layer (Layer 1)

C'est le **coeur** de tous les projets. 

Les entités sont en quelque sorte les données gérées par l'application/l'assocation.

Normalement, un système gère de l'information (sinon ça sert à rien de dev' une application...), et c'est ça les entités.

Ce sont des structures de données très simples qui ne font que contenir de l'information (ce sont des [DAO](https://en.wikipedia.org/wiki/Data_access_object)s si vous aimez le Java).

Il ne doit pas y avoir de code/logique/algorithme dans cette couche! C'est juste de la donnée, ce qui donne la raison d'être de l'application.

**Pour ADH:** ADH est une app de gestion d'Adhérents. On retrouve donc une classe `Member`, très simple, qui contient les données utiles à MiNET concernant un adhérent.

On va aussi avoir d'autres données que l'application va gérer comme les chambres (`room`) ou le réseau (`port`, `switch` et `vlan`).


### Use case (Layer 2)

C'est le comportement de l'application. 

Il contient ce qu'on appelle la *Business logic*:
Quand vous avez un cas d'utilisation et que vous l'exprimez sous la forme d'un algorithme, c'est ce que vous allez mettre dans cette couche.

Cet algorithme doit être **TOTALEMENT** indépendant de la partie technique. Autrement dit, que ça soit une API HTTP qui communique avec du SQL, ou alors une personne réelle qui prend en charge les adhérents en notant les adhésions sur un carnet, l'algorithme doit être **le même**.

Vous allez toucher à cette couche quand vous voudrez changer le fonctionnement de ADH.

**Pour ADH:** pour la cotisation d'un adhérent
Si on avait à écrire en pseudocode ça donnerait un truc du genre:
> 1. Quand tu reçois une demande d'adhésion (que ça soit un gars qui te demande ou un appel HTTP)
>
> 2. Inscris une nouvelle écriture comptable dans le livre journal (on sait pas si c'est un livre journal physique ou une base de donnée)
>
> 3. Enregistre que l'adhérent a cotisé jusqu'à le 12 janvier 2100... (pareil, peu importe où on enregistre, c'est pas notre problème dans cette couche)
>
> 4. Active le port de l'adhérent (on pourrait utiliser une communication directe avec un switch ou alors demander à un admin de SSH sur le switch et de le faire manuellement)

Bon, dans ADH, plutôt qu'en pseudo-code on l'a fait en Python... Mais c'est presque pareil ! :D

Cette façon de faire, sans jamais mentionner la technique, nous permet de nous abstraire de TOUTE dépendance à une bibliothèque ou technologie qu'on utilise.

Si jamais un jour on ne veut plus utiliser MySQL, mais Redis ou elasticsearch pour stocker des données... Ben on aura pas à modifier ces deux premières couches. 
Pareil, si on en a marre des API REST et qu'on veut utiliser gRPC ou autre, on pourra.

Encore plus important: si on utilise une bibliothèque/framework comme Flask, connexion et SQLAlchemy et que l'un vient à être abandonné (ou qu'il y a une grosse faille de sécu), l'application n'en dépend pas et on aura pas à TOUT modifier.

**Point important: Vous ne devez pas importer des bibliothèques ni des classes de la prochaine couche ici. (Voir la *law of include* de l'article de Uncle Bob)**


### Interface handler (Layer 3)

C'est la couche technique. 
Très clairement, vous ne définissez aucun comportement de l'application ici, vous faites juste une interface entre le monde et l'application.

Si jamais vous changez la technologie derrière ADH, vous irez faire des modif ici.

**Pour ADH:**

*Pour le stockage*, vous allez faire des classes qui implémentent les opérations de base [CRUD (Create, Read, Update, Delete)](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) et jamais plus compliqué. Toutes les opérations plus compliquées, ou les décisions qui n'ont pas de rapport avec la technologie utilisée derrière doit être mis dans les use cases. 
Ca doit rester débile!


*Pour l'API*: les points d'entrée de l'application se trouvent aussi dans cette couche. 
Puisqu'on arrive dans l'appli par un appel HTTP, on a des fonctions qui vont gérer la requête, transformer les données brutes en entité, faire appel au use cases, et renvoyer les bons code d'erreur HTTP.

### Framework & drivers (Layer 4)

Cette partie, ça correspond pas vraiment a notre code mais plutôt aux dépendances qu'on utilise. 
Ici on va retrouver SQLAlchemy, connexion, flask, le client Elasticserach, etc...

En gros c'est le contenu de requirements.txt.


## Un exemple de bout en bout...
Je vais prendre un exemple simple: la création d'un appareil.

Vous (en tant qu'utilisateur) faites une requête HTTP vers adh6.minet.net contenant la MAC de votre nouvel appareil.

1. Les bibliothèques *connexion* et *Flask* utilisée par ADH6, prennent cette requête, et l'interprête. (Layer 4) 
Les bibliothèque appellent une fonction python.

2. Une fonction python (dans `src/inteface_handler/http_api/device.py`) reçoit la requête HTTP et la transforme en une entité, un truc compréhensible pour l'application sans avoir aucun lien avec la techno utilisée pour recevoir le message. (Layer 3) Cette fonction va ensuite appeler le use case `create_device`.

3. Le use_case create_device (dans `src/use_case/device_manager.py`) va lire l'entité de l'appareil, vérifier que l'adresse MAC est bien valide, que tout est bon (layer 2), et va faire une demande à un *repository* (interface abstraite qui représente un moyen de stocker des appareils, voir les notes ci-dessous en italique), de sauvegarder l'appareil. 

4. `DeviceSQLRepository` est une classe qui implémente (en gros elle satisfait toutes les contraintes) DeviceRepository, elle est utilisée par la use case et va utiliser SQLAlchemy pour créer (bêtement) un appareil. (Layer 3)

5. SQLAlchemy contacte le serveur MySQL pour faire l'écriture (Layer 4)


*Une interface est une sorte de patron, un moule, une contrainte, par exemple... un repository pour appareil doit au moins avoir une méthode qui permet de créer un appareil... Ces interfaces font partie de la couche 2*

*Si vous vous posez des questions de pourquoi je vous parle des interfaces, allez lire l'article de Uncle Bob sur la Law of Include, en théorie on a pas le droit (dans le use case) d'importer des fichiers de interface_handler.
Utiliser une interface permet de dépasser cette limitation*


Comme vous pouvez le voir, lors de chaque appel, on rentre dans l'*onion* de la couche 4 à 1 (même si il n'y a pas de code, la couche 1 est utilisée grâce aux entities). 
Puis on ressort de la couche 1 à 4 pour interagir avec le monde à nouveau.

Ce cas d'utilisation est assez simple. Finalement, il ne fait que valider la MAC de l'appareil, mais certains cas sont plus complexes, comme celui pour faire cotiser un adhérent.
Dans ce cas il faut valider les données, écrire dans le livre comptable, ajouter une adhésion, changer la date de départ du membre, et *log* l'action (parce que la tracabilité c'est important). 
Il faut aussi gérer les cas d'erreur.


## Questions?

Si vous avez des interrogations en lisant ce README sur la clean archi, c'est normal. Allez lire l'article de Uncle bob et cherchez un peu sur internet.
Une fois que vous avez trouvé la solution, ajoutez ci-dessous votre question/réponse.

Sinon vous pouvez contacter InsolentBacon directement (oubliez pas que vous pouvez utiliser cette archi dans vos autres projets).

#### Pourquoi se faire chier à faire 3 couches alors qu'on pourrait tout mettre dans les fonctions dans interface_handler/http_api?
> Comme dit précédemment, parce que le jour où tu voudras changer de techno tu seras tellement dépendant de tes libs que tu devras tout refaire.
> 
> Un autre critère important est la testabilité. En découpant en couches, tu peux faire des tests unitaires pour tes use cases très facilement en 'mockant' ta couche des interface handlers.
> 
> Tu peux faire des tests d'intégration pour tester... l'intégration avec ton SQL/server web. etc.
>
> Enfin, l'argument principal est l'inversion de dépendance (le D des principes SOLID https://en.wikipedia.org/wiki/SOLID)
>
> (et puis c'est plus facile de bosser avec des projets qui ont une archi claire et unifiée!)


#### Tu nous parles d'indépendance des technos... Mais on est toujours dépendant de python...
> Oui. On peut difficilement faire plus indépendant que le langage de prog' choisi. (Voir les raisons de pourquoi Python sur le wiki)

# Cas d'utilisation

On peut identifier les fonctions principales d'ADH - celles qui doivent toujours marcher et qui doivent bien être testées.


### Core use cases
La première priorité est que on puisse enregistrer des cotisations pendant la permanence, et ça nous permet de dégager une première liste des *use cases* prioritaires (*core use cases*).
Ces cas d'utilisations sont ceux qui seront **toujours** utilisés lors d'une permanence (où il y a du monde).

En gros, si une de ces fonctionnalités est *down*, on ne peut pas faire la perm' et la personne qui doit réparer a bien la pression. :D

* Ajouter une adhésion (`MemberManager.new_membership`): Pour faire cotiser les membres de l'association.
* Ajouter un membre (`MemberManager.update_or_create`): Pour les nouveaux adhérents, il faut pouvoir leur créer un profil.
* Lire le profil d'un membre (`MemberManager.get_by_username`): Pour accéder au profil d'un adhérent et vérifier que sa cotisation a bien été faite
* Ajouter un appareil (`DeviceManager.update_or_create`): Pour ajouter un nouvel appareil au compte de l'adhérent pour qu'il puisse se connecter au réseau.
* Chercher des appareils (`DeviceManager.search`): Pour chercher les appareils d'un adhérent (nécessaire pour voir tous les appareils sur son profil).

### Level 2 use cases
Ces cas d'utilisation sont des fonctionnalités qu'on a très souvent besoin en permanence mais qui ne sont pas indispensables. 

Si une de ces fonctionnalité est *down* on peut encore inscrire les gens et leur filer un accès internet. 
Certaines personnes devront repasser plus tard pour qu'on leur règle leur problème mais ça doit être une minorité.

En gros pendant la perm' tout le monde va râler, mais on peut encore fonctionner en mode dégradé.
* Lire les logs de q* Supprimer un appareil (`DeviceManager.delete`): Pour virer une MAC d'un profil adhérentuelqu'un (`MemberManager.get_logs`): Pour aider à débugger les problèmes des adhérents.
* Changer le mot de passe d'un membre (`MemberManager.change_password`): Pour changer le mot de passe d'un membre.
* Mettre à jour le profil d'un membre (`MemberManager.update_partially`): Pour changer les infos d'un membre ou le faire déménager de chambre.
* Chercher les membres (`MemberManager.search`): Pour ne pas à avoir à taper exactement le *username* des adhérents et pouvoir chercher leur profil avec leur nom.
* Voir les infos d'un appareil (`DeviceManager.get_by_mac_address`): Pour voir les infos d'un appareil (par exemple ses IPs)
* Supprimer un appareil (`DeviceManager.delete`): Pour virer une MAC d'un profil adhérent

### Level 3 use cases
C'est principalement des cas d'utilisés lors de la gestion en dehors des perms'. 
Si ces fonctionnalités tombent en panne ça affectera pas du tout (ou très peu) les perms.
Dans le pire des cas on peut se permettre d'aller dans la base de donnée pour faire manuellement les actions.

Ces cas d'utilisations sont ajoutés à ADH pour notre propre confort mais ne sont pas indispensables.
* Supprimer un membre (`MemberManager.delete`): Supprimer un adhérent de notre base de donnée, par exemple dans le cadre du droit à l'effacement de la RGPD (article 17).
