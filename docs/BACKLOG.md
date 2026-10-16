# BACKLOG — idées gardées pour plus tard (Ascend)

Ce ne sont pas des décisions. Chaque idée sera rouverte, challengée et tranchée avant d'être codée.

## Journal de bord du renforcement (07/10/2026)
- **Besoin :** un utilisateur veut suivre sa progression en renforcement (charges, scores, reps), quel que soit le type : salle, maison, CrossFit, Hyrox, etc.
- **Principe :** le journal est séparé du moteur. Le moteur ne lit que la saisie minimale (durée, RPE, jambes sollicitées, D-74).
- **Activation :** un réglage du profil (désactivé par défaut), pas le type de séance.
- **Contenu possible :** exercices, charges, séries × reps, score de WOD, Rx/scaled, courbe de progression par exercice. Les anciens champs (wodName, score, lifts, wod) sont conservés dans les séances déjà saisies.
- **Photo (analyze-wod) :** le pré-remplissage du journal à partir d'une photo dépend de cette fonctionnalité.
- **Condition pour démarrer :** que le formulaire minimal soit en place et utilisé.

## Autres chantiers ouverts
- Import de l'historique complet (écart n° 5, partie restante).
- Signal de fatigue option C (RPE attendu vs RPE réel), qui dépend du modèle allure-effort.
- Lecture des commentaires de séance dans le bilan de phase.
- Déploiement de la fonction Supabase analyze-wod.
- Rétablir les textes de H-38, H-39 et H-40 dans HYPOTHESES.md.
- Liaison du Project avec GitHub.
- Option « malade ou douleur » pour une séance manquée, le jour où le moteur y réagit autrement que « fatigue » (D-72).
