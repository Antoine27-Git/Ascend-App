# Règles de gestion — Ascend

Registre des principes décidés pour l'app. Une règle = un identifiant stable,
un énoncé, sa justification, sa date. On ne réécrit pas l'historique : une règle
abandonnée passe en `[abandonnée]` avec la date et le motif, elle ne disparaît pas.

## Format des identifiants

`R-CAT-nnn` — la numérotation repart de 001 dans chaque catégorie, ce qui permet
d'insérer une règle sans casser la logique des autres.

| Code | Catégorie |
|------|-----------|
| DAT | Données, stockage, synchronisation |
| SEC | Compte, authentification, confidentialité |
| ENT | Entraînement, principes généraux |
| REN | Renforcement |
| MET | Conventions de travail |

Catégories prévues et non encore ouvertes : `NUT` (nutrition), `BLE` (blessure et
reprise), `UI` (interface et ergonomie). Créer une catégorie = ajouter une ligne
au tableau ci-dessus et une section plus bas, jamais renuméroter l'existant.

Quand une règle s'appuie sur une source, elle la cite : `→ S-CAT-nnn` (voir SOURCES.md).

---

## DAT — Données et stockage

**R-DAT-001 — Le stockage local n'est jamais la source de vérité, seulement un tampon hors-ligne.**
Motif : un nettoyage de navigateur ou un changement de domaine efface tout l'historique.
Incident vécu le 13/09/2026. 14/09/2026

**R-DAT-002 — Une ligne par objet (profil, séance, check-in, séance planifiée), jamais un bloc unique.**
Motif : avec un bloc unique, le dernier appareil qui synchronise écrase les modifications
de l'autre. Par objet, seule une modification réellement concurrente est arbitrée. 14/09/2026

**R-DAT-003 — Les conflits se résolvent à l'horodatage de l'édition, objet par objet.**
Motif : une saisie faite hors réseau samedi doit perdre face à une modification faite
dimanche sur un autre appareil, pas face à l'heure de synchronisation. 14/09/2026

**R-DAT-004 — Toute donnée est exportable en JSON et CSV, indépendamment de la synchronisation.**
Motif : porte de sortie que l'utilisateur contrôle, analyse externe possible,
et sauvegarde qui ne dépend d'aucun service tiers. 14/09/2026

**R-DAT-005 — L'app doit se lancer et fonctionner sans réseau.**
Motif : usage principal en montagne, souvent sans couverture. Implique un service
worker, pas seulement un stockage local. 14/09/2026

## SEC — Compte et sécurité

**R-SEC-001 — Authentification par email et mot de passe, pas de compte anonyme lié à l'appareil.**
Motif : un compte anonyme est perdu au premier nettoyage du navigateur, sans récupération
possible. L'email permet de récupérer l'accès depuis n'importe quel appareil. 14/09/2026

**R-SEC-002 — L'isolation des données repose sur les politiques RLS du serveur, jamais sur la clé publique.**
Motif : la clé « publishable » est par conception lisible dans le code client ;
elle n'est pas un secret et ne protège rien. 14/09/2026

**R-SEC-003 — Les messages d'erreur d'authentification ne révèlent jamais si un email existe.**
Motif : éviter qu'un tiers puisse énumérer les comptes existants. Exception assumée :
à la création de compte, on signale qu'un compte existe déjà, sinon l'utilisateur
est bloqué sans comprendre. 15/09/2026

## ENT — Entraînement, principes généraux

**R-ENT-001 — Aucun plan n'est générique : ce sont les paramètres et les données du coureur qui le produisent.**
Motif : principe fondateur de l'app. Toute fonctionnalité qui imposerait une trame
identique pour tous est à rejeter. 15/09/2026

**R-ENT-002 — Les zones affichées restent les zones théoriques ; la fenêtre personnelle est une consigne distincte.**
Motif : ne pas masquer la référence physiologique derrière un réglage personnel,
pour que l'écart entre les deux reste visible et discutable. 14/09/2026

## REN — Renforcement

**R-REN-001 — L'app prescrit une qualité et une dose, jamais un exercice imposé.**
Motif : la modalité (salle, box, maison, extérieur) varie selon le coureur et dans le
temps ; la qualité travaillée, elle, est ce qui produit l'adaptation. 15/09/2026

**R-REN-002 — Trois qualités couvertes : force maximale, pliométrie, excentrique.**
Motif : la force maximale améliore l'économie de course sur la plage de vitesses la
plus large ; la pliométrie agit surtout aux allures basses, donc en ultra ; l'excentrique
vise la tolérance à la descente. → S-REN-001, S-REN-002, S-REN-003. 15/09/2026

**R-REN-003 — Toute séance de renforcement est enregistrable en mode « imposée », sans prescription.**
Motif : un WOD en box ou un cours collectif est subi, pas choisi. Sans ce mode,
la charge réelle mesurée par l'app serait fausse. 15/09/2026

**R-REN-004 — La saisie minimale d'une séance de renforcement tient en quatre champs : durée, RPE, dominante, densité excentrique.**
Motif : le produit durée × RPE donne une charge comparable entre séances ; la dominante
détermine le conflit avec la course ; la densité excentrique détermine le coût de
récupération. Le texte libre reste une note, jamais une donnée de calcul. → S-CHA-001. 15/09/2026

**R-REN-005 — Alerte si une séance à dominante jambes en force ou à forte densité excentrique tombe à moins de 24 h d'une sortie longue ou de descentes.**
Motif : c'est la fenêtre où l'interférence aiguë est la plus marquée. → S-CHA-002. 15/09/2026

## MET — Conventions de travail

**R-MET-001 — Toute affirmation d'entraînement dans l'app doit pouvoir être reliée à une source ou être explicitement marquée comme extrapolation.**
Motif : éviter que des choix de confort prennent l'apparence de vérités établies. 15/09/2026

**R-MET-002 — Chercher d'abord la solution la plus simple, et ne complexifier qu'une fois la simple démontrée insuffisante.**
Motif : plusieurs allers-retours perdus sur des mécanismes inutiles (mémorisation
d'un délai que le navigateur gérait déjà seul). 15/09/2026
