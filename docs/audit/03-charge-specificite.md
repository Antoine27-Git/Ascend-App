# Audit 03 — Charge totale (CrossFit + course) et spécificité trail

Audit du 11/11/2026, moteur v54. Aucune règle modifiée. Constats lus dans le code (`tests/engine.js`, `index.html`) et mesurés sur ton plan.

## Lectures retenues

- Tes séances de CrossFit : mardi et vendredi, en mode « libre » (tu choisis le contenu). Hypothèse de calcul quand il en faut une : **60 min à 7/10** (non mesuré : tu n'as presque pas de séances notées).
- « Charge » = durée × ressenti (S-CHA-001), seule mesure commune à la course et au CrossFit. C'est un ordre de grandeur, pas une vérité physiologique.

## 1. CrossFit : le moteur ne le voit pas

| Question du brief | Réponse mesurée |
|---|---|
| Le moteur tient-il compte de la fatigue du CrossFit pour **limiter** la sortie longue ? | **Non.** Deux séances de CrossFit notées 10/10 pendant 1 h 30 : 0 séance de course modifiée sur 94. Le moteur ne lit que les courses. |
| Pour la **placer** ? | Indirectement : la qualité va de préférence un jour de renforcement, jamais à moins de 2 jours de la sortie longue ; un renforcement à moins de 48 h de la sortie longue est annoncé « sans jambes lourdes ». Chez toi : vendredi → dimanche, 48 h, rien à signaler. |
| Que change le fait d'avoir 2 séances ? | 9 séances sur 94 : les sprints en côte de la phase F2 disparaissent (« ton renforcement prend le relais »). Rien d'autre. |
| Le texte « l'app la compte dans ta charge » est-il vrai ? | **Non.** Elle compte le jour, pas la charge. À corriger (P-18). |

Ce que la spec prévoyait et que le moteur v2 n'a pas : la grandeur **G-CHG-001** (charge hors course en durée × ressenti, « contamination » d'une course proche pendant 24 à 48 h, H-12). Écrite, jamais branchée.

**Pourquoi c'est important chez toi, en trois chiffres.**

1. **Tous tes mercredis sont un lendemain de CrossFit** : 16 séances de qualité sur 16 et 30 endurances sur 31. Or une séance de musculation dégrade la course qui suit (économie de course, temps de soutien, courbatures) pendant plusieurs heures à plusieurs jours selon la séance ; les auteurs de la revue ne donnent pas de délai fixe (Doma et coll., Sports Medicine 2017).
2. **Ton seul capteur de fatigue est posé à cet endroit** : le moteur ne lit le ressenti que sur l'endurance, donc le mercredi. Il mesure en partie ton WOD de la veille. Combiné au cas J de l'audit 02 (une note isolée gèle la sortie longue), un mardi de squats peut coûter une à deux semaines de progression.
3. **Le CrossFit pèse de 35 à 71 % de ta charge hebdomadaire** sous mon hypothèse (médiane 47 % ; 62 % en moyenne de novembre à mi-février). Le moteur pilote donc sur la moitié de ce que tes jambes encaissent. Sur 11 mois : 187 h de course prévues, environ 87 h de CrossFit.

**Ce n'est pas un procès du CrossFit.** Le renforcement améliore l'économie de course (S-REN-001, S-REN-006) ; son effet sur la tolérance à la descente reste une extrapolation (S-REN-003, aucune source directe). Le problème est de mesure et de placement, pas de principe. S-CHA-002 (6 h d'écart suffisent contre l'interférence aiguë) porte sur les adaptations, pas sur la fatigue résiduelle du lendemain.

**Je te challenge.** Tu refuses la course le même jour que le CrossFit (jambes entamées), mais tu cours tous les mercredis 24 h après. Deux options à tester sur 4 semaines, l'appli recommande, tu décides : (a) course le **jeudi** au lieu du mercredi (48 h après le mardi ; la course gêne moins le CrossFit du lendemain que l'inverse : selon les auteurs de la revue de 2017, dans le communiqué de leur université, une séance d'endurance ordinaire se récupère en 24 h, une séance de musculation parfois en plusieurs jours) ; (b) garder le mercredi mais faire du mardi la séance « haut du corps et gainage ».

## 2. Descente et charge excentrique : absente du plan

- **Aucune séance de descente.** Les 16 séances de qualité de ton plan sont toutes en montée (montée lestée, intervalles en côte, tempo en montée, montée spécifique). La descente n'apparaît que comme récupération (« redescente en marchant ») et dans une note (« travaille aussi la descente »). Le type « descente » existe dans l'appli, le moteur ne le prescrit jamais.
- **L'exposition vient seulement du D+ de la sortie longue** : densité de 149 m/h au départ à 298 m/h en bloc, soit 1 500 à 1 800 m sur les trois sorties clés ; 10 sorties à 1 000 m ou plus. La course en a 4 500 : ta plus grosse descente d'entraînement vaudra **40 %** de celle de la course, 7 semaines avant.
- **Le D− n'est pas une donnée du moteur.** Le champ existe à la saisie et à l'export ; il n'entre dans aucune règle. intervals.icu ne le fournit pas : il faut la trace ou une saisie.
- **Risque propre à la reprise** : la densité de D+ suit la durée, pas l'habitude. Après une coupure, la sortie longue repart à 1 h mais à la densité de la phase : rien ne ralentit le retour du dénivelé négatif, alors que les moins habitués à la descente sont ceux qui subissent le plus de dommages (S-TRA-012). Durée de la protection acquise : **non vérifié** (aucune valeur exploitable dans nos sources).
- **Sac lesté le mercredi** (« endurance musculaire, montée lestée 30 à 40 min ») : le lendemain du CrossFit, avec la consigne de vider l'eau en haut pour épargner la descente. Cohérent sur la descente, discutable sur l'enchaînement.

Nature : tout ce pan est **convention de coach** (GABARIT § 6) appuyée sur un mécanisme documenté (dommages excentriques, effet protecteur des expositions répétées). Aucune dose validée en ultra-trail.

## 3. Temps sur les jambes, enchaînements, ventre

| Sujet | Constat | Nature |
|---|---|---|
| Temps sur les jambes | Plus longue sortie 6 h pour une course estimée à 15 h (fourchette 12–18 h) : **33 à 50 %**. | Convention (H-06) ; cohérent avec les repères de coachs, pas une preuve |
| Enchaînements | À 2 jours stricts, **aucun** week-end de choc. Tu as dit être prêt à passer à 1 CrossFit en période spécifique pour courir mercredi + samedi + dimanche : simulé, 79 % de réussite contre 75 % à 25 % de semaines perturbées (audit 01), donc pas de pénalité. | Convention (S-TRA-009, niveau faible) |
| Nuit, bâtons, sac, matériel obligatoire | Rien dans le moteur ni dans les notes de séance. | Hors modèle ; à traiter en liste de contrôle du bloc |
| Entraînement du ventre | Progression de 6 g/h par sortie longue bien tolérée (confort ≥ 3/5), plafonds 60 g/h sous 2 h et 90 au-delà. Ne progresse que si tu **saisis** les glucides pris. De 35 à 90 g/h : 10 sorties nourries et bien tolérées. | S-NUT-002 pour le principe ; le pas de 6 g/h est une convention |

## 4. Nutrition : quatre seuils pour une même question

| Endroit | Ce qui est écrit ou codé |
|---|---|
| `nutriFor` (carte de séance) | carte dès **60 min** ; cible plafonnée à 60 g/h sous 2 h, 90 au-delà |
| Écran Suivi | « dès que tes sorties dépasseront **1 h 30** » |
| D-30 et GABARIT § 7 | au-delà d'environ **2 h** ; « en deçà l'apport à l'effort n'a pas d'objet » |
| Ligne affichée quand le module est éteint | dès **1 h** : **40 g/h** sous 1 h 30, **60 g/h** au-delà, boisson **500 ml/h** |
| Profil | point de départ 15, 35 ou 55 g/h ; boisson 400, 600 ou 800 ml/h |

Les incohérences du brief viennent de là : **35 g/h** est ton point de départ de progression (carte), **60 g/h** est une valeur fixe d'une ligne de repli écrite à part. Deux fonctions, deux logiques.

**Ce que dit la littérature** (position commune ACSM, diététiciens américains et canadiens, 2016) : rien de nécessaire sous 45 min ; de petites quantités ou un rinçage de bouche de 45 à 75 min ; 30 à 60 g/h de 1 h à 2 h 30 ; jusqu'à 90 g/h au-delà de 2 h 30 à 3 h. Pour l'ultra : S-NUT-001.

**Lecture.**
- La phrase de D-30 « en deçà de 2 h l'apport n'a pas d'objet » est **fausse** au regard de cette position (30 à 60 g/h dès 1 h). Elle confond deux questions : *quand manger sert la séance* (dès 1 h à 1 h 15) et *quand la séance sert à entraîner le ventre* (assez longue pour répéter les prises : convention).
- Le seuil de 60 min du code est donc défendable pour la première question, pas pour afficher une cible de progression sur une endurance facile de 1 h.
- **Hydratation** : D-30 l'exclut du modèle et S-NUT-003 dit qu'il n'y a pas de cible générique. L'appli affiche pourtant 500 ml/h en dur d'un côté, et ton réglage × la durée de l'autre.

**Proposition P-20** : une seule fonction, deux paliers, un seul endroit pour les chiffres (`CONV`).
- 60 à 90 min : ligne simple, « eau ; un apport léger si la séance est soutenue », sans cible ;
- à partir de **90 min** : carte complète avec la cible de progression (c'est ton propre principe du projet et le texte du Suivi ; entre le seuil physiologique et celui de D-30 : **convention**) ;
- la ligne de repli du module éteint ne porte plus de chiffre propre ;
- boisson : ton réglage, présenté comme repère personnel, jamais 500 ml/h en dur.

## 5. Propositions (brouillons, `docs/audit/propositions.md`)

| # | Proposition | Priorité |
|---|---|---|
| P-17 | Ressenti du lendemain de renforcement : noté à part, jamais seul déclencheur d'un gel (complète P-10) ; conseil de placement affiché, non imposé | **1** |
| P-18 | Texte honnête : « l'app compte le jour de renforcement, pas sa charge » | 1 (une ligne) |
| P-19 | Descente : cumul de D− des 30 jours affiché face au D− de la course ; option « répétitions de descente » en F3 et en bloc ; retour progressif du D+ après une coupure | 2 |
| P-20 | Nutrition : un seuil (90 min), une fonction, chiffres dans `CONV` ; corriger la phrase de D-30 | 2 |
| P-21 | Charge hors course : commencer par **enregistrer** (durée, ressenti, jambes au réveil du lendemain) ; ne brancher G-CHG-001 qu'après 8 semaines de données (audit 06) | 2 |
| P-22 | Bloc spécifique : proposer (pas imposer) le passage à 3 jours enchaînés ; liste de contrôle nuit, bâtons, sac | 3 |

## Sources

- Doma K., Deakin G. B., Bentley D. J., *Implications of impaired endurance performance following single bouts of resistance training: an alternate concurrent training perspective*, Sports Medicine 2017, 47(11) : 2187–2200. https://doi.org/10.1007/s40279-017-0758-3 — revue narrative ; vérifiée le 11/11/2026 (résumé et introduction). Niveau moyen : études transversales, délais variables.
- Thomas D. T., Erdman K. A., Burke L. M., *Nutrition and Athletic Performance*, position commune AND / DC / ACSM, Med Sci Sports Exerc 2016, 48(3). http://journals.lww.com/acsm-msse/Fulltext/2016/03000/Nutrition_and_Athletic_Performance.25.aspx — paliers lus dans des reprises du texte le 11/11/2026, texte original **non relu** : à vérifier avant d'entrer dans `SOURCES.md`.
- Déjà dans `docs/SOURCES.md` : S-CHA-001, S-CHA-002, S-REN-001, S-REN-003 (extrapolation), S-REN-006, S-NUT-001, S-NUT-002, S-NUT-003, S-TRA-009, S-TRA-012.
- Communiqué de l'université James Cook sur la revue de 2017 : https://www.sciencedaily.com/releases/2017/07/170726103003.htm
- Code : `nutriFor`, `nutriTarget` (`index.html`), bloc « qualité » et « renforcement » de `tests/engine.js`.
