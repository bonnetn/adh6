# API

## Cas d'utilisation

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
