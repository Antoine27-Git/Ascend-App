# BACKLOG — idées gardées pour plus tard (Ascend)

Ce ne sont pas des décisions. Chaque idée sera rouverte, challengée et tranchée avant d'être codée.

## Journal de bord du renforcement (07/10/2026)
- **Besoin :** un utilisateur veut suivre sa progression en renforcement (charges, scores, reps), quel que soit le type : salle, maison, CrossFit, Hyrox, etc.
- **Principe :** le journal est séparé du moteur. Le moteur ne lit que la saisie minimale (durée, RPE, jambes sollicitées, D-74).
- **Activation :** un réglage du profil (désactivé par défaut), pas le type de séance.
- **Contenu possible :** exercices, charges, séries × reps, score de WOD, Rx/scaled, courbe de progression par exercice. Les anciens champs (wodName, score, lifts, wod) sont conservés dans les séances déjà saisies.
- **Photo (analyze-wod) :** le pré-remplissage du journal à partir d'une photo dépend de cette fonctionnalité.
- **Condition pour démarrer :** que le formulaire minimal soit en place et utilisé.

## Priorités issues de l'audit du 15/11/2026 (`docs/audit/AUDIT-2026-11-15.md`)
**Ordre validé par Antoine le 16/11/2026.** Aucun nouvel indicateur d'analyse avant la fin du point 3.

Décisions du 16/11/2026 :
- **Photo de WOD : abandonnée.** À retirer au lot « ménage » : fonction `analyze-wod` (jamais déployée), `docs/PHOTO-WOD.md`, restes de l'ancien formulaire de WOD dans `index.html`.
- **Journal de renforcement : gelé**, gardé comme évolution à faire plus tard.
- **Règles v1 : à retirer du moteur dans une version à part** (avec `sim8.py`, `sim3.py`, `serie11.py` et la parité), rien d'autre dans cette version.
- **Connaissances du Projet claude.ai** : copies de septembre supprimées le 16/11 (le dépôt fait foi). `MOTEUR-V0.md` gardé : il n'existe pas dans le dépôt.
- Antoine a exporté un fichier JSON de ses données le 16/11.
1. **Fiabilité** : P-23 (profil écrasé après effacement du navigateur), P-24 (restauration sûre), P-27 (rappel d'export), P-07 (heure d'été, avant le 28/03/2027), P-08 (sortie longue fantôme).
2. **Ménage sans changement de comportement** : code jamais appelé, statuts de SPEC.md, AGENTS.md, tests d'interface dans la batterie, 155 bpm en dur, Connaissances du Projet.
3. **Régularité** : semaine chargée (P-02), question hebdomadaire sur la sortie longue (P-31), alerte avant de perdre son niveau (P-05).
4. **Avant fin février 2027** : nutrition (D-104, écrite, pas codée), signal de fatigue (P-10, P-17), reprise après maladie (P-11).
5. **Avant le bloc du 50 km** : descente (P-19).
Autres propositions ouvertes de l'audit du 11/11 : P-01, P-03 à P-06, P-09, P-14, P-15, P-22, P-25, P-26, P-28, P-30, P-33 à P-36 (`docs/audit/propositions.md`).

## « Résistance » détaillée (15/11/2026) — spec validée, pas codée
- Trois repères, 1re moitié contre 2e moitié : cardio, montée, descente. Sorties d'au moins 1 h 30. Cadence laissée de côté. Affichée dans Suivi sous la ligne « Résistance » (nom dans le code : `tenue`). Aucun effet sur le plan.
- Spec : document du Projet `claude/SPEC-DURABILITE-brouillon.md`. Numéros à prendre : D-108, H-72.
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
- Déploiement de la fonction Supabase analyze-wod.
- Rétablir les textes de H-38 et H-39 dans HYPOTHESES.md (H-40 réécrite le 09/11/2026, D-94).
- Liaison du Project avec GitHub.
- Option « malade ou douleur » pour une séance manquée, le jour où le moteur y réagit autrement que « fatigue » (D-72).
