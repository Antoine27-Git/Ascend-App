# Audit 02 — Audit adversarial du moteur

Audit du 11/11/2026, moteur v54 (`main`). Aucune règle du moteur modifiée.

## Lectures retenues

- **Scénarios** : 3 000 tirages (`tests/audit/fuzz.js`, graine = numéro du scénario), rejoués **jour après jour** : 10 organisations de semaine (1 à 6 jours), 7 objectifs (30 à 160 km), 8 à 60 semaines, 7 types d'historique, 0 à 2 courses intermédiaires (A, B ou C), séances manquées (0 à 40 %), raison « fatigue » ou « agenda », ressenti bruité ou absent, durées faites à 60–150 % du prévu, séances décalées (D-73), courses en plus, maladie de 1 à 8 semaines. Le tout deux fois : fuseau **UTC** (pas d'heure d'été) et **Europe/Paris**.
- **Référence indépendante** : la règle des 30 jours est recalculée dans le test à partir des séances réellement faites (référence D-94 : plus longue des 30 jours, ou mémoire plafonnée ; tolérance D-96), sans passer par le moteur.
- **Invariant ≠ doctrine** : un invariant violé est un défaut. Un écart à une convention (affûtage, séances de 15 min) est signalé comme tel, pas comme un bug.
- Les cas nommés (A à M) se rejouent sur ton profil : `node tests/audit/cas.js [lettre]`. Sorties brutes dans `docs/audit/data/02-*.txt`.

## 1. Ce qui est solide

| Invariant | Résultat |
|---|---|
| Aucune exception, aucun plan refusé en cours de route | 0 sur 3 000 scénarios, deux fuseaux |
| Déterminisme (deux calculs, même plan) | 0 écart |
| Durées entières positives, une course par jour, jour de course seul, endurance ≤ 1 h 30, déroulé = durée | 0 violation sur environ 63 000 séances |
| Règle des 30 jours sur la **sortie longue lue le jour même**, hors heure d'été | **0 violation sur 26 492 sorties longues** (UTC) |
| Stabilité : la séance du jour est celle annoncée le mardi | 0 écart (UTC) |
| Parité v1 avec `sim8.py` | 0 écart sur les 5 cas de `parity.py` **et sur 60 cas tirés au hasard** (`tests/audit/parite_etendue.py`) |
| Reprise après plus de 30 jours sans course | première séance ≤ 1 h (D-94), vérifié |

Ajouté à `tools/test.py` comme garde-fou : `tests/t_invariants.js` (120 scénarios, 15 s, vert).

## 2. Cas classés par impact sur le risque de blessure

| # | Cas | Constat chiffré | Nature | Reproduire |
|---|---|---|---|---|
| **A** | **Heure d'été : le lundi, le moteur se croit la semaine d'avant** (plan démarré en hiver) | Plan lu le lundi : la semaine écoulée compte comme faite telle que prévue. **82 scénarios sur 441** lus le lundi ont au moins une sortie longue au-dessus de la règle (339 séances ; exemple +21 %, pire cas plusieurs fois la référence). Avec un jour de course le lundi : 168 scénarios sur 568 voient une autre séance le lundi que le mardi. Plan lu le jour même : 18 scénarios gardent une sortie longue au-dessus de la règle (jusqu'à +39 %). **0 cas en UTC.** | **Défaut** (`todayW`, `runsW` : `Math.floor` sur un écart de dates à cheval sur le changement d'heure) | `t_audit_heure_ete.js` ; `fuzz.js 1 1 101` |
| **M** | **Reprise après maladie : pas de mode reprise** | 3 semaines sans courir à partir de S33 : la semaine de retour prescrit **une séance de qualité de 1 h 30 le mercredi et 3 h 20 le dimanche**. La règle des 30 jours est respectée à la lettre (3 h faites 28 jours avant). Le moteur ne distingue pas maladie et agenda. | Convention manquante (S-BLE-003 : fréquence avant intensité, durée avant vitesse) | `cas.js M` |
| **I** | **Dépassement suivi** | 2 h prévues, 3 h faites (+50 %, catégorie « pic modéré », HR 1,52) : la semaine suivante le moteur prescrit **3 h**, sans signal ni message. Le dépassement devient le nouveau niveau. | Choix de conception à revoir | `cas.js I` |
| **F** | **D-96 met la sortie longue dans la catégorie « +10 à +30 % »** | Sur les plans tirés au hasard : **10,4 %** des sorties longues prescrites dépassent +10 % de la plus longue des 30 jours, contre **0,8 %** sans D-96. Sur ton plan : 6 sorties sur 44, dépassement maximal +11,8 % (1 h 16 → 1 h 25). | Convention (H-58), voir § 4 | `cas.js F` ; `ARRONDI=0 fuzz.js` |
| **E** | **L'affûtage n'allège pas (2 jours)** | S42 à S46 : 4 h 30, 4 h 30, 4 h 30, 4 h 35, 4 h 20. **3 h 20 à J−6, 1 h 25 à J−3.** La « phase de pic » est à 3 h de sortie longue ; les sorties clés sont 7, 9 et 11 semaines avant la course. | Écart à S-COU-006 (volume réduit de 41 à 60 % sur environ 2 semaines) | `cas.js E` |
| — | Semaine en cours supposée faite comme prévue | Une endurance raccourcie le mardi n'abaisse pas la limite du jeudi : 7 scénarios sur 3 000, dépassement maximal +28 % (séances ≤ 1 h 30). | Défaut mineur | `fuzz.js 1 1 409` (UTC) |
| — | Séances prescrites au-delà de +30 % du réel | 2,0 % des sorties longues (plancher de 30 min, mémoire d'1 h après coupure, historique déclaré non vérifié). | Voulu (D-94, H-21, H-48) : à savoir, pas à corriger | `fuzz.js` |
| **K** | Import montre : type par défaut | Une sortie longue de moins de 1 h 30 arrive typée « endurance » (niveau non retenu, son ressenti pollue le signal de fatigue) ; une randonnée ou une marche arrive typée course. Tu valides chaque ajout, donc risque faible si tu corriges le type. | Défaut de valeur par défaut | `cas.js K` |

## 3. Cas classés par impact sur l'atteinte de l'objectif

| # | Cas | Constat chiffré | Nature | Reproduire |
|---|---|---|---|---|
| **J** | **Le signal de fatigue tient sur un entier par semaine** | À 2 jours, une seule endurance notée par semaine. Ressenti de 3/10 ± 1 tiré au hasard, **aucune fatigue réelle, aucune séance manquée** : la sortie de 5 h n'est atteinte que dans **67 %** des cas (100 % sans bruit) et tu n'es prêt pour le 50 km que dans 59 %. Avec 25 % de semaines perturbées : 33 % (75 % sans bruit). Un seul « 4 » gèle la sortie longue une semaine ; un « 5 », deux semaines, volume −8 %. À l'inverse, **un ressenti toujours à 7/10 ne déclenche rien** (le signal est relatif aux 4 premières séances). | **Fausse précision** (H-46, H-47 ; l'échelle RPE → dérive, H-38, est introuvable dans `docs/`) | `cas.js J` ; `sim_adherence.js … BRUIT` |
| **B** | **Séance fantôme : une sortie longue manquée compte comme faite si une autre course a eu lieu dans la semaine** | Sortie clé manquée mais endurance faite : la clé est consommée (2 sorties de 4 h 30 ou plus au lieu de 3, plafond 5 h 30 au lieu de 6 h). Sortie de 3 h 50 manquée mais endurance faite : la semaine suivante propose 2 h 20 (alternance) au lieu de la retenter. Faire son mercredi **pénalise**. | **Défaut** (`clesFaites`, `lrPrec` lisent le prévu d'une semaine passée) | `cas.js B`, `B2` |
| **C** | **La course en fenêtre masque le besoin de monter** | Coupure de 4 semaines en novembre, tout le reste parfait : après le 50 km, la sortie longue reste à 3 h 10 pendant 30 jours (la course de 8 h est « la plus longue du mois »), puis manque de temps : **4 h 35 au lieu de 6 h, sans alerte d'écart**. | **Défaut** (`doitMonter` lit la fenêtre, pas le niveau) | `cas.js C` |
| **G** | **Effet de seuil à 8 h** | Sortie de référence de 1 h 47 → 50 km estimé à 8 h 06 → 3 semaines d'affûtage + 3 de récupération. À 1 h 45 → 7 h 57 → 2 + 2. **Deux minutes sur une sortie d'entraînement déplacent 2 semaines de plan**, pour une estimation à ± 15 % (H-52). | Fausse précision (seuil net sur une estimation floue) | `cas.js G` |
| **H** | **Monotonie de D-94 non tenue pour l'historique déclaré** | Une seule course réelle dans les 35 jours avant le départ annule toute la déclaration « n sorties par semaine » : endurance 90 → 30 min ; sans « dernière longue » déclarée, sortie longue 120 → 30 min. **113 états sur 3 000.** D-94 a supprimé cet effet de seuil pour la sortie déclarée, pas pour la fréquence déclarée. | **Défaut** (reste de l'ancien comportement) | `cas.js H` |
| — | Alerte d'écart muette entre 90 et 100 % | 4 h 35 pour 5 h visées : aucune alerte (seuil H-45 à 90 %). | Convention à réexaminer | `cas.js C` |
| **D** | `isRun` des tests ≠ `isRun` de l'appli | Les tests excluent le type « course », l'appli l'inclut. Aucun test ne rejoue une course : le comportement après une course réelle n'est couvert par rien. | Trou de test | — |
| — | Séances de moins de 20 min | 38 % des profils tirés ont des endurances de moins de 20 min en affûtage (14 à 19 min observées) : le plancher de 30 min (D-65b) n'y est pas tenu. | Convention à trancher | `fuzz.js` |
| — | Séance décalée (D-73) | La limite est calculée au jour d'origine : écart ≤ 1 minute. | Négligeable | `fuzz.js 1 1 615` (ARRONDI=0, UTC) |

## 4. Effets de cumul (D-94, D-96)

- **D-96, par séance** : le dépassement théorique va jusqu'à +19,8 % ; observé sur ton plan, +11,8 % au plus, sur 6 sorties. Rapporté à Frandsen 2025 : ces séances changent de **catégorie** (≤ 10 % → 10–30 %, HR 1,64 pour la catégorie entière). L'étude ne dit pas que +11 % vaut +29 % ; elle ne dit pas non plus que +11 % est sans risque, et ses auteurs écrivent qu'une hausse de 1 à 10 % porte déjà un risque. **H-58 (« pas de risque notable ») n'est pas réfutée, mais elle n'a aucun appui** : c'est un pari, de petite taille sur ton plan.
- **D-96, cumulé** : ce n'est pas un arrondi d'affichage. Il avance la sortie de 2 h d'une semaine (SPEC) et vaut **+9 points** de réussite à 25 % de semaines perturbées, **+14** à 40 % (audit 01).
- **D-94** : la référence est monotone pour les séances réelles d'avant plan, à 1 état près sur 3 000 (−6 %). Elle ne l'est pas pour l'historique déclaré (cas H) ni quand une course ajoutée transforme une semaine « arrêt » en semaine normale (11 états sur 3 000 : c'est le cas B vu sous un autre angle).

## 5. Corrections chiffrées (sur une copie du moteur, `tests/audit/corrections.js`)

Deux corrections de logique, sans toucher à une règle d'entraînement : **P-08** (une sortie longue non faite ne compte ni comme clé faite ni comme « longue la semaine d'avant ») et **P-09** (le besoin de monter se juge sur le niveau atteint, pas sur une course dans la fenêtre). À adhérence parfaite, le plan est identique.

| Semaines perturbées | Aujourd'hui | P-08 | P-08 + P-09 | + sortie longue protégée |
|---|---|---|---|---|
| 10 % | 94 % | 99 % | 99 % | 100 % |
| 25 % | 75 % | 82 % | **88 %** | 96 % |
| 40 % | 36 % | 48 % | **63 %** | 85 % |
| 25 % en grappes | 49 % | — | 74 % | — |
| 40 % en grappes | 25 % | — | 56 % | — |

(sortie clé d'au moins 5 h, 400 tirages, ± 5 points.) **Une bonne part de la fragilité mesurée dans l'audit 01 vient de ces deux défauts, pas de la physiologie.** Réserve sur P-09 telle que testée : 4 semaines après le 50 km, elle laisse la sortie longue remonter d'un coup jusqu'à la cible (la course de 8 h est dans la fenêtre). À borner avant de coder (par exemple +10 % par sortie au-dessus du niveau d'avant course).

## 6. Fausses précisions du moteur (principe Lacroix)

1. **Ressenti** : un écart de 1 point sur une seule séance décide de 1 à 2 semaines de progression (cas J). Le bruit normal d'une note sur 10 est de cet ordre.
2. **Seuils nets sur des estimations floues** : 8 h (cas G), 90 % (alerte d'écart), 3 h (alternance), 50 min (arrondi), 35 jours (cas H).
3. **Projection à 10 mois à 5 minutes près** : « 5 h le 11/07 » suppose 0 séance manquée et un ressenti constant.
4. **Durées estimées** : 15 h 05 et 8 h 06 affichées à la minute, extrapolées d'une sortie de 12 km.
5. **Minute près** : 1 h 23 contre 1 h 25 a occupé deux décisions (D-95, D-96) ; l'effet réel de D-96 est ailleurs (cumul).

## 7. Propositions (brouillons, `docs/audit/propositions.md`)

| # | Proposition | Priorité |
|---|---|---|
| P-07 | Numéro de semaine par le lundi de la date (`Math.round`), pour `todayW` et `runsW` | **1** — défaut de sécurité, correction de 2 lignes |
| P-08 | Séance fantôme : lire le réel pour les semaines passées | **1** |
| P-09 | Besoin de monter jugé sur le niveau atteint, avec borne | 2 |
| P-10 | Signal de fatigue robuste : au moins 2 notes concordantes, ou une note + une séance manquée pour fatigue ; plancher absolu (≥ 6/10 sur une endurance) | **1** |
| P-11 | Mode reprise après 2 semaines sans course ou un jour marqué « malade » : première semaine sans qualité, sortie longue ≤ 70 % de la limite | 2 |
| P-12 | Dépassement : après une séance au-delà de +30 % du prévu et de la règle, la suivante revient au prévu, avec un message | 2 |
| P-13 | Affûtage : volume des 2 dernières semaines réduit par rapport aux 3 précédentes, dernière sortie longue ≤ 2 h à J−6, rien de plus de 45 min après J−4 | 2 (convention à valider) |
| P-14 | Historique déclaré : garder la déclaration quand peu de courses réelles (prolonger D-94) | 3 |
| P-15 | Zone tampon autour des seuils (8 h : interpoler 2 + 2 ↔ 3 + 3 ; écart : signaler dès 95 %) | 3 |
| P-16 | Tests : `isRun` commun avec l'appli, un test qui rejoue une course réelle, `t_audit_heure_ete.js` dans `tools/test.py` une fois P-07 codée | 2 |

## Sources

- Frandsen et coll., BJSM 2025 (S-BLE-004), catégories et rapports de risque : https://pmc.ncbi.nlm.nih.gov/articles/PMC12421110 ; billet des auteurs (hausse de 1 à 10 %) : https://blogs.bmj.com/bjsm/?p=11751 — consultés le 11/11/2026.
- Affûtage : Bosquet et coll. 2007 (S-COU-006, `docs/SOURCES.md`). Reprise : S-BLE-003 (niveau faible, consensus clinique).
- Bruit d'une note de ressenti de ± 1 point : **non vérifié** (ordre de grandeur usuel, à sourcer dans l'audit 05).
- Données : `docs/audit/data/02-fuzz-utc.txt`, `02-fuzz-paris.txt`, `02-fuzz-utc-sans-d96.txt`, `02-cas.txt`, `02-corrections-bruit.json`.
