# Lancement « chemin qui grimpe » (prototype, 05/11/2026)

Inspiré de l'écran d'accueil de la Dacia d'Antoine (vidéo du 05/11) : relief en courbes de niveau survolé en 3D, chemin qui grimpe.
`relief.html` : prototype, 6 s (durée demandée par Antoine). Les images du logo et de « Reach your peak » sont remplacées par `__LOGO__` et `__TXT__` :
les recopier depuis `#splash` de `index.html` pour l'ouvrir. Rien n'est branché dans l'appli.

Déroulé (v2, retour d'Antoine : commencer par l'animation, finir sur le logo ; le chemin ne doit pas s'arrêter dans le vide) :
0–0,7 s le relief apparaît vu de haut ; 0,6–4,2 s la caméra descend et avance, le chemin doré grimpe jusqu'au vrai sommet du relief (courbes de niveau jusqu'au point le plus haut) ;
4,2–4,7 s halo au sommet ; 4,5–5,3 s le logo naît au sommet et prend sa place (position de l'écran de lancement, D-90) pendant que le relief s'efface ;
5,25–5,9 s « Reach your peak » ; fin sur le logo, puis fondu vers Aujourd'hui. Limite : sur Android, l'écran système (icône) s'affiche toujours avant la page.
Relief généré (gaussiennes + bruit), courbes par marching squares, projection en perspective sur un canvas 2D.
