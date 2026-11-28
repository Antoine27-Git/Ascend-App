# AGENTS.md — Ascend (application d'entraînement trail)

Lis ce fichier en entier avant de toucher au code. Il vaut pour tout assistant de code (Claude Code, Codex, autre).

## Le projet
- **Ascend** : PWA d'entraînement pour préparer un ultra-trail (objectif principal) et des courses intermédiaires. Elle génère un plan à rebours depuis la date de course, le recalcule chaque jour à partir des séances réellement faites et du ressenti (RPE), et affiche un bilan à chaque changement de phase.
- **Utilisateur actuel : Antoine** (non développeur de métier). L'app se concentre sur lui au départ, mais **aucune règle ne doit être propre à lui** : tout passe par le profil (jours, objectifs, historique) et par la table `CONV` du moteur.
- **Échanges** : en français, concis. Antoine préfère être challengé plutôt que validé. Avant toute correction, comprends pourquoi le comportement actuel se produit. Si une demande contredit une décision de `docs/SPEC.md` ou de `docs/GABARIT-TRAIL.md`, dis-le avant de coder.

## Architecture
| Élément | Rôle |
|---|---|
| `index.html` | toute l'app (CSS, HTML, JavaScript, ~553 Ko dont ~156 Ko d'images intégrées), en un seul fichier |
| `sw.js` | service worker ; le numéro de version est dans `const C='ascend-vNN'` |
| `tests/engine.js` | **source unique du moteur de plan** (fonctions pures : profil + séances réalisées + date → plan) |
| `tools/build.py` | injecte `tests/engine.js` dans `index.html` (repères `ENGINE:BEGIN` / `ENGINE:END`) et recopie la version de `sw.js` |
| `tools/test.py` | lance toute la batterie de tests |
| `tests/` | `t_profils.js` (propriétés sur 9 profils), `t_steps.js` (déroulé = durée), `t_react3.js` (réaction au ressenti et aux séances manquées), `t_decal.js` (décalage dans la semaine), `t_invariants.js` (invariants sur 120 scénarios tirés au hasard ; scripts d'audit dans `tests/audit/`, rapports dans `docs/audit/`), `t_reprise.js` (repère de reprise sans effet de seuil, D-94), `t_arrondi.js` (arrondi supérieur, D-96), `t_plafond.js` (un saut ne relève la référence que de +10 %, D-107), `t_prof.json` (profil de test) |
| `docs/` | décisions et doctrine (voir plus bas) |
| Hébergement | GitHub Pages ; connexion et synchronisation par **Supabase** (obligatoires) |
| Fonction `intervals-activities` (`supabase/functions/intervals-activities/index.ts`) | lit les activités d'intervals.icu (lecture seule, D-77) ; secret `INTERVALS_API_KEY` dans Supabase ; collée à la main dans l'éditeur du tableau de bord (pas de CLI) |
| Fonction `intervals-event` (`supabase/functions/intervals-event/index.ts`) | envoie / retire une séance prévue dans le calendrier intervals.icu (D-78) ; même secret, `external_id` = `ascend:<id>` |
| Fonction `analyze-session` (`supabase/functions/analyze-session/index.ts`) | rédige l'analyse d'une séance (D-99) à partir du bilan calculé par le moteur (`bilan`) ; secret `ANTHROPIC_API_KEY` ; ne modifie jamais le plan |
| Fonction `intervals-streams` (`supabase/functions/intervals-streams/index.ts`) | lit les données seconde par seconde d'une activité (temps, FC, distance, altitude ; pas la position à ce jour : Antoine a décidé le 15/11/2026 de lire le GPS pour les segments comparés, décision à écrire dans la spec de ce chantier) pour `flux()` (D-100) ; secret `INTERVALS_API_KEY` |

Écrans (v28, D-80) : Aujourd'hui (`vHome`), Semaine (`vSeances`), Suivi, Profil ; Journal (`vJour`, les autres jours) n'est plus un onglet.

Stockage navigateur : `trail-state-v1` (données), `trail-auth-v1` (session), `trail-sync-v1` (synchro).

## Règle d'or : ne jamais modifier le moteur dans index.html
1. Modifie `tests/engine.js`.
2. `python3 tools/build.py` (met à jour `index.html`).
3. `python3 tools/test.py` : tout doit être vert.
4. Avant un déploiement : `python3 tools/build.py --bump` (incrémente la version dans `sw.js` et `index.html`), puis tests, puis commit.
La ligne « Ascend vNN » en bas de Profil sert à vérifier qu'un déploiement est actif. Le reste de l'interface (hors bloc moteur) se modifie directement dans `index.html`.

## Moteur : ce qu'il faut savoir
- `build({profile, today, sessions, isRun, ...})` → `{weeks, sessions, garde, info, ecarts}`. Une seule série de règles (les règles v1 et leur preuve de parité avec `sim8.py` ont été retirées en v88).
- `CONV` (début du moteur) regroupe toutes les conventions réglables : sortie longue « moyenne » ≤ 3 h, samedi de week-end de choc, cibles d'objectif secondaire, nombre de week-ends de choc, seuil « course exigeante », plafond d'endurance par tranche d'objectif. Ajoute un paramètre là plutôt qu'un chiffre dans le code.
- Profil : `days` (jours de course, sortie longue, renforcement), `orgs` (organisation par phase), `orgHist` (versions passées : le passé ne se réécrit jamais), `phaseAck` (bilans acquittés), `manques` (raison d'une séance manquée : seule « fatigue » est un signal, D-72), `decal` (séance déplacée dans la semaine, D-73 ; échange de deux séances, D-97). Le champ `days.time` (temps disponible) est **ignoré en v2** (D-71) ; il n'existe plus dans l'interface.
- Le RPE pilote la fatigue, sur les **endurances seules** ; la FC est une observation secondaire (D-12).

## Décisions et documentation (sources de vérité)
- `docs/SPEC.md` : registre des décisions `D-xx` (dernières : D-66 à D-108 ; état en tête du fichier). `docs/HYPOTHESES.md` : hypothèses `H-xx` avec portée, détectabilité, priorité. `docs/GABARIT-TRAIL.md` : doctrine d'entraînement (Uphill Athlete, Koop, 80/20, Roche). `docs/MOTEUR-V1.md` : journal de la refonte de septembre 2026. `docs/SOURCES.md`, `REGLES.md`, `SCHEMA.md`, `LEXIQUE.md`, `TESTS.md`, `ALLEGEMENT.md`, `PHOTO-WOD.md` : références.
- Toute nouvelle règle : une entrée `D-xx` dans SPEC.md (avec date et motif) ; si elle repose sur une extrapolation ou une convention de coach, une entrée `H-xx` et la mention « convention » ou « extrapolation » dans le message affiché. **Ne présente jamais une convention comme un résultat scientifique.**
- Preuve la plus solide du projet : règle des 30 jours (Frandsen et al., BJSM 2025 — une séance ne dépasse pas de plus de 10 % la plus longue des 30 derniers jours). Elle prime sur toute progression plus rapide. **Tolérance D-96 (convention, v2)** : la séance de sortie longue qui bute sur cette limite est arrondie au multiple de 5 min supérieur dès 50 min (dépassement < 5 min, réglage `CONV.arrondiSup`) ; à dire comme une convention, jamais comme un résultat de l'étude.
- Ne renumérote jamais un identifiant existant. Vérifie qu'un `H-xx` n'est pas déjà utilisé (grep dans `docs/` et dans le moteur) avant d'en créer un.

## Principes produit
- **Saisie en 3 étapes (D-107)** : source (montre ou main), confirmation (mesures en lecture seule + « Ta perception »), bilan affiché tout de suite. L'analyse par IA n'est jamais lancée seule : uniquement par le bouton « Analyser la séance ».
- **Un saut n'est jamais récompensé (D-107, convention H-71)** : une séance réelle ne relève la référence des 30 jours que de +10 % au plus (`CONV.plafondSaut`) ; le bilan l'explique.
- **L'app recommande, l'utilisateur décide.** Elle ne déplace jamais ses jours sans lui.
- Le passé ne se réécrit pas (`orgHist`). Un jour ajouté démarre à son niveau, dans la règle des 30 jours.
- Une alerte d'écart dit la vraie cause (point de départ et temps restant), pas un levier inutile.
- Textes affichés : français, courts, lisibles sur téléphone.

## Règles du plan : chercher avant de proposer (demandé par Antoine le 14/11/2026)
Pour toute règle qui touche au plan : chercher d'abord les études et les pratiques de référence (ex. La Clinique du Coureur), citer les sources dans la spec, et étiqueter chaque élément : **étude**, **avis d'expert**, ou **non vérifié**. Ne jamais avancer une « habitude d'entraîneur » de mémoire.

## Sécurité
- Aucune clé secrète dans le dépôt. La clé Supabase `sb_publishable_…` de `index.html` est publique par conception ; jamais de `service_role` ni `sb_secret_…`, ni de clé Anthropic.
- Les fonctions `intervals-*` et `analyze-session` exigent un utilisateur connecté. Elles ne vérifient pas que c'est Antoine (proposition P-28 de l'audit, ouverte) : l'inscription Supabase doit rester fermée.

## Tests d'interface
`python3 tools/test.py --ui` lance aussi tous les tests `tests/ui/test_vNN.py` (Playwright, environ 8 min). À lancer avant chaque PR qui touche l'interface. Un test par version : `test_vNN.py`, captures dans `captures/ui/vNN/`.
`python3 tools/captures.py [AAAA-MM-JJ] [HH:MM]` produit des captures à 360 px de chaque onglet, d'une fiche et de la saisie dans `captures/` (à ne pas versionner) et échoue sur toute erreur JavaScript. Pour un scénario plus précis : Playwright + Chromium, ouvrir `index.html` en `file://`, préremplir `localStorage['trail-state-v1']` (profil de `tests/t_prof.json` avec `onboarded:true`, `planStart`) et `localStorage['trail-auth-v1']`, figer l'horloge avec `page.clock.set_fixed_time`, surveiller `pageerror`. L'écran de démarrage (`#splash`) masque la page pendant environ une seconde.

## Points ouverts connus
- Point de départ : seule la dernière sortie longue déclarée sert de repère (import complet de l'historique non fait).
- Signal de fatigue affiné (RPE attendu contre réel) : chantier « modèle allure-effort », **gelé jusqu'au 50 km** (16/11/2026).
- Bilan de phase : ne lit pas encore les commentaires de séance.
- Lecture de photo de WOD : **abandonnée** (16/11/2026), code et doc retirés au ménage du 25/11. Journal de renforcement : gelé.
- Idées reportées : `docs/BACKLOG.md`.
- Ordre des chantiers validé le 16/11/2026 et état des décisions : `docs/BACKLOG.md` et le tableau en tête de `docs/SPEC.md`.
