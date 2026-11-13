# HYPOTHESES.md — Registre des hypothèses non prouvées — Ascend

Construit le 17/09/2026. Motif : les extrapolations sont dispersées dans SPEC.md, à
raison d'une ou deux par décision, ce qui les rend invisibles **comme ensemble**. Ce
fichier les rassemble pour qu'on puisse juger, en une page, de ce sur quoi le modèle
s'avance sans preuve.

Ce n'est pas un doublon de SOURCES.md, qui recense ce qu'on **sait**. Celui-ci recense
ce qu'on a **décidé sans savoir**.

## Méthode d'extraction

Balayage automatique de SPEC.md sur les mentions `extrapolation`, `niveau : faible`,
`sans objet` et `à vérifier`, bloc par bloc (49 décisions, 9 grandeurs, 16 sections
d'architecture). 27 blocs ressortent. Chaque hypothèse est ensuite qualifiée à la main
sur deux axes :

- **Portée** — combien d'autres décisions s'écroulent si elle est fausse.
- **Détectabilité** — l'erreur se verrait-elle, et au bout de combien de temps.

La priorité d'audit est le croisement des deux : forte portée + faible détectabilité
d'abord. Une hypothèse fausse mais qui se voit en trois semaines est moins dangereuse
qu'une hypothèse fausse qui ne se voit jamais.

---

## Priorité 1 — forte portée, faible détectabilité

Les quatre hypothèses à éprouver avant toute autre.

### H-01 — Les seuils de régularité de segment (D-49b)
**Hypothèse** : cadence stable à ±5 %, allure stable à ±10 %, segment ≥ 60 s, une seule
bande de pente → le segment est exploitable pour apprendre.
**Portée** : maximale. Filtre l'entrée de G-TER-001, G-FAT-001 et de toute observation
FC. Si le filtre est mauvais, **tous** les coefficients terrain et fatigue sont faux.
**Détectabilité** : très faible. Trop strict → rien ne converge, et on l'attribuera au
manque de données. Trop laxiste → les coefficients sont pollués mais ont l'air normaux.
**Ce qui la testerait** : taux de segments admis sur des données réelles de trail
technique, comparé à du terrain roulant.

### H-02 — L'effort (%VC) est uniforme d'une bande de pente à l'autre sur un segment régulier
**Hypothèse** : c'est le mécanisme d'identification de G-TER-001 — un écart systématique
sur une bande révèle une correction de pente fausse.
**Portée** : forte. C'est l'apport le plus original du modèle (D-28), et rien d'autre ne
calibre le coût-pente.
**Détectabilité** : faible. L'hypothèse peut être fausse pour une raison physiologique —
un coureur peut *volontairement* lever le pied en côte sans que sa correction de pente
soit en cause. On mesurerait alors sa stratégie d'allure, pas son coût énergétique.
**Aucune source ne l'appuie** : posée par nous.

### H-03 — Le seuil de stabilité à 5 % sur 5 observations (D-49a)
**Hypothèse** : en dessous, une estimation est fiable.
**Portée** : forte. Décide quand l'app devient directive (D-42) et quand le plan se
republie (A-08).
**Détectabilité** : faible, et **asymétrique** — trop laxiste, l'app est confiante et
fausse, ce qui ne se voit qu'à l'échec d'une course.

### H-04 — Le coût-pente est beaucoup moins périssable que la capacité aérobie (D-16)
**Hypothèse** : pleine valeur à 6 mois, ignoré à 3 ans — contre 3 semaines et 6 mois pour
la vitesse de référence.
**Portée** : forte pour tout coureur reprenant après une coupure.
**Détectabilité** : très faible — il faudrait comparer un coût-pente mesuré avant et
après une longue interruption.
**Aucune source** : le raisonnement (efficacité mécanique vs transport d'oxygène) est
plausible mais non vérifié. Déjà signalé dans SPEC comme la ligne la plus fragile du
tableau.

---

## Priorité 2 — forte portée, détectabilité correcte

### H-05 — Structure de blocs par tranche de durée (D-21, D-44)
Durées de bloc spécifique et volumes par phase. **Un seul ancrage réel** (50 km → 6-8
semaines) ; 60-100 km interpolé entre deux points distants ; 10-21 et 21-42 km sans
aucun ancrage. Se verrait sur un plan manifestement sur- ou sous-dimensionné.

### H-06 — Part de la sortie longue et sorties clés (D-22)
30-45 % selon la phase, 2-3 sorties clés au-delà de 42 km. Parts et durées cibles posées
par nous. Se verrait rapidement à l'usage.

### H-07 — Répartition des intensités transposée à l'ultra (D-34)
Les cibles viennent d'études sur 5 km à marathon (S-COU-008, S-COU-009). **Aucune étude
ne couvre l'ultra-trail**, et le glissement polarisé → pyramidal extrapole une tendance
observée sur des distances bien plus courtes.

### H-08 — Budget d'affûtage à 20 % et 6-8 semaines de construction (D-25)
La durée de l'affûtage est bien documentée (S-COU-006) ; **le nombre d'affûtages
tolérable par an ne l'est pas du tout**, ni les durées de récupération post-course du
tableau.

### H-09 — Facteur trail/route de 1,2 à 1,4 (D-44)
Convention de coachs pour la comptabilité de fatigue, sans validation. Amorçage
seulement, remplacé par la tolérance observée — ce qui limite les dégâts.

---

## Priorité 3 — portée limitée ou correction rapide

| # | Hypothèse | Décision | Remarque |
|---|---|---|---|
| H-10 | Cadence de relâche 3:1 | D-57b (ex-G-PLA-001, **abandonnée**) | règle fixe assumée, recalée à rebours depuis l'affûtage (D-63f) ; plus corrigée par l'observation |
| H-11 | Progression nutrition 5-10 g/h par semaine | G-NUT-001 | protocole de traduction pratique, pas un essai |
| H-12 | Fenêtre de contamination 24-48 h | G-CHG-001 | amorçage R-REN-005, déduite ensuite |
| H-13 | Périodisation du renforcement par phase | D-39 | convergence de coachs, pas d'étude comparative |
| H-14 | Seuil de marche à 25-30 % de pente | D-40 | cohérent avec S-COU-011, borne exacte posée |
| H-15 | Plancher à 85 % du meilleur niveau atteint | D-15 | garde-fou prudent, erreur peu coûteuse |
| H-16 | Hiérarchie de priorité entre contraintes | A-05 | se corrige à l'usage, visible immédiatement |
| H-17 | Modèle de surveillance de la douleur étendu à toute gêne | D-32 | source solide (S-BLE-001) mais population tendinopathie |
| H-18 | Seuils du garde-fou (1,5× et 2,5×) | D-19 | le 2,5× est le plus arbitraire, déjà signalé |
| H-19 | Périodes d'observation par grandeur | D-23 | déduites d'une fréquence d'entraînement plausible |
| H-20 | Deux questions terrain suffisent | D-47 | corrigées par l'observation dès les premières semaines |

---

## Ajouts du 22/09/2026 — articulation G-PLA-002 / calendrier (D-63, D-35)

Dix hypothèses introduites par D-63 et son amendement. Toutes ont été **éprouvées en
simulation** (TESTS.md, huitième et neuvième séries), ce qui vérifie leur mécanique et
leurs interactions — **pas leur justesse physiologique** : le simulateur ne modélise la
fatigue que par le volume hebdomadaire.

| # | Hypothèse | Décision | Portée | Détectabilité | Priorité |
|---|---|---|---|---|---|
| H-21 | La règle des 30 jours, établie **en distance sur route**, vaut **en durée en trail** ; une séance de 30 min est toujours permise | D-63c | forte : c'est le garde-fou de sécurité principal | **très faible** — une blessure évitée ne se voit pas | **1** |
| H-28 | **Une seule** séance de progression par semaine suffit à neutraliser les hausses enchaînées | D-63k1 | forte | faible | **1** |
| H-29 | Le ressenti mesuré en semaine allégée reflète l'état reposé ; plafonner sa remontée à +5 % évite de masquer un surmenage installé ; une alerte due au seul calage de la référence peut être effacée de la mémoire | D-63k4 et amendement | forte : pilote tout le volume | moyenne | **1** |
| H-22 | Découpages d'affûtage 65/45 (2 sem.) et 70/55/40 (3 sem.) ; 3 semaines pour 8–20 h | D-63e, k7 | moyenne | moyenne (performance du jour J, un seul essai par objectif) | 2 |
| H-23 | Reprise : max(65 % ; 1 − 0,07 × (n − 1)), appliqué au volume, au seuil et à la référence des 30 jours | D-63h, k5 | moyenne | bonne (symptômes à la reprise) | 2 |
| H-24 | Consolidation : ne plus sonder la limite en bloc spécifique | D-63g | moyenne | bonne | 3 |
| H-25 | Grille d'allègement à rebours T−4, T−8… | D-63f | faible | bonne | 3 |
| H-26 | Marge de 3 semaines sur la rampe de sortie longue, entretien du niveau nécessaire | D-63d, k6 | moyenne | bonne (sortie clé atteinte ou non) | 3 |
| H-27 | Parts de sortie longue par défaut, part ≥ 1/n, alternance au-delà de 3 h | D-22, D-63d | faible | bonne | 3 |
| H-30 | Un coureur qui ne saisit pas son ressenti la moitié du temps ne doit plus voir son volume sonder sa limite | D-63 amendement | moyenne | **très faible** — sans ressenti, rien ne signale l'excès | 2 |
| H-31 | Seuil de 3 séances consécutives pour l'alerte visible, relance tous les 3 manques supplémentaires | D-64 | faible (produit, pas sécurité — la sécurité tient sur D-63/H-30) | bonne, le coureur voit vite si le seuil est mal calé | 3 |
| H-32 | Un rattrapage a posteriori éteint l'alerte mais n'alimente jamais G-PLA-002 | D-64c | faible | faible — un coureur pourrait ne jamais remarquer que ses notes tardives ne comptent pas | 3 |

**Ce qui les testerait** : H-21 et H-28 — une cohorte trail avec durée ET distance, qu'on
n'a pas ; en attendant, suivre dans l'app les gênes signalées (D-32) après chaque séance
record. H-29 — comparer le ressenti des semaines allégées à celui des 4 premières semaines
sur des données réelles : s'il dérive vers le haut sur plusieurs mois, le plafond de +5 %
se déclenche et il faut regarder pourquoi. H-22 — aucune donnée individuelle ne pourra le
trancher (un affûtage par objectif) : reste une extrapolation durable.

---

## Sources encore non vérifiées

Distinct des hypothèses : ici on a cité une source sans avoir pu confirmer sa référence
primaire. Tant qu'elles ne sont pas vérifiées, les décisions qu'elles fondent sont au
même niveau qu'une extrapolation.

| Source | Fonde | État au 17/09/2026 |
|---|---|---|
| S-COU-004 | G-FAT-001 — **grandeur entière** | **VÉRIFIÉE** — Smyth et coll., Sports Medicine 52(9), 82 303 coureurs. Niveau élevé sur route |
| S-TRA-001 | G-TER-001, rejet de la courbe générique | **VÉRIFIÉE** — deux articles Balducci (2016, 2017), niveau modéré |
| S-MES-002 | D-09, D-10, admissibilité FC | **VÉRIFIÉE** — Navalta et coll., PLoS ONE 15(8). Réserve : parcours de 3,22 km seulement |
| S-REN-006 | D-39 | **VÉRIFIÉE et corrigée** — Berryman et coll., IJSPP (pas Sports Medicine). Devient exploitable |
| S-TRA-003 | contexte de D-19 | **non retrouvée** — usage contextuel seulement, à retirer si elle reste introuvable |
| S-TRA-006 | D-28, spécificité croissante | **VÉRIFIÉE le 22/09/2026** — Jaén-Carrillo et Margarit-Boscà, résumé, n = 1, niveau faible confirmé |

**Bilan de la vérification** : quatre sources sur six confirmées, dont les deux qui
portaient le plus de poids (G-FAT-001 et G-TER-001). Deux restent introuvables, mais
aucune des deux ne porte une grandeur : S-TRA-003 n'est que contextuelle, S-TRA-006
appuie une décision qui tient par ailleurs sur S-TRA-005.

**Gain inattendu** : S-REN-006, jusque-là inexploitée, s'avère être une méta-analyse de
28 études de niveau élevé qui **fonde directement** le choix de la force maximale en
début de bloc spécifique (D-39) — celui-ci reposait jusqu'ici sur une simple convergence
de coachs.

---

## Ce que ce registre ne couvre pas

Les erreurs de **raisonnement** plutôt que de preuve : appliquer un principe juste au
mauvais cas, ou tirer d'une source une conclusion qu'elle ne porte pas. Elles ne laissent
aucune trace détectable automatiquement — les cinq relevées jusqu'ici l'ont toutes été
par la relecture humaine, aucune par un contrôle. Ce registre réduit la surface, il ne
la ferme pas.


---

## Ajouts du 23/09/2026 — finalisation v1 (D-65)

| # | Hypothèse | Décision | Portée | Détectabilité | Priorité |
|---|---|---|---|---|---|
| H-33 | Après affûtage + récupération d'un secondaire, la référence des 30 jours vaut le maximum d'avant × max(0,65 ; 1 − 0,07 × (n − 1)) | D-65a | moyenne | faible — même cécité que H-21 | 2 |
| H-34 | Départ à min(3 ; jours) × 30 min en marche-course ; fréquence avant durée sous 1,2 × « tout au plancher » ; relâche ≥ 2 × 30 min | D-65b | moyenne | bonne (gênes des premières semaines) | 2 |
| H-35 | Un coureur au ressenti très bruité doit rester prudent plutôt que suivre sa tolérance ; σ ≥ 0,10 au repos le signale | D-65c | faible (information) | bonne | 3 |
| H-36 | Le D+ monte en fond (≈ 8 dernières semaines) et se stabilise en bloc | D-65e | forte en trail | moyenne (gênes en entrée de bloc) | **1** |
| H-37 | Le coût propre de la sortie longue et du D+ se lit dans le ressenti ; aucun coefficient permanent n'est nécessaire | D-65e | forte | moyenne — sur données réelles, comparer le ressenti des semaines à sortie clé aux autres | **1** |

**Ce qui les testerait** : H-36 et H-37, tes propres données — si le ressenti monte
nettement les semaines de sortie clé à volume égal, le coût propre existe et la ligne
orange de D-19 doit se déclencher avant la S41.


## Hypothèses de la refonte du moteur (septembre 2026)

Ajoutées le 29/09/2026 (D-66 à D-71). Priorité 1 = à tester en premier (portée forte ou détectabilité faible).

| # | Hypothèse | Décision | Portée | Détectabilité | Priorité |
|---|---|---|---|---|---|
| H-40 | Reprise : une séance sortie de la fenêtre des 30 jours garde un repère qui baisse de 1 % par jour dès le 31e jour (nul au 130e), calculé au jour de la séance ; ce repère n'autorise pas de séance de plus d'1 h (2 × le plancher de 30 min) — au-delà, règle des 30 jours stricte. Après une pause déclarée, le volume de départ est réduit à 65 % (moins de 2 semaines) ou 50 %. Convention : la pente est plus rapide que la baisse de VO2max (S-COU-005) car elle vise la tolérance des tissus, non mesurée ; Frandsen 2025 (S-BLE-004) ne dit rien de la durée de la première séance après une coupure. Réécrite le 09/11/2026 (D-94), remplace le repère dégressif de 7 % par semaine (plancher 65 %) | D-94, D-63k5 | forte : première sortie après une coupure | faible — une blessure évitée ne se voit pas | **1** |
| H-41 | La densité de D+ de départ vaut au plus la moitié de celle de la course, puis monte linéairement jusqu'à la fin du fond | D-66, D-65e | moyenne | bonne (D+ ressenti dès les premières semaines) | 3 |
| H-42 | Samedi d'un week-end de choc : au plus 2/3 de la sortie longue et 3 h (4 h si la course dure 20 h ou plus) ; la fatigue de deux jours consécutifs se lit dans le ressenti | D-68, D-70 | moyenne | moyenne — le RPE des endurances ne voit pas la fatigue d'une sortie longue | **2** |
| H-43 | Récupération après un objectif secondaire à 35 / 55 / 75 % ; semaine allégée à 65 % du niveau de sortie longue ; sortie longue d'une semaine « moyenne » ≤ 3 h | D-67, D-70 | faible | bonne | 3 |
| H-44 | Une course est « exigeante » à partir de 4 h ou de 30 m de D+ par km ; sortie longue cible d'un secondaire = 50 % de sa durée, 4 h 30 au plus ; 1 week-end de choc avant lui, 3 avant l'objectif principal | D-70 | moyenne | faible — un type de course par an, aucun retour statistique | **1** |
| H-45 | Un écart est signalé sous 90 % de la cible ; un palier de +10 % prend environ 1,5 semaine (allègements et alternance compris) | D-69 | faible (information) | bonne | 3 |
| H-46 | Le RPE d'une sortie longue dépend de sa durée et de son D+ : seul celui des endurances signale une fatigue anormale | D-70 | moyenne | faible — à 2 jours de course, une endurance par semaine, parfois aucune : le signal peut rester muet | **1** |
| H-47 | Après un signal de fatigue, la sortie longue ne progresse pas pendant 2 semaines (1 après un ressenti « maintien ») | D-67 | moyenne | bonne | 2 |
| H-48 | La sortie longue déclarée au départ compte comme une séance à sa date, avec la même mémoire que H-40 (plus de condition « aucune course dans les 30 jours » ni de limite à 8 semaines). Réécrite le 09/11/2026 (D-94) | D-94, D-67 | moyenne | faible — sans historique importé, rien ne la contredit | **1** |

**Ce qui les testerait** : tes propres séances. H-44 et H-46 sont les plus fragiles : si tu
te sens « cuit » après un week-end de choc alors que le RPE de tes endurances reste bas, le
signal de fatigue est aveugle (H-46) et le ratio du samedi est trop haut (H-42). Sources de
H-42 à H-44 : pratiques de coachs (Koop, Roche), niveau de preuve « pratique de coach » — à
inscrire dans SOURCES.md.

| H-49 | Une séance manquée sans réponse est un empêchement, pas une fatigue | D-72 | moyenne | moyenne — une fatigue réelle se lit aussi dans le RPE des endurances, mais celui-ci peut rester muet (H-46) | 2 |

**À réintégrer** : H-38 (échelle RPE → dérive du simulateur) est citée dans le moteur, mais son
texte est introuvable dans ce dossier au 29/09/2026 (probablement dans MOTEUR-V0.md, retiré des
Connaissances). H-39 : non retrouvée. H-40 : réécrite le 09/11/2026 (D-94).

## Hypothèses du chantier interface (octobre 2026)

| # | Hypothèse | Décision | Portée | Détectabilité | Priorité |
|---|---|---|---|---|---|
| H-50 | Fourchette de D+ d'une séance : ± 10 %, au moins ± 50 m, au plus ± 150 m, arrondie à 50 m. Convention de coach (marge pour le choix d'itinéraire, au-dessus de la précision d'un altimètre barométrique, ± 3 à 5 %), pas un résultat d'étude | D-79 | faible (affichage) | bonne — Antoine voit vite si la fourchette est trop large ou trop serrée sur ses parcours | 3 |
| H-51 | Garmin Connect n'accepte vers la montre que les séances prévues dans les 7 jours environ. Mesure du 15/10/2026 sur Fenix 7 : envoi à J+6 reçu, à J+10 non reçu ; limite exacte (J+7 à J+9) non mesurée, non documentée par Garmin ni intervals.icu | D-78 | faible (Antoine envoie le jour J) | bonne — une séance envoyée trop tôt n'apparaît pas sur la montre | 3 |
| H-52 | Fourchette de la durée estimée d'une course (D-88) : ± (5 % + 5 % par doublement d'extrapolation), l'extrapolation étant le rapport des km-effort de la course visée et de la course de référence ; ± 25 % sans référence (7 km-effort/h). Convention, aucune source chiffrée : la formule de Riegel (exposant 1,07 ici) est une loi de puissance établie sur route ; sa précision en trail et en ultra n'est pas documentée pour une extrapolation de ×2,4. | D-88 | Affichage seulement (Ton objectif) ; ne touche pas le plan | Comparaison au temps réel de chaque course enregistrée | Moyenne |
| H-53 | Verdicts « prêt » (D-92) : *dénivelé* dans les temps si le plus grand D+ tenu en une sortie atteint la rampe de densité à cette date (densité prévue × durée de la plus longue sortie faite), en retard sous 80 % ; *ventre* dans les temps si les semaines de sorties longues restantes avant le bloc spécifique suffisent à monter de 6 g/h par semaine tolérée jusqu'à 60 g/h. Conventions | D-92 | faible (information, jamais d'effet sur le plan) | bonne | 2 |
| H-54 | Régularité (D-92) : une sortie longue manquée pèse plus qu'une endurance ; le verdict nomme d'abord les sorties longues, une endurance manquée seule ne le change pas. Convention de coach (la sortie longue est la seule séance qui progresse chaque semaine, règle du moteur) | D-92 | faible | bonne | 3 |
| H-55 | Verdicts « j'encaisse » (D-92) : « fatigue » si la semaine est marquée symptôme par le moteur ou si une séance est manquée pour fatigue ; « au-delà du prévu » si une séance faite dépasse à la fois sa durée prévue de plus de 10 % et de plus de 10 % la plus longue des 30 jours précédents (le levier est de s'en tenir au prévu ; une prescription du moteur au-delà de la règle relève de D-92 f) ; sinon « tu encaisses ». Pas de verdict « tu encaisses » sans repère d'effort (moins de 4 endurances notées depuis le début du plan) | D-92 | moyenne | moyenne — dépend de H-46 | 2 |
| H-56 | Message de progression (D-92) : affiché à un nouveau record de durée ou de D+ tenu en une sortie, au plus une fois par sortie, jamais sur la vitesse (D-60). Convention | D-92 | faible | bonne | 3 |
| H-57 | Verdicts « Prêt pour le jour J ? » (D-92, v52) : réel depuis la reprise rapporté au prévu à la même date (niveau de sortie longue, plus gros D+ en une sortie, glucides par heure tolérés) ; au moins 95 % = dans le plan, 80 à 95 % = un peu en retard, moins de 80 % = en retard ; « à construire » sans séance réelle. Remplace les verdicts de durée et de dénivelé de H-53. Convention | D-92 | faible (information, jamais d'effet sur le plan) | bonne | 2 |

Ajoutée le 10/11/2026 (D-96).

| # | Hypothèse | Décision | Portée | Détectabilité | Priorité |
|---|---|---|---|---|---|
| H-58 | Arrondi supérieur : dépasser la limite de +10 % de moins de 5 min (jusqu'à +20 % à 50 min de référence, +14 % vers 2 h, +13 % vers 3 h) n'ajoute pas de risque de blessure notable par rapport à +10 %. **Convention** : Frandsen 2025 (S-BLE-004) ne mesure que des catégories (10-30 % : HR 1,64) ; le 10 % est une frontière de catégorie, pas un seuil prouvé. Ajoutée le 10/11/2026 (D-96) | D-96 | moyenne : toute sortie longue qui bute sur la limite | faible — une blessure évitée ou causée ne se lit pas sur une séance | **1** |
| H-59 | Seuils des messages du bilan de séance (D-99) : RPE ≤ 3 avec plus de 40 % du temps au-dessus de la zone 2 = effort cardiaque supérieur au ressenti ; RPE ≥ 7 avec moins de 20 % = fatigue non cardiaque ; écart de 25 % au prévu. **Convention** (aucun seuil publié pour ces combinaisons ; la FC au poignet est imprécise). Ajoutée le 11/11/2026 | D-99 | faible : messages seulement, jamais le plan | moyenne — le retour « Pas vraiment » les met à l'épreuve | 2 |
| H-60 | Seuils de pente du profil de terrain (D-100) : montée au-delà de +3 %, descente en deçà de −3 %, plat entre les deux. **Convention** (le coût énergétique varie de façon continue avec la pente ; ces seuils servent seulement à regrouper). Ajoutée le 11/11/2026 | D-100 | faible : affichage seulement | moyenne — se vérifie sur les tranches réelles | 2 |
| H-61 | Zones de FC par la méthode de Karvonen (D-100) : zone de base = 60 à 70 % de la FC de réserve (FC max − FC repos), zones 3 à 5 par tranches de 10 %. Méthode établie ; **incertitudes** : la FC max (205 d'après la montre, 200 dans le plan du Bloc 1, bornes de base 143–158 ou 140–155) et la variabilité individuelle des seuils. FC max à confirmer sur une séance de référence. Ajoutée le 11/11/2026 | D-100 | moyenne : fausse les temps par zone si la FC max est mal estimée | à challenger | 2 |
| H-62 | Dérive cardiaque début contre fin de séance et FC de croisière (D-100) : la dérive en effort prolongé est établie ; le seuil d'alerte (souvent 5 %) est une **convention** et dépend de la correction de pente. Le retard du capteur optique au départ (FC basse les premières minutes) est une explication possible, non établie. Aucun verdict avant validation sur plusieurs séances d'Antoine. Ajoutée le 11/11/2026 | D-100 | faible : information seulement, jamais le plan | élevée — la FC au poignet est imprécise | 3 |
| H-63 | Pente, allure équivalente plat et dérive (D-100, v64) : pente mesurée sur 200 m centrés (le bruit d'altitude de la montre, 1 à 2 m, fausse la pente sur 60 m) ; 5 catégories (±1 %, ±3 %) : **convention**. Allure équivalente plat = coût énergétique de Minetti et al. 2002 (tapis, coureurs entraînés, pentes −45 à +45 %) : établi pour l'énergie, **non affiché en descente** car en trail la descente est limitée par la technique et le travail excentrique, pas l'énergie. Dérive = rapport FC / vitesse équivalente plat, 1re moitié contre 2e moitié, sans les 10 premières minutes ni les descentes, seulement si 40 min utiles ; seuil 5 % : **convention** (Friel). Lecture « FC monte = dérive cardiaque (Coyle 2001) ; FC baisse et allure chute = fatigue musculaire » : interprétation plausible, à confirmer sur plusieurs sorties. Ajoutée le 11/11/2026 | D-100 | faible : information seulement, jamais le plan | moyenne — le 42 km donne +21 % avec FC 171 → 156, cohérent avec la fatigue ressentie | 2 |
| H-64 | Repères de progression (D-101) : allure ramenée à la limite facile par proportion sur la FC de réserve (relation FC–vitesse à peu près linéaire en sous-maximal : établie ; précision individuelle : non vérifiée), seuil de 3 % entre « stable » et « en progrès » (**convention**, ordre de grandeur de la variation d'une sortie à l'autre), fenêtre de 6 semaines (**convention**). Ajoutée le 12/11/2026 | D-101 | faible : information seulement, jamais le plan | moyenne — à confronter aux sensations d'Antoine sur 2 à 3 mois | 2 |
| H-65 | Temps de course estimé ajusté de la progression en allure facile (D-101, v67) : temps = estimation de départ × (allure facile maintenant / allure facile au départ). Suppose que l'amélioration à effort facile se retrouve à l'identique en course, sans tenir compte de la résistance ni de la technique : **convention**, ordre de grandeur. Ajoutée le 13/11/2026 | D-101 | faible : information seulement | faible — à comparer au temps réel du 50 km le 8 mai 2027 | 1 |
