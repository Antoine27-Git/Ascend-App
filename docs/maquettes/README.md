# Sources des maquettes

Scripts Python qui produisent les maquettes HTML/PNG montrées à Antoine avant chaque développement (`render.py` + `base.py` = moteur de rendu ; `screens_*.py` = un jeu d'écrans par sujet : prof5 à prof7 = Profil, obj3 à obj5 = Ton objectif, today = Aujourd'hui, rpe/res = saisie et résultat). Les PNG et HTML générés ne sont pas conservés : relancer `python3 render.py` pour les refaire.
Règle de travail : maquettes validées par Antoine avant de coder.

Exception : `screens_suivi.py` (Suivi en 3 questions, 17/10/2026) produit aussi `suivi.html` (page de comparaison des 4 variantes, interactive, à ouvrir sur téléphone) et `suivi/*.png` (une image par variante), conservés pour la relecture depuis GitHub. Données : profil reconstitué (`tests/ui/state.py`), semaine du 12/10 supposée.
