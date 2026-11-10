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
