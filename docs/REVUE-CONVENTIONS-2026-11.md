# Revue de cinq conventions du plan — 14/11/2026

Demandée par Antoine le 14/11/2026, selon la règle « chercher avant de proposer » (AGENTS.md).
Aucun code n'est modifié par ce document. Chaque proposition attend sa validation.

**Étiquettes.** **Étude** : résultat publié, avec son niveau. **Avis d'expert** : pratique de coach ou consensus, sans essai. **Non vérifié** : aucune source trouvée.

**Méthode.** Pour chaque point : ce que l'app fait aujourd'hui (lu dans `tests/engine.js`), ce que disent les sources, un verdict (confirmé, à ajuster, non vérifiable), une proposition. Les plans cités sont des simulations du moteur (v69) sur un profil proche de celui d'Antoine : 2 courses par semaine, puis mercredi + samedi + dimanche à partir de F3, 50 km / 1 900 m le 8 mai, 80 km / 5 000 m le 25 septembre. **À confirmer sur son vrai profil.**

## Synthèse

| # | Convention | Verdict | Ce qu'il faut retenir |
|---|---|---|---|
| 1 | Plafond de la sortie longue | **Non vérifiable**, valeurs gardées | Aucune étude ne fixe un plafond. Les études désignent le volume hebdomadaire, pas la sortie la plus longue. |
| 2 | Affûtage | Principe **confirmé**, application **à ajuster** | Les études sont solides. Mais le plan produit ne ressemble pas à ce qu'elles décrivent. |
| 3 | 3 semaines de charge, 1 allégée | **Non vérifiable**, gardé | Aucun essai en endurance. Rien ne montre que c'est nuisible. |
| 4 | Nutrition, +5 à 10 g/h par semaine | Principe **confirmé**, rythme **non vérifié** | Les études ne montent pas par paliers. Elles exposent souvent, sur des sorties d'1 h. |
| 5 | Règle des 30 jours en durée et en trail | **Confirmée** comme garde-fou, transposition **non vérifiée** | L'étude ne mesure ni la durée ni le dénivelé. Un coach de référence l'applique en heures. |

**Le constat le plus important ne figurait pas dans la liste.** En vérifiant les points 1 et 2 sur le plan réel, trois écarts apparaissent dans les 9 dernières semaines avant le 80 km. Ils sont décrits en fin de document (« Ce que la revue a fait apparaître »).

---

## 1. Le plafond de la sortie longue

**Ce que fait l'app.** 80 km (course de 8 à 20 h) : trois sorties clés de 5 h, 5 h 30 et 6 h. 50 km : sortie longue visée à 50 % de la durée estimée de la course, 4 h 30 au plus (H-44). Hors sorties clés : 3 h au plus.

**Ce que disent les sources.**
- **Étude** (observationnelle, 100 km route). Tanda et Knechtle 2015 : le volume hebdomadaire moyen et l'allure d'entraînement prédisent la performance. Sur 100 km, le volume pèse plus que l'allure.
- **Étude** (observationnelle, trail 50, 80 et 160 km). « Physiological Determinants of Ultramarathon Trail-Running Performance » : le volume d'entraînement n'est lié à la performance que sur le 50 km. Les non-finishers couraient moins par semaine que les finishers (51 contre 77 km).
- **Étude** (marathon, route). Fokkema 2020 : une plus longue sortie sous 25 km va avec un temps plus lent, sans lien avec les blessures. Doherty 2020 (méta-régression, 85 études) : la plus longue sortie fait partie des variables associées à un meilleur temps. Ce sont des associations, sur marathon.
- **Étude** (laboratoire, 10 coureurs non habitués). 30 min de descente à −20 % : la force du quadriceps met 4 jours à revenir. Le coût d'une longue sortie avec beaucoup de descente se compte donc en jours.
- **Avis d'expert.** Koop (CTS) : la plus longue sortie compte peu sur le plan physique, car une seule journée pèse peu dans le volume total. Ses athlètes qui réussissent ont fait de 20 à 80 % de la distance de course. La progression raisonnable passe avant la durée visée. Une ou deux sorties proches du maximum par mois, les autres à 50–75 %. Il juge peu étayée l'idée de rendements décroissants au-delà de 4 h. Au moins 4 h pour répéter la nutrition de course.
- **Avis d'expert.** Campus (programmes ultra) : sorties de 4 à 6 h en alternant course et marche ; week-ends de choc, repris de Guillaume Millet.
- **Non vérifié.** Aucune étude ne compare des plafonds entre eux, ni ne fixe une part de la durée de course. La Clinique du Coureur : rien trouvé sur ce point précis (recherche sans résultat exploitable).

**Verdict : non vérifiable. Valeurs gardées.** Nos valeurs sont dans la fourchette de pratique : 5 à 6 h pour une course estimée à 16 h 20, soit 31 à 37 % ; 4 h 35 pour 8 h 15, soit 55 %.

**Proposition.**
1. Garder 5–6 h et 50 % / 4 h 30.
2. Requalifier H-44 et la cible 5–6 h : « avis d'expert, dans la fourchette 20–80 % observée par Koop ; aucune étude ».
3. Corriger le texte de l'app (« habitude d'entraîneur » → « pas d'étude sur ce point ; fourchette de pratique »).
4. Déplacer l'attention : ce que les études désignent, c'est le volume hebdomadaire. Voir l'écart n° 1 en fin de document.

---

## 2. L'affûtage

**Ce que fait l'app.** Course de 8 à 20 h (le 80 km, et le 50 km estimé à 8 h 15) : 3 semaines, coefficients 0,70 / 0,55 / 0,40. Course de 4 à 8 h : 2 semaines, 0,65 / 0,45. L'intensité et le nombre de séances sont maintenus. Le D+ par heure reste celui de la course.

**Ce que disent les sources.**
- **Étude** (méta-analyse, 27 études). Bosquet 2007 : baisser le volume de 41 à 60 % sur environ 2 semaines, en gardant intensité et fréquence, donne le meilleur gain (S-COU-006).
- **Étude** (méta-analyse, 14 études, contre-la-montre de 800 m à 40 km). Wang 2023 : gain significatif avec une baisse de 41 à 60 %, intensité et fréquence maintenues, sur 7 jours ou moins, 8 à 14 jours ou 15 à 21 jours. Conclusion des auteurs : 21 jours au plus, baisse progressive.
- **Étude** (observationnelle, 158 117 marathoniens amateurs). Smyth et Lawlor 2021 : un affûtage strict, où le volume baisse chaque semaine, jusqu'à 3 semaines, va avec de meilleurs temps.
- **Avis d'expert.** Koop : 2 à 3 semaines ; volume à 40–50 % la première semaine, 20–30 % la deuxième, moins de 20 % la dernière ; même terrain et même dénivelé que la course ; gain attendu de 1,5 à 3 %. Il précise qu'un affûtage raisonnable suffit.
- **Non vérifié.** Aucune de ces études ne porte sur l'ultra ni sur le trail.

**Verdict : principe confirmé, application à ajuster.** La durée (2 à 3 semaines), l'intensité, la fréquence et le terrain sont conformes. Mais la baisse de volume n'est pas celle des études quand on regarde le plan produit :

| Semaine avant le 80 km | Volume | Sortie longue |
|---|---|---|
| Pic, S−4 | 5 h 20 | 3 h |
| Affûtage, S−3 | 4 h 50 | 3 h 20 |
| Affûtage, S−2 | 4 h 30 | 3 h 20, 6 jours avant la course |
| Semaine de course | 40 min + course | — |

- La baisse est de 10 % puis 15 % par rapport à la dernière semaine de pic, pas de 41 à 60 %. Les coefficients s'appliquent à un volume théorique, pas à ce que le coureur faisait juste avant.
- La sortie longue **monte** pendant l'affûtage (3 h → 3 h 20).
- Une sortie de 3 h 20 et 1 000 m de D+ tombe 6 jours avant le 80 km. Avant le 50 km : 2 h 30 et 650 m, 6 jours avant. Koop limite la dernière semaine à 2 h au total.

**Proposition (à valider, puis spec).**
1. Calculer la baisse par rapport au volume réel moyen des 3 semaines précédentes, pour viser −41 à −60 % sur l'ensemble de l'affûtage. **Étude.**
2. Interdire à la sortie longue de monter pendant l'affûtage. **Étude** (baisse progressive).
3. Raccourcir la dernière sortie longue, à moins de 7 jours de la course. La valeur exacte est **non vérifiée** : je proposerai une valeur prudente dans la spec, étiquetée comme telle.

---

## 3. Trois semaines de charge, une semaine allégée

**Ce que fait l'app.** Une semaine allégée toutes les 4 semaines, placée à rebours depuis l'affûtage (D-57b, D-63f), à environ 60–65 % du volume. S'y ajoute une semaine allégée à la demande quand le ressenti se dégrade.

**Ce que disent les sources.**
- **Non vérifié.** Je n'ai trouvé aucun essai comparant 3:1 à 2:1, 4:1 ou à l'absence de semaine allégée en endurance.
- **Avis d'expert** (musculation). Consensus Delphi de Bell 2023 : pratique jugée universelle mais peu étudiée ; en général toutes les 4 à 6 semaines, pendant environ 7 jours.
- **Étude** (essai randomisé, musculation, 39 sujets, 9 semaines, PMID 38274324). Une semaine d'arrêt au milieu du programme n'apporte rien et pénalise un peu la force. C'est un arrêt complet, dans un autre sport : transposition faible.
- **Étude** (essai croisé, 20 skieurs de fond juniors). Walther 2026 : une semaine à 160 % suivie de semaines réduites ne fait pas mieux que le même volume réparti également, et dégrade l'humeur et la récupération perçue. Pour le volume à basse intensité, la régularité vaut la concentration.
- **Étude** (deux méta-analyses, 2021). Adapter la charge à l'état du jour, mesuré par la variabilité cardiaque, donne un avantage faible et non significatif sur la performance, avec moins de non-répondeurs. C'est un appui modeste pour la semaine allégée « à la demande ».

**Verdict : non vérifiable. Gardé.** Le 3:1 est une tradition de planification. Rien ne montre qu'il aide, rien ne montre qu'il nuit. La partie la mieux étayée de notre dispositif est celle qui réagit au ressenti.

**Proposition.**
1. Garder la grille et la semaine à la demande.
2. Requalifier H-10 : « tradition, aucun essai en endurance ».
3. Ne pas ajouter de complexité ici. Le sujet d'Antoine est la régularité, pas la cadence des semaines allégées. Un effet favorable des semaines allégées sur l'assiduité est plausible mais **non vérifié**.

---

## 4. La progression de la nutrition en course

**Ce que fait l'app.** Départ à 35 g de glucides par heure. +6 g/h par semaine où une sortie de 1 h 30 ou plus a été nourrie et bien digérée. Progression gelée si la digestion a été mauvaise. Visée de 60 à 90 g/h. L'hypothèse H-11 parle de 5 à 10 g/h par semaine.

**Ce que disent les sources.**
- **Étude** (essai randomisé, 25 coureurs). Costa 2017 : 2 semaines de sorties d'1 h avec 90 g/h. Les symptômes digestifs baissent d'environ 60 % et la performance s'améliore face au placebo.
- **Étude** (essai randomisé, 18 coureurs). Miall 2018 : même protocole, 90 g/h contre placebo. Moins d'inconfort et moins de malabsorption.
- **Étude** (revue systématique, 8 études). Martinez 2023 : l'inconfort baisse de 47 % en moyenne après 2 semaines ; la malabsorption baisse dans 2 études sur 3 ; les résultats sur les symptômes sont flous dans 4 études sur 6. Les auteurs demandent de meilleures mesures avant d'affiner les protocoles.
- **Étude** (athlètes très entraînés). King 2022 : effets mineurs sur le confort digestif et la performance.
- **Non vérifié.** Aucune étude ne teste une montée par paliers hebdomadaires. Les protocoles donnent d'emblée 90 g/h, une dizaine de fois en 2 semaines.

**Verdict : principe confirmé, rythme non vérifié.** Le ventre s'entraîne : niveau de preuve modéré, petits effectifs. Le « +5 à 10 g/h par semaine » est une traduction pratique, pas un résultat. Deux écarts avec les études :
- **La fréquence.** Les études exposent le ventre presque chaque jour. L'app ne le fait que sur les sorties de 1 h 30 ou plus, soit une fois par semaine pour Antoine.
- **La durée des séances.** Les études utilisent des sorties d'1 h. Notre seuil de 1 h 30 les exclut.

**Proposition (à valider).**
1. Garder la montée progressive : elle est prudente et une erreur coûte peu. L'étiqueter « non vérifié ».
2. Ajouter une exposition sur la deuxième course de la semaine dès 1 h, pendant les 8 à 10 semaines qui précèdent chaque course. C'est une séance d'entraînement du ventre, distincte du besoin énergétique. Cela ne contredit pas la règle « pas de glucides conseillés sous 1 h 15 » de l'analyse de séance, qui parle de besoin et non d'entraînement digestif. La dose reste à fixer dans la spec.
3. Aligner H-11 et le code (6 g/h) sur une seule formulation.

---

## 5. La règle des 30 jours, en durée et en trail

**Ce que fait l'app.** La séance de progression ne dépasse pas de plus de 10 % la plus longue des 30 jours précédents, en durée (D-63c), avec l'arrondi aux 5 minutes supérieures (D-96) et une mémoire au-delà de 30 jours (D-94).

**Ce que disent les sources.**
- **Étude** (cohorte, 5 205 coureurs, 18 mois). Frandsen 2025 : dépasser de plus de 10 % la plus longue sortie des 30 jours augmente le taux de blessure de surmenage : rapport de 1,64 pour +10 à 30 %, 1,52 pour +30 à 100 %, 2,28 au-delà. La variation d'une semaine à l'autre n'est pas associée au risque.
- **Limites dites par les auteurs.** Étude exploratoire. Blessures déclarées par les coureurs. Mesure en **distance**. Dénivelé, surface, montée et descente non pris en compte. Population surtout masculine, 46 ans en moyenne. Le risque ne croît pas régulièrement (1,64 puis 1,52) : le seuil de 10 % est une frontière de catégorie, pas un seuil démontré.
- **Avis d'expert.** CTS (Pittman) applique cette règle à la sortie longue **en heures**, sur un mois. Koop accepte des hausses plus fortes pour la sortie longue (+20 %, +20 %, +10 %, puis moins) : notre règle est du côté prudent de la pratique.
- **Non vérifié.** Aucune étude ne teste la règle en durée, ni en trail. Texte intégral de Frandsen non relu cette nuit (page bloquée) : chiffres repris du résumé officiel et d'une synthèse détaillée, cohérents avec SOURCES.md (S-BLE-004). Intervalles de confiance non revérifiés.

**Verdict : confirmée comme garde-fou. Transposition non vérifiée, mais cohérente avec la pratique.**

**Point de vigilance.** La règle ne voit que la durée. En trail, à durée égale, plus de descente charge davantage les muscles. Vérification par simulation, après la D-102 : hors week-ends de choc, le D+ d'une sortie ne dépasse jamais de plus de 20 % le plus gros D+ des 30 jours. Le D+ suit donc la durée, sans saut propre.

**L'élément le moins étayé est le week-end de choc.** 2 h 50 + 4 h 10 et 1 750 m en deux jours, quand la plus longue sortie du mois est de 4 h 10. Les auteurs de Frandsen signalent eux-mêmes que des hausses enchaînées restent risquées. L'idée que découper la charge sur deux jours limite le risque vient de coachs (Millet, Campus) : **avis d'expert**, pas d'étude.

**Proposition.**
1. Garder la règle telle quelle.
2. Écrire dans H-21 : « en durée : avis d'expert (CTS) ; en trail : non vérifié ».
3. Ajouter un test automatique : hors week-end de choc, le D+ d'une sortie ne dépasse pas de plus de 20 % le plus gros des 30 jours. C'est un contrôle, pas une règle nouvelle.
4. Revoir H-42 (week-end de choc) dans une prochaine passe, avec la même méthode.

---

## Ce que la revue a fait apparaître

Trois écarts, mesurés sur les plans simulés (profil à 4 jours et profil à 3 jours enchaînés). Ils comptent plus que les cinq conventions.

**Écart n° 1 — La dernière grosse sortie est à 7 semaines de la course.** Les trois sorties clés (5 h, 5 h 30, 6 h) sont placées dans les 5 premières semaines du bloc spécifique. Ensuite, la sortie longue retombe à 3 h jusqu'à la course. Le gabarit dit pourtant que le pic porte « les plus hautes charges spécifiques ». Les méta-analyses situent l'affûtage utile à 21 jours au plus.

**Écart n° 2 — Le volume des 9 dernières semaines est bas.** Repère de Koop (**avis d'expert**) pour un 100 km ou plus : pouvoir tenir 9 h par semaine pendant 6 semaines, à partir de 9 semaines avant la course. Plan simulé d'Antoine sur ces 6 semaines : 10 h, 4 h 50, 10 h 30, 4 h 05, 4 h 40, 5 h, soit 6 h 30 en moyenne, et 5 h environ sur les 5 dernières semaines avant l'affûtage. Avec 4 jours de course : 8 h 10 en moyenne. Cause : trois jours de course, des endurances limitées à 1 h 30, une sortie longue limitée à 3 h hors sorties clés.

**Écart n° 3 — L'affûtage ne baisse presque pas** (point 2).

**Question pour Antoine.** Les études désignent le volume et la régularité, pas la sortie la plus longue. Avec trois jours de course en période spécifique, le plan plafonne vers 5 h par semaine hors week-ends clés. Deux leviers possibles, à discuter : un quatrième jour de course pendant les 9 dernières semaines, ou des sorties longues « moyennes » au-delà de 3 h. Lequel est réaliste dans ton agenda ?

**Ordre proposé.** (a) Spec « fin de préparation » : placement des sorties clés, volume des 9 dernières semaines, affûtage (écarts 1 à 3). (b) Spec « entraînement du ventre » (point 4). (c) Requalification des hypothèses H-10, H-11, H-21, H-44 et textes de l'app (points 1, 3, 5). (d) Revue du week-end de choc (H-42).

---

## Sources

À reporter dans `docs/SOURCES.md` après validation.

1. Tanda G., Knechtle B. Effects of training and anthropometric factors on marathon and 100 km ultramarathon race performance. Open Access J Sports Med, 2015. PMC4425319.
2. Physiological Determinants of Ultramarathon Trail-Running Performance. Int J Sports Physiol Perform. https://www.scienceofultra.com/s/Physiological-Determinants-of-Ultramarathon-Trail-Running-Performance.pdf
3. Fokkema T. et coll. Training for a (half-)marathon: training volume and longest endurance run related to performance and running injuries. Scand J Med Sci Sports, 2020. DOI 10.1111/sms.13725.
4. Doherty C. et coll. An evaluation of the training determinants of marathon performance: a meta-analysis with meta-regression. J Sci Med Sport, 2020. PMID 31704026.
5. Downhill running increases markers of muscle damage… Eur J Appl Physiol, 2024. DOI 10.1007/s00421-023-05412-z.
6. Koop J. How Long Should Your Longest Run Be Before An Ultramarathon? https://trainright.com/longest-run-ultramarathon-training/
7. Koop J. Ultramarathon training time required. https://trainright.com/ultramarathon-training-time-required/
8. Campus. Préparation ultra-trail : conseils ; week-end choc. https://www.campus.coach/blog/preparation-ultra-trail-conseils ; https://www.campus.coach/blog/week-end-choc-trail-long
9. Bosquet L. et coll. Effects of tapering on performance: a meta-analysis. Med Sci Sports Exerc, 2007 (S-COU-006).
10. Wang Z. et coll. Effects of tapering on performance in endurance athletes. PLOS ONE, 2023. PMID 37163550.
11. Smyth B., Lawlor A. Longer disciplined tapers improve marathon performance for recreational runners. Front Sports Act Living, 2021. PMC8506252.
12. Koop J. Tapering for ultrarunning. https://trainright.com/tapering-ultrarunning-prevent-taper-tantrum
13. Bell L. et coll. Integrating deloading into strength and physique sports training programmes: an international Delphi consensus approach. Sports Med Open, 2023. PMC10511399.
14. Essai randomisé sur une semaine d'arrêt en musculation, 2024. PMID 38274324.
15. Walther J. et coll. No additional effects of block- compared to even-periodization of low-intensity training in junior cross-country skiers. Int J Sports Physiol Perform, 2026. PMID 42177035.
16. Düking P. et coll. Monitoring and adapting endurance training on the basis of heart rate variability… J Sci Med Sport, 2021. PMID 34489178. Manresa-Rocamora A. et coll., Int J Environ Res Public Health, 2021. PMC8507742.
17. Costa R.J.S. et coll. Gut-training: the impact of two weeks repetitive gut-challenge during exercise… 2017. Miall A. et coll. Two weeks of repetitive gut-challenge reduce exercise-associated gastrointestinal symptoms and malabsorption. Scand J Med Sci Sports, 2018. DOI 10.1111/sms.12912.
18. Martinez I.G. et coll. The effect of gut-training and feeding-challenge on markers of gastrointestinal status… Sports Med, 2023. PMC10185635.
19. King A.J. et coll. Short-term very high carbohydrate diet and gut-training have minor effects… Nutrients, 2022. PMC9105618.
20. Frandsen J.S.B. et coll. How much running is too much? Br J Sports Med, 2025. PMC12421110. Synthèse lue : https://www.physiotutors.com/?p=26053
21. Pittman C. (CTS). The 10% running rule reframed. https://trainright.com/10-running-rule-reframed/

**Non consulté.** Texte intégral de Frandsen 2025, de Wang 2023 et de Martinez 2023 (pages bloquées ou autorisation requise en l'absence d'Antoine) : résumés officiels utilisés. Programmes de La Clinique du Coureur : rien d'exploitable trouvé.
