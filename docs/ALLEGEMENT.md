# ALLEGEMENT.md — Revue d'allègement du modèle — Ascend

Faite le 20/09/2026, à la demande. Question posée à chaque élément : **qu'est-ce qui
casserait si on le retirait ?** Quand la réponse est « rien de mesurable », l'élément
sort.

Méthode : inventaire automatique des citations croisées dans SPEC.md, puis confrontation
aux résultats de simulation (TESTS.md, jeux 1 à 6). Les décisions d'allègement qui
suivent s'appuient sur des mesures, pas sur un jugement de style.

---

## État avant revue

| | Nombre |
|---|---|
| Décisions actives | 60 |
| Décisions abandonnées (identifiant conservé) | 3 |
| Grandeurs actives | 8 |
| Grandeurs rétrogradées ou abandonnées | 2 |
| Sections d'architecture | 16 |
| Sources | 30 |

**Le modèle a déjà maigri** : G-PLA-001 (cadence de relâche) supprimée faute de pouvoir
discriminer, G-PLA-003 (adhérence) rétrogradée en règle d'affichage, et une dépendance
retirée entre G-FAT-001 et G-TER-001.

---

## Allègements retenus

### A1 — Le gel sur dérive monotone (D-53b-ii) devient un filet, pas un mécanisme

**Mesure** : sur 8 profils × 5 bandes = 40 occasions, il s'est déclenché **0 fois**.

**Analyse** : il avait été conçu pour contenir la boucle de rétroaction de H-02. Or D-54
a supprimé cette boucle **à la source**, en retirant la prescription d'allure en pente.
Un mécanisme qui protège d'un scénario devenu impossible est du poids mort.

**Décision** : conservé mais **rétrogradé** — il ne protège plus la prescription
(supprimée) mais la voie d'information ouverte par D-59, où afficher une estimation peut
modifier le comportement. À réévaluer si cette voie est fermée autrement ; il sortira
alors complètement.

### A2 — Un seul mécanisme de régularité au lieu de deux

**Constat** : D-49b définit un filtre binaire (pour la FC) et H-01 a ajouté une
pondération (pour le coût-pente). Deux mécanismes sur le même critère.

**Mesure** : la pondération fait mieux partout (erreur 0,3 % contre 5,0 %, et le filtre
binaire ne calibre **jamais** la descente forte). Le filtre binaire n'est conservé que
pour la FC, qui est optionnelle et dont la fiabilité en trail est faible.

**Décision** : **un seul mécanisme, la pondération**. La FC devient un cas particulier —
elle exige simplement une pondération au-dessus d'un plancher élevé. Deux concepts
fusionnés en un, sans perte mesurée.

### A3 — Le lissage du volume prescrit : testé, écarté

**Mesure** : gain de 2,8 points d'oscillation (20,5 % → 17,7 %), et **dégradation** de la
justesse. Les correctifs de V3 (recul adouci, progression plafonnée après la première
limite) font mieux — 14,6 % — **sans état supplémentaire**.

**Décision** : non retenu. Consigné pour ne pas être reproposé.

### A4 — Séance étalon (D-55) et segment doublé (D-58) fusionnés

**Constat** : deux décisions, un seul objet — un repère volontaire placé par le coureur,
alimentant G-TER-002 et, pour le doublé, G-FAT-001. Mêmes règles (optionnel, jamais
appelé un test, toujours au même moment du cycle).

**Décision** : fusion sous un seul intitulé, **séances de repère**, avec deux variantes.
Une décision de moins, aucune règle perdue.

### A5 — D-06 absorbée par G-RES-001

**Constat** : D-06 (« un ressenti obligatoire par séance, global ») n'est citée nulle
part ailleurs et redit ce que G-RES-001 décrit déjà, plus précisément.

**Décision** : D-06 marquée absorbée, son identifiant conservé.

---

## Allègements examinés et **refusés**

### Erreur de méthode corrigée le 20/09/2026 — G-TER-002 n'aurait jamais dû apparaître ici

La première version de cette revue listait « supprimer G-TER-002 » comme option
**examinée** sur la base d'un critère mécanique (nombre de citations dans le texte). Faute
réelle : quelques échanges plus tôt, on avait établi qu'elle est la **seule observation
indépendante de l'estimation du modèle** — donc le seul détecteur possible de la boucle
H-02 — et tranché qu'elle était irremplaçable. Le compte de citations mesure combien de
fois un mot apparaît, pas si la chose compte. Faire réapparaître une question déjà close
sous forme de « conservée après examen » dilue les vraies décisions de cette revue dans du
bruit, et donne l'illusion qu'un doute légitime existait.

**Correction de méthode** : le critère mécanique sert à repérer des **candidats**, jamais
à statuer. Toute décision déjà prise ailleurs dans la conversation prévaut sans être
rejouée. Voir la vérification refaite ci-dessous.

### R2 — Supprimer G-NUT-001 (module optionnel, 6 citations)

Module désactivable, aucune autre grandeur n'en dépend — donc supprimable sans casse.
Mais c'est la seule grandeur qui traite un facteur d'échec majeur en ultra, et son coût
est de deux champs par séance longue. **Conservée.**

### R3 — Réduire le nombre de bandes de pente de 5 à 3

Mesure : sur les profils trail, les cinq bandes atteignent une confiance pleine en un an.
Réduire à trois perdrait la distinction montée douce / montée forte, qui porte tout
D-28 (spécificité du bloc). **Refusé.**

### R4 — Fusionner A-01 à A-16 en moins de sections

Trois sections ne sont jamais citées (A-01 pipeline, A-07 stockage, A-10 testabilité),
mais elles sont référencées **hors de SPEC.md** — SCHEMA.md s'appuie sur A-04 et A-07,
TESTS.md sur A-10 et A-11. L'inventaire des citations internes est ici trompeur.
**Refusé.**

---

## Ce qui reste le plus lourd, et pourquoi on le garde

| Élément | Coût | Justification |
|---|---|---|
| Le tableau des 19 éléments de chantier | historique, tous traités | trace de ce qui a été couvert ; le supprimer rendrait impossible de vérifier qu'on n'a rien oublié |
| Les motifs de correction inscrits dans chaque décision | verbosité | c'est ce qui a permis de détecter les régressions ; une décision sans son motif se ré-inverse au tour suivant |
| Les 3 décisions abandonnées | poids mort apparent | elles empêchent de reproposer des idées déjà écartées — cas survenu deux fois |

---

## Bilan

**4 allègements retenus, 4 refusés sur mesure.** Le modèle passe de 60 à 59 décisions
actives, de deux mécanismes de régularité à un, et n'a plus de mécanisme jamais déclenché
sans justification écrite.

**Le vrai gain n'est pas le volume de texte** — il est dans le nombre de mécanismes
indépendants à maintenir : 8 grandeurs, dont **2 seulement en chaîne de dépendance**
(vitesse de référence → coût-pente), contre 3 avant.
