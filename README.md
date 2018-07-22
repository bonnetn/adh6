# ADH6
## Présentation
ADH est le système de gestion d'adhérent de l'association [MiNET](https://minet.net). Ce document a pour but de présenter la huitième version de notre outil.
## Motivations
Nous voulons produire un outil de gestion des adhérent **simple à maintenir**. Pour cela, nous prônons la *simplicité* dans *toutes* les parties de notre projet. Le but est de créer un outil maintenable, qui effectue **sa mission et qui l'a fait bien**.

Pour cela nous avons décidé de **dissocier le backend du frontend**. Ainsi un changement d'interface ne nous obligera pas à réécrire toute la logique du code (comme c'est le cas avec la précédente version).

Pour atteindre ses objectifs, nous essayons de **réduire le boilerplate code** en utilisant des bibliothèques qui sont *réputées et prouvées stables*. Cela permettra d'avoir moins de lignes de code, plus de *readability* et donc moins de potentiel bug.

La **fiabilité** de notre outil est aussi un concept important à nos yeux. C'est pour cela que nous faisons beaucoup appels à des **tests d'intégration** (*200+ pour la partie backend pour l'instant*). Nous visons un taux de *code coverage* le plus haut possible.

# Communication client/serveur

Pour communiquer entre le client et le serveur, nous avons décidé d'utiliser une
API.
En terme de techno, on a décidé de prendre la techno la plus stable et
universelle (compatible avec tous les futurs projets), HTTP.

Nous avons décidé de ne pas reprogrammer à la main tout un client/serveur pour
notre API. Ca aurait était faisable, mais trop error-prone et on risque de
perdre en flexibilité (un changement dans l'API devrait être réfléchi dans le
code du client ET du serveur). Nous avons donc décidé d'utiliser un système de
"generation" de code automatique à partir d'une spec.

Pour définir la specification de notre API nous utilisons OpenAPI (aussi appelé
swagger, oui, oui...).

Pour générer le code serveur, on utilise d'un côté connexion, qui est une
libary python développée par Zalando. https://github.com/zalando/connexion
Allez voir le repo, il est assez actif. C'est aussi la bibliothèque de
génération de code prise comme référence par Swagger (l'organisme qui fait
OpenAPI).

Pour le côté client, on utilise directement swagger-codegen, édité directement
par Swagger. https://github.com/swagger-api/swagger-codegen Pareil, allez voir
leur repo, il est "assez" actif... (10 228 commits à l'heure où j'écris ces
lignes, et plus de 900 contributeurs...)
Ca semble donc aussi être un assez bon choix pour produire un code stable.

En résumé, on a pris le parti prix d'ajouter deux dépendances au projet, mais
on a gagné en flexibilité et en maintenabilité.
