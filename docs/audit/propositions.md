# Propositions de spec issues de l'audit — BROUILLONS

Rien ici n'est décidé ni codé. Chaque proposition devient une entrée `D-xx` (et `H-xx` si elle repose sur une convention) **seulement si tu la valides**. Les numéros `D-97…` et `H-59…` sont provisoires (libres au 11/11/2026, vérifié par recherche dans `docs/` et dans le moteur) ; ne pas les considérer comme attribués.

Format : constat chiffré → règle proposée → nature (science / convention / extrapolation) → ce qui la réfuterait.

---

## Mission 1 — adhérence (rapport `01-faisabilite.md`)

### P-01 — « Niveau probable à la date » (D-97 provisoire, H-59 provisoire)
**Constat.** Le plan affiché suppose 0 % de semaines perdues. À 25 % : sortie la plus longue du bloc entre 3 h 50 et 6 h (P10–P90), 5 h atteintes dans 75 % des cas. Décaler la course de 4 à 12 semaines ne fait gagner que 3 à 11 points (plafond vers 80 %).
**Règle proposée.** À côté de la date voulue (Ton objectif, Suivi) :
- une **fourchette de niveau probable** le jour J, calculée sur le taux de sorties longues tenues des 8 dernières semaines (au moins 4 semaines de plan écoulées, sinon « pas encore de repère ») ;
- une **date réaliste** seulement quand un décalage change vraiment l'issue ; sinon dire que la date n'est pas le levier et nommer le levier (sorties longues tenues).
Jamais d'effet sur le plan (affichage seul, comme D-88).
**Table de départ** (simulée, à ± 5 points ; à recalculer si une règle change) :

| Sorties longues tenues | Plus longue sortie probable (P10–P90) | Chances d'une sortie de 5 h |
|---|---|---|
| ≥ 90 % | 5 h 30 à 6 h | environ 9 sur 10 |
| environ 80 % | 3 h 50 à 6 h | 3 sur 4 |
| environ 70 % | 2 h 35 à 6 h | 1 sur 3 |

**Nature.** Convention (H-59) : le modèle de semaines perdues (indépendantes, une ou deux sorties) est une hypothèse ; les pertes groupées font 16 à 26 points de moins.
**Réfutation.** Comparer, à chaque changement de phase, la fourchette annoncée 8 semaines plus tôt au niveau réel.

### P-02 — Mode « semaine chargée » (D-98 provisoire)
**Constat.** Protéger la sortie longue quand une seule sortie saute : 75 → 94 % (25 %), 36 → 81 % (40 %). Tenir le mercredi à 60 min au lieu de 90 : aucun effet sur la cible.
**Règle proposée.** Un bouton « semaine chargée » sur la semaine en cours ou la suivante : la sortie longue reste (déplaçable dans la semaine, D-73), les autres courses de la semaine sont retirées de l'affichage et **ne comptent ni comme manque ni comme fatigue** ; le renforcement devient facultatif. Le moteur recalcule comme aujourd'hui avec ce qui est fait. L'appli recommande ; elle n'active jamais ce mode seule.
**Nature.** Convention de coach (la sortie longue est la seule séance qui progresse, D-67), chiffrée par simulation.
**Réfutation.** Si, sur tes données, les semaines « chargées » sont suivies d'un ressenti plus haut sur l'endurance suivante, le mode cache de la fatigue.

### P-03 — Séance de repli (D-99 provisoire, H-60 provisoire)
**Constat.** Un repli de 45 ou 90 min à la place d'une sortie longue perdue ne protège pas la cible (75 → 75 / 78 % ; 36 → 31 / 36 %). Aujourd'hui il nuit même : une semaine avec une seule petite sortie consomme la sortie clé non faite (défaut B, audit 02).
**Règle proposée.** Quand ni la sortie longue ni l'endurance ne sont possibles : **30 à 45 min, dont 10 à 15 min soutenues** (côtes ou tempo), n'importe quel jour. But : ne pas rompre l'habitude et garder l'intensité. Elle ne remplace pas la sortie longue, ne consomme ni sortie clé ni semaine allégée, et le dit (« repli : ça garde l'élan, pas le niveau »).
**Nature.** Extrapolation (H-60) : Spiering et coll. 2021 montrent qu'en population générale l'endurance se maintient jusqu'à 15 semaines avec une fréquence ou un volume très réduits **si l'intensité est gardée**, mais pas l'endurance de longue durée quand le volume est coupé des deux tiers, et sans données suffisantes chez les sportifs entraînés. Aucune source sur l'ultra-trail.
**Réfutation.** Si les semaines de repli sont suivies d'autant d'arrêts que les semaines vides, le repli ne sert à rien.

### P-04 — Politique de rattrapage (D-100 provisoire)
**Règle proposée (à écrire, déjà en grande partie le comportement du moteur).** Une séance manquée n'est jamais doublée ni ajoutée à la semaine suivante. Une sortie longue manquée se déplace dans la même semaine (D-73) ; sinon la suivante reprend **au niveau atteint**, pas au niveau prévu. Une endurance manquée est perdue. Deux sorties longues ne se suivent jamais à moins de 5 jours.
**Nature.** Convention prudente ; la limite des auteurs de Frandsen 2025 (hausses enchaînées sans récupération) va dans ce sens.

### P-05 — Alerte « fenêtre » avant l'effondrement (D-101 provisoire)
**Constat.** À 25 %, 32 % des trajectoires subissent au moins un effondrement (médiane : 65 min de niveau perdues, environ 10 semaines pour revenir de 3 h 20 à 5 h).
**Règle proposée.** Quand la dernière sortie « au niveau » aura plus de 30 jours avant la prochaine sortie longue prévue, le dire **une semaine avant** : « Ta dernière sortie de 4 h 35 date du 20/06. Si tu ne refais pas une longue d'ici dimanche, la limite repart de 3 h 20. » Information seule.
**Nature.** Application directe de S-BLE-004 (la fenêtre est celle de l'étude) ; le seuil d'alerte est une convention.

### P-06 — Plafond de durée par jour pour l'endurance (réexamen de D-71) (D-102 provisoire)
**Constat.** 34 mercredis sur 47 prescrits au-delà des 60 min que tu as déclarées possibles ; effet nul sur la cible.
**Règle proposée.** Rétablir un plafond facultatif par jour, appliqué à l'**endurance et à la qualité seulement** ; la sortie longue garde sa progression (D-67). Une séance de qualité qui ne tient pas dans le plafond n'est pas posée (règle existante du créneau).
**Nature.** Choix de produit. Coût : environ 13 h d'endurance en moins sur 11 mois (7 % du volume couru prévu).
**Réfutation.** Si tu fais réellement 90 min le mercredi quand c'est prescrit, D-71 avait raison.

---

## Mission 2 — audit adversarial (rapport `02-adversarial.md`)

### P-07 — Numéro de semaine insensible au changement d'heure (correction, pas de D-xx nécessaire)
**Constat.** `todayW` et `runsW` : `Math.floor((D(a)-D(start))/(7*DAY))`. Plan démarré en hiver, lundi d'été : 7k jours − 1 h → semaine k−1. 82 scénarios sur 441 lus le lundi dépassent la règle des 30 jours ; 0 en UTC.
**Correction proposée.** Compter les semaines entre lundis avec `Math.round`, comme le fait déjà `N` ; même fonction pour `todayW`, `runsW` et tout calcul de semaine de l'interface. Test : `tests/audit/t_audit_heure_ete.js` passe au vert, à ajouter à `tools/test.py`. Parité v1 : sans effet (les cas de parité n'ont ni séance ni lundi d'été), à confirmer par `parity.py`.

### P-08 — Semaine passée : lire le réel, pas le prévu (D-103 provisoire)
**Constat.** Une semaine passée avec une course mais sans sortie longue compte la sortie longue prévue comme faite : sortie clé consommée (cas B), alternance déclenchée (cas B2). 75 → 82 % à 25 % de semaines perturbées, 36 → 48 % à 40 %.
**Règle proposée.** Pour une semaine passée : `lrPrec` = plus longue sortie longue réellement faite (0 sinon) ; une sortie clé n'est comptée que si une sortie longue d'au moins 90 % de sa durée a été faite. Texte de la correction testée : `tests/audit/corrections.js` (P08).
**Nature.** Correction de logique (« le passé ne se réécrit pas » s'applique aussi au moteur).

### P-09 — Besoin de monter jugé sur le niveau atteint (D-104 provisoire)
**Constat.** Après une course, `doitMonter` lit la plus longue des 30 jours (la course) et conclut que la cible est atteinte (cas C). Avec P-08 : 82 → 88 % (25 %), 48 → 63 % (40 %).
**Règle proposée.** `doitMonter` reçoit `min(plus longue des 30 jours, niveau de sortie longue atteint)`. **Borne à ajouter** : après une course, pas plus de +10 % par sortie au-dessus du niveau d'avant course (sinon saut direct à la cible, autorisé par la lettre de la règle des 30 jours mais sans appui).
**Nature.** Correction + convention (la borne).

### P-10 — Signal de fatigue robuste au bruit (D-105 provisoire, révise H-46 et H-47)
**Constat.** À 2 jours de course, une note par semaine. Bruit de ± 1 point sans fatigue réelle : 100 → 67 % de réussite. Un ressenti toujours haut ne déclenche rien.
**Règle proposée.** (a) Un gel de la sortie longue demande **deux signaux concordants** dans les 14 jours : deux notes au-dessus du repère, ou une note + une séance manquée pour fatigue (D-72), ou une note + une durée non tenue. Une note isolée = « à surveiller », affichée, sans effet. (b) **Plancher absolu** : une endurance notée 6/10 ou plus est un signal quel que soit le repère personnel. (c) Le repère se recalcule sur les 8 dernières notes, pas sur les 4 premières.
**Nature.** Convention. L'échelle (0,12 par point) reste H-38, dont le texte est à réintégrer.
**Réfutation.** Rejouer `sim_adherence.js … BRUIT` : la réussite sous bruit pur doit rester à ± 5 points de la réussite sans bruit ; une fatigue simulée de 3 semaines (notes +2) doit toujours déclencher.

### P-11 — Mode reprise (D-106 provisoire, H-61 provisoire)
**Constat.** 3 semaines d'arrêt : semaine de retour = qualité de 1 h 30 + 3 h 20 (cas M).
**Règle proposée.** Après 2 semaines sans course, ou une semaine avec un jour marqué « malade » ou « blessé » : la première semaine n'a **pas de séance de qualité** et la sortie longue est limitée à 70 % de ce que la règle des 30 jours autorise ; la deuxième semaine revient à la règle. Message : la raison et la durée.
**Nature.** Convention (H-61), dans l'esprit de S-BLE-003 (fréquence avant intensité, durée avant vitesse ; niveau de preuve faible).

### P-12 — Dépassement non suivi (D-107 provisoire)
**Constat.** 2 h prévues, 3 h faites : la suivante est prescrite à 3 h (cas I).
**Règle proposée.** Si une sortie longue dépasse à la fois le prévu de 30 % et la règle des 30 jours, la suivante revient à ce qui était prévu, et un message le dit (« sortie bien au-delà du prévu : on consolide avant de remonter »). La référence des 30 jours, elle, lit toujours le réel.
**Nature.** Convention prudente ; appui indirect : Frandsen 2025, catégorie +30 à +100 % (HR 1,52).

### P-13 — Affûtage qui allège (D-108 provisoire, révise les coefficients `aff` de H-06)
**Constat.** 2 jours : 4 h 30, 4 h 35, 4 h 20 sur les trois dernières semaines pleines ; 3 h 20 à J−6 ; 1 h 25 à J−3 (cas E).
**Règle proposée.** Les coefficients d'affûtage s'appliquent au **volume des 3 dernières semaines de charge**, pas au niveau de la sortie clé ; dernière sortie longue ≤ 2 h à J−6 ou J−7 ; rien de plus de 45 min après J−4.
**Nature.** Volume : S-COU-006 (niveau élevé, hors ultra). Plafonds de 2 h et 45 min : convention.

### P-14 — Historique déclaré non annulé par une course réelle (prolonge D-94)
**Constat.** Une course réelle dans les 35 jours avant le départ annule la fréquence déclarée (cas H, 113 états sur 3 000).
**Règle proposée.** Par semaine d'avant plan : le réel s'il y en a, sinon la déclaration. Jamais « tout l'un ou tout l'autre ».

### P-15 — Zones tampons autour des seuils (révise H-45, H-06)
**Constat.** 2 minutes de sortie de référence déplacent 2 semaines de plan (cas G) ; 4 h 35 pour 5 h visées : aucune alerte.
**Règle proposée.** Tranche de durée : entre 7 h et 9 h estimées, garder la tranche basse sauf priorité A (ou demander). Alerte d'écart : « dans la fourchette » de 90 à 100 %, dite comme telle, au lieu du silence.
**Nature.** Convention.

### P-16 — Tests
`isRun` unique partagé par l'appli et les tests ; un test qui rejoue une course réelle ; `tests/t_invariants.js` (déjà ajouté, vert) ; `tests/audit/t_audit_heure_ete.js` à basculer dans `tools/test.py` quand P-07 est codée ; `tests/audit/cas.js` à transformer en assertions au fil des corrections.

---

## Mission 3 — charge totale et spécificité trail (rapport `03-charge-specificite.md`)

### P-17 — Ressenti du lendemain de renforcement (complète P-10 ; H-62 provisoire)
**Constat.** 46 mercredis sur 47 sont un lendemain de CrossFit ; c'est là que le moteur lit ton seul signal de fatigue.
**Règle proposée.** Une endurance courue moins de 36 h après une séance de renforcement porte une étiquette « lendemain de renfo ». Son ressenti est comparé aux autres séances de la même étiquette, et ne déclenche jamais seul un gel. À l'écran Organisation, un conseil (non imposé) : 48 h entre renforcement des jambes et course, quand la semaine le permet.
**Nature.** Convention (H-62), appui : Doma et coll. 2017 (fatigue résiduelle de quelques heures à plusieurs jours, délai non fixé).
**Réfutation.** Si, sur 8 semaines, ton ressenti du mercredi ne diffère pas selon que le mardi a été fait ou non, l'étiquette est inutile.

### P-18 — Texte du renforcement libre (correction de texte)
« Tu gères ton renforcement : l'app la compte dans ta charge. » → « Tu gères ton renforcement. L'app compte le jour, pas la charge de la séance. »

### P-19 — Descente (D-109 provisoire, H-63 provisoire)
**Constat.** Aucune séance de descente prescrite ; plus grosse descente d'entraînement = 40 % de celle de la course ; D− saisi mais lu par aucune règle ; après une coupure le D+ revient à la densité de la phase.
**Règle proposée.** (a) Affichage : D− cumulé des 30 derniers jours et plus grosse descente, face au D− de la course (information). (b) Option de séance « répétitions de descente » en F3 et en bloc, proposée, jamais imposée, volume prudent et croissant. (c) Après une semaine « arrêt », la densité de D+ de la sortie longue repart de la densité de départ et remonte en 3 sorties.
**Nature.** Convention (H-63) ; mécanisme : S-TRA-012. Aucune dose validée en ultra-trail.

### P-20 — Nutrition : un seuil, une fonction (révise D-30 ; D-110 provisoire)
**Constat.** Quatre seuils (60 min, 1 h, 1 h 30, 2 h) et deux jeux de chiffres (35 g/h de départ sur la carte ; 40 ou 60 g/h et 500 ml/h en dur sur la ligne de repli).
**Règle proposée.** Paliers dans `CONV.nutri` : de 60 à 90 min, ligne sans cible ; à partir de 90 min, carte avec la cible de progression ; plafonds 60 g/h sous 2 h 30, 90 au-delà (alignés sur la position de 2016, à relire dans le texte original). Une seule fonction pour la carte, la note de séance et le Suivi. Boisson : le réglage du profil, présenté comme repère personnel. Corriger dans D-30 la phrase « en deçà l'apport à l'effort n'a pas d'objet ».
**Nature.** Paliers 1 h / 2 h 30 : position d'experts (2016). Seuil de 90 min pour la carte : convention.

### P-21 — Charge hors course : enregistrer d'abord (prépare G-CHG-001)
**Règle proposée.** Rien dans le moteur pour l'instant. Rendre rapide la saisie de trois valeurs après chaque séance de renforcement : durée, ressenti, « jambes au réveil le lendemain » (le champ `legs` existe). Décision de brancher G-CHG-001 après 8 semaines de données (audit 06).

### P-22 — Bloc spécifique à 3 jours et liste de contrôle
**Règle proposée.** À l'entrée en F3, l'appli propose (bilan de phase) de passer à mercredi + samedi + dimanche avec un seul renforcement, en montrant ce que cela change ; l'utilisateur décide. En bloc, une liste de contrôle hors moteur : nuit, bâtons, sac et matériel obligatoire, ravitaillement testé.
**Nature.** Convention (S-TRA-009, niveau faible). Simulé : 79 % contre 75 % à 25 % de semaines perturbées, donc sans pénalité de robustesse.

---

## Mission 4 — fiabilité des données (rapport `04-donnees.md`)

### P-23 — Connexion sur un état local vierge : le serveur d'abord (correction ; D-111 provisoire)
**Constat.** Navigateur vidé puis connexion : le profil vide local, marqué « modifié maintenant » par `boot()`, écrase le profil du serveur (scénario 1).
**Règle proposée.** (a) `markChanges()` ne marque jamais un profil non démarré (`onboarded` faux, pas de date d'objectif) ; (b) à la connexion, si l'état de synchro local est vide (`lastPull` nul), lecture complète du serveur **avant** tout marquage, et le serveur gagne pour toute clé qu'il contient ; (c) même garde quand l'état de synchro est illisible.
**Test.** Scénario 1 de `tests/audit/sync_scenarios.py` au vert.

### P-24 — Restauration sûre (D-112 provisoire)
**Règle proposée.** Avant de restaurer : résumé chiffré (« ce fichier contient 2 séances ; ton compte en a 5 ; 3 seront supprimées partout ») et confirmation ; téléchargement automatique de l'état courant ; mode par défaut « fusionner » (ajoute et met à jour, ne supprime rien), mode « remplacer » en option explicite.

### P-25 — Profil fusionné par rubrique (D-113 provisoire)
**Constat.** Le dernier appareil à synchroniser écrase tout le profil (scénario 3).
**Règle proposée.** Une ligne de synchro par rubrique du profil (objectif, jours, organisations et historique, départ, manques, décalages, bilans, réglages) ; `manques` et `decal`, qui sont des dictionnaires par date, fusionnés clé par clé. L'horodatage d'une modification est celui de la modification et n'est plus rafraîchi par `markChanges()`.

### P-26 — Serveur : horodatage, historique, schéma versionné (D-114 provisoire)
**Règle proposée.** Déclencheur qui écrit `updated_at = now()` à chaque écriture (corrige le scénario 2b) ; table `trail_items_history` alimentée par déclencheur, limitée aux 30 dernières versions par clé ; fichier `supabase/schema.sql` (table, index, politiques d'accès par `auth.uid()`) dans le dépôt, appliqué à la main comme les fonctions.
**Attention.** Avec un horodatage serveur, la comparaison locale « ma modification est plus récente » doit se faire sur un compteur de version, pas sur l'heure du téléphone : à écrire dans la spec avant de coder.

### P-27 — Rappel de sauvegarde (D-115 provisoire)
**Règle proposée.** Date du dernier export affichée dans Profil ; rappel discret si plus de 30 jours ou à chaque bilan de phase ; l'export reste un geste de l'utilisateur.

### P-28 — Fonctions intervals : vérifier l'utilisateur (sécurité)
**Constat.** Les fonctions servent ta clé intervals.icu à tout compte connecté au projet.
**Règle proposée.** La fonction lit l'utilisateur du jeton et refuse tout autre que le propriétaire (identifiant en secret), ou lit une clé par utilisateur. Tant que l'appli est personnelle : inscription fermée dans Supabase.

### P-29 — Test de synchro dans la batterie
`tests/audit/sync_scenarios.py` rejoint `tools/test.py` (étape facultative si Playwright ou Chrome manquent) quand P-23 à P-25 sont codées.

---

## Mission 5 — littérature (rapport `05-litterature.md`)

### P-30 — Rampe robuste de la sortie longue (révise H-26 ; D-116 provisoire, H-64 provisoire)
**Constat.** « Juste à temps » avec 3 semaines de marge : sans jalon intermédiaire, 71 % de réussite à 25 % de semaines perturbées et 31 % à 40 % ; la sortie longue reste à 1 h 15 pendant 3 mois. Marge de 10 semaines (copie du moteur) : 86 % et 46 %.
**Règle proposée.** (a) Monter tôt jusqu'à un plateau de 3 h (une sortie par semaine, sans alternance), l'entretenir ; (b) monter ensuite vers les sorties clés avec une marge qui dépend des sorties longues tenues sur 8 semaines : 3 semaines si ≥ 90 %, 6 si environ 80 %, 10 en dessous.
**Nature.** Convention (H-64) ; rejoint la base d'Uphill Athlete (GABARIT, écart n° 6).
**À faire avant décision.** Simuler le plateau à 3 h (non fait) et chiffrer le volume ajouté.

### P-31 — Planification « quand, où » de la sortie longue (D-117 provisoire, H-65 provisoire)
**Règle proposée.** Une question par semaine (jour et heure de la sortie longue, puis créneau de secours) ; envoi à la montre ce jour-là ; aucun compteur de séries, aucune couleur d'échec sur une séance manquée.
**Nature.** Convention (H-65) ; appui : méta-analyse de 2013 sur les intentions de mise en œuvre (effet petit à moyen) et étude de 2010 sur l'habitude (un manque isolé ne la compromet pas).
**Réfutation.** Taux de sorties longues tenues sur 8 semaines avec et sans la question (comparaison avant/après, un seul coureur : indicatif).

### P-32 — Hypothèses à réécrire dans `HYPOTHESES.md`
H-38 et H-39 (texte à réintégrer) ; H-58 (mention « pari : catégorie +10 à +30 % de S-BLE-004 ») ; H-46 (limite à 2 jours : une note par semaine, lendemain de renforcement) ; H-22 (ne produit pas de baisse de volume à 2 jours) ; H-26 (non robuste sous adhérence imparfaite) ; H-37 (non tenue : le ressenti de la sortie longue n'est pas lu). Colonne « classe » (science / extrapolation / convention) à ajouter au registre.
