# MOTEUR-V1.md — Refonte du moteur et organisation par phase (27–28/09/2026)

**Fusionné le 29/09/2026** dans SPEC.md (D-66 à D-71) et HYPOTHESES.md (H-41 à H-48). Ce fichier reste le journal détaillé de la refonte (ce qui a été livré, version par version) ; en cas de divergence, SPEC.md fait foi. Complète MOTEUR-V0.md (absent des Connaissances au 29/09/2026).

## Déjà livré (27/09) — D-66
| Point | Décision |
|---|---|
| Déroulé | la somme des étapes = durée prescrite (endurance, sortie longue, tempo) ; test `tests/t_steps.js` |
| Qualité | placée seulement dans un créneau assez long pour elle ; sinon semaine sans qualité |
| D+ F1–F2 | endurance : D+ = plafond (« ≤ X m ») ; sortie longue : repère (« environ X m, sans le chercher ») |
| D+ départ | densité de départ ≤ 50 % de celle de la course, rampe jusqu'à la fin du fond → **H-41** (et non H-40, déjà pris par la reprise après interruption) |
| FC | note fixe sur endurance et sortie longue : « le ressenti décide, la FC confirme » (conforme D-12, pas de pilotage cardio) |

## Diagnostic qui motive la refonte
La sortie longue est une part du volume (D-22) et le volume dépend de ce qui se place. Avec peu de jours ou des plafonds de temps, tout se tient à la baisse : 2 jours de course → sortie clé plafonnée à 2 h 15 en bloc. Corriger les symptômes un à un crée des régressions (simulation sur 7 profils, 28/09) : plafonner l'endurance fait chuter le profil 3 jours ; supprimer le bridage du volume casse la semaine allégée et l'alternance au-delà de 3 h.
La cible de sortie longue avant un objectif secondaire **existe déjà** (échéance, 5 h pour un 50 km de 7–9 h) : elle n'est jamais atteinte.

## D-67 — Sortie longue pilotée par elle-même (option A, validée)
- Progression propre : +10 % au plus sur la plus longue sortie des 30 jours (D-63c, Frandsen et al., BJSM 2025 — seule règle à preuve solide, mesurée **par séance**).
- Semaine allégée : sortie longue à 60–70 % de la précédente.
- Au-delà de 3 h : alternance une semaine sur deux (**convention**, H-27 preuve faible — paramètre, à confronter aux données réelles).
- Cibles : sorties clés et objectifs secondaires (échéances existantes). Rampe « juste à temps » conservée (D-63d), **calcul de faisabilité corrigé** (aujourd'hui trop optimiste : il ignore les contraintes réelles).
- Le volume hebdomadaire devient une **conséquence** des séances. Le contrôleur G-PLA-002 ne pilote plus que les autres séances.
- **Non négociable** : un signal de fatigue (ressenti, séances manquées) gèle aussi la progression de la sortie longue.
- Endurance ≤ 1 h 30 (D-29) et ≤ temps disponible du jour.
- Point de départ (écart n° 5) : la dernière sortie longue déclarée sert de repère de reprise, même décroissance qu'une interruption.
- Parité : mode « règles v1 » conservé pour prouver le socle contre `sim8.py` ; nouveau test par propriétés sur 7 profils (4 j, 2 j avec jour plafonné, 3 j, 6 j, sans objectif secondaire, objectif secondaire 30 km, sans historique) : endurance ≤ 1 h 30, sortie longue ≥ endurances, règle des 30 jours, sortie longue réduite en semaine allégée, cibles atteintes.

## D-68 — Organisation par phase (7 règles validées)
1. L'organisation (jours de course, jour de sortie longue, renforcement) est **attachée aux phases**, pas aux dates : elle suit le calendrier s'il est recalculé. **À la décision, les phases sont expliquées et visualisées** (frise des phases, ce qui change, l'organisation choisie pour chacune).
2. Le passé ne se réécrit jamais : chaque organisation est enregistrée avec sa date d'application ; les semaines passées gardent celle qui était en vigueur (corrige un défaut actuel : changer ses jours recalcule tout le plan).
3. Application le lundi de la nouvelle phase ; pas de semaine de transition.
4. Pas de remise à zéro : la règle des 30 jours s'appuie sur l'historique réel. Un jour ajouté (ex. samedi du week-end enchaîné) **démarre directement** à son niveau, plafonné par la règle des 30 jours ; samedi enchaîné ≤ 2/3 de la sortie longue (**convention**, H-42). Pas de démarrage bas supplémentaire : la règle par séance ne l'exige pas, et la fatigue des jours consécutifs est couverte par les signaux de ressenti. Un jour supprimé n'est pas reporté sur les autres.
5. La sortie longue garde sa trajectoire propre (D-67) : un changement de jours ne la fait ni sauter ni reculer.
6. Objectifs secondaires prioritaires : pendant leur affûtage et leur récupération, les volumes restent imposés ; l'organisation de phase ne fixe que les jours.
7. Recommandation refusée → la projection continue avec l'organisation actuelle ; l'alerte d'écart reste visible.

## D-69 — Alertes et bilan de phase
- **Alerte d'écart** (mécanisme principal) : dès que la projection montre une cible inatteignable avec l'organisation actuelle — écart chiffré, leviers, date limite pour agir.
- **Carte « Bilan de phase et phase suivante »**, 1 à 2 semaines avant la fin de **chaque** phase, écart ou non : réalisé (sortie longue face à la cible, ressenti, séances manquées), ce que la phase suivante change, l'organisation déjà programmée pour elle, à confirmer ou modifier.
- L'app recommande, le coureur décide ; les jours ne sont jamais déplacés sans lui.

## Hypothèses à inscrire
- **H-41** — densité de D+ de départ ≤ 50 % de celle de la course. Extrapolation.
- **H-42** — samedi d'un week-end enchaîné ≤ 2/3 de la sortie longue. Convention de coach, aucune source chiffrée.

## Livré le 28/09 — D-67 et D-68
**Moteur** (`index.html` et `tests/engine.js`, identiques) : règles v2 par défaut ; `build({regles:'v1'})` rejoue exactement les anciennes règles (parité `sim8.py` : 0 écart).
- Sortie longue : niveau atteint `niv` ; progression +10 % sur les 30 jours quand la rampe « juste à temps » l'exige, sinon entretien du niveau ; semaine allégée 65 % du niveau ; au-delà de 3 h, semaine sur deux à 2/3 du niveau (≥ 3 h) ; hors sorties clés en bloc et pic : 2/3 du niveau ; affûtage : niveau × facteurs de la tranche.
- Fatigue : symptôme → 2 semaines de charge sans progression de la sortie longue ; ressenti « maintien » → 1 semaine.
- Récupération après un objectif secondaire : sortie longue et volume à 35 %, 55 %, 75 % (**convention**, H-43) ; pas de sortie moyenne en affûtage ni en récupération.
- Endurances : budget = volume du contrôleur × (1 − part de la sortie longue), chacune ≤ 1 h 30, ≤ temps disponible, ≤ plus longue des 30 jours. Le contrôleur ne voit plus que ces séances.
- Bloc : le volume est gelé au niveau visé, plus au niveau placé.
- Reprise (écart n° 5) : dernière sortie longue déclarée, sortie de la fenêtre depuis moins de 8 semaines → repère dégressif.
- Organisation : `profile.orgs = [{from:'F3', days:{run,long,cf,time}, enchaine:true}]` (vaut pour la phase et les suivantes) ; `profile.orgHist = [{until, days, orgs}]` écrit à chaque changement après le démarrage du plan.

**Interface** : carte « Organisation par phase » dans Profil (frise des phases avec dates, organisation de chacune, réglage propre signalé) ; feuille de décision : phases expliquées, conseil de phase, jours, temps disponible, week-end enchaîné, renforcement, alertes de conflit, retour à l'organisation précédente, aperçu des 14 prochains jours.

**Tests** : `t_profils.js` (8 profils, 0 violation), `t_react3.js` (gel de la sortie longue après fatigue), `t_react2.js` et `parity.py` en règles v1, `t_steps.js`, parcours Chromium sans erreur.

## Hypothèse supplémentaire
- **H-43** — récupération après un objectif secondaire à 35 / 55 / 75 % ; semaine allégée à 65 % du niveau de sortie longue ; semaine « moyenne » à 2/3. Conventions de coach, aucune source chiffrée.

## Livré le 28/09 (suite) — D-70 : week-ends de choc et conventions réglables
Toutes les conventions sont regroupées dans la table `CONV` du moteur (une seule table, pour tous les objectifs) :
| Paramètre | Valeur | Rôle |
|---|---|---|
| `moyenneMax` | 180 min | sortie longue d'une semaine « moyenne » (hors progression, hors sortie clé) et d'une semaine allégée : 3 h au plus (seuil de D-22a) |
| `samRatio`, `samMax` | 2/3 ; 3 h (4 h si course ≥ 20 h) | samedi d'un week-end de choc |
| `secPart`, `secMax` | 50 % ; 4 h 30 | sortie longue cible avant un objectif secondaire (au lieu de l'échéance de D-63, pensée pour l'objectif principal) |
| `chocsPrincipal` | 3 | week-ends de choc avant l'objectif principal, sur les semaines de sortie clé |
| `chocsSecondaire` | 1 | avant un objectif secondaire **exigeant**, placé 4 à 6 semaines avant |
| `secExigeant` | durée ≥ 4 h **ou** D+ ≥ 30 m/km | « beaucoup de dénivelé » = 30 m de D+ par km et plus (**convention H-44**) |

- Le nombre de week-ends de choc ne change pas selon la distance ; **le volume suit la course** (durée estimée de l'objectif concerné). Exemple testé : 80 km secondaire + 160 km principal → 1 choc à 3 h + 4 h 25 avant le 80 km, 3 chocs dans le bloc, samedi jusqu'à 4 h pour le 160 km.
- Hors choc, la veille de la sortie longue reste une endurance normale, même avec le week-end enchaîné activé.
- Une course-entraînement (priorité C) ne crée plus de cible de sortie longue.
- La montée de la sortie longue s'arrête à la cible (plus de dépassement par le dernier palier de +10 %).
- Signal de fatigue : RPE des **endurances seules** (option A) ; cible : écart entre RPE réel et RPE attendu (option C, avec le modèle allure-effort).
- Objectif estimé à 20 h ou plus : avertissement (gabarit non écrit, celui des 8–20 h s'applique).

## Hypothèse supplémentaire
- **H-44** — « course exigeante » = 4 h ou plus, ou 30 m de D+ par km et plus. Convention, aucune source chiffrée.

## Numéro de version (28/09)
`APP_VERSION` dans `index.html` (ligne « Ascend vNN · moteur de plan v2 » en bas de Profil et sur l'écran de connexion) doit rester **identique** au cache de `sw.js` (`const C='ascend-vNN'`, actuellement v16). À incrémenter ensemble à chaque déploiement. Si le cache du service worker est plus récent que la page affichée, la ligne demande de fermer complètement l'app et de la rouvrir.

## D-71 — Suppression du temps disponible par jour (28/09)
Décision d'Antoine : le réglage « temps disponible » (minutes par jour de course) est retiré des deux formulaires (Semaine type, Organisation par phase). Le moteur v2 **ignore** le champ `days.time` d'un profil existant ; les règles v1 le lisent encore (parité `sim8.py`).
- Endurance : plafonnée à **1 h 30** (D-29) par `CONV.efMax`, une valeur par tranche d'objectif (4–8 h : 90, 8–20 h : 90 ; objectif < 4 h : gabarit court non écrit, tranche 4–8 h appliquée avec avertissement ; ≥ 20 h : avertissement, tranche 8–20 h). Valeur modifiable par tranche sans toucher au reste.
- Sortie longue : progression propre (D-67), plus aucun plafond de temps par jour.
- Conséquence assumée : un coureur n'a plus de moyen de dire qu'il n'a que 60 min un jour donné ; une endurance peut donc durer jusqu'à 90 min. Le signal est l'écart entre le plan et ce qui est réellement couru (alerte d'écart, D-69).
- Test : `t_profils.js` vérifie que le plan est identique avec ou sans `time`, et qu'aucune endurance ne dépasse 90 min.

## Livré le 28/09 — D-69 : alerte d'écart et bilan de phase (v17)
**Moteur** : `out.ecarts = [{obj:'secondaire'|'principal', nom, date, cible, atteint, limite}]`, calculé sur la projection.
- Objectif secondaire : sortie longue maximale (prescrite ou réelle) avant son affûtage (J−14) < 90 % de sa cible (50 % de la durée, 4 h 30 au plus).
- Objectif principal : sortie clé maximale < 90 % de la cible de la tranche ; échéance = début de l'affûtage moins une semaine.
- En v2, l'écart détaillé remplace l'ancien message « ta sortie clé plafonne… » du garde-fou.

**Constat important** : depuis D-67 et D-71, l'organisation (jours) ne limite plus la sortie longue. Un écart vient donc du **point de départ et du temps disponible jusqu'à l'échéance** (règle des 10 % sur 30 jours), pas des jours. L'alerte le dit, et ne propose pas de changer de jours pour le résoudre.

**Accueil — carte d'écart** (tant que l'écart existe) : écart chiffré, échéance, cause, leviers (déclarer une sortie plus longue récente si aucun historique, enregistrer ses vraies sorties, semaines de progression manquantes ≈ 1,5 semaine par palier de 10 % → décaler la date ou viser plus court).

**Accueil — carte « Bilan de phase et phase suivante »** : affichée les 14 derniers jours de chaque phase, **écart ou non**, jusqu'à « C'est bon pour moi » (`profile.phaseAck[phase]`). Contenu :
- réalisé : sorties faites / prévues, sortie longue réalisée / prévue, ressenti moyen en endurance ;
- phase suivante : explication, sortie longue projetée (min–max), types de qualité, nombre de week-ends de choc ;
- organisation déjà programmée pour cette phase ;
- **recommandation calculée et testée sur le moteur** : en phase spécifique (F3, F4, bloc, pic) sans week-end enchaîné → simulation avec la veille de la sortie longue ajoutée et l'enchaînement activé, nombre de week-ends de choc obtenus et nombre de jours de sport ; renforcement : 2 en Base, 1 suffit en phase spécifique ;
- boutons « C'est bon pour moi » et « Modifier » (ouvre l'organisation de la phase suivante).
- Accessible à tout moment depuis Profil › Organisation par phase.

**Tests** : `t_profils.js` vérifie aucun écart avec historique, deux écarts sans historique ; parcours Chromium (bilan Reprise → Base, Base → Endurance musculaire, écart sans historique, accusé de lecture, feuille depuis Profil) sans erreur.

## Hors périmètre, à décider plus tard
- Le bilan ne relit pas encore les commentaires (verbatims) des séances.
- Le seuil de 90 % pour déclarer un écart et l'estimation « 1,5 semaine par palier » sont des conventions.

## Hypothèses supplémentaires (29/09/2026)
- **H-45** — seuil d'écart à 90 % de la cible ; un palier de +10 % ≈ 1,5 semaine.
- **H-46** — le RPE des sorties longues n'est pas comparable d'une semaine à l'autre : le signal de fatigue ne lit que les endurances.
- **H-47** — gel de la sortie longue : 2 semaines après un symptôme, 1 après un ressenti « maintien ».
- **H-48** — repère de reprise dégressif sur la dernière sortie longue déclarée.

## Dépôt (29/09/2026)
`tools/build.py` (injecte `tests/engine.js` dans `index.html`, synchronise la version avec `sw.js`), `tools/test.py` (toute la batterie), `.github/workflows/tests.yml` (la même batterie à chaque envoi sur GitHub), `AGENTS.md` et `CLAUDE.md` (instructions pour un assistant de code). `t_react2.js` est retiré : `parity.py` couvre le comportement v1.


## Séances manquées, décalage, renforcement minimal (07/10/2026, v19)
- **D-72** : une séance de course manquée ne déclenche l'allègement que si l'utilisateur répond « fatigue » (carte d'accueil). Sans réponse : agenda (H-49).
- **D-73** : décalage d'une séance de course dans la semaine en cours, vers un jour sans course ; jamais de rattrapage la semaine suivante.
- **D-74** : renforcement réduit à durée, RPE, jambes sollicitées ; lieu et matériel retirés du profil. Journal de progression reporté (BACKLOG).
- Tests : `t_react3.js` étendu, `t_decal.js` ajouté. Parcours Chromium : carte, reprogrammation, annulation du décalage, formulaire, ancienne séance de renforcement lisible, sans erreur.

## D+ de départ (09/10/2026, v20)
- **D-75** : la densité de D+ de départ ne se nourrit plus des séances faites après le démarrage du plan (les endurances plates prescrites la tiraient vers le bas). Sorties longues et courses des 8 semaines avant le démarrage, puis déclaration, puis 150 m/h ; plafond H-41 inchangé.

## Manquée le jour même (11/10/2026, v21)
- Bouton « Pas faite » sur la séance du jour : la raison (fatigue ou agenda) se déclare sans attendre le lendemain (complément de D-72).

## Fenêtre « Séance manquée » (11/10/2026, v23)
- Un seul geste : « Séance manquée ? » ouvre une fenêtre avec une question (« Pourquoi ? » : agenda/imprévu ou fatigue, chacun avec son effet), ou « La faire un autre jour cette semaine ». Le choix enregistre et ferme. Raison modifiable depuis la fiche de la séance. Sur l'accueil, une séance passée non saisie propose « Je l'ai faite » ou « Manquée ».
