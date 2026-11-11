# Audit 04 — Fiabilité des données

Audit du 11/11/2026, appli v54. Aucun code de l'appli modifié.

## Lectures retenues

- **Méthode** : lecture du code (`index.html` : persistance, synchro, export, restauration ; `sw.js` ; fonctions Supabase), puis **rejeu sur la vraie appli** dans Chrome sans écran, face à un faux serveur Supabase en mémoire (`tests/audit/sync_scenarios.py`). Aucun appel à ton vrai projet, aucune donnée réelle.
- **Hypothèse sur le serveur** : la table `trail_items` garde l'horodatage envoyé par le téléphone (pas de déclencheur). **Le schéma de la base et ses politiques d'accès ne sont pas dans le dépôt** : je ne peux ni le confirmer ni auditer l'isolation des données (R-SEC-002). Chaque scénario est donc joué deux fois, avec et sans horodatage par le serveur.
- Je n'ai pas pu interroger ton projet Supabase (réseau fermé ici) : ce qui touche au serveur réel est marqué **non vérifié**.

## 1. Résultat des scénarios

| # | Scénario | Attendu | Observé | Avec horodatage serveur |
|---|---|---|---|---|
| 1 | Données du navigateur effacées (ou nouveau téléphone), puis connexion | le profil du compte revient | **✗ Le profil du compte est écrasé par un profil vide**, sur le téléphone et sur le serveur. Les 5 séances reviennent. | ✗ identique |
| 2 | Séance saisie hors ligne sur B, synchronisée après une saisie de A | A la reçoit | ✓ | ✓ |
| 2b | Même chose, horloge de B en retard de 3 h | A la reçoit | **✗ A ne la reçoit jamais, sans message** | ✓ |
| 3 | Deux appareils modifient deux réglages différents du profil | les deux survivent | **✗ Le dernier à synchroniser écrase tout le profil** : une modification de 9 h, synchronisée à 11 h, efface celle de 10 h | ✗ identique |
| 4 | Restaurer une sauvegarde JSON de 2 séances sur un compte de 5 | les 3 autres restent sur le serveur | **✗ Les 3 séances sont supprimées sur le serveur, contenu effacé** ; aucune confirmation | ✗ identique |

Reproduire : `python3 tests/audit/sync_scenarios.py` (et `SERVEUR_HORODATE=1 …`).

## 2. Les cinq risques, classés

### R1 — Se connecter sur un navigateur vide efface le profil du compte (critique)

**Mécanisme.** Au démarrage, `boot()` appelle `markChanges()` avant toute connexion : le profil par défaut, absent du dernier état synchronisé (vide), est marqué « modifié maintenant ». À la connexion, `pull()` compare : la modification locale (maintenant) est plus récente que le profil du serveur, donc elle gagne ; `push()` envoie le profil vide.

**Ce qui est perdu** : objectif et date, jours, organisations par phase et leur historique, date de départ du plan, sortie de référence déclarée, raisons des séances manquées, décalages, bilans acquittés, réglages de nutrition. **Ce qui survit** : les séances, le journal quotidien (une ligne par identifiant).

**Pourquoi c'est ton risque n° 1.** Tu effaces souvent les données de navigation, et tu as déjà perdu ton historique une fois (hébergement précédent). Chaque effacement suivi d'une connexion rejoue ce scénario. Tu as redémarré « de zéro » le 02/11 : je ne peux pas dire si ce défaut y a contribué (non vérifié), mais il produit exactement ce symptôme (retour à l'écran de démarrage, séances présentes).

**En attendant une correction** : avant d'effacer les données du navigateur, **exporte le JSON** (Profil → Exporter). Après une reconnexion sur un navigateur vide, ne refais pas le parcours de démarrage : restaure le JSON.

### R2 — Le profil est un seul bloc : le dernier à synchroniser gagne (élevé si deux appareils)

`markChanges()` remet l'horodatage de toute modification en attente à « maintenant » à chaque appel (démarrage, enregistrement, synchro). La règle réelle n'est donc pas « la dernière modification gagne » mais « **le dernier appareil à synchroniser gagne** », et pour le profil entier. Une raison de manque saisie sur le téléphone hors réseau en montagne peut effacer un changement de jours fait le soir sur l'ordinateur, ou l'inverse. Aucun message.

Effet de bord utile : c'est ce qui fait passer le scénario 2 (l'horodatage devient celui de la synchro).

### R3 — Restaurer une sauvegarde supprime du serveur tout ce qui est plus récent (élevé, sur action de ta part)

`importJSON()` remplace l'état local, sans confirmation. La synchro lit ensuite toute séance absente de la sauvegarde comme une suppression volontaire et l'efface du serveur (contenu mis à vide). Il n'existe ni corbeille ni historique : la restauration d'un vieux fichier est irréversible sur tous les appareils.

### R4 — Le serveur n'est pas une sauvegarde (moyen)

- Il reproduit fidèlement les écrasements et les suppressions (R1 à R3) : aucune version antérieure n'est gardée.
- **Offre gratuite Supabase** : pas de sauvegarde automatique ; projet **mis en pause après une semaine d'inactivité**, restaurable depuis le tableau de bord pendant 90 jours selon la documentation lue le 11/11/2026 (une autre lecture d'octobre 2026 cite un an : à vérifier chez toi). Tu n'as presque pas utilisé l'appli en septembre et octobre : ton projet a pu être mis en pause (**non vérifié**). Pendant une pause, l'appli fonctionne en local et affiche « Échec » à la synchro.
- La seule vraie sauvegarde est l'**export JSON manuel**. Rien ne te le rappelle.

### R5 — Horloges et silences (faible à moyen)

- Horloge d'un appareil en retard : ses envois portent une date antérieure à la dernière lecture de l'autre, qui ne les voit jamais (scénario 2b). Un horodatage par le serveur corrige ce cas.
- `lsSet()` avale les erreurs d'écriture de l'état de synchro : si cet état est perdu, tout l'état local est remarqué « modifié maintenant » au prochain démarrage et écrase le serveur (même mécanisme que R1).
- Stockage refusé pour l'état principal : l'appli prévient (« Aucun stockage disponible ici : exporte un JSON »), une seule fois par session. Correct.
- Modifications en attente : elles ne vivent que dans le navigateur. Effacer les données avant de retrouver du réseau les perd.

## 3. Autres constats

| Sujet | Constat |
|---|---|
| **Fonctions `intervals-*`** | Une seule clé intervals.icu (la tienne) sert tout appelant ; la protection est « Verify JWT », qui accepte **tout compte connecté** au projet, pas seulement le tien. Si l'inscription est ouverte (l'appli a un écran de création de compte), toute personne inscrite peut lire tes activités et écrire dans ton calendrier intervals.icu. État du réglage d'inscription : **non vérifié**. À corriger avant toute ouverture, et dès maintenant si l'inscription est libre : vérifier l'identifiant de l'utilisateur dans la fonction. |
| Isolation des données | Repose sur les politiques du serveur (R-SEC-002), absentes du dépôt. Vérification à faire toi-même : `curl "https://<projet>.supabase.co/rest/v1/trail_items?select=kind&limit=1" -H "apikey: <clé publique>"` doit répondre `[]` ou une erreur d'autorisation. |
| Fichier unique | `index.html` (490 Ko) = toute l'appli. Le service worker sert la page du réseau d'abord, du cache sinon : hors ligne correct. Un déploiement cassé n'a pas de retour arrière automatique (le cache n'est utilisé que si le réseau échoue). La ligne « Ascend vNN » reste le bon contrôle. |
| Taille | Tout l'état dans une seule clé `trail-state-v1`. Ordre de grandeur estimé : 1 Ko par séance, limite usuelle de 5 Mo par site : pas un risque à ton échelle (**estimation**, non mesurée avec des traces jointes). |
| Export | JSON complet (état entier) et CSV des séances. Le JSON n'embarque pas l'état de synchro : normal. Aucun export daté automatique. |
| Vestige | `window.storage` (ancien hébergement en artefact) est encore testé en premier dans `storageGet` / `storageSet` : sans effet sur GitHub Pages, à retirer. |
| Passé recalculé | Le plan passé n'est pas stocké, il est recalculé (chantier « historique du plan », point 3 de CHANTIER-MOTEUR) : une perte de profil (R1) réécrit donc aussi le passé affiché. |

## 4. Ce qui est solide

- Les séances et le journal sont synchronisés ligne par ligne par identifiant : deux appareils qui ajoutent des séances différentes ne se marchent pas dessus (scénario 2).
- Hors ligne : l'appli garde une file d'attente, la renvoie au retour du réseau et toutes les 2 minutes.
- Session expirée : les modifications restent en attente, rien n'est perdu.
- Aucune clé secrète dans le dépôt ; la clé publique seule est dans `index.html` (conforme à AGENTS.md).
- Aucune erreur JavaScript pendant les scénarios.

## 5. Propositions (brouillons, `docs/audit/propositions.md`)

| # | Proposition | Priorité |
|---|---|---|
| P-23 | Connexion sur un état local vierge : **lire d'abord** le serveur, ne jamais marquer « modifié » un profil par défaut ; test `sync_scenarios.py` n° 1 au vert | **1 — avant toute autre évolution** |
| P-24 | Restauration : confirmation avec le compte (« 3 séances plus récentes seront supprimées »), export automatique de l'état courant avant, et fusion par défaut (remplacement en option) | **1** |
| P-25 | Profil : fusion par rubrique (objectif, jours, organisations, manques, décalages, bilans) au lieu d'un bloc ; horodatage à la modification, pas à la synchro | 2 |
| P-26 | Serveur : horodatage par déclencheur ; table d'historique (30 dernières versions du profil) ; **schéma et politiques versionnés** dans `supabase/schema.sql` | 2 |
| P-27 | Sauvegarde : rappel d'export mensuel et à chaque changement de phase ; date du dernier export affichée dans Profil | 2 |
| P-28 | Fonctions `intervals-*` : vérifier l'utilisateur ; fermer l'inscription tant que l'appli est personnelle | **1 si l'inscription est ouverte** |
| P-29 | Test : `sync_scenarios.py` dans `tools/test.py` une fois P-23 à P-25 codées (demande Playwright et Chrome) | 3 |

## Sources

- Code : `index.html` (`boot`, `markChanges`, `pull`, `push`, `doSync`, `importJSON`, `storageGet`, `storageSet`), `sw.js`, `supabase/functions/intervals-*/index.ts`.
- Pause des projets gratuits : https://supabase.com/docs/guides/platform/free-project-pausing ; sauvegardes par offre : https://supabase.com/pricing — lus le 11/11/2026.
- Scénarios : `tests/audit/sync_scenarios.py`, sortie dans `docs/audit/data/04-sync.txt`.
