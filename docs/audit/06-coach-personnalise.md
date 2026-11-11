# Audit 06 — Note de décision : coach personnalisé

Note du 11/11/2026. Aucun code. Elle demande quatre décisions (§ 7).

## Lectures retenues

- « Personnaliser » = **régler quelques paramètres du moteur sur tes données**, sous des garde-fous qui ne bougent pas. Pas un plan écrit par une IA.
- Tu as très peu de données (une sortie depuis la reprise). La note part donc de ce qu'il faut **enregistrer maintenant** pour pouvoir, plus tard, réfuter une hypothèse.
- D-77 (15/10/2026) : seules les activités sont lues ; sommeil, variabilité cardiaque et poids ne transitent pas par l'appli. Le brief demande de la rouvrir ou non, explicitement.

## 1. Le constat qui cadre tout : ton débit de données

Avec 2 sorties par semaine, tu produis **une** note d'endurance et **une** sortie longue par semaine. Pour distinguer deux réglages qui diffèrent d'un point de ressenti, avec un bruit d'un point (audit 05) et les seuils statistiques usuels, il faut environ **16 observations par réglage**, soit **4 mois de chaque côté**. Calcul : n = 2 × (1,96 + 0,84)² × σ² / δ², avec σ = δ = 1.

Conséquences :
- la plupart des paramètres ne seront **pas identifiables avant 6 à 12 mois** ; certains jamais (tu n'auras qu'un 80 km) ;
- un « coach qui apprend de toi » en quelques semaines serait de la fausse précision avec un vernis de personnalisation ;
- ce qui est accessible vite, c'est de **réfuter des hypothèses grossières** (ton ressenti du mercredi dépend-il du CrossFit du mardi ?) et de mesurer **ta régularité**, qui est le paramètre le plus prédictif de ta réussite (audit 01).

## 2. Ce qui peut se régler, et ce qui ne doit pas

| Paramètre | Aujourd'hui | Réglable sur tes données ? | Données nécessaires | Délai réaliste |
|---|---|---|---|---|
| **Régularité** (sorties longues tenues) → marge de rampe (P-30), « niveau probable » (P-01) | supposée parfaite | **oui, et c'est le premier** | prévu contre fait, par semaine | 8 semaines |
| Repère de ressenti et bruit personnel (P-10) | 4 premières séances | oui | ressenti de toutes les courses, étiquette « lendemain de renfo » | 8 à 12 semaines |
| Effet du CrossFit sur la course du lendemain (P-17) | ignoré | oui (réfutable) | durée et ressenti du CrossFit, jambes au réveil | 8 à 12 semaines |
| Récupération après une sortie longue | grille fixe | peut-être | jambes au réveil à J+1 et J+2, ressenti de l'endurance suivante | 4 à 6 mois |
| Cadence des semaines allégées (3 pour 1) | fixe | peu probable | il faudrait comparer deux cadences | plus de 8 mois |
| Tolérance aux glucides | déjà suivie | oui (déjà le cas) | glucides pris, confort digestif | en cours |
| Tolérance à la descente | absente | plus tard | D− par sortie, jambes à J+2 | 4 à 6 mois |
| **Règle des 30 jours, mémoire de reprise, plancher, mode reprise** | fixes | **non : garde-fous, jamais personnalisés** | — | — |
| Pente de +10 % | fixe | **non** tant qu'aucune donnée de blessure ne le justifie (une personne, événements rares) | — | — |

## 3. Garde-fous déterministes (non négociables)

1. Un paramètre réglé reste dans un **intervalle écrit d'avance** (dans `CONV`), issu des conventions actuelles.
2. Les garde-fous de sécurité s'appliquent **après** tout réglage et ne sont jamais réglés.
3. Un réglage change au plus **une fois par phase**, au bilan, avec la donnée qui le justifie affichée ; tu acceptes ou tu gardes l'ancien.
4. Tout réglage est **réversible** et journalisé (date, ancienne valeur, nouvelle, nombre d'observations).
5. En dessous d'un nombre minimal d'observations, écrit dans la spec, le réglage est **impossible** : l'appli dit « pas assez de données » plutôt que de régler.
6. Le moteur reste une fonction pure et déterministe : mêmes entrées, même plan (invariant vérifié, audit 02).

## 4. Suivi « prévu contre réel » : la brique manquante

Aujourd'hui le plan passé est **recalculé** chaque jour (point 3 de CHANTIER-MOTEUR). On ne peut donc pas comparer ce qui était prévu le jour J à ce qui a été fait. C'est le préalable à tout le reste.

**À figer, automatiquement, chaque semaine** (aucune saisie) : les séances prévues de la semaine telles qu'affichées (type, durée, D+ visé), la version du moteur, la phase, le niveau de sortie longue, les limites en vigueur (référence des 30 jours). Une ligne par semaine, jamais réécrite.

## 5. Données à enregistrer dès maintenant

Critère : moins de 30 secondes par séance, sinon tu ne le feras pas.

| # | Donnée | Coût | Existe déjà ? | Sert à réfuter |
|---|---|---|---|---|
| 1 | Plan de la semaine figé (§ 4) | aucun | non | tout |
| 2 | Durée et D+ faits contre prévus | aucun (import montre) | oui | H-26, H-45 |
| 3 | Ressenti de **toutes** les courses, sortie longue comprise (stocké même s'il n'est pas lu) | 1 geste | oui | H-46, H-37 |
| 4 | « Jambes au réveil » le lendemain d'une sortie longue et d'un renforcement (3 niveaux) | 1 geste | champ `legs` présent | H-12, P-17 |
| 5 | Renforcement : durée, ressenti, jambes sollicitées ou non | 2 gestes | champs présents | G-CHG-001 |
| 6 | Séance manquée : raison en 4 choix (agenda, fatigue, maladie, blessure) et « annoncée d'avance » ou non | 1 geste | 2 choix aujourd'hui | H-49, P-11 |
| 7 | Créneau prévu de la sortie longue (P-31) contre jour réel | 1 question par semaine | non | adhérence |
| 8 | D− de la sortie quand la trace est jointe | aucun | champ présent | P-19 |
| 9 | Glucides par heure et confort digestif | déjà saisi | oui | H-11 |

**À ne pas enregistrer pour l'instant** : sommeil, variabilité cardiaque, poids, humeur quotidienne. Voir § 6.

## 6. D-77 : rouvrir la lecture des données de santé ?

**Recommandation : non, pas maintenant. Réexamen daté à la fin de la phase F2.**

- Le problème du signal de fatigue n'est pas un manque de capteurs, c'est une règle trop nerveuse sur une note par semaine (audit 02, cas J). Ajouter une variable bruitée de plus n'y change rien.
- Bénéfice d'un entraînement guidé par la variabilité cardiaque à 2 séances par semaine : **non vérifié** dans cet audit ; je ne le présume pas.
- Coût : données de santé envoyées à un service de plus, alors que l'isolation côté serveur n'est pas auditable aujourd'hui (audit 04) et que les fonctions servent ta clé à tout compte connecté.
- Condition de réouverture, à écrire : si après 12 semaines le signal corrigé (P-10, P-17) reste muet alors que tu as manqué au moins 2 séances pour fatigue, on rouvre, pour la fréquence cardiaque de repos seulement.

## 7. Rôle d'un LLM

| Oui (lecture seule, après le moteur) | Non |
|---|---|
| **Expliquer** le plan et ses changements à partir du fil « ce qui a changé et pourquoi » (codes de raison du point 4 de CHANTIER-MOTEUR) | Modifier le plan, proposer une durée, une allure, un nombre de répétitions |
| **Résumer** un bilan de phase, commentaires de séance compris | Régler un paramètre du moteur |
| **Traduire** : photo de WOD, note dictée → champs de saisie (fonction `analyze-wod`, écrite, non déployée) | Lever ou assouplir un garde-fou |
| Répondre à « pourquoi ? » en citant la décision (`D-xx`) et sa classe (science, extrapolation, convention) | Interpréter une douleur ou un symptôme (renvoi vers un professionnel) |

Conditions :
1. Le LLM reçoit les chiffres du moteur et ne peut citer qu'eux : tout nombre affiché est vérifié contre le plan avant affichage, sinon le message est rejeté.
2. Il **étiquette** chaque affirmation : « règle de sécurité », « convention de coach », « non vérifié ». Un texte fluide fait passer une convention pour un fait ; c'est le risque principal.
3. Clé d'API en secret Supabase seulement, utilisateur vérifié (P-28), consentement explicite avant tout envoi de données personnelles.
4. Préalable : le fil de raisons existe et le plan est figé. Sans eux, le LLM inventerait l'explication.

**Ta décision du 25/09 reste la bonne** : reporter le chat sur le plan jusqu'à avoir observé un premier cycle fatigue → semaine allégée → reprise sur tes données. Rien dans l'audit ne la contredit.

## 8. Étapes et portes de décision

| Étape | Contenu | Porte pour passer à la suivante |
|---|---|---|
| **0. Maintenant** | Corriger les défauts (P-07, P-08, P-23) ; figer le plan ; enregistrer les 9 données | 8 semaines consécutives avec au moins une sortie par semaine |
| **1. Lire** (fin F1–F2) | Tableau prévu contre réel ; ta régularité ; premières réfutations (mercredi et CrossFit, bruit du ressenti) | au moins 16 endurances notées et 8 sorties longues |
| **2. Régler** (pas avant 6 mois) | Deux paramètres au plus : marge de rampe selon la régularité ; repère de ressenti | un cycle complet observé, aucun garde-fou touché |
| **3. Expliquer** | LLM en lecture seule sur le fil de raisons | fil de raisons et plan figé en service depuis une phase |

## 9. Décisions demandées

1. **Valider la liste des 9 données** (§ 5) et le plan figé (§ 4) comme prochaine spec, avant toute nouvelle règle d'entraînement.
2. **D-77 reste fermée** jusqu'à la fin de F2, avec la condition de réouverture du § 6.
3. **LLM = explication seulement**, après le fil de raisons ; jamais de réglage ni de prescription.
4. **Aucun réglage automatique** avant les seuils du § 8 ; le premier paramètre « personnalisé » est ta régularité, pas ta physiologie.

## Lien avec le chantier « modèle allure-effort »

Le « ressenti attendu contre réel » demande un modèle d'effort attendu : il dépend de ce chantier et de traces en nombre. D'ici là, le repère est personnel et par type de séance (P-10). Ce que cette note ajoute au chantier : joindre la trace à chaque sortie longue dès maintenant, même si rien ne la lit encore.

## Sources

- Calcul de taille d'échantillon : formule usuelle de comparaison de deux moyennes (risque de 5 %, puissance de 80 %) ; application à un seul coureur = ordre de grandeur, pas un plan d'étude.
- Bruit du ressenti, intentions de mise en œuvre, habitude : `docs/audit/05-litterature.md`.
- Entraînement guidé par la variabilité cardiaque : **non vérifié** ici.
- Décisions citées : D-72, D-77, `claude/CHANTIER-MOTEUR.md` (points 3 et 4).
