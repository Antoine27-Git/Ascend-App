# Audit 01 — Faisabilité sous adhérence réelle (pré-mortem chiffré)

Audit du 11/11/2026, moteur v54 (`main` après fusion de la PR #21). Aucune règle du moteur modifiée.

## Lectures retenues (tu n'étais pas là pour trancher)

- **Profil simulé** : le tien au 10/11 (`tests/ui/state.py`, plan redémarré le 02/11, sortie longue de 1 h 16 faite le 08/11, 80 km / 4 500 m D+ le 25/09/2027, 50 km le 08/05/2027 en priorité B), en **2 jours stricts** (mercredi + dimanche). Variantes : passage à 3 jours enchaînés dès F3, sans 50 km, 50 km en priorité C.
- **Semaine perturbée** : une fois sur deux une seule sortie perdue (au hasard), une fois sur deux les deux. Raison « agenda » (pas un signal de fatigue, D-72). Ressenti constant à 3/10. Les courses sont courues.
- **Cible** : celle du moteur, une sortie clé d'au moins **5 h** dans le bloc spécifique (`cible` 300 à 360 min). C'est une **convention** (H-06), pas un seuil scientifique : je donne donc aussi 4 h 30 et 4 h.
- **Lecture du plan** : le mardi de chaque semaine (même résultat que le jour de la séance). Pas le lundi : voir le défaut d'heure d'été, § 5.
- 400 tirages par scénario, graine fixe : chaque pourcentage est juste à **± 5 points**. Les scénarios sont simulés, pas observés : aucun rétro-test possible.

## 1. Résultat principal

| Semaines perturbées | Sorties longues tenues | Sortie ≥ 5 h | ≥ 4 h 30 | ≥ 4 h | 3 sorties clés | Prêt pour le 50 km | Plus longue sortie du bloc (P10 / médiane / P90) | Au moins un effondrement |
|---|---|---|---|---|---|---|---|---|
| 0 % | 100 % | **100 %** | 100 % | 100 % | 100 % | 100 % | 6 h 00 / 6 h 00 / 6 h 00 | 0 % |
| 10 % | 93 % | **94 %** | 96 % | 99 % | 89 % | 98 % | 5 h 30 / 6 h 00 / 6 h 00 | 9 % |
| 25 % | 82 % | **75 %** | 82 % | 88 % | 56 % | 84 % | 3 h 50 / 5 h 30 / 6 h 00 | 32 % |
| 40 % | 70 % | **36 %** | 50 % | 62 % | 20 % | 49 % | 2 h 35 / 4 h 35 / 6 h 00 | 62 % |
| 10 % en grappes de 3 semaines | 93 % | **78 %** | 85 % | 90 % | 71 % | 88 % | 4 h 00 / 6 h 00 / 6 h 00 | 29 % |
| 25 % en grappes | 81 % | **49 %** | 62 % | 71 % | 37 % | 64 % | 2 h 35 / 4 h 35 / 6 h 00 | 60 % |
| 40 % en grappes | 70 % | **25 %** | 34 % | 47 % | 14 % | 41 % | 1 h 40 / 3 h 50 / 5 h 30 | 78 % |

« Prêt pour le 50 km » = sortie longue d'au moins 3 h 39 (90 % de la cible du moteur, 4 h 03) deux semaines avant. « Effondrement » = un dimanche où la fenêtre des 30 jours ne porte plus 80 % du niveau atteint. D+ : il suit la durée (le moteur le déduit d'elle) ; une sortie d'au moins 1 350 m est tenue dans 96 / 83 / 51 % des cas à 10 / 25 / 40 %.

**Lecture.** À 10 % de semaines perdues, le plan tient. À 25 %, une fois sur quatre tu n'as pas ta sortie de 5 h. À 40 %, deux fois sur trois. Et les mêmes semaines perdues **groupées** (un mois de boulot, une maladie) coûtent 16 à 26 points de plus que dispersées.

**Je te challenge.** Ta seule donnée réelle est pire que mon pire scénario : septembre et octobre 2026, environ 8 semaines sur 9 sans courir, d'un seul bloc. Les scénarios à 10 et 25 % sont donc des hypothèses optimistes pour toi tant que tu n'as pas tenu 8 semaines d'affilée. Le plan affiché dans l'appli, lui, suppose 0 % : « 5 h le 11/07/2027 » est le meilleur cas, pas une prévision.

## 2. Retard typique et effondrements

- **Retard** : quand la sortie de 5 h est atteinte, c'est le 11/07 (date prévue) en médiane et avant le 08/08 dans 9 cas sur 10 à 25 % ; le 25/07 en médiane et avant le 22/08 à 40 %. Le retard n'est pas le problème : c'est **tout ou rien**. À 25 %, 25 % des trajectoires n'y arrivent jamais ; à 40 %, 64 %.
- **Ce qui compte, c'est la fin** : à 25 %, avec 0 à 2 sorties longues perdues entre mi-mai et début septembre (S31 à S44), la cible tient dans 85 à 87 % des cas ; avec 3 ou plus, 63 %. À 40 % : 31 % dès 3 pertes.
- **Une seule coupure totale** (`sim_coupure.js`, tout le reste parfait) :

| Coupure | 5 h manquées si elle commence en | Cible du 50 km manquée |
|---|---|---|
| 2 semaines | S30, S34 | jamais |
| 3 semaines | S10, S14–S16, S29–S30, S32–S34, S36 | S6, S10, S14–S18 |
| 4 semaines | S3–S16 (début entre le 16/11 et le 15/02), S28–S36 (début entre le 10/05 et le 05/07) | S2–S18 |
| 6 semaines | S2–S16, S26–S36 | S2–S18 |
| 8 semaines | S2–S16, S24–S36 | S2–S18 |

Deux zones rouges : **novembre à février** (la rampe vers le 50 km) et **mi-mai à mi-juillet** (la rampe vers les sorties clés). De fin février à avril, une coupure passe… parce que le 50 km couru sert ensuite de référence des 30 jours (8 h de course autorisent tout) : c'est un artefact, pas une bonne nouvelle (§ 5, cas C).

- **Mécanique de l'effondrement** (à 25 %, médiane de 65 min de niveau perdues) : au-delà de 3 h, le moteur n'envoie une sortie « au niveau » qu'une semaine sur deux (D-22a, convention H-27), plus une semaine allégée sur quatre. Il suffit de **deux sorties au niveau perdues de suite** pour que la dernière sorte de la fenêtre des 30 jours : tu repars de 3 h 20 (1,1 × 3 h), puis +10 % toutes les deux semaines, soit environ 10 semaines pour revenir à 5 h. Après plus de 30 jours sans rien de long, la mémoire de D-94 te ramène à 1 h.

## 3. Sensibilité aux règles et aux leviers

| Scénario (25 % puis 40 % de semaines perturbées) | Sortie ≥ 5 h à 25 % | à 40 % |
|---|---|---|
| Référence | 75 % | 36 % |
| **Sortie longue protégée** : quand une seule sortie saute, c'est l'endurance | **94 %** | **81 %** |
| Repli de 45 min à la place d'une sortie longue perdue | 75 % | 31 % |
| Repli de 90 min | 78 % | 36 % |
| Sortie longue protégée + repli de 90 min | 90 % | 68 % |
| Course décalée de +4 / +8 / +12 semaines | 82 / 78 / 80 % | 47 / 46 / 46 % |
| Sans D-96 (arrondi à la minute inférieure) | 66 % | 22 % |
| Mémoire de D-94 plafonnée à 2 h au lieu d'1 h | 76 % | 38 % |
| Mémoire de D-94 sans plafond | 97 % | 91 % |
| Mercredi tenu à 60 min au lieu des 90 prescrites | 75 % | 36 % |
| 3 jours enchaînés dès F3 | 79 % | 41 % |
| Sans le 50 km | 71 % | 31 % |
| 50 km en priorité C (course-entraînement) | **12 %** | **2 %** |

Six constats.

1. **Le seul levier puissant à ta main : protéger la sortie longue.** +19 points à 25 %, +45 à 40 %. Le mercredi ne compte pas pour cette cible : le tenir à 60 min au lieu de 90 ne change rien (75 % contre 75 %).
2. **Décaler la course ne règle pas l'irrégularité.** +3 à +11 points seulement, et plafond vers 80 % (à 25 %) quel que soit le décalage. Le moteur monte « juste à temps » (D-63d) : plus de calendrier ne donne pas plus de marge, seulement plus de semaines où décrocher. Une « date réaliste » seule serait donc une fausse promesse (§ 4, P-01).
3. **La séance de repli ne sauve pas la progression**, et elle peut coûter : une semaine avec une seule petite sortie n'est plus une semaine « arrêt », donc le moteur **consomme la sortie clé non faite** (3 clés : 56 % → 40 %). Défaut du moteur, pas du repli (§ 5, cas B). Le repli garde un intérêt pour l'habitude (audit 05), pas pour la cible.
4. **D-96 pèse lourd** : +9 points à 25 %, +14 à 40 %. Ce n'est pas un détail d'affichage, c'est un accélérateur de reconstruction. Son coût en risque est traité dans l'audit 02 (les sorties ainsi arrondies tombent dans la catégorie « +10 à +30 % » de Frandsen 2025, HR 1,64).
5. **Le plafond d'1 h de la mémoire (D-94) est ce qui rend une coupure si chère** : sans lui, 97 % et 91 %. Mais le lever contredit la seule preuve du projet : reprendre à 4 h après un mois à 1 h 30, c'est un pic de plus de 100 % au sens de Frandsen (HR 2,28). Je ne propose pas de le lever. Je propose d'éviter de vider la fenêtre (constat 1).
6. **Le 50 km en priorité C est un piège.** Le moteur ne prépare pas une course-entraînement : plus longue sortie avant un 50 km de 8 h = 3 h 10 ; la rampe vers l'objectif principal devient tardive (12 % à 25 %). Garde-le en B, ou renonce-y. « Sans 50 km » est aussi moins robuste (71 %) : sans jalon, le moteur te laisse à 1 h 15 de sortie longue jusqu'à fin janvier puis monte juste à temps.

### D-71 (temps disponible ignoré) : réexamen

Motif de D-71 (SPEC, 28/09/2026) : simplifier, l'endurance est plafonnée à 1 h 30 et la sortie longue suit sa progression ; conséquence assumée, « un coureur ne peut plus dire qu'il n'a que 60 min ». Mesure : sur ton plan, le moteur prescrit **plus de 60 min 34 mercredis sur 47** (dont 22 à 90 min, à partir du 06/01/2027 ; 13 h au total au-delà de 60 min), alors que tu as déclaré 60 min maximum ce jour-là (27/09). Effet sur la cible : nul. Effet réel : 34 mercredis « raccourcis » par construction, donc un plan que tu ne tiens jamais entièrement. Pour quelqu'un dont le point faible déclaré est la régularité, c'est un mauvais signal fabriqué par l'appli. Proposition P-06 : rétablir un plafond par jour, **en affichage et en prescription de l'endurance seulement**, sans effet sur la sortie longue.

## 4. L'objectif et sa date tiennent-ils ?

- **Sur le papier, oui** : 3 sorties clés de 5 h, 5 h 30, 6 h en juillet–août, 50 km préparé (4 h 35 le 18/04).
- **Avec ton historique, non démontré.** Il faut tenir environ 8 sorties longues sur 10, et surtout ne pas perdre deux sorties « au niveau » de suite entre mi-mai et mi-juillet. C'est la période des ponts, des fins d'année scolaire et du début des vacances.
- **Fausses précisions à corriger** : (a) la date « 5 h le 11/07 » affichée à 10 mois ; (b) la durée de course estimée, 15 h 05, extrapolée d'une sortie d'entraînement de 12 km (rapport de 7 en km-effort ; fourchette H-52 : environ ± 19 %, soit 12 h à 18 h) ; (c) la durée du 50 km, 8 h 06 : à 6 minutes près il passe de la tranche 4–8 h (2 semaines d'affûtage, 2 de récupération) à 8–20 h (3 + 3), soit 2 semaines de construction en moins sur une estimation à ± 15 % (audit 02).
- **Alternatives, de la moins à la plus coûteuse** :
  1. Garder date et course, mais piloter sur une **fourchette** (sortie la plus longue de 4 h 30 à 6 h) et sur la régularité des sorties longues, pas sur une date.
  2. Faire du **50 km du 08/05 un point de décision** : si tu n'as pas tenu une sortie d'environ 3 h 30 deux semaines avant, ou si la course se passe mal, le 80 km de septembre devient un 50–60 km d'automne, et le 80 km passe au printemps 2028. À 25 % de semaines perturbées, tu es prêt pour le 50 km dans 84 % des cas ; à 40 %, une fois sur deux.
  3. Décaler le 80 km de 4 à 8 semaines : gain faible (constat 2). À ne faire que pour une raison de calendrier, pas pour « rattraper ».

## 5. Défauts du moteur rencontrés en route (détaillés dans l'audit 02)

- **A. Heure d'été** : pour un plan démarré en hiver, tout lundi d'heure d'été est compté dans la semaine précédente (`todayW`, `runsW` en `Math.floor`). Le lundi, la semaine écoulée n'est pas « passée ». Reproduit par `tests/audit/t_audit_heure_ete.js` (rouge attendu). Si le plan est lu le lundi, la probabilité de 5 h tombe de 75 à 66 % (25 %) et de 36 à 26 % (40 %) dans ma première série.
- **B. Sortie clé consommée sans être faite** : une semaine clé où seule l'endurance est courue compte comme clé faite.
- **C. La course en fenêtre masque le besoin de monter** : pendant 30 jours après le 50 km, `doitMonter` voit 8 h dans la fenêtre et conclut que le niveau est atteint ; la sortie longue reste à son niveau d'avant course alors que la règle des 30 jours autoriserait la montée. Exemple : coupure de 4 semaines en novembre → sortie clé finale de 4 h 35 au lieu de 6 h, **sans alerte d'écart** (4 h 35 ≥ 90 % de 5 h).
- **D. `isRun` des tests ≠ `isRun` de l'appli** : les tests excluent le type « course », l'appli l'inclut. Sans effet aujourd'hui (aucun test ne rejoue une course), mais un test futur donnerait un autre plan que l'appli.

## 6. Propositions (spec seulement, brouillons dans `docs/audit/propositions.md`)

| # | Proposition | Chiffre à l'appui |
|---|---|---|
| P-01 | « Niveau probable à la date » à côté de la date voulue (fourchette P10–P90 selon tes sorties longues tenues sur 8 semaines), et « date réaliste » seulement si elle existe | à 82 % de sorties longues tenues : 3 h 50 à 6 h ; décaler la date plafonne à 80 % |
| P-02 | Mode « semaine chargée » : on garde la sortie longue, déplaçable (D-73), le reste saute sans compter comme manque | 75 → 94 %, 36 → 81 % |
| P-03 | Séance de repli : 30 à 45 min dont un passage soutenu, pour l'habitude ; ne consomme ni clé ni semaine allégée | repli seul : 0 à −5 points sur la cible tant que le défaut B existe |
| P-04 | Rattrapage : jamais de séance doublée ; une sortie longue manquée se refait au même niveau la semaine suivante | déjà le comportement de la sortie longue (niveau tenu) ; à écrire |
| P-05 | Alerte « fenêtre » : prévenir **avant** que la dernière sortie au niveau sorte des 30 jours | 32 % des trajectoires à 25 % ont un effondrement |
| P-06 | Plafond par jour pour l'endurance (réexamen de D-71), sans effet sur la sortie longue | effet nul sur la cible, 34 mercredis concernés |

Ce que je ne propose pas : lever le plafond d'1 h de D-94 (constat 5), ni une date réaliste seule (constat 2).

## Sources

- Frandsen et coll., BJSM 2025 (S-BLE-004) : https://pmc.ncbi.nlm.nih.gov/articles/PMC12421110 — catégories et rapports de risque relus le 11/11/2026 (≤ 10 % référence ; > 10–30 % : 1,64 ; > 30–100 % : 1,52 ; > 100 % : 2,28), en **distance**, sur route.
- Règles et conventions du moteur : `docs/SPEC.md` D-63d, D-67, D-71, D-94, D-96 ; `docs/HYPOTHESES.md` H-06, H-26, H-27, H-40, H-52, H-58.
- Données : `docs/audit/data/01-adherence.json` (85 scénarios), scripts dans `tests/audit/`.
