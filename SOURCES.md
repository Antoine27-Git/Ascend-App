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

Catégories ouvertes à ce jour : REN, CHA, COU, TRA, MES, NUT, BLE. Les autres existent dans la
nomenclature mais n'ont pas encore de source.

| Code ajouté | Domaine |
|-------------|---------|
| MES | Fiabilité de mesure, capteurs, conditions de validité |

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

### S-REN-005 — Périodisation du renforcement pour coureurs, convergence de pratique
McMillan Running (*Guide to Strength Training Periodization*), TrainingPeaks (*Periodized
Strength Training for Endurance Athletes*), First Endurance — consultés le 17/09/2026.

Plusieurs coachs indépendants convergent sur la même structure, calquée sur la
périodisation de la course : base/stabilité (charges légères, volume modéré) pendant la
construction du fond, force maximale (charges lourdes, peu de répétitions) en début de
bloc spécifique, pliométrie/puissance en fin de bloc, volume fortement réduit sans arrêt
complet à l'approche de la course. Fréquence décroissante : 2-3 séances/semaine en fond,
1-2 en fin de préparation.
**Niveau : sans objet** (convergence de pratique de coachs, aucune étude comparative).
→ fonde D-39 dans SPEC.md

### S-REN-006 — Renforcement et performance en endurance — **VÉRIFIÉE, revue corrigée**
Berryman N., Mujika I., Arvisais D., Roubeix M., Binet C., Bosquet L. *Strength Training
for Middle- and Long-Distance Performance: A Meta-Analysis.* International Journal of
Sports Physiology and Performance, 13(1):57-63, 2018. DOI 10.1123/ijspp.2017-0032

Méta-analyse, 28 études retenues sur 554. Un mésocycle de renforcement en course,
cyclisme, ski de fond et natation est associé à une amélioration modérée de la
performance (SMD net = 0,52 ; IC95 % 0,33–0,70), accompagnée d'améliorations du **coût
énergétique de la locomotion** (0,65 ; 0,32–0,98), de la force maximale (0,99) et de la
puissance maximale (0,50). **L'entraînement en force maximale produit les plus grandes
améliorations**, et les effets sont constants quel que soit le niveau des athlètes.
**Niveau : élevé** — méta-analyse, large base.
**Vérifiée le 17/09/2026** : la source secondaire annonçait « Sports Medicine », la revue
réelle est l'IJSPP. La citation était incomplète et non exploitée ; elle devient
**exploitable** et fonde directement le choix de la force maximale en début de bloc
spécifique (D-39).
→ fonde D-39 (SPEC.md)

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

### S-CHA-003 — Transfert d'entraînement entre modalités (cross-training)
Tanaka H.
*Effects of Cross-Training: Transfer of Training Effects on VO2max Between Cycling,
Running and Swimming.*
Sports Medicine, 18(5):330-339, 1994. DOI 10.2165/00007256-199418050-00005
https://pubmed.ncbi.nlm.nih.gov/7871294/

Revue. Un transfert d'effets sur la VO2max existe d'une modalité à l'autre, mais il est
minimal quand la modalité d'apport est la natation, et les effets du cross-training ne
dépassent jamais ceux de l'entraînement spécifique. Le principe de spécificité pèse
d'autant plus que l'athlète est entraîné.
**Niveau : modéré** pour le sens des transferts. **Réserve :** revue ancienne (1994),
à réactualiser ; ne fournit aucun coefficient de transfert exploitable.
→ justifie de ne pas modéliser l'adaptation croisée dans SPEC.md (trou ouvert)

### S-CHA-004 — Volume et périodisation chez les coureurs de fond entraînés
Casado A., González-Mohíno F., González-Ravé J.M., Foster C. *Training Periodization,
Methods, Intensity Distribution, and Volume in Highly Trained and Elite Distance Runners:
A Systematic Review.* International Journal of Sports Physiology and Performance,
17(6):820-833, 2022. DOI 10.1123/ijspp.2021-0435. Vérifiée le 22/09/2026.

Revue systématique, 10 études. Distribution d'intensité plutôt pyramidale ; périodisation
linéaire généralement recommandée pour cette population ; en période de compétition, moins
de travail au seuil et **davantage à allure de course**. Le volume reste du même ordre en
préparation et en pré-compétition. **Niveau : modéré** pour la population étudiée (élites,
route et piste) — **transposition au trail amateur : extrapolation**.
→ fonde D-63a

### S-CHA-005 — La périodisation inversée n'est pas supérieure
González-Ravé J.M., González-Mohíno F., Rodrigo-Carranza V., Pyne D.B. *Reverse
Periodization for Improving Sports Performance: A Systematic Review.* Sports Medicine -
Open, 8:56, 2022. DOI 10.1186/s40798-022-00445-8. Vérifiée le 22/09/2026.

11 études, 200 athlètes : la périodisation inversée n'apporte pas de gain supérieur au
modèle traditionnel ou en blocs (course, natation, VO2max, force). Qualité des études
modeste (PEDro moyen 4,9). **Niveau : modéré** — dit surtout qu'**aucun modèle ne s'impose**.
→ fonde D-63a (pas de modèle de périodisation privilégié)

## NUT — Nutrition, hydratation

### S-NUT-001 — Apport glucidique à l'effort : fourchettes recommandées
Tiller N.B. et coll. *International Society of Sports Nutrition Position Stand:
nutritional considerations for single-stage ultra-marathon training and racing.*
Journal of the International Society of Sports Nutrition, 16(1):50, 2019.
https://pubmed.ncbi.nlm.nih.gov/31699159/

Complété par : *From Metabolism to Medals: Contemporary Perspectives and Revisiting
Carbohydrate Guidelines for Fueling Endurance Athletes during Exercise*, 2026.
https://www.sciencedirect.com/science/article/pii/S002231662600091X

Les recommandations s'étagent de 30 à 90 g/h selon la durée, l'intensité, la tolérance
et la praticité ; jusqu'à 90 g/h de glucides à transporteurs multiples pour un effort de
plus de 2,5 à 3 h. Le taux d'utilisation des glucides dépend largement de l'intensité,
plus basse sur les épreuves longues — d'où des besoins horaires moindres pour les
finishers lents. Des apports de 120 g/h ont été tolérés et bénéfiques chez des
trailers élite entraînés, mais uniquement après entraînement digestif.
**Niveau : élevé** pour la fourchette générique (position officielle + revue récente).
→ fonde G-NUT-001 et D-30 dans SPEC.md

### S-NUT-002 — Entraînement digestif : protocole de progression
*The Effect of Gut-Training and Feeding-Challenge on Markers of Gastrointestinal Status
in Response to Endurance Exercise: A Systematic Literature Review.* Sports Medicine,
2023. DOI 10.1007/s40279-023-01841-0
https://link.springer.com/article/10.1007/s40279-023-01841-0

Revue systématique : l'exposition répétée du tube digestif aux glucides pendant
l'exercice améliore la tolérance et réduit les symptômes. Protocole pratique associé,
issu de la traduction appliquée de cette littérature : augmenter d'environ 5 à 10 g/h par
semaine, consolider 3 à 4 semaines à la dose cible, compter au moins 8 à 10 semaines au
total, et pratiquer l'alimentation de course au moins trois fois par semaine dont une
sortie longue — l'exposition régulière primant sur les grosses séances occasionnelles.
**Niveau : modéré** — revue systématique solide sur le principe, mais études de petite
taille, populations entraînées, et les **valeurs précises du protocole (5–10 g/h par
semaine) relèvent de la traduction pratique**, pas d'un essai comparatif.
→ fonde la case 4 de G-NUT-001 dans SPEC.md

### S-NUT-003 — Hydratation : variabilité individuelle et absence de cible générique
Même position stand que S-NUT-001 (Tiller et coll., 2019).

Les besoins hydriques à l'effort dépendent du taux de sudation individuel, lui-même
fonction des conditions, de l'intensité et du sujet ; la stratégie recommandée reste
largement guidée par la soif plutôt que par un volume horaire fixe, le sur-apport
comportant son propre risque.
**Niveau : modéré** pour l'absence de cible générique exploitable.
→ justifie l'exclusion de l'hydratation du modèle (D-30) : sans pesée avant/après, le
volume bu n'a pas d'observation correctrice.

## COU — Course à pied, physiologie de l'endurance

### S-COU-001 — Coût énergétique de la course selon la pente
Minetti A.E., Moia C., Roi G.S., Susta D., Ferretti G.
*Energy cost of walking and running at extreme uphill and downhill slopes.*
Journal of Applied Physiology, 93(3):1039-1046, 2002. DOI 10.1152/japplphysiol.01177.2001
https://journals.physiology.org/doi/10.1152/japplphysiol.01177.2001

Mesure du coût métabolique de la marche et de la course sur tapis, de -45 % à +45 % de
pente. Reste la référence par défaut du domaine et le fondement de la plupart des
calculs d'allure ajustée à la pente.
**Niveau : modéré** comme référence de groupe.
**Réserve majeure :** population d'origine restreinte (hommes bien entraînés, habitués
à la montagne). Non généralisable à un individu — voir S-TRA-001.
→ amorce G-TER-001 (SPEC.md)

### S-COU-002 — Vitesse critique estimée depuis les données d'entraînement
Smyth B., Muniz-Pumares D.
*Calculation of Critical Speed from Raw Training Data in Recreational Marathon Runners.*
Medicine & Science in Sports & Exercise, 52(12):2637-2645, 2020.
DOI 10.1249/MSS.0000000000002412
https://pmc.ncbi.nlm.nih.gov/articles/PMC7664951

Plus de 25 000 coureurs récréatifs. La vitesse critique calculée à partir des meilleures
allures ajustées à la pente sur 400 à 5000 m issues de l'entraînement prédit la
performance marathon (erreur ~8 %). Les coureurs partant au-delà de 94 % de leur VC
ralentissent davantage en seconde moitié.
**Niveau : modéré** — très grand échantillon, mais données de plateforme grand public
et population marathon route.
→ fonde G-CAP-001 (SPEC.md)

### S-COU-003 — Détermination à distance de la vitesse critique
Hunter B., Ledger A., Muniz-Pumares D.
*Remote Determination of Critical Speed and Critical Power in Recreational Runners.*
International Journal of Sports Physiology and Performance, 18(12):1449-1456, 2023.
https://repository.londonmet.ac.uk/8870/

23 coureurs récréatifs, 8 semaines. Les estimations de VC issues de l'entraînement
habituel (6 semaines) ne diffèrent pas de celles issues de contre-la-montre ou de tests
3 min all-out, avec un accord fort et une excellente reproductibilité pour la VC.
En revanche, l'accord est limité pour D' (capacité au-dessus de la VC).
**Niveau : faible à modéré** — échantillon réduit (4 femmes), terrain non trail.
→ fonde G-CAP-001 et D-07 (SPEC.md)

### S-COU-004 — Découplage interne/externe et durabilité en marathon — **VÉRIFIÉE**
Smyth B., Maunder E., Meyler S., Hunter B., Muniz-Pumares D. *Decoupling of Internal and
External Workload During a Marathon: An Analysis of Durability in 82,303 Recreational
Runners.* Sports Medicine, 52(9):2283-2295, 2022. DOI 10.1007/s40279-022-01680-5
https://pmc.ncbi.nlm.nih.gov/articles/PMC9388405/

82 303 marathoniens (13 125 femmes). Charge interne = % de la FC maximale ; charge
externe = vitesse rapportée à la vitesse critique estimée. Le rapport interne/externe
augmente d'environ 16 % entre le km 10 et les km 35-40. Apparition du découplage vers
25 km en moyenne, mais à 33,4 km chez les coureurs à faible découplage contre 19,1 km
chez ceux à découplage élevé. La vitesse critique seule prédit le temps final à environ
6,5 % d'erreur ; ajouter l'ampleur et le moment du découplage ramène l'erreur à ~5,2 %.
**Niveau : élevé** — très grand échantillon, revue de premier plan.
**Vérifiée le 17/09/2026** : citée de mémoire depuis le 16/09 alors qu'elle fondait
**la totalité de G-FAT-001**. Confirmée, chiffres inclus.
**Réserve partiellement levée** : la transposition à l'ultra n'est plus une pure
extrapolation — De Pauw et coll. (2024) rapportent le même phénomène sur un
ultramarathon « backyard », les coureurs les moins performants montrant un découplage
FC/vitesse significativement plus élevé dans le dernier quart
(cité dans https://www.tandfonline.com/doi/full/10.1080/02640414.2025.2567780).
**Réserve maintenue** : ni le marathon route ni le backyard n'ont de dénivelé — le cas
trail reste non couvert.
→ fonde G-FAT-001 (SPEC.md)

### S-COU-005 — Désentraînement : cinétique de perte
Mujika I., Padilla S. *Detraining: loss of training-induced physiological and
performance adaptations. Part II: Long term insufficient training stimulus.*
Sports Medicine, 30(3):145-154, 2000. https://pubmed.ncbi.nlm.nih.gov/10999420/

Complété par : *Cardiorespiratory and metabolic consequences of detraining in endurance
athletes.* Frontiers in Physiology, 2023.
https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2023.1334766/full

À l'arrêt, la VO2max baisse dès quelques jours (environ 7 % à 12 jours), des baisses
significatives sont rapportées entre 2 et 4 semaines, et la décroissance se poursuit de
façon quasi linéaire jusqu'à environ 20 % sur des arrêts prolongés. Point essentiel pour
nous : chez l'athlète, la VO2max reste au-dessus des valeurs des non-entraînés, tandis
que les gains les plus récents sont entièrement perdus.
**Niveau : modéré** — revue et travaux convergents, mais populations entraînées jeunes.
→ fonde D-15 et D-16 dans SPEC.md

### S-COU-006 — Affûtage : durée et ampleur optimales
Bosquet L., Montpetit J., Arvisais D., Mujika I. *Effects of Tapering on Performance:
A Meta-Analysis.* Medicine & Science in Sports & Exercise, 39(8):1358-1365, 2007.
https://www.semanticscholar.org/paper/a41517ab5fa06b92568b861e2b1aa32b3003d214

Complété par : Wang et coll. *Effects of tapering on performance in endurance athletes:
a systematic review and meta-analysis.* PLOS ONE, 2023. DOI 10.1371/journal.pone.0282838
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10171681/

Et par : *Longer Disciplined Tapers Improve Marathon Performance for Recreational
Runners.* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8506252/

Bosquet (27 études) : réduire le volume de 41 à 60 % sur environ deux semaines, en
maintenant intensité et fréquence, améliore la performance d'environ 2,2 % — les coureurs
concernés finissant environ 2,6 % plus vite. Wang (14 études) : effet le plus marqué sur
8 à 14 jours, gains également sur 7 et sur 15 à 21 jours. Chez des marathoniens
récréatifs, un affûtage strict de 3 semaines fait gagner environ 5 min 32 s (2,6 %)
comparé à un affûtage minimal.
**Niveau : élevé** pour la durée et l'ampleur de l'affûtage — deux méta-analyses
convergentes plus une étude sur grand échantillon récréatif.
**Limite décisive pour nous : aucune de ces sources ne dit combien de fois par an on peut
s'affûter.** La règle de D-25 en déduit un budget par soustraction ; les durées de
récupération post-course qu'elle emploie ne viennent d'aucune de ces sources et sont
marquées extrapolation.
→ fonde D-25, contextualise D-21 (affûtage) dans SPEC.md

### S-COU-007 — Signification physiologique de la vitesse/puissance critique
*Is Stryd critical power a meaningful parameter for runners?*
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10286607/

La puissance critique mesurée sur le terrain se situe à proximité du second seuil
ventilatoire (ou de l'OBLA), ce qui lui donne un ancrage physiologique et non purement
statistique.
**Niveau : modéré** — étude unique, échantillon réduit. Suffisant pour ancrer le
repère « travail au seuil ≈ 100 % de la vitesse de référence », insuffisant pour en
déduire les autres bornes d'intensité, qui restent des extrapolations.
**Créée le 17/09/2026 lors de l'audit** : cette affirmation était auparavant rattachée
à S-MES-003, une entrée de veille produit sans valeur de preuve.
→ fonde D-29 dans SPEC.md

### S-COU-008 — Polarisé vs seuil : méta-analyse d'essais randomisés
Rosenblat M.A., Perrotta A.S., Vicenzino B. *Polarized vs. Threshold Training Intensity
Distribution on Endurance Sport Performance: A Systematic Review and Meta-Analysis of
Randomized Controlled Trials.* Journal of Strength and Conditioning Research,
33(12):3491-3500, 2019. DOI 10.1519/JSC.0000000000002618
https://pubmed.ncbi.nlm.nih.gov/29863593/

Effet modéré en faveur du modèle polarisé sur la performance en contre-la-montre, contre
un modèle centré sur le seuil.
**Niveau : modéré**, avec une réserve posée par les auteurs eux-mêmes : seulement quatre
essais comparés, base de preuve limitée.
→ fonde D-34 dans SPEC.md

### S-COU-009 — Polarisé vs pyramidal : méta-analyse en données individuelles
Rosenblat M.A., Watt J., Arnold J., Treff G., Sandbakk Ø., Seiler S. *Which Training
Intensity Distribution Intervention will Produce the Greatest Improvements in Maximal
Oxygen Uptake and Time-Trial Performance in Endurance Athletes? A Systematic Review and
Network Meta-analysis of Individual Participant Data.* 2025.
https://pubmed.ncbi.nlm.nih.gov/39888556/

Différences plus petites qu'attendu entre modèles polarisé et pyramidal, avec un effet
qui dépend de la distance : léger avantage polarisé sur 5-10 km, léger avantage
pyramidal sur marathon. Notable : Stephen Seiler, auteur du concept polarisé, est
coauteur de cette nuance.
**Niveau : modéré à élevé** — méthodologie en données individuelles, plus robuste
qu'une méta-analyse classique. **Aucune distance au-delà du marathon n'est couverte** :
l'extension à l'ultra-trail dans D-34 est une extrapolation de la tendance, pas une
donnée.
→ fonde D-34 dans SPEC.md

### S-COU-010 — Entraînement par intervalles en pyramide (protocole de séance)
Thibault G., Dubois B. *Le mystère de la grande pyramide : l'entraînement par EPI sans
se blesser.* Zatopek, #21, p. 20-25, 2012.
https://lacliniqueducoureur.com/coureurs/medias/magazine/le-mystere-de-la-grande-pyramide-l-entrainement-par-epi-sans-se-blesser-zatopek-21-2012/

Protocole de séance en « pyramide » : fractions d'effort à allure cible fixe, distance
croissante puis décroissante (100 m, 200 m, 300 m… jusqu'à un sommet propre à chaque
coureur, souvent 700-800 m), récupérations passives calées sur le temps de la fraction.
L'intérêt avancé : cumuler beaucoup plus de temps aux allures élevées qu'en continu, à
fatigue ressentie égale. Vitesse cible calculée depuis une performance récente sur
distance proche, via les tables de cotation IAAF. Règle de progression associée :
introduction sur 6 semaines, jamais plus de 2 séances intenses par semaine, repos complet
la veille et le lendemain, arrêt immédiat sur douleur persistante à une articulation ou
un tendon.
**Niveau : sans objet** — synthèse experte de deux praticiens (Guy Thibault,
physiologiste ; Blaise Dubois, physiothérapeute), **aucune référence primaire citee dans
le texte**, rien à remonter derrière. Article de 2012.
**Précision importante :** ce « pyramidal » désigne la forme d'une séance (fractions
croissantes puis décroissantes), à ne pas confondre avec le modèle de répartition
saisonnière du même nom étudié par Seiler/Rosenblat (S-COU-008, S-COU-009, fonde D-34) —
deux concepts distincts sous un même mot.
→ fonde le protocole du type Intervalles dans G-CAT... voir D-29 (SPEC.md)

### S-COU-011 — Vitesse ascensionnelle comme indicateur d'intensité en pente forte
*Specific Incremental Test for Aerobic Fitness in Trail Running: IncremenTrail.*
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9693161/

Entre 25 et 40 % de pente, la vitesse ascensionnelle (VAM) est un indicateur pertinent
de l'intensité : le VO2 atteint à l'épuisement et les seuils ventilatoires ne diffèrent
pas entre des tests à 25 % et à 40 % de pente lorsqu'on pilote par cette variable.
**Niveau : modéré** — étude spécifique au trail, méthodologie de test incrémental.
**Complète S-COU-001** (Minetti) : à pente très raide, le déplacement vertical domine
le coût énergétique (jusqu'à ~75 % du coût total sur une pente à 30 %), ce qui justifie
physiologiquement l'abandon de l'allure horizontale au profit du VAM.
→ fonde le traitement de la marche (bande G-TER-001) dans SPEC.md

### S-COU-012 — Fréquence respiratoire comme marqueur d'effort
*Respiratory Rate is a Valid and Reliable Marker for the Anaerobic Threshold.*
https://ncbi.nlm.nih.gov/pmc/articles/PMC3899665
Foster C. et coll., travaux sur le test de la parole (talk test), synthétisés par l'ACE :
https://www.acefitness.org/certifiednewsarticle/888/ace-sponsored-research-validating-the-talk-test-as-a-measure-of-exercise-intensity/

La fréquence respiratoire est un marqueur valide et reproductible du seuil, confirmé par
plusieurs travaux indépendants. Le test de la parole fonctionne d'ailleurs par ce
mécanisme : parler impose de ralentir la respiration, ce qui devient impossible au point
où la fréquence respiratoire s'emballe — il identifie les seuils ventilatoires sans test
maximal.
**Niveau : modéré.** Réserves : la fréquence respiratoire au seuil ne permet pas
d'identifier l'intensité en compétition (elle y est plus élevée), et les limites d'accord
individuelles du test de la parole sont larges — c'est un repère, pas une mesure.
→ fonde le repère respiratoire optionnel de D-54 (SPEC.md)

### S-COU-013 — Pratique d'entraînement des coureurs de fond de classe mondiale
Haugen T., Sandbakk Ø., Seiler S., Tønnessen E. *The Training Characteristics of
World-Class Distance Runners: An Integration of Scientific Literature and Results-Proven
Practice.* Sports Medicine - Open, 8:46, 2022. Référence confirmée par recoupement le
22/09/2026 (résumé non relu intégralement).

Synthèse littérature + pratique : à l'approche de l'objectif, c'est le volume couru **à
allure de course** qui augmente, pas le volume total ; la plupart des coureurs de haut
niveau ne réduisent sensiblement leur volume que dans les 7 à 10 derniers jours. **Niveau :
faible à modéré** (élites, piste et route ; synthèse, pas un essai).
→ fonde D-63a ; appuie D-63e (sortie longue maintenue en début d'affûtage)

## TRA — Spécificités trail

### S-TRA-001 — Coût de course en côte : variabilité individuelle — **VÉRIFIÉE**
Deux références, pas une :
Balducci P., Clémençon M., Morel B., Quiniou G., Saboul D., Hautier C.A. *Comparison of
Level and Graded Treadmill Tests to Evaluate Endurance Mountain Runners.* Journal of
Sports Science and Medicine, 15(2):239-246, 2016. PMCID PMC4879436
https://pubmed.ncbi.nlm.nih.gov/27274660/
Balducci P., Clémençon M., Trama R., Hautier C.A. *The Calculation of the Uphill Energy
Cost of Running from the Level Energy Cost of Running in a Heterogeneous Group of
Mountain Ultra Endurance Runners.* Asian Journal of Sports Medicine, 8(1):e42091, 2017.
DOI 10.5812/asjsm.42091

Groupe homogène de coureurs de montagne de bon niveau (2016) : les coûts en côte à
12,5 % et 25 % sont corrélés entre eux (r = 0,78), alors que le coût au plat n'est
corrélé à aucun des deux (r = 0,09 et r = 0,10). Groupe hétérogène de 24 ultra-traileurs
(2017), pente de 10 % : corrélation forte plat/côte (r = 0,84 avant, r = 0,86 après un
ultra de montagne), mais l'écart entre coût théorique (équation de di Prampero) et coût
mesuré atteint 7,9 % et 8,5 % — les auteurs concluent qu'une **mesure du coût en côte est
nécessaire** pour prédire la performance.
**Niveau : modéré** — deux études convergentes, échantillons réduits, protocole tapis.
**Vérifiée le 17/09/2026.** Nuance ajoutée par une source tierce (Frontiers in
Physiology, 2021, https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2021.697315/full) :
la corrélation plat/côte existe chez les traileurs **élite** (Willis et coll. 2019) mais
pas chez les sub-élite (Balducci) — la variabilité individuelle est donc **plus forte
dans notre population cible**, ce qui renforce le motif de G-TER-001.
→ motive le rejet de S-COU-001 comme valeur finale dans G-TER-001 (SPEC.md)

### S-TRA-002 — Volume d'entraînement des finishers d'ultras de montagne
*Sleep and Ultramarathon: Exploring Patterns, Strategies, and Repercussions of 1,154
Mountain Ultramarathons Finishers.* Sports Medicine – Open, 2024.
https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-024-00704-w

1 154 finishers (Diagonale des Fous, Trail de Bourbon). Durée d'entraînement
hebdomadaire moyenne : 8,3 ± 4,0 heures.
**Niveau : faible** pour notre usage — donnée **descriptive** d'un peloton de finishers,
en aucun cas prescriptive. L'écart-type de 4 h est l'information principale : la
fourchette individuelle va d'environ 4 h à plus de 12 h.
→ contextualise D-21 dans SPEC.md

### S-TRA-003 — Volume et probabilité de terminer un 50 km — **à vérifier**
Étude rapportée secondairement : les finishers d'un 50 km affichaient un volume
nettement supérieur aux non-finishers dans les semaines précédant la course (~77 contre
~51 km/semaine) et sur l'année (~58 contre ~32 km/semaine).
**Référence primaire non vérifiée** — auteurs, titre, revue et année à confirmer.
**Niveau provisoire : faible**, et **association, pas causalité** : beaucoup de coureurs
sous ces volumes terminent malgré tout.
→ contextualise D-19 dans SPEC.md

### S-TRA-004 — Rendement décroissant du volume — veille, pas une source scientifique
Propos d'entraîneur (Jason Koop), rapportés par Suunto.
https://www.suunto.com/de-AT/sports/News-Articles-container-page/Four-myths-about-ultra-running-that-you-need-to-know/

Au-delà d'environ 9 h par semaine, chaque tranche de 10 % de volume supplémentaire
n'apporte plus 10 % de progression, parfois 1 %. Repères cités : 10 à 12 h pendant 8 à
10 semaines pour un 100 milles, environ 9 h pendant 6 à 8 semaines pour un 50 km.
**Niveau : sans objet** (avis d'expert, aucune donnée publiée). Sert uniquement à
justifier la **structure par phases** de D-21 plutôt qu'un volume moyen soutenu.
→ contextualise D-21 dans SPEC.md

---

### S-TRA-005 — Correspondance manuelle profil de course → séances (pratique de coach)
Observation de pratique professionnelle, **pas une source scientifique**.
*Smarter Training Starts With a Map*, Footpath.
https://footpathapp.com/blog/smarter-training-starts-with-a-map/
*Training Considerations for Mountain Trail Races*, Higher Running.
https://higherrunning.substack.com/p/training-considerations-for-mountain

Des coachs cartographient le profil de la course visée et conçoivent des séances qui en
reproduisent la durée et le dénivelé des montées plutôt que de prescrire une durée
abstraite ; connaître la répartition du D+ (montées soutenues contre relief roulant) est
jugé précieux pour cibler l'entraînement adapté.
**Niveau : sans objet** (veille de pratique professionnelle). Sert à établir que la
correspondance profil → séance est une pratique de coach existante, pas un besoin
inventé, et qu'elle se fait aujourd'hui à la main.
→ fonde D-28 dans SPEC.md

### S-TRA-006 — Périodisation inversée et spécificité progressive en ultra-trail —
**vérifiée le 22/09/2026**
Jaén-Carrillo D., Margarit-Boscà A. *Reverse periodization in ultratrail: The road to the
2023 World Mountain and Trail Running Championships of an elite female ultrarunner.*
Current Issues in Sport Science, 9(4), 2024. DOI 10.36950/2024.4ciss039.
https://doaj.org/article/b81bc617a4404a499f34edd3d493eedc
**Statut confirmé : résumé de communication, étude de cas n = 1** (29 semaines analysées
a posteriori ; 8h53 par semaine en moyenne, 14h58 la semaine la plus chargée).

Résumé de communication : la spécificité de l'entraînement (intensité de course, mode
d'exercice, caractéristiques de la course) progresse au long du macrocycle, avec
davantage de sorties vallonnées, de sorties longues et de modes spécifiques (marche,
séances mixtes) à mesure qu'on se rapproche des courses principales.
**Niveau : faible** (confirmé — un seul cas, élite, résumé). Nuance relevée à la
vérification : l'athlète suit une périodisation **inversée** ; S-CHA-005 montre que ce
modèle n'est pas supérieur aux autres — la source illustre la spécificité croissante, elle
ne prouve pas qu'il faille la suivre.
→ fonde D-28 dans SPEC.md (spécificité croissante en fin de cycle)

### S-TRA-007 — Durée de préparation semi-marathon : convergence de pratique
Plusieurs guides de coaching indépendants (Marathon Handbook, Coach, RunToTheFinish,
TrainingPeaks), consultés le 17/09/2026.

Convergence entre sources indépendantes : coureur déjà régulier → 8–10 semaines ;
niveau intermédiaire → 12–16 semaines ; débutant complet → 16–20 semaines.
**Niveau : faible** — aucune étude contrôlée, mais accord entre plusieurs sources
indépendantes plutôt qu'une affirmation isolée.
**Usage :** notre minimum actuel de 8 semaines (D-21, tranche 10–21 km) ne correspond
qu'au cas « coureur déjà régulier » ; un débutant complet sur cette tranche est mal
couvert par la valeur minimale telle qu'écrite.
→ nuance D-21 dans SPEC.md

### S-TRA-008 — Concept du « minimum-maximum » en préparation ultra
Koop J. *How Much Do You Need To Train For A 100-Mile Ultramarathon?*, CTS (Carmichael
Training Systems), consulté le 17/09/2026.
https://trainright.com/how-much-do-you-need-to-train-for-a-100-mile-ultramarathon/

Coach ultra reconnu, auteur de *Training Essentials for Ultrarunning*. Concept du
« minimum-maximum » : le bloc de plus haut volume doit se placer 6 à 9 semaines avant la
course, pas nécessairement le volume moyen sur tout le cycle.
**Niveau : sans objet** (avis d'expert publié, pas une étude) — proche de notre fenêtre
de 8–10 semaines pour la tranche 60–100 km, mais ne la remplace pas comme preuve.
→ nuance D-21 dans SPEC.md : confirme qu'il existe une convergence de pratique, pas
seulement notre propre interpolation, sans élever le niveau de preuve au-delà de
« extrapolation » pour les valeurs chiffrées.

### S-TRA-009 — Sorties longues consécutives ("back-to-back") en ultra
Convergence de pratique, consultée le 17/09/2026 : Koop J. (CTS/trainright.com,
concept de "block training" et de "DIY ultrarunning camp") ; ultrarunning.com ;
Trail Runner Magazine ; Marathon Handbook.

Plusieurs coachs indépendants situent cet outil de la même façon : deux sorties
substantielles sur des jours consécutifs plutôt qu'une seule sortie démesurée, pour
simuler la fatigue accumulée d'un ultra avec un coût de récupération et un risque de
blessure moindres. Réservé aux formats **50 miles / 100 km et au-delà** ; placé dans le
**bloc spécifique** (jamais en fond, une base aérobie doit déjà exister) ; typiquement
4 à 8 semaines avant la course ; aborder cette séance depuis un état déjà fatigué en
réduit l'intérêt et augmente le risque de blessure.
**Niveau : sans objet** (convergence de pratique de coachs, aucune étude contrôlée).
→ fonde l'amendement de D-22 dans SPEC.md

### S-TRA-010 — Kilomètre-effort : convention de conversion distance/dénivelé
Convention de pratique largement répandue en trail francophone (campus.coach,
randonner-leger, FFME), consultée le 17/09/2026 ; origine attribuée aux militaires
alpins.

`km-effort = distance (km) + D+ (m) / 100` — soit 100 m de dénivelé positif comptés
comme 1 km à plat. Variante incluant le D− (souvent 200 m de D− pour 1 km). Sert à
estimer grossièrement la charge et le temps d'effort d'un parcours.
**Niveau : sans objet** (convention de pratique, aucune validation expérimentale).
**Limites explicites, reconnues par les sources elles-mêmes** : ne prend pas en compte
la technicité, ni le profil (une montée continue de 1500 m est plus exigeante que le
même D+ réparti en petites bosses), ni l'individu — c'est un coefficient fixe là où
S-TRA-001 montre que le coût en côte varie fortement d'un coureur à l'autre.
**Usage dans le modèle : amorçage uniquement.** Remplacé par l'estimation issue de
G-CAP-001 et G-TER-001 dès que celles-ci convergent — exactement le rôle tenu par
S-COU-001 pour le coût-pente.
→ fonde D-44 dans SPEC.md

### S-TRA-011 — Coût de récupération du trail à durée égale : différence avec la route
*Muscle, Neuromuscular, and Cardiac Damage in Trail Running: A Systematic Review.* 2025,
PROSPERO CRD420251135043. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12921809/
Complété par : *Downhill Running: What Are The Effects and How Can We Adapt? A Narrative
Review.* Sports Medicine, 2020. DOI 10.1007/s40279-020-01355-z
Et, pour le facteur d'équivalence uniquement : The Running Genie (2026), veille de
pratique — https://therunninggenie.com/blog/trail-running-vs-road-running

Le trail induit un stress musculaire, neuromusculaire et cardiaque substantiel,
particulièrement sur les épreuves à forte charge excentrique ; la descente repose sur des
contractions excentriques associées à une fatigue importante et un risque de blessure
élevé. À durée égale, une semaine chargée en trail récupère plus lentement qu'une semaine
route. Profil d'intensité également différent : la route est proche d'un état stable, le
trail ressemble davantage à du fractionné (FC qui monte en côte, redescend en descente).
Facteur d'équivalence empirique employé par des coachs : **1 h de trail modéré ≈ 1,2 à
1,4 h de route** pour la comptabilité de fatigue.
**Niveau : modéré** pour la différence de coût de récupération (revue systématique +
revue narrative). **Sans objet** pour le facteur 1,2–1,4 — convention de coachs, aucune
validation expérimentale.
**Usage dans le modèle : amorçage uniquement** — remplacé par la tolérance observée
(G-PLA-002, D-33) dès qu'elle converge.
→ corrige D-44 dans SPEC.md

## BLE — Gêne, douleur, charge d'impact

### S-BLE-001 — Modèle de surveillance de la douleur sous charge
Silbernagel K.G., Thomeé R., Eriksson B.I., Karlsson J. *Continued Sports Activity, Using
a Pain-Monitoring Model, During Rehabilitation in Patients With Achilles Tendinopathy: A
Randomized Controlled Study.* American Journal of Sports Medicine, 35(6):897-906, 2007.
DOI 10.1177/0363546506298279. https://pubmed.ncbi.nlm.nih.gov/17307888/

Essai randomisé. Les patients qui poursuivaient la course et les sauts en suivant un
modèle de surveillance de la douleur ont obtenu des résultats équivalents à ceux mis au
repos six semaines. Le modèle autorise une douleur pendant et après la charge jusqu'à
environ 5 sur 10, à condition qu'elle revienne à son niveau de base le lendemain matin et
qu'elle n'augmente pas d'une semaine à l'autre.
**Niveau : modéré** — essai randomisé, devenu la règle clinique de référence pour le
dosage de charge en tendinopathie.
**Limite décisive : population de tendinopathies achilléennes en rééducation.** L'appliquer
à la surveillance générale d'une gêne chez un coureur sain est une **extrapolation**, à
signaler comme telle partout où D-32 l'emploie.
→ fonde D-32 dans SPEC.md

### S-BLE-002 — Course récréative et arthrose de hanche et de genou
Alentorn-Geli E. et coll. *The Association of Recreational and Competitive Running With
Hip and Knee Osteoarthritis: A Systematic Review and Meta-analysis.* Journal of
Orthopaedic & Sports Physical Therapy, 47(6):373-390, 2017. DOI 10.2519/jospt.2017.7137
https://pubmed.ncbi.nlm.nih.gov/28504066/

25 études, 125 810 individus (17 études et 114 829 individus méta-analysées). Prévalence
d'arthrose de hanche et de genou : 3,5 % chez les coureurs récréatifs, 10,2 % chez les
témoins sédentaires, 13,3 % chez les coureurs de compétition.
**Niveau : modéré à élevé** — très grand échantillon, mais études observationnelles :
association, pas causalité, avec un biais de sélection plausible (les articulations
fragiles cessent de courir).
**Usage dans le modèle : négatif.** Cette source ne justifie aucune prescription ; elle
**interdit** l'argumentaire « le vélo protège tes articulations » (D-31). La relation
n'est pas linéaire : le volume très élevé de la compétition est associé à davantage
d'arthrose — le sujet est le dosage, pas l'impact en soi.
→ fonde l'interdit d'argumentaire santé de D-31 dans SPEC.md

### S-BLE-003 — Retour à la course après blessure : protocoles de progression
Protocoles cliniques convergents, consultés le 17/09/2026 : Ohio State University
Wexner Medical Center, *Basic Return to Running Guideline*
(https://wexnermedical.osu.edu/-/media/files/wexnermedical/patient-care/healthcare-services/sports-medicine/education/medical-professionals/other/basic-return-to-running-guideline.pdf) ;
The Prehab Guys, *Return To Running After Injury* ; Warden et coll. 2021 (gestion des
lésions osseuses de stress, cité secondairement).

Principes convergents : progression **marche-course graduée** (alterner marche et
fractions courues, allonger progressivement les fractions courues jusqu'à la course
continue facile) ; **fréquence avant intensité, durée avant vitesse** ; 3 sorties par
semaine au plus, jamais deux jours de suite en début de reprise ; progression
**guidée par les symptômes, pas par le calendrier** — douleur pendant l'échauffement :
2 jours d'arrêt et retour au palier précédent ; pendant la séance : 1 jour d'arrêt et
retour au palier précédent ; après la séance : rester au même palier. Retour à
l'entraînement normal lorsque 75 à 80 % du volume hebdomadaire d'avant blessure est
atteint sans symptôme pendant 2 à 3 semaines consécutives. Augmentation hebdomadaire de
10 à 30 % ensuite.

**Délais très variables selon le tissu** : une lésion musculaire mineure peut autoriser
un footing léger en 10 à 14 jours, une fracture de fatigue tibiale demande 6 à 8 semaines
ou plus sans course. **Aucune application ne peut trancher cela** — c'est la raison pour
laquelle D-50 exige l'avis d'un professionnel plutôt que de l'estimer.

**Niveau : faible.** Les sources le disent elles-mêmes : le principe marche-course
gradué et les règles de douleur par tissu sont solides, mais les protocoles chiffrés
construits dessus relèvent du consensus et de l'expérience clinique, **pas d'essais
contrôlés**. Les délais publiés sont des points de départ, pas des garanties.
→ fonde D-51 (SPEC.md)

### S-BLE-004 — Séance isolée au-delà de la plus longue des 30 derniers jours
Schuster Brandt Frandsen J., Hulme A., Parner E.T., Møller M., Lindman I., Abrahamson J.
et coll., Nielsen R.O. *How much running is too much? Identifying high-risk running
sessions in a 5200-person cohort study.* British Journal of Sports Medicine,
59:1203-1210, 2025. DOI 10.1136/bjsports-2024-109380. Vérifiée le 22/09/2026.

Cohorte prospective, 5 205 coureurs récréatifs (âge moyen 46 ans, 22 % de femmes),
18 mois, 588 071 séances enregistrées par montre GPS, 1 820 blessés. Une séance dépassant
de plus de 10 % la plus longue des 30 jours précédents augmente le taux de blessure de
surmenage : +10–30 % → HR 1,64 ; +30–100 % → 1,52 ; > +100 % → 2,28. **La hausse de
volume d'une semaine à l'autre n'est pas associée**, le rapport aigu/chronique l'est
négativement. Les coureurs sans aucune séance dans les 30 jours précédents (état « non
calculable ») ne montrent pas de risque accru (HR 0,82, non significatif).
**Limite posée par les auteurs** : le résultat porte sur une séance isolée ; des hausses
de 10 % **enchaînées** sur plusieurs séances rapprochées (11, 12,1 puis 13,3 km dans la
même semaine) peuvent rester excessives faute de récupération.
**Niveau : modéré** (grande cohorte, observationnelle, auto-déclaration des blessures,
**en distance, sur route**) — transposition à la **durée** et au trail : **extrapolation**
(H-21).
→ fonde D-63c ; sa limite fonde D-63k1 ; l'état « non calculable » appuie D-63k5

## MES — Fiabilité de mesure et capteurs

### S-MES-001 — FC optique poignet en course régulière
Parak J., Uuskoski M., Machek J., Korhonen I.
*Estimating Heart Rate, Energy Expenditure, and Physical Performance With a Wrist
Photoplethysmographic Device During Running.*
JMIR mHealth and uHealth, 5(7):e97, 2017. DOI 10.2196/mhealth.7437
https://mhealth.jmir.org/2017/7/e97/

24 volontaires, course auto-régulée en extérieur et test maximal en laboratoire. La FC
optique poignet mesure la FC avec une erreur moyenne de 1,9 % jusqu'à la FC maximale,
référence ECG.
**Niveau : modéré** — échantillon réduit, mais mesure directe contre référence ECG.
**Portée :** course régulière. Ne dit rien des conditions de trail.
→ fonde D-09 (affichage libre de la FC) dans SPEC.md

### S-MES-002 — FC optique poignet en trail — **VÉRIFIÉE**
Navalta J.W., Montes J., Bodell N.G., Salatto R.W., Manning J.W., DeBeliso M.
*Concurrent heart rate validity of wearable technology devices during trail running.*
PLoS ONE, 15(8):e0238569, 2020. DOI 10.1371/journal.pone.0238569
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7458324/

21 participants (10 femmes), course en sentier de 3,22 km en aller-retour (1,61 km de
montée puis 1,61 km de descente), allure libre. Dispositifs : montre Garmin Fenix 5 au
poignet, écouteurs, bague, brassard d'avant-bras, montre Suunto avec ceinture ;
référence : ceinture Polar H7. Conclusion des auteurs : **quelle que soit la position sur
le corps** (doigt, poignet, oreille, avant-bras), les dispositifs à photopléthysmographie
ne fournissent pas une validité de FC acceptable sur un trail de plus de 20 minutes ;
ils recommandent une ceinture à base ECG en extérieur.
**Niveau : modéré** — protocole représentatif de notre usage, mais **échantillon réduit
et parcours très court (3,22 km)** : l'extrapolation à une sortie de plusieurs heures
reste une extrapolation.
**Vérifiée le 17/09/2026.** Les auteurs soulignent que les validations classiques se font
en régime stationnaire, ce qui surestime la précision réelle en conditions variées.
→ fonde D-09 et D-10 (admissibilité par segment) dans SPEC.md

### S-MES-003 — Capacité de référence auto-calculée : pratique du marché
Observation de l'état de l'art produit, **pas une source scientifique**.
Stryd calcule automatiquement la puissance critique depuis les données d'entraînement
récentes depuis 2019, en exigeant des efforts de durées variées (10-30 s, 10-20 min).
Intervals.icu calcule de même une allure critique depuis la courbe des meilleures
performances. La puissance critique mesurée par Stryd se situe près du second seuil
ventilatoire ou de l'OBLA → *Is Stryd critical power a meaningful parameter for
runners?*, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10286607/
**Niveau : sans objet** (veille produit). Sert uniquement à situer nos choix par
rapport à l'existant : l'auto-calcul et l'exigence de protocole sont standards, la
calibration d'une correction de pente personnelle ne l'est pas.
→ contextualise G-CAP-001, D-07 et D-12 dans SPEC.md

## Trous identifiés

Sujets où l'app décide sans appui solide. À traiter en priorité quand on développera
le modèle allure-effort.

| Sujet | Catégorie visée | État |
|-------|-----------------|------|
| Excentrique et descente en trail | TRA | extrapolation, voir S-REN-003 |
| Progression de charge d'un bloc à l'autre | CHA | **partiellement comblé le 22/09/2026** : S-BLE-004 (séance isolée), S-CHA-004, S-CHA-005, S-COU-013 (volume selon la phase) ; aucune source sur la progression de la **durée** en trail |
| Sorties longues consécutives : aucune étude contrôlée | TRA | convention de coachs uniquement (S-TRA-009), D-35 |
| Seuils d'alerte de charge aiguë / chronique | CHA | valeurs usuelles contestées |
| Adaptation du plan au sommeil et à la FC de repos | CHA | non documenté |
| Hydratation et sodium : aucune cible générique exploitable sans pesée avant/après | NUT | exclu du modèle, D-30 |
| Références primaires de S-COU-004 et S-TRA-001 | COU, TRA | citées sans vérification, à confirmer |
| Auteurs et référence complète de S-MES-002 | MES | à confirmer |
| Référence primaire de S-TRA-003 | TRA | **non retrouvée au 17/09/2026** — usage contextuel seulement |
| Aucune source sur la cadence optimale de semaine de relâche | CHA | convention de coaching uniquement |
| Aucune source sur le nombre d'affûtages tolérable par an, ni sur les durées de récupération post-course | COU | extrapolation assumée (D-25) |
| Aucune source sur la part optimale de la sortie longue dans le volume | TRA | extrapolation assumée |
| Auteurs exacts et statut de publication de S-TRA-006 | TRA | **retrouvés le 22/09/2026** — résumé, n = 1, niveau faible confirmé |
| Aucune source sur le taux de décroissance de la confiance d'une VC non rafraîchie | COU | extrapolation assumée |
