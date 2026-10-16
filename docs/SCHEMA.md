# SCHEMA.md — Schéma de données — Ascend

Écrit le 17/09/2026, dernier trou structurel avant de pouvoir coder quoi que ce soit.
Gouverné par A-04 (tout est recalculé de zéro), A-07 (stocké contre recalculé) et
R-MET-002 (interprétable, chaque valeur lisible).

---

## Le principe, et une distinction qu'il a fallu ajouter

A-07 dit : on stocke les séances brutes, on recalcule tout le reste. En le mettant en
œuvre, une contrainte apparaît qui n'avait pas été vue.

**Le problème.** Une trace GPS à 1 Hz produit 3 600 points par heure. Trois cents séances
par an, dont des sorties de plusieurs heures, représentent plusieurs millions de points.
Le stockage d'un navigateur ne l'absorbe pas confortablement, et recalculer depuis les
points bruts à chaque ouverture contredit le budget de A-14.

**La distinction à faire** — elle manquait, et elle est structurante :

| Dérivé de… | Exemple | Stockable ? |
|---|---|---|
| **du signal seul** — déterministe, sans aucun paramètre du modèle | découpage d'une trace en segments, pente moyenne, allure moyenne, écart-type de cadence | **oui** — le résultat ne changera jamais, quelle que soit l'évolution du modèle |
| **du modèle** — dépend d'un coefficient, d'un seuil ou d'une grandeur | %VC d'un segment, admissibilité au sens de D-49b, coût-pente, confiance, volume cible | **jamais** — recalculé, sinon A-13 (versionnement) est violé et un ancien coefficient survit en silence |

Un seuil de régularité qui change (H-01, D-49b) doit reclasser toutes les observations
passées. Il ne le peut que si la donnée stockée est **antérieure au seuil** — d'où le
stockage au niveau segment brut, et pas au niveau « segment admissible ».

**Conséquence** : on stocke une **normalisation par séance**, pas la trace complète ni
des valeurs de modèle. Environ 50 segments par séance, une dizaine de champs numériques
chacun — de l'ordre de quelques mégaoctets par an, compatible avec un stockage
navigateur. IndexedDB plutôt que localStorage si le volume dépasse les limites.

---

## Entités

### profil
Les neuf paramètres déclarés (D-17, D-38, D-47), plus les préférences.

| Champ | Type | Source |
|---|---|---|
| jours_course | liste de jours | D-38 |
| jour_sortie_longue | jour | D-37, doit appartenir à jours_course |
| jours_renforcement | liste de jours | D-38 |
| volume_actuel_h | nombre | D-17c, déduit de l'historique s'il existe |
| autres_activites | liste de {type: jambes/haut/mixte, frequence} | D-17d |
| acces_velo, acces_bassin | booléen | D-31 |
| terrain_dplus_max_m, terrain_frequence | nombre, énum | D-47, seulement si cible avec D+ |
| affichage_duree_ou_distance | énum | D-45 |
| modules_actifs | {nutrition, renforcement} booléens | D-30, D-31 |

### parcours
| Champ | Type | Source |
|---|---|---|
| id, nom | — | — |
| technicite | énum | D-07b, déclarée une fois par parcours |

### objectif
| Champ | Type | Source |
|---|---|---|
| id, date, mode | date, fixe/flexible | D-26 |
| statut | principal / secondaire / course-entrainement | D-24 |
| distance_km, dplus_m | nombre | D-17a |
| profil_etat | gpx_connu / gpx_inconnu / ambition | D-27 |
| profil_segments | liste de segments, si GPX | D-27 |

La **durée d'effort attendue** (D-44), qui indexe toutes les tranches, n'est **pas
stockée** : elle dépend de G-CAP-001 et G-TER-001, donc du modèle. Exception unique :
la **tranche figée à la création du plan** est stockée, parce que A-08 exige qu'elle ne
bascule pas d'elle-même — c'est une décision, pas une valeur dérivée.

### seance
Une ligne par séance, importée ou saisie.

| Champ | Type | Source |
|---|---|---|
| id, date, source | import / saisie | D-14 |
| type_activite | course / velo / natation / aquajogging / renforcement | D-31 |
| parcours_id | référence, optionnel | D-07b |
| duree_s, distance_m, dplus_m, ddenivele_neg_m | nombre | signal |
| capteur_fc | optique / ceinture / aucun | D-11, attribut par observation |
| statut | conforme / modifiee / remplacee / reprogrammee / non_realisee | D-43 |
| ressenti | 0-10, optionnel | G-RES-001 |
| rejetee_motif | texte, optionnel | A-15 — marquée, jamais supprimée |

### segment
Enfants d'une séance. **Dérivés du signal uniquement** : aucune valeur de modèle.

| Champ | Type |
|---|---|
| seance_id, ordre | — |
| duree_s, distance_m | nombre |
| pente_moyenne_pct, denivele_m | nombre |
| allure_moyenne_s_par_km | nombre |
| vam_m_par_h | nombre — utile au-delà du seuil de marche (D-40) |
| cadence_moyenne, cadence_ecart_type | nombre |
| allure_ecart_type | nombre — alimente le critère de régularité D-49b |
| marche_detectee | booléen — critère de signal (D-40) |
| fc_moyenne | nombre, optionnel |

L'**admissibilité** et la **pondération par régularité** (D-49b, H-01) ne sont pas
stockées : elles dépendent de seuils susceptibles de changer.

### nutrition
| Champ | Type | Source |
|---|---|---|
| seance_id, glucides_g_par_h, troubles_digestifs | — | G-NUT-001 |
| produit, note | texte | D-30, carnet hors modèle |

### gene
| Champ | Type | Source |
|---|---|---|
| seance_id ou date, localisation, intensite_0_10 | — | D-32 |
| moment | echauffement / pendant / apres / lendemain | D-32, D-51 |

### indisponibilite
| Champ | Type | Source |
|---|---|---|
| debut, fin, niveau | aucune_activite / course_facile_seulement | D-46 |

### blessure
| Champ | Type | Source |
|---|---|---|
| debut, active | — | D-50 |
| diagnostic_texte | texte | D-50 — **jamais lu par le modèle** |
| course_autorisee | non / avec_restrictions / sans_restriction | D-50 |
| reduction_volume_pct ou reduction_qualitative | nombre ou énum | D-50 |
| drapeaux | pas_d_intensite, pas_de_denivele, surface, duree_max_s | D-50 |
| substitutions_autorisees | liste | D-50 |
| date_reevaluation | date, optionnelle | D-50 — au-delà, retour au plus conservateur |
| remontee_palier | entier | D-51 |

### plan_publie
Le seul état dérivé qui soit stocké, et A-08 l'exige.

| Champ | Type | Source |
|---|---|---|
| date_publication, version_modele | — | A-13 |
| seances_fermes | liste de séances prescrites | A-09 |
| tranche_figee | énum | D-44 |
| niveau_garde_fou | vert / orange / rouge | D-19 |
| contraintes_cedees | liste | A-05, A-06, pour A-16 |

Les plans passés ne sont **jamais réécrits** (A-13) : ils gardent la version de modèle
qui les a produits.

---

## Ce qui n'est stocké nulle part

Tout ce qui se recalcule : les neuf grandeurs et leurs coefficients, les niveaux de
confiance, les états de convergence (D-49a), le %VC de chaque segment, l'admissibilité
et la pondération des segments, la date projetée (D-26), l'histogramme d'intensités
(D-34, ex-G-PLA-003), le volume cible (G-PLA-002), la structure de blocs.

**Test à appliquer à tout nouveau champ** : si une valeur peut changer parce qu'un
coefficient ou un seuil a changé, elle ne se stocke pas.

---

## Trous ouverts

| Sujet | État |
|---|---|
| Volume réel de stockage à mesurer sur des données véritables — l'estimation à quelques Mo par an n'est pas vérifiée | à mesurer |
| Choix localStorage / IndexedDB, à trancher une fois le volume mesuré | à trancher |
| Import : formats acceptés (GPX, FIT, TCX) et déduplication (A-15) | non traité |
| Export du journal de blessure (D-50) : format à définir | non traité |
