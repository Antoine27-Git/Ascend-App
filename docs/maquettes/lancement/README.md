# Lancement « chemin qui grimpe » (prototype, 05/11/2026)

Inspiré de l'écran d'accueil de la Dacia d'Antoine (vidéo du 05/11) : relief en courbes de niveau survolé en 3D, chemin qui grimpe.
`relief.html` : prototype, 6 s (durée demandée par Antoine). Les images du logo et de « Reach your peak » sont remplacées par `__LOGO__` et `__TXT__` :
les recopier depuis `#splash` de `index.html` pour l'ouvrir. Rien n'est branché dans l'appli.

Déroulé : 0–0,8 s logo fixe (raccord avec l'écran d'Android, D-90) ; 0,8–1,6 s zoom et fondu du logo, le relief apparaît vu de haut ;
1,6–4,6 s la caméra descend et avance, le chemin doré grimpe jusqu'au sommet ; 4,8–5,5 s retour du logo et de « Reach your peak » ;
5,6–6 s fondu vers l'écran Aujourd'hui. Relief généré (gaussiennes + bruit), courbes par marching squares, projection en perspective sur un canvas 2D.
