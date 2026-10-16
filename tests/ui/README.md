# Tests d'interface (Playwright, 360 px)

Scripts écrits pendant le chantier UX (v25 à v35). `test_v28.py` est la base (profil de test, horloge figée, Supabase bloqué, routes de fonctions simulées) ; `test_v31` à `test_v35` la réutilisent par `exec`, donc **lancer depuis ce dossier** : `cd tests/ui && python3 test_v35.py`.
Les captures vont dans `captures/ui/` (ignoré par git). Le dernier script (`test_v35.py`) couvre le Profil, la roue de durée, la Semaine ; `t34b.py` / `t35m.py` sont des vérifications ciblées.
Prérequis : `pip install playwright` et Chromium. Chaque script échoue sur toute erreur JavaScript de la page.
Avant toute livraison : relancer au moins Semaine, fiche, saisie et Profil, et comparer les classes CSS ajoutées aux existantes (collision `.wl` en v32).
