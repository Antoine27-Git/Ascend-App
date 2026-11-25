# BACKLOG — idées gardées pour plus tard (Ascend)

Ce ne sont pas des décisions. Chaque idée sera rouverte, challengée et tranchée avant d'être codée.

## Journal de bord du renforcement (07/10/2026)
- **Besoin :** un utilisateur veut suivre sa progression en renforcement (charges, scores, reps), quel que soit le type : salle, maison, CrossFit, Hyrox, etc.
- **Principe :** le journal est séparé du moteur. Le moteur ne lit que la saisie minimale (durée, RPE, jambes sollicitées, D-74).
- **Activation :** un réglage du profil (désactivé par défaut), pas le type de séance.
- **Contenu possible :** exercices, charges, séries × reps, score de WOD, Rx/scaled, courbe de progression par exercice. Les anciens champs (wodName, score, lifts, wod) sont conservés dans les séances déjà saisies.
- **Condition pour démarrer :** que le formulaire minimal soit en place et utilisé.

## Bibliothèque (25/11/2026) — maquette proposée, à valider
- 5e onglet « Biblio » : fiches par thème (titre clair, source, niveau de preuve, à retenir, ce que ça change pour toi, limites, lien). Départ : les sources déjà utilisées par l'appli. Maquette : `docs/maquettes/screens_biblio.py`.

## Priorités issues de l'audit du 15/11/2026 (`docs/audit/AUDIT-2026-11-15.md`)
**Ordre validé par Antoine le 16/11/2026.** Aucun nouvel indicateur d'analyse avant la fin du point 3.

Décisions du 16/11/2026 :
- **Photo de WOD : abandonnée.** Retirée au ménage du 25/11 (`docs/PHOTO-WOD.md`, ancien formulaire de WOD ; la fonction `analyze-wod` n'était plus dans le dépôt).
- **Journal de renforcement : gelé**, gardé comme évolution à faire plus tard.
- **Règles v1 : à retirer du moteur dans une version à part** (avec `sim8.py`, `sim3.py`, `serie11.py` et la parité), rien d'autre dans cette version.
- **Connaissances du Projet claude.ai** : copies de septembre supprimées le 16/11 (le dépôt fait foi). `MOTEUR-V0.md` gardé : il n'existe pas dans le dépôt.
- Antoine a exporté un fichier JSON de ses données le 16/11.
1. **Fiabilité** : faits : P-23 (v76), P-07 (v76), P-08 (v82, choix A). P-24 et P-27 (v83). Restent : P-25 et P-26 (synchro à deux téléphones, heure du téléphone).
2. ~~**Ménage sans changement de comportement**~~ : **fait le 25/11/2026** (v79). Reste : retirer les règles v1 du moteur, dans une version à part.
3. **Régularité** : semaine chargée (P-02), question hebdomadaire sur la sortie longue (P-31), alerte avant de perdre son niveau (P-05).
4. **Avant fin février 2027** : nutrition (D-104, écrite, pas codée), signal de fatigue (P-10, P-17), reprise après maladie (P-11).
5. **Avant le bloc du 50 km** : descente (P-19).
Autres propositions ouvertes de l'audit du 11/11 : P-01, P-03 à P-06, P-09, P-14, P-15, P-22, P-25, P-26, P-28, P-30, P-33 à P-36 (`docs/audit/propositions.md`).

## « Résistance » détaillée (15/11/2026) — spec validée, pas codée
- Trois repères, 1re moitié contre 2e moitié : cardio, montée, descente. Sorties d'au moins 1 h 30. Cadence laissée de côté. Affichée dans Suivi sous la ligne « Résistance » (nom dans le code : `tenue`). Aucun effet sur le plan.
- Spec : document du Projet `claude/SPEC-DURABILITE-brouillon.md`. Numéros à prendre : D-109, H-72 (D-108 pris par la synchro, v76).
- Audit du 15/11 : facultatif ; rien d'exploitable avant fin janvier (première sortie d'1 h 30 vers le 20/12 sur un profil proche).

## Segments comparés par GPS (15/11/2026) — spec à écrire
- Besoin : reconnaître une sortie ou un segment déjà fait et montrer l'évolution (G-TER-002, D-55, D-58 : décidés sur le papier, rien de codé).
- Décision d'Antoine : lire les coordonnées GPS. Cela remplace le « jamais la position » de D-100 : à écrire dans la spec.
- Garde-fous proposés : l'appli ne garde que le début et la fin de chaque segment ; aucune coordonnée envoyée à l'IA, qui reçoit le résultat de la comparaison.
- Lié : séance de repère (D-55, D-58), gardée pour plus tard.

## Autres chantiers ouverts
- Import de l'historique complet (écart n° 5, partie restante).
- Signal de fatigue option C (RPE attendu vs RPE réel), qui dépend du modèle allure-effort.
- Lecture des commentaires de séance dans le bilan de phase.
- Liaison du Project avec GitHub.
- Option « malade ou douleur » pour une séance manquée, le jour où le moteur y réagit autrement que « fatigue » (D-72).
