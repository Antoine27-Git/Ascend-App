# Sources des maquettes

Scripts Python qui produisent les maquettes HTML/PNG montrées à Antoine avant chaque développement (`render.py` + `base.py` = moteur de rendu ; `screens_*.py` = un jeu d'écrans par sujet : prof5 à prof7 = Profil, obj3 à obj5 = Ton objectif, today = Aujourd'hui, rpe/res = saisie et résultat). Les PNG et HTML générés ne sont pas conservés : relancer `python3 render.py` pour les refaire.
Règle de travail : maquettes validées par Antoine avant de coder.

`screens_suivi2.py` (D-92, 2e tour du Suivi, 17/10/2026) : même principe, produit `suivi2.html` et `suivi2/*.png` ; il réutilise `screens_suivi.py`.

`screens_suivi3.py` (3e tour, 03/11/2026, après essai de la v49) : réel face au plan à la date du jour ; produit `suivi3.html` et `suivi3/*.png`.
