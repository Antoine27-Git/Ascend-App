# Audit 05 — Littérature : classement des hypothèses, dose minimale, adhérence, mental

Audit du 11/11/2026. Aucune règle modifiée. Paraphrases, pas de citations longues.

## Lectures retenues

- **Trois classes**, plus deux cas à part :
  - **science** : un résultat publié porte directement sur la règle, dans une population proche ;
  - **extrapolation** : un résultat publié existe, mais dans une autre population, une autre grandeur ou une autre durée ;
  - **convention** : pratique de coach ou choix de conception, sans résultat publié ;
  - *mesure* : observation faite sur ton matériel ; *introuvable* : texte absent de `docs/`.
- Une source n'est citée que si elle est déjà dans `docs/SOURCES.md` ou si je l'ai relue pendant cet audit (date et lien en fin de rapport). Le reste est écrit **non vérifié**.
- « Appui » = ce qui soutient la règle. « Mis à l'épreuve » = ce que les audits 01 à 04 ont mesuré dessus.

## 1. Bilan en une ligne

Sur 58 hypothèses numérotées : **0 science directe**, **10 extrapolations** d'un résultat publié (H-04, H-07, H-08, H-12, H-14, H-17, H-21, H-22, H-28, H-34), **1 mesure** (H-51), **2 introuvables** (H-38, H-39), **45 conventions**. Le moteur est un plan de coach écrit en code, tenu par **un** résultat solide (la règle des 30 jours) lui-même extrapolé (distance sur route → durée en trail). Ce n'est pas un reproche : c'est l'état du savoir en ultra-trail. C'est une raison de plus pour afficher des fourchettes.

## 2. Classement

### Hypothèses qui portent le moteur v2

| H | Sujet | Classe | Appui | Mis à l'épreuve par l'audit |
|---|---|---|---|---|
| H-21 | Règle des 30 jours, en durée, en trail ; 30 min toujours permises | **extrapolation** | S-BLE-004 (5 205 coureurs, 18 mois ; distance, route, blessures déclarées) | 0 violation sur 26 492 sorties longues hors heure d'été ; 2 % des sorties longues prescrites restent au-delà de +30 % du réel (plancher, mémoire, déclaratif) |
| H-28 | Une seule séance de progression par semaine | extrapolation | limite citée par les auteurs de S-BLE-004 (hausses enchaînées) | non testé |
| H-58 | Arrondi supérieur sans risque notable | **convention sans appui** | aucun ; S-BLE-004 classe +10 à +30 % à HR 1,64 et ses auteurs voient déjà un risque entre 1 et 10 % | 10,4 % des sorties longues prescrites dans la catégorie (0,8 % sans D-96) ; chez toi 6 sur 44, +11,8 % au plus ; +9 à +14 points de réussite |
| H-40, H-48 | Mémoire de reprise : −1 %/jour, pas plus d'1 h ; sortie déclarée à sa date | convention | sens général de S-COU-005 (désentraînement en semaines) | le plafond d'1 h est le premier coût d'une coupure (75 → 97 % sans lui) mais le lever contredit S-BLE-004 ; la fréquence déclarée n'est pas couverte (cas H) |
| H-26 | Rampe « juste à temps », marge de 3 semaines | convention | aucun ; contraire à la base d'Uphill Athlete (GABARIT, écart n° 6) | sans jalon : 71 % à 25 % de semaines perturbées ; marge de 10 semaines : 86 % ; le moteur laisse la sortie longue à 1 h 15 pendant 3 mois |
| H-27 | Alternance au-delà de 3 h ; parts de sortie longue | convention | pratique de coach | l'alternance est le mécanisme de l'effondrement : deux sorties au niveau perdues de suite vident la fenêtre |
| H-06, H-44 | Sorties clés de 5 à 6 h ; cible d'un secondaire à 50 % | convention | S-TRA-008 (concept, niveau faible) | c'est la définition même du « succès » de l'audit 01 : à lire en fourchette |
| H-46, H-47 | Fatigue lue sur le ressenti des endurances ; gel de 1 à 2 semaines | convention | S-CHA-001 (durée × ressenti comme mesure de charge) | à 2 jours : une note par semaine, 24 h après le CrossFit ; bruit de ± 1 point : 100 → 67 % ; reproductibilité publiée du ressenti de séance : écarts de l'ordre de 28 à 32 % d'un essai à l'autre |
| H-38 | Échelle ressenti → dérive (0,12 par point) | **introuvable** | — | c'est le coefficient qui transforme un « 4 » en gel |
| H-39 | (cité dans le moteur) | introuvable | — | — |
| H-37 | Le coût de la sortie longue et du D+ « se lit dans le ressenti » | convention | aucun | contredit par H-46 (le ressenti de la sortie longue n'est pas lu) et par l'audit 03 (CrossFit non vu) |
| H-49 | Manque sans réponse = empêchement | convention | — | cohérent avec ton cas (obstacle : le temps) |
| H-22, H-08 | Affûtage 65/45 et 70/55/40 ; budget de 20 % | **extrapolation** | S-COU-006 (volume −41 à −60 % sur 2 semaines ; hors ultra) | à 2 jours le volume ne baisse pas (4 h 30, 4 h 35, 4 h 20), 3 h 20 à J−6 : la règle codée ne produit pas ce que sa source décrit |
| H-23, H-33 | Reprise : max(65 % ; 1 − 0,07 × (n − 1)) | convention | sens de S-COU-005 | pas de mode reprise après maladie (cas M) |
| H-10, H-25 | Semaine allégée toutes les 4, à rebours | convention | aucun essai comparatif retrouvé (**non vérifié**) | une semaine allégée de plus = une sortie au niveau de moins dans la fenêtre |
| H-36, H-41 | D+ : monte en fond, densité de départ ≤ moitié de la course | convention | mécanisme de S-TRA-012 | aucune descente prescrite ; plus grosse descente = 40 % de la course |
| H-42 | Samedi d'un week-end de choc ≤ 2/3 | convention | S-TRA-009 (niveau faible) | jamais posé à 2 jours |
| H-43 | Récupération 35/55/75 % ; allégée à 65 % ; « moyenne » ≤ 3 h | convention | — | — |
| H-45 | Écart signalé sous 90 % | convention | — | 4 h 35 pour 5 h : silence (cas C) |
| H-52 | Fourchette de durée estimée | convention | formule de type Riegel, extrapolation ×7 | seuil net à 8 h sur cette estimation (cas G) |
| H-34 | Départ en marche-course | extrapolation | S-BLE-005 (débutants, essai GRONORUN) | non testé |
| H-07 | Répartition des intensités transposée à l'ultra | extrapolation | S-COU-008, S-COU-009 (jusqu'au marathon) | non testé |
| H-05, H-13, H-24 | Blocs par tranche de durée ; renforcement par phase ; consolidation | convention | GABARIT (Uphill Athlete, Koop) | — |
| H-29, H-30, H-35 | Ressenti en semaine allégée ; coureur qui ne note pas ; ressenti bruité | convention | — | le garde-fou « ressenti bruité » (H-35) existe mais n'empêche pas le cas J |
| H-09 | Facteur trail/route 1,2 à 1,4 | convention | S-TRA-011 | — |
| H-11 | Glucides : +5 à 10 g/h par semaine | convention | traduction pratique de S-NUT-002 | codé à +6 g/h par sortie tolérée |
| H-12 | Charge hors course : fenêtre de 24 à 48 h | extrapolation | Doma 2017 : de quelques heures à plusieurs jours, sans délai fixe | spec non branchée (audit 03) |

### Hypothèses d'affichage, de produit ou hors moteur v2

| H | Sujet | Classe |
|---|---|---|
| H-01 à H-04 | Modèle allure-effort (segments, effort par pente, stabilité, coût-pente) | extrapolation (H-04) et convention ; **hors moteur v2**, à reclasser quand le chantier reprend |
| H-14 | Seuil de marche à 25–30 % de pente | extrapolation (ordre de grandeur : S-COU-011 ; borne : convention) |
| H-15, H-18, H-19 | Plancher à 85 % ; seuils 1,5× et 2,5× ; périodes d'observation | convention |
| H-16, H-20, H-31, H-32 | Hiérarchie des contraintes ; questions terrain ; seuils d'alerte de saisie | convention de produit |
| H-17 | Modèle de douleur étendu à toute gêne | extrapolation (S-BLE-001, tendinopathie) |
| H-50 | Fourchette de D+ ± 10 % | convention (au-dessus de la précision d'un altimètre) |
| H-51 | Fenêtre d'envoi Garmin d'environ 7 jours | **mesure** (15/10/2026, Fenix 7) |
| H-53 à H-57 | Verdicts et messages du Suivi | convention d'affichage |

## 3. Contradictions à trancher

1. **H-58 contre S-BLE-004.** La seule preuve du projet range les sorties arrondies dans une catégorie à risque plus élevé. Le dépassement est petit chez toi. À assumer par écrit (« pari ») ou à borner (par exemple +12 % au plus).
2. **H-22 contre S-COU-006, dans les faits.** Les coefficients d'affûtage portent sur le niveau de la sortie clé, pas sur le volume récent : à 2 jours, rien ne baisse.
3. **D-30 contre la position d'experts de 2016** sur les glucides (audit 03).
4. **H-37 contre H-46 et l'audit 03.** « Le coût se lit dans le ressenti », mais le moteur ne lit qu'une note par semaine, pas celle de la sortie longue, et ne voit pas le CrossFit.
5. **H-46 contre la reproductibilité du ressenti.** Deux essais identiques donnent des notes qui diffèrent de l'ordre de 30 % : à 3/10, c'est ± 1 point. Le moteur réagit à 1 point.
6. **H-26 contre ta réalité et contre le gabarit.** « Juste à temps » suppose un coureur régulier. Tu ne l'es pas encore.

## 4. Dose minimale avec peu de séances

- **Maintenir** : une revue de 2021 conclut que l'endurance se maintient jusqu'à 15 semaines avec seulement 2 séances par semaine, ou un volume réduit d'un à deux tiers, **à condition de garder l'intensité** ; l'intensité est la variable qui protège. Limites dites par les auteurs : population générale surtout, peu de données chez les sportifs, et l'endurance de longue durée résiste moins bien à une coupe des deux tiers.
- **Progresser vers un ultra avec 2 sorties** : aucune étude retrouvée (**non vérifié**). Repères descriptifs : les finishers d'ultras de montagne déclarent 8,3 ± 4,0 h par semaine (S-TRA-002) ; ton plan fait 4,1 h de course en moyenne (187 h en 46 semaines), 7 h 30 au pic, plus environ 2 h de CrossFit. Tu es dans le bas de la fourchette observée, pas en dehors.
- **Risque** : chez des marathoniens, moins de 30 km par semaine avant la course allait avec plus de blessures qu'entre 30 et 60 km (Rasmussen 2013 ; marathon sur route, extrapolation pour toi).
- **Conséquence pour l'appli.** Ton budget de 2 sorties suffit à *maintenir* et la sortie longue fait le travail de *progression* : c'est donc elle qu'il faut protéger (audit 01, +19 à +45 points). Le repli court avec un passage soutenu est cohérent avec la revue (l'intensité protège), pour le maintien seulement.

## 5. Adhérence à un plan

Ce que les sources relues disent, sans le gonfler :

- **Intentions « quand, où, quoi »** : sur l'activité physique, une méta-analyse de 2013 trouve un effet **petit à moyen**, qui s'atténue au suivi. Utile, pas magique.
- **Habitude** : dans l'étude de référence (2010), l'automatisme a pris 66 jours en médiane, de 18 à 254 selon les personnes ; **manquer une occasion n'a pas compromis la formation de l'habitude**. Une séance manquée n'est donc pas un échec à signaler.
- **Autosuivi, plans de secours (« si… alors »), effet des séries à ne pas rompre** : **non vérifié** dans cet audit. À ne pas présenter comme prouvé.

Traduction en règles d'appli (conventions, à valider) :

| Idée | Forme proposée | Ce qu'il ne faut pas faire |
|---|---|---|
| « Quand, où, quoi » | Le dimanche soir ou le lundi, l'appli demande **quel jour et à quelle heure** tu feras la sortie longue de la semaine (une question, une réponse), et l'envoie à la montre ce jour-là | une notification par séance |
| Plan de secours | Avec la réponse : « et si ça saute ? » → un second créneau, ou le repli (P-03) | déplacer la séance sans toi |
| Manque neutre | Une séance manquée se range sans commentaire ; seul compte le niveau porté par la fenêtre (P-05) | compteur de séries, badge perdu, rouge |
| Semaine chargée | P-02 : déclarée d'avance, elle n'est pas un échec | compter les manques d'une semaine annoncée chargée |
| Sens | Le verdict du Suivi parle du **niveau** (« ta plus longue sortie du mois : 2 h 10 ») avant de parler d'écart | un pourcentage d'adhérence affiché en tête |

Ton cas : ton obstacle déclaré est le temps, pas l'envie. La littérature sur la motivation t'aidera moins qu'une décision d'agenda. La question utile n'est pas « comment me motiver » mais « quel créneau de 2 à 5 h le week-end est protégé, 4 semaines sur 5 ».

## 6. Mental de course (pour plus tard, en bloc spécifique)

- Une revue systématique de 2015 trouve un appui constant pour trois techniques : **imagerie, discours interne, fixation de buts** ; elle montre aussi que la **fatigue mentale** dégrade la performance d'endurance. Limites : épreuves surtout courtes et en laboratoire ; l'ultra-trail y est peu représenté (**transposition = extrapolation**).
- Ton idée (le plan écrit d'avance contre l'intuition du moment, d'après Kahneman) est une bonne image de ces techniques ; ce n'est pas une preuve.
- Proposition, hors moteur : à 8 semaines de la course, trois fiches courtes dans l'appli (un but de processus par tronçon ; deux phrases prêtes pour les passages durs ; un plan « si… alors » pour les trois pannes probables : ventre, descente, nuit), à répéter pendant les sorties clés. Semaine de course : éviter la surcharge mentale la veille. Convention, appuyée sur la revue.

## 7. Proposition ajoutée (brouillon)

**P-30 — Rampe robuste (révise H-26)** : monter tôt jusqu'à un plateau de 3 h (sortie hebdomadaire, sans alternance : la fenêtre des 30 jours est alors tenue par 4 sorties), l'entretenir, puis monter vers les sorties clés avec une marge qui dépend des sorties longues tenues (3 semaines si ≥ 90 %, 6 si environ 80 %, 10 en dessous). Chiffrage partiel disponible : sans jalon, marge de 10 semaines = 86 % contre 71 % (25 % de semaines perturbées), 46 % contre 31 % (40 %). Le plateau à 3 h n'a pas été simulé : à faire avant toute décision.

## Sources relues pendant l'audit (10–11/11/2026)

- Frandsen J. S. B. et coll., *How much running is too much? Identifying high-risk running sessions in a 5200-person cohort study*, BJSM 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12421110 ; billet des auteurs : https://blogs.bmj.com/bjsm/?p=11751
- Spiering B. A., Mujika I., Sharp M. A., Foulis S. A., *Maintaining physical performance: the minimal dose of exercise needed to preserve endurance and strength over time*, J Strength Cond Res 2021, 35(5). Résumé lu ; lien direct **à compléter** avant d'entrer dans `SOURCES.md`.
- Bélanger-Gravel A., Godin G., Amireault S., *A meta-analytic review of the effect of implementation intentions on physical activity*, Health Psychology Review 2013, 7(1). Résumé lu ; lien direct à compléter.
- Lally P. et coll., *How are habits formed: modelling habit formation in the real world*, European Journal of Social Psychology 2010, 40(6). Résumé lu ; lien direct à compléter.
- Rasmussen C. H. et coll., *Weekly running volume and risk of running-related injuries among marathon runners*, Int J Sports Phys Ther 2013, 8(2). Résumé lu ; lien direct à compléter.
- Doma K., Deakin G. B., Bentley D. J., Sports Medicine 2017. https://doi.org/10.1007/s40279-017-0758-3
- McCormick A., Meijen C., Marcora S., *Psychological determinants of whole-body endurance performance*, Sports Medicine 2015, 45(7) : 997–1015. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4473096/
- Reproductibilité du ressenti de séance : Wallace L. K. et coll., *Establishing the criterion validity and reliability of common methods for quantifying training load*, J Strength Cond Res 2014 (écart de 28,1 % entre essais, sportifs de loisir) ; Scott T. J. et coll., J Strength Cond Res 2013, 27(1) : 270–276 (31,9 %, course intermittente). Résumés lus ; à l'inverse, Herman et coll. 2006 trouvent une bonne concordance sur des paliers continus (r = 0,88) : https://journals.assaf.org.za/sajsm/article/view/247/185
- Déjà dans `docs/SOURCES.md` : S-BLE-001, S-BLE-004, S-BLE-005, S-CHA-001, S-COU-005, S-COU-006, S-COU-008, S-COU-009, S-COU-011, S-NUT-002, S-TRA-002, S-TRA-008, S-TRA-009, S-TRA-011, S-TRA-012.

Règle d'entrée de `SOURCES.md` respectée : rien de ce rapport n'y est ajouté tant que le texte original n'a pas été relu et le lien vérifié.
