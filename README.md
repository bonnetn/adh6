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
