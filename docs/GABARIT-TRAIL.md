# GABARIT-TRAIL.md — Couche A : le plan de référence trail — Ascend

**Statut : BROUILLON, rien n'est acté.** Rédigé le 24/09/2026, à relire par Antoine.

## 0. Rôle de ce fichier

Le modèle se lit désormais en trois couches (décision de méthode du 24/09/2026) :

| Couche | Contenu | Où |
|---|---|---|
| **A. Gabarit** | ce qu'un coach de trail prescrirait sans rien savoir du coureur : phases, semaine type, séances et leurs progressions | **ce fichier** |
| **B. Personnalisation** | volume toléré, allures, longueur et rampe de sortie longue, jours et terrain, réactions (fatigue, gêne, séance manquée), coût-pente (prédiction seulement) | SPEC.md (G-PLA-002, G-CAP-001, D-63d, D-38, D-47, G-TER-001) |
| **C. Sécurité** | règle des 30 jours, une seule séance de progression par semaine, espacement des séances dures, plafond de pic, blessure | SPEC.md (D-63c, D-63k1, R-REN-005, D-21, D-50–D-51) — **prime sur A et B** |

Règle d'or : **le gabarit ne décide jamais d'une durée ni d'une allure absolue.** Il
décide *quel type* de séance, *quand*, et *comment elle progresse*. Les minutes viennent
de la couche B, et la couche C peut toujours les réduire.

**Ouverture future** : ce fichier est écrit pour être transcrit en données (un gabarit par
discipline × tranche de durée, D-44). Un gabarit route, ou une autre doctrine, sera un
autre fichier du même format — pas un autre moteur.

Portée de cette version : **trail, tranche 8–20 h** (80 km d'Antoine), avec ses règles
de compression pour une préparation plus courte (§ 2.3). Tranche 4–8 h : même structure,
à écrire ensuite.

---

## Amendements du 29/09/2026 (refonte du moteur, D-66 à D-71)

La doctrine ci-dessous ne change pas. Ce qui change, c'est la façon dont le moteur l'applique :

- **§ 2.4 (objectif secondaire)** : sortie longue cible = 50 % de sa durée estimée, 4 h 30 au plus ; week-ends de choc : 1 avant un secondaire exigeant (4 à 6 semaines avant), 2 à 3 avant l'objectif principal (D-70, H-44).
- **§ 3 (semaine type par phase)** : les jours peuvent changer d'une phase à l'autre (D-68). Recommandation : week-end enchaîné en phase spécifique pour qui court moins de 3 jours, avec un seul renforcement lourd.
- **§ 4 et § 5 (endurance, sortie longue, dénivelé)** : endurance ≤ 1 h 30 (D-71) ; sortie longue pilotée par sa propre progression, ≤ 3 h hors progression et sorties clés (D-67, D-70) ; en F1–F2, D+ des endurances = plafond, D+ de la sortie longue = repère (D-66).
- **§ 8.3 et § 8.4** : ce sont les sorties du moteur v1, **périmées**. Ne pas les lire comme le plan actuel.
- **§ 9, écart n° 5** : partiellement traité (D-67 : la dernière sortie longue déclarée sert de repère de reprise) ; l'import de l'historique reste à faire. **Écart n° 6** : traité (D-67 : rampe « juste à temps » conservée, calcul de faisabilité corrigé). Les autres écarts sont inchangés.

## 1. Doctrine — la colonne vertébrale

Choisie le 24/09/2026. **Ce sont des conventions assumées** : aucune logique de phases
n'est démontrée supérieure aux autres → S-CHA-005. Le choix se justifie par l'adéquation
à la cible (ultra de montagne : durabilité, endurance musculaire en montée, tolérance à la
descente, pas la vitesse maximale).

| Emprunt | Ce qu'il apporte | Source | Niveau |
|---|---|---|---|
| **Uphill Athlete** (Johnston, House, Jornet) — **colonne vertébrale** | base aérobie d'abord ; endurance musculaire en montée une fois la base installée ; ne jamais remplacer le volume aérobie par ce travail | S-TRA-013 | sans objet (pratique de coachs) |
| **Koop** | du général au spécifique : le travail à très haute intensité précède le travail au seuil et en endurance soutenue ; la préparation finit plus longue et plus lente, comme la course | S-TRA-014 | sans objet |
| **80/20** | répartition des intensités ; seule partie étayée par des essais | S-COU-008, S-COU-009 | modéré |
| **Accélérations et sprints en côte** | entretien neuromusculaire toute l'année, coût quasi nul | S-TRA-013 (sprints en côte) ; accélérations : **à sourcer** | extrapolation |

**Ce qui n'est pas repris** : le pilotage à la fréquence cardiaque d'Uphill Athlete (test
de seuil aérobie, « 10 % entre seuils ») — contraire à D-12. Traduction : le prérequis
« base installée » est jugé par la couche B (volume toléré stable, sortie longue ≥ 2 h
sans décrochage), pas par un test cardio.

**Cohérence vérifiée entre emprunts** : Uphill Athlete et Koop placent tous les deux le
travail à très haute intensité **après** la base et **avant** le spécifique. Ils ne
se contredisent pas sur l'ordre des phases — c'est la condition pour les combiner.

---

## 2. Calendrier — construit à rebours depuis la course

### 2.1 Phases (reprend D-21, D-25, D-63)

| Phase | Durée (8–20 h) | Objet |
|---|---|---|
| **Fond** | le reste : N − bloc − affûtage | construire le moteur et les tissus |
| **Bloc spécifique** | 9 semaines (8–10, D-21) | ressembler à la course |
| dont **pic** | 3 dernières semaines du bloc | plus hautes charges spécifiques |
| **Affûtage** | 3 semaines (D-25, D-63k7) | 70 / 55 / 40 % du volume de référence |

Semaines allégées : grille à rebours depuis l'affûtage (T−4, T−8…), règle 3:1 (D-57b,
D-63f). Semaine allégée ≈ 60 % du volume, sortie longue raccourcie.

### 2.2 Le fond découpé en sous-phases (nouveau)

Un fond de 40 semaines d'un seul tenant n'a pas de sens pour un coach. Quatre
sous-phases, dans cet ordre :

| Sous-phase | Durée cible | Dominante | Séance de qualité de la semaine |
|---|---|---|---|
| **F1 Reprise** | jusqu'à 8 sem. | fréquence, régularité, tissus | aucune ; accélérations à partir de la 3e semaine |
| **F2 Base aérobie** | le reste du fond | volume facile, sortie longue qui grandit, force | sprints en côte puis côtes courtes |
| **F3 Endurance musculaire** | 8 sem. | montée chargée, jambes limitantes | 1 séance d'endurance musculaire |
| **F4 Intensité en côte** | 6 sem. | VO2max en montée (Koop) | 1 séance d'intervalles en côte |

Enchaînement : F4 finit la veille du bloc spécifique ; F3 finit au début de F4 ; F2
remplit ce qui reste entre F1 et F3.

### 2.3 Compression si la préparation est plus courte

Retirer dans cet ordre, jamais l'inverse : raccourcir F2 → F3 à 6 semaines → F4 à 4
semaines → F1 au minimum de 4 semaines. En dessous de la durée minimale de D-21, c'est le
garde-fou qui parle (D-19), pas le gabarit.

### 2.4 Objectif secondaire (D-25 complétée, brouillon D-65a)

Affûtage + course + récupération **entièrement dans le fond**, jamais dans le bloc. Les
semaines qu'il occupe remplacent celles de la sous-phase où il tombe ; la sous-phase ne se
décale pas. Juste avant son affûtage : 2 semaines « spécifiques » courtes (montées
soutenues, sortie longue) si la sous-phase le permet.

---

## 3. Semaine type par phase

Chaque semaine est une liste de **créneaux**, posés sur les jours disponibles (D-38).
Moins de jours que de créneaux → on retire **par la fin de la liste** (priorité 1 gardée
en dernier).

| Priorité | F1 | F2 | F3 | F4 | Bloc | Affûtage |
|---|---|---|---|---|---|---|
| 1 | sortie longue | sortie longue | sortie longue | sortie longue | sortie longue / clé | sortie longue courte |
| 2 | endurance + accélérations | qualité F2 | endurance musculaire | intervalles en côte | tempo ou montée spécifique | rappel d'allure court |
| 3 | endurance | endurance | endurance | endurance | endurance vallonnée | endurance |
| 4 | endurance | endurance + accélérations | endurance + accélérations | endurance + accélérations | 2e séance spécifique (pic) | — |
| Renfo | 2 × général | 2 × force | 1–2 × force + ME en salle possible | 1–2 × force | 2 × force → pliométrie / excentrique au pic | 0–1 |

Contraintes de pose (couche C) : **au plus 2 séances dures par semaine**, renforcement
jambes et endurance musculaire compris ; jamais une séance dure ou une séance de jambes
la veille ou le lendemain de la sortie longue (R-REN-005) ; une séance de course par jour
(D-35).

Répartition cible : fond ≥ 80 % facile (D-34) — en F1 la part intense est quasi nulle, la
cible de D-34 y est un **plafond**, pas un objectif ; bloc 65–75 % facile.

---

## 4. Catalogue et progressions

Intensités exprimées comme dans D-29 (en % de vitesse critique sur le plat) ; **en côte,
jamais d'allure ni de VAM cible, seulement l'effort** (D-54). Chaque table donne la
progression **si tout va bien** ; une séance manquée ou un symptôme fait rester au
palier, jamais sauter.

**Accélérations** (nouveau type) — fin d'une séance d'endurance, sur le plat ou en légère
montée, récupération complète en marchant.
| Semaines de pratique | 1–2 | 3–4 | 5 et + |
|---|---|---|---|
| Dose | 4 × 15 s | 6 × 20 s | 6–8 × 20 s |

**Sprints en côte** (F2, début) — côte raide, 8–12 s vite mais relâché, redescente
en marchant, récupération complète (2–3 min).
| Séances | 1–2 | 3–4 | 5–6 |
|---|---|---|---|
| Dose | 6 × 10 s | 8 × 10 s | 8–10 × 12 s |

**Côtes courtes** (F2, suite ; D-29 : > 105 %, 30 s–2 min)
| Séances | 1–2 | 3–4 | 5–6 | 7 et + |
|---|---|---|---|---|
| Dose | 6 × 30 s | 8 × 30 s | 6 × 45 s | 8 × 1 min |

**Endurance musculaire** (nouveau type ; F3) — montée raide (> 20 % idéalement), sac
lesté, **les jambes limitent, pas le souffle** ; vider l'eau du sac en haut pour épargner
la descente. Alternative sans relief : version en salle (montées sur box lestées).
Coût de récupération élevé (2–3 jours) : compte comme séance dure.
| Semaine de F3 | 1–2 | 3–4 | 5–6 | 7–8 |
|---|---|---|---|---|
| Charge (% du poids du corps) | 5 % | 8–10 % | 10–15 % | 15 % |
| Temps de montée | 30 min | 40 min | 50 min | 60 min |
Source : S-TRA-013 (départ à 5–10 % du poids, 8–16 semaines à une séance par semaine,
ne jamais remplacer le volume aérobie). Paliers intermédiaires : **extrapolation**.

**Intervalles en côte** (F4 ; remplace la pyramide de S-COU-010 comme type par défaut en
trail) — montée régulière, fractions de 2 à 4 min, récupération égale en descente
tranquille, 12 à 24 min d'effort au total, ressenti 9/10.
| Séance | 1 | 2 | 3 | 4 | 5–6 |
|---|---|---|---|---|---|
| Dose | 5 × 2 min | 4 × 3 min | 5 × 3 min | 5 × 4 min | 6 × 4 min |
Source : S-TRA-014 (fractions de 2–4 min, 12–24 min, en montée, jamais en descente).

**Tempo en montée** (bloc ; D-29 « seuil », 95–105 %) — effort soutenu mais contrôlé.
| Séance | 1 | 2 | 3 | 4 et + |
|---|---|---|---|---|
| Dose | 3 × 8 min | 3 × 10 min | 3 × 12 min | 2 × 20 min |

**Montée spécifique** (bloc ; D-29 « allure spécifique », 80–95 %) — montées longues à
l'effort de course, alternance montée courue ou marchée selon la pente, descente
travaillée.
| Séance | 1 | 2 | 3 et + |
|---|---|---|---|
| Dose | 45 min d'effort | 60 min | 75–90 min |
En bloc, **alterner d'une semaine à l'autre** tempo et montée spécifique ; au pic, les
deux possibles la même semaine si le volume le permet (≤ 2 séances dures).

**Endurance** et **sortie longue** : facile (< 80 %), terrain de plus en plus vallonné au
fil du fond. Leur durée vient entièrement de la couche B.

---

## 5. Sortie longue et dénivelé

**Sortie longue** : toute la mécanique est déjà dans la couche B/C (D-22, D-63c-d, k1,
k6) : part du volume par défaut, rampe à rebours vers la sortie clé, +10 % au plus sur
la plus longue des 30 jours, une semaine sur deux au-delà de 3 h. Le gabarit ajoute
seulement **son contenu** :
- F1–F2 : entièrement facile, marche autorisée en côte raide ;
- F3–F4 : vallonnée, le D+ de la semaine s'y concentre ;
- bloc : **sortie clé** sur un terrain proche de la course, avec nutrition de course
  (D-30), dernière portion à l'effort de course.

**Dénivelé** (brouillon D-65e) : le D+ hebdomadaire **monte pendant le fond** et atteint
le niveau du bloc avant la fin du fond ; en bloc il **se stabilise** — c'est le type de
montée qui devient spécifique (D-28). La descente monte avec le D+ : jamais de première
grosse descente en bloc (S-TRA-012). Vitesse de progression du D+ : **non chiffrée**
(trou ouvert, élément 5 du chantier).

---

## 6. Renforcement (reprend D-39, avec un écart à trancher)

| Sous-phase | Dominante | Fréquence |
|---|---|---|
| F1 | stabilité, gainage, dos, force générale légère | 2 × |
| F2 | **force maximale** (charges lourdes, peu de répétitions) | 2 × |
| F3 | force maximale en entretien ; endurance musculaire en salle si pas de relief | 1–2 × |
| F4 | force en entretien | 1–2 × |
| Bloc | force → **pliométrie et excentrique** au pic | 2 × → 1–2 × |
| Affûtage | volume fortement réduit, pas d'arrêt | 0–1 × |

**Écart avec D-39** : D-39 place la force maximale en début de bloc spécifique ; Uphill
Athlete la place dans la base, avant l'endurance musculaire. S-REN-006 (force maximale et
économie de course, niveau élevé) ne dit rien du moment. Proposition : suivre la colonne
vertébrale (force en F2). **À trancher.**

---

## 7. Nutrition (reprend D-30)

Entraînement digestif sur les séances de plus de 2 h, progression de 5–10 g/h par
semaine, 8–10 semaines. Extension proposée : le démarrer **~10 semaines avant un objectif
secondaire long** aussi, pas seulement avant le bloc.

---

## 8. Instance — Antoine (première application, 24/09/2026)

### 8.1 Données d'entrée

| Paramètre | Valeur | Statut |
|---|---|---|
| Objectif principal | 80 km, 3000–6000 m D+, **~samedi 25/09/2027** | date approximative |
| Objectif secondaire | 50 km, 2000 m D+, **samedi 08/05/2027** | statut objectif ou course-entraînement à confirmer |
| Durée estimée du 50 km | 7–9 h (km-effort 70) | **tranche incertaine** (4–8 h ou 8–20 h) |
| Volume actuel | quasi nul ; une sortie de 12 km / 500 m D+ en endurance ~3 semaines avant S1 | déclaré |
| Historique | ultras passés | **non importé** |
| Jours disponibles, jour de sortie longue, terrain | — | **à déclarer** |

### 8.2 Calendrier (S1 = lundi 28/09/2026, N = 52)

| Semaines | Dates (lundi) | Phase |
|---|---|---|
| S1–S8 | 28/09 → 16/11/2026 | F1 Reprise |
| S9–S20 | 23/11/2026 → 08/02/2027 | F2 Base aérobie |
| S21–S28 | 15/02 → 05/04/2027 | F3 Endurance musculaire |
| S29–S30 | 12/04 → 19/04 | spécifique 50 km (courte) |
| S31–S32 | 26/04 → 03/05 | affûtage 50 km (2 sem. si 4–8 h ; commence S30 si 8–20 h) |
| **S32** | **samedi 08/05/2027** | **50 km** |
| S33–S34 | 10/05 → 17/05 | récupération (jusqu'à S35 si 8–20 h) |
| S35–S40 | 24/05 → 28/06 | F4 Intensité en côte |
| S41–S49 | 05/07 → 30/08 | bloc spécifique (pic S47–S49) |
| S50–S52 | 06/09 → 20/09 | affûtage |
| **S52** | **~samedi 25/09/2027** | **80 km** |

Contrôles : secondaire entièrement en fond ✓ ; 15 semaines de construction entre sa fin
de récupération et l'affûtage (D-25b : ≥ 6) ✓ ; budget 4–6 semaines sur 52 = 8–12 %
(D-25a : ≤ 20 %) ✓. Semaines allégées données par le modèle : S5, S10, S14, S18, S22,
S26… (grille T−4k).

### 8.3 Ce que le modèle produit pour S1–S12 (sans historique importé, 4 jours)

Sortie de `sim8.py` avec les règles v1 en brouillon (amorçage D-65b), minutes par séance :

| S1–S4 | S5 (allégée) | S6 | S7 | S8 | S9 | S10 (allégée) | S11 | S12 |
|---|---|---|---|---|---|---|---|---|
| 30-30-30 | 30-33 | 30-30-30-30 | 33-33-33-36 | 36-36-36-39 | 39-39-39-42 | 34-34-46 | 46-46-46-50 | 45-45-45-55 |

**Mon avis de coach sur cette sortie : trop prudente pour toi, et pour une raison
identifiable.** Elle te traite comme un débutant parti de zéro parce que ton historique
n'est pas importé, et elle bride la sortie longue à la part du volume de D-22 : 55 min en
S12, pour quelqu'un qui a couru des ultras et a fait 12 km / 500 m D+ en endurance il y a
trois semaines. Ce n'est pas un réglage à forcer à la main : c'est l'**import de
l'historique (D-14)** qui doit le corriger. Voir écart n° 5.

### 8.4 Proposition de coach pour S1–S4 (séances fermes)

Compatible avec la couche C (règle des 30 jours : ta sortie de 12 km autorise une séance
jusqu'à ~1,1 × sa durée tant qu'elle a moins de 30 jours).

| | Séance A | Séance B | Séance C (sortie longue) | Renfo |
|---|---|---|---|---|
| S1 | 30 min endurance | 30 min endurance | 45 min endurance, vallonné léger | 2 × 20–30 min général + dos |
| S2 | 30 min | 35 min | 50 min | idem |
| S3 | 35 min + 4 × 15 s accél. | 35 min | 55 min | idem |
| S4 | 35 min + 4 × 15 s | 40 min | 60 min | idem |

Endurance = conversation possible, marche en côte raide autorisée. Une note de ressenti
après chaque séance. La suite (S5–S8) se décide sur tes ressentis de S1–S4, pas à l'avance.

---

## 9. Écarts avec SPEC.md et points à trancher

Auto-vérification faite contre SPEC.md, REGLES.md, SOURCES.md le 24/09/2026.

| # | Écart | Proposition |
|---|---|---|
| 1 | D-39 : force maximale en bloc ; gabarit : en F2 | suivre la colonne vertébrale |
| 2 | D-29 : types « accélérations » et « endurance musculaire » absents | les ajouter au catalogue |
| 3 | D-29 : intervalles en pyramide (S-COU-010) par défaut | intervalles en côte de Koop par défaut en trail ; pyramide gardée pour la route |
| 4 | D-34 : cible de 10–15 % d'intensité en fond | en F1, plafond et non cible |
| 5 | D-65b (brouillon) : un coureur en reprise sans historique importé est traité comme un débutant, et la sortie longue reste bridée par sa part du volume | l'import de l'historique est un prérequis du premier plan ; à défaut, déclarer « ancienne plus longue sortie » (nouveau paramètre, test D-17 à passer) |
| 6 | D-63d : rampe de sortie longue « juste à temps » | la base d'Uphill Athlete fait grandir la sortie longue tôt ; à rediscuter avec la sortie de 8.3 sous les yeux |
| 7 | D-30 : entraînement digestif calé sur le bloc seulement | aussi avant un secondaire long |
| 8 | Sous-phases du fond (§ 2.2) absentes de la SPEC | à inscrire comme décision |
| 9 | D-65 entier | toujours en brouillon, non validé |
| 10 | Accélérations : aucune source vérifiée | à sourcer ou marquer extrapolation (R-MET-001) |

**Nouvelles sources à inscrire dans SOURCES.md** : S-TRA-013 (Uphill Athlete, articles
« Muscular Endurance » et « Strength Training for the Mountain Athlete », uphillathlete.com,
consultés le 24/09/2026 — pratique de coachs, niveau sans objet) ; S-TRA-014 (Koop,
*Training Essentials for Ultrarunning*, et « Key Workouts Every Ultrarunner Should Do »,
trainright.com — pratique de coach, niveau sans objet).

**Hors de ce fichier** : le visuel existant de l'app n'est pas dans les connaissances du
projet. Rien ici n'en dépend ; il faudra le fournir au moment de coder.
