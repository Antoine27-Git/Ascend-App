# Audit Ascend — Synthèse (11/11/2026)

Moteur et appli v54 (`main`, PR #21 déjà fusionnée à mon arrivée). Six rapports dans ce dossier, propositions en brouillon dans `propositions.md` (P-01 à P-36), scripts dans `tests/audit/`. **Aucune règle du moteur modifiée ; `tools/test.py` vert** (un test ajouté, `t_invariants.js`).

## Les 5 constats, par impact

**1. Tes données : se connecter sur un navigateur vidé écrase le profil du compte.** Rejoué sur la vraie appli : le profil vide local, marqué « modifié maintenant » au démarrage, gagne contre le serveur. Objectif, jours, organisation, départ du plan, manques : perdus sur le téléphone **et** sur le serveur ; les séances survivent. 4 scénarios de synchro sur 5 en défaut (profil écrasé par le dernier à synchroniser ; une vieille sauvegarde restaurée supprime du serveur les séances plus récentes). Tu effaces souvent tes données de navigation : c'est ton risque n° 1, avant tout sujet d'entraînement. → audit 04, P-23, P-24.

**2. Ton objectif tient sur le papier, pas encore dans ta vie.** Sortie clé de 5 h atteinte dans **94 / 75 / 36 %** des cas à 10 / 25 / 40 % de semaines perturbées (± 5 points) ; **78 / 49 / 25 %** si les semaines perdues sont groupées. Ta seule donnée réelle (septembre–octobre : environ 8 semaines sur 9 perdues, d'un bloc) est pire que mon pire scénario. Le levier : **protéger la sortie longue** (75 → 94 %, 36 → 81 %). Décaler la course ne gagne que 3 à 11 points. Le 50 km en priorité C est un piège (12 %). → audit 01, P-01, P-02.

**3. Une bonne part de la fragilité vient de défauts du moteur, pas de la physiologie.**
- *Heure d'été* : pour un plan démarré en hiver, tout lundi d'été est compté dans la semaine d'avant. 82 scénarios sur 441 lus le lundi dépassent la règle des 30 jours ; 0 en fuseau UTC. Lu le lundi, ton taux de réussite passe de 75 à 66 %.
- *Séance fantôme* : une sortie longue manquée compte comme faite si une autre course a eu lieu dans la semaine (clé consommée, alternance déclenchée). Faire son mercredi pénalise.
- *Course en fenêtre* : après le 50 km, le moteur croit le niveau atteint pendant 30 jours.
- Deux corrections de logique (P-08, P-09) : **75 → 88 %** et **36 → 63 %**. → audit 02.

**4. Fausse précision n° 1 : le signal de fatigue.** À 2 jours, il tient sur **une note par semaine**. Un bruit de ± 1 point, sans fatigue ni séance manquée, fait tomber la réussite de **100 à 67 %** ; un ressenti toujours à 7/10 ne déclenche rien. Cette note est prise **46 mercredis sur 47 le lendemain du CrossFit**, que le moteur ne voit pas (deux séances notées 10/10 : 0 séance de course modifiée) alors qu'il pèse 35 à 71 % de ta charge hebdomadaire (hypothèse : 60 min à 7/10). → audits 02 et 03, P-10, P-17.

**5. Le moteur est un plan de coach écrit en code.** Sur 58 hypothèses : **0 science directe, 10 extrapolations, 45 conventions**, 1 mesure, 2 introuvables. Conséquences mesurées : D-96 place 10,4 % des sorties longues prescrites dans la catégorie « +10 à +30 % » de Frandsen 2025 (0,8 % sans lui ; chez toi 6 sur 44, +11,8 % au plus) ; l'affûtage à 2 jours n'allège pas (4 h 30, 4 h 35, 4 h 20, puis 3 h 20 à J−6) ; pas de mode reprise après maladie (qualité de 1 h 30 et 3 h 20 la semaine du retour) ; aucune séance de descente ; quatre seuils de nutrition différents. → audits 02, 03, 05.

## Ce qui est solide

- Règle des 30 jours sur la sortie longue lue le jour même : **0 violation sur 26 492 sorties longues** (3 000 scénarios, fuseau UTC).
- Déterminisme, forme des séances (durées, une course par jour, déroulé = durée) : 0 violation sur environ 63 000 séances.
- Parité v1 : 0 écart sur 5 cas + 60 tirés au hasard.
- Reprise après plus de 30 jours : jamais plus d'1 h (D-94). Le plafond coûte cher en faisabilité (75 → 97 % sans lui) mais c'est lui qui respecte la seule preuve du projet : **à garder**.
- Synchro des séances ligne par ligne, file d'attente hors ligne, aucune clé secrète dans le dépôt.

## Ce qui est une convention (à afficher comme telle)

Sorties clés de 5 à 6 h, alternance au-delà de 3 h, semaine allégée sur 4, rampe « juste à temps » avec 3 semaines de marge, coefficients d'affûtage et de reprise, gel de 1 à 2 semaines sur un ressenti, arrondi supérieur (D-96), seuil d'écart à 90 %, tranches de durée, densité de D+, pas de 6 g/h de glucides. Extrapolations d'un résultat publié : règle des 30 jours en durée et en trail, affûtage, marche-course de départ, répartition des intensités.

## Fausses précisions à retirer

Ressenti lu au point près ; seuil net à 8 h (2 minutes sur ta sortie de référence déplacent 2 semaines de plan) ; « 5 h le 11/07 » affiché à 10 mois ; 15 h 05 et 8 h 06 à la minute pour des estimations à ± 15–19 % ; la minute d'arrondi (D-95, D-96) qui a occupé deux décisions alors que son effet réel est le cumul.

## Décisions à prendre

| # | Décision | Ma recommandation |
|---|---|---|
| 1 | **Ordre des corrections** avant toute nouveauté : P-23 (profil écrasé), P-07 (heure d'été), P-08 (séance fantôme), P-10 (signal de fatigue) | Oui, dans cet ordre |
| 2 | **Objectif** : garder le 80 km du 25/09/2027 ? | Oui, avec le 50 km du 08/05 (priorité B) comme porte : sortie d'environ 3 h 30 tenue deux semaines avant et course bien passée, sinon 50–60 km à l'automne et 80 km au printemps 2028 |
| 3 | **Semaine chargée** (P-02) et question hebdomadaire « quel jour, quelle heure » pour la sortie longue (P-31) | Oui : c'est +19 à +45 points |
| 4 | **D-96** : garder, borner ou retirer | Garder en le bornant (+12 % au plus) et réécrire H-58 comme un pari |
| 5 | **CrossFit** : tester 4 semaines la course le jeudi, ou le mardi en haut du corps | À toi ; noter le ressenti dans les deux cas |
| 6 | **Affûtage, reprise, dépassement** (P-13, P-11, P-12) | Oui pour les trois, en conventions affichées |
| 7 | **Rampe robuste** (P-30, plateau à 3 h) | Pas encore : à simuler d'abord |
| 8 | **Nutrition** : un seuil à 90 min, une fonction (P-20) | Oui |
| 9 | **Coach personnalisé** : les 4 décisions de la note 06 (données à enregistrer, D-77 fermée, LLM en explication seule, pas de réglage avant 16 notes) | Oui |

## À faire toi-même cette semaine (10 minutes, sans code)

1. **Exporter le JSON** (Profil → Exporter) et le garder hors du téléphone ; le refaire avant tout effacement des données de navigation.
2. Dans Supabase : vérifier que le projet n'est pas en pause, que **l'inscription est fermée**, et que la table n'est pas lisible sans compte (commande dans l'audit 04).
3. Lire ton plan **le jour de la séance**, pas le lundi, tant que P-07 n'est pas corrigée. Aucun effet d'ici là en heure d'hiver : le défaut apparaît au passage à l'heure d'été, le 28/03/2027.
4. Garder le 50 km en priorité B.

## Limites de cet audit

- Aucun rétro-test : tout est simulé. Le modèle de semaines perdues est une hypothèse.
- Le « succès » (sortie de 5 h) est lui-même une convention ; les seuils de 4 h et 4 h 30 sont dans l'audit 01.
- Serveur réel non inspecté (réseau fermé) : politiques d'accès, pause du projet, réglage d'inscription **non vérifiés**.
- P-10 (signal de fatigue) et P-30 (plateau à 3 h) sont spécifiés, pas simulés. P-09 demande une borne avant d'être codée.
- Sources nouvelles : résumés relus, liens directs à compléter pour quatre d'entre elles avant d'entrer dans `SOURCES.md` ; `REGLES.md` n'a pas été relu ligne à ligne.

## Auto-vérification avant livraison

- Chiffres des rapports 01 et 02 recontrôlés contre `docs/audit/data/` : un écart corrigé (pertes groupées : « 11 à 26 points », pas « 16 à 26 »).
- Ma première série de simulations lisait le plan le lundi : elle subissait le défaut d'heure d'été. Refaite en lecture le mardi ; l'ancienne mesure est gardée comme chiffrage du défaut (66 % et 26 %).
- Numéros `D-97` à `D-121` et `H-59` à `H-66` : provisoires, libres au 11/11/2026, à attribuer à la validation.

## Rapports

| Fichier | Sujet | PR |
|---|---|---|
| `01-faisabilite.md` | Pré-mortem chiffré | #22 |
| `02-adversarial.md` | Invariants, cas A à M, corrections chiffrées | #23 |
| `03-charge-specificite.md` | CrossFit, descente, nutrition | #24 |
| `04-donnees.md` | Stockage, synchro, sauvegarde | #25 |
| `05-litterature.md` | Classement des 58 hypothèses, dose minimale, adhérence, mental | #26 |
| `06-coach-personnalise.md` | Note de décision | #27 |

Chaque PR part de la précédente : **fusionner la dernière (celle de cette synthèse) suffit**.
