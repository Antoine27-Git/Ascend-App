# PHOTO-WOD.md — Lecture de photo de séance (24/09/2026)

## Ce que ça fait
Sur une séance de renforcement, un champ « Photo du WOD » apparaît. La photo est
redimensionnée dans le téléphone (1024 px, JPEG), envoyée à une fonction Supabase, qui
appelle l'API Claude (modèle Haiku, rapide et bon marché) pour classer la séance. L'app
préremplit dominante, excentrique et impacts, affiche un résumé en une phrase, et le
message existant d'interférence avec la sortie longue s'applique automatiquement. Tout
reste éditable ; la photo elle-même n'est jamais conservée, seuls ces champs le sont.

Le message de conflit avec la sortie longue est maintenant gradué : jambes chargées
lourdement ou avec un excentrique fort → message fort ; sinon, jambes ou mixte → message
léger (« garde-la facile, raccourcis si besoin »).

## À faire une seule fois, de ton côté

1. **Récupérer une clé API Anthropic** : console.anthropic.com → Settings → API Keys.
   Garde-la secrète, ne la mets jamais dans `index.html`.
2. **Installer la CLI Supabase** si tu ne l'as pas : voir supabase.com/docs/guides/cli.
3. **Déployer la fonction** depuis le dossier qui contient `supabase/` :
   ```
   supabase functions deploy analyze-wod --project-ref amvvpiwemrpbvezvetih
   supabase secrets set ANTHROPIC_API_KEY=sk-ant-... --project-ref amvvpiwemrpbvezvetih
   ```
4. Rien d'autre : la fonction exige par défaut un utilisateur connecté (`verify_jwt`).
   C'est volontaire — c'est ton garde-fou de coût. Il faut donc être connecté dans
   l'app (Profil → Sauvegarde en ligne) pour que la lecture de photo fonctionne ; en
   local seul, l'app te le dit et n'appelle rien.

## Limites connues
- Le modèle peut se tromper sur une photo floue ou un WOD écrit à la main peu lisible ;
  la « confiance » affichée (basse/moyenne/haute) te le signale, jamais silencieusement.
- La classification ne remplace pas ton ressenti (RPE) : c'est toujours lui qui pilote
  la fatigue dans le moteur, pas la lecture de la photo.
- Chaque appel a un coût (quelques centièmes de centime avec Haiku). Pas de limite de
  fréquence codée pour l'instant : à ajouter si besoin plus tard (ex. 1 appel par séance).

## Fichiers livrés
- `index.html`, `sw.js` — app mise à jour.
- `supabase/functions/analyze-wod/index.ts` — la fonction à déployer.
- `tests/engine.js`, `tests/parity.py` — inchangés, toujours à 0 écart avec `sim8.py`.
