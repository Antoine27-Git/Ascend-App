# AGENTS.md — Ascend (application d'entraînement trail)

Lis ce fichier en entier avant de toucher au code. Il vaut pour tout assistant de code (Claude Code, Codex, autre).

## Le projet
- **Ascend** : PWA d'entraînement pour préparer un ultra-trail (objectif principal) et des courses intermédiaires. Elle génère un plan à rebours depuis la date de course, le recalcule chaque jour à partir des séances réellement faites et du ressenti (RPE), et affiche un bilan à chaque changement de phase.
- **Utilisateur actuel : Antoine** (non développeur de métier). L'app se concentre sur lui au départ, mais **aucune règle ne doit être propre à lui** : tout passe par le profil (jours, objectifs, historique) et par la table `CONV` du moteur.
- **Échanges** : en français, concis. Antoine préfère être challengé plutôt que validé. Avant toute correction, comprends pourquoi le comportement actuel se produit. Si une demande contredit une décision de `docs/SPEC.md` ou de `docs/GABARIT-TRAIL.md`, dis-le avant de coder.

## Architecture
| Élément | Rôle |
|---|---|
| `index.html` | toute l'app (CSS, HTML, JavaScript, ~390 Ko), en un seul fichier |
| `sw.js` | service worker ; le numéro de version est dans `const C='ascend-vNN'` |
| `tests/engine.js` | **source unique du moteur de plan** (fonctions pures : profil + séances réalisées + date → plan) |
| `tools/build.py` | injecte `tests/engine.js` dans `index.html` (repères `ENGINE:BEGIN` / `ENGINE:END`) et recopie la version de `sw.js` |
| `tools/test.py` | lance toute la batterie de tests |
| `tests/` | `parity.py` (le moteur en règles v1 doit égaler `sim8.py`, 0 écart), `t_profils.js` (propriétés sur 9 profils), `t_steps.js` (déroulé = durée), `t_react3.js` (réaction au ressenti et aux séances manquées), `t_decal.js` (décalage dans la semaine), `t_prof.json` (profil de test) |
| `sim8.py`, `sim3.py`, `serie11.py` | simulateur de référence des règles v1 et séries historiques |
| `docs/` | décisions et doctrine (voir plus bas) |
| Hébergement | GitHub Pages ; connexion et synchronisation par **Supabase** (obligatoires) |
| Fonction `intervals-activities` (`supabase/functions/intervals-activities/index.ts`) | lit les activités d'intervals.icu (lecture seule, D-77) ; secret `INTERVALS_API_KEY` dans Supabase ; collée à la main dans l'éditeur du tableau de bord (pas de CLI) |
| Fonction `intervals-event` (`supabase/functions/intervals-event/index.ts`) | envoie / retire une séance prévue dans le calendrier intervals.icu (D-78) ; même secret, `external_id` = `ascend:<id>` |
| Fonction `analyze-wod` | lecture de photo de WOD, **pas déployée à ce jour** ; la clé API Anthropic ne doit exister que comme secret Supabase |

Écrans (v28, D-80) : Aujourd'hui (`vHome`), Semaine (`vSeances`), Suivi, Profil ; Journal (`vJour`, les autres jours) n'est plus un onglet.

Stockage navigateur : `trail-state-v1` (données), `trail-auth-v1` (session), `trail-sync-v1` (synchro).

## Règle d'or : ne jamais modifier le moteur dans index.html
1. Modifie `tests/engine.js`.
2. `python3 tools/build.py` (met à jour `index.html`).
3. `python3 tools/test.py` : tout doit être vert.
4. Avant un déploiement : `python3 tools/build.py --bump` (incrémente la version dans `sw.js` et `index.html`), puis tests, puis commit.
La ligne « Ascend vNN » en bas de Profil sert à vérifier qu'un déploiement est actif. Le reste de l'interface (hors bloc moteur) se modifie directement dans `index.html`.

## Moteur : ce qu'il faut savoir
- `build({profile, today, sessions, isRun, ...})` → `{weeks, sessions, garde, info, ecarts}`. Règles **v2** par défaut ; `regles:'v1'` rejoue l'ancien comportement (prouvé par `parity.py`). **Ne modifie pas le comportement v1** sans mettre à jour la parité et le dire.
- `CONV` (début du moteur) regroupe toutes les conventions réglables : sortie longue « moyenne » ≤ 3 h, samedi de week-end de choc, cibles d'objectif secondaire, nombre de week-ends de choc, seuil « course exigeante », plafond d'endurance par tranche d'objectif. Ajoute un paramètre là plutôt qu'un chiffre dans le code.
- Profil : `days` (jours de course, sortie longue, renforcement), `orgs` (organisation par phase), `orgHist` (versions passées : le passé ne se réécrit jamais), `phaseAck` (bilans acquittés), `manques` (raison d'une séance manquée : seule « fatigue » est un signal, D-72), `decal` (séance déplacée dans la semaine, D-73). Le champ `days.time` (temps disponible) est **ignoré en v2** (D-71) ; il n'existe plus dans l'interface.
- Le RPE pilote la fatigue, sur les **endurances seules** ; la FC est une observation secondaire (D-12).

## Décisions et documentation (sources de vérité)
- `docs/SPEC.md` : registre des décisions `D-xx` (dernières : D-66 à D-90). `docs/HYPOTHESES.md` : hypothèses `H-xx` avec portée, détectabilité, priorité. `docs/GABARIT-TRAIL.md` : doctrine d'entraînement (Uphill Athlete, Koop, 80/20, Roche). `docs/MOTEUR-V1.md` : journal de la refonte de septembre 2026. `docs/SOURCES.md`, `REGLES.md`, `SCHEMA.md`, `LEXIQUE.md`, `TESTS.md`, `ALLEGEMENT.md`, `PHOTO-WOD.md` : références.
- Toute nouvelle règle : une entrée `D-xx` dans SPEC.md (avec date et motif) ; si elle repose sur une extrapolation ou une convention de coach, une entrée `H-xx` et la mention « convention » ou « extrapolation » dans le message affiché. **Ne présente jamais une convention comme un résultat scientifique.**
- Preuve la plus solide du projet : règle des 30 jours (Frandsen et al., BJSM 2025 — une séance ne dépasse pas de plus de 10 % la plus longue des 30 derniers jours). Elle prime sur toute progression plus rapide.
- Ne renumérote jamais un identifiant existant. Vérifie qu'un `H-xx` n'est pas déjà utilisé (grep dans `docs/` et dans le moteur) avant d'en créer un.

## Principes produit
- **L'app recommande, l'utilisateur décide.** Elle ne déplace jamais ses jours sans lui.
- Le passé ne se réécrit pas (`orgHist`). Un jour ajouté démarre à son niveau, dans la règle des 30 jours.
- Une alerte d'écart dit la vraie cause (point de départ et temps restant), pas un levier inutile.
- Textes affichés : français, courts, lisibles sur téléphone.

## Sécurité
- Aucune clé secrète dans le dépôt. La clé Supabase `sb_publishable_…` de `index.html` est publique par conception ; jamais de `service_role` ni `sb_secret_…`, ni de clé Anthropic.
- La fonction `analyze-wod` exige un utilisateur connecté (garde-fou de coût).

## Tests d'interface (manuels)
`python3 tools/captures.py [AAAA-MM-JJ] [HH:MM]` produit des captures à 360 px de chaque onglet, d'une fiche et de la saisie dans `captures/` (à ne pas versionner) et échoue sur toute erreur JavaScript. Pour un scénario plus précis : Playwright + Chromium, ouvrir `index.html` en `file://`, préremplir `localStorage['trail-state-v1']` (profil de `tests/t_prof.json` avec `onboarded:true`, `planStart`) et `localStorage['trail-auth-v1']`, figer l'horloge avec `page.clock.set_fixed_time`, surveiller `pageerror`. L'écran de démarrage (`#splash`) masque la page pendant environ une seconde.

## Points ouverts connus
- Point de départ : seule la dernière sortie longue déclarée sert de repère (import complet de l'historique non fait).
- Signal de fatigue affiné (RPE attendu contre réel) : dépend du chantier « modèle allure-effort ».
- Bilan de phase : ne lit pas encore les commentaires de séance.
- Lecture de photo : fonction Supabase à déployer ; retirée du formulaire de renforcement (D-74), à reprendre avec le journal de progression.
- Idées reportées : `docs/BACKLOG.md`.
- `H-38` à `H-40` sont cités dans le moteur mais leur texte est introuvable dans `docs/` (à réintégrer depuis `MOTEUR-V0.md` s'il existe encore).
