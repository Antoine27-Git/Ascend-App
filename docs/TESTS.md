# TESTS.md — Déroulé manuel des cas limites — Ascend

Première exécution le 17/09/2026. **Déroulé sur papier**, pas exécution de code : chaque
coureur fictif est passé décision par décision à travers le pipeline de A-01, et on note
ce que le modèle produit réellement. C'est le premier contrôle **externe** du modèle —
tous les précédents ne vérifiaient que sa cohérence interne.

Résultat : **trois défauts sérieux, deux mineurs.** Aucun n'avait été détecté par les
deux audits complets ni par la passe adverse.

---

## T-01 — Débutant complet, semi-marathon dans 6 mois — **ÉCHEC**

**Entrées** : aucun historique, volume actuel déclaré ≈ 0, cible < 2 h, 26 semaines
disponibles.

**Déroulé** : tranche < 2 h → préparation minimale 8 semaines, confortable 12 (D-21).
26 semaines → **vert sur la durée**. Puis le garde-fou teste le volume : volume de bloc
requis 4-5 h/semaine contre volume actuel ≈ 0 → **ratio infini → rouge** (D-19).

**Défaut** : le garde-fou refuse **tout débutant**, par construction. Pire, les deux
sorties de D-20 ne résolvent rien — repousser la date ne fait pas monter un volume actuel
qui reste nul tant qu'on ne s'entraîne pas, et réduire la distance ne change pas un ratio
infini. Le modèle refuse et ne propose rien qui fonctionne.

**Cause** : le critère est un **ratio**, indéfini à volume nul et explosif à volume
faible. Un coureur à 1 h/semaine visant 4 h est à 4× — rouge — alors que la progression
est parfaitement sûre sur 6 mois.

**Correction** : D-52.

## T-02 — Coureur route, 2 jours disponibles, marathon — **ÉCHEC**

**Entrées** : 2 jours de course par semaine (D-38), volume actuel 4 h, cible marathon
(tranche 2-4 h).

**Déroulé** : garde-fou vert (volume de bloc 5-7 h contre 4 h actuelles → ratio 1,25 à
1,75, donc vert à orange). Puis le gabarit doit poser 5-7 h sur 2 jours, une séance par
jour (D-35) : **2 h 30 à 3 h 30 par séance**, pour un marathonien. Absurde.

**Défaut** : le garde-fou teste le volume contre le **passé** du coureur, jamais contre
ce que sa semaine **permet**. Un coureur à 2 jours disponibles passe donc au vert, puis
reçoit un gabarit inapplicable. A-05 fait bien céder le volume (niveau 3) devant la
disponibilité (niveau 2), mais on obtient alors un volume très inférieur à ce que la
cible exige, **sans que rien ne le signale**.

**Correction** : D-52.

## T-03 — Blessure pendant le bloc spécifique, à 6 semaines de la cible — **ÉCHEC**

**Déroulé** : D-50 s'active, arrêt complet. Le garde-fou se rejoue (D-19 amendé) et passe
au rouge. En mode date fixe (D-26), la date est verrouillée et c'est la performance
estimée qui se dégrade.

**Défaut** : D-19 définit le rouge comme « refus », mais **le plan existe déjà**. Refuser
a posteriori n'a pas de sens, et rien ne dit ce que le modèle fait. Il continue donc de
dégrader une estimation de performance pour une course que le coureur ne devrait
peut-être pas prendre le départ — sans jamais le dire.

**Correction** : D-52.

## T-04 — Terrain très technique, peu de segments admissibles — **PASSE**

G-TER-001 pondère au lieu d'exclure depuis H-01 : la calibration ralentit sans
s'arrêter. G-CAP-001 reste à confiance basse faute d'efforts francs exploitables, donc
l'app reste en durées et efforts ressentis (D-42). Dégradation propre, comportement
conforme.

## T-05 — Remontée après blessure, aucune déclaration de symptôme — **PASSE, avec réserve**

La progression reste bloquée au palier courant (confirmation positive obligatoire, D-51).
Comportement sûr et conforme.

**Réserve mineure** : rien ne dit au coureur **pourquoi** il stagne. Un blocage silencieux
ressemble à une panne. À afficher : « en attente de ta confirmation d'absence de
symptôme ».

## T-06 — Modules nutrition et renforcement désactivés, cible 80 km — **PASSE, avec réserve**

Les deux se désactivent proprement (D-30, D-31), le plan reste entier.

**Réserve mineure, incohérence** : D-31 affiche une information unique au moment de
désactiver le renforcement, D-30 n'affiche rien pour la nutrition. Or désactiver la
nutrition sur une cible de plus de 4 h est au moins aussi conséquent. Traitement à
aligner.

---

## Ce que ce déroulé démontre sur la méthode

Les trois défauts sérieux partagent une propriété : **ils ne sont visibles qu'en faisant
tourner un cas concret de bout en bout**. Chaque décision impliquée est correcte
isolément — D-19 est cohérente, D-35 est cohérente, D-26 est cohérente. C'est leur
composition sur un cas réel qui échoue.

Aucun contrôle de cohérence interne ne pouvait les trouver. C'est la confirmation
empirique de ce qui était écrit en A-10 : le modèle est testable sur sa cohérence, pas sur
sa justesse — et la justesse ne se révèle qu'au contact d'un cas.

**À refaire après chaque chantier**, au même titre que l'audit complet.


---

# Deuxième série — simulation sur 52 semaines (`sim.py`)

Exécutée le 17/09/2026. Premier contrôle **dynamique** : les tests précédents étaient des
instantanés à la création du plan ; ici des coureurs synthétiques, **dont on connaît la
vérité**, vivent 52 semaines et on regarde si le modèle la retrouve.

## T-S1 — Le modèle retrouve-t-il un coût-pente qu'on lui a caché ? — **PASSE**

Coureur de montagne, écart individuel de ±15 % au générique, 4 séances/semaine.

| | erreur moyenne sur les 5 bandes |
|---|---|
| Courbe générique seule | 9,6 % |
| Modèle après 52 semaines | **0,3 %** |

La mécanique est saine : le modèle retrouve la déviation individuelle qu'on avait cachée.
C'est la validation la plus importante — elle porte sur la conception, pas sur les seuils.

**Correction d'évaluation au passage.** La première mesure donnait 7,5 % pour le modèle
contre 7,4 % pour le générique, soit aucun gain. L'erreur était dans l'évaluation, pas
dans le modèle : le coût-pente ne peut mesurer qu'un **rapport à l'allure du coureur sur
le plat**, et c'est précisément la grandeur utile pour prescrire. L'écart du coureur au
générique *sur le plat* appartient à la vitesse de référence (G-CAP-001), pas au
coût-pente. Comparer à une vérité exprimée en absolu reprochait au coût-pente une erreur
appartenant à une autre grandeur. **À retenir dans la spec** : coût-pente et vitesse de
référence ne sont séparables que si le premier est normalisé sur le plat.

## T-S2 — H-01, filtre binaire contre pondération — **la correction était nécessaire**

| Mode | Erreur moyenne | Confiance descente forte | Confiance montée forte |
|---|---|---|---|
| Filtre binaire (version initiale) | 5,0 % | **0,00** | 0,44 |
| Pondération (D-49b après H-01) | **0,3 %** | 1,00 | 1,00 |

Le filtre binaire ne calibre **jamais** la descente forte — confiance nulle après un an de
trail en montagne. Exactement le biais de sélection prévu par la passe adverse : les
bandes les plus irrégulières sont aussi celles qu'on cherche le plus à mesurer. La
pondération les récupère toutes.

## T-S3 — H-02, la boucle allure/coût — **DIVERGENCE CONFIRMÉE, sérieuse**

Coureur qui lève volontairement le pied de 15 % en montée (stratégie d'allure, pas
physiologie).

| | montée forte estimée | physiologie réelle | allure réellement produite |
|---|---|---|---|
| Sans boucle de prescription | 0,353 | 0,449 | 0,382 |
| **Avec boucle** | **0,106** | 0,449 | 0,382 |

Dérive semaine par semaine : S1 0,432 → S5 0,346 → S10 0,257 → S20 0,206 → S35 0,147 →
S52 0,106. **La boucle ne se stabilise pas, elle s'effondre.** Au bout d'un an, le modèle
prescrirait des montées quatre fois trop lentes.

Sans boucle, le modèle mesure bien l'allure réellement produite (0,353 contre 0,382
observé) — conforme à ce que H-02 annonçait : il mesure une allure réalisée, pas un coût
énergétique. C'est **la rétroaction** qui est destructrice, pas la mesure.

**Le garde-fou de H-02 (« calibrer sur les segments à haute intensité ») ne suffit pas** :
il réduit l'ampleur, il n'empêche pas la divergence, puisque le mécanisme est
multiplicatif à chaque cycle. Il faut une borne dure. → correction D-53.

## T-S4 — H-03, quand le seuil de 5 % déclare-t-il la convergence ? — **PASSE, avec une réserve grave**

Convergence atteinte entre la semaine 5 et la semaine 8 selon les bandes. Le critère
fonctionne et se déclenche vite.

**Réserve** : dans la première version de T-S1, l'estimation était **convergée sur les
cinq bandes alors qu'elle était encore fausse de 7,5 %**. Convergence ≠ justesse. Le
critère mesure la stabilité, pas l'exactitude — c'est exactement l'asymétrie décrite en
H-03 : « confiant et faux » ne coûte rien au modèle, seulement au coureur. Rien dans la
spec ne distingue aujourd'hui ces deux notions à l'affichage.

## T-S5 — Coureur route pur — **PASSE**

Après un an sur le plat : seule la bande plate est calibrée (confiance 1,00), les quatre
autres restent au générique avec une confiance nulle et ne sont jamais utilisées.
Dégénérescence propre, conforme à D-23 et à la décision de portée.


## T-S6 — La correction de H-02 fonctionne-t-elle ? — **elle a dû être corrigée elle-même**

Les bornes de D-53b implémentées puis testées, au lieu d'être écrites et supposées bonnes.

| Version | Divergence (montée forte, S1 → S52) | Effet sur un coureur sain |
|---|---|---|
| Sans bornes | 0,432 → **0,106** (effondrement) | 0,3 % d'erreur |
| Bornes, 1re version | 0,432 → 0,432 (arrêtée) | **8,1 % d'erreur** — cassé |
| Bornes, après correction | 0,432 → 0,315 (contenue) | **0,3 %** — intact |

**Ce que le test a révélé.** La première version gelait la calibration dès qu'une bande
dérivait dans le même sens plusieurs cycles de suite. Or une estimation qui part du
générique et rejoint la vérité **dérive aussi de façon monotone** pendant ses premières
semaines : rien ne la distinguait d'une divergence. Le gel frappait donc le coureur sain.

**Correction** : le gel n'est armé qu'**après une première convergence** (D-49a). Une
dérive qui reprend après stabilisation est suspecte ; une dérive initiale ne l'est pas.

**Limite qui demeure** : les bornes **contiennent** la divergence, elles ne la corrigent
pas. L'estimation se stabilise à 0,315 contre 0,382 d'allure réellement produite et 0,449
de physiologie. Le modèle cesse de s'effondrer ; il ne devient pas juste. Aucune mécanique
ne sait distinguer une stratégie d'allure d'un coût énergétique sans mesure externe.


---

# Troisième série — généralisation (`sim2.py`)

Exécutée le 17/09/2026. Le jeu précédent n'éprouvait qu'**un seul** coureur : montagne,
déviation ±15 %, progression +6 %/an, 4 séances/semaine. Rien ne disait que le modèle
tenait ailleurs, ni que les corrections de D-53b, calibrées sur ce cas unique, ne
cassaient pas les autres.

## Résultat d'ensemble — le modèle généralise

| Scénario | Générique | Modèle | Bandes calibrées |
|---|---|---|---|
| Débutant lent, déviation faible | 5,5 % | 0,3 % | 5/5 |
| Confirmé, déviation moyenne | 9,3 % | 0,3 % | 5/5 |
| Élite, déviation faible | 2,7 % | 0,1 % | 5/5 |
| Atypique, déviation forte (±35 %) | 20,6 % | 0,3 % | 5/5 |
| 2 séances/semaine | 11,5 % | 0,8 % | 5/5 |
| 6 séances/semaine | 1,0 % | 0,1 % | 5/5 |
| Foulée très irrégulière (bruit ×3) | 8,8 % | 1,2 % | 5/5 |
| Progression forte (+20 %/an) | 4,7 % | 0,5 % | 5/5 |
| **Régression (−10 %/an)** | 3,2 % | 0,3 % | 5/5 |
| Objectif trail vallonné | 7,1 % | 5,9 % | 3/5 |
| Préparation courte (12 semaines) | 11,9 % | 1,1 % | 5/5 |
| Préparation très courte (8 semaines) | 7,8 % | 0,8 % | 5/5 |
| Objectif route (terrain plat) | 5,2 % | 5,2 % | **1/5** |

Points notables : le modèle tient à **2 séances par semaine**, sur une préparation de
**8 semaines**, avec une **foulée très irrégulière**, et sur un coureur en **régression**
— aucun de ces cas n'avait été éprouvé.

**Le cas « route » n'est pas un échec** malgré un gain nul : une seule bande reçoit des
observations, les quatre autres restent au générique par construction (D-23). La mesure
de gain moyen n'a simplement aucun sens quand 4 bandes sur 5 sont non observées. Défaut
de l'indicateur, pas du modèle.

## Défaut 1 — la borne à ±30 % écrasait un coureur réellement atypique

Coureur à ±35 % de déviation : sa descente forte réelle (0,576 rapportée au plat) tombe
**sous la borne basse** (0,616). Le modèle la remontait de force, portant l'erreur de
0,3 % à **1,6 %**. La borne censée contenir une dérive pathologique punissait un coureur
simplement atypique.

**Correction testée** : la borne s'**élargit avec la confiance** — ±30 % à confiance
nulle, jusqu'à ±60 % à confiance pleine. Une bande peu observée reste tenue près du
prior ; une bande bien observée gagne le droit de s'en écarter. Même philosophie que tout
le reste : la contrainte générique se relâche à mesure que la preuve s'accumule.

**Résultat** : coureur atypique **libéré** (erreur revenue à 0,3 %).

**Compromis assumé, et il est réel** : la contention de la divergence se dégrade — la
boucle se stabilise à 0,180 au lieu de 0,315, contre 0,449 de physiologie. Elle reste
**arrêtée** (sans borne elle s'effondrait à 0,106 et continuait), mais à une valeur plus
fausse. On ne peut pas avoir les deux avec ce mécanisme : toute borne assez serrée pour
bien contenir la divergence écrase les coureurs atypiques, qui sont **le cas fréquent**,
tandis que la divergence suppose un comportement pathologique persistant. Arbitrage :
protéger le cas fréquent, contenir sans prétendre corriger, et **signaler**.

## Défaut 2 — H-02 n'est pas propre à la montée

Testé sur un coureur qui freine de 20 % en descente par appréhension : le modèle estime
0,828 contre 1,035 de physiologie réelle — il mesure exactement l'allure produite, comme
en montée. D-53 ne parlait que de la montée ; le phénomène est **symétrique** et concerne
toutes les bandes. En descente, il est même plus probable : l'appréhension y est
fréquente, alors qu'elle n'a pas d'équivalent au plat.


---

# Quatrième série — boucle de charge (`sim3.py`)

Exécutée le 17/09/2026. Les trois premières séries n'éprouvaient que le coût-pente. Le
volume cible, la cadence de relâche, le garde-fou et la séquence blessure n'avaient
**jamais tourné**. Coureur synthétique doté d'une **tolérance réelle** que le modèle
ignore : au-delà, le ressenti monte et des séances sautent.

**Trois défauts, dont deux sérieux.**

## T-C1 — D-52a ne démarre jamais depuis zéro — **BUG CONFIRMÉ**

| Volume de départ | Multiplicatif seul (+20 %/sem) | Avec pas absolu de 0,5 h |
|---|---|---|
| 0 h | **jamais** | 11 semaines |
| 0,5 h | 15 semaines | 10 semaines |
| 2 h | 7 semaines | 7 semaines |

D-52a avait remplacé le ratio par un « temps de progression nécessaire » pour régler le
cas du débutant. Mais une progression **multiplicative** partant de zéro reste à zéro :
le même cas échoue, autrement. Correction : la progression est le **maximum** d'un pas
multiplicatif et d'un pas absolu.

## T-C2 — Le volume cible dépassait la tolérance réelle et oscillait — **SÉRIEUX**

| Tolérance réelle | Volume final (avant) | Écart | Oscillation | Après correction | Écart | Oscillation |
|---|---|---|---|---|---|---|
| 6,0 h | 6,8 h | **+14 %** | **37 %** | 5,8 h | −3 % | 18 % |
| 9,0 h | 10,9 h | **+21 %** | 27 % | 9,3 h | +4 % | 18 % |
| 4,5 h | 5,2 h | **+15 %** | **38 %** | 4,8 h | +7 % | **1 %** |
| 11,0 h | 12,0 h | +9 % | 12 % | 12,0 h | +9 % | 12 % |

**Le défaut** : G-PLA-002 ne recule qu'**après** l'apparition des symptômes, puis remonte
au plein plafond jusqu'à les redéclencher. Il se stabilise donc **au-dessus** de la
tolérance réelle, avec des variations de 12 à 38 % d'une semaine à l'autre. Traduit en
clair : le modèle aurait prescrit en permanence un peu trop, et de façon erratique.

**Correction** : mémoire du **dernier niveau ayant déclenché un symptôme**, et
progression **freinée à son approche** au lieu de foncer au plafond. Le dépassement passe
de +9/+21 % à −3/+9 %, l'oscillation de 12-38 % à 1-18 %. Le cas à 11 h n'est pas
amélioré parce qu'il bute sur le plafond de pic (12 h), pas sur la tolérance.

## T-C3 — La cadence de relâche ne discrimine pas — **défaut de conception**

| | Avant correction | Après correction |
|---|---|---|
| Coureur fragile (tolérance 4,5 h) | 3,0 semaines entre relâches | 4,5 |
| Coureur solide (tolérance 9,0 h) | 3,4 | 4,0 |

Même après correction, la cadence **ne distingue pas** un coureur fragile d'un coureur
solide — elle est même légèrement plus longue chez le fragile.

**Ce que la simulation révèle, et ce n'est pas un bug** : G-PLA-001 et G-PLA-002 lisent
**les trois mêmes signaux**, et le volume les absorbe en premier. Une fois le volume
ajusté à sa tolérance, le coureur fragile encaisse **aussi bien** que le solide — il n'y
a plus rien à corriger pour la cadence. C'est physiologiquement logique, mais cela
signifie que **l'observation correctrice de G-PLA-001 ne corrige rien en pratique** :
elle échoue à son propre critère d'admission (case 3), qui était précisément ce qui la
rendait admissible plutôt que générique.

**À arbitrer** : fusionner G-PLA-001 dans G-PLA-002, ou lui donner un signal propre que
le volume n'absorbe pas.

## T-C4 — Blessure et remontée — **PASSE**

Arrêt complet de 6 semaines depuis 7,8 h/semaine. Cible de retour à 77,5 % = 6,0 h,
atteinte en **10 semaines** de remontée, paliers 0,4 → 0,8 → 1,2 → 1,6 → 2,1 → 2,7 →
3,5 → 4,6 → 5,9 → 7,7 h. Progression dans la fourchette de 10-30 % de S-BLE-003.

Sans aucune déclaration d'absence de symptôme, le volume reste **bloqué à 0,4 h** :
comportement conservateur conforme à la confirmation positive de D-51.


---

# Cinquième série — G-FAT-001 refondue (`sim4.py`)

Exécutée le 17/09/2026. La grandeur a changé entièrement (D-57a) : plus de %VC, plus de
découpage en tiers, comparaison à terrain égal dans la même sortie, deux valeurs en
sortie. **Jamais testée, ni avant ni après.** Coureur synthétique doté d'une vraie
durabilité — heure de décrochage et perte par heure connues.

## T-F1 — Une sortie unique ne suffit pas — **conforme à ce qui était écrit**

| Vérité | Estimé sur une sortie |
|---|---|
| décrochage 2,0 h, −10 %/h | 1,4 h, −9 %/h |
| décrochage 1,0 h, −20 %/h | 0,7 h, −20 %/h |
| décrochage 3,0 h, −6 %/h | aucune dégradation décelée |

L'ampleur est bien retrouvée, le moment du décrochage est bruité. Confirme la règle déjà
écrite : la grandeur se lit **en tendance**, jamais sur une sortie.

## T-F2 — En moyenne sur 10 sorties — **excellent**

Vérité : décrochage 2,0 h, −10 %/h. Estimé : **1,97 h, −9,9 %/h**. Dispersion du
décrochage de 1,4 à 2,5 h d'une sortie à l'autre — d'où la nécessité de la moyenne.

## T-F3 — Sortie point à point montante — **rejet propre**

Aucune bande présente tôt et tard : la sortie est écartée, aucune valeur inventée.
Conforme à D-57a.

## T-F4 — Le modèle inventait de la fatigue — **DÉFAUT SÉRIEUX, corrigé**

Coureur synthétique **sans aucune dégradation** (durabilité infinie).

| | Perte estimée (moyenne) | Étendue | Faux positifs |
|---|---|---|---|
| Avant correction | **−3,0 %/h** | −20,5 à +10,9 %/h | non mesuré |
| Après correction | +0,0 %/h | +0,0 à +0,0 | **0/10** |

**Cause** : la recherche d'un point de rupture en trouve **toujours** un, y compris dans
du bruit pur. Sur une sortie isolée, le modèle pouvait annoncer −20 %/h à un coureur
parfaitement frais — et ce chiffre alimente le plafond systémique (D-33), donc aurait fait
baisser le volume sans raison.

**Correction** : test d'hypothèse nulle. Le modèle « dégradation » n'est retenu que s'il
explique nettement mieux les données que le modèle « aucune dégradation » (gain d'erreur
minimal exigé), et si l'ampleur dépasse un plancher. Sinon il répond **« aucune
dégradation décelée »** — réponse légitime, et non une valeur inventée.

## T-F5 — Suivi d'une progression sur 6 mois — **PASSE**

Décrochage reculant de 0,25 h par mois, 6 sorties de 5 h par point de mesure :

| Mois | Décrochage réel | Estimé |
|---|---|---|
| 0 | 1,50 h | 1,53 h |
| 2 | 2,00 h | 1,87 h |
| 4 | 2,50 h | 2,18 h |
| 6 | 3,00 h | 2,95 h |

La tendance est suivie, avec une légère sous-estimation au milieu. Toutes les sorties sont
exploitables sur une boucle vallonnée.


---

# Sixième série — modèle complet, huit profils (`sim5.py`)

Exécutée le 20/09/2026. Toutes les mécaniques branchées ensemble, sur huit coureurs très
différents — débutants route et trail, coureur du dimanche, lambda route et trail,
expérimenté, très expérimenté ultra, reprise après coupure. Chacun porte une vérité
complète et connue.

## Résultats finaux

**Coût-pente** — gain moyen +5,8 points, aucun profil en échec.

| Profil | Générique | Modèle | Bandes calibrées |
|---|---|---|---|
| débutant route | 4,4 % | 4,4 % | 1/5 |
| débutant trail | 14,3 % | 7,2 % | 3/5 |
| coureur du dimanche | 8,3 % | 2,8 % | 3/5 |
| coureur lambda route | 5,1 % | 5,1 % | 1/5 |
| coureur lambda trail | 9,4 % | **0,5 %** | 5/5 |
| expérimenté trail | 7,1 % | **0,5 %** | 5/5 |
| très expérimenté ultra | 14,6 % | **0,4 %** | 5/5 |
| reprise après coupure | 12,6 % | 8,3 % | 3/5 |

Les profils route n'ont aucun gain : une seule bande observée, les autres restent au
générique. Dégénérescence conforme, pas un échec.

**Volume** — écart moyen **7,6 %**, pire cas 11,0 % ; oscillation moyenne **14,6 %**.
En début de séance ces chiffres étaient de 14,9 % et 17,9 %, avec un pire cas à −23 %.

**Durabilité** — 79 sorties exploitables sur 80. Erreur de 1 à 15 % sur l'ampleur, de 3 à
25 % sur le moment du décrochage.

## Trois défauts trouvés et corrigés

**V1 — Le volume restait bloqué 43 % sous la tolérance réelle.** Un coureur de tolérance
9 h se voyait prescrire 5,1 h indéfiniment. Deux causes, de la même famille — **une
observation unique décidait de tout** :
- la référence de ressenti était figée sur la **première semaine**, bruitée. Si cette
  semaine tombait bas, toutes les suivantes ressemblaient à une dérive et la progression
  était bloquée dans une zone morte permanente. Corrigé : médiane des quatre premières
  semaines ;
- le niveau ayant déclenché un symptôme verrouillait la progression **à vie**. Corrigé
  par un desserrage périodique déjà présent, désormais effectif.

C'est la règle « une sortie ne dit rien », appliquée partout ailleurs et jamais ici.

**V2 — Une correction a d'abord empiré les choses.** Exiger **deux** symptômes avant de
mémoriser un niveau a porté l'oscillation de 18 % à **43 %** : le modèle dépassait bien
plus avant de freiner. Revenue à la mémorisation au premier symptôme, le risque de
verrouillage étant traité par le desserrage et non par la confirmation.

**V3 — L'oscillation venait d'une remontée trop brutale.** Après chaque recul, le modèle
repartait au plein cap de progression. Deux correctifs : recul adouci de −12 % à −8 %, et
progression plafonnée à la moitié du cap une fois la limite connue. Oscillation moyenne
ramenée de 23 % à **14,6 %**, écart de 10 % à **7,6 %**.

## Un lissage testé puis écarté

Lisser le volume prescrit sur trois semaines ne gagne que 2,8 points d'oscillation
(20,5 % → 17,7 %) et **dégrade** légèrement la justesse. Écarté : le mécanisme ne paie
pas sa complexité. Les correctifs V3 font mieux, sans état supplémentaire.

## Tentative supplémentaire — anticipation sur la tendance : testée, rejetée

Diagnostic du 20/09/2026 : le mécanisme réel derrière l'oscillation n'est pas un verrou
mais un **retard de signal**. Le ressenti monte progressivement plusieurs semaines avant
de franchir le seuil de correction (0,12) ; le volume continue de grimper pendant ce
temps, puis corrige en retard — en dépassant vers le bas. Diagnostic confirmé sur un cas
tracé semaine par semaine (tolérance 11 h : le volume grimpe à 13,3 h avant que le
ressenti dépasse le seuil, puis chute à 11,2 h).

**Piste testée** : ralentir de moitié la progression dès que le ressenti augmente trois
semaines de suite, même sous le seuil — anticiper plutôt que réagir. Sur les quatre cas
isolés déjà utilisés en T-C2, ça améliore trois cas sur quatre (oscillation moyenne
11,3 % contre 12,7 % auparavant sur ces cas).

**Rejetée en généralisation** : sur les huit profils du jeu 5, la moyenne **empire** —
14,6 % → **16,5 %**, avec un profil qui passe de 17,2 % à 26,4 %. Même leçon que sim2.py :
une amélioration mesurée sur un jeu de cas étroit peut échouer une fois généralisée.
**Un premier essai avait aussi révélé une seconde faute distincte** : le remplacement de
code correspondant avait échoué silencieusement (l'ancre textuelle ne correspondait plus
après des éditions précédentes), donnant de faux résultats identiques à la version
précédente — détecté par une vérification post-écriture systématique, désormais
appliquée à chaque modification du simulateur.

**Conclusion honnête** : l'oscillation résiduelle (14,6 % en moyenne, 34,5 % au pire cas)
n'est pas résolue par des correctifs locaux. C'est un problème de réglage d'un système à
rétroaction retardée — probablement du niveau d'un contrôleur proportionnel-intégral
correctement dimensionné plutôt que de règles ad hoc empilées. **Reste un point ouvert**,
à traiter comme un chantier propre plutôt que par petites touches.

## Un incident de méthode

Un de mes remplacements dans le simulateur a **échoué silencieusement** : j'avais affiché
un message de succès sans vérifier que l'ancre existait, et les résultats sont restés
identiques sans que j'en comprenne la cause. Corrigé en assertant chaque remplacement.
Même défaut que celui déjà rencontré sur SPEC.md — une opération doit échouer bruyamment.


---

# Septième série — calibration du contrôleur de volume (`controleur_pi.py`, `controleur_hybride.py`)

Reprise le 21/09/2026 de la piste laissée ouverte ci-dessus (essais 1 et 2, non aboutis).
Chantier mené en quatre temps : calibration par grille du PI, diagnostic de la cause
réelle de l'oscillation, tentative de contrôleur hybride avec mémoire, puis remise en
cause du protocole de mesure lui-même — qui s'est révélée être la vraie découverte.

## Calibration par grille du contrôleur PI

**Cause du biais de l'essai 2 (-33 %) identifiée : gains sous-dimensionnés d'un facteur
~10.** Près du point de fonctionnement, l'erreur typique (~0,08-0,12) multipliée par un
gain de 0,10 ne produit qu'une croissance de 0,8-1,2 %/semaine — largement insuffisant
pour rejoindre la tolérance en 40 semaines. Le mécanisme à paliers avance, lui, par pas
absolu de 0,5 h ou +20 % multiplicatif.

Grille de 600 combinaisons (Kp, Ki, cible, lissage) sur un balayage synthétique de
30 profils, validée sur les 8 profils réels du jeu 5 (tenus à l'écart de la grille) :

| | écart moyen | oscillation moyenne |
|---|---|---|
| Référence (paliers) | 7,6 % | 14,6 % |
| Meilleur PI trouvé (gains corrigés) | ~10-12 % | ~25-30 % |

**Ki n'apporte jamais de gain** : sur toute la grille, Ki=0 domine systématiquement.
Explication cohérente : la fatigue du coureur s'accumule déjà comme un intégrateur
(D-33/D-56) ; ajouter un terme intégral construit un système à deux intégrateurs, plus
instable — cohérent avec le symptôme « amplifie le bruit » de l'essai 1. **À ne pas
retenter sans nouvelle piste.**

**Cause de l'oscillation retracée précisément, pas seulement supposée** : ce n'est pas un
problème de réglage. Tracé semaine par semaine (tolérance 4,5 h) : le volume grimpe à
rythme quasi constant jusqu'à 37 % au-dessus de la tolérance *avant* que le signal ne
bondisse — le retard de détection, pas le bruit. Un contrôleur sans mémoire ne peut pas
l'anticiper.

## Contrôleur hybride (ajustement continu + mémoire du seuil)

Hypothèse testée : réintroduire la mémoire du dernier niveau ayant déclenché un symptôme
(comme le mécanisme à paliers), mais avec un freinage continu plutôt qu'à paliers.

**Corrige le point faible identifié en D-61g** : le profil « très expérimenté ultra »
passe de 34,5 % à 10-18 % d'oscillation.

**Mais dégrade d'autres profils.** Sans borne sur l'ampleur du recul, la correction est
proportionnelle à la taille du dépassement (jusqu'à -25 % en un coup, contre le -8 % fixe
du mécanisme actuel) — « reprise après coupure » passe de 13,1 % à 27,4 %. Un recul borné
(`recul_max`) répare ce cas (retour à 13-16 %) mais déplace le problème vers « coureur
lambda trail » et « expérimenté trail » (14-17 % → 23-36 %).

**Sur deux grilles complètes (900+ combinaisons), aucun réglage global ne bat la
référence sur tous les profils à la fois.** Régler pour l'un dégrade l'autre — un jeu à
somme nulle.

**Coût de complexité, sans gain net.** Pour égaler (sans dépasser) le mécanisme actuel,
le contrôleur hybride nécessite 9 paramètres (Kp, cible, lissage, seuil d'alerte,
cycles/taux de desserrage, semaines/taux de retest, recul max) contre ~6 pour le
mécanisme à paliers. **Écarté au nom de R-MET-002** (« chercher d'abord la solution la
plus simple, et ne complexifier qu'une fois la simple démontrée insuffisante ») : la
sophistication ne produit aucun gain mesuré.

## Le vrai problème n'était pas le profil ultra — c'était le protocole de mesure

**Preuve par invariance d'échelle.** Avec la graine 106 (celle du profil ultra dans le
jeu 5) fixée et la tolérance variable de 4,5 h à 15 h, l'oscillation reste **identique à
34,5 %** — la mécanique du modèle est proportionnelle, donc scale-invariante. Ce n'est
pas la tolérance élevée qui cause l'oscillation : c'est cette graine précise, et elle
produirait le même résultat pour n'importe quel autre profil.

**Sur 1 600 simulations (200 graines × 8 profils)**, la distribution d'oscillation est la
même pour tous les profils, indépendamment de la tolérance :

| Statistique | Ancien protocole (1 tirage/profil) | Nouveau protocole (200 tirages/profil) |
|---|---|---|
| Moyenne | 14,6 % | **12,3 %** (même statistique — écart dû au petit échantillon d'origine) |
| Médiane | — | 10,5 % (statistique différente : reflète l'asymétrie de la distribution, pas une correction du chiffre ci-dessus) |
| Rang du « pire cas » 34,5 % | — | **99,5ᵉ percentile** |

**Décomposition du 34,5 % lui-même** : tracé sur les 40 semaines, ce n'est pas un vrai
va-et-vient répété. C'est un seul accroc précoce (semaine ~8), suivi d'une remontée
prudente **encore en cours** à la semaine 40 (0 changement de sens sur la fenêtre de
mesure). Le calcul d'oscillation (écart pic-à-pic / moyenne) ne distingue pas « toujours
en train de converger » de « vrai yo-yo ».

**Classification sur les 1 600 simulations** : probabilité d'oscillation > 25 % =
**2,6 %**, uniforme sur tous les profils. Dont vrai yo-yo (≥2 changements de sens) :
**0,7 %**. Dont remontée/descente encore en cours (0 changement) : 1,7 %. Ambigu : 0,2 %.

**Conclusion** : il n'y a pas de « profil à problème » à isoler. L'oscillation forte est
un épisode aléatoire rare (<1 % de vrai yo-yo), touchant tout profil avec la même
probabilité, et se résorbant seul dans la majorité des cas. Une classification de
coureur (« mauvais profil ») pour le détecter est écartée : conceptuellement (l'épisode
n'est pas un trait stable, cf. D-14), et par le critère envisagé lui-même (un seuil « au-
dessus de la médiane » signale par construction 50 % de n'importe quelle population).

## Limite de périmètre découverte en clôturant : les blocs ne sont pas modélisés

**Point important, non résolu par ce chantier.** Toute cette investigation (essais 1-2,
PI calibré, hybride, diagnostic de bruit) simule G-PLA-002 seul, en continu sur
40 semaines, vers **une seule cible fixe** — aucune notion de fond / bloc spécifique /
pic / affûtage. D-21 confie bien la prescription réelle à G-PLA-002 en continu (les
repères de bloc ne sont que des « repères de structure », jamais des planchers), ce que
cette série valide indirectement. Mais rien ne garantit qu'un recul du ratchet ne tombe
pas, par hasard, juste au moment où le calendrier fait entrer le coureur en bloc
spécifique — l'app n'a aujourd'hui aucune conscience du calendrier de blocs pour
l'anticiper ou même le signaler. C'est le trou déjà listé dans SPEC.md (« Progression de
charge d'un bloc à l'autre ») — non créé par ce chantier, mais rendu plus concret et plus
prioritaire par lui.

## Conclusion honnête

Aucun changement de code sur G-PLA-002. Le mécanisme à paliers (D-56, D-57) reste en
l'état — c'est le meilleur mesuré à ce jour, avec ou sans contrôleur plus sophistiqué.
D-61g est requalifié (variance de bruit générale et rare, pas un point faible du profil
ultra). Le vrai chantier suivant n'est pas le contrôleur : c'est l'interaction, jamais
testée, entre G-PLA-002 et le calendrier de blocs.

# Huitième série — G-PLA-002 et calendrier de blocs (`sim6.py`, 22/09/2026)

**Traçabilité.** Une première version de cette série (nuit du 21 au 22/09/2026) a été
perdue avant livraison, simulateur compris. `sim6.py` a été reconstruit à partir du bilan
de cette nuit ; les chiffres ci-dessous sont ceux de la reconstruction. Deux affirmations
du bilan d'origine ne sont pas reproduites (D-63d et D-63h).

**Protocole.** Deux jeux de règles sur le même coureur et la même graine : AVANT (SPEC.md
avant D-63) et APRÈS (D-63). 7 profils × 500 tirages, préparation tirée entre 30 et 36
semaines ; 15 scénarios défavorables × 200 tirages.

| Mesure | AVANT | APRÈS |
|---|---|---|
| Séances > +10 % de la plus longue des 30 jours, par préparation | 3,1 à 6,4 | **0** |
| Sorties ≥ 3h20 dans le bloc, profil proche d'Antoine | 0 | **2,1** |
| Réduction de volume à l'affûtage | 38–40 % (**20 %** sur 8 semaines) | **45 %**, 100 % des plans dans 41–60 % |
| Semaine allégée tombant dans le pic | 76–85 % des plans | **5–9 %** |
| Sortie longue du bloc plus courte que celle du fond | jusqu'à 74 % | 0–6 % (sauf coureur à 2 séances, 51 %) |

**Défauts du simulateur trouvés et corrigés** (7) : historique antérieur compté comme
dépassement ; prévision des allégements différente de leur exécution ; rampe ignorant
l'arrondi ; arrondi à 5 min rendant la progression impossible sous 50 min ; sortie longue
plus courte que les autres séances à 2-3 séances par semaine ; G-PLA-002 montant sur un
volume non exécutable ; seuil mémorisé non mis à l'échelle à la reprise.

**Divergence tranchée.** Interruption de 5 semaines en fond : la reconstruction montrait
une **hausse** des symptômes en bloc (0,46 → 1,21), contraire au bilan. Cause : sans
seuil connu avant la coupure, le coureur reprenait doucement et ne retrouvait sa limite
qu'en bloc spécifique. Corrigé par le seuil provisoire de D-63h : 0,46 → 0,24.

**Re-vérification de D-61b.** Sur 1 600 tirages, écart moyen 11,3 % (médiane 8,9 %), pas
7,6 % : chiffre de petit échantillon, sans correction de code.

**Conclusion honnête.** Le résultat central tient : la règle des 30 jours élimine les
dépassements et rend les sorties clés atteignables. Mais la série n'a regardé que les
séances **isolées** — c'est ce qu'a révélé la neuvième.

# Neuvième série — poussée de D-63 (`sim7.py`, 22/09/2026)

**Protocole.** `sim7.py` étend `sim6.py` : affûtage de 3 semaines (8–20 h), objectif
secondaire avec son affûtage et sa récupération, paire de sorties longues, mesures
nouvelles — hausses composées sur 7 jours, sorties clés à la cible basse de D-22,
effondrement du volume (pic < 60 % de la tolérance), séances de moins de 30 min, semaines
à fatigue réelle > 0,3 et > 0,5. 23 scénarios (15 repris + 8 nouveaux : érosion lente
de tolérance, 80 km en 52 et 36 semaines, 80 km avec 50 km en objectif ou en
entraînement, paire activée, interruption de 8 semaines). Chaque mécanisme ajouté est
testé par **ablation** (retiré seul, tout le reste en place), 9 scénarios × 150 tirages.

**Défauts trouvés et corrigés** (dans le modèle, pas seulement le simulateur) :

| # | Défaut | Exemple observé | Correction | Effet mesuré |
|---|---|---|---|---|
| k1 | Hausses de +10 % enchaînées dans la même semaine | 95 → 125 min en 9 jours (+32 %) ; 4 à 15 fois par préparation | une seule séance de progression par semaine | hausses composées **0** partout ; semaines à fatigue > 0,3 : 0,61 → 0,10 sur le 80 km |
| k2 | Arrondi à 5 min mangeant la moitié du +10 % | 99 min affiché 95 | séance de progression affichée à la minute | cible atteinte 0,76 → 0,91 (Antoine) |
| k3 | Seuil figé sur un volume jamais couru | seuil 9 h pour une tolérance de 6,5 h | seuil et gel sur le volume exécuté | symptômes −9 à −11 % |
| k4 | Spirale de fausses alertes | 7 alertes, volume 2,4 h pour 6,3 h de tolérance | référence de ressenti recalée en semaine allégée | effondrements 0,07 → 0,01 (80 km) |
| k5 | Reprise bloquée à 30 min après > 30 jours d'arrêt | cible 0 % après 5 semaines d'arrêt | référence de reprise 30 jours | cible 0 → 0,83 (expérimenté) |
| k6 | Niveau atteint trop tôt sorti de la fenêtre | 3h15 en S20, puis retour à 2h | entretien du niveau nécessaire, marge 3 semaines | interruption 3 sem en fond : 0,34 → 0,60 |
| k7 | Affûtage 8–20 h limité à 14 jours | — | 70/55/40 sur 3 semaines | cible inchangée, dernière sortie longue à J-21 |
| k8 | Séances « autres » de 6 à 17 min à bas volume | 3 × 17 min + sortie longue | minimum 30 min, moins de séances | 9,6 → 0 séances courtes (Antoine), sans coût |
| k9 | L'entretien entretenait la course | 4h45 puis 4h50 deux semaines de suite après un 50 km | entretien du niveau **nécessaire**, alternance D-22a | alternance respectée |
| k10 | Le plancher de 30 min servait de marche à la sortie longue | 18 → 30 → 33 min dans la même semaine | la sortie longue se réfère à l'historique d'avant la semaine | régression de k8 éliminée |

**Mécanismes challengés par ablation, et verdict.**
- **Référence de ressenti plafonnée à +5 %** : **aucun effet mesurable** (érosion 3,87 vs
  3,89 symptômes) et un petit coût sur le coureur hyper-réactif (cible 0,34 vs 0,37).
  **Conservée comme filet**, même statut que D-61f : elle protège d'un mode que le
  simulateur ne sait pas représenter (fatigue persistante après repos).
- **Réexamen des alertes dues au seul calage de référence** : +3 à +9 points de cible,
  effondrements divisés par deux, mais +8 à +14 % de symptômes et un peu plus de
  semaines fatiguées. Variante « avec preuve » (2 semaines saines) testée : proche de
  l'absence de réexamen, donc sans intérêt. **Conservé** : l'alerte a produit son effet
  immédiat (recul, semaine allégée) ; seule sa mémoire à long terme est corrigée.
- **Repli du coureur muet** : sans lui, un coureur qui ne saisit jamais son ressenti
  accumule 7 semaines de fatigue > 0,5 par préparation. **Indispensable.**
- **k1** : le retirer ramène 6 à 15 hausses composées et presque double les semaines
  fatiguées. **k2** : le retirer coûte 15 points de cible mais réduit les semaines
  fatiguées (0,28 → 0,13) — vrai compromis, tranché pour la cible (niveau encore
  inférieur à celui sans k1).

**Non-régression finale** (23 scénarios × 200 tirages, 3 séries de graines
indépendantes × 300 tirages sur les 7 profils) : **0 dépassement, 0 hausse composée,
0 valeur invalide, 100 % des affûtages dans 41–60 %**. Écart entre séries de graines :
≤ 0,03 sur l'atteinte de la cible, ≤ 0,07 symptôme.

**Résultats notables pour l'objectif d'Antoine** (profil hypothétique : 2,5 h/semaine au
départ, tolérance 6 h) :
- 80 km en 52 semaines : sortie clé ≥ 5 h atteinte dans **~80 %** des plans ; en 36
  semaines (durée minimale de D-21) : **1 %**. La rampe de sortie longue est le goulot.
- Avec un 50 km en **objectif** en S33 : **72 %** ; en **entraînement** (sans affûtage) :
  67 %, et la course dépasse toujours la règle des 30 jours — le garde-fou doit le dire.
- Paire de sorties longues : ne s'active pas à ce volume (jour 1 < 3h30).

**Limites qui demeurent.**
- La fatigue simulée ne dépend que du volume : le coût d'une sortie longue ou du D+
  n'est pas modélisé.
- L'objectif secondaire placé dans le bloc spécifique n'est pas traité par le simulateur :
  D-25(b) doit l'interdire à la planification.
- Un coureur parti de zéro garde quelques séances de moins de 30 min au démarrage (volume
  initial nul) : l'amorçage de G-PLA-002 depuis zéro reste à définir.
- Le coureur hyper-réactif (bruit de ressenti ×3) reste mal servi : effondrement dans
  50 % des plans, inchangé par cette série.

# Dixième série — garde-fou de saisie du ressenti (D-64, `sim7.py`, 22/09/2026)

**Question posée par Antoine.** Le repli de D-63 (le volume cesse de monter quand le
ressenti manque) est une décision interne du modèle : rien n'en informait le coureur.
Trois points à trancher : le compteur d'alerte se remet-il à zéro à la première note ou
reste-t-il cumulatif, que fait un rattrapage a posteriori, et comment relancer le
coureur.

**Ajout au simulateur.** `Coureur` accepte `taux_absence` (oubli aléatoire chaque
semaine) et `periode_absence` (motif régulier, une saisie toutes les k semaines) —
distincts de `muet` (jamais aucune saisie). Une fonction d'analyse en aval,
`alerte_ressenti`, rejoue la séquence de ressenti déjà produite pour simuler ce que
verrait le garde-fou (streak, relance espacée, rattrapage) **sans jamais modifier le
calcul du modèle** — cohérence directe avec la décision (c) de D-64 : le rattrapage
n'alimente jamais G-PLA-002.

**Résultat central : les deux compteurs (streak visible et proportion structurelle de
D-63) couvrent des cas disjoints**, profil proche d'Antoine, 300 tirages :

| Motif de saisie | Repli structurel (k4) | Alerte visible (streak 3) |
|---|---|---|
| 1 semaine sur 3, jamais 3 d'affilée | 299/300 | **0/300** |
| 1 semaine sur 4, exactement 3 d'affilée | 298/300 | 300/300 |
| Oubli aléatoire, 20 % des semaines | 48/300 | 50/300 |
| Oubli aléatoire, 33 % des semaines | 157/300 | 171/300 |

Le premier cas montre qu'un compteur unique aurait manqué le coureur qui note une
séance sur trois de façon régulière : jamais 3 d'affilée, donc jamais de notification,
alors que G-PLA-002 tourne quasiment aveugle 299 fois sur 300. C'est directement
l'argument qui a tranché la question d'Antoine en faveur de deux mécanismes distincts.

**Sensibilité au seuil** (oubli aléatoire à 15 %) : seuil 2 déclenche 0,6 semaine
d'alerte par préparation en moyenne, seuil 3 → 0,1, seuil 4 et 5 → 0. Le seuil de 3
reste sensible aux motifs réguliers (ci-dessus) tout en restant rare sur un oubli
occasionnel isolé — compromis retenu.

**Conclusion honnête.** Le rattrapage est simulé comme un retour à jour global, pas
séance par séance : suffisant pour trancher la question de conception, pas pour
calibrer un comportement fin. Aucune source externe sur ce point (produit, pas
physiologie) — niveau sans objet, cohérence interne uniquement.


# Onzième série — finalisation v1 (`sim8.py`, `serie11.py`, D-65, 23/09/2026)

**Protocole.** `sim8.py` = `sim7.py` + drapeaux v1 (par défaut inactifs : `sim8` reproduit
`sim7` à l'identique, vérifié). `v1()` active les règles retenues. `sim3.py` reconstruit
(absent des connaissances), validé en reproduisant la neuvième série. Tout se rejoue par
`python3 serie11.py [sec|amorce|bruit|arrondi|fatigue|nr]`.

## T-V1 — Objectif secondaire : placement × durée

80 km en 52 semaines (fond S1–S40, bloc S41–S49), profil proche d'Antoine, 100 tirages.

| Secondaire | sim7 | v1 (référence de reprise + rampe qui anticipe) |
|---|---|---|
| 2h30 en S33 | **0 %** | 73–77 % |
| 2h30 en S38 | **0 %** | 7 % (course-entraînement : 70 %) |
| 3h30 en S28 | **0 %** | 60 % |
| 50 km en S33 | 72 % | 78–80 % |
| ≥ 4h30, S12–S40 | 58–76 % | inchangé |

Budget D-25a : 10–13 %, jamais limitant. **Défaut** : une course plus courte que la
sortie longue, avec son affûtage et sa récupération, vide le maximum des 30 jours.

**Dans le bloc** (50 km en S42, coût de course compté, sortie longue ×1,5 au-delà de 2 h) :

| | Symptômes en bloc | Fatigue > 0,5 | Semaines de charge en bloc |
|---|---|---|---|
| Secondaire en fond (S33) | 0,36 | 0,69 | 7,0 / 9 |
| En bloc, traité | 0,43 | 0,01 | **4,7 / 9** |
| En bloc, non traité | **1,96** | **1,03** | 6,8 / 9 |

**Constat** : D-25b (6 semaines) laisse finir la récupération dans le bloc. Corrigé par
D-25 complétée.

## T-V2 — Amorçage depuis zéro

| Jours | sim7 : 5 premières semaines | v1 | Séances < 30 min |
|---|---|---|---|
| 3 | vide, vide, vide, vide, 6+12 min | 3 × 30 min dès S1 | 3,2 → **0** |
| 2 | vide ×4, 9+9 min | 2 × 30 min dès S1 | 4,9 → 0,2 |

Deux régressions du correctif trouvées et corrigées en cours de série : (1) la sortie longue
à 33 min faisait tomber les autres sous 30 min, retirées par D-63k8 → fréquence avant
durée ; (2) appliquée sans condition, la règle bridait la sortie longue des profils
normaux (course avancée : 0,86 → 0,67) → restreinte au régime d'amorçage (volume à moins
de 20 % du « tout au plancher »).

## T-V3 — Ressenti bruité (200 tirages)

| Variante | Effondrement (bruit ×3) | Fatigue > 0,5 (bruit ×3) | Fatigue > 0,5 (normal, chute −30 %) |
|---|---|---|---|
| sim7 | 0,50 | 0,15 | 0,04 |
| Seuil ∝ bruit, K = 2 | 0,10 | 1,38 | 0,97 |
| K = 2,5 | 0,06 | 1,94 | 2,27 |
| K = 2, bruit estimé au repos | 0,40 | 0,46 | 0,26 |
| Confirmation 2 semaines | 0,27 | 0,40 | 0,76 |

**Verdict** : aucune variante retenue — chacune échange un volume trop bas contre une
fatigue réelle plus haute, y compris chez le coureur normal. Détection du bruit (σ au
repos ≥ 0,10) : 70 % des coureurs à bruit ×3, 1 % à bruit normal, 38 % à bruit ×2.

## T-V4 — Arrondi

| Règle | Sortie clé 3h30 | Sortie clé 5 h | Pas de 50 à 110 min |
|---|---|---|---|
| D-63j + k2 | 91 % | 81 % | 10 |
| Antoine, sortie longue seule | **77 %** | 77 % | 11 |
| Antoine partout + minute au plafond (retenue) | 92 % | 80 % | 11 |

## T-V5 — Coût propre de la sortie longue et du D+ (150 tirages)

| Vérité simulée | 80 km : cible | sympt. bloc | fatigue > 0,5 | 4–8 h : cible |
|---|---|---|---|---|
| Volume seul | 0,82 | 0,36 | 0,00 | 0,87 |
| SL ×1,25 au-delà de 2 h | **0,27** | 0,34 | 0,00 | 0,87 |
| SL ×1,5 | **0,01** | 0,46 | 0,00 | 0,87 |
| D+ 1,1 fond / 1,3 bloc | 0,03 | 1,79 | 0,00 | 0,88 |
| + choc en entrée de bloc | 0,03 | **2,01** | **0,84** | 0,87 |
| D+ monté sur 8 sem. de fond | 0,00 | 0,61 | 0,00 | 0,51 |

**Lecture.** Sécurité tenue partout sauf au choc de D+. L'atteinte de la sortie clé de 5 h
dépend entièrement d'un coût que seul le coureur réel révélera. Le coût d'atteinte de la
rampe de D+ en fond (4–8 h : 0,88 → 0,51) est le prix de la sécurité dans cette vérité
simulée, pas une mesure : il vient de la tolérance plafonnée du profil.

## T-V6 — Non-régression v1

22 scénarios + 7 profils × 200 : **0 dépassement, 0 hausse composée, 0 valeur invalide,
100 % des affûtages dans 41–60 %**. Trois séries de graines × 300 (80 km, 80 km + 50 km,
80 km + 2h30) : écart ≤ 0,05.

**Conclusion honnête.** Le simulateur vérifie toujours la mécanique, pas la physiologie ;
T-V5 montre précisément où l'écart entre les deux compte. `controle_d61b` n'est plus
exécutable (dépend de `sim5.py`, absent).
