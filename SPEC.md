# SPEC.md — Grandeurs du modèle allure-effort — Ascend

Registre des grandeurs qui composent le modèle. Une grandeur n'est admise que si les
quatre cases sont remplies : ce qu'elle prédit, sa valeur initiale et son origine,
l'observation qui la corrige, le volume de données à partir duquel elle devient fiable.
Tant qu'une case reste vide, la grandeur reste **en discussion** — elle ne rentre pas
dans le modèle. On ne réécrit pas l'historique : une décision abandonnée passe en
`[abandonnée]` avec la date et le motif, elle ne disparaît pas — et garde son
identifiant, jamais réattribué.

## Format des identifiants

`G-CAT-nnn`, même logique que `R-CAT-nnn` (REGLES.md) et `S-CAT-nnn` (SOURCES.md) :
numérotation qui repart de 001 dans chaque catégorie.
Les décisions de cadrage sont numérotées `D-nn`, séquence unique, par ordre de décision.

| Code | Catégorie |
|------|-----------|
| CAP | Capacité de référence (VC et dérivés) |
| TER | Terrain — coût pente/descente |
| FAT | Fatigue et durabilité intra- et inter-séance |
| RES | Ressenti (RPE) |
| CHG | Charge extra-course (renforcement, autre sport) |
| PLA | Planification — volumes, sortie longue, relâche |
| NUT | Nutrition — apport glucidique à l'effort |
| BLE | Gêne, douleur, plafond d'impact |

Pas de catégorie pour la fiabilité de mesure : elle est un attribut porté par chaque
observation, pas une grandeur (D-11).

Quand une grandeur s'appuie sur une source, elle la cite : `→ S-CAT-nnn` (SOURCES.md).
Le niveau de preuve reprend l'échelle de SOURCES.md : `élevé` / `modéré` / `faible` /
`extrapolation`. Conformément à R-MET-001, toute affirmation non reliée à une source
porte explicitement la mention `extrapolation`.

---

## Protocole d'audit

Appliqué à chaque écriture, à trois paliers pour rester praticable :
1. **Mécanique, à chaque écriture** : références croisées (D-, G-, S-, R-, A-), séquences,
   tableaux bien formés, **et renvois périmés** — toute phrase affirmant qu'un élément du
   chantier « n'est pas traité » / « reste à traiter » est confrontée au statut réel du
   tableau. Ajouté le 17/09/2026 : cinq des six problèmes du deuxième audit complet étaient
   des renvois devenus faux parce que le reste avait avancé, et les contrôles d'alors ne
   vérifiaient que l'existence des identifiants, jamais la véracité de ce qu'on en disait.
   **Et variables d'indexation obsolètes** — toute règle décidant sur une grandeur qu'une
   décision ultérieure a remplacée (ex. tranches en km après le passage de D-44 à la durée
   d'effort). Ajouté le 17/09/2026 : D-22, D-25 et D-35 décidaient encore sur la distance
   plusieurs décisions après D-44. Automatique, quelques secondes.
2. **Local, à chaque élément** : relire les seules décisions qui touchent le même objet
   que ce qui vient d'être écrit.
3. **Complet, tous les 3 à 4 éléments** : les cinq passes (contradictions, conformité à
   l'architecture, chaînes complètes des grandeurs, entrées manquantes, niveaux de
   preuve) — seul palier capable d'attraper une contradiction entre deux décisions
   écrites à plusieurs tours d'écart. Premier audit complet : 17/09/2026.

Limite assumée : une erreur commise à l'écriture et reproduite au contrôle ne sera pas
attrapée. Les audits sont un plancher, pas une preuve d'absence d'erreur.

---

## Décisions de cadrage

Pas des grandeurs — des prérequis qui conditionnent toutes celles ci-dessous.

**D-01 — Niveau de prédiction : la séance, pas la course.** Le modèle prédit
allure/effort selon pente et fatigue à l'échelle d'une sortie. Le temps de course est
dérivé a posteriori par composition, jamais une grandeur indépendante — 3 à 5 courses
par an ne suffisent pas à calibrer directement. Cohérent avec R-ENT-001. 16/09/2026

**D-02 — Le modèle ne suppose aucun capteur au-delà d'une montre GPS.** Données
minimales supposées disponibles : allure, pente, durée. FC optique poignet et ceinture
sont des **améliorations facultatives**, jamais des prérequis — le modèle doit rester
entier sans elles (R-ENT-001). Le rôle de la FC est arbitré par D-09 à D-12.
**Reformulé le 17/09/2026** : la rédaction initiale (« pas de ceinture dans
l'immédiat ») énonçait une contrainte matérielle personnelle et datée, pas une
décision de modèle générique — incohérent avec la décision de portée du chantier.
16/09/2026

**[abandonnée] D-03 — RPE différentiel par bloc (cardio / jambes, par segment).**
Proposée puis retirée le 16/09/2026. Motif : sur une sortie longue, la saisie ne peut
être que différée, et un ressenti par segment rappelé deux heures après relève de la
reconstruction, pas du rappel — le grain recherché (discriminer montée et descente)
est précisément celui qui se perd en premier. Motif aggravant : le mode d'échec est
silencieux (une note mal remplie ressemble à une note remplie), et une donnée d'effort
fausse est pire qu'absente puisque le modèle l'absorbe comme vraie.

**[abandonnée] D-04 — RPE par bloc avec VC en repli quand non rempli.** Écartée le
16/09/2026. Motif : les données manquantes ne manquent pas au hasard (les sorties
routinières et les sorties éprouvantes seraient sous-renseignées), donc le modèle
attribuerait à la pente ou à la fatigue un écart qui vient du remplissage. Motif
second : %VC et note sur 10 ne sont pas convertibles sans un coefficient qu'on ne
pourrait calibrer que sur les séances où les deux existent — coefficient ni lisible
ni discutable, contraire à R-MET-002.

**D-05 — L'effort est calculé, pas déclaré.** L'effort d'un segment est exprimé en
% de la vitesse critique personnelle (G-CAP-001), calculé depuis le GPS. Le ressenti
ne produit **aucun coefficient de terrain ni de fatigue** (G-TER-001, G-FAT-001).
**Corrigé le 17/09/2026** — la formulation initiale (« aucun coefficient du modèle »)
était fausse : le ressenti corrige bien G-PLA-002 via la dérive
ressenti/calculé (G-RES-001b). La restriction porte sur les coefficients terrain et
fatigue, pas sur la planification. 16/09/2026

**[absorbée] D-06 — Un ressenti obligatoire par séance, global.** Absorbée par
G-RES-001 le 20/09/2026 (ALLEGEMENT.md A5) : elle n'était citée nulle part ailleurs et
redisait moins précisément ce que la grandeur décrit. Identifiant conservé.
 Une note par séance, à la fin.
Elle entre dans le modèle (G-RES-001), avec des rôles définis — mais pas comme source
de calibration des coefficients terrain/fatigue. 16/09/2026

**D-07 — Deux engagements de protocole côté coureur.** (a) Un effort proche du
maximal sur 3 à 12 min toutes les quelques semaines, sans quoi la VC est sous-estimée
et tous les %VC dérivent ; (b) une technicité déclarée une fois par parcours, pas par
sortie. 16/09/2026

**D-08 — La capacité de référence est par activité, pas par coureur.** Une VC course.
Une puissance critique vélo seulement si capteur de puissance. Aucune passerelle entre
les deux : la relation est individuelle et ne se déduit pas. Ce qui circule entre
activités, c'est le sRPE (G-CHG-001). 16/09/2026

**D-09 — Double usage de la FC : affichage libre, observation filtrée.** La FC est
affichée sans restriction pendant et après la séance (zones, endurance fondamentale,
suivi personnel) — en course régulière l'erreur de l'optique poignet est faible
→ S-MES-001. Elle n'entre comme observation du modèle que sur les segments admissibles
(D-10), parce que le découplage FC/allure cherche une dérive de quelques pourcents,
inférieure à l'erreur du capteur en conditions dégradées → S-MES-002. 16/09/2026

**D-10 — L'admissibilité d'une observation FC se juge au segment, pas à la séance,
et se déduit du signal.** Un segment est admissible si le mouvement y est régulier :
cadence stable, allure stable, pente modérée, pas de marche. Tout est déductible du
fichier GPS — aucune déclaration demandée au coureur. Motif du rejet d'un drapeau
déclaratif au niveau séance (ex. « bâtons oui/non ») : mauvais grain (dix minutes
dégraderaient trois heures de données, ou l'inverse), et les bâtons ne sont pas la
seule cause de dégradation → S-MES-002.

**Seuils, rapatriés ici depuis D-49b le 20/09/2026** — la régularité d'un segment était
décrite à deux endroits, ce qui est une source de divergence :

| Critère | Seuil |
|---|---|
| Durée minimale du segment | ≥ 60 s |
| Stabilité de cadence | écart-type ≤ 5 % de la moyenne du segment |
| Stabilité d'allure | écart-type ≤ 10 % de la moyenne du segment |
| Pente | dans une seule bande, et hors zone de marche (D-40) |

**Deux régimes d'application** (D-53a/H-01) : **filtre binaire** pour la FC — l'argument
est quantitatif, 13 % d'erreur du capteur contre quelques pourcents de signal recherché,
un segment non régulier y est inexploitable ; **pondération** pour le coût-pente — un
segment moyennement régulier pèse moins, il ne disparaît pas, faute de quoi les bandes
raides et techniques, les plus irrégulières, ne seraient **jamais** calibrées (mesuré :
confiance nulle sur la descente forte après un an de trail).

**Niveau : extrapolation** — les quatre critères et leurs seuils sont posés par nous.
**À éprouver en priorité** : trop stricts, presque aucun segment n'est admis et les
grandeurs ne convergent jamais ; trop laxistes, du bruit entre dans les coefficients.
16/09/2026

**D-11 — La qualité de mesure est un attribut de chaque observation, pas un réglage
global.** Chaque observation FC porte sa source (optique poignet / ceinture) et son
niveau de confiance. Cocher une ceinture dans le matériel élargit l'admissibilité et
relève la confiance des observations **à venir** ; les observations passées gardent la
leur. Aucune bascule rétroactive, aucun recalcul des anciennes données. Ferme la
question de la catégorie MES : pas de grandeur dédiée. 16/09/2026

**D-12 — La FC ne devient jamais la donnée primaire du modèle.** Même avec ceinture,
la référence reste le %VC (D-05) : c'est lui qui porte la prédiction d'allure, et la
FC est une seconde observation de la fatigue (G-FAT-001). Motif : aucune plateforme
d'entraînement majeure n'utilise la FC pour calculer la capacité de référence
→ S-MES-003 (veille produit, **niveau : sans objet** — observation de marché, pas une
preuve scientifique), et le
modèle doit rester fonctionnel sans ceinture pour tout coureur (R-ENT-001). Ce qu'une
ceinture change : plus de segments admissibles, confiance plus haute, convergence plus
rapide de G-FAT-001. 16/09/2026

**D-13 — La case 4 du filtre d'admission prend trois formes selon le type de
grandeur.** (a) **Convergence** — pour une grandeur à coefficient stable dans le temps :
fiable quand l'estimation cesse de se déplacer en ajoutant des observations ;
(b) **Complétude** — pour une grandeur censée évoluer (la progression est le signal) :
la convergence est inapplicable, on juge la couverture et la fraîcheur des
observations ; (c) **Validité de la mesure** — pour une grandeur sans coefficient :
conditions dans lesquelles la mesure est exploitable. Motif : le filtre initial
supposait implicitement un coefficient à calibrer, ce qui ne couvre ni les grandeurs
qui doivent bouger ni les mesures directes. **Niveau : extrapolation** — le seuil de
déplacement sous lequel une estimation est dite stable reste à fixer, sans appui
scientifique ; un seul seuil pour toutes les grandeurs (R-MET-002). 16/09/2026

**D-14 — L'historique d'entraînement est importé, sans catégorie de coureur.** Aucun
profil « débutant / expérimenté / en reprise » : ces catégories ont été proposées puis
écartées le 16/09/2026, parce qu'un même coureur peut avoir des données fraîches sur
une grandeur et périmées sur une autre. C'est la fraîcheur de chaque observation qui
décide de son poids, grandeur par grandeur (D-15), dans le prolongement de D-11.
16/09/2026

**D-15 — L'ancienneté fait baisser la confiance, jamais la valeur.** Une grandeur ne
se dégrade pas toute seule parce que le temps passe : seule une observation nouvelle la
déplace. Un coureur qui s'arrête trois mois retrouve sa valeur d'avant, assortie d'une
confiance basse et d'une fourchette large, que ses premières sorties resserrent vite.
Deux garde-fous : (a) **plancher** — une grandeur ne descend jamais d'elle-même sous
85 % du meilleur niveau atteint, seules des données réelles vont plus bas ; (b) **poids
renforcé à la reprise** — les premières observations après une coupure comptent double
jusqu'à ce que la fourchette se resserre. Motif : la capacité baisse réellement à
l'arrêt → S-COU-005, mais un ancien entraîné reste au-dessus d'un non-entraîné, et le
modèle ne doit pas le rétrograder sans preuve. **Niveau : extrapolation** pour les deux
garde-fous (valeurs posées par nous). 16/09/2026

**D-16 — Poids d'une observation selon son âge, par grandeur.**

| Grandeur | Pleine valeur | Poids divisé par deux tous les | Ignorée au-delà |
|---|---|---|---|
| G-CAP-001 vitesse de référence | ≤ 3 semaines | 6 semaines | 6 mois |
| G-TER-001 coût-pente | ≤ 2 mois | 4 mois | 12 mois |
| G-FAT-001 décroissance-fatigue | ≤ 2 mois | 4 mois | 18 mois |
| G-CHG-001 charge extra-course | ≤ 72 h | — | 7 jours |

**Articulation avec D-15 — précisée le 17/09/2026.** D-15 dit que l'ancienneté ne
change jamais la **valeur** ; D-16 retire du poids aux **observations** anciennes, ce qui
déplace bien l'estimation recalculée. Les deux se concilient ainsi : le poids décroissant
élargit la fourchette et abaisse la confiance ; la valeur centrale, elle, ne bouge que
sur observation nouvelle, et ne descend jamais seule sous le plancher de D-15 (85 % du
meilleur niveau atteint). Quand **toutes** les observations d'une grandeur sont périmées,
la grandeur conserve sa dernière valeur au plancher, avec une confiance nulle — elle ne
retombe pas sur sa valeur générique d'amorçage.

Motif du 3 semaines : la baisse de capacité s'installe dès 2 à 4 semaines d'arrêt
→ S-COU-005. Motif du coût-pente plus lent : efficacité mécanique plutôt que transport
d'oxygène — **aucune source**. **Raccourci le 17/09/2026 après passe adverse (H-04)** :
valeurs initiales 6 mois / 12 mois / 3 ans, jugées imprudentes. Mécanisme inverse tout
aussi plausible — le coût en trail dépend fortement de la capacité musculaire (tolérance
excentrique, force en montée), qui se perd vite ; pour les bandes de descente la prémisse
est peut-être retournée. Conséquence asymétrique : garder un coût-pente périmé à pleine
valeur six mois fait prescrire des allures intenables après une coupure, alors que le
coût de raccourcir est faible — la grandeur se recalibre en 3 à 8 séances (D-23).
**Niveau : extrapolation** pour toutes les valeurs. 16/09/2026

**D-17 — Quatre paramètres déclarés, pas un de plus.** (a) course cible : date,
distance, dénivelé ; (b) jours disponibles et temps par jour ; (c) volume actuel des
dernières semaines, déduit de l'historique quand il existe ; (d) autres activités :
présence, fréquence, type. Test d'admission d'un paramètre : *si je change sa valeur,
le plan de la semaine 1 change-t-il ?* Sinon il n'est pas demandé. Explicitement **non
demandés** : FC maximale (une formule d'âge ne vaut rien, l'historique la contient),
niveau auto-évalué (aucun ancrage, n'entre dans aucune grandeur), vitesse de référence
déclarée (elle se calcule).

**Amendé le 17/09/2026 — le compte était faux.** Deux paramètres déclarés
supplémentaires existent ailleurs dans SPEC et contredisaient le « pas un de plus » :
la **technicité par parcours** (D-07b) et l'**accès à un vélo ou à un bassin** (D-31).
Les deux passent le test d'admission et sont conservés. La règle exacte n'est donc pas
un plafond numérique mais le **test lui-même** : un paramètre n'est demandé que si le
changer change le plan. Liste complète à ce jour : (a) à (d) ci-dessus, (e) technicité
par parcours, (f) accès vélo/bassin. Le **terrain disponible** (élément 16 du chantier)
en ajoutera probablement un septième. 16/09/2026

**[abandonnée] D-18 — Séance test d'amorçage (effort maximal sur 1,5 km).** Proposée
puis écartée le 16/09/2026. Motif : un effort unique ne donne qu'un point, alors que la
vitesse de référence est la pente d'une relation distance-temps qui demande deux ou
trois durées différentes → S-COU-003 ; la convertir exigerait un coefficient générique,
rejeté par R-ENT-001. Motif aggravant chez un débutant : gestion d'allure maximale non
maîtrisée, départ trop rapide, valeur sous-estimée avec une apparence de mesure. À la
place : les premières semaines de course facile sont la mesure, sans prescription
d'allure et avec confiance affichée basse ; l'effort franc de D-07 suffit à amorcer plus
vite ceux qui en sont capables.

**D-19 — Garde-fou de faisabilité, en trois niveaux.** Le contrôle s'exécute **après
l'import**, quel que soit l'ordre dans lequel l'objectif et les données ont été
fournis ; sans historique il porte sur le volume déclaré (D-17c).

| Niveau | Condition | Comportement |
|---|---|---|
| Vert | durée ≥ confortable **et** volume de bloc requis ≤ 1,5 × volume actuel | plan généré |
| Orange | durée entre minimum et confortable, **ou** marge de progression faible, **ou** volume réalisable très inférieur au volume de bloc requis (D-52b), **ou** terrain insuffisant pour le D+ de la cible (D-47) | plan généré, risque nommé |
| Rouge | durée < minimum, **ou** temps de progression nécessaire > semaines disponibles (D-52a), **ou** données montrant l'absence de pratique régulière depuis 6 mois avec cible longue | refus **à la création** ; en cours de préparation, dégradation de la cible et message explicite (D-52c) |
| Orange (ajout D-64) | ressenti non saisi depuis 3 séances consécutives | garde-fou orange dédié, relance active espacée, jamais de passage au rouge sur ce seul motif |
| Orange (ajout D-65e) | sortie clé de D-22 non atteignable avec le volume réellement toléré : part des sorties clés × volume tenu (G-PLA-002) < borne basse de la sortie clé | plan généré, sortie clé atteignable affichée, sorties de D-20 proposées |

Le test porte sur le **volume du bloc spécifique et la sortie longue atteignable**, pas
sur une moyenne annuelle (D-21).

**Aucun niveau rouge ne peut être déclenché par une absence de données.** Absence de
preuve n'est pas preuve d'absence : un coureur qui n'a jamais connecté sa montre n'est
pas un coureur inactif. Ordre de repli : données importées → à défaut volume déclaré
(D-17c) → à défaut l'app **demande**, elle ne refuse pas. Un garde-fou ne se déclenche
que sur une information positive, jamais sur un vide. **Niveau : extrapolation** — le
seuil 2,5 × est le plus arbitraire des trois, calé pour que le refus reste rare.
16/09/2026

**D-20 — Un refus n'est jamais un mur.** L'app propose systématiquement :
(a) **même course, plus tard** — date minimale (orange) et date sereine (vert) ;
(b) **même date, cible réduite** — distance maximale (orange) et distance sereine
(vert) ; (c) **l'explication en clair** — volume actuel, volume requis, durée de montée
nécessaire. Motif : un refus sec pousse le coureur vers un plan trouvé ailleurs,
probablement pire. Risque assumé et non résolu : un coureur déterminé peut s'inscrire
malgré tout et s'entraîner sans rien — une option de plan de sécurité explicitement
sous-dimensionné reste à étudier. 16/09/2026

**D-21 — Durée minimale de préparation et structure de volume.**

| Durée d'effort attendue | Préparation minimale | Confortable | Repère en distance |
|---|---|---|---|
| < 2 h | 8 semaines | 12 | 10–21 km |
| 2–4 h | 16 semaines | 20 | 21–42 km |
| 4–8 h | 24 semaines | 32 | 42–60 km |
| 8–20 h | 36 semaines | 52 | 60–100 km |

**Généralisé le 17/09/2026 — étape 4 (Blocs).** La version précédente ne donnait ces
chiffres que pour 80 km : un cas, pas une règle. Structure désormais fonction de la
**distance** et de la **durée de préparation déclarée** (D-17a), sur les mêmes quatre
tranches que la durée minimale ci-dessus.

**Formule** : `fond (semaines) = durée totale − bloc spécifique − affûtage (D-25)`.
Le **pic** n'est pas une phase distincte à durée propre : ce sont les **2 à 3 dernières
semaines** du bloc spécifique, quelle que soit sa longueur — évite une table
supplémentaire à généraliser pour un gain nul, et s'articule avec les phases « début de
bloc / cœur de bloc » déjà nommées en D-22.

| Durée d'effort attendue | Bloc spécifique (semaines) | Volume fond (h/sem) | Volume bloc spécifique (h/sem) | Volume pic (h/sem) |
|---|---|---|---|---|
| < 2 h | 4–6 | 2–3 | 4–5 | 5–6 |
| 2–4 h | 6–8 | 3–4 | 5–7 | 7–8 |
| 4–8 h | 6–8 | 3–5 | 7–9 | 9–10 |
| 8–20 h | 8–10 | 3–5 | 7–9 | 9–11 |

**Réindexé sur la durée le 17/09/2026** — les deux tableaux de D-21 décidaient encore
sur la distance après D-44. Les repères en distance restent affichés dans le premier
tableau et dans D-44, comme équivalence de lecture uniquement.

**Correction du 17/09/2026 sur les ancrages** — erreur repérée : la source ne donne que
deux points réels, 50 km (6–8 semaines) et **100 miles ≈ 161 km** (8–10 semaines)
→ S-TRA-004. 50 km tombe bien dans la tranche 42–60 km — ancrage direct correct. Mais
100 miles/161 km tombe **loin au-dessus** de la tranche 60–100 km, pas dedans : l'écrire
comme un ancrage direct pour cette tranche était faux, c'était coller la valeur au
mauvais bout de l'intervalle plutôt que l'interpoler. Seule **42–60 km** a donc un
ancrage réel. La tranche **60–100 km** est **interpolée entre les deux points distants**
(50 km d'un côté, 161 km de l'autre, elle-même bien plus proche du premier) — les
valeurs ne changent pas, leur statut si : **niveau extrapolation**, pas faible-lié-à-source.
**10–21 km et 21–42 km n'ont aucune étude, mais une convergence de pratique existe
pour la première** → S-TRA-007 : plusieurs guides de coaching indépendants s'accordent
sur 8–10 semaines (coureur régulier), 12–16 (intermédiaire), 16–20 (débutant complet).
**Notre minimum actuel de 8 semaines ne couvre que le premier cas** — un débutant
complet sur cette tranche est sous-couvert par la table telle qu'écrite ; le garde-fou
(D-19) durcit déjà le niveau si l'historique manque, mais la durée minimale elle-même
devrait varier avec l'expérience déclarée, pas seulement avec la distance. **Trou
ouvert** (renvoi corrigé le 17/09/2026 : pointait à tort vers l'élément 19, qui concerne
l'affichage et non la durée de préparation). Pour 60–100 km,
Koop décrit un « minimum-maximum » (bloc de plus haut volume 6–9 semaines avant la
course) → S-TRA-008, proche de notre fenêtre de 8–10 semaines — confirme une
convergence de pratique, sans élever le niveau de preuve.

**Seule la valeur de pic est un plafond dur**, jamais franchi. Fond et bloc spécifique
sont des **repères de structure** (la forme de la progression, fond < bloc < pic) que
G-PLA-002 peut dépasser si la tolérance observée le justifie — correction du 17/09/2026 :
traiter tout comme plafond interdisait à un coureur solide de faire 6 h d'endurance en
phase de fond, absurde. Le volume réellement prescrit reste porté par G-PLA-002.
**Précisé le 22/09/2026 (D-63a, b)** : la forme fond < bloc < pic est un repère
d'amorçage, pas une consigne — le volume ne dépend pas de la phase, aucun plancher
n'est posé à l'entrée du bloc spécifique ; ce qui monte, c'est la spécificité.

> **Amendé le 28/09/2026 par D-67 et D-70.** La sortie longue n'est plus une part pilotée du volume : elle suit sa propre progression, et le volume de la semaine en est la conséquence. La part reste un repère (plancher de la place laissée aux autres séances).

**D-22 — La sortie longue s'exprime en part du volume hebdomadaire, jamais en heures
absolues.** Motif : une valeur absolue par bloc (« bloc 1 : 1h30 ») recrée un plan
générique, contraire à R-ENT-001 ; exprimée en part, elle s'adapte au coureur et à
l'avancement sans règle supplémentaire.

| Phase | Part du volume hebdomadaire |
|---|---|
| Fond | 30–35 % |
| Début de bloc | 35–40 % |
| Cœur de bloc | 40–45 % |

**Généralisé le 17/09/2026 — même défaut que D-21, resté non corrigé sur son voisin.**
La version précédente fixait « 3 sorties clés de 5–6 h » pour une préparation 80 km et
appliquait une part de 55–65 % à toutes les distances : pour un coureur de semi à
4 h/semaine, cela aurait produit une « sortie clé » de 2h20, absurde. Deux décisions
écrites depuis s'appuyaient dessus (D-25 atténuation, D-35 sorties consécutives) —
l'erreur se propageait.

**Les sorties clés sont un outil d'ultra, pas une phase universelle.** **Indexées sur la
durée d'effort attendue depuis le 17/09/2026** — propagation de D-44, qui avait changé
l'index sans que D-22 suive : deux coureurs bouclant le même 60 km en 6 h et en 12 h
recevaient les mêmes sorties clés alors que leurs préparations n'ont rien à voir.

| Durée d'effort attendue | Sorties clés | Part du volume | Durée cible |
|---|---|---|---|
| < 2 h | aucune | — | — |
| 2–4 h | aucune | — | — |
| 4–8 h | 2–3 | 50–60 % | 3h30–4h30 |
| 8–20 h | 3 | 55–65 % | 5–6 h |

Trois règles associées : (a) une sortie longue par semaine **jusqu'à environ 3 h**,
puis alternance longue / très longue — au-delà, le coût de récupération dépasse 24 h et
la répétition hebdomadaire creuse au lieu de construire ; (b) **[remplacée le 22/09/2026
par la règle des 30 jours, D-63c]** progression plafonnée à ~20 % d'une sortie longue à
la suivante — incompatible avec (a) et (c) : les semaines allégées la faisaient repartir
de bas et rendaient les sorties clés inatteignables (TESTS.md, huitième série) ; (c) les sorties clés du tableau ci-dessus,
que des courses intermédiaires peuvent compléter ou remplacer (D-25).
**Niveau : extrapolation** — parts, plafonds et durées cibles posés par nous. 16/09/2026
**Amendé le 22/09/2026 (D-63d)** : les parts par phase sont des parts par défaut ; la
sortie longue suit sa propre progression, planifiée à rebours depuis la dernière sortie
clé, et reste la plus longue séance de la semaine (part ≥ 1/n pour n séances). **Et
(D-63k1, k6)** : elle est la seule séance autorisée à battre le maximum des 30 jours ;
un niveau atteint tôt est entretenu, une semaine sur deux au-delà de 3 h.

**D-23 — Période d'observation et péremption sont deux notions distinctes.** La
péremption (D-16) dit combien de temps une observation **passée** garde du poids. La
période d'observation dit au bout de combien de temps une grandeur devient **fiable**
à partir de zéro. Les deux se confondent facilement et ne se règlent pas ensemble.

Trois principes : (a) la personnalisation est **progressive, pas un interrupteur** — dès
les premières séances le coefficient n'est plus celui de la valeur générique, c'est la
confiance haute qui met du temps, pas la personnalisation ; (b) on compte en **séances
distinctes**, jamais en segments — vingt montées dans une même sortie ne font pas vingt
observations indépendantes (même jour, même fraîcheur, même matériel, même météo) ;
(c) la personnalisation du coût-pente est **par bande de pente**, et doit être affichée
ainsi — un pourcentage global de personnalisation mentirait.

| Grandeur | Devient utile | Confiance haute | Limite structurelle |
|---|---|---|---|
| G-CAP-001 vitesse de référence | 2–3 semaines | 6 semaines | exige un effort franc (D-07) |
| G-TER-001 bandes courantes | 3–4 séances | 5–8 semaines | — |
| G-TER-001 bandes rares | — | jamais sans exposition | descente très raide, montée très forte |
| G-FAT-001 décroissance-fatigue | 4–6 sorties longues | 3–4 mois | une sortie longue par semaine au mieux |
| G-RES-001b dérive ressenti/calculé | 6–8 semaines | 3 mois | — |
| G-CHG-001 charge extra-course | 1 mois | 3–4 mois | 2–3 séances par semaine |

**Résolu le 17/09/2026 — l'état zéro donnée était un trou, pas un cas couvert.**
« Efforts relatifs » ne voulait rien dire tant qu'aucune VC n'existe : le %VC est
lui-même l'effort relatif. Ce trou ne concerne que le coureur sans historique **et** sans
encore une seule séance — avec import (D-14), la VC se calcule dès le premier jour, sans
attente. Résolution : réutilisation de G-RES-001(c), déjà prévu pour les activités sans
GPS. Tant que moins de deux efforts de durées différentes n'existent pas (minimum de
S-COU-003), les séances sont pilotées en **ressenti** (allure confortable, conversation
possible), jamais en %VC. Dès le deuxième point, une première VC apparaît — large,
confiance quasi nulle — et se resserre séance après séance. Aucune fenêtre vide, aucune
réouverture de D-18, aucune valeur générique supplémentaire inventée : même mécanisme,
second usage.

Conséquence pour l'affichage une fois la VC amorcée : tant qu'elle n'a pas atteint une
confiance haute (environ 6 semaines), l'app propose des **durées et des efforts
relatifs**, sur lesquels elle est fiable tôt, plutôt que des allures précises.
G-FAT-001 est la grandeur structurellement lente : sur une préparation courte, elle
n'atteindra jamais une confiance haute. **Niveau : extrapolation** — ces durées sont
déduites d'une fréquence d'entraînement plausible, pas de la littérature. 16/09/2026

**D-24 — Trois statuts d'objectif, déclarés par le coureur.**

| Statut | Signification | Affûtage | Effet sur le plan |
|---|---|---|---|
| **Objectif principal** | la course qui structure la préparation ; tout converge vers elle. Un seul à la fois | complet | définit l'horizon et le découpage en blocs |
| **Objectif secondaire** | course qu'on veut réussir sans sacrifier la préparation | court, 5 à 10 jours | consomme le budget de D-25, récupération réelle puis retour au bloc |
| **Course-entraînement** | aucune intention de performance | aucun | remplace une sortie longue ou une séance dure de la semaine ; coût nul pour la construction |

Le statut est **déclaré, pas déduit** : c'est une intention, aucune observation ne dira si
le coureur voulait performer ou s'entraîner. Il satisfait le test de D-17 (le changer
change le plan : un affûtage de dix jours contre zéro). Il peut être **ajouté ou modifié
en cours de programme**, ce qui déclenche un recalcul du budget de D-25. 16/09/2026

**D-25 — Le nombre d'objectifs préparés se déduit d'un budget, pas d'un compte.** Aucune
source ne dit combien de fois par an on peut s'affûter ; en revanche le coût d'un
affûtage est documenté → S-COU-006. On raisonne donc par soustraction, sur les semaines
retirées à la construction. Deux contraintes :

(a) total **affûtage + récupération des objectifs secondaires ≤ 20 %** de la durée de
préparation ;
(b) au moins **6 à 8 semaines de construction ininterrompue** entre la fin de
récupération d'un secondaire et le début de l'affûtage principal.
**Complété le 23/09/2026 (D-65a)** : (b) seule **n'interdit pas** le bloc spécifique — à
6 semaines, la récupération peut y finir (semaine 3 du bloc en 8–20 h, semaine 1 en
4–8 h). Règle désormais : affûtage, course et récupération d'un objectif secondaire se
placent **entièrement en fond**, et (b) s'applique en plus. (c) **Test d'acceptation** :
le statut d'objectif n'est accepté que si la rampe de sortie longue (D-63d), creux de
l'affûtage et de la récupération compris, atteint encore la sortie clé ; sinon l'app
propose le statut de course-entraînement ou une autre date, chiffres à l'appui (D-20).

Coût par distance — affûtage documenté (S-COU-006), récupération **extrapolée** :

**Tranches alignées le 17/09/2026 sur celles de D-21** (le tableau s'arrêtait à
« 50–60 km », incohérent avec la tranche « 60–100 km » employée partout ailleurs) :

| Durée d'effort attendue | Affûtage | Récupération | Coût total |
|---|---|---|---|
| < 2 h | 5–10 j | 3–7 j | ~1,5–2,5 semaines |
| 2–4 h | 14 j | 10–14 j | ~4 semaines |
| 4–8 h | 14 j | 14–21 j | ~5 semaines |
| 8–20 h | 14–21 j | 21–28 j | ~6 semaines |

**Indexé sur la durée depuis le 17/09/2026** — propagation de D-44, même motif que
D-22 : le coût de récupération d'une course suit son temps d'effort, pas sa distance.

Ce que la règle produit, sans qu'aucun seuil ait été posé : à 3 mois de préparation le
budget est d'environ 2,6 semaines et un secondaire en coûte 3 au minimum — donc aucun,
seule une course-entraînement reste possible ; à 4–5 mois le budget atteint ~4 semaines,
un secondaire tient ; à 9–10 mois, ~8 semaines, deux tiennent. La règle s'adapte en outre
à la **distance** de la course intermédiaire, ce que des seuils fixes ne font pas.

**Atténuation — un secondaire long peut remplacer une sortie clé.** Quand la durée d'un
objectif secondaire correspond à l'une des trois sorties clés de D-22, son coût n'est pas
intégralement retiré de la construction : il remplace du volume au lieu de s'y ajouter.
Sans cette atténuation, la règle pénaliserait l'option la plus pertinente.

**En cas de dépassement du budget, le plan ne refuse pas : il propose le statut
inférieur**, avec le chiffre à l'appui — même logique que D-20. **Niveau :
extrapolation** pour le seuil de 20 %, les 6–8 semaines et les durées de récupération.
16/09/2026 **Complété le 22/09/2026 (D-63e)** : le volume d'affûtage est fixé — 65 % puis
45 % de la médiane des 3 dernières semaines de charge, G-PLA-002 gelé.

**D-26 — La cible porte toujours une date ; ce qui change selon le mode, c'est ce qui
cède quand la réalité diverge.**

| Mode | Verrouillé | S'ajuste en cas d'écart |
|---|---|---|
| Date fixe | la date | la performance estimée (allure et temps annoncés), jamais la construction |
| Flexible (ambition) | le niveau visé | la date, repoussée jusqu'à ce que l'état de préparation soit prêt |

Dans les deux modes, **la construction n'est jamais sacrifiée** — c'est le principe
commun. En mode flexible, le modèle calcule une **date projetée** : la première date où
le garde-fou (D-19) passerait en vert. Elle sert d'horizon pour placer les blocs et se
recalcule à chaque bilan. « Prêt » n'est pas un concept nouveau : c'est D-19 lu à
l'envers. Basculer de flexible à fixe (inscription à une course) ne recalcule rien
d'autre que l'ancrage de la date. 16/09/2026

**Amendement à D-19 — le garde-fou s'exécute en continu, pas seulement à la création du
plan.** Motif : en mode date fixe, un retard qui s'accumule sans re-contrôle pousse
mécaniquement à brûler les étapes pour tenir la date. Le contrôle se rejoue à chaque
bilan (cadence à définir avec D-12 du chantier — déclenchement du recalcul). 16/09/2026

**D-27 — Le profil de la cible se construit en deux états, jamais un troisième sur des
données devinées.**

| État | Donnée | Affichage |
|---|---|---|
| GPX connu | tracé complet fourni par l'organisateur | profil exact |
| GPX inconnu | distance + D+ seuls | profil générique mixte, étiqueté « supposé », confiance basse |

**Rejeté le 16/09/2026 : un champ déclaré « nombre de montées principales » en l'absence
de GPX.** Motif : sans trace, le coureur n'a lui-même aucun moyen fiable de connaître
cette structure ; une valeur devinée crée une fausse précision qui peut spécialiser
l'entraînement dans le mauvais sens (ex. longues montées soutenues prescrites pour une
course faite de répétitions courtes). Même famille d'erreur déjà écartée ailleurs (D-03,
D-18, VC sur aqua-jogging) : une fausse précision est pire qu'une absence. Impact
mesuré de l'absence : faible à ce stade — la spécificité montée longue / montée répétée
reste couverte par un travail de dénivelé généraliste ; l'usage le plus sensible à cette
donnée (stratégie d'allure en course) relève de la composition du temps de course, hors
périmètre de ce chantier.

**État supplémentaire, mode flexible sans distance fixée (D-26) :** profil générique de
la fourchette de distance visée, confiance encore plus basse, aucune donnée
supplémentaire collectée.

**Règle D+ — la valeur affichée par l'organisateur prime sur tout recalcul.** Motif :
le D+ d'un même tracé varie couramment de 15 à 30 % selon la méthode de lissage
utilisée ; annoncer un chiffre différent de celui de l'organisateur casserait la
confiance sans gain réel. Le GPX sert à découper le profil en segments, pas à recalculer
le total quand un chiffre officiel existe. Sans chiffre officiel, une méthode de lissage
unique et documentée sera fixée — **décision d'implémentation, pas de modélisation**,
reportée au chantier technique. 16/09/2026

**D-28 — Spécificité du bloc spécifique conditionnée à la connaissance du profil,
sans alerte de rattrapage.**

- **Fond** : toujours générique — cohérent avec D-21, le fond n'a jamais eu vocation à
  être spécifique.
- **Bloc spécifique** : spécifique (répartition montées longues soutenues / répétitions
  courtes ajustée au profil réel) si le profil est **connu au moment où chaque séance est
  programmée** ; générique sinon. Bascule silencieuse dès que le profil devient connu en
  cours de bloc : les séances déjà réalisées ne sont jamais rejouées ni signalées comme un
  manque, seules les séances restantes s'orientent.
- **Aucune alerte** n'est produite si le profil reste inconnu jusqu'à la fin du bloc
  spécifique, ou devient connu trop tard pour être exploité. Un entraînement dénivelé
  générique est une préparation valide en soi, pas un déficit à combler. Motif du rejet de
  l'alerte proposée le 16/09/2026 : elle n'aurait introduit qu'un doute non actionnable à
  l'approche de l'échéance, sans aucun bénéfice — le travail déjà effectué n'est pas perdu.
- **Affichage informatif, sans mécanisme de confiance séparé** : un libéllé reflète
  l'état actif de D-27 — « entraînement dénivelé : mixte » ou « adapté à ta course ».
- **Incitation avant le bloc spécifique** : si le profil n'est pas encore connu au moment
  où le bloc spécifique doit commencer, l'app invite le coureur à charger le GPX de sa
  course, en expliquant que cela permet un entraînement sur mesure adapté à la course.
- **Différenciation produit assumée** : cette correspondance profil de course → séances de
  dénivelé est une pratique de coach qu'aucune app généraliste connue n'automatise
  → S-TRA-005, S-TRA-006. Refinement du bloc spécifique, pas un fondement : son absence ne
  casserait pas le modèle.
- **Convention de ton** : tout texte adressé au coureur dans l'app tutoie. 16/09/2026

> **Amendé le 28/09/2026 par D-66 et D-71.** Le plafond de durée de l'endurance est appliqué dans le moteur (paramètre par tranche d'objectif) ; le D+ des endurances de F1–F2 est un plafond.

**D-29 — Une séance est une combinaison d'attributs, pas un nom.** Cinq attributs, tous
déjà manipulables par le modèle : **intensité cible** (en % de G-CAP-001), **durée**
(absolue ou part du volume, D-22), **terrain** (plat, montée, descente), **coût de
récupération** (pilote le placement dans la semaine, R-REN-005) et **motif affiché**.
Règle de sélection : deux types qui ne diffèrent que par le nom sont fusionnés (fartlek
et intervalles ont les mêmes attributs — un seul type).

Les ancrages en % sont cohérents avec le reste du modèle plutôt que plaqués dessus : la
vitesse de référence se situe près du second seuil ventilatoire → S-COU-007, donc le
travail au seuil tourne autour de 100 %. **Corrigé le 17/09/2026** : cette affirmation
était à l'origine rattachée à S-MES-003, une entrée de veille produit — un ancrage
physiologique ne peut pas reposer sur une observation de marché. **Niveau : modéré**
pour l'ancrage à 100 % ; **extrapolation** pour toutes les autres bornes du tableau.

| Type | Intensité | Durée | Terrain | Coût récup |
|---|---|---|---|---|
| Endurance fondamentale | < 80 % | 40 min – 1h30 | indifférent | faible |
| Sortie longue | < 80 % | part du volume (D-22) | indifférent | moyen à élevé |
| Allure spécifique | 80–95 % | 30–90 min d'effort | selon la cible | moyen |
| Seuil | 95–105 % | 20–40 min d'effort | plat ou montée douce | moyen |
| Intervalles | > 105 % | 15–25 min d'effort | plat ou côte courte | élevé |
| Côtes longues | 90–100 % | 6–30 min par répétition | montée soutenue | moyen à élevé |
| Côtes courtes | > 105 % | 30 s – 2 min | montée raide | élevé |
| Renforcement | sans objet | 20–45 min | hors course | variable selon dominante |

**Motif affiché** : chaque séance porte un motif — *récupération*, *développement*,
*spécifique course*, *maintien*. Il ne change aucun calcul, il explique au coureur
pourquoi cette séance est là (typiquement : pourquoi elle est légère).

**Pas de type « récupération » séparé** : c'est de l'endurance fondamentale courte, placée
après une séance dure. Ce qui la distingue est une règle de **placement**, pas une
physiologie — elle se lit dans le motif.

**Endurance fondamentale : borne haute, pas fourchette.** Ce qui la définit est le
plafond à 80 %, pas un plancher — entre 60 % et 80 % la différence n'est pas
actionnable. Le risque réel est la dérive **au-dessus** du plafond : **résolu par D-34**
(cible chiffrée par phase) et surveillé par la règle d'affichage de D-34 (ex-G-PLA-003, rétrogradée le 20/09/2026).

**Route et trail : même catalogue.** L'allure spécifique est la séance centrale d'une
préparation marathon route et existe aussi en ultra, plus bas dans sa fourchette et
souvent intégrée à une sortie longue — bornée par la cible, pas par une valeur fixe. Les
côtes courtes ne sont pas une spécificité trail : elles servent de renforcement à haute
intensité même sans dénivelé en course. Une sortie longue comportant un bloc
qualitatif n'est **pas un type de plus** mais une composition d'attributs : l'élément 10
du chantier (format de prescription) doit savoir l'exprimer.

**Portions marchées — ajout du 17/09/2026.** Les intensités du tableau supposent un
%VC calculable ; sur les portions marchées en montée forte, le %VC perd son sens
physiologique (réserve de G-CAP-001, non reportée ici à l'écriture initiale). Une sortie
longue d'ultra en contient. Conséquence : la borne « < 80 % » ne s'applique qu'aux
portions courues ; les portions marchées relèvent de D-40, qui les mesure en VAM plutôt
qu'en %VC.

**Protocole du type Intervalles** → S-COU-010 : forme « pyramide » — fractions d'effort
à allure cible fixe, distance croissante puis décroissante (100 m, 200 m, 300 m… jusqu'à
un sommet propre à chaque coureur, souvent 700-800 m), récupérations passives calées sur
le temps de la fraction. Intérêt : cumuler beaucoup plus de temps aux allures élevées
qu'en continu, à fatigue ressentie égale. Vitesse cible dérivée de G-CAP-001, pas des
tables de cotation IAAF de la source (déjà remplacées par notre propre calcul).
**Règle d'introduction** : 6 semaines de montée en charge, jamais plus de 2 séances
intenses par semaine (toutes catégories confondues — recoupe R-REN-005), repos complet
la veille et le lendemain, arrêt immédiat sur douleur persistante à une articulation ou
un tendon (recoupe D-32). **Niveau : sans objet** — synthèse experte, aucune référence
primaire dans le texte, à ne pas confondre avec le modèle de répartition saisonnière du
même nom (D-34).

**Côtes longues / côtes courtes sont le levier de D-28** : le bloc spécifique dose leur
répartition quand le profil est connu, mixte sinon. Aucune règle supplémentaire.

**La descente n'est volontairement pas un type.** Aucune intensité exprimable en % de
G-CAP-001, et son coût réel est musculaire — or le coût musculaire de la descente est
hors périmètre de ce chantier. L'introduire maintenant créerait un type que le modèle ne
saurait ni doser ni espacer. Elle reste un **attribut de terrain** des sorties longues.
À rouvrir avec ce trou : manque réel en trail, pas un oubli.

**Renforcement** : présent au catalogue, mais sa progression et son placement relèvent
de l'élément 8 du chantier. **Niveau : extrapolation** pour toutes les bornes de durée
et de coût de récupération du tableau. 16/09/2026

**D-30 — La nutrition entre par la tolérance glucidique, pas par un journal.**
Le suivi libre de « ce qui marche et ce qui ne marche pas » ne prédit rien et n'est
corrigé par rien : c'est un carnet, il reste **hors modèle**. Ce qui entre est une
grandeur unique, G-NUT-001, dont l'entraînement digestif progressif est documenté
→ S-NUT-001, S-NUT-002.

**Rattachement** : uniquement aux séances au-delà d'environ **2 h** — en deçà l'apport
à l'effort n'a pas d'objet. Prioritairement la sortie longue, plus une ou deux séances
plus courtes dans la semaine : l'exposition régulière compte davantage que quelques
grosses séances isolées. La durée documentée de l'entraînement digestif (8 à 10 semaines)
coïncide avec celle du bloc spécifique de D-21 — il s'y cale sans règle supplémentaire.

**Carnet, hors modèle** : produits, goûts, textures tolérés se notent et s'affichent, sans
rien calculer. Une seule conséquence modélisée : la tolérance étant en partie spécifique
au produit, changer de produit invalide une partie de l'acquis → le carnet sert de
**contrainte** (« teste ce que tu utiliseras en course »), jamais de coefficient.

**Module désactivable.** La nutrition est optionnelle : désactivée, G-NUT-001 disparaît
avec ses prescriptions et son carnet, et **rien en aval ne casse** — aucune autre
grandeur ne dépend d'elle. Elle se réactive en repartant de la valeur générique, pas de
la dernière valeur atteinte, si l'interruption dépasse la péremption de D-16. C'est la
même dégénérescence propre que pour un coureur route sans observation en pente (D-23) :
une brique en moins, pas un mode dégradé.

**Hydratation et sodium : hors périmètre, écrits comme exclus.** Motif : le volume bu
seul ne prédit rien et n'a pas d'observation correctrice — il n'est interprétable
qu'avec un taux de sudation individuel, qui exige une pesée avant et après chaque sortie
longue, protocole nettement plus lourd que celui de G-NUT-001. Les recommandations
d'apport hydrique sont par ailleurs bien moins établies que celles des glucides et la
variabilité individuelle y est très forte → S-NUT-003. Une grandeur « hydratation »
serait donc un paramètre générique permanent, à rejeter. Le **volume bu et les
conditions** (température, durée) peuvent figurer au carnet — utiles pour dimensionner
bidons et ravitaillements — sans entrer dans le modèle. À rouvrir seulement si un
sous-module de pesée avant/après est un jour souhaité.

**Route** : même mécanisme, seuil de durée plus haut et doses souvent plus basses pour
les finishers lents. Aucune règle spécifique. 17/09/2026

**D-31 — Deux modules d'activité complémentaire, séparés par ce que le modèle en fait.**

| Module | Nature | Contenu |
|---|---|---|
| **Renforcement** | prescriptif | type de séance (D-29), placement (R-REN-005), progression propre |
| **Autres activités** | déclaratif | vélo, natation, ski, autres — absorbées en charge via sRPE (G-CHG-001) |

Un module par sport dupliquerait un mécanisme identique à N exemplaires ; un module unique
écraserait une différence de nature réelle. Le **type d'activité déclaré se réduit à trois
dominantes** — jambes, haut du corps, mixte — car son seul usage est de savoir si
l'activité contamine une séance course proche (filtre de G-CHG-001). Pas de liste de
sports.

**Désactivation.** Renforcement : arrête une **prescription** et libère des créneaux — la
composition de la semaine change, ce n'est pas une simple brique en moins (contrairement
à D-30). Une **information unique** est affichée au moment du geste sur l'intérêt
documenté du renforcement (S-REN-001, S-REN-004), jamais répétée — l'action existe
(réactiver), ce qui la distingue des alertes rejetées en D-28. Autres activités :
désactiver équivaut à ne rien déclarer, l'interrupteur ne pilote **aucune** décision de
modèle — confort d'affichage uniquement, à écrire comme tel pour ne pas maintenir un
réglage creux.

**Question posée à l'inscription : disponibilité, jamais intention.** « As-tu accès à un
vélo (ou à un bassin), et accepterais-tu que le plan le propose en remplacement d'une
séance ? » Oui/non. Motif du rejet d'une question d'intention : à l'inscription le coureur
ne sait pas s'il atteindra un plafond ni s'il aura une gêne — il figerait une préférence
pour des situations inconnues, même défaut que les catégories de coureur supprimées en
D-14.

**Substitution — périmètre et interdits.** Déclencheurs utilisables : **gêne déclarée**
(D-32) et **contrainte pratique**. Le déclencheur « plafond d'impact » devient utilisable
via D-33. Interdits :
- une séance substituée **n'est jamais créditée au volume course cible** — elle compte en
  charge (G-CHG-001), rien de plus. Aucun taux de conversion n'est employé : il serait
  invérifiable chez un utilisateur unique (trou « adaptation croisée ») ;
- **jamais de substitution d'une séance clé** (sortie longue, sorties clés de D-22) : c'est
  la séance la plus spécifique, elle construit la tolérance à durer sur les pieds, que le
  vélo ne développe pas. La substitution porte sur du volume facile ;
- **aucun argumentaire santé**. L'app dit « tu as signalé une gêne » ou « contrainte de
  créneau », jamais « c'est mieux pour tes articulations » : la course à pied récréative
  est associée à **moins** d'arthrose que la sédentarité → S-BLE-002. Le sujet réel est le
  dosage, pas l'impact.

**Aqua-jogging et natation** : même mécanisme. Pour une période où la course est
impossible, l'aqua-jogging a les meilleures preuves de maintien (S-CHA-003 et trou
« adaptation croisée ») ; ni l'un ni l'autre n'est crédité au volume course. 17/09/2026

**D-32 — Champ gêne / douleur à la saisie de séance, avec conséquences graduées.**
Deux entrées facultatives : **localisation** (zone corporelle, liste courte) et
**intensité** (0–10). Cadre repris du *pain-monitoring model* → S-BLE-001 : la charge peut
continuer tant que (a) l'intensité ne dépasse pas ~5/10, (b) elle est revenue à la normale
le lendemain matin, (c) elle n'augmente pas d'une semaine à l'autre.

| Observation | Conséquence |
|---|---|
| Gêne isolée, ≤ 5/10, non récurrente | **aucune** — enregistrée, rien d'autre |
| Même localisation récurrente sur plusieurs séances | signal **localisé** de D-33 : volume course réduit, substitution proposée |
| Intensité croissante d'une semaine à l'autre, ou > 5/10, ou persistante le lendemain | réduction et **orientation vers un professionnel de santé** |

**L'app ne diagnostique jamais** et ne nomme aucune pathologie : elle adapte la charge et
oriente. **Niveau : modéré** pour les trois critères (essai randomisé), **extrapolation**
pour leur application à une gêne quelconque — S-BLE-001 porte sur des tendinopathies en
rééducation, pas sur la surveillance générale d'un coureur sain. 17/09/2026

**D-33 — Séparation du plafond d'impact et du plafond systémique.** G-PLA-002 lisait trois
signaux tous globaux (ressenti, décroissance-fatigue, séances non faites) : ils ne
disaient pas si ce sont les jambes qui saturent ou l'organisme entier. Le champ de D-32
fournit le signal localisé manquant.

| Signaux | Lecture | Action |
|---|---|---|
| Localisés seuls | **plafond d'impact** | volume course réduit, charge totale maintenue → substitution valide |
| Globaux seuls | **plafond systémique** | charge totale réduite, **aucune** substitution — ajouter du vélo aggraverait |
| Les deux | systémique prioritaire | charge totale réduite d'abord |
| Aucun | pas de plafond atteint | progression normale |

**Limite écrite** : chez un coureur qui ne pratique que la course, la distinction repose
entièrement sur le champ de D-32, facultatif. Sans gêne déclarée, le modèle **se rabat sur
la lecture systémique** — choix prudent : il réduit la charge totale plutôt que de proposer
une substitution qu'il ne sait pas justifier. **Niveau : extrapolation.** 17/09/2026


**D-34 — Répartition des intensités, polarisée en fond, pyramidale en bloc spécifique.**
Étape 5 (Semaine). Cible en part du volume hebdomadaire, par catégorie de D-29 :

| Catégorie (D-29) | Fond | Bloc spécifique |
|---|---|---|
| Endurance fondamentale + sortie longue (< 80 %) | ≥ 80 % | 65–75 % |
| Allure spécifique + côtes longues (80 % ≤ x < 95 %, zone « intermédiaire ») | ≤ 5 % | 15–25 % |
| Seuil + intervalles + côtes courtes (≥ 95 %) | 10–15 % | 8–12 % |

**Bornes disjointes — corrigé le 17/09/2026.** La rédaction initiale (« 80–100 % » et
« > 95 % ») faisait appartenir la plage 95–100 % aux deux lignes : un même segment
pouvait compter deux fois et l'histogramme d'adhérence (D-34, ex-G-PLA-003) ne pouvait pas se construire sans
ambiguïté. Frontière unique fixée à **95 %**. Les fourchettes de D-29 (seuil 95–105 %,
côtes longues 90–100 %) décrivent la **cible d'une séance** ; le classement d'un segment
observé se fait ici, sur la seule frontière à 95 %.

**Segments marchés exclus du calcul.** Les portions marchées (D-40) sont mesurées en VAM,
pas en %VC : elles ne peuvent entrer ni dans ces cibles ni dans l'histogramme d'adhérence
(D-34, ex-G-PLA-003). Elles sont **retirées du dénominateur** et leur part de temps est affichée à
part — sur une sortie longue d'ultra elle peut être importante, et la répartition serait
sinon calculée sur une fraction de la séance sans que rien ne le signale.
**Trou ouvert** : aucune cible de répartition n'existe pour le temps marché.

**Ce qui est solide** → S-COU-008, S-COU-009 : les modèles polarisé et pyramidal battent
tous deux un entraînement centré sur le seuil ; le point le plus répété dans la
littérature est que les coureurs récréatifs dérivent systématiquement vers la zone
intermédiaire, celle qui rapporte le moins pour l'effort investi. **Niveau : modéré**
pour ce point précis (converge sur plusieurs sources indépendantes).

**Ce qui est incertain** : l'avantage relatif polarisé/pyramidal dépend de la distance
(léger avantage polarisé sur 5-10 km, léger avantage pyramidal sur marathon, différences
plus petites qu'annoncé par les premières études) → S-COU-009. **Aucune étude ne couvre
l'ultra-trail** : le glissement fond→pyramidal proposé ici extrapole la tendance
observée sur des distances plus courtes. **Niveau : extrapolation** pour le tableau
chiffré et pour son application à l'ultra.

**Spécificité trail assumée** : la zone « intermédiaire » que les modèles génériques
cherchent à limiter contient l'allure spécifique et les côtes longues — en ultra-trail
ce n'est pas une dérive à corriger mais une nécessité imposée par le terrain. La montée
de sa part en bloc spécifique **recoupe directement la progression déjà écrite en D-28**
pour le dénivelé — aucun second mécanisme, même levier.

**Résout la dépendance ouverte en D-29** (risque de dérive au-dessus du plafond de
l'endurance fondamentale) : le plafond existait sans cible chiffrée à surveiller, il en a
une désormais.

**Contrôle d'adhérence — règle d'affichage, pas grandeur** (rétrogradation de G-PLA-003 le
20/09/2026). L'histogramme du temps passé par bande de %VC sur la semaine écoulée est
comparé à la cible ci-dessus ; une dérive répétée sur plusieurs semaines est **signalée**
au coureur dans le bilan hebdomadaire (D-59), **sans modifier automatiquement le plan** —
c'est un miroir, pas une correction imposée. Aucune donnée supplémentaire à collecter,
aucun état à conserver : le calcul est refait à la demande. 17/09/2026

**D-35 — Un jour porte une séance course, avec une exception pour le renforcement.**
Étape 5 (Semaine). Pas de double séance course/course : combinatoire inutile pour la
population visée, et ce n'est pas un plan pour grands champions. **Exception** : le
renforcement (20-45 min) peut s'accoler à une séance course le même jour, tant que
R-REN-005 est respecté — sinon un coureur à 3 jours disponibles perdrait un tiers de
ses créneaux à une séance courte, exactement le profil le moins bien servi sinon.

**Les jours disponibles (D-17b) sont un plafond, pas une obligation.** Une semaine de
relâche (D-57b) doit pouvoir laisser un jour disponible vide, sinon la cadence de
relâche déjà construite n'a plus de levier pour s'exercer.

**Deux jours consécutifs de sortie longue restent possibles**, et c'est distinct de
l'alternance longue/très longue semaine à semaine de D-22 — deux outils différents.
**Restreint le 17/09/2026** après vérification : réservé au **bloc spécifique**
uniquement (jamais en fond, une base aérobie doit déjà exister), et aux cibles dont la
**durée d'effort attendue dépasse 4 h** → S-TRA-009 (propagation de D-44 le 17/09/2026 ;
la source parle de 50 miles / 100 km, soit cet ordre de durée) — aucune source ne
l'applique en deçà. La paire consécutive **consomme une des trois sorties clés déjà plafonnées**
(D-22), elle ne s'ajoute pas au-delà. Ne se positionne que lorsque le plafond
systémique (D-33) est dégagé — l'aborder depuis un état déjà fatigué réduit son intérêt
et augmente le risque, exactement le défaut que l'outil cherche à éviter. **Niveau :
sans objet** (convergence de pratique de coachs). 17/09/2026 **Précisé le 22/09/2026** :
chacun des deux jours respecte la règle des 30 jours (D-63c) ; la paire n'existe ni en
fond ni en affûtage.

**Corrigé le 22/09/2026 (TESTS.md, neuvième série, `sim7.py`).** Le seuil « > 4 h »
ci-dessus était mal aligné avec sa propre source : S-TRA-009 parle de 50 miles / 100 km,
soit la tranche **8–20 h**, pas 4–8 h — l'erreur venait d'une propagation de D-44 qui
avait changé l'index sans vérifier contre le texte de la source. **La paire est donc
réservée à la tranche 8–20 h.** Simulée : n'a de sens que si le premier jour tient au
moins 3h30 sans dépasser le maximum déjà couru des 30 jours (sinon la paire dégraderait
un jour de progression normale) ; le second jour prend le reste de la part des sorties
clés (D-22). Sur un coureur à ~7 h/semaine (proche du profil d'Antoine), la paire
produit 2h49 puis 1h52 — plus faible qu'une seule sortie clé de 4h45 — et fait légèrement
reculer l'atteinte de la cible basse de D-22 (69 % → 70 %, à peu près neutre en
pratique ; testé sur un profil à volume moindre, la paire ne s'active quasiment jamais,
0,07 fois par préparation, faute d'un jour 1 suffisant). **Sans intérêt démontré au
volume d'Antoine pour un 80 km ; reste un outil pour un volume plus élevé ou un format
plus long.** Aucune source ne compare la paire à une sortie clé unique en termes de
résultat de course — seulement en termes de fatigue perçue. **Niveau : sans objet**
(convergence de pratique de coachs, aucune étude contrôlée).

**D-36 — Jour sauté : reprogrammer ou annuler, jamais rattraper.** Deux branches
proposées au coureur.

**Reprogrammer** : le générateur propose toujours en premier un créneau qui respecte
l'espacement de sécurité (A-05, niveau 1 — ne cède jamais). Si la semaine ne laisse
**aucune** case propre, il présente la moins mauvaise option avec un avertissement non
bloquant — jamais l'inverse (ne jamais proposer un mauvais créneau par défaut quand un
bon existe). A-05 reste vrai pour ce que le modèle **propose** ; le coureur garde la
main pour forcer un choix déconseillé.

**Annuler** : le volume perdu est **accepté, jamais rattrapé**. Un rattrapage romprait
la règle des 30 jours (D-63c, ex-plafond de 20 % de D-22b — renvoi corrigé le 23/09/2026) et recréerait le forçage que le garde-fou
cherche à éviter. La séance annulée devient une observation de plus pour G-PLA-002, qui
l'absorbe déjà (l'un des trois signaux qui font baisser le volume cible) — aucun
mécanisme supplémentaire. 17/09/2026

**D-37 — Jour de sortie longue : septième paramètre déclaré.** Passe le test de D-17
(le changer change la semaine). Contrainte de cohérence : doit appartenir aux jours
disponibles déclarés (D-17b), sinon les deux paramètres se contredisent silencieusement.
Reste déplaçable ponctuellement en cas d'indisponibilité datée — trou n° 13 du
chantier, **traité par D-46** (renvoi corrigé le 23/09/2026). Liste des paramètres déclarés (D-17) : (a) à (f)
précédents, (g) jour de sortie longue. 17/09/2026

**D-38 — Deux ensembles de jours déclarés, pas un pool partagé.** Amende D-17b et D-35.
« Jours disponibles course à pied » (incluant lequel porte la sortie longue — D-37 en
devient un attribut, plus un paramètre à part) et « jours disponibles renforcement »,
déclarés séparément. Motif : les jours de course sont typiquement flexibles ; les jours
de renforcement dépendent souvent d'une contrainte externe fixe (horaire de salle, cours
collectif, partenaire) — les traiter comme un seul pool que le modèle répartit librement
gommait cette différence.

**Ce qui reste au générateur** : quel type de séance course (D-29) tombe sur quel jour
de l'ensemble course, pour s'accommoder au mieux des jours de renfo fixés. **Ce qu'il
perd** : la liberté de choisir sur quels jours le renfo peut avoir lieu.

**Chevauchement** : un jour présent dans les deux ensembles déclenche l'exception de
D-35 (renfo accolé à une séance course), sous réserve de R-REN-005.

**Vérification à la déclaration, pas seulement à l'exécution.** Une incompatibilité
structurelle entre les deux ensembles (ex. sortie longue systématiquement suivie d'une
séance jambes le lendemain, hors fenêtre R-REN-005) ne peut pas être réparée semaine
après semaine par une reprogrammation ponctuelle (D-36) — c'est permanent, pas un
imprévu. Dès la déclaration ou la modification de l'un des deux ensembles, le
générateur vérifie la compatibilité avec R-REN-005 et, en cas de conflit récurrent,
nomme les jours en cause et propose un ajustement — même principe que A-06 (dégrader et
expliquer, jamais échouer en silence), appliqué au moment de la déclaration plutôt qu'à
celui de la génération.

**Paramètres déclarés, liste mise à jour** (amende D-17, D-37) : (a) course cible ;
(b) jours disponibles course à pied, incluant le jour de sortie longue ; (c) volume
actuel ; (d) autres activités : présence, fréquence, type ; (e) technicité par
parcours ; (f) accès vélo/bassin ; (g) jours disponibles renforcement. 17/09/2026

**D-39 — Progression du renforcement calée sur les phases déjà définies, dominante par
phase.** Étape 5 (Semaine), élément 8 du chantier. Aucun nouveau concept de phase :
même découpage que D-21 (fond / bloc spécifique / pic / affûtage), une dominante et une
fréquence assignées à chacune → S-REN-005.

| Phase | Dominante | Fréquence |
|---|---|---|
| Fond | Stabilité, gainage, force générale légère | 2–3 séances/semaine |
| Début / cœur de bloc spécifique | Force maximale (charges lourdes, peu de répétitions) | 2 séances/semaine |
| Fin de bloc spécifique (pic) | Pliométrie, puissance | 1–2 séances/semaine |
| Affûtage | Volume fortement réduit, intensité maintenue, pas d'arrêt complet | 0–1 séance/semaine |

**Lien avec D-28** : la dominante **excentrique** — trou déjà identifié pour la
descente en trail → S-REN-003 — peut monter en fin de bloc spécifique si le **profil de
course est connu** (D-27) et montre du dénivelé négatif significatif. Même levier que
D-28 pour les côtes, appliqué au renforcement.

**Aucune nouvelle grandeur** : si le renforcement n'est pas réduit correctement à
l'approche de la course, ça se lit déjà dans la charge extra-course (G-CHG-001) et le
plafond systémique (D-33) — mécanismes existants, rien à ajouter.

**Niveau** : S-REN-005, sans objet (convergence de pratique de coachs). Une étude est
mentionnée en appui pour l'effet du renforcement en force maximale sur l'économie de
course → S-REN-006, **vérifiée le 17/09/2026** : Berryman et coll., *International
Journal of Sports Physiology and Performance* 13(1):57-63 — et non *Sports Medicine*
comme l'annonçait la source secondaire. Méta-analyse de 28 études : la **force maximale
produit les plus grandes améliorations** du coût énergétique de la locomotion, quel que
soit le niveau de l'athlète. **Niveau : élevé.** Elle fonde désormais directement le
choix de la force maximale en début de bloc spécifique, qui ne reposait jusqu'ici que sur
une convergence de coachs. 17/09/2026

**D-40 — Marche : une bande de plus dans G-TER-001, mesurée en VAM plutôt qu'en
allure.** Étape 5 (Semaine), élément 9 du chantier. Résout la réserve déjà posée dans
G-CAP-001 (le %VC perd son sens sur les portions marchées).

**Portée du filtre — corrigée le 17/09/2026 après passe adverse (H-01).** Les critères
de régularité sont **corrélés à ce qu'on cherche à mesurer** : en pente forte et en
descente technique, cadence et allure varient naturellement davantage, donc un filtre
binaire rejette surtout les bandes qu'on peine déjà à calibrer — biais de sélection sur
la variable étudiée, pas simple perte de données. Deux régimes désormais :
**FC (D-09, D-10)** : filtre binaire conservé — l'argument est quantitatif (13 %
d'erreur du capteur contre quelques pourcents de signal recherché), un segment non
régulier est inexploitable.
**Coût-pente (G-TER-001)** : **pondération par la régularité**, pas exclusion — un
segment moyennement régulier pèse moins, il ne disparaît pas. Supprime le biais et
récupère le terrain vallonné, où les bandes changent en permanence.

**Détection** : par le signal, jamais déclarée — pente au-delà d'un seuil (~25-30 %,
cohérent avec S-COU-011) ou cadence caractéristique de la marche, selon ce qui survient
en premier. Même logique que D-10, réutilisée.

**Effort de référence** : le VAM (mètres de dénivelé positif par heure), déjà calculé
nativement par les montres de trail — aucune donnée supplémentaire à collecter. Motif
physiologique → S-COU-001, S-COU-011 : au-delà du seuil, le déplacement vertical domine
le coût énergétique, l'allure horizontale devient quasi non-informative.

**Traitée comme bande rare (D-23), pas comme grandeur séparée** : confiance nulle sans
exposition, aucune valeur générique de départ inventée — aucune source solide n'en
fournit une pour ce cas. Se calibre uniquement sur observation personnelle, comme les
autres bandes rares de G-TER-001.

**Limitation partagée avec G-FAT-001, nommée et non résolue.** Ni le %VC ni la FC (déjà
exclue par D-10 sur segments avec bâtons) ne fonctionnent sur ces portions : la
décroissance-fatigue a le même angle mort que le coût-pente. Pas de mécanisme parallèle
construit maintenant — ajouterait de la complexité pour un cas rare avant d'avoir vu si
le reste tient. **Trou ouvert**, pas un oubli. 17/09/2026



**D-41 — Encarts pédagogiques : principe posé, contenu hors périmètre.** Chaque
décision cite déjà ses sources (S-CAT-nnn) — lien exploitable pour un affichage
contextuel dans l'app, extension naturelle de la traçabilité (A-16). Deux critères pour
éviter le bruit : un encart seulement là où le choix est **contre-intuitif** ou
**débattu**, jamais en systématique. **La rédaction du contenu est un chantier
éditorial séparé**, non modélisant — SPEC.md ne devient pas un document de contenu.
17/09/2026

**D-42 — Format de prescription : plage d'allure dont la largeur suit la confiance,
jamais un chiffre unique. Referme l'élément 19 du chantier.** Étape 6 (Séances).

**Séances fermes (A-09, 1-2 semaines)** affichent : type et motif (D-29), durée,
terrain, intensité cible. L'intensité cible n'est **jamais un chiffre unique** — c'est
une plage d'allure (ou de VAM pour les segments de marche, D-40) dont la **largeur
diminue avec la confiance** de G-CAP-001 et G-TER-001. Un chiffre unique afficherait une
précision que le modèle n'a pas — même défaut que les cas déjà rejetés (D-18, le nombre
de montées de D-27). Nutrition cible affichée si la séance dépasse ~2 h (G-NUT-001).
Si le gabarit a dû dégrader une contrainte pour produire la semaine (A-06), la contrainte
cédée est nommée.

**Avant que G-CAP-001 ait au moins deux points de durées différentes** (le pont
RPE de D-23/C1) : **aucune plage d'allure** — l'affichage se limite à « effort
confortable, conversation possible », ancré sur le ressenti plutôt que sur un calcul
qui n'existe pas encore. C'est la réponse complète à l'élément 19 : le cas du coureur
sans aucune donnée n'est pas un affichage différent à inventer, c'est l'absence de
plage tant que rien ne la fonde.

**Trame indicative** (au-delà des séances fermes) : déjà définie par A-09 — type et
volume par semaine seulement, aucun détail de séance. Rien à ajouter ici. 17/09/2026

**D-43 — Statut de séance : détecté par défaut, jamais un journal à remplir.** Étape 6,
élément 11. Cinq statuts : conforme, modifiée, remplacée, reprogrammée, non réalisée.

**Détection automatique**, même philosophie que D-10 et D-40 (signal plutôt que
déclaration) : l'activité réellement enregistrée sur le créneau est comparée à ce qui
était prescrit. Dans la tolérance (durée/distance, bon type, bon jour) → conforme. Hors
tolérance mais une activité existe → modifiée, l'écart lui-même devient l'information,
rien à saisir. Une activité d'un **autre type** apparaît sur le créneau (vélo, natation)
→ remplacée, détectée sans que le coureur ait à confirmer la substitution de D-31.
Correction manuelle toujours disponible — l'auto-détection est un confort, pas une
contrainte.

**Fenêtre de grâce** avant de conclure à une séance non réalisée (quelques jours) ;
passé ce délai sans choix du coureur, D-36 s'applique rétroactivement (annulée, jamais
rattrapée).

**Ne crée aucun nouveau canal d'admissibilité.** Le statut est un objet de présentation
et de déclenchement — il alimente A-03 (recalcul, déjà répertorié) et l'un des trois
signaux de G-PLA-002 — il ne concurrence pas D-10/A-02 qui décident, indépendamment du
statut, si une observation entre dans le calcul d'un coefficient. 17/09/2026

**D-44 — Les tranches sont indexées sur la durée d'effort attendue, pas sur la
distance. Referme l'élément 15 du chantier sans doubler aucun tableau.** Étape 4
(Blocs).

Motif : un marathon route (≈ 4 h) et un 30 km trail à 1500 m D+ (≈ 4 h) demandent un
**volume et une structure de blocs** semblables, alors qu'un index sur la distance les
envoie dans deux tranches différentes. Doubler les tableaux (une version route, une
version trail) aurait figé cette incohérence en la dupliquant.

**Correction du 17/09/2026 — la rédaction initiale disait « demandent des préparations
semblables », ce qui est faux.** La durée gouverne le volume, la structure des blocs, la
durée de sortie longue et les besoins nutritionnels. Elle ne gouverne **ni le coût de
récupération, ni la composition des séances** : à durée égale, le trail produit plus de
dommages musculaires que la route (charge excentrique en descente) et une semaine
chargée en trail récupère plus lentement ; le profil d'intensité diffère aussi, la route
étant proche d'un état stable quand le trail ressemble davantage à du fractionné
→ S-TRA-011. Deux axes distincts, donc : **la durée indexe le volume, le D+ module le
coût de récupération et le contenu** (D-28 pour le type de montée, D-39 pour la
dominante excentrique du renforcement).

**Modulation du coût de récupération — amorçage seulement, aucun coefficient
permanent.** Facteur empirique de coachs : 1 h de trail modéré ≈ 1,2 à 1,4 h de route en
comptabilité de fatigue → S-TRA-011, **niveau sans objet**. Employé uniquement pour
initialiser le volume d'un coureur trail en dessous de celui d'un coureur route à durée
égale, le temps que la **tolérance observée** (G-PLA-002, plafonds de D-33) prenne le
relais — même trajectoire que le kilomètre-effort pour la durée et que S-COU-001 pour le
coût-pente.

| Durée d'effort attendue | Ancienne étiquette trail | Équivalent route indicatif |
|---|---|---|
| < 2 h | 10–21 km | 10 km → semi |
| 2–4 h | 21–42 km | semi → marathon |
| 4–8 h | 42–60 km | au-delà du marathon |
| 8–20 h | 60–100 km | — |

Les étiquettes en distance restent affichées comme repère familier ; **l'index de
calcul est la durée**.

**Estimation de la durée** : amorçage par le kilomètre-effort → S-TRA-010
(`distance + D+/100`, converti en durée via la vitesse de référence), puis remplacement
progressif par l'estimation issue de G-CAP-001 et G-TER-001 dès qu'elles convergent —
même trajectoire générique → personnel que partout ailleurs.

**Pas une violation de D-01 ni de A-02** : cette durée estimée est une **entrée de
planification** dérivée des grandeurs, jamais une observation, et le temps de course
prédit reste dérivé a posteriori par composition comme prévu.

**Stabilité (A-08)** : la tranche est **fixée à la création du plan** et n'est
réévaluée qu'aux recalculs majeurs de A-03, avec hystérésis — une VC qui progresse ne
doit pas faire basculer le coureur de tranche en cours de préparation et rejouer toute
sa structure. **Niveau : extrapolation** pour les bornes de durée. 17/09/2026

**D-45 — Le modèle calcule en durée, l'affichage se règle en durée ou en distance.**
Referme l'élément 14. Toutes les grandeurs, tous les volumes et toutes les prescriptions
sont calculés en **temps** : c'est la seule unité qui garde du sens quand la pente
change (une même distance peut coûter du simple au triple), et elle vaut aussi bien sur
route.

**Affichage** : préférence du coureur, durée ou distance. La conversion utilise **sa
propre** vitesse de référence et son coût-pente, jamais une allure générique — un
coureur route qui préfère « 10 km » les voit, un traileur voit « 1 h 10 ». Aucune
donnée supplémentaire, aucune grandeur de plus : c'est une préférence d'affichage, pas
une décision de modèle.

**Exception** : la cible (D-17a) reste toujours saisie en distance et dénivelé — c'est
ainsi que les courses sont annoncées. 17/09/2026

**D-46 — Indisponibilités datées : déclarées à l'avance, absorbées, jamais
rattrapées.** Referme l'élément 13. Périodes déclarées (début, fin) avec un niveau :
**aucune activité** ou **course facile seulement** (cas du déplacement avec des
chaussures mais sans créneau long).

| Où tombe la période | Effet |
|---|---|
| Fond | absorbée — traitée comme une relâche anticipée, la cadence de D-57b s'y cale |
| Bloc spécifique | réduit la durée effective de construction → recalcul du garde-fou (D-19), qui peut faire passer en orange ou rouge |
| Affûtage | souvent compatible — l'affûtage est déjà une baisse de volume (D-25) |

**Jamais de rattrapage** — même règle que D-36 : le volume perdu est accepté. Compresser
autour d'une absence connue recréerait exactement le forçage que le garde-fou évite.

**Déclarées à l'avance, donc anticipées** : contrairement à un jour sauté (D-36) qui est
un imprévu, une indisponibilité connue entre dans la construction du plan dès sa
déclaration — c'est une donnée de planification, pas une réaction.

**Aucun mécanisme nouveau pour la perte de forme** : une longue coupure fait décroître
la confiance des grandeurs par la péremption de D-16, et le plancher de D-15 empêche la
valeur de s'effondrer. Déjà couvert. 17/09/2026
**Corrigé le 22/09/2026 (D-63h)** : faux pour le volume. G-PLA-002 ne figure pas au
tableau de D-16 : après une coupure, le volume cible restait celui d'avant, alors que la
tolérance du coureur avait baissé. La reprise du volume et du seuil mémorisé est
désormais réglée par D-63h ; le reste de ce paragraphe tient pour les autres grandeurs.


**D-47 — Terrain disponible : deux questions à l'inscription si la cible comporte du
dénivelé, corrigées ensuite par l'observation. Referme l'élément 16.**

**Correction du 17/09/2026** : une première rédaction posait « déduit de l'historique,
jamais déclaré ». Erreur — elle appliquait à tort le motif de rejet de D-27 (le nombre
de montées d'une course inconnue), dont le critère réel était *le coureur peut-il le
savoir ?*. Pour le parcours d'une course jamais courue, non ; pour **son propre
terrain**, oui. Et une absence de dénivelé dans l'historique a deux causes opposées —
le terrain n'existe pas, ou le coureur n'y est jamais allé (coureur route passant au
trail, déménagement) — que l'observation seule ne distingue pas : c'est le cas
« absence de preuve n'est pas preuve d'absence » déjà tranché en D-19, reproduit par
inadvertance.

Deux questions, posées **seulement si la cible comporte du dénivelé** : (a) D+ maximal
atteignable en une sortie depuis chez soi ; (b) fréquence d'accès à ce terrain (chaque
semaine / occasionnellement / pas du tout). Déclarées en amorçage, corrigées ensuite par
le dénivelé réellement réalisé (D-43, même signal que G-PLA-002). Huitième et neuvième
paramètres déclarés (D-17, D-38).

**Ce qu'il contraint** : le D+ prescriptible par semaine, et la faisabilité des types de
séance de D-29. Sans pente longue accessible, les **côtes longues** ne sont pas
prescriptibles — le plan bascule sur des côtes courtes répétées, et c'est une
**limitation nommée**, pas un remplacement silencieux.

**Nouveau cas pour le garde-fou (D-19)** : un coureur dont le terrain accessible ne
permet pas d'approcher le D+ de sa cible a un manque que **ni la durée de préparation ni
le volume ne comblent** — aucune des trois conditions actuelles ne le détecte. Ajout
d'une condition **orange** : D+ hebdomadaire atteignable très inférieur à ce que la cible
exige. Orange et non rouge : des substituts partiels existent (escaliers, tapis incliné,
répétitions de côtes courtes), et l'exposition à la descente prolongée reste le vrai
manque — à relier au coût musculaire de la descente, hors périmètre.
**Niveau : extrapolation.** 17/09/2026

**D-48 — Chaleur, altitude et nuit : exclues du modèle, présentes en contenu. Referme
l'élément 17.** Ces trois facteurs sont réels sur un objectif de montagne, et
l'acclimatation à la chaleur comme à l'altitude est documentée. Ils sont pourtant
**exclus des grandeurs**, pour une raison unique et déjà éprouvée ailleurs : aucune
observation correctrice disponible. Le modèle ne collecte ni température, ni altitude
d'entraînement, ni conditions de luminosité, et n'a aucun moyen de mesurer l'effet d'une
acclimatation sur ce coureur précis. Une grandeur construite là-dessus serait un
paramètre générique permanent — rejeté par R-ENT-001.

**Ce qui reste possible sans modéliser** : un rappel éditorial déclenché par la date et
le profil de la cible (course estivale, course en altitude, course de nuit), via le
mécanisme d'encarts de D-41. Information, pas prescription — aucun calcul, aucune
grandeur, aucune donnée à collecter.

**Réouverture conditionnée** à la disponibilité d'une observation : température par
séance (certaines montres l'enregistrent), altitude des sorties (déjà dans le GPX). Le
jour où l'une existe et qu'on sait quoi lui faire corriger, le sujet redevient
admissible. 17/09/2026

**D-49 — Les deux seuils numériques laissés ouverts. Referme l'élément 18.** Aucun des
deux n'a d'appui scientifique : ce sont nos choix, écrits pour être discutés et
éprouvés sur données réelles, pas des valeurs trouvées.

**(a) Seuil de stabilité (D-13a)** — une estimation est dite **convergée** quand son
déplacement sur les dernières observations devient **petit devant la dispersion observée
de ces mêmes estimations**, avec un repère de départ à 5 % sur 5 observations.
**Corrigé le 17/09/2026 après passe adverse (H-03)** : un pourcentage fixe n'a pas le
même sens sur un coût-pente et sur un volume hebdomadaire, et cinq points bruités peuvent
s'accorder par hasard. Surtout, **l'erreur est asymétrique** — déclarer convergé trop tôt
rend l'app confiante et fausse, ce qui ne se paie qu'en course ; trop tard la rend
seulement vague. Le seuil est donc volontairement **conservateur** : en cas de doute, on
ne déclare pas convergé.
Un seuil unique pour toutes les grandeurs à convergence (G-TER-001, G-CHG-001,
G-PLA-002, G-RES-001b), conformément à R-MET-002. Sert aussi de seuil de
republication du plan (A-08) : une variation inférieure ne republie rien.

**Mesurée sur fenêtre récente pondérée, jamais sur tout l'historique — précision du
17/09/2026.** Motif : un coefficient comme le coût-pente **n'est pas censé être
immobile** — le renforcement améliore l'économie de course (S-REN-001, S-REN-004), donc
il s'améliore pendant la préparation. Un critère de convergence appliqué à l'historique
entier déclarerait « jamais fiable » précisément le coureur qui progresse — même erreur
que celle corrigée sur G-NUT-001 en la reclassant. Ce sont les **estimations récentes
qui doivent s'accorder entre elles**, la pondération étant celle de D-16.

**Diagnostic de non-convergence — une cause identifiable, pas une fatalité.**

| Cause | Action |
|---|---|
| Trop peu de segments admis (seuils trop stricts, ou terrain très technique) | assouplir les seuils : le réglage est en cause, pas le coureur |
| Trop peu de séances (1–2/semaine) | rien à corriger — mécanique, la convergence prend plus longtemps, l'app le dit |
| Données dégradées massivement rejetées par A-15 | signaler : c'est un problème de capteur ou d'import, pas de modèle |
| Le coefficient dérive réellement | ce n'est pas un échec — la fenêtre récente le fait converger quand même |

**Ce que voit l'utilisateur** : rien de bloquant. L'app fonctionne en durées et efforts
ressentis plutôt qu'en allures chiffrées (D-42) — c'est déjà le mode du premier mois
pour tout le monde. **Le taux de segments admis et l'état de convergence par grandeur
sont des indicateurs de réglage à notre usage** (jeux de test, A-11), pas un écran
utilisateur.

**(b) Seuils de régularité d'un segment — rapatriés dans D-10 le 20/09/2026.** Ils
étaient décrits à deux endroits, source de divergence. **D-10 fait foi.** 17/09/2026


**D-50 — Module blessure : exécuter les contraintes d'un professionnel, ne jamais les
produire.** Étape transverse. Distinct de D-32 : une blessure n'est pas le haut de
l'échelle de gêne, c'est structurellement une **indisponibilité** (D-46) dont la fin
n'est pas connue à la déclaration et dont la sortie est une remontée progressive (D-51).

**Activation par le coureur, jamais automatique.** Une gêne répétée (D-32) peut
**suggérer** d'activer le module et d'orienter vers un professionnel ; elle ne l'active
pas. Basculer quelqu'un en « blessé » sur la foi de deux notes serait un diagnostic
déguisé.

**Les quatre entrées, issues de la consultation :**

| # | Entrée | Format | Lu par le modèle ? |
|---|---|---|---|
| 1 | Diagnostic | texte libre | **NON** — consigné pour le coureur et pour le suivi médical, jamais interprété. En tirer quoi que ce soit reviendrait à encoder de la logique par pathologie |
| 2 | Course autorisée | non / oui avec restrictions / oui sans restriction | oui |
| 3 | Réduction de charge | % du **volume** si un chiffre a été donné ; sinon échelle qualitative (légère / modérée / forte) avec défaut conservateur. Drapeaux **séparés** : pas d'intensité, pas de dénivelé, surface imposée, durée maximale par séance | oui |
| 4 | Substitutions autorisées | vélo, natation, aqua-jogging, renforcement | oui |
| + | Date de réévaluation | date, ou « non fixée » | oui — voir péremption |

Motif du format structuré pour 2 à 4 : un texte libre donnerait l'illusion d'être pris en
compte alors que le modèle ne peut rien en faire. Motif de la séparation volume /
intensité / dénivelé : « réduire de 50 % » ne dit pas *quoi* réduire, et un chiffre unique
appliqué aux mauvaises variables est une fausse précision — même mode d'échec que D-18 et
D-27.

**Les trois scénarios et ce que le modèle en fait :**

| Scénario | Comportement |
|---|---|
| **Course autorisée, charge réduite** | le volume cible (G-PLA-002) est multiplié par le facteur ; les drapeaux retirent les types de séance concernés du catalogue (D-29) ; la structure des phases est conservée |
| **Arrêt complet, sans substitution** | plus aucune séance prescrite. Les grandeurs cessent de recevoir des observations, leur confiance décroît (D-16), le plancher de D-15 empêche l'effondrement. Le garde-fou se rejoue (D-19) et **ajuste la cible** : date projetée reculée (D-26) ou cible dégradée (D-20) |
| **Substitution autorisée** | séances de vélo, natation, aqua-jogging ou renforcement prescrites **en durée et en effort ressenti uniquement**, jamais en contenu structuré — aucun modèle n'existe pour ces disciplines (D-31, D-08). Objectif affiché : maintenir la capacité aérobie, pas entraîner la discipline. Pour un arrêt prolongé, l'aqua-jogging a les meilleures preuves de maintien (S-CHA-003 et trou « adaptation croisée ») |

**Extension assumée de D-31** : hors blessure, vélo et natation sont purement déclaratifs
et jamais prescrits. En mode blessure, ils le sont — mais sans contenu, ce qui reste
cohérent avec l'absence de grandeur pour ces disciplines.

**Péremption des contraintes médicales.** Passée la date de réévaluation, le modèle **ne
prolonge pas** l'autorisation : il retombe sur l'état le plus conservateur et redemande un
avis. Sans date fixée, une échéance par défaut s'applique. Motif : une contrainte saisie
six semaines plus tôt continuerait sinon d'autoriser la course sans que rien n'ait été
réévalué — c'est la logique de D-16 appliquée à une saisie médicale. **Sans cette règle,
l'app devient un intermédiaire médical qui prolonge indéfiniment une autorisation
périmée.**

**Journal** : toutes les saisies (séances réalisées, substitutions, symptômes, évolution
du niveau) sont consignées et **exportables**, pour que le coureur puisse restituer
plusieurs semaines de ressenti lors de la consultation suivante. C'est un usage à part
entière du module, pas un sous-produit.

**Changement d'état visible dans l'interface.** L'app affiche clairement qu'elle est en
mode blessure, et **montre l'horizon ajusté, jamais le plan d'origine**. Ce n'est pas
cosmétique : un plan inchangé affiché pendant une blessure pousse à revenir trop tôt, et
un plan dégradé qui ressemble à un plan normal se lit comme une autorisation.

**Frontière absolue** : l'app adapte la charge, exécute les restrictions déclarées et
oriente vers un professionnel. Elle ne nomme aucune pathologie, ne propose aucun protocole
de rééducation, n'estime aucun délai de guérison, et **ne décide jamais si le coureur peut
courir**. 17/09/2026

**D-51 — Remontée progressive : déclarative, à confirmation positive, jamais datée.**
S'applique à la sortie de D-50, quand la course redevient autorisée.

**Structure** : progression marche-course graduée — alterner marche et fractions courues,
allonger progressivement les fractions jusqu'à la course continue facile → S-BLE-003.
**Fréquence avant intensité, durée avant vitesse.** Au plus 3 sorties par semaine, jamais
deux jours consécutifs en début de remontée.

**Ce que l'app mesure, et ce qu'elle ne mesure pas.** Aucun capteur ne détecte une
douleur : le pilotage est **entièrement déclaratif**, et c'est écrit plutôt que maquillé
en mesure. Trois moments de déclaration seulement, pas un suivi quotidien : à
l'échauffement, pendant la séance, **le lendemain matin** — ce dernier critère vient
directement de S-BLE-001, déjà employé par D-32.

**Correction du 17/09/2026** : une première version prévoyait un suivi quotidien. Mal
calibré dans les deux sens — 7 saisies par semaine pour 3 séances, et à côté du besoin,
puisque la progression se décide par séance et non par jour.

| Symptôme déclaré | Conséquence |
|---|---|
| Pendant l'échauffement | 2 jours d'arrêt, retour au palier précédent |
| Pendant la séance | 1 jour d'arrêt, retour au palier précédent |
| Après la séance ou le lendemain | rester au même palier |
| Aucun, confirmé | passer au palier suivant |

**Confirmation positive obligatoire** : la progression exige une déclaration explicite
d'absence de symptôme. Pas de saisie, pas de passage au palier suivant — on reste où on
est. Le mode d'échec d'une donnée manquante est donc **conservateur**, ce qui rend la
saisie facultative sans danger — même mécanisme que G-NUT-001.

**Fin de la remontée** : retour à l'entraînement normal quand **75 à 80 % du volume
hebdomadaire d'avant blessure** est atteint sans symptôme pendant **2 à 3 semaines
consécutives**. Ce seuil est mesuré objectivement par le GPS, sans déclaration. Ensuite,
progression de 10 à 30 % par semaine, bornée par la règle des 30 jours (D-63c ; renvoi
corrigé le 23/09/2026, D-22b n'existe plus).

**Aucun délai fixé par le modèle.** Les écarts selon le tissu sont considérables (10-14
jours pour une lésion musculaire mineure, 6-8 semaines ou plus pour une fracture de
fatigue). Le professionnel tranche via D-50 ; le modèle n'estime rien.

**Les séances de remontée ne calibrent aucune grandeur** : allures et segments y sont
atypiques, les inclure fausserait G-CAP-001 et G-TER-001. Elles comptent en charge
(G-CHG-001) et dans le journal de D-50. La calibration reprend à la fin de la remontée.

**Niveau : faible** → S-BLE-003. Le principe marche-course et les règles de symptôme sont
solides, mais **les protocoles chiffrés relèvent du consensus clinique, pas d'essais
contrôlés**. Les paliers sont des points de départ, pas des garanties. 17/09/2026


**D-52 — Corrections issues du premier déroulé de cas limites (TESTS.md, 17/09/2026).**
**Entrée d'historique** : son contenu normatif a été **propagé le 20/09/2026** dans D-19 (garde-fou) — cette destination fait foi. Conservée pour la traçabilité des corrections, jamais réattribuée.
Trois défauts sérieux, invisibles pour tout contrôle de cohérence interne : chaque
décision impliquée était correcte isolément, c'est leur composition sur un cas concret
qui échouait.

**(a) Le garde-fou ne teste plus un ratio seul (T-01).** Le critère « volume requis >
2,5 × volume actuel » est indéfini à volume nul et explosif à volume faible : il refusait
**tout débutant**, et les deux sorties de D-20 n'y pouvaient rien — repousser la date ne
fait pas monter un volume qui reste nul tant qu'on ne s'entraîne pas. Remplacé par un
test de **temps de progression nécessaire** : partant du volume actuel, avec la
progression de G-PLA-002 (D-56a ; renvoi corrigé le 23/09/2026, D-22b n'existe plus), combien de semaines faut-il pour atteindre le
volume de bloc requis ? Comparé aux semaines réellement disponibles. Le ratio disparaît,
un volume nul devient un cas ordinaire, et le test devient interprétable (« il te faut
18 semaines de montée, tu en as 26 »). Le seuil de 2,5 × est **abandonné**.

**(b) Le garde-fou teste aussi la faisabilité de la semaine (T-02).** Il ne comparait le
volume requis qu'au **passé** du coureur, jamais à ce que sa semaine **permet** :
volume réalisable ≈ jours de course disponibles (D-38) × durée maximale plausible d'une
séance, à raison d'une séance de course par jour (D-35). Un coureur à 2 jours disponibles
passait au vert puis recevait un gabarit à 2 h 30–3 h 30 par séance. A-05 faisait bien
céder le volume devant la disponibilité, mais **sans que rien ne le signale**. Désormais :
si le volume réalisable est très inférieur au volume de bloc requis, niveau **orange** —
le plan reste généré, la limite est nommée, et les sorties de D-20 s'appliquent.

**(c) Le rouge en cours de préparation est défini (T-03).** D-19 définissait le rouge
comme « refus », ce qui n'a aucun sens quand le plan existe déjà — cas d'une blessure
(D-50) ou d'un retard accumulé. Le rouge **en cours** ne refuse rien : il **dégrade la
cible et le dit**. Le modèle propose les deux sorties de D-20 (même course plus tard,
même date avec cible réduite) et, quand aucune des deux ne ramène à l'orange, **l'écrit
explicitement** : la cible n'est plus atteignable dans des conditions raisonnables. Il
n'interdit pas de prendre le départ — ce n'est pas son rôle — mais il cesse d'afficher
une estimation de performance qui entretiendrait l'illusion.

**(d) Deux corrections mineures.** Un blocage de remontée (D-51) faute de déclaration
doit être **affiché comme tel** (« en attente de ta confirmation d'absence de symptôme »)
et non rester silencieux, sans quoi il ressemble à une panne (T-05). Et la désactivation
du module nutrition (D-30) affiche une information unique au moment du geste pour les
cibles de plus de 4 h, comme le fait déjà D-31 pour le renforcement — l'asymétrie
n'était pas justifiée (T-06). 17/09/2026


**D-53 — Corrections issues de la simulation sur 52 semaines (TESTS.md, `sim.py`,
17/09/2026).**
**Entrée d'historique** : son contenu normatif a été **propagé le 20/09/2026** dans G-TER-001 (bornes), G-FAT-001 et D-54 — ces destinations font foi. Conservée pour la traçabilité des corrections, jamais réattribuée. Premier contrôle **dynamique** du modèle : des coureurs synthétiques dont
la vérité est connue vivent une année, et on vérifie que le modèle la retrouve.

**Validation principale** : le modèle retrouve un coût-pente individuel qu'on lui avait
caché — erreur moyenne **0,3 %** après 52 semaines, contre **9,6 %** pour la courbe
générique seule. La conception est saine ; ce qui suit corrige des défauts de garde-fou,
pas de principe.

**(a) Le coût-pente est normalisé sur le plat, et cela doit être écrit.** G-TER-001 ne
mesure qu'un **rapport à l'allure du coureur sur le plat** — et c'est la grandeur utile
pour prescrire. L'écart individuel *au plat* appartient à G-CAP-001, pas à G-TER-001 : les
deux grandeurs ne sont séparables qu'à cette condition. Une première évaluation
comparait l'estimation à une vérité exprimée en absolu et concluait à tort que le modèle
n'apportait rien.

**(b) La boucle allure/prescription diverge : il faut une borne dure.** Simulée sur un
coureur qui lève volontairement le pied de 15 % en montée, l'estimation de la bande
montée forte tombe de 0,432 (semaine 1) à **0,106** (semaine 52), contre 0,449 de
physiologie réelle — le modèle finirait par prescrire des montées **quatre fois trop
lentes**. La dérive est multiplicative à chaque cycle : elle ne se stabilise pas.
L'atténuation prévue par H-02 (calibrer sur les segments à haute intensité) réduit
l'ampleur sans supprimer le mécanisme. **Bornes ajoutées, puis corrigées après test** :

(i) **Écart borné au générique, borne élargie par la confiance** — ±30 % à confiance
nulle, jusqu'à ±60 % à confiance pleine. Une bande peu observée reste tenue près du
prior ; une bande bien observée gagne le droit de s'en écarter. **Corrigé le 17/09/2026
après le jeu de généralisation** : une borne fixe à ±30 % **écrasait un coureur
réellement atypique** (déviation ±35 %, erreur portée de 0,3 % à 1,6 %) — elle punissait
la variabilité individuelle qu'on cherche justement à capter (S-TRA-001).
**Compromis assumé** : la contention de la divergence se dégrade (stabilisation à 0,180
au lieu de 0,315, contre 0,449 de physiologie). Toute borne assez serrée pour bien
contenir la divergence écrase les atypiques, qui sont le **cas fréquent**, alors que la
divergence suppose un comportement pathologique persistant. On protège le cas fréquent,
on contient sans prétendre corriger, et **on signale**.

(ii) **Gel sur dérive monotone, conditionné à une convergence préalable** — une dérive
d'une bande dans le même sens sur plusieurs cycles successifs gèle sa calibration, avec
signalement : une vraie adaptation physiologique ne dérive pas indéfiniment dans le même
sens.

**Correction du 17/09/2026, issue du test de la correction elle-même.** La première
version de (ii) ne conditionnait pas le gel à une convergence préalable. Testée, elle
arrêtait bien la divergence (estimation stable à 0,432) mais **dégradait le coureur
sain : erreur portée de 0,3 % à 8,1 %** — le gel se déclenchait aussi sur une estimation
qui dérivait **vers** la vérité pendant ses premières semaines de calibration, que rien
ne distinguait d'une divergence. Conditionner le gel à une convergence déjà atteinte
(D-49a) résout les deux : divergence stoppée à 0,315 au lieu de 0,106, et **coureur sain
inchangé à 0,3 %**. Une dérive qui reprend après stabilisation est suspecte ; une dérive
initiale ne l'est pas.

**Le phénomène n'est pas propre à la montée** — ajouté le 17/09/2026 : testé sur un
coureur qui freine de 20 % en descente par appréhension, le modèle estime 0,828 contre
1,035 de physiologie réelle. Il est **symétrique**, concerne toutes les bandes, et est
même plus probable en descente, où l'appréhension est fréquente.

**Limite honnête** : les bornes contiennent la divergence, elles ne la corrigent pas.
L'estimation reste à 0,315 contre 0,382 d'allure réellement produite et 0,449 de
physiologie. Le modèle cesse de s'effondrer, il ne devient pas juste. **Niveau :
extrapolation** pour les deux bornes et leurs valeurs.

**(c) Convergence n'est pas justesse, et l'affichage doit les distinguer.** La
simulation montre une estimation **déclarée convergée sur les cinq bandes alors qu'elle
était encore fausse**. D-49a mesure la stabilité, jamais l'exactitude — c'est exactement
l'asymétrie de H-03 : « confiant et faux » ne coûte rien au modèle, seulement au coureur.
La confiance affichée doit donc se lire « le modèle ne change plus d'avis », **jamais**
« le modèle a raison ». À reprendre dans le lexique et dans D-42.

**(d) La pondération de H-01 est confirmée par la mesure.** Le filtre binaire initial ne
calibrait **jamais** la descente forte — confiance nulle après un an de trail en
montagne — et laissait 5,0 % d'erreur moyenne contre 0,3 % pour la pondération. La
correction n'était pas un raffinement mais une nécessité. 17/09/2026


**D-54 — Pas de prescription d'allure sur les bandes en pente ; repère à l'effort.**
Coupe la boucle de H-02 **à la sortie** plutôt que de la contenir à l'entrée (D-53b).

| Bande | Prescription |
|---|---|
| Plat et pentes douces | plage d'allure (D-42), inchangé |
| Montée, descente, marche | **durée et effort uniquement**, jamais d'allure ni de VAM cible |

Motif : la divergence n'existe que parce qu'une allure en pente est prescrite à partir de
l'estimation, puis réobservée. Sans prescription, la boucle n'a plus de véhicule. Aucune
perte réelle : personne ne court une côte au chronomètre, et une allure cible n'a pas de
sens sur un terrain dont la pente varie en permanence. **Une cible de VAM est exclue au
même titre** — elle recréerait exactement la même boucle dans une autre unité.

**Le coût-pente reste calculé et utilisé** — %VC, composition du temps de course, plan de
course — mais **il ne ressort jamais en consigne d'allure quotidienne**. Règle à retenir :
il sert à **prédire**, jamais à **dicter**.

**Repère d'effort en côte** : consigne simple (« reste facile, tu dois pouvoir tenir ça
longtemps »). La FC est écartée : à effort constant en côte prolongée elle dérive vers le
haut, et un plafond strict obligerait à marcher presque toutes les montées — du
sous-entraînement déguisé en prudence. **Aide optionnelle** : le rythme respiratoire
rapporté à la foulée (3 pas/3 pas en endurance, 2/2 en limite haute, 2/1 au-dessus), la
fréquence respiratoire étant un marqueur validé de l'effort → S-COU-012. La
correspondance personnelle **émerge des séances au plat**, où l'allure est déjà
prescrite — **aucune séance de test**, proposition écartée le 17/09/2026 : compter ses
pas à chaque montée est irréaliste, et un protocole d'étalonnage respiratoire serait une
contrainte pour un gain marginal. 17/09/2026

**D-55 — Séance étalon : optionnelle, jamais appelée un test.** Complète la détection
opportuniste de G-TER-002 sans la remplacer — l'opportuniste est gratuite et universelle
mais irrégulière ; l'étalon est régulier au prix d'une contrainte.

- **Même consigne que d'habitude** : une séance d'endurance ordinaire, seul le tracé est
  fixé. **Ne jamais la présenter comme une évaluation** — une séance perçue comme un test
  est courue plus vite, ce qui la rend incomparable aux précédentes et ajoute une séance
  dure non prévue à la charge. C'est le piège principal.
- **Toujours au même point du cycle de charge** (D-57b) : comparer une troisième
  semaine de bloc à une sortie de semaine allégée comparerait surtout deux états de
  fraîcheur.
- **Un segment, pas un parcours** : une montée de 15-20 minutes suffit.
- **Cadence** : toutes les 4 à 6 semaines, ce qui tombe naturellement avec le cycle.
- **Coût réel nul** : c'est une séance d'endurance qui aurait eu lieu de toute façon,
  placée sur un tracé imposé. **Proposée, jamais imposée** — un coureur qui la refuse
  garde la détection opportuniste. **Niveau : extrapolation.** 17/09/2026


**D-56 — Corrections issues de la simulation de la boucle de charge (TESTS.md,
`sim3.py`, 17/09/2026).**
**Entrée d'historique** : son contenu normatif a été **propagé le 20/09/2026** dans G-PLA-002 (pas absolu, mémoire du niveau) et D-57b — ces destinations font foi. Conservée pour la traçabilité des corrections, jamais réattribuée. Premier passage de G-PLA-002, G-PLA-001, du garde-fou et de la
séquence blessure dans le temps.

**(a) La progression de volume est le maximum d'un pas multiplicatif et d'un pas
absolu.** D-52a avait remplacé le ratio par un « temps de progression nécessaire » pour
régler le cas du débutant ; une progression purement multiplicative partant de **zéro
reste à zéro** — le même cas échouait autrement. Un pas absolu (de l'ordre de 0,5 h par
semaine) le débloque : 11 semaines depuis zéro pour atteindre 7 h.

**(b) G-PLA-002 garde en mémoire le dernier niveau ayant déclenché un symptôme, et
freine à son approche.** Sans cela, le volume ne reculait qu'**après** l'apparition des
symptômes puis remontait au plein plafond jusqu'à les redéclencher : il se stabilisait
**au-dessus** de la tolérance réelle (+9 à +21 %) avec des variations de 12 à 38 % d'une
semaine à l'autre. Le modèle aurait prescrit en permanence un peu trop, et de façon
erratique. Après correction : dépassement de −3 à +9 %, oscillation de 1 à 18 %.
**Niveau : extrapolation.**

**(c) G-PLA-001 échoue à son critère d'admission — à arbitrer.** La simulation montre que
la cadence de relâche **ne distingue pas** un coureur fragile d'un coureur solide (4,5
contre 4,0 semaines). Cause : G-PLA-001 et G-PLA-002 lisent **les trois mêmes signaux**,
et le volume les absorbe en premier ; une fois le volume ajusté, le coureur fragile
encaisse aussi bien que le solide. Physiologiquement logique, mais l'observation
correctrice de G-PLA-001 **ne corrige rien en pratique** — or c'était précisément ce qui
la rendait admissible plutôt que générique (case 3). **Deux issues** : fusionner
G-PLA-001 dans G-PLA-002, ou lui trouver un signal propre que le volume n'absorbe pas.
**Non tranché.**

**(d) La séquence blessure passe.** Arrêt de 6 semaines depuis 7,8 h : retour à 77,5 %
atteint en 10 semaines, progression dans la fourchette de S-BLE-003. Sans déclaration
d'absence de symptôme, le volume reste bloqué — confirmation positive conforme à D-51.
17/09/2026


**D-57 — Trois simplifications issues de la simulation de charge et de la revue de
dépendances (17/09/2026).**
**Entrée d'historique** : son contenu normatif a été **propagé le 20/09/2026** dans G-FAT-001 et G-PLA-002 ; les points (b) et (c) restent ici, sans autre hôte — ces destinations font foi. Conservée pour la traçabilité des corrections, jamais réattribuée. Le modèle devient **plus simple** qu'avant : une grandeur en
moins, une dépendance en moins.

**(a) G-FAT-001 ne passe plus par le %VC.** Elle mesure la perte d'**allure brute** à
terrain égal **à l'intérieur d'une même sortie**. Une première rédaction exigeait des
parcours répétés ou un terrain homogène — corrigée le 17/09/2026 : inutilement
restrictive (20-30 % des sorties contre 94 %) et confondant le besoin de G-FAT-001 (début
contre fin d'une même sortie) avec celui de G-TER-002 (même segment à deux dates). Elle
héritait sinon du biais de G-TER-001 (H-02) sans que ce soit écrit, et aucun test ne
l'avait éprouvée sur terrain hétérogène. Sur 10 grandeurs, la chaîne de dépendances passe
de 3 maillons à 2.

**(b) [abandonnée] G-PLA-001 — cadence de relâche.** Supprimée comme grandeur le
17/09/2026, après D-56c. Motif : la simulation montre qu'elle **ne discrimine pas** un
coureur fragile d'un coureur solide (4,5 contre 4,0 semaines), parce que G-PLA-002 absorbe
les trois mêmes signaux en premier — une fois le volume ajusté, chacun encaisse sa propre
charge aussi bien. Son observation correctrice ne corrigeait donc rien : elle échouait à
son propre critère d'admission.
**Une version objective a été envisagée puis écartée** : comparer le %VC d'une séance
48 h après une sortie longue au niveau habituel. Elle suppose qu'une séance tombe dans
cette fenêtre, et l'écart est noyé dans le bruit ordinaire (sommeil, météo, journée de
travail) — une grandeur qui convergerait en un an pour piloter un paramètre jugé
acceptable tel quel. Mauvais rapport.
**Remplacée par une règle fixe assumée : 3 semaines de charge pour 1 allégée**, bornée 2
à 4. Convention de coaching largement acceptée, sans source (trou déjà inscrit dans
SOURCES.md). **Recalée le 22/09/2026 (D-63f)** : la grille part de l'affûtage, à rebours
(T−4, T−8…) ; la règle 3:1 est inchangée, seul son point de départ change.

**(c) Relâche à la demande.** Le coureur peut demander une semaine allégée — fatigue
ressentie, contrainte à venir. Ce n'est **pas une auto-évaluation** mais une décision, donc
aucun problème de fiabilité déclarative. Trois règles :
- elle **décale le cycle** au lieu de s'y ajouter : le compteur repart à zéro, sinon une
  seconde relâche tomberait la semaine suivante ;
- elle se **distingue de l'indisponibilité** (D-46) : ici le coureur *pourrait*
  s'entraîner mais choisit d'alléger. Une indisponibilité **totale** satisfait le besoin
  de relâche — inutile d'en programmer une juste après — mais **n'y est pas équivalente** :
  une semaine allégée est de la récupération *active* à ~60 % du volume, une semaine à
  zéro est une interruption, à laquelle la péremption de D-16 s'applique ;
- **trois demandes anticipées sur des cycles successifs deviennent un quatrième signal
  pour G-PLA-002** — non pas sur la cadence, mais sur le **volume**, jugé trop élevé.
  C'est un comportement, pas une auto-évaluation.

**(d) Séances non réalisées : ne pas demander pourquoi.** Une question sur le motif
produirait du déclaratif peu fiable — personne n'écrit « j'étais cuit », on écrit « pas eu
le temps ». Inutile de la poser : la **relâche à la demande** sépare déjà les deux cas
(le fatigué demande une relâche, l'occupé saute une séance et continue), et D-46 couvre
les périodes chargées connues à l'avance. Règle : **une séance sautée ne fait baisser le
volume que si elle se répète**, jamais au premier incident. 17/09/2026

**D-58 — Segment doublé sur sortie longue : recommandation, jamais prescription.**
Le coureur est invité à repasser par un **même segment au début et à la fin** de sa sortie
longue : même segment, même jour, même météo — seule la fatigue a changé. Mesure de
durabilité la plus propre possible sans laboratoire, et elle alimente **G-FAT-001 et
G-TER-002 d'un coup**.

**Recommandation et non prescription** : le coureur connaît son terrain, le modèle non —
il ignore quelle montée se trouve à dix minutes de chez lui. Il place, le modèle détecte.
Variante **optionnelle** de la séance étalon (D-55) : elle suppose une montée accessible
deux fois dans une boucle, ou un aller-retour, ce qui ne convient pas à tous les terrains.

**Rappel de D-55 applicable ici** : l'étalon se place **toujours au même moment du cycle
de charge**, sans quoi on mesure la fraîcheur et non l'adaptation. Une vraie progression
de durabilité se compte en **mois** : un écart de plusieurs points en trois semaines
signale une différence de fraîcheur, pas une adaptation. 17/09/2026

**D-59 — Restitution au coureur : deux niveaux, hebdomadaire, en constats.** Miroir de
A-16 (« pourquoi cette séance ») : ce que le modèle a lu dans les séances passées.

**Niveau 1 — pourquoi cette séance** : motif (D-29), place dans la phase, contraintes
ayant cédé (A-05). Déjà exigé par A-16.

**Niveau 2 — bilan hebdomadaire** : constats factuels sur la semaine écoulée, puis **une
décision à prendre** pour la suivante. Hebdomadaire et **non par séance** : un chiffre qui
bouge de 2 % d'une séance à l'autre invite à y chercher un sens qu'il n'a pas, et « pas
encore assez de données » répété quarante fois décourage.

**Quatre règles de rédaction, chacune issue d'un risque identifié :**

(a) **Des constats, jamais des jugements comparatifs.** « Tu as perdu 8 % sur la fin » et
non « ton coût en montée est élevé pour ton niveau ». Motif : afficher une estimation peut
recréer par l'information la boucle que D-54 a fermée par la prescription — informé que
son coût en montée est élevé, le coureur pousse en montée, et la mesure suit. **A-02 ne
couvre pas ce cas** (voir sa limite). Détection possible via G-TER-002, qui verrait un
changement de comportement sur le segment habituel.

(b) **Jamais les valeurs des coefficients.** « Ta montée forte est calibrée » est neutre ;
« ton coût en montée est de 0,42 » relance le mécanisme de (a).

(c) **Seulement ce dont la confiance le permet.** Afficher une décroissance-fatigue après
trois semaines, alors qu'elle demande 3-4 mois, c'est montrer du bruit — le coureur verra
le chiffre sauter et cessera d'y croire, à juste titre.

(d) **Expliquer les conclusions, jamais les critères d'admission.** Savoir que la
calibration se fait sur les segments réguliers conduit à courir plus régulièrement ; savoir
que les sorties clés pèsent davantage conduit à les soigner. Une mesure qui devient une
cible cesse d'être une bonne mesure. **Limite assumée à la transparence.**

**Veto « séance non représentative » — restreint aux faits vérifiables.** Le coureur peut
**invalider une observation**, jamais corriger un coefficient (extension du veto de
G-RES-001a). Motifs admis : arrêts répétés, couru avec plus lent que soi, neige ou boue,
matériel inhabituel. **Motifs refusés : l'état du coureur** (« je me sentais mal »,
« j'étais fatigué »).
Motif du refus, identifié au second passage d'analyse : un veto ouvert a un **biais de
remplissage asymétrique** — on signale une séance ratée, jamais une séance où l'on avait
le vent dans le dos. On retirerait donc systématiquement les mauvaises séances en gardant
les bonnes, et **le modèle surestimerait le coureur** sans que rien ne l'indique. Même
mécanisme que celui qui a fait écarter le RPE par bloc (D-03). Et une séance difficile
parce que le coureur était fatigué est **précisément le signal qu'on veut garder**.
17/09/2026

**D-60 — Ce que l'app met en avant, par ordre d'importance.** Décidé en écartant
l'approche « chercher le facteur le plus motivant », jugée fausse pour trois raisons : la
progression est **plate** la plupart du temps (fond d'hiver, plateaux, semaines allégées)
et **recule** après une coupure, donc une app qui repose dessus décourage quand on en a le
plus besoin ; célébrer les gains de vitesse **pousse contre le modèle**, qui prescrit plus
de 80 % du volume en endurance fondamentale (D-34) ; et la rétention vient de l'**utilité**
— une app qu'on ouvre parce qu'on a besoin d'une réponse est utilisée, une app qu'on
consulte quand on en a envie est abandonnée.

| Rang | Ce qui est mis en avant | Pourquoi |
|---|---|---|
| 1 | **La séance du jour et son motif** (D-29) | c'est ce qui crée l'usage quotidien |
| 2 | **L'avancement vers la cible** — « il te reste 18 semaines, tu es dans les clous » | survit aux plateaux, et a un horizon daté (D-26) |
| 3 | **La progression** (G-TER-002), montrée **quand elle existe** | puissante, mais jamais comme métrique permanente — une notification quand la montée habituelle s'améliore vaut mieux qu'un graphique qu'on consulte en espérant |
| 4 | **La constance** — semaines conformes au plan | progresse même quand la performance stagne, et c'est ce que le coureur contrôle |

**Garde-fou** : ce qui est mis en avant doit être ce que l'entraînement **veut** voir
faire. On valorise la régularité et le volume tenu, **jamais la vitesse** — sinon l'app
pousse contre son propre modèle.

**État de calibration : par brique, jamais un chiffre global.** Un pourcentage unique
mélangerait des grandeurs sans rapport (vitesse de référence fiable en 6 semaines,
décroissance-fatigue en 3-4 mois, descente raide peut-être jamais) et masquerait
l'information utile : **quelle** brique manque et **ce qui la débloque**. Il reculerait
en outre après une coupure (D-16), sans explication.
Présentation : une brique manquante est un **usage indisponible** (« pas encore
d'estimation sur ce terrain »), jamais un **trou à combler** — sinon compléter le modèle
devient un jeu et le coureur va chercher du dénivelé raide pour remplir une case plutôt
que parce que sa préparation le demande. L'état se **consulte**, il ne s'affiche pas en
permanence. 17/09/2026

**D-61 — Corrections et allègements issus de la simulation complète sur huit profils
(TESTS.md jeu 6, ALLEGEMENT.md, 20/09/2026).**

**(a) Le volume restait bloqué 43 % sous la tolérance réelle — corrigé.** Deux causes, de
la même famille : **une observation unique décidait de tout**. La référence de ressenti
de G-PLA-002 était figée sur la **première semaine**, bruitée — si elle tombait bas,
toutes les suivantes ressemblaient à une dérive et la progression restait bloquée dans
une zone morte permanente. Corrigé par la **médiane des quatre premières semaines**. **Complété le 22/09/2026 (D-63k4)** : la référence se recale
ensuite sur les semaines allégées (état reposé), avec un plafond de +5 % et le réexamen
des alertes dues au seul calage. Et
le niveau ayant déclenché un symptôme verrouillait la progression à vie ; le desserrage
périodique le rend réversible. C'est la règle « une sortie ne dit rien », appliquée
partout ailleurs et jamais ici.

**(b) L'oscillation du volume venait d'une remontée trop brutale — corrigée.** Après
chaque recul, le modèle repartait au plein cap. Recul adouci de −12 % à −8 %, progression
plafonnée à la moitié du cap une fois la limite connue. Résultats sur huit profils :
écart moyen de 14,9 % à **7,6 %**, oscillation de 17,9 % à **14,6 %**.
**Requalifié le 22/09/2026** (TESTS.md, huitième série) : 7,6 % est un chiffre de petit
échantillon (n = 8) ; sur 1 600 tirages, l'écart moyen est de **11,3 %** (médiane 8,9 %).
Même phénomène que D-61g pour l'oscillation. Aucune correction de code.

**(c) Une correction intermédiaire a empiré les choses, et c'est consigné.** Exiger
**deux** symptômes avant de mémoriser un niveau a porté l'oscillation de 18 % à **43 %** —
le modèle dépassait bien plus avant de freiner. Retour à la mémorisation au premier
symptôme, le risque de verrouillage étant traité par le desserrage et non par la
confirmation.

**(d) Un lissage du volume prescrit a été testé puis écarté.** Gain de 2,8 points
d'oscillation et **dégradation** de la justesse ; (b) fait mieux sans état supplémentaire.
Consigné pour ne pas être reproposé.

**(e) Un seul mécanisme de régularité au lieu de deux (A2).** D-49b définissait un filtre
binaire et H-01 une pondération, sur le même critère. La pondération fait mieux partout
(0,3 % contre 5,0 % d'erreur, et le filtre binaire ne calibre **jamais** la descente
forte). **Mécanisme unique : la pondération.** La FC devient un cas particulier exigeant
une pondération au-dessus d'un plancher élevé.

**(f) Le gel sur dérive monotone (D-53b-ii) rétrogradé en filet.** Déclenché **0 fois**
sur 8 profils × 5 bandes. Il protégeait de la boucle de H-02, que **D-54 a supprimée à la
source**. Conservé uniquement contre la voie d'information ouverte par D-59 ; il sortira
si cette voie est fermée autrement.

**(g) Point faible résiduel, non résolu** : le profil « très expérimenté ultra » conserve
**34,5 % d'oscillation** de volume, seul cas au-dessus de 17 %. Non expliqué à ce stade.

**Requalifié le 21/09/2026** (TESTS.md, septième série) : n'est pas un point faible du
profil ultra. Preuve par invariance d'échelle — même graine, oscillation identique
(34,5 %) de 4,5 h à 15 h de tolérance — et par distribution sur 1 600 simulations
(200 graines × 8 profils) : le 34,5 % se situe au **99,5ᵉ percentile** d'une distribution
partagée par tous les profils (médiane 10,5 %, moyenne 12,3 % — à comparer à la moyenne
14,6 % de l'échantillon d'origine, n=8, un peu haute par petit échantillon). Probabilité
d'un vrai va-et-vient (≥2 changements de sens) au-delà de 25 % d'oscillation : **0,7 %**,
uniforme sur tous les profils. Aucune correction de code : variance de bruit rare et non
catégorielle, pas un défaut du profil.

**(h) Séances de repère : D-55 et D-58 fusionnées.** Même objet — un repère volontaire
placé par le coureur, mêmes règles. Deux variantes : segment répété (alimente G-TER-002)
et segment doublé début/fin de sortie longue (alimente aussi G-FAT-001). Une décision de
moins, aucune règle perdue. 20/09/2026

**D-62 — Tentative de contrôleur continu (PI, puis hybride) pour G-PLA-002 — écartée.**
Suite à D-61g (avant sa requalification). Calibration par grille (600 puis 900+
combinaisons, balayage synthétique + validation sur les 8 profils du jeu 5) d'un
contrôleur proportionnel-intégral remplaçant les paliers actuels par un ajustement
continu. Aucune configuration ne bat la référence (écart 7,6 %, oscillation 14,6 %) sur
l'ensemble des profils — au mieux un compromis qui répare un profil en en dégradant un
autre. Un contrôleur hybride (ajustement continu + mémoire du seuil cassé, pour
retrouver l'ingrédient qui manquait au PI pur) nécessite 9 paramètres contre ~6 au
mécanisme actuel, pour un résultat qui ne le dépasse toujours pas. **Écarté au nom de
R-MET-002** : pas de complexité sans preuve d'insuffisance de la solution simple — et
l'insuffisance supposée (D-61g) s'est révélée être un artefact de mesure, pas un défaut
réel. Ki n'apporte aucun gain sur toute la grille testée : la fatigue du coureur
s'accumule déjà comme un intégrateur (D-33/D-56), en ajouter un second déstabilise plutôt
qu'il ne corrige — à ne pas retenter sans nouvelle piste. → TESTS.md, septième série.
21/09/2026

> **Amendé le 28/09/2026 par D-67 et D-70.** Le bloc gèle le volume visé (et non le volume placé) ; le contrôleur G-PLA-002 ne pilote plus que les séances autres que la sortie longue ; la cible de sortie longue d'un objectif secondaire n'est plus l'échéance de D-63 mais 50 % de sa durée, 4 h 30 au plus (D-70).

**D-63 — Articulation de G-PLA-002 avec le calendrier de blocs (TESTS.md huitième série,
`sim6.py`, 22/09/2026).** Referme le trou « Progression de charge d'un bloc à l'autre »
(priorisé le 21/09/2026). **Traçabilité** : une première version de ce travail (nuit du 21
au 22/09/2026) a été perdue avant livraison, simulateur compris. `sim6.py` a été
reconstruit et relancé ; **les chiffres ci-dessous sont ceux de la reconstruction** (7
profils × 500 tirages, préparation tirée entre 30 et 36 semaines ; 15 scénarios
défavorables × 200 tirages). Deux affirmations de la première version ne sont pas
reproduites, signalées en (d) et (h).

**(a) Le volume ne dépend pas de la phase ; ce qui monte en bloc spécifique, c'est la
spécificité.** Chez les coureurs de fond entraînés, le volume est semblable en préparation
et en pré-compétition, et ne baisse qu'en compétition → S-CHA-004 ; ce qui augmente à
l'approche de l'objectif, c'est le volume couru à allure de course → S-COU-013 ; même
tendance décrite en ultra-trail (sorties plus vallonnées, plus longues, plus de marche)
→ S-TRA-006 ; aucun modèle de périodisation ne s'est montré supérieur → S-CHA-005.
G-PLA-002 continue donc de piloter le volume en bloc spécifique ; les valeurs de D-21
restent des repères. **Variante écartée** : un plafond de fond à 85 % du pic — il n'agit
qu'au-delà de ~8,5 h/semaine (85 % de 10 h), sur les coureurs qui n'en ont pas besoin.
**Niveau : faible** (populations élites, route et piste ; un seul cas en ultra-trail).

**(b) Pas de plancher de volume à l'entrée du bloc spécifique.** Le volume moyen du bloc
passe sous celui des 4 dernières semaines de fond dans 12 à 48 % des plans selon le profil
(13 à 37 % avant D-63). Cause : les reculs de sécurité de G-PLA-002 après symptôme, et la
consolidation (g). Un plancher passerait outre un signal de fatigue, que A-05 place
au-dessus du volume cible.

**(c) Règle des 30 jours — remplace D-22b.** Aucune séance ne dépasse de plus de 10 % la
plus longue séance des 30 jours précédents, **courses comprises** dans cet historique.
Le risque de blessure de surmenage augmente dès qu'une séance dépasse de plus de 10 % la
plus longue des 30 derniers jours, alors que la hausse de volume d'une semaine à l'autre
n'y est pas associée → S-BLE-004. **Plancher** : une séance de 30 min ou moins est
toujours permise — sans lui, un coureur sans historique ne pourrait jamais démarrer.
Résultat : 3,1 à 6,4 dépassements par préparation avant, **0 après**, sur les 7 profils
et les 15 scénarios. D-22b (+20 % d'une sortie longue à la suivante) laissait passer ces
dépassements et, combinée aux semaines allégées, faisait repartir la sortie longue de bas
après chacune (ex. 2h08, 1h23 allégée, 1h40, 2h00, 2h22 : les sorties clés devenaient
inatteignables). **Niveau : modéré** pour la règle en distance (cohorte de 5 205 coureurs,
observationnelle) ; **extrapolation** pour sa transposition à la durée et au trail, et
pour le plancher de 30 min (HYPOTHESES.md H-21).

**(d) La sortie longue suit sa propre progression, planifiée à rebours.** La chaîne des
+10 % doit amener la dernière sortie clé à la borne basse de D-22 (3h30 pour 4–8 h, 5 h
pour 8–20 h). La rampe démarre en fond juste à temps, **avec une semaine de marge** ;
seules les semaines de charge du fond et les sorties clés sont des occasions de
progresser ; au-delà de 3 h, une semaine sur deux (D-22a). Pendant la rampe, la sortie
longue peut monter jusqu'à la part des sorties clés (60 % en 4–8 h, 65 % en 8–20 h) : les
parts de D-22 deviennent des parts par défaut. **La sortie longue reste la plus longue
séance de la semaine** : sa part ne descend jamais sous 1/n du volume (n séances) — trou
de D-22 révélé par le simulateur : à 2 ou 3 séances, 30–35 % du volume faisait de la
« sortie longue » une séance plus courte que les autres. Les courses secondaires sont des
échéances de la même chaîne. Résultats : séances ≥ 3h20 dans le bloc, profil proche
d'Antoine **0 → 2,1** par préparation ; 0 → 0 pour les deux profils à faible volume (ils
n'atteignent pas 3h30 : c'est au garde-fou D-19 de le dire). Course secondaire faisable
(2h30 en S20) : course au-delà de +10 % dans 58 % → 17 % des plans (reste : rampe
interrompue par un symptôme). Course secondaire infaisable (3h30 en S16, depuis des
sorties de 50 min) : 100 % → 100 %, **attendu** — le garde-fou doit le signaler (D-19) et
proposer le statut inférieur (D-25, D-20). **Non reproduit** : « la plus longue sortie du
bloc n'est jamais plus courte que celle du fond » — vrai à 0–6 % près pour 6 profils,
**faux pour le coureur à 2 séances et faible volume (51 %)**, dont le volume du bloc
recule et dont la sortie clé reste plafonnée à 60 % du volume. **Niveau : extrapolation**
(marge, parts, alternance — H-26, H-27).

**(e) Affûtage : volume fixé, G-PLA-002 gelé.** Référence = médiane des 3 dernières
semaines de charge ; 65 % puis 45 % de cette référence, soit 45 % de réduction moyenne,
dans la fourchette 41–60 % → S-COU-006. Avant : l'affûtage n'existait qu'en semaines de
relâche calculées sur un volume cible encore en mouvement — 38 à 40 % de réduction, **20 %
sur une préparation de 8 semaines**. La sortie longue d'affûtage suit la part du volume
(40 % la première semaine), puis vient la course. Résultat : dans la fourchette pour
**100 %** des plans simulés. **Non testé** : affûtage de 3 semaines (tranche 8–20 h,
D-25 : 14–21 j). **Niveau : élevé** pour l'ampleur, **extrapolation** pour le découpage
65/45 (H-22).

**(f) Semaines allégées recalées à rebours depuis l'affûtage (T−4, T−8…).** Règle 3:1
inchangée (D-57b), seul son point de départ change ; au moins 2 et au plus 4 semaines de
charge entre deux allègements, borne haute levée dans le pic (l'affûtage qui suit en
tient lieu) ; une relâche avancée par un symptôme ne décale pas la grille, qui saute
seulement le point devenu trop proche. Résultat : semaine allégée dans le pic **76–85 % →
5–9 %** des plans (reste : relâches déclenchées par un symptôme). **Niveau :
extrapolation** (H-25).

**(g) Consolidation : pendant le bloc spécifique, G-PLA-002 ne sonde plus sa limite.**
Ni retest ni desserrage du seuil mémorisé ; **et si aucun seuil n'est connu à l'entrée du
bloc, le volume ne monte plus au-delà de son niveau d'entrée** (il peut toujours baisser).
Quatre variantes testées : aucune ; B, ni retest ni desserrage ; **C, B + gel si aucun
seuil connu (retenue)** ; A, gel toujours. C = B sur les 7 profils nominaux (symptômes en
bloc −0 à −29 % par rapport à « aucune », atteinte du pic −0 à −2,4 points) ; C ≫ B quand
la limite n'a pas été trouvée en fond — préparation de 16 semaines : **1,27 → 0,13
symptôme en bloc** (volume de pic de 1,13 à 0,85 de la tolérance) ; A coûte 3 à 5 points
d'atteinte partout, pour un gain nul chez les expérimentés. Motif : ne pas augmenter deux
contraintes à la fois — la spécificité monte, le volume se stabilise. **Niveau :
extrapolation** (H-24).

**(h) Reprise après interruption.** Après n semaines sans course (n ≥ 2), le volume
repart à max(65 % ; 1 − 0,07 × (n − 1)) du volume d'avant ; le seuil mémorisé est réduit
du même facteur ; **si aucun seuil n'était connu, le volume d'avant la coupure devient
seuil provisoire**, rejoint en mode freiné — même logique que le retour après blessure
(retrouver d'abord l'ancien volume → S-BLE-003). La règle des 30 jours s'applique d'elle-
même : après 30 jours sans course, seules des séances de 30 min sont permises, puis +10 %
par séance. **Corrige D-46**, qui disait la perte de forme « déjà couverte » : faux pour
le volume, G-PLA-002 ne figurant pas au tableau de D-16. Résultat, coupure de 5 semaines
en fond : symptômes en bloc **0,46 → 0,24**, sur toute la préparation **2,17 → 0,48**,
dépassements 5,8 → 0 ; coût : volume de pic à 0,86 de la tolérance contre 1,01. Coupure
de 3 semaines en bloc : 0,91 → 0,15. **Non reproduit sans le seuil provisoire** : la
première version annonçait déjà une baisse ; la reconstruction montre une **hausse**
(0,46 → 1,21) tant que le seuil n'est pas traité — le coureur reprenait doucement et ne
retrouvait sa limite qu'en bloc spécifique, au pire moment. **Niveau : extrapolation**
pour les coefficients ; ordre de grandeur de la perte → S-COU-005 (H-23).

**(i) G-PLA-002 repart du volume exécutable.** Quand la règle des 30 jours empêche de
réaliser le volume prescrit, le volume cible suivant ne dépasse pas le volume réellement
prescriptible augmenté d'un pas. Sans cela, le volume cible gonflait sans retour (jusqu'à
deux fois la tolérance chez le débutant simulé, sans symptôme puisqu'il n'était jamais
couru). Application directe de A-05 : la sécurité ne cède pas, le volume cède. **Niveau :
sans objet** (cohérence interne).

**(j) Arrondi des durées affichées.** **Remplacé le 23/09/2026 par D-65d** (règle
d'Antoine, séance de progression à la minute au plafond) ; texte d'origine conservé : 5 min les plus proches à partir de 50 min, la minute
en dessous ; égalité vers le bas ; **jamais au-dessus du plafond des 30 jours** — dans ce
cas, les 5 min inférieures (3h44 permis → 3h40, pas 3h45). Le coureur court la valeur
affichée : l'arrondi entre dans l'historique, testé à 0 dépassement. Sous 50 min, 5 min
pèsent plus de 10 % : une séance de 30 min ne progressait jamais (bug trouvé par le
simulateur). Coût : 11 pas de +10 % au lieu de 9 pour passer de 50 à 110 min (environ
deux semaines). **Niveau : sans objet** (affichage).

**Limites assumées.** La fatigue simulée ne dépend que du volume hebdomadaire : le coût
propre d'une sortie longue ou du D+ n'est pas modélisé — le simulateur vérifie la
mécanique, pas la physiologie. La paire de sorties longues consécutives (D-35) n'est pas
simulée. Une part des symptômes vient du seul bruit du ressenti (référence de D-61a basse
dans certains tirages), commune aux deux jeux de règles. 22/09/2026

**Amendé le 22/09/2026 (TESTS.md, neuvième série, `sim7.py`) — sept défauts trouvés en
poussant la simulation, tous corrigés.**

**(k1) La règle des 30 jours (c) laissait passer une hausse composée sur la semaine.**
Chaque séance individuelle respecte +10 %, mais rien n'empêchait une chaîne du type
95 → 100 → 105 → 115 → 125 min en 9 jours : +32 % au total, exactement le schéma contre
lequel S-BLE-004 met en garde (« ne rend pas compte d'une progression continue sur
plusieurs séances »). Observé 4 à 10 fois par préparation selon le profil. **Correction :
une seule séance de progression par semaine — la sortie longue.** Les autres séances ne
dépassent jamais le maximum déjà couru des 30 jours (ni +10 %, ni davantage). Résultat :
hausses composées à 7 jours, 0 sur les 7 profils (contre 3,5 à 9,1 avant) ; symptômes
totaux en baisse (profil proche d'Antoine 2,15 → 2,06 ; débutant 1,79 → 1,47) ; atteinte
de la cible basse de D-22 inchangée (84 % → 86 %). **Coût** : les symptômes en bloc
spécifique montent chez les deux profils à faible volume, qui n'atteignaient déjà pas
les sorties clés — aucune dégradation nette, un signal qui existait déjà autrement.

**(k2) L'arrondi à 5 min (D-63j) freinait la rampe.** 90 min × 1,10 = 99, arrondi à 95 :
+5,5 % réels au lieu de 10. **Correction : seule la sortie longue en progression
s'affiche à la minute** (ex. 1h39) ; toutes les autres séances restent arrondies à 5 min
comme prévu par (j) — l'arrondi grossier ne pénalise que l'affichage courant, pas la
rampe qui a besoin de chaque point de pourcentage. Résultat : sorties ≥ 3h20 chez le
profil proche d'Antoine, 1,3 → 1,8 par préparation.

**(k3) Après un symptôme, le seuil se figeait sur le volume visé, jamais couru.** Cas
observé : seuil mémorisé à 9 h pour une tolérance réelle de 6,5 h — la sécurité de A-05
n'avait plus de prise. **Correction : le seuil se fige sur le dernier volume réellement
exécuté**, jamais sur une cible qui n'a pas eu lieu.

**(k4) Spirale de fausses alertes quand la référence de ressenti (D-61a) tombe basse par
hasard.** Cas observé : 7 fausses alertes, volume effondré à 2,4 h pour une tolérance de
6,3 h — G-PLA-002 ne s'en remettait jamais dans la fenêtre de la préparation.
**Correction : la référence se recale sur les semaines allégées**, c'est-à-dire sur
l'état reposé du coureur, au lieu de rester figée sur les quatre premières séances (D-61a)
tout au long de la préparation. Résultat : symptômes en bloc −5 à −21 % selon le profil ;
effondrements du volume de pic (< 60 % de la tolérance) sur le 80 km d'Antoine, 6 % → 3 %
des plans. Une vraie perte de tolérance reste détectée : chute simulée de 30 %, 2,76 puis
2,72 symptômes en bloc, quasi inchangé.

**(k5) Reprise après interruption trop lente malgré D-63h.** Une fois (k1) posée, plus de
30 jours sans la moindre longue séance ramenait le plafond à 30 min, puis +10 % par
semaine — bien plus lent que le volume et le seuil réduits de D-63h. **Correction : la
référence des 30 jours ne tombe pas à zéro après une coupure : pendant 30 jours suivant
la reprise, elle vaut la plus longue séance d'avant la coupure multipliée par le même
facteur que D-63h.** Cohérent avec Frandsen et coll. : les coureurs sans la moindre
course dans les 30 jours précédents (état « non calculable ») ne montraient pas de
risque accru — l'absence de référence n'est pas un plancher à zéro. Résultat, coureur
expérimenté après 5 semaines d'arrêt : cible atteinte 0 % → 82 % des plans.

**(k6) Un niveau atteint tôt sortait de la fenêtre des 30 jours avant d'avoir servi.**
Cas observé : 3h15 en semaine 20, retour à 2h ensuite, la rampe vers la sortie clé
repartait de plus bas qu'elle n'était montée. **Correction : le niveau déjà atteint est
répété (sans être dépassé) tant qu'une échéance à venir en a besoin et qu'il approche des
30 jours sans avoir été rejoué** ; la marge de la rampe (D-63d) passe de 1 à 3 semaines.
Résultat : interruption de 3 semaines en fond, cible atteinte 34 % → 60 % des plans ;
coût quasi nul ailleurs.

**(k7) Affûtage à trois semaines pour la tranche 8–20 h.** D-25 prévoit 14 à 21 jours
pour cette tranche ; D-63e n'en simulait que 14. **Ajout : 70 %, 55 % puis 40 % de la
référence pour un affûtage de 3 semaines** (45 % de réduction moyenne, dans la fourchette
S-COU-006 ; Smyth & Lawlor, 158 000 marathoniens, trouvent un affûtage strict de 3
semaines supérieur à un affûtage minimal, quand Bosquet situe plutôt l'optimum vers
2 semaines — d'où un **niveau de preuve modéré**, pas élevé, pour le choix de 3 plutôt
que 2). Dernière sortie longue à J-21 au lieu de J-14, atteinte de la cible inchangée.
**Répond au point resté ouvert sur la sortie longue en affûtage (D-63d)** : elle suit la
même part que le volume de la semaine — 40 % la première semaine de l'affûtage, quelle
que soit sa longueur.

**Poussée du 22/09/2026, suite (TESTS.md, neuvième série) — rejeu des scénarios et
ablation.** Les 15 scénarios défavorables de D-63 ont été rejoués avec (k1)–(k7), plus 8
nouveaux ; chaque mécanisme a été retiré seul pour mesurer ce qu'il apporte. Trois défauts
supplémentaires trouvés, trois mécanismes challengés.

**(k8) Séance minimale de 30 min.** Avec (k1), les séances autres que la sortie longue
tombaient à 6–17 min à bas volume (9,6 par préparation chez le profil proche d'Antoine).
Une séance de 17 min n'a pas d'intérêt d'entraînement et occupe un jour. **Correction :
aucune séance « autre » sous 30 min ; on retire des séances plutôt** — D-35 fait déjà
des jours disponibles un plafond, pas une obligation. **Arguments contre, pesés** : la
fréquence entretient l'habitude et répartit la charge ; mais à ce volume, les séances
retirées étaient de toute façon trop courtes pour porter une adaptation. Résultat : 9,6 →
0 séance courte, **aucun effet mesurable** sur la cible, les symptômes ou la fatigue. Ne
reste qu'au démarrage d'un coureur parti de zéro (volume initial nul), **amorçage traité
par D-65b** (23/09/2026).

**(k9) L'entretien de (k6) entretenait la course.** Après un 50 km, le maximum des 30
jours valait 6h30 : l'entretien a programmé 4h45 puis 4h50 deux semaines de suite, en
violation de l'alternance de D-22a. **Correction : on entretient le niveau que les
échéances exigent, pas le maximum** — une course n'est pas un niveau d'entraînement à
maintenir — et l'alternance au-delà de 3 h s'applique aussi à l'entretien.

**(k10) Le plancher de 30 min servait de marche à la sortie longue.** Coureur parti de
zéro : une séance « autre » hissée à 30 min par le plancher (D-63c), puis la sortie
longue à 33 min sur cette base, dans la même semaine : 18 → 30 → 33 min. Régression
introduite par (k8), trouvée au contrôle de non-régression. **Correction : la sortie
longue se réfère à l'historique d'avant la semaine.**

**Trois mécanismes supplémentaires de la référence de ressenti (k4), challengés.**
- **Plafond de remontée à +5 % de la référence initiale.** *Pour* : un surmenage installé
  laisse une fatigue qui persiste après une semaine allégée ; sans plafond, la référence
  suivrait et masquerait la dérive. *Contre* : **aucun effet mesuré** en simulation
  (érosion lente de tolérance : 3,87 contre 3,89 symptômes), petit coût chez le coureur
  hyper-réactif. **Conservé comme filet**, même statut que D-61f : il protège d'un mode
  que le simulateur ne représente pas — sa fatigue se dissipe entièrement en semaine
  allégée. À surveiller sur données réelles (H-29).
- **Réexamen des alertes.** Une alerte due à la seule dérive de ressenti (sans séance
  sautée), qui ne se déclencherait plus avec la référence recalée, n'a pas lieu de
  laisser un seuil mémorisé : le seuil antérieur est rétabli. *Pour* : +3 à +9 points
  d'atteinte de la cible, effondrements divisés par deux (7 % → 3 % chez le profil proche
  d'Antoine). *Contre* : +8 à +14 % de symptômes ; et le coureur a réellement déclaré un
  ressenti dégradé — l'effacer a posteriori heurte A-05. **Conservé**, parce que l'alerte
  **a produit son effet immédiat** (recul de volume, semaine allégée) : seule sa mémoire
  à long terme est corrigée, et l'app doit le dire au coureur. Variante « rétablir
  seulement après 2 semaines saines » testée : se comporte comme l'absence de réexamen,
  écartée. Même logique que D-61a (desserrage), en plus rapide et mieux ciblé.
- **Coureur qui ne saisit pas son ressenti.** Une case vide n'est pas un ressenti normal :
  l'ancien simulateur le traitait comme une valeur constante, ce qui laissait le volume
  monter sans frein (7 semaines de fatigue > 0,5 par préparation). **Correction : si la
  moitié des 8 dernières semaines n'a pas de ressenti et qu'aucun seuil n'est connu,
  G-PLA-002 cesse de sonder sa limite** ; seules les séances sautées restent observables.
  Même principe que D-19 : absence de preuve n'est pas preuve d'absence — mais ici elle
  impose la prudence plutôt que l'audace. Résultat : 0 semaine de fatigue > 0,5.
  **Indispensable** à l'ablation.

**Objectif secondaire (D-25), simulé pour la première fois.** Affûtage selon la tranche
de la course secondaire (même règle que D-63e), récupération en semaines allégées avec
G-PLA-002 gelé, puis reprise. **Échéance plafonnée** : avant une course, la sortie
longue à atteindre est min(durée / 1,10 ; cible haute de sa tranche) — sans ce plafond,
un 50 km de 6h30 en objectif secondaire exigeait une sortie de 5h55 en fond, plus que les
sorties clés du 80 km. **Placement** : jamais dans le bloc spécifique de l'objectif
principal. **Corrigé le 23/09/2026 (D-65a)** : l'affirmation « D-25b l'interdit déjà » était
fausse — D-25 est complétée en conséquence. Résultats,
profil proche d'Antoine, 80 km en 52 semaines : sortie clé ≥ 5 h atteinte dans ~80 % des
plans sans 50 km, **72 % avec un 50 km en objectif en S33**, 67 % avec le même 50 km
couru en entraînement (sans affûtage) — et dans ce dernier cas, la course dépasse
toujours la règle des 30 jours : le garde-fou doit le signaler et proposer le statut
d'objectif.

**Non-régression finale** : 23 scénarios × 200 tirages et 3 séries de graines
indépendantes × 300 tirages : 0 dépassement, 0 hausse composée, 0 valeur invalide,
100 % des affûtages dans 41–60 % ; écart entre séries ≤ 0,03 sur l'atteinte de la cible.
**Reste ouvert** : amorçage depuis un volume nul ; coureur au ressenti très bruité
(effondrement dans 50 % des plans, inchangé) ; la fatigue simulée ne dépend que du
volume. 22/09/2026 **Les trois points sont traités par D-65 (23/09/2026)** : (b), (c)
limite assumée et rendue visible, (e). Le chiffre « 72 % avec un 50 km en objectif »
devient 78–80 % avec D-65a.

---

**D-64 — Garde-fou de saisie du ressenti (TESTS.md dixième série, `sim7.py`,
22/09/2026).** D-63k4 (référence de ressenti recalée au repos) et D-63 amendement
(repli quand le ressenti n'est pas saisi) n'informaient jamais le coureur : le volume
pouvait plafonner en silence. Contraire à D-19 et D-20, qui interdisent toute
conséquence non expliquée.

**(a) Deux compteurs, pas un.** Argument pour un compteur unique remis à zéro à la
moindre note : simple à comprendre. Argument contre : un coureur qui note une séance
sur trois ne franchit jamais un streak de 3, alors qu'il est aussi peu renseigné qu'un
coureur qui en oublie 3 puis se rattrape. **Tranché : les deux compteurs coexistent.**
Le streak consécutif pilote l'alerte visible (rapide, orientée action) ; la proportion
sur 8 semaines (D-63, repli) pilote la prudence réelle sur le volume (lente, orientée
sécurité). Vérifié en simulation, profil proche d'Antoine, 300 tirages :

| Motif de saisie | Repli structurel déclenché (k4) | Alerte visible (streak 3) déclenchée |
|---|---|---|
| 1 semaine sur 3, jamais 3 d'affilée | 299/300 | **0/300** |
| 1 semaine sur 4, exactement 3 d'affilée | 298/300 | 300/300 |
| Oubli aléatoire, 20 % des semaines | 48/300 | 50/300 |
| Oubli aléatoire, 33 % des semaines | 157/300 | 171/300 |

Le premier cas est la preuve : sans le repli structurel de D-63, un coureur avec un
motif de saisie régulier mais clairsemé ne déclencherait **jamais** l'alerte visible,
alors que G-PLA-002 tourne quasiment aveugle. Un compteur unique aurait manqué
exactement le cas que D-63 a été écrit pour couvrir.

**(b) Seuil d'alerte à 3 séances consécutives sans ressenti.** À ce seuil, l'app
relance activement le coureur (notification) et le garde-fou de faisabilité (D-19)
passe en **orange** avec le message explicite : « je ne peux plus ajuster ton
entraînement en sécurité sans ton ressenti ». **Jamais rouge** — D-19 l'interdit déjà :
« aucun niveau rouge ne peut être déclenché par une absence de données ». **Relance
espacée**, pas à chaque séance : un rappel à 3, puis un nouveau tous les 3 manques
supplémentaires (3, 6, 9…) pour éviter la lassitude. Convention produit, **niveau :
sans objet**.

**(c) Remise à zéro et rattrapage a posteriori.** Le compteur remonte à 0 seulement par
une saisie réelle — jamais par la simple fermeture de la notification, sinon le
garde-fou n'a plus de valeur. Question posée pour une saisie **rétroactive** (le
coureur note après coup une séance déjà manquée) : compte-t-elle comme une saisie
normale ?

Deux précédents tranchent contre l'équivalence totale : **D-03** (RPE différentiel par
segment, abandonnée) — une saisie rappelée après coup relève de la reconstruction, pas
du rappel, et l'échec est **silencieux** : une note reconstruite ressemble à une vraie
note. **D-04** (repli VC sur note non remplie, abandonnée) — les données manquantes ne
manquent pas au hasard, et un coefficient calé dessus serait faussé sans qu'on le voie.

**Tranché : la saisie tardive éteint l'alerte visible (le badge orange disparaît, le
compteur revient à 0), mais elle n'alimente jamais G-PLA-002.** Un garde-fou qui reste
allumé après une réponse sincère du coureur devient une punition, contraire à D-20 ;
mais rattraper le passé rassure l'app sur l'historique, pas sur l'état du coureur
**au moment présent** — même distinction que D-23 entre péremption et fiabilité
actuelle. Concrètement : le modèle ne réécrit jamais une semaine passée avec une valeur
saisie en retard ; la fenêtre de 8 semaines du repli (D-63) continue de la compter comme
manquante. **Niveau : sans objet** (cohérence interne, aucune source ne traite ce cas).

**Limite assumée.** Le rattrapage est simulé comme un retour à jour global (le coureur
répond à la relance et se remet à jour), pas séance par séance — modéliser le
recouvrement fin d'un historique partiel n'apporterait rien à la décision produit.
22/09/2026

---

**D-65 — Finalisation de la v1 : objectif secondaire, amorçage, ressenti bruité,
arrondi, coût de la sortie longue et du D+ (TESTS.md onzième série, `sim8.py`,
`serie11.py`, 23/09/2026).** Traite les trois points laissés ouverts par D-63 et deux
demandes d'Antoine. **Traçabilité** : `sim3.py` et `sim5.py` manquaient aux connaissances
du projet ; `sim3.py` a été reconstruit au minimum utile à `sim7.py` (valeurs d'origine
relues dans l'historique) et **validé** en reproduisant les chiffres de la neuvième série
(80 %, 72 %, 67 %, effondrement 50 %). `controle_d61b` (qui importe `sim5`) n'est plus
exécutable.

**(a) Objectif secondaire — deux défauts.**
(a1) **D-25b n'interdisait pas le bloc spécifique** (voir D-25, complétée). Simulé, 50 km
en S42 d'une préparation 80 km de 52 semaines, coût propre de la course compté : traité
(affûtage + récupération), il ne reste que **4,7 semaines de charge sur 9**, sous le
minimum de D-21 ; non traité, symptômes en bloc **0,46 → 1,96** et 1 semaine de fatigue
> 0,5. Règle : tout le secondaire en fond.
(a2) **Une course courte en fin de fond cassait la rampe de sortie longue.** Balayage
placement S12–S40 × durée 2h30–8h : sortie clé atteinte **0 %** pour 2h30 en S33, S36,
S38 et 3h30 en S28, S38. Cause : 3 à 4 semaines de sortie longue courte (affûtage,
course plus courte que la sortie longue, récupération) vident le maximum des 30 jours,
la rampe repart de trop bas et le bloc n'offre que trois sorties clés pour remonter. Au-
delà de 3h30 la course elle-même, comptée dans l'historique, porte la rampe.
**Correction** : la référence de reprise de D-63k5 s'applique aussi après affûtage +
récupération d'un secondaire (même facteur max(0,65 ; 1 − 0,07 × (n − 1)), n = semaines
réduites), et la rampe (D-63d) anticipe ce creux. Résultat : 2h30 en S33, **0 → 73–77 %** ;
50 km en S33, **72 → 78–80 %** (trois séries de graines × 300). Reste 2h30 en S38 :
**7 %** en objectif contre **70 %** en course-entraînement — c'est le test d'acceptation de
D-25c qui le tranche. Budget de D-25a : 10–13 % sur 52 semaines, jamais limitant.
**Niveau : extrapolation** pour l'extension de la référence de reprise (H-33).

**(b) Amorçage depuis un volume nul.** Constat : avec un volume de départ nul, quatre
semaines **vides** (G-PLA-002 attend quatre ressentis avant de progresser), puis des séances
de 6 à 12 min. Règles :
- volume de départ = **min(3 ; jours disponibles) × 30 min**, en **marche-course**
  (structure de D-51, réutilisée) → S-BLE-005 : dans l'essai GRONORUN, les débutants
  démarrent à 3 séances marche-course par semaine, et une progression plus graduée
  (10 %/semaine sur 13 semaines) n'a pas réduit les blessures ;
- **fréquence avant durée** tant que le volume est à moins de 20 % du « tout au
  plancher » : la sortie longue ne progresse que si les autres séances tiennent 30 min
  (→ S-BLE-003) ; au-dessus, D-63k8 s'applique ;
- **moins de séances plutôt que plus courtes** : sous n × 30 min, on retire des séances ;
- une semaine allégée au plancher ne descend pas sous **2 × 30 min**.
Résultat : séances de moins de 30 min **3,2 → 0** par préparation, 0 dépassement, aucune
fatigue > 0,5, aucun effet sur les profils partant d'un volume non nul. Limite : le
simulateur ignore la part marchée. **Niveau : faible** pour le départ (un essai, 4 miles),
**extrapolation** pour le seuil de 20 % et le plancher de relâche (H-34).

**(c) Coureur au ressenti très bruité — aucune correction de la détection.** Trois
correctifs testés : seuil de dérive proportionnel au bruit estimé (K = 2 ; 2,5 ; 3), même
chose avec un bruit estimé sur les seules semaines allégées, confirmation sur deux
semaines. Tous réduisent l'effondrement (**50 % → 3–40 %**), tous transfèrent le risque au
coureur : semaines de fatigue réelle > 0,5 de **0,15 à 0,4–2,5** ; et chez un coureur
**normal** dont la tolérance chute réellement de 30 %, de **0,04 à 0,3–1,0**. A-05
tranche : la sécurité ne cède pas. **Limite assumée, rendue visible** : le bruit est
estimé sur les semaines allégées (état reposé) ; au-delà de **σ ≥ 0,10**, le bilan (D-59)
le dit — « ton ressenti varie beaucoup d'une semaine à l'autre, je garde un volume
prudent » — sans modifier le plan. Mesuré : 70 % des coureurs à bruit ×3 signalés, 1 % de
faux positifs, pas avant la quatrième semaine allégée (~S15). **Niveau : sans objet**
(cohérence interne, H-35).

**(d) Arrondi — règle d'Antoine, avec une exception.** À partir de 50 min, le chiffre des
minutes 1-2-3 arrondit à 0, 4-5-6 à 5, 7-8-9 à la dizaine supérieure — pour **toutes** les
séances (une seule règle au lieu de celle de D-63j). Sous 50 min, la minute (sinon une
séance de 30 min ne progresse jamais : 33 → 30). **Jamais au-dessus du plafond des 30
jours** ; la séance de progression qui y bute s'affiche **à la minute** (D-63k2).
Appliquée sans l'exception, la règle recrée le défaut k2 (90 × 1,1 = 99 → 100 > plafond →
95) : sortie clé de 3h30 **91 → 77 %**, 80 km **81 → 77 %**. Avec l'exception : **92 %** et
**80 %**, 0 dépassement. **Niveau : sans objet** (affichage).

**(e) Coût propre de la sortie longue et du D+ — la limite « fatigue = volume » éprouvée.**
Ajouté côté **vérité simulée** (jamais côté modèle) : heures de sortie longue au-delà de
2 h comptées ×1,25 ou ×1,5 ; heure de trail ×1,1 en fond et ×1,3 en bloc ; variante
« choc », sans exposition préalable, ×1,4 les deux premières semaines du bloc.
- **La sécurité tient**, parce que G-PLA-002 lit le ressenti, pas un coût posé : aucune
  semaine de fatigue > 0,5 hors cas du choc.
- **Sauf un saut de D+ à l'entrée du bloc** : symptômes en bloc **0,36 → 2,0**, 0,8 semaine
  de fatigue > 0,5. La consolidation (D-63g) gèle le volume mais ne peut rien contre un
  coût horaire qui saute. Avec un D+ monté progressivement sur les 8 dernières semaines
  de fond : **0,6** et **0**. → S-TRA-012 : l'exposition préalable à la descente est la
  stratégie la plus efficace, les coureurs les moins habitués subissent le plus de dégâts.
  **Règle** : le D+ (et le D−) hebdomadaire **monte en fond** et **se stabilise en bloc**,
  où monte la spécificité du type de montée (D-28) — même principe que D-63g, ne pas
  augmenter deux contraintes à la fois.
- **L'atteinte de la sortie clé de 5 h n'est pas robuste** : 80 % sous « fatigue =
  volume », **27 %** avec la sortie longue à ×1,25, **0–3 %** avec le D+ à ×1,3 en bloc. La
  sortie clé de 3h30 (4–8 h) n'est pas affectée (87 %). Une sortie de 5 h à 65 % du volume
  suppose de tenir ~7h40 par semaine en trail : c'est le **volume toléré observé** qui
  décide, d'où la ligne orange ajoutée à D-19.
- **Aucun coefficient ajouté** (R-MET-002) : le coût réel se lit dans le ressenti ; le
  facteur 1,2–1,4 de D-44 reste un amorçage.
**Niveau : modéré** pour le principe d'exposition progressive (revue narrative),
**extrapolation** pour la forme (8 semaines de fond, stabilisation en bloc — H-36) et pour
les coûts simulés (H-37).

**(f) Audit de palier 1 — sept renvois périmés corrigés** : D-36 et D-51 (« plafond de 20 %
de D-22 »), D-52a (« progression plafonnée de D-22 »), A-10 (« plafonds de D-22 »), D-37
(« trou n° 13 non encore traité », traité par D-46), D-63 (« D-25b l'interdit déjà »,
faux), D-63k8 (« amorçage reste à définir »). Tableau des trous ouverts : trois lignes
affichaient « non traité » ou « à fixer » pour des sujets décidés depuis le 17/09.

**Non-régression v1** (drapeaux retenus : `v1()` dans `sim8.py`) : 22 scénarios + 7 profils
× 200 tirages — **0 dépassement, 0 hausse composée, 0 valeur invalide, 100 % des
affûtages dans 41–60 %** ; atteinte de la cible à ±0,02 de `sim7` partout, sauf 80 km +
50 km objectif (0,72 → 0,81, voulu) et débutant parti de zéro (séances courtes supprimées).
**Modèle v1 figé à cette date.** 23/09/2026

---

**D-66 — Premiers retours d'usage : déroulé, dénivelé des endurances, fréquence cardiaque.**
Quatre corrections issues de la première utilisation en conditions réelles. (a) *Déroulé* :
la somme des étapes d'une séance égale toujours sa durée prescrite (une sortie de 30 min
affichait 15 + 20 + 5) ; une endurance de moins de 25 min et une sortie longue de moins de
40 min forment un seul bloc ; test `t_steps.js` sur toutes les séances du plan. (b) *Qualité* :
elle n'est placée que dans un créneau assez long pour elle, sinon la semaine n'a pas de
qualité ; le tempo comptait aussi 3 min de trop (récupération de la dernière fraction).
(c) *Dénivelé* : D-29 déclare le terrain indifférent, et « plat » n'a jamais été décidé ;
en F1–F2, le D+ d'une endurance est un **plafond** (« ≤ X m ») et celui de la sortie longue
un **repère** (« environ X m, sans le chercher ») ; la densité de D+ de départ vaut au plus
la moitié de celle de la course et la rejoint à la fin du fond (prolonge D-65e ; H-41). Un
peu de D+ dès la première séance est utile (une exposition légère protège des courbatures ;
le risque vient de la descente) ; ce qui ne l'est pas, c'est la densité de course dès la S1.
(d) *Fréquence cardiaque* : le %VC ne garantit pas que l'endurance soit facile (sans VC
amorcée il n'y a pas d'allure ; en côte, D-54 interdit toute allure cible ; la borne < 80 %
est une extrapolation). Décision d'Antoine : on reste sur le modèle du gabarit (le pilotage
cardio d'Uphill Athlete est écarté), D-12 est conservé (la FC est une observation
secondaire), et chaque endurance et sortie longue affiche une note fixe — « reste dans ta
zone facile ; si elle en sort, ralentis ou marche ; le ressenti décide, la FC confirme ».
Une vérification après coup à partir de la trace reste possible plus tard. 27/09/2026

**D-67 — La sortie longue suit sa propre progression ; le volume hebdomadaire en est la
conséquence (amende D-22 et D-63).** *Diagnostic* (simulation sur sept puis neuf profils,
28/09/2026) : la sortie longue était une part du volume, et le volume dépendait de ce qui
se plaçait ; avec peu de jours de course, tout se tenait à la baisse (2 jours : sortie clé
plafonnée à 2 h 15 en bloc). Corriger les symptômes un à un créait des régressions
(plafonner l'endurance faisait chuter le profil à 3 jours ; supprimer le bridage du volume
cassait la semaine allégée et l'alternance). *Décision* : (a) progression propre : au plus
+10 % sur la plus longue sortie des 30 derniers jours (D-63c, seule règle de charge à
preuve solide, mesurée par séance), jusqu'à la cible ; (b) semaine allégée : 65 % du niveau
atteint, 3 h au plus ; (c) au-delà de 3 h, une semaine sur deux (convention, H-27) ;
(d) hors sorties clés du bloc et du pic : 2/3 du niveau, 3 h au plus (D-70) ; (e) le volume
de la semaine devient une conséquence des séances, le contrôleur G-PLA-002 ne pilote plus
que les autres séances, chacune ≤ 1 h 30 (D-71) ; le bloc gèle le volume visé ;
(f) **un signal de fatigue gèle aussi la progression de la sortie longue** (2 semaines après
un symptôme, 1 après un ressenti « maintien » ; H-47) ; (g) récupération après un objectif
secondaire : sortie longue et volume à 35, 55 puis 75 % (H-43) ; (h) écart n° 5 du gabarit :
la dernière sortie longue déclarée, sortie de la fenêtre des 30 jours depuis moins de
8 semaines, sert de repère de reprise dégressif, même formule qu'une interruption (H-40,
H-48) ; (i) la rampe « juste à temps » (D-63d) est conservée, mais son calcul de faisabilité
est corrigé : il croyait la cible atteinte alors qu'elle ne l'était pas, et la montée
s'arrête à la cible. *Garde-fou de la refonte* : le moteur garde un mode `regles:'v1'`
qui rejoue exactement l'ancien comportement, prouvé contre `sim8.py` (0 écart) ; le
comportement v2 est couvert par `t_profils.js` (propriétés sur 9 profils) et `t_react3.js`.
28/09/2026

**D-68 — Organisation par phase (sept règles).** Les jours de course, le jour de sortie
longue et les jours de renforcement peuvent changer d'une phase à l'autre. (1) L'organisation
est attachée aux **phases**, pas aux dates : elle suit le calendrier s'il est recalculé ; à
la décision, les phases sont expliquées et visualisées (frise, dates, ce que chaque phase
change, conseil de phase). (2) Le passé ne se réécrit jamais : chaque organisation est
enregistrée avec sa date d'application (`orgHist`), les semaines commencées gardent celle
qui était en vigueur. (3) Application le lundi de la nouvelle phase, sans semaine de
transition. (4) Pas de remise à zéro de la charge : la règle des 30 jours s'appuie sur
l'historique réel ; un jour ajouté démarre à son niveau, plafonné par cette règle (aucun
démarrage bas supplémentaire : la règle par séance ne l'exige pas et la fatigue de deux
jours consécutifs se lit dans le ressenti) ; un jour supprimé n'est pas reporté sur les
autres. (5) La sortie longue garde sa trajectoire (D-67) : changer de jours ne la fait ni
sauter ni reculer. (6) Les objectifs secondaires restent prioritaires : pendant leur
affûtage et leur récupération, les volumes restent imposés. (7) Une recommandation refusée
ne change rien : la projection continue avec l'organisation actuelle et l'alerte d'écart
reste visible. **L'app recommande, l'utilisateur décide** : elle ne déplace jamais ses
jours, et avertit d'un conflit (R-REN-005 : renforcement à moins de 48 h de la sortie
longue, ou la veille d'un week-end de choc). 28/09/2026

**D-69 — Alerte d'écart et bilan de phase.** (a) *Alerte d'écart* (mécanisme principal) :
dès que la projection montre qu'une cible de sortie longue ne sera pas atteinte avant son
échéance (moins de 90 % de la cible ; objectif secondaire : avant J−14, principal : début
de l'affûtage moins une semaine ; H-45), l'app affiche l'écart chiffré, l'échéance, la
cause et les leviers. Depuis D-67 et D-71, l'organisation ne limite plus la sortie longue :
la cause est le point de départ et le temps restant (règle des 10 % sur 30 jours), et
l'alerte ne propose pas de changer de jours pour la résoudre. (b) *Carte « Bilan de phase
et phase suivante »* : affichée les 14 derniers jours de **chaque** phase, écart ou non
(décision d'Antoine : une décision prise quinze semaines plus tôt s'oublie), jusqu'à
« C'est bon pour moi ». Elle montre le réalisé (sorties faites, sortie longue réalisée
contre prévue, ressenti moyen en endurance), ce que la phase suivante change, l'organisation
déjà programmée pour elle et une recommandation **calculée et testée sur le moteur**
(par exemple : passer au week-end enchaîné, avec le nombre de week-ends de choc obtenus et le
nombre de jours de sport ; un seul renforcement lourd suffit en phase spécifique) ; boutons
« C'est bon pour moi » et « Modifier ». Elle reste accessible à tout moment depuis Profil.
Hors périmètre : lecture des commentaires (verbatims). 28/09/2026

**D-70 — Week-ends de choc et conventions réglables.** Tous les seuils de cette décision
sont regroupés dans la table `CONV` du moteur : un seul jeu de paramètres, valable pour tout
objectif (un 80 km secondaire et un 160 km principal ont le même mécanisme, le volume suit
la durée estimée de la course concernée). (a) Il n'existe pas de consensus scientifique sur
la plus longue sortie avant un ultra ; les pratiques de coachs sont dispersées (Koop : de
20 à 80 % de la distance ; Roche : sorties longues aussi courtes que possible ; pour un
premier ultra, deux ou trois week-ends enchaînés ; pour un 50 km à fort dénivelé, un ou deux
dans les six dernières semaines) — niveau de preuve : pratique de coach. (b) Week-ends de
choc : jusqu'à **3** avant l'objectif principal, sur les semaines de sortie clé ; **1** au
plus avant un objectif secondaire *exigeant*, 4 à 6 semaines avant (jamais dans les trois
dernières) ; aucun avant un autre secondaire ; hors choc, la veille de la sortie longue reste
une endurance normale, même si le week-end enchaîné est activé (H-42, H-44). (c) Samedi d'un
choc : au plus 2/3 de la sortie longue et 3 h (4 h si la course dure 20 h ou plus). (d) Sortie
longue d'une semaine « moyenne » : 3 h au plus (seuil de D-22a). (e) Objectif secondaire :
sortie longue cible = 50 % de sa durée estimée, 4 h 30 au plus (au lieu de l'échéance de
D-63, pensée pour l'objectif principal) ; une course-entraînement (priorité C) ne crée pas de
cible. (f) « Course exigeante » : 4 h ou plus, ou 30 m de D+ par km ou plus (H-44).
(g) Signal de fatigue : le RPE des **endurances seules** (option A) ; le RPE d'une sortie
longue dépend de sa durée et de son D+ (H-46) ; cible : l'écart entre RPE réel et RPE
attendu (option C), qui suppose le modèle allure-effort. (h) Objectif estimé à 20 h ou plus :
le gabarit de cette durée n'est pas écrit, celui des 8–20 h s'applique avec un avertissement.
28/09/2026

**D-71 — Suppression du temps disponible par jour.** Décision d'Antoine : le réglage
« temps disponible » n'existe plus dans l'interface et le moteur v2 ignore `days.time` (les
règles v1 le lisent encore, pour la parité). L'endurance est plafonnée à **1 h 30** (D-29)
par `CONV.efMax`, une valeur par tranche d'objectif (4–8 h : 90 ; 8–20 h : 90 ; objectif de
moins de 4 h : gabarit court non écrit, tranche 4–8 h appliquée avec avertissement) ; la
sortie longue est pilotée par sa progression (D-67). Conséquence assumée : un coureur ne peut
plus dire qu'il n'a que 60 min un jour donné, une endurance peut durer jusqu'à 90 min ; le
signal est l'écart entre le plan et ce qui est réellement couru (D-69). Test : le plan est
identique avec ou sans `time`, et aucune endurance ne dépasse 90 min. 28/09/2026


**D-72 — Raison d'une séance manquée.** Une séance de course prescrite, passée, sans séance
réalisée ce jour-là, n'est plus d'office un signal de fatigue. Accueil : carte « séance non
saisie » (semaine en cours et précédente) avec quatre réponses : « Je l'ai faite » (ouvre la
saisie), « Agenda, autre », « Fatigue », « Reprogrammer » (D-73). Réponse stockée dans
`profile.manques[date] = 'fatigue' | 'autre'`. **Règles v2 : seule « fatigue » compte comme
séance sautée** (volume ×0,92, semaine suivante allégée, sortie longue gelée 2 semaines —
D-67, H-47). Sans réponse, on retient « autre » (H-49). Motif : rater une séance pour une
raison d'agenda est fréquent et ne dit rien de la fatigue ; le RPE des endurances reste le
signal principal (H-46) ; la sécurité ne dépend pas de la réponse, car la règle des 30 jours
borne de toute façon la séance suivante. Pas de pop-up bloquant : le cas le plus courant est
une séance faite mais pas encore saisie. Règles v1 inchangées (parité). Option « malade ou
douleur » écartée tant que le moteur n'y réagit pas autrement que « fatigue ». Tests :
`t_react3.js` (fatigue = gel ; agenda ou sans réponse = plan identique au plan stable).
07/10/2026 — **Complément du 11/10/2026** : la raison se déclare aussi **le jour même** (bouton « Pas faite » sur la séance du jour) ; la séance passe aussitôt en « Manquée · fatigue/agenda ». L'effet sur le plan reste celui de la fin de semaine (la semaine en cours n'ajuste rien, A-02).

**D-73 — Décaler une séance dans la semaine.** Une séance de course générée peut être
déplacée par l'utilisateur, **dans la semaine en cours seulement**, vers un jour à partir
d'aujourd'hui **sans autre course** (`profile.decal[date d'origine] = nouvelle date`). Jamais
vers la semaine suivante : rattraper une séance, c'est concentrer la charge. Une sortie
longue manquée le dimanche n'est donc pas reprogrammable, le plan continue. Le moteur
déplace la séance après le placement de la qualité et des accélérations (durée, contenu et
D+ inchangés), garde son identifiant (rattachement de la séance réalisée stable) et refuse un
décalage hors semaine ou vers un jour déjà couru. Accès : carte de séance manquée, ou fiche
d'une séance à venir (« Déplacer cette semaine », « Remettre au … »). La veille de la sortie
longue est proposée avec un avertissement. Le passé ne se réécrit pas : un décalage d'une
semaine close reste tel quel. Test : `t_decal.js`. 07/10/2026

**D-74 — Renforcement : saisie minimale.** Le moteur ne lit du renforcement que sa date et sa
présence ; l'interface s'en sert pour un seul message (jambes chargées la veille d'une sortie
longue, d'une descente ou d'une course). La saisie se réduit à **durée, RPE, jambes
sollicitées (non / un peu / beaucoup)** et une note ; les deux premiers et les jambes sont
obligatoires (`cfJ`). Retirés du formulaire : photo, origine, qualité travaillée, dominante,
excentrique, détail du WOD, charges, impacts, FC, et l'état des jambes 1–5 (redondant). Les
données déjà saisies sont conservées et lues (`cfJ` déduit de l'ancienne dominante,
excentrique ou impacts). Profil : lieu et matériel retirés (demandés, obligatoires, jamais
utilisés). Un renforcement fait un autre jour de la même semaine est rattaché au
renforcement prévu non fait. Le **journal de progression** (charges, scores, tout type de
renforcement), activable dans le profil, est noté pour plus tard (BACKLOG). 07/10/2026

**D-75 — D+ de départ figé au démarrage du plan.** Constat d'Antoine (09/10/2026) : sortie
longue de 110 min proposée avec 100 m de D+. Cause : la densité de D+ de départ (m/h) était
recalculée chaque jour sur **toutes** les sorties des 8 dernières semaines, y compris les
endurances que le plan prescrit lui-même sur terrain roulant (D+ plafonné en F1–F2) — boucle
de A-02 : la consigne fabrique la mesure qui la nourrit. Règles v2 : la densité de départ se
calcule sur les **sorties longues et courses des 8 semaines avant le démarrage du plan**, puis
sur la sortie longue déclarée, puis 150 m/h ; elle est plafonnée à la moitié de la densité de
la course (H-41) et monte linéairement jusqu'à la densité de course à la fin du fond. Après le
démarrage, le D+ réalisé ne la modifie plus. Règles v1 inchangées (parité). Test :
`t_profils.js` (densité identique avec ou sans séances après démarrage, plus basse avec une
sortie longue plate avant). 09/10/2026

**D-76 — Saisie de séance : effort, trace, nutrition (interface v24).** Issu de l'audit UX
du 11/10/2026 et des remarques d'Antoine du 13/10/2026. (a) *Effort ressenti* : boutons de
1 à 10 sur une seule rangée, sans 0 (« repos » n'a pas de sens pour une séance faite) et sans
valeur par défaut ; le libellé du chiffre choisi s'affiche (mêmes mots qu'avant). Les
séances déjà saisies à 0 restent lisibles. (b) *Trace* : une trace importée **remplace** la
durée, la distance, le D+ et le D− pré-remplis depuis la séance prévue (avant, elle ne
remplissait que les champs vides : la durée prévue restait, alors que la règle des 30 jours
s'appuie sur la durée réelle). D+ et D− ne sont remplacés que si la trace contient de
l'altitude. (c) *Date* : jamais dans le futur ; une séance prévue plus tard se saisit à la
date du jour. (d) *Nutrition* (module actif, course de 60 min et plus, seuil de `nutriFor`
inchangé ; écart connu avec les ~2 h de D-30) : trois réponses — « J'ai pris » (glucides,
boisson, inconfort), « Rien pris » (0 g), « Non suivi » (aucune donnée). La progression de
la cible ne compte plus que les sorties avec **des glucides pris (> 0 g)** : avant, 0 g
saisi faisait monter la cible de 6 g/h. (e) *Inconfort digestif* : quatre mots, dans le sens
de la littérature (plus à droite = pire ; Gaskell, Rauch et Costa, Front. Nutr. 2022) —
Aucun, Léger, Gênant, Arrêt —, stockés en 5, 4, 2, 1 sur l'ancienne échelle 1–5 : la règle
« cible gelée si ≤ 2 » est inchangée et les données existantes restent valables.
(f) *Jambes 1–5* retiré de la saisie de course : lu par rien (ni moteur ni écran), même
logique que D-74. Moteur inchangé. 13/10/2026

## CAP — Capacité de référence

### G-CAP-001 — Vitesse critique course (VC)
- **Prédit** : l'intensité de référence qui convertit une allure en effort (%VC), et
  sert de dénominateur à toutes les grandeurs terrain et fatigue
- **Valeur initiale / origine** : meilleures allures ajustées à la pente sur 400 à
  5000 m extraites de l'entraînement habituel ; dérivée, confiance croissante avec
  l'historique → S-COU-002
- **Observation correctrice** : chaque nouvelle sortie course ; efforts quasi-maximaux
  3–12 min (D-07) en apport principal → S-COU-003
- **Case 4 — complétude** (D-13b) : la VC est censée évoluer, la convergence est donc
  inapplicable. Fiable quand la plage 400–5000 m est couverte par des efforts récents,
  et que l'effort quasi-maximal le plus récent n'est pas trop ancien. Repère :
  S-COU-003 documente une estimation sur 6 semaines d'entraînement habituel
- **Péremption** : porte une date de dernière observation course. Sans donnée course
  récente, la confiance décroît — le modèle doit pouvoir dire « je ne sais plus »
  plutôt qu'afficher une valeur périmée avec assurance (voir trou ouvert
  « adaptation croisée »). **Niveau : extrapolation** (aucune source sur le taux de
  décroissance)
- **Réserve** : S-COU-002 et S-COU-003 portent sur marathon route et coureurs
  récréatifs, pas sur ultra-trail. Sur les portions marchées en montée forte, le %VC
  perd son sens physiologique — zone non couverte. **Niveau : extrapolation**
- **Statut** : admise

## TER — Terrain

### G-TER-001 — Coût-pente personnel
- **Prédit** : allure atteignable par bande de pente (plat, montée douce/forte,
  descente douce/forte), **exprimée en rapport à l'allure du coureur sur le plat**
  (D-53a) — l'écart individuel au plat appartient à G-CAP-001, les deux grandeurs ne sont
  séparables qu'à cette condition
- **Valeur initiale / origine** : courbe générique du coût de course selon la pente,
  en amorçage seulement → S-COU-001. **Niveau : modéré** comme référence de groupe,
  **non généralisable à l'individu** → S-TRA-001
- **Observation correctrice** : identification par cohérence — sur des **segments
  admissibles au sens de D-10** (cadence stable, allure stable, pente modérée, pas de
  marche), l'effort (%VC) devrait être uniforme d'une bande de pente à l'autre ; un écart
  systématique révèle une correction de pente fausse pour ce coureur. **Corrigé le
  17/09/2026** : la rédaction initiale filtrait par « séance prescrite régulière », ce qui
  faisait dépendre l'apprentissage de la prescription — boucle contraire à A-02 (aucune
  valeur prescrite n'est une observation). Le filtre par régularité **du signal GPS**
  (D-10) rompt la boucle ; depuis D-49/H-01, il s'agit d'une **pondération** et non d'une
  exclusion.
- **Ce que la grandeur mesure réellement — précisé le 17/09/2026 après passe adverse
  (H-02).** Elle ne mesure **pas un coût énergétique** mais une **allure réalisée par
  bande de pente**. La nuance est décisive : un coureur qui lève volontairement le pied
  en côte — ce que tout coach d'ultra enseigne — produit le même signal qu'un coureur
  dont la montée coûte cher. Le modèle fossiliserait une stratégie d'allure en la prenant
  pour une donnée physiologique, et le ferait de façon **auto-renforçante** (prescrire
  des montées plus lentes confirmerait la mesure). **A-02 ne protège pas de ce cas** :
  elle interdit qu'une valeur prescrite devienne une observation, pas qu'une prescription
  modifie le comportement qui produit l'observation. Faille identifiée le 17/09/2026.
  **Atténuation** : calibrer en priorité sur les segments à **haute intensité**, où
  l'allure est contrainte par la physiologie plutôt que par le choix. Atténuation, pas
  solution. **Niveau : extrapolation** — l'hypothèse « effort uniforme sur segment
  régulier » n'a aucun appui direct, elle est posée par nous et testable séance après
  séance
- **Bornes contre la divergence** (D-53b) : l'estimation ne peut s'écarter de la courbe
  générique au-delà de **±30 % à confiance nulle, jusqu'à ±60 % à confiance pleine** — une
  bande bien observée gagne le droit de s'écarter, une bande peu observée reste tenue près
  du prior. Et une **dérive monotone** sur plusieurs cycles **gèle** la calibration de la
  bande, mais **seulement après une première convergence** : une estimation qui rejoint la
  vérité dérive elle aussi de façon monotone, et la geler à ce moment casserait un coureur
  sain (mesuré : erreur portée de 0,3 % à 8,1 %)
- **Case 4 — convergence** (D-13a) : le coût-pente bouge lentement, l'estimation doit
  se stabiliser bande par bande. Fiable quand les dernières observations d'une bande ne
  déplacent plus son coefficient au-delà du seuil commun
- **Non couvert** : la technicité du terrain du jour (boue, neige, nuit). Seule une
  technicité stable par parcours est déclarée (D-07)
- **Statut** : admise

## FAT — Fatigue et durabilité

### G-FAT-001 — Décroissance-fatigue intra-séance
- **Prédit** : de combien la performance se dégrade au fil d'une sortie longue, et **à
  partir de quand**
- **Ce qu'elle mesure, en clair** : sur une même sortie, la vitesse du coureur sur un
  **même type de terrain** au début et plus tard. Exemple : 7,2 km/h en montée douce dans
  la première heure, 6,3 km/h en montée douce dans la dernière — 12,5 % de perte.
  Comparaison **contrôlée** : météo, sommeil, fraîcheur et motivation sont constants à
  l'intérieur d'une sortie ; seule la fatigue accumulée a changé
- **Valeur initiale / origine** : littérature durability → S-COU-004, **vérifiée** :
  82 303 marathoniens ; découplage vers 25 km en moyenne, à 33,4 km chez les plus durables
  contre 19,1 km chez les moins durables. **Niveau : élevé** sur route, **faible** en ultra
- **Observation correctrice** : pour **chaque bande de pente présente tôt et tard dans la
  sortie**, les vitesses observées, placées selon le temps écoulé depuis le départ. Deux
  valeurs en sortent : l'**ampleur** (perte par heure) et le **moment du décrochage** —
  ce second point est le plus précieux, S-COU-004 montrant qu'il prédit la performance
  mieux que l'ampleur
- **Pas de découpage en tiers ni en quarts pour le calcul** (17/09/2026) : un découpage
  fixe jette de l'information et **ne peut pas voir le moment du décrochage**. Le calcul
  suit la dégradation **en continu** — une pente, un point de rupture. Les tiers restent
  utiles à **l'affichage** (« tu perds 8 % sur le dernier tiers »), jamais au calcul
- **Aucune dépendance au %VC ni au coût-pente** (D-57a) : en comparant à terrain égal
  **dans la même sortie**, la correction de pente devient inutile et le biais de
  G-TER-001 (H-02) n'est plus hérité
- **Sortie non exploitable si aucune bande n'est présente tôt et tard** : on saute, on
  n'invente rien. Mesuré sur des formes de parcours réalistes, **94 % des sorties restent
  exploitables** — seuls les parcours point à point montants ou descendants sont exclus
  (TESTS.md). La règle précédente (parcours répété ou terrain homogène) n'en retenait que
  20 à 30 % : la simplification a **élargi** la base
- **Test d'hypothèse nulle obligatoire** — ajouté le 17/09/2026 après simulation
  (TESTS.md, T-F4). La recherche d'un point de rupture en trouve **toujours** un, y
  compris dans du bruit pur : un coureur synthétique **sans aucune dégradation** était
  mesuré à −3 %/h en moyenne, jusqu'à −20 %/h sur une sortie isolée — chiffre qui alimente
  le plafond systémique (D-33) et aurait fait baisser le volume sans raison. Le modèle
  « dégradation » n'est donc retenu que s'il explique **nettement** mieux les données que
  le modèle « aucune dégradation », et si l'ampleur dépasse un plancher. Sinon la réponse
  est **« aucune dégradation décelée »** — réponse légitime, jamais une valeur inventée.
  Après correction : 0 faux positif sur 10 sorties
- **Seconde observation** : découplage FC/allure sur segments admissibles (D-09, D-10),
  signal plus précoce, quand une FC exploitable existe
- **Case 4 — complétude** (D-13b) : la durabilité est censée s'améliorer, convergence
  inapplicable. Fiable selon le nombre et la fraîcheur des sorties exploitables — environ
  une par semaine, donc grandeur lente : 3 à 4 mois. **Vérifié en simulation** : sur une
  sortie isolée le décrochage varie de 1,4 à 2,5 h pour une vérité à 2,0 h ; moyenné sur
  10 sorties, l'estimation tombe à 1,97 h et −9,9 %/h pour une vérité de −10 %/h
- **Statut** : admise

### G-TER-002 — Progression sur segments répétés
- **Prédit** : l'évolution de la performance **sur un même segment** au fil des mois, à
  effort libre. Exemple : ta montée habituelle à 6,8 km/h en mars, 7,4 km/h en juin
- **Au niveau du segment, jamais de la sortie** (17/09/2026). Un coureur refait
  « globalement » les mêmes sorties, mais il les rallonge, les inverse, part d'ailleurs :
  au niveau sortie ces variantes ne se reconnaissent plus. **La montée près de chez lui
  reste la même montée**, quelle que soit la boucle autour
- **Reconnaissance** : coordonnées de **début et de fin**, direction, longueur, dénivelé.
  Pas de comparaison de la trace complète point par point — coûteuse et fragile. Quatre
  repères grossiers suffisent. Aucune déclaration du coureur
- **Équivalence par profil écartée** (deux parcours différents de distance et D+
  semblables) : la technicité change tout et n'est pas mesurée
- **Valeur initiale / origine** : aucune — la grandeur n'existe qu'au deuxième passage
- **Observation correctrice** : vitesse sur un segment reconnu, rapportée au ressenti de
  séance (G-RES-001) pour écarter les jours manifestement atypiques
- **Case 4 — complétude** (D-13b) : **un passage unique ne dit rien** — météo, sommeil et
  fatigue de la veille décalent une performance de plusieurs pourcents. On lit une
  tendance sur plusieurs passages
- **Deux usages** : (a) **signal de progression** objectif, sans prescription donc **sans
  boucle possible** ; (b) **détecteur de dérive H-02** — une vitesse qui baisse sur le
  segment habituel alors que le ressenti reste stable est la signature de la boucle. Seule
  observation du coût en pente **indépendante de l'estimation du modèle**
- **Deux sources** : passages **opportunistes** et **séance étalon** (D-55), version
  organisée du même signal — même segment, même moment du cycle, même consigne
- **Statut** : admise

## RES — Ressenti

### G-RES-001 — RPE de séance
- **Prédit** : trois usages, tous dans le modèle —
  (a) **veto d'admission** : un désaccord fort entre effort calculé et ressenti écarte
  la séance de l'identification des coefficients terrain/fatigue, et le désaccord est
  montré au coureur ;
  (b) **dérive ressenti/calculé dans le temps** : à effort calculé constant, un
  ressenti qui baisse sur plusieurs semaines marque l'adaptation, qui monte marque la
  fatigue accumulée. C'est le signal précoce que le %VC seul ne donne pas ;
  (c) **seule source d'effort** pour les activités sans équivalent GPS
- **Valeur initiale / origine** : déclarée, une note par séance à la fin → S-CHA-001.
  **Niveau : élevé** comme indicateur relatif de charge interne
- **Observation correctrice** : sans objet (mesure directe) ; son ancrage dérive avec
  la forme — dérive assumée et exploitée en (b), pas corrigée
- **Case 4 — validité de la mesure** (D-13c) pour (a) et (c) : la note existe et le
  coureur a un historique suffisant pour que son échelle personnelle soit ancrée.
  **Case 4 — convergence** (D-13a) pour (b) : la relation ressenti/calculé doit se
  stabiliser avant d'être lue comme un signal d'adaptation ou de fatigue
- **Ne fait pas** : ne produit aucun coefficient terrain ou fatigue (D-05) — mais
  corrige bien G-PLA-002 par l'usage (b)
- **Effet d'une absence** — **corrigé le 17/09/2026**, la formulation initiale (« son
  absence ne change pas ce que le modèle apprend ») était fausse : le veto (a) exclut
  des séances, donc modifie l'ensemble d'apprentissage. Formulation juste : une note
  **manquante** ne fausse aucun coefficient (aucune valeur n'est inventée), mais elle
  laisse entrer une séance qui aurait pu être écartée. Erreur de type « bruit », qui
  se dilue avec le volume, et non de type « biais »
- **Statut** : admise

## CHG — Charge extra-course

### G-CHG-001 — Charge extra-course récente — effet fatigue uniquement
- **Prédit** : covariable de fraîcheur et filtre de contamination des observations
  TER et FAT. **Cette grandeur ne couvre que l'effet charge. L'effet adaptation
  n'est pas modélisé** — voir trou ouvert
- **Valeur initiale / origine** : sRPE (durée × RPE) de toute activité hors course,
  cumulé sur fenêtre 24–48h — seule unité commune entre modalités → S-CHA-001,
  R-REN-004. **Niveau : élevé** pour l'usage comme indicateur relatif
- **Observation correctrice** : **corrigée le 17/09/2026** — la rédaction initiale
  (« poids et largeur de fenêtre à calibrer ») était une tâche, pas une observation, et
  la grandeur était donc admise avec sa case 3 vide. Observation réelle : la
  **contamination mesurée** — écart entre l'effort calculé (%VC) attendu et observé sur
  une séance course qui suit une activité hors course, rapporté au délai qui les sépare.
  La fenêtre et le poids se déduisent de cet écart au lieu d'être posés. Valeur
  d'amorçage de la fenêtre : R-REN-005 → S-CHA-002. **Niveau : modéré** pour la fenêtre
  d'amorçage, **extrapolation** pour le mécanisme de déduction
- **Case 4 — convergence** (D-13a) : 2 à 3 séances par semaine, donc stabilisation
  attendue en plusieurs mois. Critère valide mais lent à se déclencher
- **Réserve** : la corrélation sRPE / charge physiologique se dégrade aux intensités
  hautes — fiable pour du vélo ou de la natation d'endurance, moins pour une séance
  intense mal évaluée au ressenti → S-CHA-001
- **Statut** : admise

## PLA — Planification

### [abandonnée] G-PLA-001 — Cadence de relâche
Supprimée comme grandeur le 17/09/2026 (D-57b). Son identifiant est conservé et ne sera
jamais réattribué. Motif : son observation correctrice ne discriminait pas — G-PLA-002
absorbe les mêmes signaux en premier (D-56c, TESTS.md T-C3). Remplacée par la règle fixe
assumée 3 semaines de charge pour 1 allégée, bornée 2 à 4, plus la relâche à la demande
(D-57c).

### G-PLA-002 — Volume hebdomadaire cible
- **Prédit** : le volume d'entraînement prescrit pour la semaine à venir, par phase
- **Valeur initiale / origine** : repères de D-21 (fond 3–5 h, bloc 7–9 h, pic 9–11 h
  pour une cible 80 km) → S-TRA-002, S-TRA-004. **Niveau : faible** — valeurs de peloton,
  amorçage uniquement
- **Observation correctrice** : la tolérance de charge observée du coureur, **lue selon
  D-33 en distinguant plafond d'impact et plafond systémique**, sur trois signaux globaux
  déjà présents dans le modèle — dérive ressenti/calculé (G-RES-001b),
  aggravation de la décroissance-fatigue (G-FAT-001), et séances prescrites non
  réalisées, plus (D-57c) **trois demandes de relâche anticipées sur des cycles
  successifs**. Le volume cible monte quand tout reste stable sous charge croissante, et
  redescend dès qu'un signal se dégrade
- **Progression : le maximum d'un pas multiplicatif et d'un pas absolu** (D-56a). Une
  progression purement multiplicative partant de **zéro reste à zéro** — un débutant ne
  démarrait jamais. Avec un pas absolu de l'ordre de 0,5 h/semaine : 11 semaines depuis
  zéro pour atteindre 7 h
- **Mémoire du dernier niveau ayant déclenché un symptôme, et freinage à son approche**
  (D-56b). Sans cela, le volume ne reculait qu'**après** les symptômes puis remontait au
  plein plafond jusqu'à les redéclencher : il se stabilisait **au-dessus** de la tolérance
  réelle (+9 à +21 %) avec des variations de 12 à 38 % d'une semaine à l'autre. Après
  correction : dépassement de −3 à +9 %, oscillation de 1 à 18 %
- **Une séance sautée ne fait baisser le volume que si elle se répète** (D-57d), jamais au
  premier incident
- **Articulation avec le calendrier (D-63, 22/09/2026)** : **gelée en affûtage**, le volume
  y est fixé (D-63e) ; **consolidation en bloc spécifique**, ni retest ni desserrage, et
  gel au volume d'entrée si aucun seuil n'est connu (D-63g) ; **reprise après
  interruption**, volume et seuil réduits d'un même facteur, seuil provisoire si aucun
  n'était connu (D-63h) ; **repart du volume exécutable** quand la règle des 30 jours
  empêche de réaliser le volume prescrit (D-63i)
- **Case 4 — convergence** (D-13a) : la tolérance propre au coureur est établie quand
  deux ou trois cycles de charge successifs donnent le même point de bascule — environ 3 mois
- **Bornes** : seule la valeur de **pic** de D-21 est un plafond de sécurité, jamais
  dépassée. Fond et bloc spécifique sont des repères de structure, pas des plafonds :
  G-PLA-002 peut les dépasser si la tolérance observée le justifie (D-21, corrigé le
  17/09/2026). **Corrigé le 21/09/2026** : cette ligne disait auparavant que toutes les
  valeurs de D-21 étaient des plafonds jamais dépassés — incohérence avec la correction de
  D-21, jamais répercutée ici. Aucun effet sur le mécanisme (D-56/D-57) : il n'a jamais lu
  fond/bloc spécifique comme des plafonds, seulement le pic via `plafond_pic`.
- **Statut** : admise — c'est l'observation correctrice qui la rend admissible ; sans
  elle, les volumes de D-21 seraient des paramètres génériques permanents, à rejeter

### [abandonnée comme grandeur] G-PLA-003 — Adhérence à la répartition des intensités
Rétrogradée le 20/09/2026 en **règle d'affichage de D-34**, identifiant conservé et jamais
réattribué. Motif : elle ne portait **aucun coefficient**, ne se calibrait pas, n'évoluait
pas — elle comparait simplement l'histogramme de la semaine écoulée à la cible de D-34, ce
qui est calculable à tout instant sans état. Une grandeur qui ne stocke rien et n'apprend
rien n'est pas une grandeur. Son action (signaler une dérive répétée au coureur, sans
modifier le plan) devient une ligne du bilan hebdomadaire (D-59).

## NUT — Nutrition

### G-NUT-001 — Tolérance glucidique à l'effort
- **Prédit** : la quantité de glucides par heure à prescrire sur la prochaine séance
  longue
- **Valeur initiale / origine** : générique et basse — les recommandations s'étagent de
  30 à 90 g/h selon durée et intensité, jusqu'à 90 g/h au-delà de 2h30 d'effort
  → S-NUT-001. **Niveau : élevé** pour la fourchette générique
- **Observation correctrice** : quantité réellement ingérée sur la séance + présence ou
  absence de troubles digestifs. Deux champs, saisis après la séance
- **Case 4 — complétude** (D-13b) — **reclassée le 17/09/2026** : la tolérance est
  censée **augmenter** avec l'exposition, comme la vitesse de référence ; la convergence
  y est donc inapplicable (elle signalerait « fiable » pendant les plateaux). On juge la
  couverture et la fraîcheur : progression d'environ **5 à 10 g/h par semaine**,
  puis **3 à 4 semaines de consolidation** à la dose cible ; au moins **8 à 10 semaines**
  au total → S-NUT-002. **Niveau : modéré** — protocole documenté, mais études de petite
  taille et populations entraînées
- **Progression plafonnée** : jamais plus de 10 g/h supplémentaires d'une semaine à la
  suivante, quelle que soit la tolérance observée — même logique de plafond que la règle des 30 jours (D-63c, ex-D-22b)
- **Sens unique de la progression** : la tolérance ne monte que sur **confirmation
  positive** (dose ingérée sans trouble). Une saisie manquante ne fait pas progresser et
  ne dégrade rien : le mode d'échec d'une donnée absente est **conservateur**, ce qui
  rend la saisie facultative acceptable ici — contrairement au RPE par bloc (D-03), où
  une absence faussait un coefficient
- **Statut** : admise

---

## Trous ouverts

| Sujet | État |
|-------|------|
| **Démarrage à froid** — traité par D-14 à D-18 et D-23. Reste ouvert : la formulation exacte de l'affichage à confiance basse, et le cas où le coureur n'importe rien et ne déclare rien — le garde-fou n'a alors rien à mordre, l'app ne bloque pas mais ne peut pas prétendre être calibrée. **Volume de départ depuis zéro traité par D-65b** (23/09/2026) | partiellement traité |
| **Horizon et objectif** — où et comment la course cible entre dans le modèle. **Traité** : cible et profil (D-26, D-27), hiérarchie des objectifs et budget (D-24, D-25, D-65a), index sur la durée d'effort (D-44). Ligne corrigée le 23/09/2026 : elle affichait « non traité » depuis le 16/09 | **traité** |
| **Progression de charge d'un bloc à l'autre** — rien ne dit comment la charge augmente de semaine en semaine, ni comment se décident les blocs, les semaines de relâche et l'affûtage. Déjà identifié comme trou dans SOURCES.md, sans critère mesuré retenu. **Précisé le 21/09/2026** (chantier contrôleur, TESTS.md septième série) : le risque concret est qu'un recul de G-PLA-002 (D-56, D-57) tombe, par hasard, au moment où le calendrier de blocs (D-21) fait entrer le coureur en bloc spécifique — l'app n'a aujourd'hui aucune conscience du calendrier de blocs pour l'anticiper ou le signaler. G-PLA-002 reste prioritaire sur les repères de bloc (D-21), donc rien à corriger dans son fonctionnement seul ; ce qui manque est l'articulation entre les deux. **Traité le 22/09/2026 par D-63** (TESTS.md, huitième série). Limite « fatigue = volume seul » **éprouvée le 23/09/2026 par D-65e** : sécurité tenue grâce à la lecture du ressenti, règle de progression du D+ ajoutée, garde-fou de la sortie clé ajouté. Reste une limite : le coût réel est inconnu pour chaque coureur, seule son observation le fixe | **traité — D-63, D-65e** |
| **Composition du temps de course** — D-01 prévoit que le temps de course est dérivé par composition des prédictions de séance, mais la règle de composition n'est écrite nulle part | non traité |
| **Coût musculaire de la descente** — G-TER-001 couvre le coût énergétique d'une bande de pente, pas les dégâts musculaires qu'une descente longue laisse pour les jours suivants. Facteur central en trail, déjà en extrapolation dans S-REN-003 | non traité |
| **Blessure et reprise** — catégorie BLE vide dans REGLES.md. Interruption, reprise progressive, effet sur la péremption de la VC. **Reprise du volume après interruption traitée par D-63h** (22/09/2026) ; le reste demeure | partiellement traité |
| **Seuil de stabilité** — valeur de déplacement sous laquelle une estimation est dite convergée (D-13a). **Fixé par D-49a** (5 % sur 5 observations, relatif à la dispersion, fenêtre récente pondérée). Extrapolation assumée, à éprouver sur données réelles. Ligne corrigée le 23/09/2026 | **traité — D-49a**, valeur à éprouver |
| **Seuils de régularité d'un segment** (D-10) — **fixés dans D-10** (≥ 60 s, cadence ≤ 5 %, allure ≤ 10 %, une bande de pente), pondération plutôt que filtre (D-61e). Sans appui scientifique. Ligne corrigée le 23/09/2026 | **traité — D-10**, valeurs à éprouver |
| **Coureur au ressenti très bruité** — à bruit ×3, le volume s'effondre dans 50 % des plans. Aucun correctif testé ne le résout sans faire porter le risque au coureur (D-65c) | **limite assumée**, rendue visible (D-65c) |
| **Adaptation croisée** — une activité non-course ne fait pas bouger la VC ; le modèle constate la progression après coup via les sorties course, sans l'anticiper ni l'attribuer. Simplification assumée : le transfert natation→course est faible → S-CHA-003. Angle mort réel : un coureur blessé remplaçant la course par de l'aqua-jogging n'a aucune donnée course, sa VC devient périmée sans que rien ne le signale (d'où la péremption G-CAP-001). Prérequis avant toute levée : pouvoir attribuer un saut de VC à un bloc croisé plutôt qu'au volume course de la même période — indémontrable sur un utilisateur unique, possible sur données multi-utilisateurs | non modélisé, à lever plus tard ou jamais |
| **Suivi explicite de la FC en montée** (option écartée le 16/09/2026) — aurait fait de la FC-à-allure-donnée par bande de pente une quatrième grandeur. Écartée au profit de D-09/D-12 : ajouter une grandeur avant que les cinq premières aient tourné sur données réelles va contre R-MET-002. Besoin couvrable hors modèle par les données Garmin croisées aux segments | extension possible, non retenue |
| **Catégorie NUT de REGLES.md** — ouverte côté SPEC et SOURCES, mais les règles de gestion correspondantes restent à écrire dans REGLES.md (fichier de référence, non modifié depuis ce chantier) | à faire |
| Sources encore non retrouvées : S-TRA-003 (contextuelle, D-19). **S-TRA-006 retrouvée le 22/09/2026** (Jaén-Carrillo et Margarit-Boscà, résumé, n = 1, niveau faible confirmé). Vérifiées le 17/09/2026 : S-COU-004, S-TRA-001, S-MES-002, S-REN-006 | à retirer si elles restent introuvables |

---

## Chantier en cours — Génération du plan

Périmètre arrêté le 16/09/2026. « Génération du plan » désigne la cascade
**horizon → blocs → semaine → séance** et sa boucle de retour. Le mot *composition*
reste réservé à son seul sens de D-01 : dériver un temps de course en composant des
prédictions de séance.

Méthode d'établissement de cette liste : parcours de la chaîne dans les deux sens, en
cherchant à chaque maillon ce que le maillon suivant réclame en entrée, puis passage de
chaque élément au test route / trail. L'exhaustivité n'est pas démontrable ; la liste
est révisable et doit l'être à chaque fin d'étape.

**Décision de portée, 16/09/2026 : on généralise à la course sur route dès maintenant**,
plutôt que d'assumer une V1 trail. Motif : le modèle dégénère déjà proprement sur route
(les bandes de pente raides ne reçoivent simplement aucune observation et ne sont jamais
utilisées — D-23), donc aucun « mode route » n'est nécessaire ; mais trois éléments sont
aujourd'hui écrits en trail et doivent être doublés.

| # | Élément | Route / trail | État |
|---|---|---|---|
| 1 | **Cible** : date, distance, dénivelé et **profil** — un 40 km en deux longues montées ne se prépare pas comme 40 km vallonnés | profil aplati sur route, paramètre neutralisé | **traité — D-26, D-27** |
| 2 | **Hiérarchie des objectifs** — une course intermédiaire est-elle un objectif préparé (affûtage + récupération) ou une séance déguisée ? Sans hiérarchie, le plan s'affûte plusieurs fois par an et ne construit rien | identique | **traité — D-24, D-25** |
| 3 | **Progression de charge** — montée du volume, découpage des blocs, décision de l'affûtage | identique | **traité — D-21, D-25, D-63** (articulation G-PLA-002 / calendrier de blocs, 22/09/2026) |
| 4 | **Répartition des intensités** — proportion de facile et de dur dans la semaine | identique | **traité — D-34** (G-PLA-003 rétrogradée en règle d'affichage de D-34 le 20/09/2026) |
| 5 | **Progression du dénivelé** — D-22 fait progresser la durée, rien ne fait progresser le D+. **Type de montée (D-28) traité** ; **forme de la progression traitée par D-65e** (le D+ monte en fond, se stabilise en bloc) ; la vitesse de progression du D+ hebdomadaire reste sans valeur chiffrée | aucune observation sur route, dégénère | partiellement traité |
| 6 | **Typologie des séances** — aucun catalogue de types n'existe, donc rien à choisir | identique | **traité — D-29** |
| 7 | **Gabarit de semaine** — pose sur les jours disponibles, espacement minimal entre séances dures (R-REN-005 : 24–48 h) | identique | **traité — D-35, D-36, D-37** |
| 8 | **Place du renforcement** | identique | **traité — D-39** |
| 9 | **Marche et portions marchées** | inexistant sur route | **traité — D-40** |
| 10 | **Format de prescription** | identique | **traité — D-42** |
| 11 | **Statut des séances réalisées** | identique | **traité — D-43** |
| 12 | **Déclenchement du recalcul** — à chaque séance, chaque semaine, ou sur écart seulement | identique | **traité — A-03** |
| 13 | **Indisponibilités datées** | identique | **traité — D-46** |
| 14 | **Durée ou distance** | résolu | **traité — D-45** |
| 15 | **Tableaux de D-21 à doubler** — résolu autrement : index sur la durée d'effort, pas de doublement | résolu | **traité — D-44** |
| 16 | **Terrain disponible** | divergent | **traité — D-47** |
| 17 | **Chaleur, altitude, nuit** | identique | **traité — D-48 (exclus, réouverture conditionnée)** |
| 18 | **Seuil de stabilité** (D-13a) et **seuils de régularité d'un segment** (D-10) | identique | **traité — D-49** |
| 19 | **Affichage à confiance basse** et cas du coureur sans aucune donnée | identique | **traité — D-42** |

Hors périmètre de ce chantier, traités ensuite : composition du temps de course (suppose
la génération faite), coût musculaire de la descente (grandeur à part entière), blessure
et reprise (chantier propre).

---

## Architecture d'exécution

Écrite le 16/09/2026, avant la suite du chantier de contenu. Motif : SPEC.md était un
registre de décisions vraies, sans ordre d'exécution — vingt-neuf décisions ne forment
pas une chaîne. Quatre éléments du chantier (7, 11, 12, 19) relèvent d'ailleurs de
l'architecture plutôt que du contenu. L'élément 12 (déclenchement du recalcul) est
absorbé ici. La hiérarchie de priorité (A-05) a été rejouée le 17/09/2026, l'élément 7
(gabarit de semaine) étant traité.

Méthode : parcours du trajet complet d'une donnée, de son entrée à l'écran, puis
balayage des modes de défaillance à chaque étape. Liste révisable comme celle du
chantier.

### A-01 — Pipeline

`observations → grandeurs → horizon → [garde-fou] → blocs → semaine → séances`

Chaque étage ne lit que les étages amont. Aucun étage aval n'écrit en amont.

**Le garde-fou (D-19) n'est pas un étage mais une porte**, placée entre horizon et blocs :
il autorise (vert), autorise en nommant le risque (orange) ou refuse et propose une
alternative (D-20). **Amendé le 17/09/2026 : il se rejoue en continu**, pas seulement à la
création du plan — un retard accumulé en mode date fixe (D-26) pousserait sinon à brûler
les étapes.

### A-02 — Absence de boucle, résolue par le temps
La circularité apparente (volume prescrit → séances réalisées → tolérance observée →
volume prescrit, G-PLA-002) n'en est pas une : les grandeurs se calculent **uniquement
sur le passé observé**, la prescription ne porte que sur le **futur**. Une séance
prescrite n'entre dans aucune grandeur tant qu'elle n'a pas été réalisée et observée.
Règle dure : **aucune valeur prescrite n'est jamais une observation.** Toute future
grandeur devra satisfaire ce test avant d'être admise.

**Limite de cette règle, découverte le 17/09/2026 (passe adverse, H-02).** A-02 interdit
qu'une valeur prescrite serve d'observation ; elle **n'interdit pas qu'une prescription
modifie le comportement qui produit l'observation**. Exemple : prescrire des montées plus
lentes amène le coureur à les courir plus lentement, ce que G-TER-001 enregistre comme un
coût en côte élevé — boucle réelle, non couverte par A-02. Aucune parade générale
n'existe ; l'atténuation est au cas par cas (pour G-TER-001, calibrer en priorité sur les
segments à haute intensité, où l'allure est contrainte par la physiologie plutôt que par
le choix). **Toute grandeur dont l'observation dépend d'un comportement que le plan
influence doit porter cette réserve explicitement.**

### A-03 — Déclenchement du recalcul (élément 12 du chantier)

| Événement | Recalculé |
|---|---|
| Nouvelle séance observée | grandeurs, puis semaine courante et suivantes |
| Statut de séance modifié ou détecté (D-43) | idem |
| Gêne déclarée (D-32) | grandeurs, plafonds de D-33, semaine courante |
| Indisponibilité datée déclarée ou modifiée (D-46) | blocs et semaines concernés |
| Module activé ou désactivé (D-30 nutrition, D-31 renforcement) | semaine courante et suivantes |
| Paramètre déclaré modifié (D-17), objectif ajouté ou requalifié (D-24) | tout, depuis l'horizon |
| Profil de course obtenu (D-27) | séances restantes du bloc spécifique uniquement (D-28) |
| Ouverture de l'app sans nouvelle donnée | **rien** — voir A-08 |

### A-04 — Recalcul intégral et idempotence
Tout est recalculé de zéro à partir des séances brutes, jamais mis à jour de façon
incrémentale. Volume réaliste (quelques centaines de séances par an) : le coût est
négligeable en navigateur, et l'absence d'état dérivé persisté supprime toute
désynchronisation possible entre ce qui est stocké et ce qui est vrai. **Idempotence
exigée** : deux calculs sur les mêmes données donnent un résultat identique.

### A-05 — Hiérarchie de priorité entre contraintes
Les contraintes peuvent devenir insatisfiables ensemble (ex. D-22 veut une sortie longue
à 40–45 % du volume en cœur de bloc, R-REN-005 impose 24–48 h entre séances dures, D-38
ne donne que trois jours disponibles en course). Ordre de cédage proposé, du plus intangible au plus négociable :

1. **Sécurité** — espacement des séances dures (R-REN-005), règle des 30 jours (D-63c,
   remplace D-22b le 22/09/2026) avec une seule séance de progression par semaine
   (D-63k1), plafonds de volume (D-21), volume d'affûtage fixé (D-63e). Ne cèdent
   jamais.
2. **Disponibilité déclarée** (D-38) et indisponibilités datées (D-46). Ne cèdent
   pas : le plan doit être exécutable.
3. **Volume cible** (G-PLA-002) — cède avant la structure.
4. **Composition de la semaine** — nombre et type de séances qualitatives.
5. **Part de la sortie longue** (D-22) — cède en dernier recours.

**Rejouée le 17/09/2026, l'élément 7 étant traité (D-35 à D-38).** Deux ajustements
issus du gabarit : les **jours déclarés des deux ensembles** (D-38) rejoignent le
niveau 2 (ne cèdent pas — le plan doit rester exécutable) ; le **jour de sortie longue**
(D-37) est au niveau 4, déplaçable avant que la part de sortie longue ne cède. Ordre
confirmé pour le reste. **Niveau : extrapolation.**
**Complété le 22/09/2026 (D-63i)** : quand la règle des 30 jours empêche d'atteindre le
volume cible, c'est le volume qui cède, et G-PLA-002 repart du volume réellement
prescriptible au lieu de gonfler un volume jamais couru. **Et (D-63k3)** : après un
symptôme, le seuil se fige sur le volume réellement couru, jamais sur la cible.

### A-06 — Aucune solution : dégrader et expliquer, jamais échouer
Si aucune combinaison ne satisfait les niveaux 1 et 2, le plan est produit dégradé —
volume réduit, séances fusionnées — avec l'explication en clair et, le cas échéant, le
passage du garde-fou en orange ou rouge (D-19, D-20). Même principe que D-20 : jamais un
mur, toujours une alternative chiffrée.

### A-07 — Stocké contre recalculé
**Précision du 17/09/2026, issue de l'écriture du schéma de données (SCHEMA.md).**
« Séances brutes » était ambigu et matériellement intenable : une trace GPS à 1 Hz sur
une année représente plusieurs millions de points, que le stockage navigateur n'absorbe
pas et dont le recalcul complet contredirait A-14. Distinction à appliquer : ce qui est
dérivé **du signal seul** (découpage en segments, pente, allure, écarts-types) est
déterministe, ne dépendra jamais d'un coefficient, et **est stockable** ; ce qui est
dérivé **du modèle** (%VC, admissibilité, pondération, coût-pente, confiance, volume
cible) ne l'est **jamais** — sinon un seuil modifié laisserait survivre des valeurs
calculées avec l'ancien, en violation de A-13. On stocke donc une **normalisation par
séance au niveau segment**, antérieure à tout seuil.

**Stocké** : séances normalisées en segments (SCHEMA.md), statuts de séance (D-43), les neuf
paramètres déclarés (D-17, D-38, D-47), objectifs et leurs statuts (D-24), profil de
course (D-27), notes de ressenti (G-RES-001), entrées de gêne — localisation et intensité
(D-32), indisponibilités datées (D-46), saisies de nutrition et carnet produits (D-30),
état activé/désactivé des modules (D-30, D-31), plan publié en cours (A-08).
**Complété le 17/09/2026** : l'inventaire initial datait d'avant D-30 à D-47 et omettait
six catégories.
**Recalculé** : toutes les grandeurs, tous les coefficients, tous les niveaux de
confiance, l'état du garde-fou, la date projetée (D-26).

### A-08 — Stabilité du plan
Un plan qui change à chaque ouverture détruit la confiance, même si chaque changement est
justifié. Règles :
- le plan **publié** (les séances fermes, A-09) est stocké et ne bouge pas sans
  événement déclencheur listé en A-03 ;
- une variation de grandeur inférieure au seuil de stabilité (D-13a) **ne republie pas**
  le plan ;
- quand le plan change, l'app dit **ce qui a changé et pourquoi**, en une ligne.

### A-09 — Horizon de prescription
Deux zones : les séances **fermes** (une semaine, deux au maximum) affichées en détail
et stables au sens de A-08 ; au-delà, une **trame indicative** (type et volume par
semaine, sans détail de séance) qui peut évoluer librement. Motif : prescrire finement
à trois mois donne une précision que le modèle n'a pas.

### A-10 — Ce qui est testable, et ce qui ne l'est pas
**Testable** : cohérence interne (contraintes respectées, aucune séance absurde),
progressivité (règle des 30 jours D-63c et pic de D-21 jamais franchis ; renvoi corrigé
le 23/09/2026), idempotence (A-04),
déterminisme (A-12), robustesse aux données aberrantes (A-15).
**Non testable** : l'**efficacité** du plan. Un coefficient se vérifie contre une
observation ; un plan ne se vérifie que contre une course, trois à cinq fois par an.
Limite **structurelle assumée**, pas un défaut à corriger : l'app ne pourra jamais
démontrer que son plan était le meilleur, seulement qu'il était cohérent et sûr.

### A-11 — Jeux de test
Coureurs fictifs couvrant les cas limites, rejoués avant chaque livraison : débutant sans
données ; coureur avec historique d'un an périmé ; coureur route pur (aucune observation
en pente) ; deux jours disponibles seulement ; cible déclenchant le rouge ; coupure de
six semaines en milieu de préparation ; profil de course obtenu tardivement ; volume
déclaré sans aucun import.
**Ajoutés le 17/09/2026**, issus des décisions postérieures : coureur qui ne déclare
jamais de gêne (angle mort de D-33, le modèle doit se rabattre sur la lecture
systémique) ; coureur en plaine visant une cible à fort D+ (condition orange de D-47) ;
modules nutrition et renforcement désactivés (D-30, D-31) ; deux ensembles de jours
structurellement incompatibles (D-38) ; cible sans GPX jusqu'à la fin du bloc spécifique
(D-28, aucune alerte attendue) ; terrain très technique où presque aucun segment ne passe
le filtre de régularité (D-49b).
**Ajoutés le 17/09/2026 avec le module blessure** : contrainte médicale périmée sans
réévaluation (D-50, l'app doit retomber au plus conservateur) ; arrêt complet sans
substitution pendant 8 semaines puis remontée ; remontée où le coureur ne déclare jamais
l'absence de symptôme (la progression doit rester bloquée, pas avancer) ; blessure
survenant pendant le bloc spécifique à 6 semaines de la cible.

### A-12 — Déterminisme
Aucun aléatoire non maîtrisé dans la génération. Si une variation est souhaitée (choix
entre deux séances équivalentes), elle est dérivée d'une graine stable, jamais tirée à
l'exécution.

### A-13 — Versionnement du modèle
Changer un coefficient alors que de l'historique existe modifierait rétroactivement des
plans passés. Règles : chaque plan publié porte la **version de modèle** qui l'a produit ;
les grandeurs sont recalculées avec la version courante, mais les plans passés ne sont
jamais réécrits ; un changement de version est visible et daté. Les **observations
brutes ne sont jamais migrées** — seul le calcul change, jamais la donnée.

### A-14 — Budget de calcul
Recalcul complet ciblé sous ~200 ms sur un mobile de milieu de gamme, pour quelques
centaines de séances. **Revérifié le 17/09/2026** après l'ajout de la pondération par
régularité (D-49b/H-01) et des régressions par bande de pente : l'ordre de grandeur reste
quelques milliers d'opérations, sans effet sur la cible. Contrainte de lisibilité (R-MET-002) prioritaire sur
l'optimisation : aucune structure opaque pour gagner quelques millisecondes.

### A-15 — Données aberrantes
Filtres explicites avant toute entrée dans une grandeur : vitesses impossibles,
altitudes incohérentes, durées démesurées (pause oubliée), séances vides, doublons
d'import. Une observation rejetée est **marquée et visible**, jamais supprimée
silencieusement — le coureur doit pouvoir la réintégrer s'il s'agit d'un faux positif.

### A-16 — Traçabilité
Toute séance prescrite doit pouvoir répondre à « pourquoi celle-ci » : bloc en cours,
motif (D-29), grandeurs mobilisées et leur niveau de confiance, contraintes ayant cédé
(A-05). Exigence déjà posée par R-MET-002 (chaque coefficient lisible et discutable),
étendue ici à la décision complète.


**D-77 — Lecture des activités de la montre via intervals.icu (v25, 15/10/2026).** Chaîne :
Garmin Fenix 7 → Garmin Connect → intervals.icu → fonction Supabase `intervals-activities` →
Ascend. (a) *Lecture seule, activités seulement* : la fonction ne demande à intervals.icu que
la liste des activités (durée, distance, D+, FC) ; aucune donnée de santé (sommeil, VFC, poids)
ne transite par Ascend, même si elles sont importées dans intervals.icu à la demande
d'Antoine. (b) *Clé d'API* : uniquement dans le secret Supabase `INTERVALS_API_KEY`, jamais
dans le dépôt, dans l'appli ou dans le navigateur ; « Verify JWT » reste activé (utilisateur
connecté exigé). (c) *L'appli recommande, l'utilisateur décide* : l'écran Jour propose les
sorties des 7 derniers jours (bouton « Récupérer mes séances ») ; chacune n'entre dans le
suivi que par « Ajouter », qui ouvre la saisie pré-remplie où l'effort reste à noter. Aucune
séance n'est créée automatiquement. (d) *Doublons* : une activité est masquée si une séance
porte déjà son identifiant (`ext`, « icu:… ») ou si une séance du même jour a une durée à ±2 min
(même règle que l'import CSV Garmin). (e) *Rattachement* : si une seule séance prévue ce jour-là
est du même genre (course ou renforcement) et non réalisée, elle est rattachée d'office ; sinon
le menu « Rattacher à une séance prévue » reste à choisir. (f) *Type* déduit du type
intervals.icu et du titre (course à pied : « Sortie longue » à partir de 90 min, sinon
« Endurance » ; musculation/CrossFit : « Renforcement »). (g) Moteur inchangé. Les séances
gardent `src:'intervals'` et `ext`. Limites connues : D− non fourni (reste vide) ; fenêtre
de 7 jours (30 jours sur demande, bouton « Chercher sur 30 jours ») ; envoi du plan vers la montre non fait (v27).

**D-78 — Envoi d'une séance prévue vers la montre (v27, 15/10/2026).** Chaîne inverse de D-77 :
Ascend → fonction Supabase `intervals-event` → calendrier intervals.icu (événement WORKOUT) →
Garmin Connect → Fenix 7. (a) *Une séance à la fois, sur demande* : bouton « Envoyer sur ma montre »
sur la fiche d'une séance de course prévue (aujourd'hui ou plus tard, non réalisée) ; « Retirer »
la supprime d'intervals.icu. Aucun envoi automatique : l'appli recommande, l'utilisateur décide.
(b) *Identifiant* : `external_id = ascend:<id de la séance>` ; renvoyer met à jour l'événement
existant au lieu d'en créer un second ; la fonction ne touche jamais un événement dont
l'identifiant ne commence pas par `ascend:`. (c) *Contenu* : le déroulé de `sessionSteps` converti
en texte intervals.icu (durées seulement, sans cible de FC ni d'allure, nom de l'étape en
en-tête, `Nx` pour les répétitions). (d) *Suivi* : `profile.sent[id] = {date, dur, at}` ; si la date
ou la durée prévues changent après l'envoi, la fiche indique « le plan a changé : renvoie ».
Le renvoi n'est pas automatique. (e) *Fenêtre* : la fonction accepte de hier à +60 jours ; la
fenêtre réellement acceptée par Garmin est à mesurer sur la Fenix (non documentée). (f) Moteur
inchangé. Limites : pas de cible de FC dans la séance envoyée ; pas d'envoi de la semaine
entière ; pas de suppression automatique d'une séance déplacée ou supprimée par le moteur.

**D-79 — D+ d'une séance affiché en fourchette (décidé le 15/10/2026, affichage en v29).**
Le D+ prévu d'une séance de course s'affiche en fourchette : ± 10 % du repère, au moins
± 50 m, au plus ± 150 m, bornes arrondies à 50 m (300 m → 250 à 350 m ; 1 500 m → 1 350 à
1 650 m ; 3 000 m → 2 850 à 3 150 m). Convention (H-50). La première proposition (± 20 %)
a été écartée par Antoine : ± 600 m sur 3 000 m n'a pas de sens. Une course (type `race`)
n'a pas de fourchette : son D+ est celui du parcours.

**D-80 — Écran Aujourd'hui (v28, 15/10/2026).** Accueil et Jour fusionnés ; 4 onglets :
Aujourd'hui, Semaine (ex-Séances), Suivi, Profil. Jour devient « Journal » (les autres jours),
accessible par un lien en bas d'Aujourd'hui. (a) *Ordre* : alertes (garde-fou, séances non
saisies, écarts, bilan de phase), puis la séance du jour, « À compléter » (effort non noté,
14 derniers jours), séances hors plan du jour, « Cette semaine » (7 jours, état de chaque
séance), Journal du matin si le module est actif, « Ma montre », objectif. (b) *Séance du
jour* : type, durée, D+, consigne, « Pourquoi » (texte du moteur, sans code de phase), bouton
principal « J'ai fait ma séance » ; liens « Vers ma montre » (D-78) et « Pas faite » (D-72).
La carte entière ouvre la fiche (fin du lien « Détail »). Seconde séance du jour : carte
compacte. Faite : réalisé, effort, et la séance suivante. Pas de séance : « Repos » et la
prochaine séance. Journée malade/blessé/indispo : la carte de statut remplace la séance ;
le statut se choisit par « Malade, blessé ou indisponible ? ». (c) *Montre d'abord* : à
l'ouverture, Ascend lit en silence les activités des 7 derniers jours (D-77, lecture seule,
erreurs non affichées). Si une activité de course du même jour correspond à une séance
prévue (du jour ou non saisie), la carte affiche « Ta montre · durée · km · D+ » et le
bouton devient « Noter mon effort » : saisie pré-remplie, l'effort reste à noter. Rien n'est
enregistré sans action d'Antoine. (d) *Après l'enregistrement* d'une course, un message dit
ce que le plan prévoit ensuite (prochaine sortie longue après une sortie longue). (e) *Journal
du matin* : nouveau module, **désactivé par défaut**, y compris pour les profils existants
(sommeil, énergie, jambes, envie, FC repos, poids). Le moteur ne lit pas ces notes ; le
statut du jour et le module blessure restent hors du module. Moteur inchangé.

**D-81 — Nom de la séance envoyée à la montre (15/10/2026).** Format `AAAAMMJJ_TYPE_D<D+>` :
date ISO 8601 basique (unique sur 12 mois, tri alphabétique = tri chronologique), code du type
(EF, SL, QUAL, DESC, COURSE, CF), puis le D+ repère (pas la fourchette) s'il existe. 2e séance le
même jour : `AAAAMMJJ-2_TYPE`. Exemples : `20261018_SL_D300`, `20261016_EF`. Le `+` est remplacé
par `D` (demande d'Antoine). Longueur : 17 caractères visibles mesurés sur la Fenix 7 (« Sortie
longue 109 » coupé après le 9) ; jusqu'à 20 supposés, non mesurés. Le vrai identifiant reste
`ascend:<id>` (external_id). Le séparateur `_` et les codes sont une convention, pas une norme.

**D-82 — Fiche séance (v29, 15/10/2026).** Trois blocs : *À faire* (déroulé, puis les consignes :
note de séance, D+, effort, FC, nutrition si le module est éteint), *Pourquoi* (texte du moteur,
sans codes de phase ni de règle), une carte *Nutrition* (module actif). Le D+ prévu s'affiche en
fourchette D-79 : sur la fiche (« 200–300 m de D+ repère ») et sur Aujourd'hui (« 200 à 300 m de
D+ ») ; une course garde son D+ de parcours. « Pas faite », « Déplacer », « Remettre au… » et
« Exporter le fichier Garmin » passent dans le menu ⋯ (plus de lien « Séance manquée ? »). Le
bouton principal s'appelle « J'ai fait ma séance » comme sur Aujourd'hui. La phrase « D+ repère :
environ N m » et la ligne « Joins la trace TCX » quittent les consignes (la saisie gère la trace).
Une seule nutrition : la carte si le module est actif, la ligne de consigne sinon. Moteur inchangé ;
le texte exporté (`planText`) n'a plus de ligne D+. Point ouvert : la carte (35 g/h) et la ligne
du module éteint (60 g/h) viennent de deux règles différentes (`nutriFor` / `sessionSteps`).

**D-83 — Semaine en liste de 7 jours (v30, 15/10/2026).** L'onglet Semaine affiche une carte de
synthèse (séances faites / prévues, minutes de course, D+ réalisé / prévu), puis les 7 jours du
lundi au dimanche : jour, icône, titre, ligne de détail (durée, D+ en fourchette D-79 ; pour une
séance faite, durée, D+ et effort réels), et un statut (Fait, Manquée, Annulée, ou › pour ouvrir
la fiche). Un jour sans séance s'affiche « Repos » (« Indisponible » si le statut du jour l'est) ;
le jour courant est surligné, deux séances le même jour partagent le même fond. Navigation de
semaine, alerte du garde-fou et « Ajouter une séance prévue » inchangés. Moteur inchangé.

**D-82 amendé (v31, 15/10/2026) — Fiche séance en deux sections, sans menu ⋯.** Après revue des
maquettes : en-tête avec « × » et « Déplacer » (si un autre jour libre existe ; « Remettre au … »
dans le cadre de déplacement), chiffres de la séance, puis **1 · Ta séance** (carte de la montre :
« Envoyer » / « Renvoyer » / « Retirer de la montre » ; sans connexion intervals.icu, « Fichier
Garmin » en secours ; À faire ; Pourquoi ; nutrition réduite à la cible) et **2 · Résultat de la
séance** (le jour même ou après : « Récupérer depuis ta montre » si une sortie du jour est lue
dans intervals.icu, « Saisir à la main », « Pas faite » ; séance faite : « Réalisé »). À faire :
un bloc unique s'annonce en une ligne (« 1 h 50 d'endurance continue ») ; une séance structurée
affiche une barre de déroulé et sa légende. Nom de la montre : `profile.watchName` s'il existe,
sinon « Ta montre » (écran Matériel à venir). Durée prévue affichée en heures et minutes.

**D-84 — Endurance et sortie longue en un seul bloc (v31, 15/10/2026).** Demande d'Antoine :
une endurance ou une sortie longue n'a ni échauffement ni retour au calme structurés (avant :
10 + 5 min et 15 + 5 min) ; la consigne dit « départ tranquille : les premières minutes servent
d'échauffement ». Les séances de qualité (côtes, intervalles, tempo, montées) gardent leur
échauffement et leur retour au calme (moteur inchangé). La séance envoyée à la montre suit (un
seul pas). Convention, sans source qui montre un bénéfice d'un retour au calme structuré après
un effort facile.

**D-85 — Saisie : effort avec repères, nutrition par séance (v31, 15/10/2026 ; précise D-76).**
(a) *Effort* : boutons 1 à 10 sur une rangée (D-76 inchangé) avec des repères visibles avant le
choix sous 1, 3, 5, 7 et 10 (Très facile, Modéré, Dur, Très dur, Maximal), aux places des repères
de l'échelle CR-10 ; libellé du chiffre choisi dessous. L'échelle en 4 mots a été écartée : le
moteur utilise le chiffre (charge durée × effort, effort des endurances comme signal de fatigue).
(b) *Nutrition* : un interrupteur « J'ai suivi ma nutrition sur cette séance », activé par défaut,
remplace les trois réponses ; désactivé = « Non suivi » (champs vidés). « Rien pris » devient
« suivi, 0 g ». La progression de la cible ne compte toujours que les sorties avec des glucides
pris (> 0 g). (c) Champ libre « Détail de ce que tu as pris » (`nutriNote`), non lu par le moteur.
(d) Champ « Coup de mou » retiré (demande d'Antoine du 27/09/2026, jamais appliquée).

### D-86 — Profil en 7 sous-écrans, édition en place (v32, 16/10/2026)
Maquettes validées par Antoine le 16/10/2026 (home, semaine_v3, toi_v5, toi_v5_roue, acc_1, materiel2, donnees, avances).
(a) *Accueil* : carte objectif (nom, J−n, distance, D+, début du plan) puis une liste de 7 entrées :
Ton objectif, Ta semaine, Toi, Tes modules, Ton matériel, Données et synchro, Réglages avancés.
(b) *Ta semaine* : jours en carrés L M M J V S D (course, sortie longue, renforcement si le module est actif),
lecture seule ; « Modifier » ouvre la fenêtre existante, qui garde l'aperçu des 14 prochains jours.
Phases en accordéon, la phase en cours ouverte par défaut ; fermée : nom, dates, badges « en cours » /
« jours propres ». Ouverte : description (PHASES), conseil, jours, « Modifier les jours de cette phase »,
bilan de phase. Le texte « logique du plan » par phase est reporté à la version consacrée aux textes.
(c) *Toi* : chaque champ se modifie en place et s'enregistre à la sortie de la case, sans aperçu du plan
(ces réponses ne calent que les premières semaines). Choix fermés en pastilles, durées par une roue
heures + minutes (course passée : 0 à 72 h, pour couvrir la Diagonale des Fous, 66 h ; plus longue sortie :
0 à 24 h ; durée moyenne : 0 à 6 h). Courses passées dépliables (fermée : nom, durée · km · D+ · date) ;
badge « référence » sur la course retenue par le moteur (km-effort le plus proche de l'objectif, même calcul que refC).
Champ `name` ajouté aux courses passées (non lu par le moteur).
(d) *Tes modules* : accordéon, interrupteur sur chaque carte ; ouvert : pourquoi, ce que ça change, réglages.
(e) *Ton matériel* : « Tu cours avec une montre ? » Oui/Non (`hasWatch`, oui par défaut). Non = pas de carte
montre ni de « Récupérer depuis ta montre » dans la fiche séance. `watchName` rempli depuis le champ `device`
de intervals-activities (champ `device_name` d'intervals.icu) s'il est vide ; modifiable.
(f) *Données et synchro* : sauvegarde, exports (CSV journal masqué si le module journal est éteint), imports.
(g) *Réglages avancés* : redémarrer le plan, tout effacer, tout retélécharger.
(h) Correctif : la fonction d'étiquette « Ta montre » portait le même nom que `watchName(ps)` (D-81) et
l'écrasait ; renommée `watchLabel()`.
(i) v33 (16/10/2026), correctif : la classe CSS `.wl` de la roue de durée écrasait celle de la liste de la
Semaine (D-83), qui s'affichait comme une roue. Roue renommée `.whl`. Avant chaque livraison, les classes
CSS ajoutées sont désormais comparées à celles qui existent déjà.

### D-87 — Profil, retouches après essai (v34, 16/10/2026)
Maquettes validées par Antoine le 16/10/2026 (home_v3, objectif_v2, objectif_confirm, semaine_v4, bilan_v2).
(a) Accueil : les sous-titres disent à quoi sert la rubrique (plus de données recopiées). Carte objectif
visuelle : fond vert foncé, jours restants, distance / D+ / jalon en pastilles, frise des phases avec un repère
« semaine n sur N ».
(b) Ton objectif : lignes modifiables comme dans Toi ; courses intermédiaires dépliables avec statut en pastilles.
Un changement de date, distance, D+ ou statut passe par « Ce que ça change » (14 prochains jours, `planDiff`)
avant d'être enregistré ; sans effet sur 14 jours, il est enregistré directement. Le nom s'enregistre sans confirmation.
(c) Ta semaine : un seul bouton « Modifier mes jours » ouvre une fenêtre unique (course, sortie longue,
renforcement), avec l'aperçu existant. Phases : titre de section hors de la carte, frise verticale (point coloré
par phase, orange pour la phase en cours), durée en semaines.
(d) Bilan de phase : proposé seulement pendant les 2 dernières semaines de la phase (règle `fenetre` existante ;
le lien de Ta semaine l'ignorait en v32-v33). Il doit arriver avant la phase suivante, pas après : il sert à décider
des jours de cette phase. Contenu allégé : date de début, ce qui change, 2 chiffres sur la phase finie,
recommandation s'il y en a, jours en carrés, « Modifier » / « Garder ces jours ».
