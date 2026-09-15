# Sources — Ascend

Base des références utilisées pour justifier les règles d'entraînement (voir REGLES.md).

## Format des identifiants

`S-CAT-nnn` — numérotation indépendante par catégorie, comme pour les règles.

| Code | Domaine |
|------|---------|
| REN | Renforcement musculaire |
| CHA | Charge d'entraînement, planification, interférence |
| COU | Course à pied, physiologie de l'endurance |
| TRA | Spécificités trail : dénivelé, descente, terrain |
| NUT | Nutrition, hydratation |
| BLE | Blessure, prévention, reprise |

Catégories ouvertes à ce jour : REN, CHA. Les autres existent dans la nomenclature
mais n'ont pas encore de source.

## Règle d'entrée

Une source ne rentre que si elle est vérifiable — titre, auteurs, année, revue, lien.
Aucune référence citée de mémoire sans vérification.

## Niveau de preuve

- `élevé` — méta-analyse ou revue systématique, résultats convergents
- `modéré` — méta-analyse avec hétérogénéité, ou essais contrôlés concordants
- `faible` — étude isolée, petit échantillon, ou population éloignée de la nôtre
- `extrapolation` — aucune preuve directe, raisonnement de spécificité uniquement

Ce dernier niveau est le plus important à ne pas dissimuler : il signale les endroits
où l'app décide sans appui démontré.

---

## REN — Renforcement musculaire

### S-REN-001 — Force maximale et économie de course
Llanos-Lagos C., Ramirez-Campillo R., Moran J., Sáez de Villarreal E.
*Effect of Strength Training Programs in Middle- and Long-Distance Runners' Economy at
Different Running Speeds: A Systematic Review with Meta-analysis.*
Sports Medicine, 2024. DOI 10.1007/s40279-023-01978-y
https://link.springer.com/article/10.1007/s40279-023-01978-y

Méta-analyse. Les charges lourdes améliorent l'économie de course sur la plage la plus
large (environ 8,6 à 17,9 km/h), avec un effet plus marqué aux vitesses élevées. Les
charges sous-maximales et l'isométrie ne montrent pas d'amélioration.
**Niveau : modéré.** → fonde R-REN-002

### S-REN-002 — Pliométrie aux allures basses
Même source que S-REN-001 (analyse par sous-groupes de méthodes).

La pliométrie améliore l'économie de course aux vitesses inférieures ou égales à
12 km/h, les méthodes combinées entre 10 et 14,45 km/h. C'est la plage d'allure d'un
ultra, d'où sa place dans le programme malgré un effet plus étroit que les charges lourdes.
**Niveau : modéré.** → fonde R-REN-002

### S-REN-003 — Excentrique et tolérance à la descente
**Aucune source directe identifiée à ce jour.**

Le raisonnement repose sur la spécificité : la descente sollicite le muscle en régime
excentrique, donc un entraînement excentrique devrait améliorer la tolérance à la casse
musculaire en descente. Les méta-analyses disponibles portent sur l'économie de course
en terrain plat, pas sur les dommages musculaires en descente prolongée.
**Niveau : extrapolation.** → fonde R-REN-002, avec réserve explicite

*À chercher :* essais contrôlés sur coureurs de trail, protocoles de descente répétée,
marqueurs de dommage musculaire (créatine kinase, force maximale volontaire post-effort).
Cette source a vocation à migrer en `TRA` une fois documentée.

### S-REN-004 — Bénéfice du renforcement sous fatigue
Zanini et al., *Strength Training Improves Running Economy Durability and Fatigued
High-Intensity Performance in Well-Trained Male Runners: A Randomized Control Trial.*
Medicine & Science in Sports & Exercise, 2025.

Le renforcement améliore le maintien de l'économie de course sous fatigue, plutôt que
l'économie mesurée à l'état frais. Particulièrement pertinent sur ultra, où c'est
la dégradation en fin de course qui décide du résultat.
**Niveau : faible à modéré** — essai unique, population masculine bien entraînée.

## CHA — Charge et planification

### S-CHA-001 — Charge d'entraînement par la méthode durée × RPE
Méthode dite sRPE (session RPE), introduite par Foster et collègues.
Largement utilisée et validée comme indicateur de charge interne, toutes disciplines.
**Niveau : élevé** pour l'usage comme indicateur relatif de charge.
**Réserve :** c'est une mesure de charge perçue, pas une mesure physiologique ;
elle compare des séances entre elles, elle ne mesure pas un travail absolu.
→ fonde R-REN-004

*À compléter :* référence primaire exacte (Foster et al., J Strength Cond Res, 2001)
à vérifier avant publication.

### S-CHA-002 — Interférence entre renforcement et endurance
*Effect of Strength and Endurance Training Sequence on Endurance Performance.*
PMC, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11359207/

Séparer les deux séances d'au moins 6 h réduit nettement l'interférence aiguë.
L'ordre des séances dans une même session a un effet faible sur l'endurance, plus
marqué sur les adaptations de force. Au niveau moléculaire, l'AMPK élevée après une
séance d'endurance intense met au moins 3 h à revenir à sa valeur de base.
**Niveau : modéré.** → fonde R-REN-005

**Réserve importante :** la plupart de ces travaux portent sur des populations
non spécialistes d'ultra, souvent masculines et sur des durées d'intervention courtes.
La transposition à un coureur préparant 80 km est raisonnable mais non testée.

---

## Trous identifiés

Sujets où l'app décide sans appui solide. À traiter en priorité quand on développera
le modèle allure-effort.

| Sujet | Catégorie visée | État |
|-------|-----------------|------|
| Excentrique et descente en trail | TRA | extrapolation, voir S-REN-003 |
| Progression de charge d'un bloc à l'autre | CHA | aucun critère mesuré retenu |
| Seuils d'alerte de charge aiguë / chronique | CHA | valeurs usuelles contestées |
| Adaptation du plan au sommeil et à la FC de repos | CHA | non documenté |
| Ensemble de la partie nutrition | NUT | catégorie vide |
